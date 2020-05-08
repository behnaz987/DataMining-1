import csv


def find_transactions_items():
    item_grouped_by_transaction = []
    with open('Online_Shopping_edit.csv', 'r') as inp, open('question1/transactions_items.csv', 'w', newline='') as out:
        writer = csv.writer(out)
        reader = csv.DictReader(inp, delimiter=',')
        key = None
        item_of_one_transaction = []
        for row in reader:
            if not len(row) > 0:
                continue
            if key != row["InvoiceNo"]:
                key = row["InvoiceNo"]
                if len(item_of_one_transaction) > 0:
                    item_grouped_by_transaction.append(item_of_one_transaction)
                    writer.writerow(item_of_one_transaction)
                item_of_one_transaction = [row["StockCode"]]
            else:
                item_of_one_transaction.append(row["StockCode"])
        return item_grouped_by_transaction
