import csv
import time
from src.question1.code import find_transactions_items
from src.question2.code import find_similar_items
from src.question4.eclat import run_eclat
from src.question5.generate_rules import generate_rules_and_save_rules
# import re
# import numpy as np
# import matplotlib.pyplot as plt
# from src.eclat import eclat


#
# def is_similar(element1: dict, element2: dict):
#     if element1["StockCode"] == element2["StockCode"]:
#         return True
#     x = re.findall("[a-z|A-Z]$", element1["StockCode"][-1]) and re.findall("[a-z|A-Z]$", element2["StockCode"][-1])
#     if element1["StockCode"][0:-1] == element2["StockCode"][0:-1]:
#         if x:
#             intersection = list(set(element1["Description"]) & set(element2["Description"])).__len__()
#             if min(intersection / list(element1["Description"]).__len__(),
#                    intersection / list(element2["Description"]).__len__()):
#                 return True
#     return False


# def draw_chart(param, items_frequency):
#     height = items_frequency
#     bars = param
#     y_pos = np.arange(len(bars))
#     plt.plot(y_pos, height, color=(0.2, 0.4, 0.6, 0.6))
#     plt.savefig("frequency.png")


# changed
# def find_items_frequency(total, similar_items: dict):
#     items_frequency = list()
#     for item in similar_items.values():
#         items_frequency.append(int(item) / total)
#     return items_frequency


# def find_similar_items():
#     with open('Online_Shopping_edit.csv', 'r') as inp, open('similar_items.txt', 'w') as out:
#         reader = csv.DictReader(inp, delimiter=',')
#         similar_items = dict()
#         total = 0
#         for row in reader:
#             b = True
#             if len(row) > 0 and row["StockCode"] != "StockCode":
#                 for key, value in similar_items.items():
#                     if is_similar({"StockCode": key, "Description": value["Description"].split(" ")},
#                                   {"StockCode": row["StockCode"], "Description": row["Description"].split(" ")}):
#                         similar_items[key]["Quantity"] += int(row['Quantity'])
#                         b = False
#                         break
#                 if b:
#                     similar_items[row["StockCode"]] = {"Description": row["Description"],
#                                                        "Quantity": int(row['Quantity'])}
#         for key, value in similar_items.items():
#             total += int(similar_items[key]["Quantity"])
#
#         items_frequency = find_items_frequency(total, similar_items)
#         draw_chart(list(similar_items.keys()), items_frequency)
#
#     return similar_items, total

# def find_transactionsNo_list():
#     transactions = set()
#     with open('Online_Shopping_edit.csv', 'r') as inp, open('transactions.txt', 'w') as out:
#         reader = csv.DictReader(inp, delimiter=',')
#         for row in reader:
#             if len(row) > 0 and row["InvoiceNo"] != "InvoiceNo" and row["InvoiceNo"] not in transactions:
#                 transactions.add(row["InvoiceNo"])
#
#         transactions_1 = list(transactions)
#         transactions_1.sort()
#         return transactions_1


# def find_transactions_items():
#     item_grouped_by_transaction = []
#     with open('Online_Shopping_edit.csv', 'r') as inp, open('transactions_items.csv', 'w',  newline='') as out:
#         writer = csv.writer(out)
#         reader = csv.DictReader(inp, delimiter=',')
#         key = None
#         item_of_one_transaction = []
#         for row in reader:
#             if not len(row) > 0:
#                 continue
#             if key != row["InvoiceNo"]:
#                 key = row["InvoiceNo"]
#                 if len(item_of_one_transaction) > 0:
#                     item_grouped_by_transaction.append(item_of_one_transaction)
#                     writer.writerow(item_of_one_transaction)
#                 item_of_one_transaction = [row["StockCode"]]
#             else:
#                 item_of_one_transaction.append(row["StockCode"])
#         return item_grouped_by_transaction

def clean_data():
    with open('Online_Shopping.csv', 'r') as inp, open('Online_Shopping_edit.csv', 'w') as out:
        reader = csv.reader(inp, delimiter=',')
        writer = csv.writer(out)
        for row in reader:
            if row[2] not in (None, "") and row[2] != "Manual" and (row[3] == "Quantity" or int(row[3]) > 0):
                # print(row[0], " ", row[1])
                writer.writerow(row)


if __name__ == '__main__':
    # print("question1")
    # start = time.time()
    # find_transactions_items()
    # print("time for question 1")
    # print(time.time()-start)
    # print("________________________________________________")
    # print("question2")
    # start = time.time()
    # find_similar_items()
    # print("time for question 2")
    # print(time.time() - start)
    # print("________________________________________________")
    print("question4")
    start = time.time()
    run_eclat(0.02)
    print("time for question 4")
    print(time.time() - start)
    print("________________________________________________")
    # print("question5")
    # start = time.time()
    # generate_rules_and_save_rules(0.7, 0.014)
    # print(time.time() - start)
    # print("________________________________________________")




