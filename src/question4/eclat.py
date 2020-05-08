import csv


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


def generate_lk(last_lk, k, min_sup_, number_of_transactions, sup_list):
    lk = []
    support_list_k = {}
    try:
        for i in range(len(last_lk)):
            for j in range(i + 1, len(last_lk)):
                l1 = sorted(list(last_lk[i])[:k - 2])
                l2 = sorted(list(last_lk[j])[:k - 2])
                if l1 == l2:
                    s1 = set(sup_list[last_lk[i]])
                    s2 = set(sup_list[last_lk[j]])
                    s1_and_s2 = list(s1 & s2)
                    sup = 0
                    for i in range(len(s1_and_s2)):
                        if s1_and_s2[i] == 1:
                            sup += 1
                    if (sup / number_of_transactions) >= min_sup_:
                        l1 = set(l1)
                        l2 = set(l2)
                        new = l1.union(l2)
                        if new not in lk:
                            # @ZH support_list_k[new] = sup
                            support_list_k[new] = sup
                            lk.append(new)

        return sorted(list(map(frozenset, sorted(lk)))), support_list_k
    except Exception as e:
        print("AAAAAAAAAAAA")

def eclat(data, min_sup):
    number_of_transactions = (len(data))
    vertical_data, id_item = convert_horizontal_to_vertical(data, number_of_transactions)
    l1, support_list = generate_l1(vertical_data, id_item, number_of_transactions, min_sup)
    l = [l1]
    k = 1
    while True:
        print('Running Eclat: the %i-th iteration with %i itemsets in l%i...' % (k, len(l[-1]), k))
        k += 1
        lk, support_k = generate_lk(l[-1], k, support_list, number_of_transactions, min_sup)

        if len(lk) == 0:
            l = [sorted([tuple(sorted(itemset)) for itemset in lk]) for LK in l]
            # support_list = dict((tuple(sorted(k)), np.sum(v)) for k, v in support_list.items())
            print('Running Eclat: the %i-th iteration. Terminating ...' % (k - 1))
            break
        else:
            l.append(lk)
            support_list.update(support_k)
    return l, support_list


def run_eclat():
    with open('question1/test.csv', 'r') as inp:
        reader = csv.reader(inp, delimiter=',')
        data = []
        for row in reader:
            data.append(row)
        print(eclat(data, 0.02))
