def coordinate_trans(index_file, init, target):
    idx = open(index_file, 'r')
    x_size, y_size = idx.readline().strip().split(',')
    x_size, y_size = int(x_size), int(y_size)
    x_trans = y_trans = []
    if target % init != 0:
        print("Can't complete BinSize transform")
        quit()
    if target % init == 0:
        x_trans = list(range(0, x_size, target))
        y_trans = list(range(0, y_size, target))

    idx.close()
    return x_trans, y_trans


def create_bin_block(init_line, stop_line, multi):
    init = init_line/multi
    stop = stop_line/multi
    block = {}
    for i in range(init, stop+1):
        block[i] = []
    return block


def data_trans(index_file, data_file, x_trans, y_trans, init, target):
    idx = open(index_file, 'r')
    dt = open(data_file, 'r')
    multi = target/init
    idx.readline()
    line_idx = list(map(int, idx.readline().strip().split(':')))
    for block_idx in range(0, len(line_idx), 2):
        init_line = line_idx[block_idx]
        stop_line = line_idx[block_idx+1]
        block = create_bin_block(init_line, stop_line, multi)
        col_idx = list(map(int, idx.readline().strip().split(':')))
        data_idx = list(map(int, idx.readline().strip().split(',')[:-1]))
        dt.seek(data_idx[0])
        date_inLine = dt.read(data_idx[-1]-data_idx[0])

        for point in date_inLine.split(',')[:-1]:
                gene, x, y, value = point.split(':')


        line_bin = list(range(init_line, stop_line+1, target/init))
        for i in


def main(index_file, data_file, out_file, init, target):
    x_trans, y_trans = coordinate_trans(index_file, init, target)
    data_trans(index_file, data_file, x_trans, y_trans, init, target)


if __name__ == '__main__':
    index = "C:/Users/chenyujie/Desktop/Test/spatial_format_index.txt"
    data = "C:/Users/chenyujie/Desktop/Test/spatial_format_data.txt"
    init_bin = 1
    target_bin = 5
    out = "C:/Users/chenyujie/Desktop/Test/spatial_format_bin" + str(target_bin) + ".txt"
    main(index, data, out, init_bin, target_bin)

