import csv
from utils import and_two_list


def convert_horizontal_to_vertical(transactions_items, number_of_transactions):
    id = 0
    item_id = {}
    for transaction in transactions_items:
        for item in transaction:
            if item not in item_id:
                item_id[item] = id
                id += 1
    keys = item_id.keys()
    values = item_id.values()
    id_item = dict(zip(values, keys))

    vertical_data = dict()
    for id in item_id.values():
        item_transactions = [0] * number_of_transactions
        vertical_data[id] = item_transactions
    for transaction_id, transaction in enumerate(transactions_items):
        for item in transaction:
            vertical_data[item_id[item]][transaction_id] = 1
    return vertical_data, id_item


def generate_l1(vertical_data, id_item, number_of_transactions, min_sup):
    l1 = list()
    support_list = dict()
    # @ZH : for id, item_transactions_list in enumerate(vertical_data):
    for id, item_transactions_list in vertical_data.items():
        sup = 0
        for i in range(len(item_transactions_list)):
            if item_transactions_list[i] == 1:
                sup += 1
        # @ZH : if (sup / len(number_of_transactions)) >= min_sup:
        if (sup / number_of_transactions) >= min_sup:
            support_list[frozenset([id_item[id]])] = item_transactions_list
            l1.append([id_item[id]])
    return sorted(list(map(frozenset, sorted(l1)))), support_list


def generate_lk(last_lk, k, min_sup, number_of_transactions, sup_list):
    lk = []
    support_list_k = {}
    for i in range(len(last_lk)):
        for j in range(i + 1, len(last_lk)):
            l1 = sorted(list(last_lk[i])[:k - 2])
            l2 = sorted(list(last_lk[j])[:k - 2])
            if l1 == l2:
                # @ZH s1 = set(sup_list[last_lk[i]])
                # @ZH s2 = set(sup_list[last_lk[j]])
                s1 = sup_list[last_lk[i]]
                s2 = sup_list[last_lk[j]]
                s1_and_s2 = and_two_list(s1, s2)
                sup = sum(s1_and_s2)
                if (sup / number_of_transactions) >= min_sup:
                    # @ZH l1 = set(l1)
                    # @ZH l2 = set(l2)
                    l1 = set(sorted(list(last_lk[i])))
                    l2 = set(sorted(list(last_lk[j])))
                    new = l1.union(l2)
                    if new not in lk:
                        # @ZH support_list_k[new] = sup
                        support_list_k[frozenset(new)] = s1_and_s2
                        # @ ZH lk.append(new)
                        lk.append(frozenset(new))

    return sorted(lk), support_list_k


def eclat(data, min_sup):
    result = []
    number_of_transactions = (len(data))
    vertical_data, id_item = convert_horizontal_to_vertical(data, number_of_transactions)
    l1, support_list = generate_l1(vertical_data, id_item, number_of_transactions, min_sup)
    l = [l1]
    k = 1
    while True:
        k += 1
        print("generate: " + str(k))
        # @ZH lk, support_k = generate_lk(l[-1], k, support_list, number_of_transactions, min_sup)
        # (last_lk, k, min_sup_, number_of_transactions, sup_list):
        lk, support_k = generate_lk(l[-1], k, min_sup, number_of_transactions, support_list)
        if len(lk) == 0:
            for elements in l:
                for element in elements:
                    result.append(element)
            break
        else:
            l.append(lk)
            # print(support_k)
            support_list.update(support_k)
    return sorted(result), support_list


def read_data():
    print("read_input_file")
    print("___________________________________________________")
    data = []
    with open('question1/transactions_items.csv', 'r') as inp:
        reader = csv.reader(inp, delimiter=',')
        for row in reader:
            data.append(row)
    return data


def save_results(results, support_list, min_sup):
    print("run_save_result")
    print("___________________________________________________")
    with open('question4/result' + str(min_sup) + '.csv', 'w', newline='') as out:
        writer = csv.writer(out)
        for result in results:
            writer.writerow(result)

    with open('question4/supports' + str(min_sup) + '.csv', 'w', newline='') as out:
        writer = csv.writer(out)
        for support, value in support_list.items():
            writer.writerow(support)
            writer.writerow(value)


def run_eclat(min_sup=0):
    data = read_data()
    print("run eclat")
    print("___________________________________________________")
    results, support_list = eclat(data, min_sup)
    save_results(results, support_list, min_sup)
