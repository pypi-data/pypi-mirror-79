# ***************************************************************
# Copyright (c) 2020 Jittor. Authors: Dun Liang <randonlang@gmail.com>. All Rights Reserved.
# This file is subject to the terms and conditions defined in
# file 'LICENSE.txt', which is part of this source code package.
# ***************************************************************
import unittest
import jittor as jt
import numpy as np


class TestConcatOp(unittest.TestCase):
    def test_concat_op(self):
        def check(tmp, dim=0):
            res1 = jt.WIP_concat(tmp, dim=dim)
            res2 = jt.contrib.concat(tmp, dim=dim)
            assert (res1!=res2).data.sum()==0, "concat fail..."
        check([jt.array([[1],[2]]), jt.array([[2],[2]])])
        check([jt.array(np.array(range(24))).reshape((1,2,3,4)), jt.array(np.array(range(24))).reshape((1,2,3,4))])
        check([jt.array(np.array(range(120))).reshape((5,2,3,4)), jt.array(np.array(range(24))).reshape((1,2,3,4))])
        check([jt.array(np.array(range(5))).reshape((5,1)), jt.array(np.array(range(1))).reshape((1,1))])
        print('concat success...')

    @jt.flag_scope(use_cuda = 1)
    def test_concat_perf(self):
        def check(dim, size, backward=False):
            n = 64
            a = jt.random((n,n,n,n))
            a.sync()
            m = n // size
            arr = []
            for i in range(m):
                arr.append(a[(slice(None),)*dim + (slice(i*size,i*size+size),)])
            b = jt.contrib.concat(arr, dim)
            if backward:
                loss = b * a
                b = jt.grad(loss, a)
            with jt.profile_scope(1, 0) as rep:
                b.sync()
            # print(rep)
            i = rep[0].index("TotalTime")
            stime = 0
            for r in rep[1:]:
                stime += float(r[i])
            bw = 4*64**4*2*2 / stime
            # sizeof(float) * numel * (split and concat) * (read and write)
            print(f"{dim} {size} {stime/1e6}ms, {bw}GB/s")
            return bw
        ndim = 4
        splits = [1, 2, 4, 8, 16, 32, 64]
        m = len(splits)
        result = np.zeros((4, m))
        result_back = np.zeros((4, m))
        for i in range(ndim):
            for j in range(m):
                result[i,j] = check(i, splits[j])
                result_back[i,j] = check(i, splits[j], True)
        print(result.T)
        print(result_back.T)


if __name__ == "__main__":
    unittest.main()