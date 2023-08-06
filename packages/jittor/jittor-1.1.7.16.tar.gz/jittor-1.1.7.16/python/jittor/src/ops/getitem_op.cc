// ***************************************************************
// Copyright (c) 2020 Jittor. All Rights Reserved.
// Authors: Dun Liang <randonlang@gmail.com>. 
// This file is subject to the terms and conditions defined in
// file 'LICENSE.txt', which is part of this source code package.
// ***************************************************************
#include <cmath>
#include "var.h"
#include "ops/getitem_op.h"
#include "ops/op_register.h"

namespace jittor {

#ifndef JIT

GetitemOp::GetitemOp(Var* x, VarSlices&& slices)
    : vs(move(slices)) {
    flags.set(NodeFlags::_cpu);
    // flags.set(NodeFlags::_cuda);
    create_output(nullptr, x->dtype());
}

void GetitemOp::infer_slices(
    StackVector<>& __restrict__ i_to_vs, 
    StackVector<>& __restrict__ i_to_o,
    StackVector<>& __restrict__ out_shape
) {
    auto in = inputs().front();
    auto in_shape = in->shape;
    auto nin = in_shape.size();
    i_to_vs.n = i_to_o.n = nin;
    out_shape.n = 0;

    int vid = 0;
    first_oid_of_var = -1;
    var_dim = 0;
    for (int i=0; i<nin; i++) {
        auto& s = vs.slices[vid];
        if (vid >= vs.n) {
            // i i i 
            // | | |
            // v v v --> overflow
            // s s
            i_to_vs[i] = -1;
            i_to_o[i] = out_shape.size();
            out_shape.push_back(in_shape[i]);
        } else
        if (s.is_var()) {
            // i --> s ---> o
            //       + ---> o
            // var maybe multiple dims
            if (first_oid_of_var == -1) {
                for (int i=0; i<vs.n; i++)
                    if (vs.slices[i].is_var())
                        var_dim = std::max(var_dim, vs.slices[i].var->shape.size());
                first_oid_of_var = out_shape.size();
                for (int j=0; j<var_dim; j++) {
                    out_shape.push_back(1);
                }
            }
            i_to_vs[i] = vid++;
            i_to_o[i] = -1;
            auto iv = s.var;
            auto iv_shape = iv->shape;
            auto niv = iv_shape.size();
            for (int j=0; j<niv; j++) {
                auto iv_shape_j = iv_shape[niv-j-1];
                auto& out_shape_j = out_shape[first_oid_of_var+var_dim-j-1];
                if (out_shape_j == 1)
                    out_shape_j = iv_shape_j;
                else
                    ASSERT(out_shape_j == iv_shape_j || out_shape_j < 0 || iv_shape_j < 0)
                        << out_shape_j << iv_shape_j << out_shape;
            }
        } else
        if (s.is_ellipsis()) {
            auto remain_slice = vs.n-vid-1;
            auto remain_idims = nin-i;
            auto ellipsis_size = remain_idims - remain_slice;
            ASSERT(ellipsis_size>=0) << "NDims not match";
            for (int j=0; j<ellipsis_size; j++) {
                i_to_vs[i+j] = -1;
                i_to_o[i+j] = out_shape.size();
                out_shape.push_back(in_shape[i+j]);
            }
            vid ++;
            i += ellipsis_size-1;
        } else
        if (s.is_none()) {
            i--;
            out_shape.push_back(1);
            vid++;
            continue;
        } else
        if (s.is_int()) {
            i_to_vs[i] = vid++;
            i_to_o[i] = -1;
            auto in_shape_i = in_shape[i];
            auto& v = s.slice.start;
            if (v<0) v += in_shape_i;
            CHECK(v>=0 && v<in_shape_i) << "slice overflow, " << v << "not in [0,">>in_shape_i>>")";
        } else {
            // slice
            auto& slice = s.slice;
            auto in_shape_i = in_shape[i];
            auto out_shape_j = in_shape_i;
            if (slice.mask == 7) {
                // slice is a[::]
                // start, stop, step is not filled
                vid++;
                i_to_vs[i] = -1;
                i_to_o[i] = out_shape.size();
                out_shape.push_back(out_shape_j);
            } else {
                i_to_vs[i] = vid++;
                i_to_o[i] = out_shape.size();
                if (in_shape_i > 0) {
                    slice.fill(in_shape_i);
                    if (abs(slice.step) <= 1)
                        out_shape_j = (slice.stop - slice.start) * slice.step;
                    else if (slice.step>0)
                        out_shape_j = (slice.stop - slice.start - 1) / slice.step + 1;
                    else
                        out_shape_j = (slice.start - slice.stop - 1) / -slice.step + 1;
                    out_shape_j = std::max(0l, out_shape_j);
                }
                out_shape.push_back(out_shape_j);
            }
        }
    }
}

void GetitemOp::infer_shape() {
    auto in = inputs().front();
    auto out = outputs().front();
    auto in_shape = in->shape;
    auto nin = in_shape.size();

    StackVector<> i_to_vs(nin);
    StackVector<> i_to_o(nin);
    // shape return to use
    StackVector<> out_shape;
    infer_slices(i_to_vs, i_to_o, out_shape);

    // optimized shape (each dim is a loop var)
    StackVector<> o_shape;
    int fov = -1;
    for (int i=0; i<nin; i++) {
        auto& vid = i_to_vs[i];
        auto& oid = i_to_o[i];
        auto os = out_shape[oid];
        if (oid>=0) {
            if (vid==-1 && i && i_to_vs[i-1]<0) {
                vid = -2;
                o_shape.back() *= os;
            } else
                o_shape.push_back(os);
            oid = o_shape.size()-1;
        } else {
            auto& s = vs.slices[vid];
            if (s.is_var() && fov == -1) {
                fov = o_shape.size();
                for (int i=0; i<var_dim; i++)
                    o_shape.push_back(out_shape[first_oid_of_var+i]);
            }
        }
    }
    first_oid_of_var = fov;

    if (!out_shape.size()) out_shape.push_back(1);
    out->set_shape(out_shape.to_nano_vector());

    this->i_to_vs = i_to_vs.to_nano_vector();
    this->i_to_o = i_to_o.to_nano_vector();
    this->o_shape = o_shape.to_nano_vector();

    LOGvvvv << "\ni_to_vs:" << i_to_vs
        << "\ni_to_o:" << i_to_o
        << "\no_shape:" << o_shape;
}

VarPtr GetitemOp::grad(Var* out, Var* dout, Var* v, int v_index) {
    // TODO
    return nullptr;
}

void GetitemOp::jit_prepare() {
    auto in = inputs().front();
    int idim = i_to_vs.size();
    add_jit_define("Ti", in->dtype());
    add_jit_define("IDIM", JK::hex1(i_to_vs.size()));
    add_jit_define("ODIM", JK::hex1(o_shape.size()));
    if (first_oid_of_var>=0) {
        add_jit_define("FOV", JK::hex1(first_oid_of_var));
        add_jit_define("VD", JK::hex1(var_dim));
    }
    for (int i=0; i<idim; i++) {
        auto iv = i_to_vs[i];
        auto io = i_to_o[i];
        add_jit_define("IV", JK::hex1(i), JK::shex1(iv));
        add_jit_define("IO", JK::hex1(i), JK::shex1(io));
        auto& v = vs.slices[iv];
        if (iv>=0 && io==-1) {
            if (v.is_int()) {
                add_jit_define("VS", JK::hex1(i), "-1");
            } else {
                ASSERT(v.is_var());
                auto var = v.var;
                auto vshape = var->shape;
                auto vdim = vshape.size();
                int vsmask = 0;
                for (int j=0; j<vdim; j++) {
                    int k = first_oid_of_var+j+var_dim-vdim;
                    if (vshape[j] == o_shape[k])
                        vsmask |= 1<<(j+var_dim-vdim);
                }
                add_jit_define("VS", JK::hex1(i), JK::hex(vsmask));
                add_jit_define("VST", JK::hex1(i), var->dtype());
            }
        } else
        if (iv>=0 && io>=0) {
            ASSERT(v.is_slice());
            if (std::abs(v.slice.step) <= 1)
                add_jit_define("VS", JK::hex1(i), JK::shex1(v.slice.step));
            else
                add_jit_define("VS", JK::hex1(i), "0");
        }
    }
}

#else // JIT

#pragma GCC diagnostic ignored "-Wunused-variable"

void GetitemOp::jit_run() {
    auto in = inputs().front();
    auto out = outputs().front();

    @for(i, 0, ODIM, index_t oshape@i = o_shape[@i];)
    @if(ODIM>0,
        index_t ostride@{ODIM-1} = 1;
        @for(i, ODIM-2, -1, -1, index_t ostride@i = ostride@{i+1} * oshape@{i+1};)
    )
    Ti* op = out->ptr<Ti>();

    Ti* ip = in->ptr<Ti>();
    @for(i, 0, IDIM, index_t ishape@i = 
        @if(IV@i==-1,oshape@{IO@i},
        @if(IV@i==-2,1,in->shape[@i]));
    )
    index_t istride@{IDIM-1} = 1;
    @for(i, IDIM-2, -1, -1, index_t istride@i = istride@{i+1} * ishape@{i+1};)

    
    @for(i, 0, IDIM, 
        @if(IV@i>=0 && IO@i>=0, 
            index_t vstart@i = vs.slices[@{IV@i}].slice.start;
            index_t vstep@i = @if(VS@i==0,vs.slices[@{IV@i}].slice.step;,@{VS@i});
        )
    )
    
    @for(i, 0, IDIM, 
        @if(IV@i>=0 && IO@i<0, 
            @if(VS@i==-1,index_t vi@i = vs.slices[@{IV@i}].slice.start;);
        )
    )
    
    @for(i, 0, IDIM, 
        @if(IV@i>=0 && IO@i<0, 
            @if(VS@i>=0,
                index_t vs@i@@s@{VD-1} = 1;
                VST@i* vp@i = vs.slices[IV@i].var->ptr<VST@i>();
                @for(j,VD-2,-1,-1,index_t vs@i@@s@j = vs@i@@s@{j+1} * 
                    @if((VS@i>>(j+1))&1,oshape@{j+1+FOV},1);
                )
            );
        )
    )
    
    

    @for(d, 0, ODIM, for (index_t i@d=0; i@d < oshape@d; i@d++)) {
        index_t oid = 0 @for(d, 0, ODIM, + i@d * ostride@d);
        @for(d, 0, IDIM, index_t iid@d = 
            @if(IV@d==-1, i@{IO@d},
            @if(IV@d==-2, 0,
            @if(IO@d!=-1, (i@{IO@d}*vstep@d+vstart@d),
            @if(VS@d==-1, vi@d,
            @if(VS@d>=0,
                index_t(vp@d[0 @for(j,0,VD,@if((VS@d>>j)&1, + i@{j+FOV} * vs@d@@s@j,))])
            , ??? )))));
        )
        auto iid = 0 @for(d, 0, IDIM,  + iid@d * istride@d);
        op[oid] = ip[iid];
    }
}
#endif // JIT

} // jittor