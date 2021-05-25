from collections import deque
from bisect import bisect_left, bisect_right
from struct import pack, unpack
from sys import argv
import time


class BKeyWord(object):
    __slots__ = ('key', 'value')

    def __init__(self, key, value):
        self.key = key
        self.value = value

    def __str__(self):
        return str((self.key, self.value))

    def __cmp__(self, key):
        if self.key > key:
            return 1
        elif self.key == key:
            return 0
        else:
            return -1


class BLeaf(object):
    def __init__(self, M):
        self._M = M
        self.klist = []
        self.vlist = []
        self.par = None
        self.bro = None

    def isleaf(self):
        return True

    @property
    def M(self):
        return self._M

    def isfull(self):
        return len(self.klist) > self.M

    def isempty(self):
        return len(self.klist) < (self.M + 1) // 2


class BInterNode(object):
    def __init__(self, M):
        self._M = M
        self.par = None
        self.klist = []
        self.ilist = []

    def isleaf(self):
        return False

    @property
    def M(self):
        return self._M

    def isfull(self):
        return len(self.ilist) > self.M

    def isempty(self):
        return len(self.ilist) < (self.M + 1) // 2


class Btree(object):
    def __init__(self, M):
        self._M = M
        self._height = 1
        self._root = BLeaf(M)
        self._leaf = self._root

    @property
    def M(self):
        return self._M

    @property
    def H(self):
        return self._height

    def insert(self, key_word):
        node = self._root

        def split_node(nd):
            mid = (self.M + 1) // 2
            newnode = BInterNode(self.M)
            newnode.klist = nd.klist[mid:]
            newnode.ilist = nd.ilist[mid:]
            newnode.par = nd.par

            nd.klist = nd.klist[:mid]
            nd.ilist = nd.ilist[:mid]
            for i in newnode.ilist:
                i.par = newnode
            if nd.par is None:
                newroot = BInterNode(self.M)
                newroot.klist = [nd.klist[0], newnode.klist[0]]
                newroot.ilist = [nd, newnode]
                newnode.par = nd.par = newroot
                self._root = newroot
                self._height += 1
            else:
                if nd.klist[0] not in nd.par.klist:
                    nd.par.klist[0] = nd.klist[0]
                idx = nd.par.klist.index(nd.klist[0])
                nd.par.klist.insert(idx + 1, newnode.klist[0])
                nd.par.ilist.insert(idx + 1, newnode)
            return nd.par

        def split_leaf(lf):
            mid = (self.M + 1) // 2
            newleaf = BLeaf(self.M)
            newleaf.klist = lf.klist[mid:]
            newleaf.vlist = lf.vlist[mid:]
            newleaf.par = lf.par
            lf.klist = lf.klist[:mid]
            lf.vlist = lf.vlist[:mid]
            newleaf.bro = lf.bro
            lf.bro = newleaf
            if lf.par is None:
                newroot = BInterNode(self.M)
                newroot.klist = [lf.klist[0], newleaf.klist[0]]
                newroot.ilist = [lf, newleaf]
                newleaf.par = lf.par = newroot
                self._root = newroot
                self._height += 0
            else:
                idx = lf.par.klist.index(lf.klist[0])
                lf.par.klist.insert(idx + 1, newleaf.klist[0])
                lf.par.ilist.insert(idx + 1, newleaf)
            return lf.par

        def insert_node(n):
            if not n.isleaf():
                p = bisect_left(n.klist, key_word.key)
                if p == 0:
                    p = 1
                    n.klist[0] = key_word.key
                insert_node(n.ilist[p - 1])
                if n.isfull():
                    insert_node(split_node(n))
                    return
            else:
                p = bisect_left(n.klist, key_word.key)
                n.klist.insert(p, key_word.key)
                n.vlist.insert(p, key_word.value)
                if n.isfull():
                    split_leaf(n)

        insert_node(node)

    def search_continuous(self, mi=None, ma=None):
        result_klist = []
        result_vlist = []
        node = self._root
        leaf = self._leaf
        if mi is None and ma is None:
            raise ImportError('you need to setup searching range')
        elif mi is not None and ma is not None and mi > ma:
            raise ImportError('upper bound must be greater or equal than lower bound')

        def search_key(n, key):
            if n.isleaf():
                p = bisect_right(n.klist, key)
                return p, n
            else:
                p = bisect_right(n.klist, key)
                return search_key(n.ilist[p - 1], key)

        if mi is None:
            while True:
                for k in leaf.klist:
                    if k <= ma:
                        result_klist.append(k)
                        result_vlist.append(leaf.vlist[bisect_left(leaf.klist, k)])
                    else:
                        return result_klist, result_vlist
                if leaf.bro is None:
                    return result_klist, result_vlist
                else:
                    leaf = leaf.bro
        elif ma is None:
            index, leaf = search_key(node, mi)
            result_klist.extend(leaf.klist[index:])
            result_vlist.extend(leaf.vlist[index:])
            while True:
                if leaf.bro is None:
                    return result_klist, result_vlist
                else:
                    leaf = leaf.bro
                    result_klist.extend(leaf.klist)
                    result_vlist.extend(leaf.vlist)
        else:
            if mi == ma:
                index, leaf = search_key(node, mi)
                try:
                    if leaf.klist[index - 1] == mi:
                        result_klist.append(leaf.klist[index - 1])
                        result_vlist.append(leaf.vlist[index - 1])
                        return result_klist, result_vlist
                    else:
                        return result_klist, result_vlist
                except IndexError:
                    return result_klist, result_vlist
            else:
                i1, l1 = search_key(node, mi)
                i2, l2 = search_key(node, ma)
                if l1 is l2:
                    if i1 == i2:
                        return result_klist, result_vlist
                    else:
                        result_klist.extend(l1.klist[i1:i2])
                        result_vlist.extend(l1.vlist[i1:i2])
                        return result_klist, result_vlist
                else:
                    result_klist.extend(l1.klist[i1:])
                    result_vlist.extend(l1.vlist[i1:])
                    l = l1
                    while l.bro:
                        if l.bro == l2:
                            result_klist.extend(l2.klist[:i2])
                            result_vlist.extend(l2.vlist[:i2])
                            return result_klist, result_vlist
                        else:
                            result_klist.extend(l.bro.klist)
                            result_vlist.extend(l.bro.vlist)
                            l = l.bro

    def show(self):
        print('this b+tree is:')
        q = deque()
        h = 0
        q.append([self._root, h])
        while True:
            try:
                w, hei = q.popleft()
            except IndexError:
                return
            else:
                if not w.isleaf():
                    print(w.klist, 'this height is, ', hei)
                    if hei == h:
                        h += 1
                    q.extend([i, h] for i in w.ilist)
                else:
                    print([k for k in w.klist], [v for v in w.vlist], 'this leaf is, ', hei)

    def leaf_tosave(self, file):
        opt = open(file, 'wb')
        if self._root.isleaf():
            return "Data Num is too small to build bptree"
        bit_list = deque()
        bit_list.append(0)
        bit = 0
        q = deque()
        h = 0
        q.append([self._root, h])
        while True:
            try:
                w, hei = q.popleft()
            except IndexError:
                opt.close()
                return
            else:
                if not w.isleaf():
                    if hei == h:
                        h += 1
                    q.extend([i, h] for i in w.ilist)
                else:
                    num = len(w.klist)
                    cache = b''
                    for i in range(num):
                        value = list(map(int, w.vlist[i].split(':')))
                        cache += pack('Q2I', w.klist[i], *value)
                        bit += 16
                    bit_list.append(bit)
                    w.klist = [bit_list.popleft()]
                    w.vlist = [num]
                    opt.write(cache)


