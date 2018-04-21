#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:gjduan time:2018/4/21
'''
参考：https://www.cnblogs.com/MrLJC/p/3715783.html
'''
import xlrd


def readdata(dt, row, table):
    dt['no'] = table.cell(row, 0).value
    dt['name'] = table.cell(row, 1).value
    dt['age'] = table.cell(row, 2).value
    dt['scope'] = table.cell(row, 3).value


'''/Users/duanguanjun/work/t1/exceltest.py'''
if __name__ == '__main__':
    workbook = xlrd.open_workbook('test.xls')
    worksheet = workbook.sheet_by_name('test')
    title = {}
    row = 0
    readdata(title, row, worksheet)

    row = 1
    tb1 = {}
    readdata(tb1, row, worksheet)
    row = 2
    tb2 = {}
    readdata(tb2, row, worksheet)

    print(title)
    print(tb1)
    print(tb2)
