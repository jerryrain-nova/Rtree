import numpy as np
from sys import getsizeof

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

a = [3, 1, 4, 2, 5]
ai = [1, 3, 0, 2, 4]
def argsort(l , il):
    for i in range(len(l)):
        il[i] = l[il[i]]
    return il
print(argsort(a, ai))