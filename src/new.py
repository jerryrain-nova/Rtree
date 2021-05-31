

class Point:
    __slots__ = ('x', 'y', 'gene', 'value')

    def __init__(self, x, y, gene, value):
        self.x = x
        self.y = y
        self.gene = gene
        self.value = value

    def __str__(self):
        return str((self.x, self.y, self.gene, self.value))


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


class Data:
    def __init__(self, x, y, gene, value):
        point = Point(x, y, gene, value)
        self.point = [point]
        self.xmin = self.xmax = x
        self.ymin = self.ymax = y

    def border(self):
        return str((self.xmin, self.xmax, self.ymin, self.ymax))

    def update_border(self, x, y):
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
        self.point.append(point)


    def sort_y(self):
        y_dedup = list({}.fromkeys(self.y).keys())
        y_sorted = []
        orderDict = {}
        for idx in range(len(y_dedup)):
            orderDict[y_dedup[idx]] = idx
        for idx in range(len(self.y)):
            order = orderDict[self.y[idx]]
            if order != idx:










