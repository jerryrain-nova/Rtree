from sys import argv
from time import time


def load(file, opt_path):
    st = time()

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
        return gtf, xtf, ytf, vtf
    gtf, xtf, ytf, vtf = rename_out(file, opt_path)
    gt = open(gtf, 'w')
    xt = open(xtf, 'w')
    yt = open(ytf, 'w')
    vt = open(vtf, 'w')

    gc = xc = yc = vc = ''
    i = 0
    point = dt.readline()
    while point:
        gene, x, y, value = point.strip().split('\t')
        gc += gene + ','
        xc += x + ','
        yc += y + ','
        vc += value + ','
        i += 1

        if i == 32:
            print(gc, end='', file=gt)
            print(xc, end='', file=xt)
            print(yc, end='', file=yt)
            print(vc, end='', file=vt)
            gc = xc = yc = vc = ''
            i = 0

        point = dt.readline()
    print("run time = ", time()-st, 's')


def main():
    # file = argv[1]
    # opt_path = argv[2]
    file = "C:/Users/chenyujie/Desktop/Test/new_spatial_1kw.txt"
    opt_path = "C:/Users/chenyujie/Desktop/Test"
    load(file, opt_path)


if __name__ == '__main__':
    main()