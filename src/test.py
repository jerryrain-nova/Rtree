import numpy as np
from sys import getsizeof
import psutil
import os


class test:
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

    def insert(self, l):
        self.data.append(l)


file = "C:/Users/chenyujie/Desktop/Test/new_spatial_1kw.y_tmp"
f = open(file, 'r')
print(u'当前进程的内存使用: %.4f MB' % (psutil.Process(os.getpid()).memory_info().rss / 1024 / 1024))
a = np.zeros(10000000).astype(np.uint32)
print(u'当前进程的内存使用: %.4f MB' % (psutil.Process(os.getpid()).memory_info().rss / 1024 / 1024))
for i in range(10000000):
    a[i] = int(f.readline().strip())
    print(u'当前进程的内存使用: %.4f MB' % (psutil.Process(os.getpid()).memory_info().rss / 1024 / 1024))
    if i == 10000000-1:
        print(u'当前进程的内存使用: %.4f MB' % (psutil.Process(os.getpid()).memory_info().rss / 1024 / 1024))
print(a)
print(u'当前进程的内存使用: %.4f MB' % (psutil.Process(os.getpid()).memory_info().rss / 1024 / 1024))


