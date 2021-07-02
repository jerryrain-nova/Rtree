import struct
import threading
import os
import psutil
import gzip
import numpy as np
from time import time
from multiprocessing import Process, Pool
from sys import argv


class Block:
    def __init__(self):
        self.bit_len = 0
        self.num = 0
        self.x_basic = self.y_basic = 0
        self.gene_list = []
        self.gene_idx = []


class CellOut:
    def __init__(self, _tmp):
        self.num = self.g_num = 0
        self.gd = {}
        self.workers = 4
        self.circle = 32
        self.block_M = 256
        self._tmp = _tmp
        self.y_index = self.xmax = self.xmin = self.ymax = self.ymin = None
        self.b_i = []


    @staticmethod
    def isgzip(file):
        return '.gz' in file

    def write_tmp_thread(self, _tmp, contents):
        threads = []

        def write_tmp(tf, content):
            tf.write(content)

        for i in range(4):
            t = threading.Thread(target=write_tmp(_tmp[i], contents[i]))
            threads.append(t)
        for t in threads:
            t.setDaemon(True)
            t.start()
        for t in threads:
            t.join()

    def load_tmp(self, tf, bit):
        bit_dict = {8: np.uint8, 32: np.uint32, 64: np.uint64}
        rl = np.zeros(self.num, dtype=bit_dict[bit])
        with open(tf, 'r') as ipt:
            for i in range(self.num):
                rl[i] = int(ipt.readline().strip())
        return rl

    def write_tmp(self, tf, il):
        st = time()
        with open(tf, 'w') as f:
            cache = ''
            for i in range(len(il)):
                cache += str(il[i]) + '\n'
                if (i + 1) % self.circle == 0:
                    f.write(cache)
                    cache = ''
            f.write(cache)
        print(tf+" write_time = ", time()-st, 's')

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

    def cut_block(self, il):
        length = (len(il)-1)//256+1
        b_i = np.zeros(length+1, dtype=np.uint32)
        idx = 0
        for i in range(0, len(il), self.block_M):
            b_i[idx] = i
            idx += 1
        b_i[-1] = len(il)
        return b_i

    def load(self, file):
        st = time()

        gtf, xtf, ytf, vtf = self._tmp
        with open(gtf, 'w') as gt, open(xtf, 'w') as xt, open(ytf, 'w') as yt, open(vtf, 'w') as vt:
            if self.isgzip(file):
                f = gzip.open(file, 'rt')
            else:
                f = open(file, 'r')

            header = f.readline()
            while '#' in header:
                header = f.readline()
            point = f.readline()
            gc = xc = yc = vc = ''
            circle = g_idx = 0
            while point:
                gene, x, y, value = point.strip().split('\t')

                if gene not in self.gd:
                    self.gd[gene] = str(g_idx)
                    g_idx += 1

                gc += self.gd[gene] + '\n'
                xc += x + '\n'
                yc += y + '\n'
                vc += value + '\n'
                self.num += 1
                circle += 1
                point = f.readline()

                if not point:
                    self.g_num = g_idx
                    gt.write(gc)
                    xt.write(xc)
                    yt.write(yc)
                    vt.write(vc)

                if circle == self.circle:
                    gt.write(gc)
                    xt.write(xc)
                    yt.write(yc)
                    vt.write(vc)
                    gc = xc = yc = vc = ''
                    circle = 0
            f.close()
        print("load time = ", time()-st, 's')

    def sort_and_block(self):
        st = time()
        gtf, xtf, ytf, vtf = self._tmp

        pool = Pool(self.workers)
        yl_r = pool.apply_async(func=self.load_tmp, args=(ytf, 32,))
        xl_r = pool.apply_async(func=self.load_tmp, args=(xtf, 32,))
        gl_r = pool.apply_async(func=self.load_tmp, args=(gtf, 32,))
        vl_r = pool.apply_async(func=self.load_tmp, args=(vtf, 8,))
        # pool.close()
        # pool.join()
        # yl_r = self.load_tmp(ytf, 32)
        # xl_r = self.load_tmp(xtf, 32)
        yl_r = yl_r.get()
        xl_r = xl_r.get()

        print("time = ", time() - st, 's')
        s_i = yl_r.argsort().astype(np.uint32)
        xl_s = xl_r[s_i]
        yl_s = yl_r[s_i]
        print("time = ", time() - st, 's')
        yl_c = self.cut_list(yl_s)
        self.y_index = yl_s[yl_c]

        self.ymin = str(yl_r[s_i[0]])
        self.ymax = str(yl_r[s_i[-1]])
        self.xmin = str(xl_s.min())
        self.xmax = str(xl_s.max())

        print("time = ", time()-st, 's')
        for i in range(0, len(yl_c), 2):
            xr = xl_s[yl_c[i]:yl_c[i + 1] + 1]
            r_s_i = xr.argsort()
            self.b_i.append(self.cut_block(xr))
            s_i[yl_c[i]:yl_c[i + 1] + 1] = s_i[yl_c[i]:yl_c[i + 1] + 1][r_s_i]
        del i, xr, r_s_i, xl_s, yl_c

        print("write_st = ", time()-st, 's')

        gl_r = gl_r.get()
        vl_r = vl_r.get()
        print(u'当前进程的内存使用: %.4f MB' % (psutil.Process(os.getpid()).memory_info().rss / 1024 / 1024))
        # gl_r = self.load_tmp(gtf, 32)
        # pool = Pool(self.workers)
        gl = gl_r[s_i]
        pool.apply_async(func=self.write_tmp, args=(gtf, gl,))
        print("t4_st = ", time() - st, 's')
        del gl_r, gl
        # vl_r = self.load_tmp(vtf, 8)
        vl = vl_r[s_i]
        pool.apply_async(func=self.write_tmp, args=(vtf, vl,))
        print("t3_st = ", time() - st, 's')
        del vl_r, vl
        yl = yl_r[s_i]
        pool.apply_async(func=self.write_tmp, args=(ytf, yl,))
        print("t1_st = ", time()-st, 's')
        del yl_r, yl
        xl = xl_r[s_i]
        pool.apply_async(func=self.write_tmp, args=(xtf, xl,))
        print("t2_st = ", time() - st, 's')
        del xl_r, xl

        pool.close()
        pool.join()
        pool.terminate()
        print(u'当前进程的内存使用: %.4f MB' % (psutil.Process(os.getpid()).memory_info().rss / 1024 / 1024))
        print("sort time = ", time() - st, 's')

    def printf(self, _opt):
        st = time()




def main():
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
        return gdf, [gtf, xtf, ytf, vtf], [df, idxf, gidxf]

    file = "C:/Users/chenyujie/Desktop/Test/new_spatial_1kw.txt"
    opt_path = "C:/Users/chenyujie/Desktop/Test"
    # file = argv[1]
    # opt_path = argv[2]
    gdf, _tmp, _opt = rename_out(file, opt_path)
    data = CellOut(_tmp)
    data.load(file)
    data.sort_and_block()


if __name__ == '__main__':
    main()
