"""
 Plots the expenses...
 TO-DO: ADD SOME INFORMATION
"""
import os.path
import sys

import xlrd
import matplotlib.pyplot as plt
import PyQt5
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QPushButton, QHBoxLayout, QVBoxLayout, QLabel
import re


class CategoryInfo:
    category_name = ""
    category_amount = 0
    category_company_names = []


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
    total_income = 0

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
            'tempo vimmerby storg',
            'restaurang monte car',
            'sibylla',
            'foodora ab',
            'bakfickan',
            'go banana vimmerby'
            ]

    bills = ['telia', 'bredband2', 'spotify', 'heimstaden', 'tekniska ver', 'åhman', 'alfa kassan', 'hyresgästför',
             'autogiro lf', 'betalning pg 4962303-6 vimmerby ene', 'vimarhem akt', 'hallon', 'länsförsäk']
    pleasure = ['blizzard', 'netflix', 'hbo', 'frisor', 'agatan bar', 'gymbolaget', 'steamgames', 'systembolaget',
                'inet', 'hultins sportfiske', 'raidbots', 'svedea ab', 'handelsboden linkopi']
    clothes = ['mq', 'dressman', 'gant']
    home = ['clas ohlson', 'oob vimmerby', 'st1 vimmerby', 'albins jarn', 'circle k']
    income = ['lön', 'lån']
    payback_loans = ['centrala studie', 'centrala stu', 'open banking bg 5196-5770 resurs ba', 'resurs bank']
    car = ['st1 vimmerby']
    expenses = {}

    def __init__(self, path):
        # To open Workbook
        file_path, file_extension = os.path.splitext(path)
        if '.csv' in file_extension:
            self.populate_categories_csv_format(path)
        elif '.xlsx' in file_extension:
            self.populate_categories_xmlx_format(path)

        # self.draw_graph([self.food_expenses, self.bills_expenses, self.pleasure_expenses, self.clothes_expenses,
        #                 self.other_expenses, self.payback_loans_amount, self.home_expenses])

    def reset_amounts(self):
        self.expenses = {}
    def get_all_categories(self):
        return {'food': self.food, 'bills': self.bills, 'pleasure': self.pleasure, 'clothes': self.clothes,
                'home': self.home, 'payback_loans': self.payback_loans, 'car': self.car}

    def get_expenses(self):
        return {'food': self.food_expenses, 'bills': self.bills_expenses, 'pleasure': self.pleasure_expenses,
                'clothes': self.clothes_expenses, 'other': self.other_expenses,
                'payback_loans': self.payback_loans_amount, 'home': self.home_expenses}

    def get_income(self):
        return {'income': self.income_amount}

    def group_expenses(self, amount, info):
        if info in self.expenses:
            self.expenses[info] = self.expenses[info] + amount
        else:
            self.expenses[info] = amount

    def populate_categories(self, amount, info):
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
                self.total_income += amount
                category_found = True

        for category in self.payback_loans:
            if category in info:
                self.payback_loans_amount += amount
                self.total_expenses += amount
                category_found = True

        for category in self.home:
            if category in info:
                self.home_expenses += amount
                self.total_expenses += amount
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

    def check_and_update_category(self, category_name, category_amount, amount, category_found, info):
        for element in category_name:
            if element in info:
                category_amount += amount
                self.total_expenses += amount
                category_found = True
        return category_found

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
                value = sheet.cell_value(row, 5).lower()
                amount = sheet.cell_value(row, 1)
                if isinstance(amount, str):
                    continue
                amount = float(amount)
                amount = abs(amount)
                self.populate_categories(amount, value)
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

                    # Quick/ugly fix to omit transactions. Assumed to be transfers between my own accounts.
                    if 'överföring' in info:
                        continue
                    info = self.clean_up_info_text(info)
                    amount = abs(amount)
                    # self.populate_categories(amount, info)
                    self.group_expenses(amount, info)

    def get_all_expenses(self):
        return self.expenses

    def clean_up_info_text(self, info):
        cleaned_info = info.replace('Autogiro', '')
        pattern = r'[0-9]'
        cleaned_info = re.sub(pattern, '', cleaned_info)
        cleaned_info = cleaned_info.replace('kortköp', '')
        cleaned_info = cleaned_info.replace('Avbet', '')
        cleaned_info = cleaned_info.strip()
        return cleaned_info


