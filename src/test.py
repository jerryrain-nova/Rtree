import pickle
from src import build_btree
from bisect import bisect_left

a = ['f', 'a', 'c', 'e', 'd', 'g', 'i', 'z']
a = sorted(a)
print(a)
print(bisect_left(a, 'i'))
