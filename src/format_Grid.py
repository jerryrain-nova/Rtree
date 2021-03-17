import time
from src import load_grid


def main(raw_file, index_file, data_file, grid_size):
    data_grid = load_grid.load_data(raw_file, grid_size)



if __name__ == '__main__':
    start_time = time.time()
    file = "C:/Users/chenyujie/Desktop/Test/spatial_1w.txt"
    index = "C:/Users/chenyujie/Desktop/Test/spatial_format_index.txt"
    out = "C:/Users/chenyujie/Desktop/Test/spatial_format_data.txt"
    grid = 5
    main(file, index, out, grid)
    end_time = time.time()
    print("run_time = ", end_time - start_time, 's')