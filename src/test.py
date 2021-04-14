from bisect import bisect_left, bisect_right
a = [0, 1, 3, 5]
b = 6
p = bisect_right(a, b)
print(p)
