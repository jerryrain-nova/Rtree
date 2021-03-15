import time


def load_data(input_file):
    data_dict = {}
    with open(input_file, 'r') as Input:
        Input.readline()
        for line in Input:
            gene, x, y, value = line.strip().split('\t')
            point = ':'.join([x, y, value])
            if gene not in data_dict.keys():
                data_dict[gene] = []
            data_dict[gene].append(point)
    return data_dict


def classify(data_dict):
    gene_list = sorted(data_dict.keys())
    print("row_len = ", len(gene_list))
    num_list = list(map(str, range(10)))
    gene_dict = {'': [], 'same': []}
    for gene in gene_list:
        gene_prefix = ''
        for site in gene:
            if site in num_list:
                if not gene_prefix:
                    gene_dict[''].append(gene)
                else:
                    if gene_prefix not in gene_dict.keys():
                        gene_dict[gene_prefix] = []
                    gene_dict[gene_prefix].append(gene)
                break
            gene_prefix += site
            if gene_prefix == gene:
                gene_dict[gene_prefix] = [gene]
                gene_dict['same'].append(gene)
    print(gene_dict.keys())
    print("len = ", len(list(gene_dict.keys())))
    print(gene_dict['same'])


def format_data(data_dict, out_file, index_file):
    output = open(out_file, 'w')
    idx = open(index_file, 'w')
    gene_list = sorted(data_dict.keys())
    print(','.join(gene_list), file=idx)
    site = 0
    for gene in gene_list:
        for point in data_dict[gene]:
            print(point, end=',', file=output)
            site += len(point.encode()) + 1
        print(site, end=',', file=idx)


def main(input_file, out_file, index_file):
    data = load_data(input_file)
    # classify(data)
    format_data(data, out_file, index_file)


if __name__ == '__main__':
    file = "C:/Users/chenyujie/Desktop/Test/spatial_1kw.txt"
    out = "C:/Users/chenyujie/Desktop/Test/spatial_format_gene.data"
    index = "C:/Users/chenyujie/Desktop/Test/spatial_format_gene.index"
    main(file, out, index)
