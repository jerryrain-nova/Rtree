from sys import argv
from src import build_btree
from struct import pack
import time
import numpy as np
from bisect import bisect_left, bisect_right


class ResultIter:
    def __init__(self, klist, vlist):
        self.klist = klist
        self.vlist = vlist
        self.i = 0
        self.len = len(self.klist)

    def __iter__(self):
        return self

    def __next__(self):
        if self.i < self.len:
            ret = str(self.klist[self.i]) + self.vlist[self.i]
            self.i += 1
            return ret
        else:
            raise StopIteration()


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

    def split_primekey(self, primekey):
        primekey = str(primekey)
        pre, post = primekey[:-self._bit], primekey[-self._bit:]
        return pre, str(int(post))

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
        # print("save_data =", data_ed-build_ed, 's')
        # self.bptree.show()

    def search_bptree(self, ipt_target):
        x_min, x_max = ipt_target.split(',')[0].split(':')
        y_min, y_max = ipt_target.split(',')[1].split(':')
        x_min, x_max, y_min, y_max = int(x_min), int(x_max), int(y_min), int(y_max)
        _result_klist, _result_vlist = [], []
        for x in range(x_min, x_max+1):
            mi = self.primekey(str(x), str(y_min))
            ma = self.primekey(str(x), str(y_max))
            result_klist, result_vlist = self.bptree.search_continuous(mi, ma)
            _result_klist.extend(result_klist)
            _result_vlist.extend(result_vlist)
        return _result_klist, _result_vlist

    def printf_result(self, opt_file, _result_klist, _result_vlist):
        opt = open(opt_file, 'w')
        # _result_klist = list(map(lambda x: ':'.join(self.split_primekey(x)), _result_klist))
        cache = []
        split_time = 0
        for i in range(len(_result_vlist)):
            st = time.time()
            pre, post = self.split_primekey(_result_klist[i])
            split_time += time.time()-st
            one_tip = pre + ':' + post + ':' + _result_vlist[i]
            cache.append(one_tip)
        print('\n'.join(cache), file=opt)
        print("\tsplit_time =", split_time, 's')

        # result_print = ResultIter(_result_klist, _result_vlist)
        # for i in result_print:
        #     print(i, file=opt)
        # print(_result_klist, file=opt)
        # print(_result_vlist, file=opt)


class Project:
    def __init__(self, ipt, pt, tg):
        self.file = ipt
        self.path = pt
        self.target = tg
        self.dt = None
        self.idx = None
        self.opt = None
        self.file_name()
        self._rank = 256

    def __str__(self):
        return "Transform Result Path(Rank=%s):\nData:%s\nIndex:%s" % (self._rank, self.dt, self.idx)

    @property
    def rank(self):
        return self._rank

    def file_name(self):
        prefix = self.file.split('/')[-1].split('.')[0]
        self.dt = self.path + '/' + prefix + '.data'
        self.idx = self.path + '/' + prefix + '.index'
        self.opt = self.path + '/' + prefix + '.search'

    def do(self):
        st = time.time()
        projectA = DataKey(self.file, self.dt, self.idx, self.rank)
        init_ed = time.time()
        projectA.load()
        load_ed = time.time()
        projectA.build_bptree()
        build_ed = time.time()
        _result_klist, _result_vlist = projectA.search_bptree(self.target)
        search_ed = time.time()
        projectA.printf_result(self.opt, _result_klist, _result_vlist)
        ed = time.time()
        print(projectA.border_print)
        print("init_time =", init_ed-st, 's')
        print("load_time =", load_ed-init_ed, 's')
        print("build_time =", build_ed-load_ed, 's')
        print("search_time =", search_ed - build_ed, 's')
        print("print_time =", ed-search_ed, 's')
        print("run_time =", ed-st, 's')


if __name__ == '__main__':
    file = "C:/Users/chenyujie/Desktop/Test/new_spatial_1kw.txt"
    path = "C:/Users/chenyujie/Desktop/Test"
    target = "2300:16000,1900:16000"

    def main():
        project = Project(file, path, target)
        project.do()
    main()


