def search(gene_target, data_file, index_file, out_file):
    dt = open(data_file, 'r')
    idx = open(index_file, 'r')
    opt = open(out_file, 'w')
    gene_list = idx.readline().strip().split(',')
    site_list = idx.readline().strip().split(',')
    result = False
    if gene_target not in gene_list:
        print("No Gene")
        quit()
    else:
        site = gene_list.index(gene_target)
        if site == 0:
            dt.seek(0)
            get_data = dt.read(int(site_list[0]))
        else:
            dt.seek(int(site_list[site - 1]))
            get_data = dt.read(int(site_list[site]) - int(site_list[site - 1]))
        result = '\n'.join(get_data.split(',')[:-1])
    print(result, file=opt)


def main(gene_target, data_file, index_file, out_file):
    search(gene_target, data_file, index_file, out_file)


if __name__ == '__main__':
    data = "C:/Users/chenyujie/Desktop/Test/spatial_format_gene.data"
    index = "C:/Users/chenyujie/Desktop/Test/spatial_format_gene.index"
    out = "C:/Users/chenyujie/Desktop/Test/spatial_format_search.result"
    target = 'Gm42418'
    main(target, data, index, out)
