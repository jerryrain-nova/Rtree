def calculate_percent(ipt_file):
    ipt = open(ipt_file, 'r')
    Sum = 0
    NameList = []
    NumList = []
    oneLine = ipt.readline()
    while oneLine:
        oneLineList = oneLine.strip().split('\t')
        NameList.append(oneLineList[0])
        NumList.append(int(oneLineList[1]))
        Sum += int(oneLineList[1])
        oneLine = ipt.readline()
    ipt.close()
    return NameList, NumList, Sum


def printf_data(File, NameList, NumList, Sum):
    opt = open(File, 'w')
    for i in range(len(NameList)):
        percent = NumList[i]/Sum*100
        print(NameList[i], '\t', NumList[i], '\t', "%.2f" % percent, '%', file=opt)


def main(ipt_file):
    NameList, NumList, Sum = calculate_percent(ipt_file)
    printf_data(ipt_file, NameList, NumList, Sum)


if __name__ == '__main__':
    file = "C:/Users/chenyujie/Desktop/Test/FP200000284BR_A2.Gene_Expression_table_grid.xls"
    main(file)
