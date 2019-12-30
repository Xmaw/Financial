# Reading an excel file using Python
import xlrd
import matplotlib.pyplot as plt


def write_graph(components):
    # Pie-chart of two separate charts.
    fig1, ax1 = plt.subplots()

    # Chart 1: Represent the different categories with how much money was spent on them.
    labels = 'Food', 'Bills', 'Pleasure', 'Clothes', 'Others'
    explode = (0, 0, 0, 0, 0.1)  # only "explode" the 2nd slice
    ax1.pie(components, explode=explode, labels=labels, autopct='%1.1f%%',
            shadow=True, startangle=90)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.show()


class FinancialGraphic:
    expenses_list = []
    food_expenses = 0
    bills_expenses = 0
    pleasure_expenses = 0
    clothes_expenses = 0
    other_expenses = 0
    path = ""

    # Different categories
    food = ['de fyra arstiderna', 'ica', 'eurest', 'vallastaden rest', '7 eleven', 'city gross']
    bills = ['telia', 'bredband2', 'spotify', 'heimstaden']
    pleasure = ['blizzard']
    clothes = ['mq', 'dressman', 'gant']

    def __init__(self, path_to_file):
        # Give the location of the file
        self.other_list = []
        self.path_to_file = path_to_file
        expenses_list = []
        self.food_expenses = 0
        self.bills_expenses = 0
        self.pleasure_expenses = 0
        self.clothes_expenses = 0
        self.other_expenses = 0

        # Add all the expenses to a list to make it easier to handle them.
        expenses_list.append(self.food_expenses)
        expenses_list.append(self.bills_expenses)
        expenses_list.append(self.pleasure_expenses)
        expenses_list.append(self.clothes_expenses)
        expenses_list.append(self.other_expenses)

        # To open Workbook
        wb = xlrd.open_workbook(path_to_file)
        sheet = wb.sheet_by_index(0)
        self.populate_categories(sheet)

        print("Food: {0}\nBills: {1}\nPleasure: {2}\nClothes: {3}\nOther: {4}".format(self.food_expenses,
                                                                                      self.bills_expenses,
                                                                                      self.pleasure_expenses,
                                                                                      self.clothes_expenses,
                                                                                      self.other_expenses))
        write_graph(
            [abs(self.food_expenses), abs(self.bills_expenses), abs(self.pleasure_expenses), abs(self.clothes_expenses),
             abs(self.other_expenses)])

    def populate_categories(self, sheet):
        for row in range(sheet.nrows):
            try:
                transaction_info = sheet.cell_value(row, 1).lower()
                amount = sheet.cell_value(row, 3)
                amount = amount.replace('.', '')
                amount = amount.replace(',', '.')
                amount = float(amount)

                for category in self.food:
                    if category in transaction_info:
                        self.food_expenses += amount

                for category in self.bills:
                    if category in transaction_info:
                        self.bills_expenses += amount

                for category in self.pleasure:
                    if category in transaction_info:
                        self.pleasure_expenses += amount

                for category in self.clothes:
                    if category in transaction_info:
                        self.clothes_expenses += amount

                else:
                    self.other_expenses += amount
                    self.other_list.append(transaction_info)

            except ValueError as e:
                print(e)


if __name__ == '__main__':
    path = 'C:\\Users\\Johan\\PycharmProjects\\Financial_Graphic\\excel_files\\october.xls'
    FinancialGraphic(path)
