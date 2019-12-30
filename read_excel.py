# Reading an excel file using Python
import xlrd
import matplotlib.pyplot as plt


class FinancialGraphic:
    path = ""
    expenses_list = []
    food_expenses = 0
    bills_expenses = 0
    pleasure_expenses = 0
    clothes_expenses = 0
    other_expenses = 0
    total_expenses = 0

    # Different categories
    food = ['fyra', 'de fyra arstiderna', 'ica', 'eurest', 'vallastaden rest', '7 eleven', 'city gross']
    bills = ['telia', 'bredband2', 'spotify', 'heimstaden']
    pleasure = ['blizzard']
    clothes = ['mq', 'dressman', 'gant']

    def __init__(self, path_to_file):
        # Add all the expenses to a list to make it easier to handle them.
        self.expenses_list.append(self.food_expenses)
        self.expenses_list.append(self.bills_expenses)
        self.expenses_list.append(self.pleasure_expenses)
        self.expenses_list.append(self.clothes_expenses)
        self.expenses_list.append(self.other_expenses)

        # To open Workbook
        wb = xlrd.open_workbook(path_to_file)
        sheet = wb.sheet_by_index(0)

        # Populate the categories given the data in the excel file.
        self.populate_categories(sheet)

        self.draw_graph(
            [self.food_expenses, self.bills_expenses, self.pleasure_expenses, self.clothes_expenses,
             self.other_expenses])

    def populate_categories(self, sheet):
        for row in range(sheet.nrows):
            try:
                transaction_info = sheet.cell_value(row, 1).lower()
                amount = sheet.cell_value(row, 3)
                amount = amount.replace('.', '')
                amount = amount.replace(',', '.')
                amount = float(amount)
                amount = abs(amount)
                amount = abs(amount)

                for category in self.food:
                    if category in transaction_info:
                        self.food_expenses += amount
                        self.total_expenses += amount

                for category in self.bills:
                    if category in transaction_info:
                        self.bills_expenses += amount
                        self.total_expenses += amount

                for category in self.pleasure:
                    if category in transaction_info:
                        self.pleasure_expenses += amount
                        self.total_expenses += amount

                for category in self.clothes:
                    if category in transaction_info:
                        self.clothes_expenses += amount
                        self.total_expenses += amount

                # Round the total amount to two decimals.
                self.total_expenses = float("{0:.2f}".format(self.total_expenses))

            except ValueError as e:
                print(e)

    def draw_graph(self, components):
        # Pie-chart of two separate charts.
        fig1, plot = plt.subplots()

        # Chart 1: Represent the different categories with how much money was spent on them.
        labels = 'Food', 'Bills', 'Pleasure', 'Clothes', 'Others'
        explode = (0.1, 0, 0, 0, 0)  # only "explode" the 2nd slice

        # White ring for the middle of the doughnut
        middle_circle = plt.Circle((0, 0), 0.7, color='white')

        plot.pie(components, explode=explode, labels=labels, autopct='%1.1f%%',
                 shadow=True, startangle=90, pctdistance=0.85, labeldistance=1.2)

        p = plt.gcf()
        p.gca().add_artist(middle_circle)

        # List of elements to the side of the chart. (Legends)
        # plot.legend(bbox_to_anchor=(1.1, 1.05), fancybox=True, shadow=True)

        # Explanatory text to complement the text.
        plot.text(1.5, 0, 'Food: {0} SEK'.format(self.food_expenses))
        plot.text(1.5, 0.1, 'Bills: {0} SEK'.format(self.bills_expenses))
        plot.text(1.5, 0.2, 'Pleasure: {0} SEK'.format(self.pleasure_expenses))
        plot.text(1.5, 0.3, 'Other: {0} SEK'.format(self.other_expenses))
        plot.text(1.5, -0.2, 'Total expenses: {0} SEK'.format(self.total_expenses))

        plt.show()


if __name__ == '__main__':
    path = 'C:\\Users\\Johan\\PycharmProjects\\Financial_Graphic\\excel_files\\october.xls'
    FinancialGraphic(path)
