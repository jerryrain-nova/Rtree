from src import load_data
from src import format_data
import numpy as np
import pandas as pd


def trans_dataframe(line_range, input_data, input_num):
    lower, upper = line_range.split('-')
    num = np.asarray(input_num).sum()
    data = []
    for list in input_data:
        data.extend(list)
    print(len(input_data[1][0]))
    data = np.asarray(data).reshape(num, 4)
    data = pd.DataFrame(data, columns=['gene', 'x', 'y', 'value'])
    data[['x', 'y', 'value']] = data[['x', 'y', 'value']].apply(pd.to_numeric)
    data_by_x = data.sort_values(by='x')
    data_by_y = data
    return data_by_x, data_by_y


def rectangle(data, max_blank=300):
    x = list(data['x'])
    unique_x = len(data['x'].unique())
    max_x = data.loc[:, 'x'].max()
    divide_list = {'each_stat': []}
    block = []
    lower_idx, init_idx, blank_num, point_num = x[0], x[0], 0, 0
    for idx in x:
        if abs(idx - lower_idx) <= 1:
            interval = 0
        else:
            interval = idx - lower_idx - 1
        if blank_num + interval > max_blank:
            key = str(init_idx)+'-'+str(lower_idx)
            divide_list[key] = block
            divide_list['each_stat'].append(point_num)
            init_idx = idx
            blank_num, point_num = 0, 0
            block = []
        else:
            blank_num += interval
        point_num += 1
        block.append(idx)
        lower_idx = idx
    print(divide_list.keys())
    print(divide_list['each_stat'])





if __name__ == '__main__':
    file = "C:/Users/chenyujie/Desktop/Test/spatial_1w.txt"
    data_dict = load_data.load(file)
    data_format = format_data.delete_blank(data_dict)
    print("line_block = ", len(list(data_format.keys())) - 1)
    print(list(data_format.keys())[1:])
    key = list(data_format.keys())[1]
    data_by_x, data_by_y = trans_dataframe(key, data_format[key], data_format['each_stat'][key])

    rectangle(data_by_x)