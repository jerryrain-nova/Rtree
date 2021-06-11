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

    gt = f.readlines()
    print(u'当前进程的内存使用: %.4f MB' % (psutil.Process(os.getpid()).memory_info().rss / 1024 / 1024))

    print("gene_list memory = %.4f MB " % (getsizeof(gt) / 1024 / 1024))
    print("run time = ", time()-st, 's')


def main():
    file = "C:/Users/chenyujie/Desktop/Test/new_spatial_1kw.g_tmp"
    reload(file)


if __name__ == '__main__':
    main()