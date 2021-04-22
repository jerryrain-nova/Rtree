from sys import argv
import time


def trans_bin(index_file, data_file, target):
    data_ipt = open(data_file, 'r')
    index_ipt = open(index_file, 'r')
    target = int(target)
    min_x, min_y, max_x, max_y, grid_size = list(map(int, index_ipt.readline().strip().split(',')))
    info = [min_x, min_y, max_x, max_y, grid_size, target]
    if target % grid_size != 0:
        quit("Can't transform data from " + str(grid_size) + " to " + str(target))

    times = target // grid_size
    last_lineBin_idx = max_y // target
    last_colBin_idx = max_x // target
    last_col_range = list(range(max_x // grid_size + 1 - times, last_colBin_idx * times))
    last_line_range = list(range(max_y // grid_size + 1 - times, last_lineBin_idx * times))

    line_list = list(map(int, index_ipt.readline().strip().split(',')))
    trans_line_list = list(map(lambda x: x // times, line_list))
    all_col_list = index_ipt.readlines()
    seek_pos_list = list(map(int, all_col_list[-1].strip().split(',')))

    trans_data = {}
    for i in range(len(trans_line_list)):
        if trans_line_list[i] not in trans_data.keys():
            trans_data[trans_line_list[i]] = {}
        col_list = list(map(int, all_col_list[2 * i].strip().split(',')))
        trans_col_list = list(map(lambda x: x // times, col_list))
        col_pos_list = list(map(int, all_col_list[2 * i + 1].strip().split(',')[:-1]))
        col_pos_list.insert(0, 0)
        last_col = trans_col_list[0]
        last_idx = col_pos_list[0]
        seek_pos = seek_pos_list[i]
        data_ipt.seek(seek_pos)
        for col_idx in range(len(trans_col_list)):
            if trans_col_list[col_idx] == last_col:
                continue
            if trans_col_list[col_idx - 1] not in trans_data[trans_line_list[i]].keys():
                trans_data[trans_line_list[i]][trans_col_list[col_idx - 1]] = {}
            data_read = data_ipt.read(col_pos_list[col_idx] - last_idx)
            last_idx = col_pos_list[col_idx]
            last_col = trans_col_list[col_idx]
            blocks = data_read.split(',')[:-1]
            for block in blocks:
                points = block.split(';')
                for point in points:
                    gene, x, y, value = point.split(':')
                    if gene not in trans_data[trans_line_list[i]][trans_col_list[col_idx - 1]].keys():
                        trans_data[trans_line_list[i]][trans_col_list[col_idx - 1]][gene] = 0
                    trans_data[trans_line_list[i]][trans_col_list[col_idx - 1]][gene] += int(value)

                    if line_list[i] in last_line_range:
                        if last_lineBin_idx not in trans_data.keys():
                            trans_data[last_lineBin_idx] = {}
                        if trans_col_list[col_idx - 1] not in trans_data[last_lineBin_idx].keys():
                            trans_data[last_lineBin_idx][trans_col_list[col_idx - 1]] = {}
                        if gene not in trans_data[last_lineBin_idx][trans_col_list[col_idx - 1]].keys():
                            trans_data[last_lineBin_idx][trans_col_list[col_idx - 1]][gene] = 0
                        trans_data[last_lineBin_idx][trans_col_list[col_idx - 1]][gene] += int(value)
                    if col_list[col_idx - 1] in last_col_range:
                        if last_colBin_idx not in trans_data[trans_line_list[i]].keys():
                            trans_data[trans_line_list[i]][last_colBin_idx] = {}
                        if gene not in trans_data[last_lineBin_idx][trans_col_list[col_idx - 1]].keys():
                            trans_data[trans_line_list[i]][last_colBin_idx][gene] = 0
                        trans_data[trans_line_list[i]][last_colBin_idx][gene] += int(value)

    # fill the last block
    data_ipt.seek(seek_pos_list[-2])
    data_read = data_ipt.read(col_pos_list[-1] - last_idx)
    if trans_col_list[-1] not in trans_data[trans_line_list[-1]].keys():
        trans_data[trans_line_list[-1]][trans_col_list[-1]] = {}
    blocks = data_read.split(',')[:-1]
    for block in blocks:
        points = block.split(';')
        for point in points:
            gene, x, y, value = point.split(':')
            if gene not in trans_data[trans_line_list[-1]][trans_col_list[-1]].keys():
                trans_data[trans_line_list[-1]][trans_col_list[-1]][gene] = 0
            trans_data[trans_line_list[-1]][trans_col_list[-1]][gene] += int(value)
    return trans_data, info


def printf_data(trans_data, info, out_file, out_index_file):
    opt = open(out_file, 'w')
    idx = open(out_index_file, 'w')
    min_x, min_y, max_x, max_y = list(map(lambda x: x//info[-1], info[:4]))
    print(','.join(list(map(str, [0, 0, max_x-min_x, max_y-min_y, info[-1]]))), file=idx)

    Bit = 0
    Bit_block = [Bit]
    print(','.join(list(map(str, sorted(list(trans_data.keys()))))), file=idx)
    for line in sorted(list(trans_data.keys())):
        bit = 0
        if not trans_data[line]:
            continue
        print(','.join(list(map(str, sorted(list(trans_data[line].keys()))))), file=idx)
        for col in sorted(list(trans_data[line].keys())):
            if not trans_data[line][col]:
                continue
            points = []
            for gene in trans_data[line][col].keys():
                point = gene + ':' + str(trans_data[line][col][gene])
                points.append(point)
            out_dt = ';'.join(points)
            print(out_dt, end=',', file=opt)
            Bit += len(out_dt.encode()) + 1
            bit += len(out_dt.encode()) + 1
            print(bit, end=',', file=idx)
        print('', file=idx)
        Bit_block.append(Bit)
    print(','.join(list(map(str, Bit_block))), file=idx)


def main(index_file, data_file, out_file, out_index_file, target):
    st = time.time()
    trans_data, info = trans_bin(index_file, data_file, target)
    trans_t = time.time()
    print("trans_time = ", trans_t - st, 's')
    printf_data(trans_data, info, out_file, out_index_file)
    ed = time.time()
    print("print_time = ", ed - trans_t, 's')
    print("run_time = ", ed - st, 's')


def rename(prefix, target, path):
    idx = path + '/' + prefix + '.index'
    dt = path + '/' + prefix + '.data'
    opt = path + '/' + prefix + '_bin' + str(target) + '.data'
    opt_idx = path + '/' + prefix + '_bin' + str(target) + '.index'
    return idx, dt, opt, opt_idx


if __name__ == '__main__':
    # index = "C:/Users/chenyujie/Desktop/Test/spatial_format_index.txt"
    # data = "C:/Users/chenyujie/Desktop/Test/spatial_format_data.txt"
    # target_bin = 15
    # out = "C:/Users/chenyujie/Desktop/Test/spatial_format_bin" + str(target_bin) + ".data"
    # out_index = "C:/Users/chenyujie/Desktop/Test/spatial_format_bin" + str(target_bin) + ".index"
    file_prefix = argv[1]
    out_path = argv[2]
    target_bin = int(argv[3])
    index, data, out, out_index = rename(file_prefix, target_bin, out_path)
    main(index, data, out, out_index, target_bin)
