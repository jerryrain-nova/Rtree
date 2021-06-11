import os
import psutil
from time import time
from sys import getsizeof
import numpy as np
import re


def reload(file):
    st = time()
    f = open(file, 'r')
    print(u'当前进程的内存使用: %.4f MB' % (psutil.Process(os.getpid()).memory_info().rss / 1024 / 1024))

    gl = [''] * 1000000

    def find_l(ipt, t):
        for i in range(t):
            if i == t-1:
                print(u'当前进程的内存使用: %.4f MB' % (psutil.Process(os.getpid()).memory_info().rss / 1024 / 1024))
                re = ipt.readline().strip()
                ipt.seek(0)
                return re
            ipt.readline()
    re = find_l(f, 100)
    gl[9999] = re
    re = find_l(f, 100)
    gl[9998] = re
    print(gl[9998:10000])
    print(u'当前进程的内存使用: %.4f MB' % (psutil.Process(os.getpid()).memory_info().rss / 1024 / 1024))

    print("gene_list memory = %.4f MB " % (getsizeof(gl) / 1024 / 1024))
    print("run time = ", time()-st, 's')


def main():
    file = "C:/Users/chenyujie/Desktop/Test/new_spatial_1kw.g_tmp"
    reload(file)


if __name__ == '__main__':
    main()