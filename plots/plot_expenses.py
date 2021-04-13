"""
 Plots the expenses...
 TO-DO: ADD SOME INFORMATION
"""
import os.path

import xlrd
import matplotlib.pyplot as plt


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
            'ellas kok',
            'delivery hero sweden',
            'sukaldari',
            'storan restaurang',
            'brodernas',
            'bobbys pizzahus',
            ]

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
        file_path, file_extension = os.path.splitext(path)
        if '.csv' in file_extension:
            self.populate_categories_csv_format(path)
        elif '.xlsx' in file_extension:
            self.populate_categories_xmlx_format(path)

        self.draw_graph([self.food_expenses, self.bills_expenses, self.pleasure_expenses, self.clothes_expenses,
                         self.other_expenses, self.payback_loans_amount, self.home_expenses])

    def populate_categories(self, amount, info):
        print("Populating...")
        print("amount found: {0}".format(amount))

        category_found = False
        for category in self.food:
            if category in info:
                self.food_expenses += amount
                self.total_expenses += amount
                category_found = True

        for category in self.bills:
            if category in info:
                self.bills_expenses += amount
                self.total_expenses += amount
                category_found = True

        for category in self.pleasure:
            if category in info:
                self.pleasure_expenses += amount
                self.total_expenses += amount
                category_found = True

        for category in self.clothes:
            if category in info:
                self.clothes_expenses += amount
                self.total_expenses += amount
                category_found = True

        for category in self.income:
            if category in info:
                self.income_amount += amount
                category_found = True

        for category in self.payback_loans:
            if category in info:
                self.payback_loans_amount += amount
                category_found = True

        for category in self.home:
            if category in info:
                self.home_expenses += amount
                category_found = True

        if not category_found:
            if 'överföring' not in info:
                self.other_expenses += amount
                self.total_expenses += amount
                self.other_list.append({info: amount})

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

        plt.show()

    def populate_categories_xmlx_format(self, path):
        wb = xlrd.open_workbook(path)
        sheet = wb.sheet_by_index(0)

        # Populate the categories given the data in the excel file.
        for row in range(sheet.nrows):
            try:
                print(sheet.cell_value(row, 5))
                info = sheet.cell_value(row, 5).lower()
                amount = sheet.cell_value(row, 1)
                if isinstance(amount, str):
                    continue
                amount = float(amount)
                amount = abs(amount)
                self.populate_categories(amount, info)
            except ValueError as e:
                pass

    def populate_categories_csv_format(self, path):
        with open(path, 'r', encoding='utf-8') as file:
            for row in file:
                row = row.replace(',', '.')
                row_elements = row.split(';')
                amount = row_elements[1]
                info = row_elements[5].lower()
                try:
                    amount = float(amount)
                except ValueError:
                    print('Unable to convert "{0}" to a float.'.format(amount))
                else:
                    amount = abs(amount)
                    self.populate_categories(amount, info)


if __name__ == '__main__':
    path = 'C:\\Users\\Johan\\PycharmProjects\\banking'
    files = os.listdir(path)
    banking_files = [x for x in os.listdir(path) if ".xlsx" in x or ".csv" in x]

    some_file = banking_files[-1]
    path_to_some_file = os.path.join(path, some_file)
    FinancialGraphic(path_to_some_file)
