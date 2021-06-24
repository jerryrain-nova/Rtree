from sys import argv
from time import time

st = time()

file = argv[1]

with open(file, 'r') as f:
    while True:
        line = f.readline()
        if not line:
            break

print("read time = ", time()-st, 's')
