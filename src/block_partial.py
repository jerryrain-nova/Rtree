from sys import argv
from time import time
import numpy as np
from sys import getsizeof
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
        self.num = 0
        self.circle_t = 32

    def load(self, file, _tmp):
        st = time()
        gdf, gtf, xtf, ytf, vtf = _tmp

        with open(file, 'r') as dt, open(gdf, 'w') as gdt, open(gtf, 'w') as gt, open(xtf, 'w') as xt, open(ytf, 'w') as yt, open(vtf,
                                                                                                           'w') as vt:
            dt.readline()
            gd = {}
            gc = xc = yc = vc = ''
            point = dt.readline()
            i = 0
            g_idx = 0
            while point:
                gene, x, y, value = point.strip().split('\t')
                if gene not in gd:
                    gd[gene] = str(g_idx)
                    g_idx += 1
                gc += gd[gene] + '\n'
                xc += x + '\n'
                yc += y + '\n'
                vc += value + '\n'
                self.num += 1
                i += 1
                point = dt.readline()

                if not point:
                    print(u'当前进程的内存使用: %.4f MB' % (psutil.Process(os.getpid()).memory_info().rss / 1024 / 1024))
                    print(gc, end='', file=gt)
                    print(xc, end='', file=xt)
                    print(yc, end='', file=yt)
                    print(vc, end='', file=vt)
                    break

                if i == self.circle_t:
                    print(gc, end='', file=gt)
                    print(xc, end='', file=xt)
                    print(yc, end='', file=yt)
                    print(vc, end='', file=vt)
                    gc = xc = yc = vc = ''
                    i = 0

            gc = ''
            i = 0
            for key in gd.keys():
                gc += key + '\n'
                i += 1
                if i == self.circle_t:
                    print(gc, end='', file=gdt)
                    gc = ''
            print(gc, end='', file=gdt)
        print("load time = ", time() - st, 's')

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

    def read_tmp(self, tf, bit):
        bit_dict = {8: np.uint8, 32: np.uint32, 64: np.uint64}
        rl = np.zeros(self.num, dtype=bit_dict[bit])
        with open(tf, 'r') as ipt:
            for i in range(self.num):
                rl[i] = int(ipt.readline().strip())
                if i == self.num-1:
                    print(u'当前进程的内存使用: %.4f MB' % (psutil.Process(os.getpid()).memory_info().rss / 1024 / 1024))
        return rl

    def write_tmp(self, tf, il):
        with open(tf, 'w') as f:
            cache = ''
            for i in range(len(il)):
                cache += str(il[i]) + '\n'
                if (i+1) % self.circle_t == 0:
                    print(cache, end='', file=f)
                    cache = ''
            print(cache, end='', file=f)

    def sort(self, _tmp):
        st = time()
        gdf, gtf, xtf, ytf, vtf = _tmp
        print(u'当前进程的内存使用: %.4f MB' % (psutil.Process(os.getpid()).memory_info().rss / 1024 / 1024))

        t1 = time()
        yl_r = self.read_tmp(ytf, 32)
        xl_r = self.read_tmp(xtf, 32)
        vl_r = self.read_tmp(vtf, 8)
        gl_r = self.read_tmp(gtf, 32)

        print("\treload_time = ", time()-t1, 's')
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
        self.write_tmp(ytf, yl)
        del yl_r, yl
        xl = xl_r[s_i]
        self.write_tmp(xtf, xl)
        del xl_r, xl
        vl = vl_r[s_i]
        self.write_tmp(vtf, vl)
        del vl_r, vl
        gl = gl_r[s_i]
        self.write_tmp(gtf, gl)
        del gl_r, gl

        print(u'当前进程的内存使用: %.4f MB' % (psutil.Process(os.getpid()).memory_info().rss / 1024 / 1024))

        print("sort time = ", time()-st, 's')


def rename_out(ipt_file, opt_path):
    path = ipt_file.split('/')[-1]
    prefix = path.split('.')[:-1]
    prefix = '.'.join(prefix)
    gdf = opt_path + '/' + prefix + '.gd_tmp'
    gtf = opt_path + '/' + prefix + '.g_tmp'
    xtf = opt_path + '/' + prefix + '.x_tmp'
    ytf = opt_path + '/' + prefix + '.y_tmp'
    vtf = opt_path + '/' + prefix + '.v_tmp'
    return [gdf, gtf, xtf, ytf, vtf]


def main():
    st = time()
    # file = "C:/Users/chenyujie/Desktop/Test/new_spatial_1kw.txt"
    # opt_path = "C:/Users/chenyujie/Desktop/Test"
    file = "/mnt/c/Users/chenyujie/Desktop/Test/new_spatial_1kw.txt"
    opt_path = "/mnt/c/Users/chenyujie/Desktop/Test"
    _tmp = rename_out(file, opt_path)
    data = Data()
    data.load(file, _tmp)
    data.sort(_tmp)

    print("\n************\nrun time = ", time()-st, 's')


if __name__ == '__main__':
    main()

