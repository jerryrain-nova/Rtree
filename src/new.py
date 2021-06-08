import numpy as np
import sys


class Point:
    __slots__ = ('x', 'y', 'gene', 'value')

    def __init__(self, x, y, gene, value):
        self.x = x
        self.y = y
        self.gene = gene
        self.value = value

    def __str__(self):
        return ':'.join(str((self.x, self.y, self.gene, self.value)))


class Block:
    __slots__ = ('_M', 'x', 'y', 'num', 'points')

    def __init__(self, M):
        self._M = M
        self.x = None
        self.y = None
        self.num = 0
        self.points = []

    def isexist(self):
        return self.x and self.y

    def isfull(self, n):
        return self._M < self.num + n


class Data:
    def __init__(self, x, y, gene, value):
        point = Point(x, y, gene, value)
        self.xmin = self.xmax = x
        self.ymin = self.ymax = y
        self.point = []
        self._B = 0
        self._sortDict = {y: {x: [point]}}

    def border(self):
        return str((self.xmin, self.xmax, self.ymin, self.ymax))

    def update_border(self, x, y):
        if len(str(x)) > self._B:
            self._B = len(str(x))
        if len(str(y)) > self._B:
            self._B = len(str(y))
        if x < self.xmin:
            self.xmin = x
        elif x > self.xmax:
            self.xmax = x
        if y < self.ymin:
            self.ymin = y
        elif y > self.ymax:
            self.ymax = y

    def insert(self, x, y, gene, value):
        point = Point(x, y, gene, value)
        self.update_border(x, y)
        if y not in self._sortDict.keys():
            self._sortDict[y] = {}
        if x not in self._sortDict[y].keys():
            self._sortDict[y][x] = []
        self._sortDict[y][x].append(point)

    @staticmethod
    def cut_list(iptLsit):
        st = ed = iptLsit[0]
        iptList_cutted = []
        for i in iptLsit:
            if i - ed > 1:
                iptList_cutted.extend([st, ed])
                st = i
            ed = i
            if i == iptLsit[-1]:
                iptList_cutted.extend([st, ed])
        return iptList_cutted

    def sort_dict(self):
        yLsit_sorted = np.asarray(list(self._sortDict.keys()), dtype=np.uint32)
        yLsit_sorted.sort()
        print(yLsit_sorted)
        y_st = y_ed = yLsit_sorted[0]
        yList_cutted = []
        xList = []
        xList_sorted = []
        point = []
        for y in yLsit_sorted:
            if y - y_ed > 1:
                yList_cutted.extend([y_st, y_ed])
                y_st = y
                xList = np.asarray(xList, dtype=np.uint32)
                xList_sorted.append(xList.argsort())
                self.point.append(point)
                xList = []
                point = []
            xList.extend(list(self._sortDict[y].keys()))
            for x in self._sortDict[y].keys():
                point.extend(self._sortDict[y][x])
            y_ed = y
            if y == yLsit_sorted[-1]:
                yList_cutted.extend([y_st, y_ed])
                xList = np.asarray(xList, dtype=np.uint32)
                xList_sorted.append(xList.argsort())
        yList_cutted = np.asarray(yList_cutted, dtype=np.uint32)
        print(xList_sorted)
        


def load_data(file):
    ipt = open(file, 'r')
    ipt.readline()
    point = ipt.readline()
    gene, x, y, value = point.strip().split('\t')
    data = Data(int(x), int(y), gene, value)
    point = ipt.readline()
    while point:
        gene, x, y, value = point.strip().split('\t')
        data.insert(int(x), int(y), gene, value)
        point = ipt.readline()
    return data


def main():
    file = "C:/Users/chenyujie/Desktop/Test/FP200000289TR_A2_1M.txt"
    out_path = "C:/Users/chenyujie/Desktop/Test"
    data = load_data(file)
    data.sort_dict()


if __name__ == '__main__':
    main()








