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

n = 3
print(n//3)

t = test()
a = [0, 1, 2, 3, 4, 5, 6]
for i in a:
    t.insert(i)
for x in t:
    print(x)