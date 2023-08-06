# !/usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 2020/9/15 20:42
# @Author  : WardenAllen
# @File    : excel.py
# @Brief   : 

import xlrd
from xlrd import xldate_as_tuple
from datetime import datetime

class Excel:
    def __init__(self):
        self.d = []
        self.func_dict = {
            'INT' : self.read_int,
            'FLOAT': self.read_float,
            'STRING': self.read_string,
            'TIME': self.read_time,
        }

    def read_int(self, idx, key, val):
        self.d[idx][key] = int(val)

    def read_float(self, idx, key, val):
        self.d[idx][key] = float(val)

    def read_string(self, idx, key, val):
        self.d[idx][key] = str(val)

    def read_time(self, idx, key, val):
        date = xldate_as_tuple(val, 0)
        self.d[idx][key] = datetime(*date)

    def read(self, file):
        book = xlrd.open_workbook(file)
        sheet = book.sheets()[0]
        for i in range(0, sheet.ncols):
            self.d.append(dict())

        key_rows = sheet.row_values(0)
        type_rows = sheet.row_values(1)

        for i in range(sheet.nrows)[2:]:
            row_values = sheet.row_values(i)
            for j in range(0, sheet.ncols):
                self.func_dict[type_rows[j]](
                    i, key_rows[j], row_values[j]
                )

        self.d = self.d[2:]
        print(self.d)
        return self.d