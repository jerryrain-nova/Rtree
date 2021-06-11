from sys import argv
from time import time
import numpy as np

import os
import psutil


def load(file, _tmp):
    st = time()
    gtf, xtf, ytf, vtf = _tmp

    with open(file, 'r') as dt, open(gtf, 'w') as gt, open(xtf, 'w') as xt, open(ytf, 'w') as yt, open(vtf, 'w') as vt:
        dt.readline()

        gc = xc = yc = vc = ''
        point = dt.readline()
        i = 0
        while point:
            gene, x, y, value = point.strip().split('\t')

            gc += gene + ','
            xc += x + ','
            yc += y + ','
            vc += value + ','
            i += 1
            point = dt.readline()

            if not point:
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
    print("load time = ", time()-st, 's')


class Data:
    def __init__(self):
        self.xmax = self.xmin = self.ymax = self.ymin = None

    @staticmethod
    def cut_list(il):
        st = ed = 0
        il_c = []
        for i in range(len(il)):
            if il[i] - il[ed] > 1:
                il_c.extend([st, ed])
                st = i
            ed = i
            if i == len(il) - 1:
                il_c.extend([st, ed])
        return il_c

    @staticmethod
    def argsort(l, il):
        for i in range(len(l)):
            il[i] = l[il[i]]
        return il

    def sort(self, _tmp):
        st = time()
        gtf, xtf, ytf, vtf = _tmp
        print(u'当前进程的内存使用: %.4f MB' % (psutil.Process(os.getpid()).memory_info().rss / 1024 / 1024))

        t1 = time()
        yl_r = np.loadtxt(ytf, dtype=np.uint32, delimiter=',')
        xl_r = np.loadtxt(xtf, dtype=np.uint32, delimiter=',')
        vl_r = np.loadtxt(vtf, dtype=np.uint8, delimiter=',')
        with open(gtf, 'r') as gt:
            gl_r = gt.readline().strip().split(',')
        print("load_time = ", time()-t1, 's')
        print(u'当前进程的内存使用: %.4f MB' % (psutil.Process(os.getpid()).memory_info().rss / 1024 / 1024))

        s_i = yl_r.argsort().astype(np.uint32)
        xl_s = xl_r[s_i]
        yl_c = self.cut_list(yl_r[s_i])

        self.ymin = yl_r[s_i[0]]
        self.ymax = yl_r[s_i[-1]]
        self.xmin = xl_s.min()
        self.xmax = xl_s.max()

        for i in range(0, len(yl_c), 2):
            xr = xl_s[yl_c[i]:yl_c[i+1]+1]
            r_s_i = xr.argsort()
            s_i[yl_c[i]:yl_c[i+1]+1] = s_i[yl_c[i]:yl_c[i+1]+1][r_s_i]
        del i, xr, r_s_i, yl_c, xl_s
        print(u'当前进程的内存使用: %.4f MB' % (psutil.Process(os.getpid()).memory_info().rss / 1024 / 1024))

        yl = yl_r[s_i]
        print(yl[11711], end='\t')
        np.savetxt(ytf, yl, fmt='%.d')
        del yl_r, yl
        xl = xl_r[s_i]
        print(xl[11711], end='\t')
        np.savetxt(xtf, xl, fmt='%.d')
        del xl_r, xl
        vl = vl_r[s_i]
        print(vl[11711], end='\t')
        np.savetxt(vtf, vl, fmt='%.d')
        del vl_r, vl
        gl = self.argsort(gl_r, s_i.tolist())
        print(gl[11711])
        with open(gtf, 'w') as gt:
            print('\n'.join(gl), file=gt)
        del gl_r, gl
        print(u'当前进程的内存使用: %.4f MB' % (psutil.Process(os.getpid()).memory_info().rss / 1024 / 1024))

        print("sort time = ", time()-st, 's')


def rename_out(ipt_file, opt_path):
    path = ipt_file.split('/')[-1]
    prefix = path.split('.')[:-1]
    prefix = '.'.join(prefix)
    gtf = opt_path + '/' + prefix + '.g_tmp'
    xtf = opt_path + '/' + prefix + '.x_tmp'
    ytf = opt_path + '/' + prefix + '.y_tmp'
    vtf = opt_path + '/' + prefix + '.v_tmp'
    return [gtf, xtf, ytf, vtf]


def main():
    file = "C:/Users/chenyujie/Desktop/Test/new_spatial_1kw.txt"
    opt_path = "C:/Users/chenyujie/Desktop/Test"
    _tmp = rename_out(file, opt_path)
    load(file, _tmp)
    data = Data()
    data.sort(_tmp)


if __name__ == '__main__':
    main()

