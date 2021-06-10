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


a = []
b = ''
for i in range(5):
    a.append(i)
b += "a"
print("a size = ", getsizeof(a))
print("b size = ", getsizeof(b))