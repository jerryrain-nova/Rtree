import numpy as np
import psutil
from sys import getsizeof
from sys import getrefcount
import os
import gc
from time import time


class IterList:
    def __init__(self):
        self.data = []
        self.index = 0

    def __iter__(self):
        return self

    def __next__(self):
        while self.index < len(self.data):
            v = self.data[self.index]
            self.index += 1
            return v
        else:
            self.index = 0
            raise StopIteration

    def append(self, n):
        self.data.append(n)


def read(file):
    st = time()
    dt = open(file, 'r')
    dt.readline()
    point = dt.readline()
    scala = 1024*1024

    gene_list = []
    x_list = []
    y_list = []
    value_list = []

    print(u'当前进程的内存使用: %.4f MB' % (psutil.Process(os.getpid()).memory_info().rss / 1024 / 1024))
    while point:
        gene, x, y, value = point.strip().split('\t')

        gene_list.append(gene)
        x_list.append(x)
        y_list.append(y)
        value_list.append(value)

        point = dt.readline()
        if not point:
            print(u'\t当前进程的内存使用: %.4f MB' % (psutil.Process(os.getpid()).memory_info().rss / 1024 / 1024))

    print(u'当前进程的内存使用: %.4f MB' % (psutil.Process(os.getpid()).memory_info().rss / 1024 / 1024))

    print("gene_list memory = ", getsizeof(gene_list)/scala)
    print("x_list memory = ", getsizeof(x_list)/scala)
    print("y_list memory = ", getsizeof(y_list)/scala)
    print("value_list memory = ", getsizeof(value_list)/scala)

    # print(len(gene_set))

    # gene_list = np.asarray(gene_list)
    # x_list = np.asarray(x_list, dtype=np.uint32)
    # y_list = np.asarray(y_list, dtype=np.uint32)
    # value_list = np.asarray(value_list, dtype=np.uint8)
    #
    # print("gene_list memory = ", getsizeof(gene_list)/scala)
    # print("x_list memory = ", getsizeof(x_list)/scala)
    # print("y_list memory = ", getsizeof(y_list)/scala)
    # print("value_list memory = ", getsizeof(value_list)/scala)
    print(u'当前进程的内存使用: %.4f MB' % (psutil.Process(os.getpid()).memory_info().rss / 1024 / 1024))
    print("\trun time = ", time() - st, 's')


def npread(file):
    st = time()
    idx = 0
    scala = 1024 * 1024

    gene_list = [''] * 10000000
    x_list = np.zeros(10000000).astype(np.uint32)
    y_list = np.zeros(10000000).astype(np.uint32)
    value_list = np.zeros(10000000).astype(np.uint8)
    print(u'当前进程的内存使用: %.4f MB' % (psutil.Process(os.getpid()).memory_info().rss / scala))

    f = open(file, 'r')
    f.readline()
    idx = 0
    point = f.readline()
    while point:
        gene, x, y, value = point.strip().split('\t')
        gene_list[idx] = gene
        x_list[idx] = x
        y_list[idx] = y
        value_list[idx] = value

        point = f.readline()
        idx += 1
        if not point:
            print(u'\t当前进程的内存使用: %.4f MB' % (psutil.Process(os.getpid()).memory_info().rss / scala))

    print(u'当前进程的内存使用: %.4f MB' % (psutil.Process(os.getpid()).memory_info().rss / scala))

    print("gene_list memory = ", getsizeof(gene_list) / scala)
    print("x_list memory = ", getsizeof(x_list) / scala)
    print("y_list memory = ", getsizeof(y_list) / scala)
    print("value_list memory = ", getsizeof(value_list) / scala)
    print("\trun time = ", time()-st, 's')


class Cache:
    def __init__(self):
        self._size = 256
        self.data = ''

    def isfull(self):
        return getsizeof(self.data) >= self._size

    def append(self, n):
        self.data += n + ','


