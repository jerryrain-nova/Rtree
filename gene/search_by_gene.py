import time
from sys import argv


def search(target_que, data_file, index_file, out_file):
    dt = open(data_file, 'r')
    idx = open(index_file, 'r')
    opt = open(out_file, 'w')
    st = time.time()
    gene_list = idx.readline().strip().split(',')
    site_list = idx.readline().strip().split(',')
    print("index_time = ", time.time() - st, 's')
    seek_time = 0
    read_time = 0
    print_time = 0
    for gene_target in target_que:
        print(gene_target, file=opt)
        last_time = time.time()
        if gene_target not in gene_list:
            print("No Values: ", gene_target, end='\n\n', file=opt)
            print_time += time.time() - last_time
            continue
        else:
            site = gene_list.index(gene_target)
            if site == 0:
                dt.seek(0)
                seek_stop = time.time()
                seek_time += seek_stop - last_time
                get_data = dt.read(int(site_list[0]))
                read_stop = time.time()
                read_time += read_stop - seek_stop
            else:
                dt.seek(int(site_list[site - 1]))
                seek_stop = time.time()
                seek_time += seek_stop - last_time
                get_data = dt.read(int(site_list[site]) - int(site_list[site - 1]))
                read_stop = time.time()
                read_time += read_stop - seek_stop
            result = '\n'.join(get_data.split(',')[:-1])
            print_time += time.time() - read_stop
        print(result, end='\n\n', file=opt)
    ed = time.time()
    print("seek = ", len(target_que))
    print("seek_time = ", seek_time, 's')
    print("read_time = ", read_time, 's')
    print("print_time = ", print_time, 's')
    print("search_time = ", ed - st, 's')


def target_list(target_file):
    que = []
    with open(target_file, 'r') as ipt:
        for gene in ipt:
            gene = gene.strip()
            que.append(gene)
    return que


def main(target_file, data_file, index_file, out_file):
    st = time.time()
    target_que = target_list(target_file)
    load_t = time.time()
    print("load_target time =", load_t - st, 's')
    search(target_que, data_file, index_file, out_file)
    ed = time.time()
    print("run time =", ed-st, 's')


if __name__ == '__main__':
    # data = "C:/Users/chenyujie/Desktop/Test/spatial_format_gene.data"
    # index = "C:/Users/chenyujie/Desktop/Test/spatial_format_gene.index"
    # out = "C:/Users/chenyujie/Desktop/Test/spatial_format_search.result"
    # target = "C:/Users/chenyujie/Desktop/Test/spatial_gene.list"
    file_path = argv[1]
    index = file_path + '.index'
    data = file_path + '.data'
    out = file_path + '_search.result'
    target = argv[2]
    main(target, data, index, out)
