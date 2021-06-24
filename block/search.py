import time
import numpy as np
import bisect
import os
import argparse


def ipt_error_detect(x_min, x_max, y_min, y_max):
    if x_min > x_max or y_min > y_max:
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
        raise KeyboardInterrupt("Input Wrong: Target is Error!")
    return [x_min, x_max, y_min, y_max]


def idx_error_detect(target, border):
    x_min, x_max, y_min, y_max = target
    if x_max < int(border[0]) or x_min > int(border[1]) or y_max < int(border[2]) or y_min > int(border[3]):
        return True
    else:
        return False


def load_index(index, target):
    st = time.time()
    if not os.path.exists(index):
        raise KeyboardInterrupt("Input Wrong: Index File doesn\'t exit!")

    x_min, x_max, y_min, y_max = target
    with open(index, 'r') as idx:
        border = idx.readline().strip().split(',')
        if idx_error_detect(target, border):
            raise KeyboardInterrupt("Input Wrong: Target is out of Data Range!")
        y_idx = np.asarray(idx.readline().strip().split(':'), dtype=np.uint32)
        ymin_i = bisect.bisect_left(y_idx, y_min) // 2
        ymax_i = bisect.bisect_right(y_idx, y_max) // 2
        if ymax_i == len(y_idx)//2:
            ymax_i = len(y_idx)//2-1
        dt_idx = np.zeros(2*(ymax_i-ymin_i+1), dtype=np.uint64)
        for i in range(ymax_i+1):
            if i < ymin_i:
                idx.readline()
                idx.readline()
                continue
            else:
                x_idx = np.asarray(idx.readline().strip().split(':'), dtype=np.uint32)
                x_bit = np.asarray(idx.readline().strip().split(','), dtype=np.uint64)
                xmin_i = bisect.bisect_left(x_idx, x_min) // 2
                xmax_i = bisect.bisect_right(x_idx, x_max) // 2
                if xmax_i == len(x_idx)//2:
                    xmax_i = len(x_idx)//2-1
                dt_idx_i = 2*(i-ymin_i)
                dt_idx[dt_idx_i] = x_bit[xmin_i]
                dt_idx[dt_idx_i+1] = x_bit[xmax_i+1]
    print("load index time = ", time.time() - st, 's')
    return dt_idx


def load_data(data, dt_idx, target):
    st = time.time()
    if not os.path.exists(data):
        raise KeyboardInterrupt("Input Wrong:Data File doesn\'t exit!")
    x_min, x_max, y_min, y_max = target

    re_l = []
    with open(data, 'r') as dt:
        for i in range(0, len(dt_idx), 2):
            dt.seek(dt_idx[i])
            if dt_idx[i+1] == dt_idx[i]:
                continue
            points = dt.read(dt_idx[i+1]-dt_idx[i]).split(',')[:-1]
            lg = len(points)
            if i == 0:
                for point in points:
                    x, y = point.split(':')[:2]
                    x, y = int(x), int(y)
                    if y < y_min:
                        continue
                    else:
                        if x < x_min or x > x_max:
                            continue
                        else:
                            re_l.append(point)
            elif i == len(dt_idx)-2:
                for point in points:
                    x, y = point.split(':')[:2]
                    x, y = int(x), int(y)
                    if y > y_max:
                        continue
                    else:
                        if x < x_min or x > x_max:
                            continue
                        else:
                            re_l.append(point)
            else:
                offset = 0
                lfc = -1
                rhc = 0
                while True:
                    if lfc != -1 and rhc != 0:
                        re_l.extend(points[lfc:lg + rhc + 1])
                        break
                    if offset == lg:
                        break
                    x_lf = int(points[offset].split(':')[0])
                    x_rh = int(points[-1-offset].split(':')[0])
                    if x_lf >= x_min and lfc == -1:
                        lfc = offset
                    if x_rh <= x_max and rhc == 0:
                        rhc = -1-offset
                    offset += 1

    print("load data time = ", time.time() - st, 's')
    return re_l


def printf(result, re_l):
    st = time.time()
    with open(result, 'w') as re:
        print("X:Y:Gene:Value", file=re)
        print('\n'.join(re_l), file=re)
    print("print time = ", time.time() - st, 's')


def file_need(file_path, opt):
    index = file_path+'.index'
    g_index = file_path+'.g_index'
    data = file_path+'.data'
    result = opt + '/search.result'
    return [data, index, result, g_index]


def search_s(file_path, ipt_target, opt):
    st = time.time()
    target = target_get(ipt_target)
    data, index, result, g_index = file_need(file_path, opt)
    dt_idx = load_index(index, target)
    re_l = load_data(data, dt_idx, target)
    printf(result, re_l)
    print("\n************\nrun time = ", time.time() - st, 's\n************\n')


def load_g_index(g_index, target):
    st = time.time()
    if not os.path.exists(g_index):
        raise KeyboardInterrupt("Input Wrong:G_Index File doesn\'t exit!")

    with open(g_index, 'r') as gi:
        g_l = gi.readline().strip().split(',')
        target_s = sorted(target.split(','))

        res = []
        t_i = 0
        for i in range(len(g_l)):
            if g_l[i] == target_s[t_i]:
                res.append(i)
                t_i += 1
                if t_i == len(target_s):
                    break

        idx = 0
        d_i = []
        for i in range(res[-1]+1):
            if i == res[idx]:
                il = gi.readline().strip().split(',')
                d_i.extend(il)
                idx += 1
            else:
                gi.readline()

    print("load index time = ", time.time() - st, 's')
    return d_i


def load_g_data(data, d_i):
    st = time.time()
    res = []
    with open(data, 'r') as dt:
        for i in range(0, len(d_i), 2):
            dt.seek(int(d_i[i]))
            point = dt.read(int(d_i[i+1])).strip(',')
            res.append(point)
    print("load data time = ", time.time() - st, 's')
    return res


def search_g(file_path, target, opt):
    st = time.time()
    data, index, result, g_index = file_need(file_path, opt)
    d_i = load_g_index(g_index, target)
    re_l = load_g_data(data, d_i)
    printf(result, re_l)
    print("\n************\nrun time = ", time.time() - st, 's\n************\n')


def main():
    parser = argparse.ArgumentParser()
    parser.description = 'python3 search.py [-m Mode] [-f File_Path] [-o Out_Path]'
    parser.add_argument("-m", "--mode", help="G: gene ; S: site")
    parser.add_argument("-f", "--file", help="File Path(prefix).  Eg: PWD/data")
    parser.add_argument("-t", "--target", help="Gene: gene1,gene2,gene3,... \t Site: xmin:xmax,ymin:ymax (Eg:1000:2000,1000:2000)")
    parser.add_argument("-o", "--opt", help="Output Path")
    args = parser.parse_args()

    file_path = args.file
    target = args.target
    opt = args.opt
    if args.mode == 'S':
        search_s(file_path, target, opt)
    elif args.mode == 'G':
        search_g(file_path, target, opt)
    else:
        print("Check Search Mode!")
        quit()


if __name__ == '__main__':
    main()
