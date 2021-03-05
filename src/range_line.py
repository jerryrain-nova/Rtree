import numpy as np
import pandas as pd
from src import load_data


def line_cut(data_dict):
    each_stat = np.asarray(data_dict['each_stat'][0])
    each_idx = np.asarray(data_dict['each_stat'][1])
    zero_line = each_idx[np.where(each_stat == 0)[0]]
    init_idx = each_idx[np.where(each_stat != 0)[0][0]]
    block = []
    num = []
    data_format = {'each_stat': {}}
    for line_idx in each_idx:
        if line_idx in zero_line:
            if block:
                key = str(init_idx) + '-' + str(line_idx - 1)
                data_format[key] = block
                data_format['each_stat'][key] = num
                init_idx = line_idx
                block = []
                num = []
            continue
        else:
            if not block:
                init_idx = line_idx
        block.append(data_dict[line_idx])
        num.append(data_dict['each_stat'][0][data_dict['each_stat'][1].index(line_idx)])
    if block:
        key = str(init_idx) + '-' + str(line_idx)
        data_format[key] = block
        data_format['each_stat'][key] = num

    return data_format


def format(file):
    data_dict = load_data.load(file)
    data_by_line = line_cut(data_dict)


if __name__ == '__main__':
    import time
    start_time = time.time()
    file = "C:/Users/chenyujie/Desktop/Test/spatial_1kw.txt"
    format(file)
    end_time = time.time()
    print("run_time = ", end_time - start_time, 's')