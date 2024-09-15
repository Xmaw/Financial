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



if __name__ == '__main__':
    # path = '/Users/johan/PycharmProjects/banking/2024'
    path = '/Users/elias/PycharmProjects/banking/2024'
    files = os.listdir(path)
    banking_files = [x for x in os.listdir(path) if ".xlsx" in x or ".csv" in x]

    file_index = 0
    some_file = banking_files[file_index]
    path_to_some_file = os.path.join(path, some_file)
    print(get_transactions(path_to_some_file))

