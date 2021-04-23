from bisect import bisect_left, bisect_right
a = [1, 1, 2, 3, 5, 6]
print(bisect_left(a, 2))
print(bisect_right(a, 4))