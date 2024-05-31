import csv
import numpy as np


def read_csv(filename):
    with open(filename, 'r', newline='') as file:
        reader = csv.reader(file)
        data = [row for row in reader]
    return data


def to_id(strings, id_dict=None):
    if id_dict is None:
        id_dict = {}
    id_counter = len(id_dict)
    int_ids = []
    for string in strings:
        if string not in id_dict:
            id_dict[string] = id_counter
            id_counter += 1
        int_ids.append(id_dict[string])
    return int_ids, id_dict


def extract_data(file_path):
    csv_data = read_csv(file_path)
    ret = {'s': [], 'c': [], 'r': []}
    for i in range(1, len(csv_data)):
        ret['s'].append(csv_data[i][0])
        ret['c'].append(csv_data[i][1])
        ret['r'].append(csv_data[i][2])
    ret_num = {}
    ret_num['s'] = to_id(ret['s'])[0]
    ret_num['c'] = to_id(ret['c'])[0]
    ret_num['r'] = [int(r) for r in ret['r']]
    ret_num = np.stack([ret_num['s'], ret_num['c'], ret_num['r']]).T
    ret_num = ret_num[ret_num[:, 2] > 0.5]
    return ret_num[:, :2]
