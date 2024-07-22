"""
This is a program that is designed to retrieve the transaction history between you and another person.

Input:
    The name of the person that you wish to display the transaction history with.

Output:
    A list of the transaction history. Displayed in [+x,xx, -z,xx] in SEK.
"""

import xlrd
import os
from os import listdir
from os.path import isfile, join


def get_history(name):
    dir_path = "/Users/elias/PycharmProjects/banking"
    files = [f for f in listdir(dir_path) if isfile(join(dir_path, f))]
    print(files)
    return_list = []
    for file in files:
        file_path = dir_path + '/' + file
        word_book = xlrd.open_workbook(file_path)
        sheet = word_book.sheet_by_index(0)
        for i in range(sheet.nrows):
            cell = str(sheet.cell(i, 1)).lower()
            if name in cell:
                return_list.append(sheet.cell(i, 3))
    return return_list


if __name__ == '__main__':
    print(os.getcwd())
    name = input('Name of the person  you wish to get transactional history from: ')
    print(get_history(name))
