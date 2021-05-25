import numpy as np
import sys
import os
import psutil
from time import time


def max_min(x, y, min_x, max_x, min_y, max_y):
    if x > max_x:
        max_x = x
    elif x < min_x:
        min_x = x
    if y > max_y:
        max_y = y
    elif y < min_y:
        min_y = y
    return min_x, max_x, min_y, max_y


def load_data(ipt_file):
    ipt = open(ipt_file, 'r')
    ipt.readline()
    point = ipt.readline()
    rawdata_dict = {}
    x_min, y_min = list(map(int, point.strip().split('\t')[1:3]))
    x_max = x_min
    y_max = y_min
    while point:
        gene, x, y, value = point.strip().split('\t')
        x, y = list(map(int, [x, y]))
        x_min, x_max, y_min, y_max = max_min(x, y, x_min, x_max, y_min, y_max)
        if y not in rawdata_dict.keys():
            rawdata_dict[y] = {}
        if x not in rawdata_dict[y].keys():
            rawdata_dict[y][x] = []
        rawdata_dict[y][x].append(':'.join([str(x), str(y), gene, value]))
        point = ipt.readline()
    return rawdata_dict, [x_min, x_max, y_min, y_max]


