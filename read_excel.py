# Reading an excel file using Python
import xlrd

# Give the location of the file
path = 'C:\\Users\\Johan\\PycharmProjects\\Financial_Graphic\\excel_files\\october.xls'

# To open Workbook
wb = xlrd.open_workbook(path)
sheet = wb.sheet_by_index(0)

# For row 0 and column 0
print(sheet.cell_value(0, 0))
amount = 0.0

# Different categories
food = [
    'de fyra arstiderna',
    'ica',
    'EUREST',
    'vallastaden rest',
    '7 eleven'
    'city gross'
]

bills = ['telia', 'bredband2', 'spotify', 'heimstaden']
pleasure = ['blizzard']
clothes = ['mq', 'dressman', 'gant']

expenses_list = []
food_expenses = 0
bills_expenses = 0
pleasure_expenses = 0
clothes_expenses = 0
other_expenses = 0

# Add all the expenses to a list to make it easier to handle them.
expenses_list.append(food_expenses)
expenses_list.append(bills_expenses)
expenses_list.append(pleasure_expenses)
expenses_list.append(clothes_expenses)
expenses_list.append(other_expenses)

other_list = []

# Populate the categories
for row in range(sheet.nrows):
    try:
        transaction_info = sheet.cell_value(row, 1).lower()
        amount = sheet.cell_value(row, 3)
        amount = amount.replace('.', '')
        amount = amount.replace(',', '.')
        amount = float(amount)

        for category in food:
            if category in transaction_info:
                food_expenses += amount

        for category in bills:
            if category in transaction_info:
                bills_expenses += amount

        for category in pleasure:
            if category in transaction_info:
                pleasure_expenses += amount

        for category in clothes:
            if category in transaction_info:
                clothes_expenses += amount

        else:
            other_expenses += amount
            other_list.append(transaction_info)

    except ValueError as e:
        print(e)

print("Food: {0}\nBills: {1}\nPleasure: {2}\nClothes: {3}\nOther: {4}".format(food_expenses, bills_expenses,
                                                                              pleasure_expenses, clothes_expenses,
                                                                              other_expenses))
