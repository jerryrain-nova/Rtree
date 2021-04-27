from sys import argv
from time import time


def extremum(x, y, min_x, max_x, min_y, max_y):
    if x >= max_x:
        max_x = x
    if y >= max_y:
        max_y = y
    if x < min_x:
        min_x = x
    if y < min_y:
        min_y = y
    return min_x, max_x, min_y, max_y


def load_rawdata(ipt_file):
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
        x_min, x_max, y_min, y_max = extremum(x, y, x_min, x_max, y_min, y_max)
        if y not in rawdata_dict.keys():
            rawdata_dict[y] = {}
        if x not in rawdata_dict[y].keys():
            rawdata_dict[y][x] = []
        rawdata_dict[y][x].append(':'.join([str(x), str(y), gene, value]))
        point = ipt.readline()
    return rawdata_dict, [x_min, x_max, y_min, y_max]


def sorted_by_y(rawdata_dict):
    y_list = sorted(list(rawdata_dict.keys()))
    init_y = last_y = y_list[0]
    y_idx = 0
    data_y = {y_idx: {}}
    y_range = []
    for y in y_list:
        if y - last_y > 1:
            y_range.extend([init_y, last_y])
            init_y = y
            y_idx += 1
            data_y[y_idx] = {}
        for col in rawdata_dict[y].keys():
            if col not in data_y[y_idx].keys():
                data_y[y_idx][col] = []
            data_y[y_idx][col].extend(rawdata_dict[y][col])
        last_y = y
        if y == y_list[-1]:
            y_range.extend([init_y, last_y])
    return data_y, y_range


def format_data(data_y):
    _M = 256
    data_format = {}
    for y_idx in data_y.keys():
        num = 0
        x_idx = 0
        data_format[y_idx] = {'x_range': [], x_idx: []}
        x_list = sorted(list(data_y[y_idx].keys()))
        init_x = last_x = x_list[0]
        for x in x_list:
            if num >= _M:
                data_format[y_idx]['x_range'].extend([init_x, last_x])
                init_x = x
                x_idx += 1
                data_format[y_idx][x_idx] = []
            data_format[y_idx][x_idx].extend(data_y[y_idx][x])
            num += len(data_y[y_idx][x])
            last_x = x
            if x == x_list[-1]:
                data_format[y_idx]['x_range'].extend([init_x, last_x])
    return data_format


def printf_data(data_format, y_range, border, opt_data, opt_index):
    dt = open(opt_data, 'w')
    idx = open(opt_index, 'w')
    offset = 0
    init = 0
    print(','.join(list(map(str, border))), file=idx)
    print(':'.join(list(map(str, y_range))), file=idx)
    for y_idx in data_format.keys():
        print(':'.join(list(map(str, data_format[y_idx]['x_range']))), file=idx)
        cout = []
        offset_list = [init]
        for x_idx in list(data_format[y_idx].keys())[1:]:
            grid = ','.join(data_format[y_idx][x_idx])
            cout.append(grid)
            offset += len(grid.encode()) + 1
            offset_list.append(offset)
        print(','.join(cout), end=',', file=dt)
        print(','.join(list(map(str, offset_list))), file=idx)
        init = offset


def do(ipt_file, opt_data, opt_index):
    st = time()
    rawdata_dict, border = load_rawdata(ipt_file)
    load_t = time()
    print("load_data time =", load_t-st, 's')
    data_y, y_range = sorted_by_y(rawdata_dict)
    data_format = format_data(data_y)
    format_t = time()
    print("format_data time =", format_t-load_t, 's')
    printf_data(data_format, y_range, border, opt_data, opt_index)
    print_t = time()
    print("print time =", print_t-format_t, 's')
    print("run time =", print_t-st, 's')


def rename_out(ipt_file, opt_path):
    path = ipt_file.split('/')[-1]
    prefix = path.split('.')[:-1]
    prefix = '.'.join(prefix)
    out_data = opt_path + '/' + prefix + '.data'
    out_index = opt_path + '/' + prefix + '.index'
    return out_data, out_index


if __name__ == '__main__':
    file = "C:/Users/chenyujie/Desktop/Test/new_spatial_1kw.txt"
    out_path = "C:/Users/chenyujie/Desktop/Test"
    # file = argv[1]
    # out_path = argv[2]
    f_data, f_index = rename_out(file, out_path)
    do(file, f_data, f_index)
