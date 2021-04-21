import numpy as np
import pandas as pd
import time
from sys import argv


def fill_zero(lower, upper, data_dict):
    for i in range(lower + 1, upper):
        data_dict['each_stat'][0].append(0)
        data_dict['each_stat'][1].append(i)


def load(file):
    with open(file, 'rt') as Input:
        Input.readline()
        line_count = 0
        line_list = []
        data_dict = {'each_stat': [[], []]}
        stat = False
        for line in Input:
            [gene, x, y, value] = line.strip().split('\t')
            if not stat:
                line_idx = int(y)
                stat = True
            if int(y) != line_idx:
                data_dict[line_idx] = []
                data_dict[line_idx].extend(line_list)
                data_dict['each_stat'][0].append(line_count)
                data_dict['each_stat'][1].append(line_idx)
                fill_zero(line_idx, int(y), data_dict)
                line_idx = int(y)
                line_count = 0
                line_list = []
            point = (gene, x, y, value)
            line_list.append(point)
            line_count += 1
    data_dict[line_idx] = line_list
    fill_zero(line_idx, int(y), data_dict)
    data_dict['each_stat'][0].append(line_count)
    data_dict['each_stat'][1].append(int(y))
    return data_dict


def load_disorder(file):
    with open(file, 'rt') as Input:
        Input.readline()
        max_y = max_x = 0
        min_y = min_x = 99999999
        data_dict = {'each_stat': [[], []]}
        for line in Input:
            point = [gene, x, y, value] = line.strip().split('\t')
            x, y = int(x), int(y)
            if y >= max_y:
                max_y = y
            if y < min_y:
                min_y = y
            if x >= max_x:
                max_x = x
            if x < min_x:
                min_x = x
            if y not in data_dict.keys():
                data_dict[y] = []
            data_dict[y].append(point)
        count_list = [0] * (max_y - min_y + 1)
        line_range = list(range(min_y, max_y+1))
        nz_line = []
        for line_idx in line_range:
            if line_idx in data_dict.keys():
                count_list[line_range.index(line_idx)] = len(data_dict[line_idx])
            nz_line.append(line_idx)
    data_dict['each_stat'][0] = count_list
    data_dict['each_stat'][1] = nz_line
    return data_dict


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
                key = str(init_idx) + ':' + str(line_idx - 1)
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
        key = str(init_idx) + ':' + str(line_idx)
        data_format[key] = block
        data_format['each_stat'][key] = num

    return data_format


def trans_dataframe(input_data, input_num):
    num = np.asarray(input_num).sum()
    data = []
    for list in input_data:
        data.extend(list)
    data = np.asarray(data).reshape(num, 4)
    data = pd.DataFrame(data, columns=['gene', 'x', 'y', 'value'])
    data[['x', 'y', 'value']] = data[['x', 'y', 'value']].apply(pd.to_numeric)
    data_by_x = data.sort_values(by='x')
    return data_by_x


def column_cut_range(data, max_blank=300):
    x = list(data['x'])
    divide_list = {'each_stat': []}
    block = []
    lower_idx, init_idx, blank_num, point_num = x[0], x[0], 0, 0
    for row in data.itertuples():
        gene, x, y, value = getattr(row, 'gene'), getattr(row, 'x'), getattr(row, 'y'), getattr(row, 'value')
        point = (gene, x, y, value)
        if abs(x - lower_idx) <= 1:
            interval = 0
        else:
            interval = x - lower_idx - 1
        if blank_num + interval > max_blank:
            key = str(init_idx)+':'+str(lower_idx)
            divide_list[key] = block
            divide_list['each_stat'].append(point_num)
            init_idx = x
            blank_num, point_num = 0, 0
            block = []
        else:
            blank_num += interval
        point_num += 1
        block.append(point)
        lower_idx = x
    return divide_list


