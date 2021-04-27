from sys import argv
from src import build_btree
from struct import pack
import time
from bisect import bisect_left, bisect_right


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
        self._bit = None

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
        self._bit = max(len(str(self._x_ma)), len(str(self._y_ma)))

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
            x, y = int(x), int(y)
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
        self.x_list = sorted(self.x_list)
        print("load_complete")

    def primekey(self, x, y):
        query = [x, y]
        for i in range(2):
            diff = self._bit - len(query[i])
            if diff > 0:
                query[i] = ''.join(['0' * diff]) + query[i]
        primekey = query[0] + query[1]
        return int(primekey)

    def build_bptree(self):
        st = time.time()
        self.bptree = build_btree.Btree(self.rank)
        for i in range(len(self.x_list)):
            # primekey = 10**len(str(self.y_list[i]))*self.x_list[i]+self.y_list[i]
            primekey = self.primekey(str(self.x_list[i]), str(self.y_list[i]))
            # kv = build_btree.BKeyWord(primekey, self.value_list[i])
            kv = build_btree.BKeyWord(primekey, str(bisect_left(self.all_gene, self.gene_list[i]))+':'+str(self.value_list[i]))
            self.bptree.insert(kv)
        build_ed = time.time()
        print("\tbuild_time =", build_ed - st, 's')
        # self.bptree.leaf_tosave(self.opt)
        data_ed = time.time()
        print("height =", self.bptree.H)
        print("save_data =", data_ed-build_ed, 's')
        # self.bptree.show()

    def search_bptree(self, ipt_target):
        st = time.time()
        x_min, x_max = ipt_target.split(',')[0].split(':')
        y_min, y_max = ipt_target.split(',')[1].split(':')
        # mi = self.primekey(x_min, y_min)
        # ma = self.primekey(x_max, y_max)
        x_min, x_max, y_min, y_max = int(x_min), int(x_max), int(y_min), int(y_max)
        # print(mi, ma)
        _result_klist, _result_vlist = [], []
        x_lf = bisect_left(self.x_list, x_min)
        x_rh = bisect_right(self.x_list, x_max) - 1
        x_range = self.x_list[x_lf:x_rh+1]
        for x in x_range:
            mi = self.primekey(str(x), str(y_min))
            ma = self.primekey(str(x), str(y_max))
            result_klist, result_vlist = self.bptree.search_continuous(mi, ma)
            _result_klist.extend(result_klist)
            _result_vlist.extend(result_vlist)

        def filter_result(klist, vlist):
            _result_klist, _result_vlist = [], []
            for i in range(len(klist)):
                key_y = int(str(klist[i])[-self._bit:])
                if y_min <= key_y <= y_max:
                    _result_klist.append(klist[i])
                    _result_vlist.append(vlist[i])
            return _result_klist, _result_klist
        # _result_klist, _result_vlist = filter_result(result_klist, result_vlist)

        ed = time.time()
        print("\tfilter_time =", ed-st, 's')
        # print(_result_klist)
        # print(_result_vlist)
        # print(result_klist)
        # print(result_vlist)


class Project:
    def __init__(self, ipt, pt, tg):
        self.file = ipt
        self.path = pt
        self.target = tg
        self.opt = None
        self.idx = None
        self.file_name()
        self._rank = 256

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
        build_ed = time.time()
        projectA.search_bptree(self.target)
        ed = time.time()
        print(projectA.border_print)
        print("init_time =", init_ed-st, 's')
        print("load_time =", load_ed-init_ed, 's')
        print("build_time =", build_ed-load_ed, 's')
        print("search_time =", ed - build_ed, 's')
        print("run_time =", ed-st, 's')


if __name__ == '__main__':
    file = "C:/Users/chenyujie/Desktop/Test/new_spatial_1kw.txt"
    path = "C:/Users/chenyujie/Desktop/Test"
    target = "4000:12000,4000:12000"

    def main():
        project = Project(file, path, target)
        project.do()
    main()


