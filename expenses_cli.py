import os

def get_transactions(path):
    expenses = []
    with open(path, 'r', encoding='utf-8') as file:
        for row in file:
            row = row.replace(',', '.')
            row_elements = row.split(';')
            amount = row_elements[1]
            info = row_elements[5].lower()
            expenses.append((info, amount))

    return expenses

def group_transactions(transaction_list):
    grouped_transactions = {}
    for transaction in transaction_list:
        info = transaction[0]
        try:
            amount = float(transaction[1])
        except Exception as e:
            continue
        if info in grouped_transactions:
            grouped_transactions[info] += amount
        else:
            grouped_transactions[info] = amount
    return grouped_transactions


if __name__ == '__main__':
    # path = '/Users/johan/PycharmProjects/banking/2024'
    path = '/Users/elias/PycharmProjects/banking/2024'
    files = os.listdir(path)
    banking_files = [x for x in os.listdir(path) if ".xlsx" in x or ".csv" in x]
    file_index = 0
    some_file = banking_files[file_index]
    path_to_some_file = os.path.join(path, some_file)
    transactions = get_transactions(path_to_some_file)
    grouped_transactions = group_transactions(transactions)
    grouped_transactions = sorted(grouped_transactions.items(), key=lambda x: x[1])
    for transaction in grouped_transactions:
        print(transaction)

