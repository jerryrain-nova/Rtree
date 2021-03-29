from collections import Counter


def trans_bin(index_file, data_file, target):
    data_ipt = open(data_file, 'r')
    index_ipt = open(index_file, 'r')
    target = int(target)
    min_x, min_y, max_x, max_y, grid_size = list(map(int, index_ipt.readline().strip().split(',')))
    if target % grid_size != 0:
        quit("Can't transform data from " + str(grid_size) + " to " + str(target))

    times = target // grid_size
    line_list = list(map(int, index_ipt.readline().strip().split(',')))
    trans_line_list = list(map(lambda x: x // times, line_list))
    print(trans_line_list)
    all_col_list = index_ipt.readlines()
    seek_pos_list = list(map(int, all_col_list[-1].strip().split(',')))

    last_col_range = list(range(max_x + 1 - grid_size, max_x // grid_size * grid_size))
    last_line_range = list(range(max_y + 1 - grid_size, max_y // grid_size * grid_size))
    last_lineBin_idx = max_y // target
    last_colBin_idx = max_x // target
    data_edge = {last_colBin_idx: {}, last_lineBin_idx: {}}

    trans_data = {}
    last_line = trans_line_list[0]
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
    return trans_data


def main(index_file, data_file, out_file, out_index_file, target):
    trans_data = trans_bin(index_file, data_file, target)


if __name__ == '__main__':
    index = "C:/Users/chenyujie/Desktop/Test/spatial_format_index.txt"
    data = "C:/Users/chenyujie/Desktop/Test/spatial_format_data.txt"
    target_bin = 15
    out = "C:/Users/chenyujie/Desktop/Test/spatial_format_bin" + str(target_bin) + ".data"
    out_index = "C:/Users/chenyujie/Desktop/Test/spatial_format_bin" + str(target_bin) + ".index"
    main(index, data, out, out_index, target_bin)
