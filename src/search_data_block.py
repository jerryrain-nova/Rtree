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
    if upper < index_list[0] or upper > index_list[-1] or lower < index_list[0] or lower > index_list[-1]:
        print("input wrong")
        quit()
    for idx in range(len(index_list)):
        if init and stop:
            if stop_block < init_block:
                print("No value exits")
                quit()
            break
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
        init_idx = data_index[0]
        data_index = data_index[1:]
        col_idx_range = get_search_target(col_lower, col_upper, col_index)
        if len(col_idx_range) == 1:
            if col_idx_range[0] == 0:
                data_range.extend([init_idx, data_index[0]])
            else:
                data_range.extend([data_index[col_idx_range[0] - 1], data_index[col_idx_range[0]]])
        else:
            if col_idx_range[0] == 0:
                data_range.extend([init_idx, data_index[col_idx_range[-1]]])
            else:
                data_range.extend([data_index[col_idx_range[0] - 1], data_index[col_idx_range[-1]]])
    return data_range


def get_data(data_file, data_range, target, size=2000):
    data = open(data_file, 'r')
    data_target = []
    line_lower, line_upper, col_lower, col_upper = input_info(target)
    length = len(data_range)
    seek_time = 0
    seek_num = 0
    filter_time = 0
    read_time = 0
    for data_idx in range(0, length, 2):
        start_time = time.time()
        data.seek(data_range[data_idx])
        seek_t = time.time()
        get_data = data.read(data_range[data_idx + 1] - data_range[data_idx])
        read_t = time.time()
        seek_time += seek_t - start_time
        seek_num += 1
        read_time += read_t - seek_t
        data_list = get_data.split(',')[:-1]
        split_lf, split_rh = False, False
        for idx in range(size):
            x_lf = int(data_list[idx].split(':')[1])
            x_rh = int(data_list[-size + idx].split(':')[1])
            if split_lf and split_rh:
                break
            if not split_lf and x_lf >= col_lower:
                data_list = data_list[idx:]
                split_lf = True
            if not split_rh and x_rh > col_upper:
                data_list = data_list[:-size + idx]
                split_rh = True

        if data_idx == 0:
            data_filter = []
            for point in data_list:
                y = int(point.split(':')[2])
                if y >= line_lower:
                    data_filter.append(point)
            data_list = data_filter
        if data_idx == length - 2:
            data_filter = []
            for point in data_list:
                y = int(point.split(':')[2])
                if y <= line_upper:
                    data_filter.append(point)
            data_list = data_filter
        end_time = time.time()
        filter_time += end_time - read_t
        data_target.extend(data_list)
    print("\tseek_num = ", seek_num)
    print("\tseek_time = ", seek_time, 's')
    print("\tread_time = ", read_time, 's')
    print("\tfilter_time = ", filter_time, 's')
    return data_target


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
    start_time = time.time()
    out.write(output)
    end_time = time.time()
    print("\twrite_time = ", end_time - start_time, 's')


def printf_data_new(data, out_file):
    out = open(out_file, 'w')
    header = ['gene', 'x', 'y', 'value']
    output = ':'.join(header) + '\n'
    for item in data:
        output += item + '\n'
    out.write(output)


def search_data(index, data, target, out):
    start_time = time.time()
    data_range = search_idx_range(index, target)
    end_time1 = time.time()
    target_data = get_data(data, data_range, target)
    end_time2 = time.time()
    printf_data_new(target_data, out)
    end_time3 = time.time()
    print("index time = ", end_time1 - start_time, 's')
    print("search time = ", end_time2 - end_time1, 's')
    print("print time = ", end_time3 - end_time2, 's')
    print("run time = ", end_time3 - start_time, 's')
    return target_data


if __name__ == '__main__':
    file_path = argv[1]
    index = file_path + '.index'
    data = file_path + '.data'
    out = file_path + '_search.result'
    target = argv[2]

    data_target = search_data(index, data, target, out)





