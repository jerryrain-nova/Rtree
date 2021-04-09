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


def gene_collect(ipt_file, grid_size):
    gene_collection = {}

    ipt = open(ipt_file, 'r')
    ipt.readline()
    point = ipt.readline()
    min_x = max_x = int(point.strip().split('\t')[1])
    min_y = max_y = int(point.strip().split('\t')[2])
    while point:
        point = point.strip().split('\t')
        gene = point[0]
        x, y, count = list(map(int, point[1:]))
        if gene not in gene_collection.keys():
            gene_collection[gene] = 0
        gene_collection[gene] += 1
        min_x, min_y, max_x, max_y = extremum(x, y, min_x, min_y, max_x, max_y)
        point = ipt.readline()
    info = [min_x, min_y, max_x, max_y, grid_size]
    return gene_collection, info


def grid_collect(ipt_file, info):
    min_x, min_y, max_x, max_y, grid_size = info
    grid_collection = {}
    ipt = open(ipt_file, 'r')
    ipt.readline()
    point = ipt.readline()
    while point:
        point = point.strip().split('\t')
        x, y, count = list(map(int, point[1:]))
        mbr_x = (x-min_x)//grid_size
        mbr_y = (y-min_y)//grid_size
        if mbr_y not in grid_collection.keys():
            grid_collection[mbr_y] = {}
        if mbr_x not in grid_collection[mbr_y].keys():
            grid_collection[mbr_y][mbr_x] = 0
        grid_collection[mbr_y][mbr_x] += 1
        point = ipt.readline()
    return grid_collection


def gene_display(gene_collection):
    num_list = list(set(gene_collection.values()))
    gene_stat = {}
    for num in num_list:
        gene_stat[num] = 0
    for gene in gene_collection.keys():
        gene_stat[gene_collection[gene]] += 1
    return gene_stat


def grid_display(grid_collection):
    grid_stat = {}
    for line in grid_collection.keys():
        for col in grid_collection[line].keys():
            if grid_collection[line][col] not in grid_stat.keys():
                grid_stat[grid_collection[line][col]] = 0
            grid_stat[grid_collection[line][col]] += 1
    return grid_stat


def printf_stat(gene_stat, grid_stat, gene_opt_file, grid_opt_file):
    gene_opt = open(gene_opt_file, 'w')
    grid_opt = open(grid_opt_file, 'w')
    opt_query = [gene_opt, grid_opt]
    stat_query = [gene_stat, grid_stat]
    for query in stat_query:
        for num in sorted(list(query.keys())):
            print(num, '\t', query[num], file=opt_query[stat_query.index(query)])


def main(ipt_file, grid_size, gene_opt_file, grid_opt_file):
    gene_collection, info = gene_collect(ipt_file, grid_size)
    grid_collection = grid_collect(ipt_file, info)
    gene_stat = gene_display(gene_collection)
    grid_stat = grid_display(grid_collection)
    printf_stat(gene_stat, grid_stat, gene_opt_file, grid_opt_file)


def rename(ipt_file, path):
    prefix = '.'.join(ipt_file.split('/')[-1].split('.')[:-1])
    gene_opt_file = path + '/' + prefix + '_gene.stat'
    grid_opt_file = path + '/' + prefix + '_grid.stat'
    return gene_opt_file, grid_opt_file


if __name__ == '__main__':
    # file = "C:/Users/chenyujie/Desktop/Test/new_spatial_1w.txt"
    # out_path = "C:/Users/chenyujie/Desktop/Test"
    # grid = 5
    file = argv[1]
    out_path = argv[2]
    grid = int(argv[3])
    gene_file, grid_file = rename(file, out_path)
    main(file, grid, gene_file, grid_file)