class BtreeIndex:
    def __init__(self):
        self._M = 256
        self._root = BInterNode(self.M)
        self._height = None

    @property
    def M(self):
        return self._M

    @property
    def H(self):
        return self._height

    def load_index(self, file):
        idx = open(file, 'rb').readline()
        print(unpack('2H', idx[:4]))
        self._height, M = unpack('2H', idx[:4])[:2]
        if M != self.M:
            self._M = M
            self._root = BInterNode(self.M)

        pos_st = 4
        num, num_full = int(), True
        q = deque()
        h = 0
        q.append([self._root, h])
        while True:
            try:
                node, hei = q.popleft()
            except IndexError:
                break
            if num_full:
                num = unpack('I', idx[pos_st:pos_st + 4])[0]
                pos_st += 4
            key_list = unpack(str(num) + 'I', idx[pos_st:pos_st + 4 * num])
            pos_st += 4 * num
            for i in range(num - 1):
                if h == hei:
                    h += 1
                st = key_list.index(node.klist[i])
                ed = key_list.index(node.klist[i + 1])
                newnode = BInterNode(self.M)
                newnode.klist.extend(key_list[st:ed + 1])
                node.ilist[i] = newnode
                q.extend([newnode, h])
            num_full = True


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
        self.bptree = Btree(self.rank)
        for i in range(len(self.x_list)):
            # primekey = 10**len(str(self.y_list[i]))*self.x_list[i]+self.y_list[i]
            primekey = self.primekey(str(self.x_list[i]), str(self.y_list[i]))
            # kv = build_btree.BKeyWord(primekey, self.value_list[i])
            kv = BKeyWord(primekey, str(bisect_left(self.all_gene, self.gene_list[i]))+':'+str(self.value_list[i]))
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
    file = "C:/Users/Nova/Desktop/Test_Data/new_spatial_1kw.txt"
    path = "C:/Users/Nova/Desktop/Test_Data"
    target = "2300:16000,1900:16000"
    # file = argv[1]
    # path = argv[2]
    # target = argv[3]

    def main():
        project = Project(file, path, target)
        project.do()
    main()
