import numpy as np
import bisect
from time import time


def target_get(ipt_target):
    target_x_range = ipt_target.split(',')[0]
    target_y_range = ipt_target.split(',')[1]
    x_min, x_max = target_x_range.split(':')
    x_min, x_max = int(x_min), int(x_max)
    y_min, y_max = target_y_range.split(':')
    y_min, y_max = int(y_min), int(y_max)
    return [x_min, x_max, y_min, y_max]


def load_index(index, target):
    st = time()

    x_min, x_max, y_min, y_max = target
    with open(index, 'r') as idx:
        border = idx.readline().strip().split(',')
        y_idx = np.asarray(idx.readline().strip().split(':'), dtype=np.uint32)
        ymin_i = bisect.bisect_left(y_idx, y_min) // 2
        ymax_i = bisect.bisect_right(y_idx, y_max) // 2
        if ymax_i == len(y_idx)//2:
            ymax_i = len(y_idx)//2-1
        dt_idx = np.zeros(2*(ymax_i-ymin_i+1), dtype=np.uint64)
        for i in range(ymax_i+1):
            if i < ymin_i:
                idx.readline()
                idx.readline()
                continue
            else:
                x_inf = idx.readline().strip().split(':')
                x_idx = np.asarray(x_inf, dtype=np.uint32)
                b_inf = idx.readline().strip().split(',')
                x_bit = np.asarray(b_inf, dtype=np.uint64)
                xmin_i = bisect.bisect_left(x_idx, x_min) // 2
                xmax_i = bisect.bisect_right(x_idx, x_max) // 2
                if xmax_i == len(x_idx)//2:
                    xmax_i = len(x_idx)//2-1
                dt_idx_i = 2*(i-ymin_i)
                dt_idx[dt_idx_i] = x_bit[xmin_i]
                dt_idx[dt_idx_i+1] = x_bit[xmax_i+1]
    print("load index time = ", time() - st, 's')
    return dt_idx


if __name__ == '__main__':
    index = "C:/Users/chenyujie/Desktop/Test/new_spatial_1kw.index"
    target = "16000:16424,16000:16847"
    target = target_get(target)
    dt_idx = load_index(index, target)
    print(dt_idx)
