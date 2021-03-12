import numpy as np
import pandas as pd
import time
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
    # print(divide_list.keys())
    # print(divide_list['each_stat'])
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
    # print(divide_list.keys())
    # print("column_block = ", len(list(divide_list.keys())) - 1)
    # print(divide_list['each_stat'])
    # print("each_length = ", len(divide_list['each_stat']))
    # f = open("C:/Users/chenyujie/Desktop/Test/block_test.txt", 'w')
    # print(list(divide_list.keys())[1:], file=f)
    # print(divide_list['each_stat'], file=f)
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
        # if blank_num > 1:
        #     print("blank = ", blank_num, "lower = ", lower, "upper = ", upper)
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
    # print(data_cut_block.keys())
    # print(data_cut_block.keys())
    # print("length = ", len(list(data_cut_block.keys())))
    # print(data_cut_block['each_stat'])
    return data_cut_block


def format(file):
    data_dict = load_data.load(file)
    data_by_line = line_cut(data_dict)
    data_format = {}
    length_list = []
    # key = list(data_by_line.keys())[7]
    # print("key = ", key)
    # data_df = trans_dataframe(data_by_line[key], data_by_line['each_stat'][key])
    # column_cut_block(data_df)
    for key in list(data_by_line.keys())[1:]:
        # print("key = ", key)
        data_df = trans_dataframe(data_by_line[key], data_by_line['each_stat'][key])
        data_by_column = column_cut_block(data_df)
        item = key + ':' + str(len(list(data_by_column.keys())))
        length_list.append(item)
        data_format[key] = data_by_column
    # for i in length_list:
    #     print(i)
    return data_format


def printf_data(data_format, index_file, data_file):
    index = open(index_file, 'w')
    out = open(data_file, 'w')
    # index_output = ''
    # out_output = ''
    # index_output += ':'.join(list(data_format.keys()))
    print(':'.join(list(data_format.keys())), file=index)
    # idx = 0
    # for line_key in data_format.keys():
    #     length = len(list(data_format[line_key])) - 1
    #     idx += 1
    #     col_range = str(init_idx) + '-' + str(idx)
    #     init_idx = idx
    #     print(col_range, end=',', file=index)
    # print('', file=index)
    idx = 0
    init = 0
    for line_key in data_format.keys():
        # index_output += ':'.join(list(data_format[line_key].keys())[1:])
        print(':'.join(list(data_format[line_key].keys())[1:]), file=index)
        print(init, end=',', file=index)
        for col_key in list(data_format[line_key].keys())[1:]:
            cout = data_format[line_key][col_key]
            cout = list(map(lambda x: ':'.join(list(map(str, x))), cout))
            for item in cout:
                # out_output += item + ','
                print(item, end=',', file=out)
                bits = len(item.encode()) + 1
                idx += bits
            # index_output += str(idx) + ','
            print(idx, end=',', file=index)
        # index_output += '\n'
        init = idx
        print('', file=index)
    # index.write(index_output)
    # out.write(out_output)


if __name__ == '__main__':
    start_time = time.time()
    file = "C:/Users/chenyujie/Desktop/Test/spatial_1kw.txt"
    data_format = format(file)
    index = "C:/Users/chenyujie/Desktop/Test/spatial_format_index.txt"
    out = "C:/Users/chenyujie/Desktop/Test/spatial_format_data.txt"
    printf_data(data_format, index, out)
    end_time = time.time()
    print("run_time = ", end_time - start_time, 's')