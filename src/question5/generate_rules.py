import csv

import itertools


def find_subsets(s, n):
    return list(itertools.combinations(s, n))


def read_item_sets_satisfied_min_sup(min_sup):
    data = []
    max_len = 0
    with open('question4/result' + str(min_sup) + '.csv', 'r') as input:
        reader = csv.reader(input, delimiter=',')
        for row in reader:
            if len(row) > max_len:
                max_len = len(row)
            data.append(frozenset(row))
    return data, max_len


def read_data_frequency_list(min_sup):
    data = {}
    with open('question4/supports' + str(min_sup) + '.csv', 'r') as input:
        reader = csv.reader(input, delimiter=',')
        i = 0
        key = None
        for row in reader:
            if i % 2 == 0:
                key = frozenset(row)
                data[key] = None
            else:
                data[key] = [int(i) for i in row]
            i += 1
        return data


def generate_rules(data, data_frequency_list):
    pass


def save_rules(rules):
    pass

def calculate_confidence(s1,s2,data_frequency_list):
    return 0

def generate_rules_and_save_rules(confident, min_sup):
    data, max_len = read_item_sets_satisfied_min_sup(min_sup)
    data = sorted(data, key=lambda x: - len(x))
    data_frequency_list = read_data_frequency_list(min_sup)
    rules = []
    for row in data:
        if len(row) < max_len:
            break
        for i in range(1, max_len):
            subsets = find_subsets(row,i)
            for subset in subsets:
                if calculate_confidence(subset, row - set(subset), data_frequency_list) >= confident:
                    pass

