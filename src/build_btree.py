import sys
from collections import deque
from bisect import bisect_left, bisect_right
from random import shuffle
from struct import pack, unpack
import time, pickle


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
            mid = (self.M+1)//2
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
                nd.par.klist.insert(idx+1, newnode.klist[0])
                nd.par.ilist.insert(idx+1, newnode)
            return nd.par
        def split_leaf(lf):
            mid = (self.M+1)//2
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
                lf.par.ilist.insert(idx+1, newleaf)
            return lf.par
        def insert_node(n):
            if not n.isleaf():
                p = bisect_left(n.klist, key_word.klist)
                if p == 0:
                    p = 1
                    n.klist[0] = key_word.klist
                insert_node(n.ilist[p-1])
                if n.isfull():
                    insert_node(split_node(n))
                    return
            else:
                p = bisect_left(n.klist, key_word.klist)
                n.klist.insert(p, key_word.klist)
                n.vlist.insert(p, key_word.vlist)
                if n.isfull():
                    split_leaf(n)
        insert_node(node)
    def search(self, mi=None, ma=None):
        result = []
        node = self._root
        leaf = self._leaf
        if mi is None and ma is None:
            raise ImportError('you need to setup searching range')
        elif mi is not None and ma is not None and mi > ma:
            raise ImportError('upper bound must be greater or equal than lower bound')
        def search_key(n, key):
            if n.isleaf():
                p = bisect_left(n.klist, key)
                if p == len(n.klist):
                    p = p-1
                return p, n
            else:
                p = bisect_right(n.klist, key)
                return search_key(n.ilist[p-1], key)
        if mi is None:
            while True:
                for k in leaf.klist:
                    if k <= ma:
                        result.append(k)
                    else:
                        return result
                if leaf.bro is None:
                    return result
                else:
                    leaf = leaf.bro
        elif ma is None:
            index, leaf = search_key(node, mi)
            result.extend(leaf.klist[index:])
            while True:
                if leaf.bro is None:
                    return result
                else:
                    leaf = leaf.bro
                    result.extend(leaf.klist)
        else:
            if mi == ma:
                index, leaf = search_key(node, mi)
                try:
                    if leaf.klist[index] == mi:
                        result.append(leaf.klist[index])
                        return result
                    else:
                        return result
                except IndexError:
                    return result
            else:
                i1, l1 = search_key(node, mi)
                i2, l2 = search_key(node, ma)
                if l1 is l2:
                    if i1 == i2:
                        return result
                    else:
                        result.extend(l1.klist[i1:i2 + 1])
                        return result
                else:
                    result.extend(l1.klist[i1:])
                    l = l1
                    while l.bro:
                        if l.bro == l2:
                            result.extend(l2.klist[:i2 + 1])
                            return result
                        else:
                            result.extend(l.bro.klist)
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
    def node_tosave(self, file):
        node_dict = {'leaf': []}
        opt = open(file, 'wb')
        if self._root.isleaf():
            return "Data Num is too small to build bptree"
        q = deque()
        h = 0
        q.append([self._root, h])
        while True:
            try:
                w, hei = q.popleft()
            except IndexError:
                break
            else:
                if not w.isleaf():
                    if hei not in node_dict.keys():
                        node_dict[hei] = []
                    node_dict[hei].append(w.klist)
                    if hei == h:
                        h += 1
                    q.extend([i, h] for i in w.ilist)
                else:
                    node_dict['leaf'].append([w.klist, w.data])
        opt.write(pack('2H', len(list(node_dict.keys())), self.M))
        for key in list(node_dict.keys())[1:]:
            node_num = len(node_dict[key])
            cache = b''
            for node in node_dict[key]:
                child_num = len(node)
                cache += pack('2I', node, child_num)
            opt.write(pack('I', num))
            opt.write(pack(str(num)+'I', *idx[key]))
        num = len(idx['offset'])
        opt.write(pack('I', num))
        opt.write(pack(str(num)+'I', *idx['offset']))
        opt.close()


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
            key_list = unpack(str(num)+'I', idx[pos_st:pos_st + 4 * num])
            pos_st += 4 * num
            for i in range(num-1):
                if h == hei:
                    h += 1
                st = key_list.index(node.klist[i])
                ed = key_list.index(node.klist[i+1])
                newnode = BInterNode(self.M)
                newnode.klist.extend(key_list[st:ed+1])
                node.ilist[i] = newnode
                q.extend([newnode, h])
            num_full = True






def test():
    st = time.time()
    rank = 5
    # numlist = list(range(1, 20))
    # shuffle(numlist)
    # print(numlist)
    numlist = [19, 8, 18, 1, 4, 10, 14, 16, 6, 13, 3, 17, 2, 12, 15, 5, 11, 9, 7]
    testlist = []
    for i in numlist:
        key = i
        value = i
        testlist.append(BKeyWord(key, value))
    mybtree = Btree(rank)
    for kw in testlist:
        mybtree.insert(kw)
    mybtree.show()
    search_result = mybtree.search(4, 12)
    print("search_result =", search_result)
    ed = time.time()
    print("run_time =", ed-st, 's')


if __name__ == '__main__':
    test()