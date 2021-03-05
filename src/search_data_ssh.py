import pandas as pd
import numpy as np
import time
from sys import argv


def input_info(target):
    target_line_range = target.split(',')[0]
    target_col_range = target.split(',')[1]
    line_lower, line_upper = target_line_range.split(':')
    line_lower, line_upper = int(line_lower), int(line_upper)
    col_lower, col_upper = target_col_range.split(':')
    col_lower, col_upper = int(col_lower), int(col_upper)
    return line_lower, line_upper, col_lower, col_upper


def get_search_target(lower, upper, index_list):
    init, stop = False, False
    init_block, stop_block = 0, 0
    search_target = []
    if upper < index_list[0] or lower > index_list[-1]:
        print("input wrong")
        quit()
    for idx in range(len(index_list)):
        if index_list[idx] <= lower <= index_list[idx + 1]:
            if idx % 2 == 1:
                init_block = int((idx + 1) / 2)
            else:
                init_block = int(idx / 2)
            search_target.append(init_block)
            init = True
        if index_list[idx] <= upper <= index_list[idx + 1]:
            if idx % 2 == 1:
                stop_block = int(idx / 2)
            else:
                stop_block = int((idx + 1) / 2)
            search_target.append(stop_block)
            stop = True
        if init and stop:
            if stop_block < init_block:
                print("No value exits")
                quit()
            break
    search_target = list(set(search_target))
    search_target.sort(key=int)
    return search_target


def search_idx_range(index_file, target):
    index = open(index_file, 'r')
    line_index = list(map(int, index.readline().strip().split(':')))
    line_lower, line_upper, col_lower, col_upper = input_info(target)
    line_idx_range = get_search_target(line_lower, line_upper, line_index)
    col_data_idx = index.readlines()[2 * line_idx_range[0]:2 * line_idx_range[-1] + 2]
    data_range = []
    for line_idx in range(0, line_idx_range[-1] - line_idx_range[0] + 1):
        col_index, data_index = col_data_idx[2 * line_idx:2 * line_idx + 2]
        col_index = list(map(int, col_index.strip().split(':')))
        data_index = list(map(int, data_index.strip().split(',')[:-1]))
        col_idx_range = get_search_target(col_lower, col_upper, col_index)
        if len(col_idx_range) == 1:
            if col_idx_range[0] == 0:
                data_range.extend([0, data_index[0]])
            else:
                data_range.extend([data_index[col_idx_range[0] - 1], data_index[col_idx_range[0]]])
        else:
            if col_idx_range[0] == 0:
                data_range.extend([0, data_index[col_idx_range[-1]]])
            else:
                data_range.extend([data_index[col_idx_range[0] - 1], data_index[col_idx_range[-1]]])
    return data_range


def get_data(data_file, data_range, target):
    data = open(data_file, 'r')
    data_target = []
    num = 0
    line_lower, line_upper, col_lower, col_upper = input_info(target)
    for data_idx in range(0, len(data_range), 2):
        data.seek(data_range[data_idx])
        get_data = data.read(data_range[data_idx + 1] - data_range[data_idx])
        data_list = get_data.split(',')[:-1]
        num += len(data_list)
        data_target.extend(data_list)

    data_format = []
    for item in data_target:
        item_split = item.split(':')
        data_format.extend(item_split)
    data_format = np.asarray(data_format).reshape(num, 4)
    data_format = pd.DataFrame(data_format, columns=['gene', 'x', 'y', 'value'])
    data_format[['x', 'y', 'value']] = data_format[['x', 'y', 'value']].apply(pd.to_numeric)
    data_format = data_format.sort_values(by='x')
    x_loc = np.asarray(data_format['x'].tolist())
    target_x = np.where((x_loc >= col_lower) & (x_loc <= col_upper))[0]
    data_filter_x = data_format[target_x[0]: target_x[-1] + 1].reset_index().drop('index', axis=1)
    data_filter_x = data_filter_x.sort_values(by='y')
    y_loc = np.asarray(data_filter_x['y'].tolist())
    target_y = np.where((y_loc >= line_lower) & (y_loc <= line_upper))[0]
    data_filter_y = data_filter_x[target_y[0]: target_y[-1] + 1].reset_index().drop('index', axis=1)
    return data_filter_y


def printf_data(data, out_file):
    out = open(out_file, 'w')
    header = ['gene', 'x', 'y', 'value']
    output = '\t'.join(header) + '\n'
    # print('\t'.join(header), file=output)
    for row in data.itertuples():
        gene, x, y, value = getattr(row, 'gene'), getattr(row, 'x'), getattr(row, 'y'), getattr(row, 'value')
        output += gene + '\t' + str(x) + '\t' + str(y) + '\t' + str(value) + '\n'
        # point = list(map(str, [gene, x, y, value]))
        # output.write('\t'.join(point)+'\n')
        # print('\t'.join(point), file=output)
    out.write(output)

def search_data(index, data, target, out):
    start_time = time.time()
    data_range = search_idx_range(index, target)
    target_data = get_data(data, data_range, target)
    end_time = time.time()
    printf_data(target_data, out)
    print("search_time = ", end_time - start_time, 's')
    return target_data


if __name__ == '__main__':
    file_path = argv[1]
    index = file_path + '_index.txt'
    data = file_path + '_data.txt'
    out = file_path + '_search.result'
    target = argv[2]

    data_target = search_data(index, data, target, out)