def stread(file):
    st = time()
    scala = 1024 * 1024
    _tmp_prefix = "C:/Users/chenyujie/Desktop/Test/new_spatial_1kw"
    _gene_tmp = open(_tmp_prefix+".gene_tmp", 'w')
    _x_tmp = open(_tmp_prefix + ".x_tmp", 'w')
    _y_tmp = open(_tmp_prefix + ".y_tmp", 'w')
    _value_tmp = open(_tmp_prefix + ".value_tmp", 'w')


    # gene_cache = Cache()
    # x_cache = Cache()
    # y_cache = Cache()
    # value_cache = Cache()


    gene_cache = x_cache = y_cache = value_cache = ''

    print(u'当前进程的内存使用: %.4f MB' % (psutil.Process(os.getpid()).memory_info().rss / scala))

    f = open(file, 'r')
    f.readline()
    idx = 0
    point = f.readline()

    def cache_print(cache_list):
        for i in range(4):
            if cache_list[i].isfull():
                print(cache_list[i].data, end=',', file=cache_list[i].tmp)
                cache_list[i].data = []

    i = 0
    while point:
        gene, x, y, value = point.strip().split('\t')

        gene_cache += gene + ','
        x_cache += x + ','
        y_cache += y + ','
        value_cache += value + ','
        i += 1
        # print(u'\t当前进程的内存使用: %.4f MB' % (psutil.Process(os.getpid()).memory_info().rss / scala))
        if i == 32:
            print(gene_cache, end='', file=_gene_tmp)
            print(x_cache, end='', file=_x_tmp)
            print(y_cache, end='', file=_y_tmp)
            print(value_cache, end='', file=_value_tmp)
            gene_cache = x_cache = y_cache = value_cache = ''
            i = 0


        # gene_cache.append(gene)
        # x_cache.append(x)
        # y_cache.append(y)
        # value_cache.append(value)
        # # cache_print([gene_cache, x_cache, y_cache, value_cache])
        # if gene_cache.isfull():
        #     print(gene_cache.data, end='', file=_gene_tmp)
        #     gene_cache = Cache()
        # if x_cache.isfull():
        #     print(x_cache.data, end='', file=_x_tmp)
        #     x_cache = Cache()
        # if y_cache.isfull():
        #     print(y_cache.data, end='', file=_y_tmp)
        #     y_cache = Cache()
        # if value_cache.isfull():
        #     print(value_cache.data, end='', file=_value_tmp)
        #     value_cache = Cache()


        # print(u'\t当前进程的内存使用: %.4f MB' % (psutil.Process(os.getpid()).memory_info().rss / scala))
        point = f.readline()
        idx += 1
        if not point:
            print(u'\t当前进程的内存使用: %.4f MB' % (psutil.Process(os.getpid()).memory_info().rss / scala))

    print(u'当前进程的内存使用: %.4f MB' % (psutil.Process(os.getpid()).memory_info().rss / scala))
    print("\trun time = ", time() - st, 's')


def yieldread(file):
    st = time()
    scala = 1024 * 1024
    dt = open(file, 'r')
    dt.readline()

    gene_list = []
    x_list = []
    y_list = []
    value_list = []

    def line_read(dt):
        while True:
            point = dt.readline()
            if not point:
                break
            yield point
    for point in line_read(dt):
        gene, x, y, value = point.strip().split('\t')

        gene_list.append(gene)
        x_list.append(x)
        y_list.append(y)
        value_list.append(value)

    print(u'当前进程的内存使用: %.4f MB' % (psutil.Process(os.getpid()).memory_info().rss / scala))
    print("\trun time = ", time() - st, 's')


def main():
    file = "C:/Users/chenyujie/Desktop/Test/new_spatial_1kw.txt"
    out_path = "C:/Users/chenyujie/Desktop/Test"
    # read(file)
    # print("-----------------")
    # npread(file)
    # print("-----------------")
    # stread(file)
    # print("-----------------")
    yieldread(file)
    print(u'当前进程的内存使用: %.4f MB' % (psutil.Process(os.getpid()).memory_info().rss / 1024 / 1024))


if __name__ == '__main__':
    main()