class MainWindow(QMainWindow):
    def __init__(self, financial):
        super().__init__()
        self.financial = financial
        self.setWindowTitle("Expenses App")
        self.main_box = QVBoxLayout()
        self.expenses_layout = QVBoxLayout()
        self.income_layout = QVBoxLayout()
        self.remaining_money_layout = QVBoxLayout()
        self.top_button_layout = QHBoxLayout()

        self.configure_top_button_layout(self.top_button_layout)

        self.update_layouts()

        self.main_box.addLayout(self.top_button_layout)
        self.main_box.addLayout(self.expenses_layout)
        self.main_box.addLayout(self.income_layout)
        self.main_box.addLayout(self.remaining_money_layout)

        widget = QWidget()
        widget.setLayout(self.main_box)
        self.setCentralWidget(widget)

        self.setMinimumSize(500, 500)

    def configure_remaning_money_layout(self, remaining_money_layout):
        self.clear_layout(remaining_money_layout)
        remaining_money_layout.addWidget(QLabel("List remaining money here"))
        remaining_money = self.financial.total_income - self.financial.total_expenses
        remaining_money_layout.addWidget(QLabel(f'remaning money: {remaining_money}'))

    def configure_income_layout(self, income_layout):
        self.clear_layout(income_layout)
        income_layout.addWidget(QLabel("Add income here"))
        income_amount = self.financial.get_income()
        for i in income_amount:
            income_layout.addWidget(QLabel(f'{i}: {income_amount}'))

    def configure_expenses_layout(self, expenses_layout):
        self.clear_layout(expenses_layout)
        expenses_amount = self.financial.get_all_expenses()
        expenses_layout.addWidget(QLabel("List fixed expenses here:"))
        expenses_total = 0
        for e in expenses_amount:
            amount = expenses_amount.get(e)
            expenses_layout.addWidget(QLabel(f'{e}: {amount}'))
            expenses_total += amount
        expenses_layout.addWidget(QLabel(f'Total: {round(expenses_total, 2)}'))
        expenses_layout.addWidget(QLabel("List variable expenses here:"))

    def configure_top_button_layout(self, top_button_layout):
        button_previous = QPushButton('<- Previous')
        button_next = QPushButton('Next ->')

        button_next.clicked.connect(self.button_next)
        button_previous.clicked.connect(self.button_previous)
        top_button_layout.addWidget(button_previous)
        top_button_layout.addWidget(button_next)

    def button_next(self):
        print(f'next!')
        path_to_some_file = os.path.join(path, banking_files[file_index + 1])
        self.financial.reset_amounts()
        self.financial = FinancialGraphic(path_to_some_file)
        self.update_layouts()

    def button_previous(self):
        print('previous')

    def clear_layout(self, layout):
        if bool(layout.layout().count()):
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                widget.deleteLater()

    def update_layouts(self):
        self.configure_expenses_layout(self.expenses_layout)
        self.configure_income_layout(self.income_layout)
        self.configure_remaning_money_layout(self.remaining_money_layout)



if __name__ == '__main__':
    # path = '/Users/johan/PycharmProjects/banking/2024'
    path = '/Users/elias/PycharmProjects/banking/2024'
    files = os.listdir(path)
    banking_files = [x for x in os.listdir(path) if ".xlsx" in x or ".csv" in x]

    file_index = 0
    some_file = banking_files[file_index]
    path_to_some_file = os.path.join(path, some_file)
    f = FinancialGraphic(path_to_some_file)

    app = QApplication(sys.argv)

    window = MainWindow(f)
    window.show()
    app.exec()
