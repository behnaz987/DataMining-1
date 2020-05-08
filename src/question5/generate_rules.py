import csv

import itertools
from src.question4.eclat import run_eclat
from os import path


def find_subsets(s, n):
    return [set(i) for i in itertools.combinations(s, n)]


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


def generate_rules(data, data_frequency_list, confident):
    rules = {}
    for row in data:
        if row in rules.keys():
            continue
        for i in range(1, len(row)):
            subsets = find_subsets(row, i)
            for subset in subsets:
                if len(subset) == 0:
                    continue
                if calculate_confidence(subset, row - subset, data_frequency_list) >= confident:
                    rules[frozenset(subset)] = row - subset
    return rules


def save_rules(rules):
    pass


def calculate_confidence(s1, s2, data_frequency_list):
    return sum(data_frequency_list[frozenset(s2)]) / sum(data_frequency_list[frozenset(s1)])


def prepare_data(min_sup):
    if not path.exists('question4/result' + str(min_sup) + '.csv'):
        run_eclat(min_sup)


def generate_rules_and_save_rules(confident, min_sup):
    prepare_data(min_sup)
    data, max_len = read_item_sets_satisfied_min_sup(min_sup)
    data_frequency_list = read_data_frequency_list(min_sup)
    rules = generate_rules(sorted(data, key=lambda x: - len(x)), data_frequency_list, confident)
    print(rules)
    print(len(rules))
