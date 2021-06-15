import os
import psutil
from time import time
from sys import getsizeof
import numpy as np
import re


def reload(file):
    st = time()
    # f = open(file, 'r')
    print(u'当前进程的内存使用: %.4f MB' % (psutil.Process(os.getpid()).memory_info().rss / 1024 / 1024))

    def find_l(ipt, t):
        for i in range(t):
            if i == t-1:
                print(u'当前进程的内存使用: %.4f MB' % (psutil.Process(os.getpid()).memory_info().rss / 1024 / 1024))
                re = ipt.readline().strip()
                ipt.seek(0)
                return re
            ipt.readline()

    def list_r(ipt):

        gl = [''] * 1000000
        idx = 0
        print("gene memory = %.4f MB " % (getsizeof(gl) / 1024 / 1024))
        print(u'当前进程的内存使用: %.4f MB' % (psutil.Process(os.getpid()).memory_info().rss / 1024 / 1024))

        f = open(file, 'r')
        for i in range(len(gl)):
            gl[i] = f.readline().strip()
            print(u'当前进程的内存使用: %.4f MB' % (psutil.Process(os.getpid()).memory_info().rss / 1024 / 1024))
            # if i == len(gl) - 1:
            #     print(u'当前进程的内存使用: %.4f MB' % (psutil.Process(os.getpid()).memory_info().rss / 1024 / 1024))
        return gl

    gl = list_r(file)
    print(u'当前进程的内存使用: %.4f MB' % (psutil.Process(os.getpid()).memory_info().rss / 1024 / 1024))

    print("gene_list memory = %.4f MB " % (getsizeof(gl) / 1024 / 1024))
    print("run time = ", time()-st, 's')


def num_read(ipt):
    # yl = np.loadtxt(ipt, dtype=np.uint32, delimiter=',')
    # print(u'当前进程的内存使用: %.4f MB' % (psutil.Process(os.getpid()).memory_info().rss / 1024 / 1024))
    # print("y_list memory = %.4f MB " % (getsizeof(yl) / 1024 / 1024))

    f = open(ipt, 'r')
    yl = f.readline().strip().split(',')
    print(yl)


def main():
    file = "C:/Users/chenyujie/Desktop/Test/new_spatial_1kw.g_tmp"
    num_file = "C:/Users/chenyujie/Desktop/Test/new_spatial_1kw.y_tmp"
    # reload(file)
    num_read(num_file)


if __name__ == '__main__':
    main()