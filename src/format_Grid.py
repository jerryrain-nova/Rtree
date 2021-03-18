import time
import numpy as np
import pandas as pd
from src import load_grid


def grid_info(data):
    info = {'info': data['info'], 'gene_list': data['gene_list'], 'nz_block': data['nz_block']}
    zero_col = list(set(list(range(data['info'][0] + 1))).difference(data['nz_col']))
    info['zero_col'] = sorted(zero_col)
    info['zero_line'] = list(set(list(range(data['info'][1] + 1))).difference(data['nz_line']))
    [data.pop(k) for k in ['info', 'nz_line', 'nz_col', 'nz_block', 'gene_list']]
    return info, data


def format_grid(data, grid_size):
    grid_data = {}
    for line_key in data.keys():
        num = data[line_key]['num']
        grid_data[line_key] = {'num': num, 'nz_col': set(), 'nz_block': set()}
        block_data = np.asarray(data[line_key]['data']).reshape(num, 4)
        block_data = pd.DataFrame(block_data, columns=['gene', 'x', 'y', 'value'])
        block_data[['x', 'y', 'value']] = block_data[['x', 'y', 'value']].apply(pd.to_numeric)
        block_data = block_data.sort_values(by='x')
        for point in block_data.itertuples():
            gene, x, y, value = getattr(point, 'gene'), getattr(point, 'x'), getattr(point, 'y'), \
                                getattr(point, 'value')
            col_idx = int(x / grid_size)
            if col_idx not in grid_data[line_key].keys():
                grid_data[line_key][col_idx] = [0]
            grid_data[line_key][col_idx].append(':'.join([gene, str(x), str(y), str(value)]))
            grid_data[line_key][col_idx][0] += 1
            grid_data[line_key]['nz_col'].add(x)
            grid_data[line_key]['nz_block'].add(col_idx)
    return grid_data


def main(raw_file, index_file, data_file, grid_size):
    data_grid = load_grid.load_data(raw_file, grid_size)
    info_dict, data_grid = grid_info(data_grid)
    data_grid = format_grid(data_grid, grid_size)
    print(data_grid[0]['nz_col'])
    print(data_grid[0]['nz_block'])
    print(info_dict['zero_line'])
    print(info_dict['zero_col'])


if __name__ == '__main__':
    start_time = time.time()
    file = "C:/Users/chenyujie/Desktop/Test/spatial_1w.txt"
    index = "C:/Users/chenyujie/Desktop/Test/spatial_format_index.txt"
    out = "C:/Users/chenyujie/Desktop/Test/spatial_format_data.txt"
    grid = 5
    main(file, index, out, grid)
    end_time = time.time()
    print("run_time = ", end_time - start_time, 's')
