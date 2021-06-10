from sys import argv
from time import time


def load(file):
    st = time()

    dt = open(file, 'r')
    dt.readline()

    gl = xl = yl = vl = []
    point = dt.readline()
    while point:
        gene, x, y, value = point.strip().split('\t')
        gl.append(gene)
        xl.append(x)
        yl.append(y)
        vl.append(value)
        point = dt.readline()
    print("run time = ", time()-st, 's')


def main():
    file = argv[1]
    load(file)


if __name__ == '__main__':
    main()