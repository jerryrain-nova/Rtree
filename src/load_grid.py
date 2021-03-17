def load_data(data_file, grid_size):
    ipt = open(data_file, 'r')
    ipt.readline()
    max_x = max_y = 0
    grid_block = {'info': [max_x, max_y, grid_size], 'zero_line': [], 'zero_col': [], 'nz_line': [], 'nz_col': [],
                  'nz_block': []}
    point = ipt.readline().strip()
    while point:
        gene, x, y, value = point.split('\t')
        x, y = int(x), int(y)
        if y not in grid_block['nz_line']:
            grid_block['nz_line'].append(y)
        if x not in grid_block['nz_col']:
            grid_block['nz_col'].append(x)
        line_idx = int(y / grid_size)
        col_idx = int(x / grid_size)
        if line_idx not in grid_block.keys():
            grid_block[line_idx] = {'num': 0, 'nz_block': []}
            grid_block['nz_block'].append(line_idx)
        if col_idx not in grid_block[line_idx].keys():
            grid_block[line_idx][col_idx] = [0]
            grid_block[line_idx]['nz_block'].append(col_idx)
        if x >= max_x:
            max_x = x
        if y >= max_y:
            max_y = y
        grid_block[line_idx][col_idx].append(':'.join([gene, str(x), str(y), value]))
        grid_block[line_idx]['num'] += 1
        grid_block[line_idx][col_idx][0] += 1
        point = ipt.readline().strip()
    grid_block['info'] = [max_x, max_y, grid_size]
    grid_block['nz_col'] = sorted(grid_block['nz_col'])
    grid_block['zero_col'] = list(set(list(range(grid_block['info'][0] + 1))).difference(set(grid_block['nz_col'])))
    grid_block['zero_line'] = list(set(list(range(grid_block['info'][1] + 1))).difference(set(grid_block['nz_line'])))
    grid_block['zero_col'] = sorted(grid_block['zero_col'])
    return grid_block


if __name__ == '__main__':
    file = "C:/Users/chenyujie/Desktop/Test/spatial_1kw.txt"
    grid = 5
    data = load_data(file, grid)
    print(data['zero_col'])
    print(data['zero_line'])
