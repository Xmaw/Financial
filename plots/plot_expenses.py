"""
 Plots the expenses...
 TO-DO: ADD SOME INFORMATION
"""
from os.path import isfile

import xlrd
import matplotlib.pyplot as plt
import os


class FinancialGraphic:
    path = ""
    expenses_list = []
    other_list = []

    # Outgoing expenses
    food_expenses = 0
    bills_expenses = 0
    pleasure_expenses = 0
    clothes_expenses = 0
    other_expenses = 0
    total_expenses = 0
    payback_loans_amount = 0
    home_expenses = 0

    # Income
    income_amount = 0

    # Different categories
    food = ['fyra arstider',
            'de fyra arstiderna',
            'ica', 'eurest',
            'vallastadens rest',
            '7 eleven',
            'city gross',
            'restaurang skyline',
            'krubbstugan',
            'pressbyrån',
            '4 krogar steakhouse',
            'kungsgril',
            'hemköp',
            'cafe cioccolata',
            'espresso house',
            'stangebro gatukok',
            'stora hotellets rest',
            'resturang',
            'kharma',
            'piri piri',
            'maestro',
            'ellas kok']

    bills = ['telia', 'bredband2', 'spotify', 'heimstaden', 'tekniska ver', 'åhman', 'alfa kassan', 'hyresgästför',
             'autogiro lf']
    pleasure = ['blizzard', 'netflix', 'hbo', 'frisor', 'agatan bar', 'gymbolaget', 'steamgames', 'systembolaget',
                'inet', 'hultins sportfiske']
    clothes = ['mq', 'dressman', 'gant']
    home = ['clas ohlson']
    income = ['lön', 'lån']
    payback_loans = ['centrala studie', 'centrala stu']

    def __init__(self, path):
        # To open Workbook
        wb = xlrd.open_workbook(path)
        sheet = wb.sheet_by_index(0)

        # Populate the categories given the data in the excel file.
        self.populate_categories(sheet)

        self.draw_graph(
            [self.food_expenses, self.bills_expenses, self.pleasure_expenses, self.clothes_expenses,
             self.other_expenses, self.payback_loans_amount, self.home_expenses])

    def populate_categories(self, sheet):
        print("Populating...")
        for row in range(sheet.nrows):
            try:
                print(sheet.cell_value(row, 5))
                transaction_info = sheet.cell_value(row, 5).lower()
                amount = sheet.cell_value(row, 1)
                if isinstance(amount, str):
                    continue
                amount = float(amount)
                amount = abs(amount)
                print("amount found: {0}".format(amount))

                category_found = False
                for category in self.food:
                    if category in transaction_info:
                        self.food_expenses += amount
                        self.total_expenses += amount
                        category_found = True

                for category in self.bills:
                    if category in transaction_info:
                        self.bills_expenses += amount
                        self.total_expenses += amount
                        category_found = True

                for category in self.pleasure:
                    if category in transaction_info:
                        self.pleasure_expenses += amount
                        self.total_expenses += amount
                        category_found = True

                for category in self.clothes:
                    if category in transaction_info:
                        self.clothes_expenses += amount
                        self.total_expenses += amount
                        category_found = True

                for category in self.income:
                    if category in transaction_info:
                        self.income_amount += amount
                        category_found = True

                for category in self.payback_loans:
                    if category in transaction_info:
                        self.payback_loans_amount += amount
                        category_found = True

                for category in self.home:
                    if category in transaction_info:
                        self.home_expenses += amount
                        category_found = True

                if not category_found:
                    if 'överföring' not in transaction_info:
                        self.other_expenses += amount
                        self.total_expenses += amount
                        self.other_list.append({transaction_info: amount})

            except ValueError as e:
                print(e)
        print("Others: {0}".format(self.other_list))

        # Round the values of the expenses to two decimals
        self.total_expenses = float("{0:.2f}".format(abs(self.total_expenses)))
        self.bills_expenses = float("{0:.2f}".format(abs(self.bills_expenses)))
        self.pleasure_expenses = float("{0:.2f}".format(abs(self.pleasure_expenses)))
        self.food_expenses = float("{0:.2f}".format(abs(self.food_expenses)))
        self.other_expenses = float("{0:.2f}".format(abs(self.other_expenses)))
        self.clothes_expenses = float("{0:.2f}".format(abs(self.clothes_expenses)))
        self.payback_loans_amount = float("{0:.2f}".format(abs(self.payback_loans_amount)))
        self.home_expenses = float("{0:.2f}".format(abs(self.home_expenses)))

        print("Done populating!")

    def draw_graph(self, components):
        # Pie-chart of two separate charts.
        fig1, plot = plt.subplots()

        # Chart 1: Represent the different categories with how much money was spent on them.
        labels = 'Food', 'Bills', 'Pleasure', 'Clothes', 'Others', 'Payback Loans', 'Home'
        explode = (0.1, 0, 0, 0, 0, 0, 0)  # only "explode" the 1st slice

        # White ring for the middle of the doughnut
        middle_circle = plt.Circle((0, 0), 0.7, color='white')

        plot.pie(components, explode=explode, labels=labels, autopct='%1.1f%%',
                 shadow=True, startangle=90, pctdistance=0.85, labeldistance=1.2)

        p = plt.gcf()
        p.gca().add_artist(middle_circle)

        # Explanatory text to complement the text.
        plot.text(2.0, 0, 'Food: {0} SEK'.format(self.food_expenses))
        plot.text(2.0, 0.1, 'Bills: {0} SEK'.format(self.bills_expenses))
        plot.text(2.0, 0.2, 'Pleasure: {0} SEK'.format(self.pleasure_expenses))
        plot.text(2.0, 0.3, 'Payback Loans: {0} SEK'.format(self.payback_loans_amount))
        plot.text(2.0, 0.4, 'Home: {0} SEK'.format(self.home_expenses))
        plot.text(2.0, 0.5, 'Other: {0} SEK'.format(self.other_expenses))
        plot.text(2.0, -0.2, 'Total expenses: {0} SEK'.format(self.total_expenses))

        # plt.show()


if __name__ == '__main__':
    path = 'E:/Users/Elias/PycharmProjects/banking/202006.xlsx'
    path = 'C:/Users/Johan/Banking/202011.'
    print(isfile(path))
    FC = FinancialGraphic(path)
