from sys import argv
from src import build_btree
from struct import pack
import time


class DataKey:
    def __init__(self, ipt, opt, idx, r):
        self.file = ipt
        self.opt = opt
        self.idx = idx
        self._rank = r

        self._border = False
        self._x_mi = None
        self._x_ma = None
        self._y_mi = None
        self._y_ma = None

        self.all_gene = set()
        self.x_list = []
        self.y_list = []
        self.gene_list = []
        self.value_list = []
        self.bptree = None

    def border_change(self, x, y):
        if self._x_mi > x:
            self._x_mi = x
        if self._x_ma < x:
            self._x_ma = x
        if self._y_mi > y:
            self._y_mi = y
        if self._y_ma < y:
            self._y_ma = y

    @property
    def border_print(self):
        return self._x_mi, self._x_ma, self._y_mi, self._y_ma

    @property
    def rank(self):
        return self._rank

    def load(self):
        data = open(self.file, 'r')
        data.readline()
        point = data.readline().strip()
        while point:
            gene, x, y, value = point.split('\t')
            x, y, value = int(x), int(y), int(value)
            if not self._border:
                self._x_mi = self._x_ma = x
                self._y_mi = self._y_ma = y
                self._border = True
            self.border_change(x, y)
            self.x_list.append(x)
            self.y_list.append(y)
            self.gene_list.append(gene)
            self.value_list.append(value)
            self.all_gene.add(gene)
            point = data.readline().strip()
        self.all_gene = sorted(self.all_gene)

    # def data_print(self):
    #     opt = open(self.opt, 'wb')
    #     self.all_gene = list(sorted(self.all_gene))
    #     cache = b''
    #     for i in range(len(self.x_list)):
    #         key = pack('4I', self.x_list[i], self.y_list[i], self.all_gene.index(self.gene_list[i]), self.value_list[i])
    #         if i % self.rank == 0 and i != 0:
    #             opt.write(cache)
    #             cache = b''
    #         cache += key

    def build_bptree(self):
        st = time.time()
        self.bptree = build_btree.Btree(self.rank)
        for i in range(len(self.x_list)):
            primekey = str(self.x_list[i])+str(self.y_list[i])
            kv = build_btree.BKeyWord(int(primekey), str(list(self.all_gene).index(self.gene_list[i]))+':'+str(self.value_list[i]))
            self.bptree.insert(kv)
        build_ed = time.time()
        self.bptree.leaf_tosave(self.opt)
        print("height =", self.bptree.H)
        self.bptree.show()
        self.bptree.node_tosave(self.idx)
        print("\tbuild_time =", build_ed-st, 's')

        bptree_idx = build_btree.BtreeIndex()
        bptree_idx.load_index(self.idx)




class Project:
    def __init__(self, ipt, pt):
        self.file = ipt
        self.path = pt
        self.opt = None
        self.idx = None
        self.file_name()
        self._rank = 5

    def __str__(self):
        return "Transform Result Path(Rank=%s):\nData:%s\nIndex:%s" % (self._rank, self.opt, self.idx)

    @property
    def rank(self):
        return self._rank

    def file_name(self):
        prefix = self.file.split('/')[-1].split('.')[0]
        self.opt = self.path + '/' + prefix + '.data'
        self.idx = self.path + '/' + prefix + '.index'

    def do(self):
        st = time.time()
        projectA = DataKey(self.file, self.opt, self.idx, self.rank)
        init_ed = time.time()
        projectA.load()
        load_ed = time.time()
        projectA.build_bptree()
        ed = time.time()
        print(projectA.border_print)
        print("init_time =", init_ed-st, 's')
        print("load_time =", load_ed-init_ed, 's')
        print("run_time =", ed-st, 's')


if __name__ == '__main__':
    file = "C:/Users/chenyujie/Desktop/Test/new_spatial_100.txt"
    path = "C:/Users/chenyujie/Desktop/Test"
    project = Project(file, path)
    project.do()

