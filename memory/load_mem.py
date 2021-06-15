from sys import argv
from time import time
from sys import getsizeof
import os
import psutil
import numpy as np


def load(file, opt_path):
    st = time()

    gd = {}

    dt = open(file, 'r')
    dt.readline()

    def rename_out(ipt_file, opt_path):
        path = ipt_file.split('/')[-1]
        prefix = path.split('.')[:-1]
        prefix = '.'.join(prefix)
        gtf = opt_path + '/' + prefix + '.g_tmp'
        xtf = opt_path + '/' + prefix + '.x_tmp'
        ytf = opt_path + '/' + prefix + '.y_tmp'
        vtf = opt_path + '/' + prefix + '.v_tmp'
        return [gtf, xtf, ytf, vtf]
    _tmp = rename_out(file, opt_path)
    gtf, xtf, ytf, vtf = _tmp
    gt = open(gtf, 'w')
    xt = open(xtf, 'w')
    yt = open(ytf, 'w')
    vt = open(vtf, 'w')

    gc = xc = yc = vc = ''
    i = 0
    point = dt.readline()
    idx = 0
    while point:
        gene, x, y, value = point.strip().split('\t')

        if gene not in gd:
            gd[gene] = str(idx)
            idx += 1

        gc += gd[gene] + '\n'
        xc += x + '\n'
        yc += y + '\n'
        vc += value + '\n'
        i += 1

        point = dt.readline()

        if not point:
            print("gene_dict memory = ", getsizeof(gd) / 1024 / 1024)
            print(u'当前进程的内存使用: %.4f MB' % (psutil.Process(os.getpid()).memory_info().rss / 1024 / 1024))
            print(gc[:-1], end='', file=gt)
            print(xc[:-1], end='', file=xt)
            print(yc[:-1], end='', file=yt)
            print(vc[:-1], end='', file=vt)
            break

        if i == 32:
            print(gc, end='', file=gt)
            print(xc, end='', file=xt)
            print(yc, end='', file=yt)
            print(vc, end='', file=vt)
            gc = xc = yc = vc = ''
            i = 0

    print("run time = ", time()-st, 's')
    return _tmp


def main():
    # file = argv[1]
    # opt_path = argv[2]
    # file = "C:/Users/chenyujie/Desktop/Test/new_spatial_1kw.txt"
    # opt_path = "C:/Users/chenyujie/Desktop/Test"
    file = "/mnt/c/Users/chenyujie/Desktop/Test/new_spatial_1kw.txt"
    opt_path = "/mnt/c/Users/chenyujie/Desktop/Test"
    _tmp = load(file, opt_path)


if __name__ == '__main__':
    main()