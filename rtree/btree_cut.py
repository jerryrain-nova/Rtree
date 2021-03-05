import numpy as np


class Leaf:
    def __init__(self):
        self.father = None
        self.minsize_idx = None
        self.length = 0
        self.element = []

    def __str__(self):
        return "range: %s, length: %s, element: %s" % (str(self.range), str(self.length), self.element)


class Node:
    def __init__(self):
        self.left = None
        self.right = None
        self.index = []

    def __str__(self):
        return "Index: %s" % self.index


class BTree:
    def __init__(self, key, num, minsize=500):
        self.root = Node()
        self.key_list = key
        self.num_list = num
        self.minsize = minsize
        self.leaves = []

    @staticmethod
    def _split_item(lf):
        item_split = [[], []]
        item = np.asarray(lf.element)
        split_idx = lf.minsize_idx + 1
        item_split[0], item_split[1] = item[:split_idx], item[split_idx:]
        lf.element = item_split[0]
        length = item_split[1].sum()
        return item_split[1].tolist(), length

    def build_tree(self):
        lf = Leaf()
        idxs = range(len(self.num_list))
        init_lower, fin_upper = key_list[0].split('-')
        for idx in idxs:
            num = int(num_list[idx])
            if lf.length > 2*self.minsize:
                split_element, length = self._split_item(lf)
                lf = Leaf()
                lf.length = length
                lf.element = split_element
            upper = int(key_list[idx].split('-')[1])
            lf.element.append(num)
            if lf.length + num >= self.minsize:
                lf.minsize_idx = idx
            lf.length += num

            fin_upper = upper



if __name__ == '__main__':
    file = "C:/Users/chenyujie/Desktop/Test/block_test.txt"
    input = open(file, 'rt')
    key_list = input.readline().strip().strip('[').strip(']').split(',')
    num_list = input.readline().strip().strip('[').strip(']').split(',')
    num_list = list(map(int, num_list))
    for idx in range(len(key_list)):
        new_key = key_list[idx].strip(' ').strip('\'')
        key_list[idx] = new_key
    btree_build = BTree(key_list, num_list)
