from sys import argv
from time import time
import numpy as np
from sys import getsizeof
import gzip
import os


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
    def __init__(self, _tmp):
        self.xmax = self.xmin = self.ymax = self.ymin = self.yl_c = None
        self.num = self.g_num = 0
        self.b_i = []
        self._tmp = _tmp
        self.circle_t = 32
        self.block_M = 256

    def load(self, file):
        st = time()
        gdf, gtf, xtf, ytf, vtf = self._tmp

        with open(file, 'r') as dt, open(gdf, 'w') as gdt, open(gtf, 'w') as gt, open(xtf, 'w') as xt, open(ytf, 'w') as yt, open(vtf,
                                                                                                           'w') as vt:
            header = dt.readline()
            while header:
                if '#' in header.strip():
                    header = dt.readline()
                else:
                    break
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
                    # print(u'当前进程的内存使用: %.4f MB' % (psutil.Process(os.getpid()).memory_info().rss / 1024 / 1024))
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

            self.g_num = g_idx
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

    def load_gzip(self, file):
        st = time()
        gdf, gtf, xtf, ytf, vtf = self._tmp

        with gzip.open(file, 'rt') as dt, open(gdf, 'w') as gdt, open(gtf, 'w') as gt, open(xtf, 'w') as xt, open(ytf, 'w') as yt, open(vtf, 'w') as vt:
            header = dt.readline()
            while header:
                if '#' in header.strip():
                    header = dt.readline()
                else:
                    break
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
                    # print(u'当前进程的内存使用: %.4f MB' % (psutil.Process(os.getpid()).memory_info().rss / 1024 / 1024))
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

            self.g_num = g_idx
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

    def load_tmp(self, tf, bit):
        bit_dict = {8: np.uint8, 32: np.uint32, 64: np.uint64}
        rl = np.zeros(self.num, dtype=bit_dict[bit])
        with open(tf, 'r') as ipt:
            for i in range(self.num):
                rl[i] = int(ipt.readline().strip())
        return rl

    def load_dict(self, dtf):
        gd = {}
        gd_b = {}
        with open(dtf, 'r') as f:
            for i in range(self.g_num):
                gene = f.readline().strip()
                gd[str(i)] = gene
                gd_b[gene] = []
        return gd, gd_b

    def write_tmp(self, tf, il):
        with open(tf, 'w') as f:
            cache = ''
            for i in range(len(il)):
                cache += str(il[i]) + '\n'
                if (i+1) % self.circle_t == 0:
                    print(cache, end='', file=f)
                    cache = ''
            print(cache, end='', file=f)

    def cut_block(self, il):
        length = (len(il)-1)//256+1
        b_i = np.zeros(length+1, dtype=np.uint32)
        idx = 0
        for i in range(0, len(il), self.block_M):
            b_i[idx] = i
            idx += 1
        b_i[-1] = len(il)
        return b_i

    def sort_and_block(self):
        st = time()
        gdf, gtf, xtf, ytf, vtf = self._tmp

        t1 = time()
        yl_r = self.load_tmp(ytf, 32)
        xl_r = self.load_tmp(xtf, 32)

        print("\treload_time = ", time()-t1, 's')

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
            xr = xl_s[yl_c[i]:yl_c[i+1]+1]
            r_s_i = xr.argsort()
            self.b_i.append(self.cut_block(xr))
            s_i[yl_c[i]:yl_c[i+1]+1] = s_i[yl_c[i]:yl_c[i+1]+1][r_s_i]
        del i, xr, r_s_i, xl_s, yl_c

        yl = yl_r[s_i]
        self.write_tmp(ytf, yl)
        del yl_r, yl
        xl = xl_r[s_i]
        self.write_tmp(xtf, xl)
        del xl_r, xl
        vl_r = self.load_tmp(vtf, 8)
        vl = vl_r[s_i]
        self.write_tmp(vtf, vl)
        del vl_r, vl
        gl_r = self.load_tmp(gtf, 32)
        gl = gl_r[s_i]
        self.write_tmp(gtf, gl)
        del gl_r, gl

        print("sort time = ", time()-st, 's')

    def printf(self, _opt):
        st = time()
        gdf, gtf, xtf, ytf, vtf = self._tmp
        df, idxf, gidxf = _opt
        with open(gtf, 'r') as gt, open(xtf, 'r') as xt, open(ytf, 'r') as yt, open(vtf, 'r') as vt, open(df, 'w') as dt, open(idxf, 'w') as it, open(gidxf, 'w') as git:
            gd, gd_b = self.load_dict(gdf)
            print(','.join([self.xmin, self.xmax, self.ymin, self.ymax]), file=it)
            print(':'.join(list(map(str, self.yl_c.tolist()))), file=it)
            bit = 0
            sum = 0
            for y_b in self.b_i:
                cout = ''
                x_l = []
                off_l = [str(bit)]
                for i in range(len(y_b)-1):
                    num = y_b[i+1]-y_b[i]
                    sum += num
                    for j in range(num):
                        g = gd[gt.readline().strip()]
                        y = yt.readline().strip()
                        x = xt.readline().strip()
                        v = vt.readline().strip()
                        point = ':'.join([x, y, g, v]) + ','
                        cout += point
                        gd_b[g].extend([bit, len(point.encode())])
                        bit += len(point.encode())
                        if num == 1:
                            x_l.extend([x, x])
                            break
                        if j == 0 or j == num-1:
                            x_l.append(x)
                    off_l.append(str(bit))
                print(':'.join(x_l), file=it)
                print(','.join(off_l), file=it)
                print(cout, end='', file=dt)

            g_l = sorted(list(gd_b.keys()))
            print(','.join(g_l), file=git)
            for gene in g_l:
                print(','.join(list(map(str, gd_b[gene]))), file=git)

        print("print time = ", time()-st, 's')





def rename_out(ipt_file, opt_path):
    path = ipt_file.split('/')[-1]
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


def remove_tmp(_tmp):
    for file in _tmp:
        os.remove(file)


def isgzip(file):
    if '.gz' in file:
        return True
    else:
        return False


def main():
    st = time()
    file = argv[1]
    opt_path = argv[2]
    _tmp, _opt = rename_out(file, opt_path)
    data = Data(_tmp)
    if isgzip(file):
        data.load_gzip(file)
    else:
        data.load(file)
    data.sort_and_block()
    data.printf(_opt)
    remove_tmp(_tmp)
    print("************\nrun time = ", time()-st, 's\n************\n')


if __name__ == '__main__':
    main()

