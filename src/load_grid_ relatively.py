import time
import math


def extremum(x, y, min_x, min_y, max_x, max_y):
    if x >= max_x:
        max_x = x
    if y >= max_y:
        max_y = y
    if x < min_x:
        min_x = x
    if y < min_y:
        min_y = y
    return min_x, min_y, max_x, max_y


def info_sort(data_info):
    data_info['nz_col'] = sorted(list(data_info['nz_col']))
    data_info['nz_line'] = sorted(list(data_info['nz_line']))
    data_info['gene_lis'] = sorted(list(data_info['gene_list']))
    return data_info


def matrix_info(data_file, grid_size):
    ipt = open(data_file, 'r')
    ipt.readline()
    max_x = max_y = min_x = min_y = 0
    data_info = {'info': [min_x, min_y, max_x, max_y, grid_size], 'nz_col': set(), 'nz_line': set(), 'gene_list': set()}
    point = ipt.readline().strip()
    min_x, min_y = list(map(int, point.split('\t')[1:-1]))
    while point:
        gene, x, y, value = point.split('\t')
        x, y = int(x), int(y)
        data_info['nz_col'].add(x)
        data_info['nz_line'].add(y)
        data_info['gene_list'].add(gene)
        min_x, min_y, max_x, max_y = extremum(x, y, min_x, min_y, max_x, max_y)
        point = ipt.readline().strip()
    data_info['info'] = [min_x, min_y, max_x, max_y, grid_size]
    data_info = info_sort(data_info)
    ipt.close()
    return data_info


def format_data(data_file, data_info):
    ipt = open(data_file, 'r')
    ipt.readline()
    min_x, min_y, max_x, max_y, grid_size = data_info['info']
    last_col_range = list(range(max_x+1-grid_size, max_x))
    last_line_range = list(range(max_y+1-grid_size, max_y))
    last_colMBR_idx = math.ceil((max_x-min_x+1)/grid_size)
    last_lineMBR_idx = math.ceil((max_y-min_y+1)/grid_size)
    data_stat = {'col': [0] * last_colMBR_idx, 'line': [0] * last_lineMBR_idx}
    data_format = {}
    point = ipt.readline().strip()
    while point:
        gene, x, y, value = point.split('\t')
        x, y = int(x), int(y)
        trans_x = int((x-min_x)/grid_size)
        trans_y = int((y-min_y)/grid_size)
        if trans_y not in data_format.keys():
            data_format[trans_y] = {}
        if trans_x not in data_format[trans_y].keys():
            data_format[trans_y][trans_x] = [0]
        data_stat['line'][trans_y] += 1
        data_stat['col'][trans_x] += 1
        data_format[trans_y][trans_x].append(':'.join([gene, str(x), str(y), value]))
        data_format[trans_y][trans_x][0] += 1
        point = ipt.readline().strip()
    return data_stat, data_format


def load_data(data_file, grid_size):
    data_info = matrix_info(data_file, grid_size)
    # print(data_info)
    data_stat, data_format = format_data(data_file, data_info)


if __name__ == '__main__':
    file = "C:/Users/chenyujie/Desktop/Test/new_spatial_1w.txt"
    grid = 5
    st = time.time()
    load_data(file, grid)
    ed = time.time()
    print("run_time = ", ed-st, 's')
