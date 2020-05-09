import csv
import numpy as np
import matplotlib.pyplot as plt


def similarity_of_description(des1, des2):
    intersection = list(set(des1) & set(des2)).__len__()
    if min(intersection / list(des1).__len__(),
           intersection / list(des2).__len__()):
        return True
    return False


def find_items_frequency(total, similar_items: dict):
    items_frequency = {}
    for key, value in similar_items.items():
        items_frequency[str(key)] = (int(value) / total) * 100
    return items_frequency


def draw_chart(items_frequency: dict):
    height = list(items_frequency.values())
    bars = list(items_frequency.keys())
    y_pos = np.arange(len(bars))
    plt.plot(y_pos, height, color=(0.2, 0.4, 0.6, 0.6))
    plt.savefig("question2/frequency.png")


def save_result_to_file(items):
    with open('question2/similar_items.csv', 'w', newline='') as out:
        writer = csv.writer(out)
        for item in items:
            writer.writerow(item)


def save_to_file_for_eclat(items):
    with open('question2/for_eclat.csv', 'w', newline='') as out:
        writer = csv.writer(out)
        for item in items:
            writer.writerow(item)


def find_similar_items():
    with open('Online_Shopping_edit.csv', 'r') as inp:
        reader = csv.DictReader(inp, delimiter=',')
        similar_items = {}
        similar_items2 = {}
        base_of_keys = dict()
        total = 0
        for row in reader:
            if not len(row) > 0:
                continue
            if row["StockCode"][:-1] in base_of_keys.keys():
                if base_of_keys[row["StockCode"][:-1]]["key"] == row["StockCode"] or \
                        similarity_of_description(base_of_keys[row["StockCode"][:-1]]["Description"].split(" "),
                                                  row["Description"].split(" ")):
                    similar_items2[base_of_keys[row["StockCode"][:-1]]["key"]].append(row["InvoiceNo"])
                    similar_items[base_of_keys[row["StockCode"][:-1]]["key"]] += int(row['Quantity'])
                    total += int(row['Quantity'])
                    continue
            if row["StockCode"] in base_of_keys.keys():
                if base_of_keys[row["StockCode"]]["key"] == row["StockCode"] or \
                        similarity_of_description(base_of_keys[row["StockCode"]]["Description"].split(" "),
                                                  row["Description"].split(" ")):
                    similar_items2[base_of_keys[row["StockCode"]]["key"]].append(row["InvoiceNo"])
                    similar_items[base_of_keys[row["StockCode"]]["key"]] += int(row['Quantity'])
                    total += int(row['Quantity'])
                    continue
            if str(row["StockCode"])[-1].isalpha():
                base_of_keys[row["StockCode"][:-1]] = {"key": row["StockCode"], "Description": row["Description"]}
            else:
                base_of_keys[row["StockCode"]] = {"key": row["StockCode"], "Description": row["Description"]}

            similar_items2[row["StockCode"]] = [row["InvoiceNo"]]

            similar_items[row["StockCode"]] = int(row['Quantity'])
            total += int(row['Quantity'])
        items_frequency = find_items_frequency(total, similar_items)
        draw_chart(items_frequency)
        save_result_to_file(list(zip(similar_items.keys(), similar_items.values(), items_frequency.values())))
        save_to_file_for_eclat(list(similar_items2.values()))
        return list(zip(similar_items.keys(), similar_items.values()))
