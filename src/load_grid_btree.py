import sys
from collections import deque
from bisect import bisect_left, bisect_right
from random import shuffle


class BKeyWord(object):
    __slots__ = ('key', 'data')
    def __init__(self, key, data):
        self.key = key
        self.data = data
    def __str__(self):
        return str((self.key, self.data))
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
        self.data = []
        self.par = None
        self.bro = None
    def isleaf(self):
        return True
    @property
    def M(self):
        return self._M
    def isfull(self):
        return len(self.data) > self.M
    def isempty(self):
        return len(self.data) < (self.M + 1) // 2


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
        self._root = BLeaf(M)
    @property
    def M(self):
        return self._M
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
            else:
                idx = nd.par.klist.index(nd.klist[0])
                nd.par.klist.insert(idx+1, newnode.klist[0])
                nd.par.ilist.insert(idx+1, newnode)
            return nd.par
        def split_leaf(lf):
            mid = (self.M+1)//2
            newleaf = BLeaf(self.M)
            newleaf.data = lf.data[mid:]
            newleaf.par = lf.par

            lf.data = lf.data[:mid]
            lf.bro = newleaf
            if lf.par is None:
                newroot = BInterNode(self.M)
                newroot.klist = [lf.data[0], newleaf.data[0]]
                newroot.ilist = [lf, newleaf]
                newleaf.par = lf.par = newroot
                self._root = newroot
            else:
                idx = lf.par.klist.index(lf.data[0])
                lf.par.klist.insert(idx+1, newleaf.data[0])
                lf.par.ilist.insert(idx+1, newleaf)
            return lf.par
        def insert_node(n):
            # print(key_word)
            if not n.isleaf():
                # print(n.klist, '\n', n.ilist)
                if n.isfull():
                    insert_node(split_node(n))
                p = bisect_left(n.klist, key_word.key)
                if p == 0:
                    p = 1
                    n.klist[0] = key_word.key
                insert_node(n.ilist[p-1])
            else:
                p = bisect_left(n.data, key_word.key)
                n.data.insert(p, key_word.key)
                if n.isfull():
                    split_leaf(n)
                else:
                    return
        insert_node(node)
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
                    print([v for v in w.data], 'this leaf is, ', hei)


def test():
    numlist = list(range(1, 20))
    shuffle(numlist)
    print(numlist)
    testlist = []
    for i in numlist:
        key = i
        value = i
        testlist.append(BKeyWord(key, value))
    mybtree = Btree(4)
    for kw in testlist:
        mybtree.insert(kw)
    mybtree.show()


if __name__ == '__main__':
    test()