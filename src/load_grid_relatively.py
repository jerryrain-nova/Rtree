import time
from sys import argv


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
    data_info['gene_list'] = sorted(list(data_info['gene_list']))
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
    last_colMBR_idx = int((max_x-min_x)/grid_size)
    last_lineMBR_idx = int((max_y-min_y)/grid_size)
    data_stat = {'col': [0] * (last_colMBR_idx+1), 'line': [0] * (last_lineMBR_idx+1)}
    data_format = {}
    data_edge = {last_colMBR_idx: {}, last_lineMBR_idx: {}}
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
        if x in last_col_range:
            if trans_y not in data_edge[last_colMBR_idx].keys():
                data_edge[last_colMBR_idx][trans_y] = []
            data_edge[last_colMBR_idx][trans_y].append(':'.join([gene, str(x), str(y), value]))
        if y in last_line_range:
            if trans_x not in data_edge[last_lineMBR_idx].keys():
                data_edge[last_lineMBR_idx][trans_x] = []
            data_edge[last_lineMBR_idx][trans_x].append(':'.join([gene, str(x), str(y), value]))
        data_stat['line'][trans_y] += 1
        data_stat['col'][trans_x] += 1
        data_format[trans_y][trans_x].append(':'.join([gene, str(x), str(y), value]))
        data_format[trans_y][trans_x][0] += 1
        point = ipt.readline().strip()
    return data_stat, data_format, data_edge


def data_merge(data_format, data_edge):
    last_col, last_line = list(data_edge.keys())
    for line_key in data_edge[last_col]:
        if last_col not in data_format[line_key].keys():
            data_format[line_key][last_col] = []
        data_format[line_key][last_col].extend(data_edge[last_col][line_key])
    for col_key in data_edge[last_line]:
        if col_key not in data_format[last_line].keys():
            data_format[last_line][col_key] = []
        data_format[last_line][col_key].extend(data_edge[last_line][col_key])
    return data_format


def build_index(data_format, data_info, data_stat):
    nz_col = data_info['nz_col']
    nz_line = data_info['nz_line']
    for query in [nz_line, nz_col]:
        last_idx = init_idx = query[0]
        opt_list = []
        num = 0
        for idx in query:
            if idx - last_idx > 1:
                opt_list.extend([init_idx, last_idx])
                init_idx = idx
                num += 1
            last_idx = idx
        print("block_num = ", num)
        print(opt_list)


def printf_data(index_file, out_file, data_format, data_info, data_stat):
    opt = open(out_file, 'w')
    idx = open(index_file, 'w')
    print(','.join(list(map(str, list(data_info['info'])))), file=idx)

    Bit = 0
    Bit_block = [Bit]
    print(','.join(list(map(str, sorted(list(data_format.keys()))))), file=idx)
    for line in sorted(list(data_format.keys())):
        bit = 0
        print(','.join(list(map(str, sorted(list(data_format[line].keys()))))), file=idx)
        for col in sorted(list(data_format[line].keys())):
            print(';'.join(data_format[line][col][1:]), end=',', file=opt)
            Bit += len(','.join(data_format[line][col][1:]).encode()) + 1
            bit += len(','.join(data_format[line][col][1:]).encode()) + 1
            print(bit, end=',', file=idx)
        print('', file=idx)
        Bit_block.append(Bit)
    print(','.join(list(map(str, Bit_block))), file=idx)


def main(data_file, index_file, out_file, grid_size):
    data_info = matrix_info(data_file, grid_size)
    data_stat, data_format, data_edge = format_data(data_file, data_info)
    data_format = data_merge(data_format, data_edge)
    # build_index(data_format, data_info, data_stat)
    print(data_format.keys())
    printf_data(index_file, out_file, data_format, data_info, data_stat)


def rename_out(input_file, opt_path):
    path = input_file.split('/')[-1]
    prefix = path.split('.')[:-1]
    prefix = '.'.join(prefix)
    out_data = opt_path + '/' + prefix + '_data.txt'
    out_index = opt_path + '/' + prefix + '_index.txt'
    return out_data, out_index


if __name__ == '__main__':
    file = "C:/Users/chenyujie/Desktop/Test/new_spatial_1w.txt"
    index = "C:/Users/chenyujie/Desktop/Test/spatial_format_index.txt"
    out = "C:/Users/chenyujie/Desktop/Test/spatial_format_data.txt"
    # file = argv[1]
    # out_path = argv[2]
    # out, index = rename_out(file, out_path)
    grid = 5
    st = time.time()
    main(file, index, out, grid)
    ed = time.time()
    print("run_time = ", ed-st, 's')
