def bin_cut(index_file, init, target):
    idx = open(index_file, 'r')
    x, y = idx.readline().strip().split(',')
    x, y = int(x), int(y)



def main(index_file, data_file, out_file, init, target):



if __name__ == '__main__':
    index = "C:/Users/chenyujie/Desktop/Test/spatial_format_index.txt"
    data = "C:/Users/chenyujie/Desktop/Test/spatial_format_data.txt"
    init_bin = '3'
    target_bin = '7'
    out = "C:/Users/chenyujie/Desktop/Test/spatial_format_bin" + target_bin + ".txt"
    main(index, data, out, init_bin, target_bin)

