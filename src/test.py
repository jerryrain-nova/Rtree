from bisect import bisect_left
a = [0]
b = 1
p = bisect_left(a, b)
print(p)