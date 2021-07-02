import numpy as np
import psutil
import os
import struct
import gzip
from sys import argv
from time import time


class Data:
    def __init__(self, _tmp):
        self.xmax = self.xmin = self.ymax = self.ymin = self.yl_c = None
        self.num = self.g_num = 0
        self.b_i = []
        self._tmp = _tmp
        self.circle_t = self.block_M = 256

    @staticmethod
    def isgzip(file):
        if '.gz' in file:
            return True
        else:
            return False

    def cut_list(self, il):
        st = ed = 0
        il_c = []
        limit = int(self.block_M**0.5)
        for i in range(len(il)):
            if il[i] - il[ed] > 1 or ed - st == limit-1:
                il_c.extend([st, ed])
                st = i
            ed = i
            if i == len(il) - 1:
                il_c.extend([st, ed])
        return il_c

    def cut_block(self, il):
        length = (len(il)-1)//self.block_M+1
        b_i = np.zeros(length+1, dtype=np.uint32)
        idx = 0
        for i in range(0, len(il), self.block_M):
            b_i[idx] = i
            idx += 1
        b_i[-1] = len(il)
        return b_i

    def load_tmp(self, tf, bit):
        bit_dict = {8: np.uint8, 32: np.uint32, 64: np.uint64}
        rl = np.zeros(self.num, dtype=bit_dict[bit])
        with open(tf, 'r') as ipt:
            for i in range(self.num):
                rl[i] = int(ipt.readline().strip())
        return rl

    def load(self, file):
        st = time()
        gdf, gtf, xtf, ytf, vtf = self._tmp

        if self.isgzip(file):
            dt = gzip.open(file, 'rt')
        else:
            dt = open(file, 'r')
        with open(gdf, 'w') as gdt, open(gtf, 'w') as gt, open(xtf, 'w') as xt, open(ytf, 'w') as yt, open(vtf, 'w') as vt:
            header = dt.readline()
            while header:
                if '#' in header.strip():
                    header = dt.readline()
                else:
                    break

            gc = xc = yc = vc = ''
            i = g_i = 0
            gd = {}
            point = dt.readline()
            while True:
                gene, x, y, value = point.strip().split('\t')
                if gene not in gd:
                    gd[gene] = str(g_i)
                    g_i += 1
                gc += gd[gene] + '\n'
                xc += x + '\n'
                yc += y + '\n'
                vc += value + '\n'
                i += 1
                self.num += 1

                if i == self.circle_t:
                    print(gc, end='', file=gt)
                    print(xc, end='', file=xt)
                    print(yc, end='', file=yt)
                    print(vc, end='', file=vt)
                    gc = xc = yc = vc = ''
                    i = 0

                point = dt.readline()
                if not point:
                    print(gc, end='', file=gt)
                    print(xc, end='', file=xt)
                    print(yc, end='', file=yt)
                    print(vc, end='', file=vt)
                    break

            self.g_num = g_i
            print('\n'.join(list(gd.keys())), file=gdt)
        dt.close()
        print("load time = ", time()-st, 's')

    def sort_and_block(self, data_file):
        st = time()
        gdf, gtf, xtf, ytf, vtf = self._tmp

        yl_r = self.load_tmp(ytf, 32)
        xl_r = self.load_tmp(xtf, 32)

        s_i = yl_r.argsort().astype(np.uint32)
        xl_s = xl_r[s_i]
        self.yl_c = yl_r[s_i]
        yl_c = self.cut_list(yl_r[s_i])
        self.yl_c = self.yl_c[yl_c]

        self.ymin = str(yl_r[s_i[0]])
        self.ymax = str(yl_r[s_i[-1]])
        self.xmin = str(xl_s.min())
        self.xmax = str(xl_s.max())

        for i in range(0, len(yl_c), 2):
            xr = xl_s[yl_c[i]:yl_c[i + 1] + 1]
            r_s_i = xr.argsort()
            self.b_i.append(self.cut_block(xr))
            s_i[yl_c[i]:yl_c[i + 1] + 1] = s_i[yl_c[i]:yl_c[i + 1] + 1][r_s_i]
        del i, xr, r_s_i, xl_s, yl_c

        with open(data_file, 'wb') as dt:

            xl = xl_r[s_i]
            dt.write(struct.pack(str(self.num) + 'I', *xl))
            del xl_r, xl
            yl = yl_r[s_i]
            dt.write(struct.pack(str(self.num)+'I', *yl))
            del yl_r, yl
            gl_r = self.load_tmp(gtf, 32)
            gl = gl_r[s_i]
            dt.write(struct.pack(str(self.num)+'H', *gl))
            del gl_r, gl
            vl_r = self.load_tmp(vtf, 8)
            vl = vl_r[s_i]
            dt.write(struct.pack(str(self.num)+'B', *vl))
            del vl_r, vl


def file_name(file, opt_path):
    path = file.split('/')[-1]
    prefix = path.split('.')[:-1]
    prefix = '.'.join(prefix)
    gdf = opt_path + '/' + prefix + '.gd_tmp'
    gtf = opt_path + '/' + prefix + '.g_tmp'
    xtf = opt_path + '/' + prefix + '.x_tmp'
    ytf = opt_path + '/' + prefix + '.y_tmp'
    vtf = opt_path + '/' + prefix + '.v_tmp'
    df = opt_path + '/' + prefix + '.data'
    idxf = opt_path + '/' + prefix + '.index'
    gidxf = opt_path + '/' + prefix + '.g_index'
    return [gdf, gtf, xtf, ytf, vtf], [df, idxf, gidxf]


def main():
    file = "C:/Users/chenyujie/Desktop/Test/new_spatial_1kw.txt"
    opt_path = "C:/Users/chenyujie/Desktop/Test"
    _tmp, _opt = file_name(file, opt_path)
    dt = Data(_tmp)
    dt.load(file)
    dt.sort_and_block(_opt[0])
    

if __name__ == '__main__':
    main()
