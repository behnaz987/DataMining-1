def convert_h2v(transactions_items, transactions_Num):
    id = 0
    item_id = {}
    for transaction in transactions_items:
        for item in transaction:
            if not item in item_id:
                item_id[item] = id
                id += 1
    keys = item_id.keys()
    values = item_id.values()
    id_item = dict(zip(values, keys))

    vertical_data = dict()
    for id in item_id.values():
        item_transactions = [0] * transactions_Num
        vertical_data[id] = item_transactions
    for transaction_id, transaction in enumerate(transactions_items):
        for item in transaction:
            vertical_data[item_id[item], transaction_id] = 1
    return vertical_data, id_item


def generate_L1(vertical_data, id_item, transactions_Num, min_sup):
    L1 = list()
    sup_list = dict()
    for id, item_transactions_list in enumerate(vertical_data):
        sup = 0
        for i in range(len(item_transactions_list)):
            if item_transactions_list[i] == 1:
                sup += 1
        if (sup / len(transactions_Num)) >= min_sup:
            sup_list[frozenset([id_item[id]])] = item_transactions_list
            L1.append([id_item[id]])
    return sorted(list(map(frozenset, sorted(L1)))), sup_list


def generate_LK(lastLK, k, min_sup_, transactions_Num, sup_list):
    LK = []
    supportK = {}
    for i in range(len(lastLK)):
        for j in range(i + 1, len(lastLK)):
            L1 = sorted(list(lastLK[i])[:k - 2])
            L2 = sorted(list(lastLK[j])[:k - 2])
            if L1 == L2:
                s1 = set(sup_list[lastLK[i]])
                s2 = set(sup_list[lastLK[j]])
                s1_and_s2 = list(s1 & s2)
                sup = 0
                for i in range(len(s1_and_s2)):
                    if s1_and_s2[i] == 1:
                        sup += 1
                if (sup/transactions_Num) >= min_sup_:
                    l1 = set(L1)
                    l2 = set(L2)
                    new = l1.union(l2)
                    if new not in LK:
                        supportK[new] = sup
                        LK.append(new)

    return sorted(LK), supportK


def eclat(data, min_sup, transactions):
        transactions_Num = (len(transactions))
        vertical_data, id_item = convert_h2v(data , transactions_Num)
        L1, sup_list = generate_L1(vertical_data, id_item, transactions, min_sup)
        L = [L1]
        k = 1
        while True:
            print('Running Eclat: the %i-th iteration with %i itemsets in L%i...' % (k, len(L[-1]), k))
            k += 1
            LK, supportK = generate_LK(L[-1], sup_list, k, transactions_Num, min_sup)

            if len(LK) == 0:
                L = [sorted([tuple(sorted(itemset)) for itemset in LK]) for LK in L]
                # support_list = dict((tuple(sorted(k)), np.sum(v)) for k, v in support_list.items())
                print('Running Eclat: the %i-th iteration. Terminating ...' % (k - 1))
                break
            else:
                L.append(LK)
                sup_list.update(supportK)
        return L, sup_list
