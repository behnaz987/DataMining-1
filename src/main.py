import csv
import re
import numpy as np
import matplotlib.pyplot as plt


def is_similar(element1: dict, element2: dict):
    if element1["StockCode"] == element2["StockCode"]:
        return True
    x = re.findall("[a-z|A-Z]$", element1["StockCode"][-1]) and re.findall("[a-z|A-Z]$", element2["StockCode"][-1])
    if element1["StockCode"][0:-1] == element2["StockCode"][0:-1]:
        if x:
            intersection = list(set(element1["Description"]) & set(element2["Description"])).__len__()
            if min(intersection / list(element1["Description"]).__len__(),
                   intersection / list(element2["Description"]).__len__()):
                return True
    return False


def draw_chart(param, items_frequency):
    height = items_frequency
    bars = param
    y_pos = np.arange(len(bars))
    plt.bar(y_pos, height, color=(0.2, 0.4, 0.6, 0.6))


def find_items_frequency(total, similar_items:dict):
    items_frequency=list()
    for key, value in similar_items.items():
        for i in range (len(similar_items)):
            items_frequency[i]=int(similar_items[key]["Quantity"])/total
    return items_frequency

def find_similar_items():
    with open('Online_Shopping_edit.csv', 'r') as inp, open('similar_items.txt', 'w') as out:
        reader = csv.DictReader(inp, delimiter=',')
        similar_items = dict()
        total = 0
        for row in reader:
            b = True
            if len(row) > 0 and row["StockCode"] != "StockCode":
                for key, value in similar_items.items():
                    if is_similar({"StockCode": key, "Description": value["Description"].split(" ")},
                                  {"StockCode": row["StockCode"], "Description": row["Description"].split(" ")}):
                        similar_items[key]["Quantity"] += int(row['Quantity'])
                        b = False
                        break
                if b:
                    similar_items[row["StockCode"]] = {"Description": row["Description"],
                                                       "Quantity": int(row['Quantity'])}
        for key, value in similar_items.items():
            total += int(similar_items[key]["Quantity"])

        items_frequency=find_items_frequency(total,similar_items)
        draw_chart(list(similar_items.keys()),items_frequency)

    return similar_items, total


def find_transactionsNo_list():
    transactions = set()
    with open('Online_Shopping_edit.csv', 'r') as inp, open('transactions.txt', 'w') as out:
        reader = csv.DictReader(inp, delimiter=',')
        for row in reader:
            if len(row) > 0 and row["InvoiceNo"] != "InvoiceNo" and row["InvoiceNo"] not in transactions:
                transactions.add(row["InvoiceNo"])

        transactions_1 = list(transactions)
        transactions_1.sort()
        return transactions_1


def find_transactions_items(transactions: list):
    transactions_items = list()
    with open('Online_Shopping_edit.csv', 'r') as inp, open('transactions_items.txt', 'w') as out:
        reader = csv.DictReader(inp, delimiter=',')
        # print(transactions)
        data = []
        for row in reader:
            data.append(row)
        for trans in transactions:
            transaction_item = []
            for row in data:
                if len(row) > 0 and row["InvoiceNo"] == trans:
                    transaction_item.append(row["StockCode"])
            if len(transaction_item) > 0:
                transactions_items.append(transaction_item)
                out.write('%s\n' % transaction_item)
        return transactions_items


if __name__ == '__main__':
    transaction = list()
    with open('Online_Shopping.csv', 'r') as inp, open('Online_Shopping_edit.csv', 'w') as out:

        reader = csv.reader(inp, delimiter=',')
        writer = csv.writer(out)
        for row in reader:
            if row[2] not in (None, "") and row[2] != "Manual" and (row[3] == "Quantity" or int(row[3]) > 0):
                writer.writerow(row)
    transactions = find_transactionsNo_list()
    transactions_items = find_transactions_items(transactions)
    similar_items = find_similar_items()

