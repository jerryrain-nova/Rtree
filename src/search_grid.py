from sys import argv
import time
import pandas as pd


def target_info(ipt_target, info_list):
    target_line_range = ipt_target.split(',')[0]
    target_col_range = ipt_target.split(',')[1]
    line_lower, line_upper = target_line_range.split(':')
    line_lower, line_upper = int(line_lower), int(line_upper)
    col_lower, col_upper = target_col_range.split(':')
    col_lower, col_upper = int(col_lower), int(col_upper)
    if line_lower > line_upper or col_lower > col_upper:
        print("input wrong")
        quit()
    min_x, min_y, max_x, max_y, grid_size = info_list
    if col_lower < min_x or col_lower > max_x:
        print("input wrong")
        quit()
    if line_lower < min_y or line_upper > max_y:
        print("input wrong")
        quit()
    init_line = int((line_lower - min_y) / grid_size)
    stop_line = int((line_upper - min_y) / grid_size)
    init_col = int((col_lower - min_x) / grid_size)
    stop_col = int((col_upper - min_x) / grid_size)
    return [init_line, stop_line, init_col, stop_col]


def get_range(idx_list, init_idx, stop_idx):
    init = stop = False
    start_idx = 0
    end_idx = len(idx_list) - 1
    for i in range(len(idx_list)):
        if init and stop:
            break
        if not init and idx_list[i] >= init_idx:
            start_idx = i
            init = True
        if not stop and idx_list[i] > stop_idx:
            end_idx = i-1
            stop = True
        if end_idx < start_idx:
            return False
    if not init:
        return False
    return start_idx, end_idx


def read_data(index_file, data_file, ipt_target, out_file):
    idx_time = 0
    seek_time = 0
    read_time = 0
    st = time.time()
    idx = open(index_file, 'r')
    dt = open(data_file, 'r')
    opt = open(out_file, 'w')
    info_list = list(map(int, idx.readline().strip().split(',')))
    init_line, stop_line, init_col, stop_col = target_info(ipt_target, info_list)
    line_list = list(map(int, idx.readline().strip().split(',')))
    col_info = idx.readlines()
    init_list = list(map(int, col_info[-1].strip().split(',')))
    if not get_range(line_list, init_line, stop_line):
        print("The area has no values")
        quit()
    else:
        line_start_idx, line_end_idx = get_range(line_list, init_line, stop_line)
    nz_bin = {}
    opt_data = []
    idx_time += time.time() - st
    for i in range(line_start_idx, line_end_idx+1):
        cir_st = time.time()
        seek_pos = init_list[i]
        col_list = list(map(int, col_info[2*i].strip().split(',')))
        col_bit_list = list(map(int, col_info[2*i+1].strip().split(',')[:-1]))
        col_bit_list.insert(0, 0)
        if not get_range(col_list, init_col, stop_col):
            continue
        else:
            col_start_idx, col_end_idx = get_range(col_list, init_col, stop_col)
        search_col_range = col_list[col_start_idx:col_end_idx+1]
        idx_t = time.time()
        idx_time += idx_t - cir_st
        dt.seek(seek_pos+col_bit_list[col_start_idx])
        seek_t = time.time()
        seek_time += seek_t-idx_t
        part_opt = dt.read(col_bit_list[col_end_idx+1] - col_bit_list[col_start_idx]).split(',')[:-1]
        read_t = time.time()
        read_time += read_t - seek_t
        nz_bin[line_list[i]] = search_col_range
        opt_data.extend(part_opt)
    print_t = time.time()
    print('\n'.join(opt_data), file=opt)

    ed = time.time()
    print("index_time = ", idx_time, 's')
    print("seek_time = ", seek_time, 's')
    print("read_time = ", read_time, 's')
    print("print_time = ", ed-print_t, 's')
    print("search_time = ", ed-st, 's')
    return opt_data, nz_bin, info_list


def trans_dataframe(opt_data, nz_bin, info_list):
    st = time.time()
    min_x, min_y, max_x, max_y, grid_size = info_list
    line_num = int((max_y-min_y)/grid_size) + 1
    col_num = int((max_x-min_x)/grid_size) + 1
    bin_name = []
    for line in range(line_num):
        for col in range(col_num):
            bin_name.append(str(line)+':'+str(col))
    bin_num = len(bin_name)

    idx = 0
    data_trans = {}
    for line in nz_bin.keys():
        for col in nz_bin[line]:
            name = str(line)+':'+str(col)
            for point in opt_data[idx].split(';'):
                gene, x, y, value = point.split(':')
                if gene not in data_trans.keys():
                    data_trans[gene] = [0] * bin_num
                data_trans[gene][bin_name.index(name)] += 1
            idx += 1
    print(data_trans.keys())
    print(len(data_trans['THRAP3']))
    ed = time.time()
    print("trans_dataframe_time = ", ed-st, 's')


def main(index_file, data_file, ipt_target, out_file):
    search_data, nz_bin, info_list = read_data(index_file, data_file, ipt_target, out_file)
    trans_dataframe(search_data, nz_bin, info_list)


if __name__ == '__main__':
    index = "C:/Users/chenyujie/Desktop/Test/spatial_format_index.txt"
    data = "C:/Users/chenyujie/Desktop/Test/spatial_format_data.txt"
    out = "C:/Users/chenyujie/Desktop/Test/spatial_format_search.result"
    target = '4900:5200,4500:4800'
    # file_path = argv[1]
    # index = file_path + '_index.txt'
    # data = file_path + '_data.txt'
    # out = file_path + '_search.result'
    # target = argv[2]
    st = time.time()
    main(index, data, target, out)
    ed = time.time()
    print("run_time = ", ed-st, 's')
