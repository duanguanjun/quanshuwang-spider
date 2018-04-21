#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:gjduan time:2018/4/21
import xlwt
'''
参考：https://www.cnblogs.com/MrLJC/p/3715783.html
'''


def writedata(row,sheet,tb):
    sheet.write(row, 0, tb.get('no'))
    sheet.write(row, 1, tb.get('name'))
    sheet.write(row, 2, tb.get('age'))
    sheet.write(row, 3, tb.get('scope'))


'''/Users/duanguanjun/work/t1/exceltest.py'''
if __name__ == '__main__':
    tb1 = dict(no="0001", name='张三', age=18, scope=100)
    tb2 = {'no':"0002", 'name':'王五', 'age':20, 'scope':80}

    # print(tb1.keys(),tb1.values())
    # print(tb2)

    # print(dir(xlwt))
    # print('-'*100)
    # print(dir(xlrd))
    workbook=xlwt.Workbook()
    worksheet=workbook.add_sheet('test')
    row=0
    worksheet.write(row,0,'no')
    worksheet.write(row, 1, 'name')
    worksheet.write(row, 2, 'age')
    worksheet.write(row, 3, 'scope')
    row=1
    writedata(row,worksheet,tb1)
    row = 2
    writedata(row,worksheet,tb2)

    workbook.save('test.xls')







