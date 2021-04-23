from sys import argv
from time import time
from bisect import bisect_left, bisect_right

def ipt_error_detect(x_min, x_max, y_min, y_max):
    if x_min > x_max or y_min > y_max:
        return True
    else:
        return False


def idx_error_detect(x_min, x_max, y_min, y_max, border):
    if x_max < border[0] or x_min > border[1] or y_max < border[2] or y_min > border[3]:
        return True
    else:
        return False


def target_get(ipt_target):
    target_x_range = ipt_target.split(',')[0]
    target_y_range = ipt_target.split(',')[1]
    x_min, x_max = target_x_range.split(':')
    x_min, x_max = int(x_min), int(x_max)
    y_min, y_max = target_y_range.split(':')
    y_min, y_max = int(y_min), int(y_max)
    if ipt_error_detect(x_min, x_max, y_min, y_max):
        raise KeyboardInterrupt("Input Wrong: Target is Error")
    return [x_min, x_max, y_min, y_max]


def index_load(idx_file, ipt_target):
    idx = open(idx_file, 'r')
    x_min, x_max, y_min, y_max = target_get(ipt_target)
    border = list(map(int, idx.readline().strip().split(',')))
    if idx_error_detect(x_min, x_max, y_min, y_max, border):
        raise KeyboardInterrupt("Index Wrong: Target is out of Data Range")
    # y_list = idx.readline().strip().split(':')
    # print(y_list)
    y_list = list(map(int, idx.readline().strip().split(':')))
    x_idxs = idx.readlines()
    y_start = bisect_left(y_list, y_min)
    y_end = bisect_right(y_list, y_max)
    if y_end % 2 == 0:
        y_end -= 1
    _y_start, _y_end = y_start//2, y_end//2
    idx_range = []
    for y in range(_y_start, _y_end+1):
        x_list = list(map(int, x_idxs[y*2].strip().split(':')))
        x_offset_list = list(map(int, x_idxs[y*2+1].strip().split(',')))
        x_start = bisect_left(x_list, x_min)
        x_end = bisect_right(x_list, x_max)
        if x_start == x_end:
            continue
        if x_end % 2 == 0:
            x_end -= 1
        _x_start, _x_end = x_start//2, x_end//2
        idx_range.append(x_offset_list[_x_start:_x_end+1+1])
    return idx_range


def load_data(data_file, idx_range, ipt_target):
    dt = open(data_file, 'r')
    x_min, x_max, y_min, y_max = target_get(ipt_target)
    dt_search = []
    for idx in range(len(idx_range)):
        dt.seek(idx_range[idx][0])
        dt_get = dt.read(idx_range[idx][-1] - idx_range[idx][0])
        points = dt_get.split(',')[:-1]
        if idx == 0:
            for point in points:
                x, y = point.split(':')[:2]
                x, y = int(x), int(y)
                if y < y_min:
                    continue
                else:
                    if x < x_min or x > x_max:
                        continue
                    else:
                        dt_search.append(point)
        elif idx == len(idx_range) - 1:
            for point in points:
                x, y = list(map(int, point.split(':')[:2]))
                x, y = int(x), int(y)
                if y > y_max:
                    break
                else:
                    if x < x_min or x > x_max:
                        continue
                    else:
                        dt_search.append(point)
        else:
            i = 0
            CutLeft = CutRight = 0
            length = len(points)
            while True:
                if CutLeft != 0 and CutRight != 0:
                    break
                x_left, y_left = list(map(int, points[i].split(':')[:2]))
                x_right, y_right = list(map(int, points[length-1-i].split(':')[:2]))

                i += 1



def do(data_file, index_file, out_file, ipt_target):
    idx_range = index_load(index_file, ipt_target)
    print(idx_range)


if __name__ == '__main__':
    # file_path = argv[1]
    # target = argv[2]
    file_path = "C:/Users/chenyujie/Desktop/Test/new_spatial_100"
    target = "4500:6000,3000:4500"
    index = file_path + '.index'
    data = file_path + '.data'
    out = file_path + '.search'
    do(data, index, out, target)
