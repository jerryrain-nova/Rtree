def fill_zero(lower, upper, data_dict):
    for i in range(lower + 1, upper):
        data_dict['each_stat'][0].append(0)
        data_dict['each_stat'][1].append(i)


def load(file):
    with open(file, 'rt') as Input:
        Input.readline()
        line_count = 0
        line_list = []
        data_dict = {'each_stat': [[], []]}
        stat = False
        for line in Input:
            [gene, x, y, value] = line.strip().split('\t')
            if not stat:
                line_idx = int(y)
                stat = True
            if int(y) != line_idx:
                data_dict[line_idx] = []
                data_dict[line_idx].extend(line_list)
                data_dict['each_stat'][0].append(line_count)
                data_dict['each_stat'][1].append(line_idx)
                fill_zero(line_idx, int(y), data_dict)
                line_idx = int(y)
                line_count = 0
                line_list = []
            point = (gene, x, y, value)
            line_list.append(point)
            line_count += 1
    data_dict[line_idx] = line_list
    fill_zero(line_idx, int(y), data_dict)
    data_dict['each_stat'][0].append(line_count)
    data_dict['each_stat'][1].append(int(y))

    return data_dict
    # for key in data_dict.keys():
    #     print(key, end=',')
    # print('')
    # zero = []
    # for idx in range(len(data_dict['each_stat'])):
    #     if data_dict['each_stat'][idx] == 0:
    #         zero.append(idx)
    # print(zero)
    # print("num = ", len(zero))

if __name__ == '__main__':
    file = "C:/Users/chenyujie/Desktop/Test/spatial_loadtest.txt"
    a = load(file)
