from sys import argv
import time
import threading
import fcntl

_data = []


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


def seek_data_head(data_idx, data, target, size=2000):
    global _data
    st = time.time()
    line_lower, line_upper, col_lower, col_upper = input_info(target)
    data = open(data, 'r')
    fcntl.flock(data.fileno(), fcntl.LOCK_EX)
    data.seek(data_idx[0])
    get_data = data.read(data_idx[1] - data_idx[0])
    fcntl.flock(data.fileno(), fcntl.LOCK_UN)
    data.close()
    data_list = get_data.split(',')[:-1]
    data_filter = []
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
    for point in data_list:
        y = int(point.split(':')[2])
        if y >= line_lower:
            data_filter.append(point)
    data_list = data_filter
    _data.extend(data_list)
    ed = time.time()
    print("head_time = ", ed-st, 's')


def seek_data_tail(data_idx, data, target, size=2000):
    global _data
    st = time.time()
    line_lower, line_upper, col_lower, col_upper = input_info(target)
    data = open(data, 'r')
    fcntl.flock(data.fileno(), fcntl.LOCK_EX)
    data.seek(data_idx[0])
    get_data = data.read(data_idx[1] - data_idx[0])
    fcntl.flock(data.fileno(), fcntl.LOCK_UN)
    data.close()
    data_list = get_data.split(',')[:-1]
    data_filter = []
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
    for point in data_list:
        y = int(point.split(':')[2])
        if y <= line_upper:
            data_filter.append(point)
    data_list = data_filter
    _data.extend(data_list)
    ed = time.time()
    print("tail_time = ", ed-st, 's')


def seek_data(data_idx, data, target, size=2000):
    global _data
    st = time.time()
    line_lower, line_upper, col_lower, col_upper = input_info(target)
    data = open(data, 'r')
    fcntl.flock(data.fileno(), fcntl.LOCK_EX)
    data.seek(data_idx[0])
    get_data = data.read(data_idx[1] - data_idx[0])
    fcntl.flock(data.fileno(), fcntl.LOCK_UN)
    data.close()
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
    _data.extend(data_list)
    ed = time.time()
    print("mid_time = ", ed-st, 's')


def search_data_range(index_file, data_file, target):
    index = open(index_file, 'r')
    data = data_file
    line_index = list(map(int, index.readline().strip().split(':')))
    line_lower, line_upper, col_lower, col_upper = input_info(target)
    line_idx_range = get_search_target(line_lower, line_upper, line_index)
    col_data_idx = index.readlines()[2 * line_idx_range[0]:2 * line_idx_range[-1] + 2]
    threads = []
    for line_idx in range(0, line_idx_range[-1] - line_idx_range[0] + 1):
        col_index, data_index = col_data_idx[2 * line_idx:2 * line_idx + 2]
        col_index = list(map(int, col_index.strip().split(':')))
        data_index = list(map(int, data_index.strip().split(',')[:-1]))
        init_idx = data_index[0]
        data_index = data_index[1:]
        col_idx_range = get_search_target(col_lower, col_upper, col_index)
        if len(col_idx_range) == 1:
            if col_idx_range[0] == 0:
                data_range = [init_idx, data_index[0]]
            else:
                data_range = [data_index[col_idx_range[0] - 1], data_index[col_idx_range[0]]]
        else:
            if col_idx_range[0] == 0:
                data_range = [init_idx, data_index[col_idx_range[-1]]]
            else:
                data_range = [data_index[col_idx_range[0] - 1], data_index[col_idx_range[-1]]]
        if line_idx == 0:
            print("start")
            t = threading.Thread(target=seek_data_head, args=(data_range, data, target))
            threads.append(t)
            t.setDaemon(True)
            t.start()
        if line_idx == line_idx_range[-1] - line_idx_range[0]:
            print("end")
            t = threading.Thread(target=seek_data_tail, args=(data_range, data, target))
            threads.append(t)
            t.setDaemon(True)
            t.start()
        else:
            t = threading.Thread(target=seek_data, args=(data_range, data, target))
            threads.append(t)
            t.setDaemon(True)
            t.start()

    for t in threads:
        t.join()
    print("threads = ", len(threads))


def printf_data_new(data, out):
    out = open(out, 'w')
    header = ['gene', 'x', 'y', 'value']
    output = ':'.join(header) + '\n'
    for item in data:
        output += item + '\n'
    out.write(output)


def search_data(index, data, out, target):
    global _data
    start_time = time.time()
    search_data_range(index, data, target)
    end_time1 = time.time()
    printf_data_new(_data, out)
    end_time2 = time.time()
    print("search_time = ", end_time1 - start_time, 's')
    print("print_time = ", end_time2 - end_time1, 's')


if __name__ == '__main__':
    file_path = argv[1]
    index = file_path + '_index.txt'
    data = file_path + '_data.txt'
    out = file_path + '_search.result'
    target = argv[2]
    search_data(index, data, out, target)