def column_cut_single(data):
    x = list(data['x'])
    divide_list = {'each_stat': []}
    block = []
    lower_idx, init_idx, point_num = x[0], x[0], 0
    for row in data.itertuples():
        gene, x, y, value = getattr(row, 'gene'), getattr(row, 'x'), getattr(row, 'y'), getattr(row, 'value')
        point = (gene, x, y, value)
        if abs(x - lower_idx) >= 1:
            key = str(init_idx) + ':' + str(lower_idx)
            divide_list[key] = block
            divide_list['each_stat'].append(point_num)
            init_idx = x
            block = []
            point_num = 0
        block.append(point)
        point_num += 1
        lower_idx = x
    key = str(init_idx) + ':' + str(lower_idx)
    divide_list[key] = block
    divide_list['each_stat'].append(point_num)
    return divide_list


def column_cut_block(data, size=2000):
    data_col_single = column_cut_single(data)
    key_list = list(data_col_single.keys())[1:]
    each_stat = data_col_single['each_stat']
    point_num= 0
    init_lower, init_upper = list(map(int, key_list[0].split(':')))
    b_lower, b_upper = init_lower, init_upper
    block = []
    data_cut_block = {'each_stat': []}
    for idx in range(len(each_stat)):
        lower, upper = list(map(int, key_list[idx].split(':')))
        if point_num + each_stat[idx] > size:
            key = str(init_lower) + ':' + str(b_upper)
            data_cut_block[key] = block
            data_cut_block['each_stat'].append(point_num)
            init_lower, init_upper = lower, upper
            point_num = 0
            block = []
        block.extend(data_col_single[key_list[idx]])
        point_num += each_stat[idx]
        b_lower, b_upper = lower, upper
    key = str(init_lower) + ':' + str(b_upper)
    data_cut_block[key] = block
    data_cut_block['each_stat'].append(point_num)
    return data_cut_block


def format(file):
    data_dict = load_disorder(file)
    data_by_line = line_cut(data_dict)
    data_format = {}
    length_list = []
    for key in list(data_by_line.keys())[1:]:
        data_df = trans_dataframe(data_by_line[key], data_by_line['each_stat'][key])
        data_by_column = column_cut_block(data_df)
        item = key + ':' + str(len(list(data_by_column.keys())))
        length_list.append(item)
        data_format[key] = data_by_column
    return data_format, length_list


def printf_data(data_format, index_file, data_file):
    index = open(index_file, 'w')
    out = open(data_file, 'w')
    print(':'.join(list(data_format.keys())), file=index)
    idx = 0
    init = 0
    for line_key in data_format.keys():
        print(':'.join(list(data_format[line_key].keys())[1:]), file=index)
        print(init, end=',', file=index)
        for col_key in list(data_format[line_key].keys())[1:]:
            cout = data_format[line_key][col_key]
            cout = list(map(lambda x: ':'.join(list(map(str, x))), cout))
            for item in cout:
                print(item, end=',', file=out)
                bits = len(item.encode()) + 1
                idx += bits
            print(idx, end=',', file=index)
        init = idx
        print('', file=index)


def printf_stat(length_list, stat_file):
    stat = open(stat_file, 'w')
    for i in length_list:
        print(i, file=stat)


def rename_out(file, out_path):
    path = file.split('/')[-1]
    prefix = path.split('.')[:-1]
    prefix = '.'.join(prefix)
    out_data = out_path + '/' + prefix + '.data'
    out_index = out_path + '/' + prefix + '.index'
    out_stat = out_path + '/' + prefix + '.stat'
    return out_data, out_index, out_stat


if __name__ == '__main__':
    start_time = time.time()
    file = argv[1]
    out_path = argv[2]
    data_format, length_list = format(file)
    out, index, stat = rename_out(file, out_path)
    printf_data(data_format, index, out)
    printf_stat(length_list, stat)
    end_time = time.time()
    print("run_time = ", end_time - start_time, 's')