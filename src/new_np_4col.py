import numpy as np
from itertools import chain
from time import time
import gc
from sys import argv


class Block:
    __slots__ = ('_M', 'x', 'y', 'num', 'gene', 'value')

    def __init__(self):
        self._M = 256
        self.num = 0
        self.gene = []
        self.x = []
        self.y = []
        self.value = []

    @property
    def M(self):
        return self._M

    # def isfull(self, num):
    #     return self._M < self.num + num

    def insert(self, gene, x, y, value):
        self.num += len(gene)
        self.gene.extend(gene)
        self.x.extend(x)
        self.y.extend(y)
        self.value.extend(value)


class Blocks:
    def __init__(self):
        self.index = 0
        self.data = []

    def __iter__(self):
        return self

    def __next__(self):
        while self.index < len(self.data):
            block = self.data[self.index]
            self.index += 1
            return block
        else:
            self.index = 0
            raise StopIteration

    def insert(self, block):
        self.data.append(block)


class Data:
    def __init__(self, gene, x, y, value):
        self.xmin = self.xmax = x
        self.ymin = self.ymax = y
        self.gene = [gene]
        self.x = [x]
        self.y = [y]
        self.value = [value]

        self.y_index = None
        self.sorted_idx_part = []

    def border(self):
        return list(map(str, [self.xmin, self.xmax, self.ymin, self.ymax]))

    def update_border(self, x, y):
        if x < self.xmin:
            self.xmin = x
        elif x > self.xmax:
            self.xmax = x
        if y < self.ymin:
            self.ymin = y
        elif y > self.ymax:
            self.ymax = y

    def insert(self, gene, x, y, value):
        self.gene.append(gene)
        self.x.append(x)
        self.y.append(y)
        self.value.append(value)
        self.update_border(x, y)

    @staticmethod
    def cut_list(iptLsit):
        st = ed = 0
        iptList_cutted = []
        for i in range(len(iptLsit)):
            if iptLsit[i] - iptLsit[ed] > 1:
                iptList_cutted.extend([st, ed])
                st = i
            ed = i
            if i == len(iptLsit)-1:
                iptList_cutted.extend([st, ed])
        return iptList_cutted

    def sort(self):
        self.x = np.asarray(self.x, dtype=np.uint32)
        self.y = np.asarray(self.y, dtype=np.uint32)
        self.gene = np.asarray(self.gene)
        self.value = np.asarray(self.value, dtype=np.uint8)
        y_sorted_idx = self.y.argsort()
        x_sorted = self.x[y_sorted_idx]
        self.y_index = np.sort(self.y)
        y_cutted_idx = self.cut_list(self.y_index)
        for i in range(0, len(y_cutted_idx), 2):
            x_range = x_sorted[y_cutted_idx[i]:y_cutted_idx[i+1]+1]
            x_range_sorted_idx = x_range.argsort()
            x_sorted_idx_range = y_sorted_idx[y_cutted_idx[i]:y_cutted_idx[i+1]+1][x_range_sorted_idx].astype(np.uint32)
            self.sorted_idx_part.append(x_sorted_idx_range)

        sorted_idx = np.asarray(list(chain(*self.sorted_idx_part)), dtype=np.uint32)
        self.y_index = self.y_index[y_cutted_idx]
        self.y = self.y[sorted_idx]
        self.x = self.x[sorted_idx]
        self.gene = self.gene[sorted_idx]
        self.value = self.value[sorted_idx]

    def block(self):
        idx = 0
        blocks = Blocks()
        block = Block()
        t = 0
        blocks_num = np.asarray(list(range(len(self.sorted_idx_part))), dtype=np.uint32)
        for y in self.sorted_idx_part:
            num = len(y)
            gene_range = self.gene[idx:idx+num]
            x_range = self.x[idx:idx+num]
            y_range = self.y[idx:idx+num]
            value_range = self.value[idx:idx+num]
            idx += num
            blocks_num[t] = (num-1)//block.M
            t += 1
            for i in range(0, num, block.M):
                block = Block()
                block.insert(gene_range[i:i+block.M], x_range[i:i+block.M], y_range[i:i+block.M], value_range[i:i+block.M])
                blocks.insert(block)
        return blocks, blocks_num

    def printf(self, blocks, blocks_num, data_file, idx_file, gene_file):
        dt = open(data_file, 'w')
        index = open(idx_file, 'w')
        gn = open(gene_file, 'w')
        idx = 0

        print(','.join(self.border()), file=index)
        print(':'.join(list(map(str, self.y_index.tolist()))), file=index)

        d = st = 0
        x_index = []
        bits = [st]
        last_b = 0

        gene_list = sorted(set(self.gene))
        geneDict = {}.fromkeys(gene_list)

        cell_list = sorted(set(self.cell))
        cellDict = {}.fromkeys(cell_list)

        for block in blocks:
            points = []
            if d <= blocks_num[idx]:
                x_index.extend([min(block.x), max(block.x)])
                d += 1
            else:
                print(':'.join(list(map(str, x_index))), file=index)
                print(','.join(list(map(str, bits))), file=index)
                bits = [st]
                x_index = [[min(block.x), max(block.x)]]
                d = 1
                idx += 1
            for i in range(block.num):
                point = ':'.join(list(map(str, [block.gene[i], block.x[i], block.y[i], block.value[i]])))
                points.append(point)
                bit = len(point)+1
                st += bit

                if geneDict[block.gene[i]] is None:
                    geneDict[block.gene[i]] = [last_b, bit-1]
                else:
                    geneDict[block.gene[i]].extend([last_b, bit-1])
                last_b = st

            bits.append(st)
            print(','.join(points) + ',', end='', file=dt)

        print(','.join(list(gene_list)), file=gn)
        for gene in gene_list:
            print(','.join(map(str, geneDict[gene])), file=gn)
        del gene_list, geneDict
        gc.collect()


def load_data(file):
    ipt = open(file, 'r')
    ipt.readline()
    point = ipt.readline()
    gene, x, y, value= point.strip().split('\t')
    data = Data(gene, int(x), int(y), value)
    point = ipt.readline()
    while point:
        gene, x, y, value = point.strip().split('\t')
        data.insert(gene, int(x), int(y), value)
        point = ipt.readline()
    return data


def rename_out(ipt_file, opt_path):
    path = ipt_file.split('/')[-1]
    prefix = path.split('.')[:-1]
    prefix = '.'.join(prefix)
    out_data = opt_path + '/' + prefix + '.data'
    out_index = opt_path + '/' + prefix + '.index'
    out_gene = opt_path + '/' + prefix + '.gene'
    return out_data, out_index, out_gene


def main():
    st = time()
    # file = "C:/Users/chenyujie/Desktop/Test/Cell_sample_1M.txt"
    # out_path = "C:/Users/chenyujie/Desktop/Test"
    file = argv[1]
    out_path = argv[2]
    f_data, f_index, f_gene = rename_out(file, out_path)
    data = load_data(file)
    load_t = time()
    data.sort()
    sort_t = time()
    blocks, blocks_num = data.block()
    block_t = time()
    data.printf(blocks, blocks_num, f_data, f_index, f_gene)
    ed = time()
    print("load time = ", load_t-st, 's')
    print("sort time = ", sort_t-load_t, 's')
    print("block time = ", block_t-sort_t, 's')
    print("print time = ", ed - block_t, 's')
    print("\n\trun time = ", ed-st, 's')


if __name__ == '__main__':
    main()