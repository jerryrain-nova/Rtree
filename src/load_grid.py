def load_data(data_file, grid_size):
    ipt = open(data_file, 'r')
    ipt.readline()
    max_x = max_y = 0
    gene_list = set()
    grid_block = {'info': [max_x, max_y, grid_size], 'nz_line': set(), 'nz_col': set(),
                  'nz_block': [], 'gene_list': []}
    point = ipt.readline().strip()
    while point:
        gene, x, y, value = point.split('\t')
        x, y = int(x), int(y)
        grid_block["nz_line"].add(y)
        grid_block['nz_col'].add(x)
        line_idx = int(y / grid_size)
        if line_idx not in grid_block.keys():
            grid_block[line_idx] = {'num': 0, 'data': []}
            grid_block['nz_block'].append(line_idx)
        if x >= max_x:
            max_x = x
        if y >= max_y:
            max_y = y
        # grid_block[line_idx][col_idx].append([gene, x, y, value])
        # grid_block[line_idx][col_idx][0] += 1
        grid_block[line_idx]['data'].extend([gene, x, y, value])
        grid_block[line_idx]['num'] += 1
        gene_list.add(gene)
        point = ipt.readline().strip()
    grid_block['info'] = [max_x, max_y, grid_size]
    grid_block['nz_col'] = sorted(grid_block['nz_col'])
    grid_block['gene_list'] = sorted(list(gene_list))
    return grid_block


if __name__ == '__main__':
    file = "C:/Users/chenyujie/Desktop/Test/spatial_1kw.txt"
    grid = 5
    data = load_data(file, grid)
    print(data['zero_col'])
    print(data['zero_line'])
