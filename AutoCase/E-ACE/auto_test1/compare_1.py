#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@file : compare_1.py
@comment:
@date : 2021/12/2 15:20
@author : fei.li
@version : 1.0
"""
import sys
import time
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from auto_test import compare_file
from check_compare import *


class EACETestCase:
    """
    比较 E-ACE 生产环境和测试环境，相同条件下导出的交付报告
    """

    # 分别从正式环境和测试环境导出交付报告，并记录文件位置
    # 单独写一个UI脚本完成导出报告的工作

    def compare_xls(self, percent):
        # 修改input.yaml中的文件路径,23为测试环境，15为生产环境
        path_23 = 'D:/PythonProject/AutoCase/E-ACE/xls2'
        path_15 = 'D:/PythonProject/AutoCase/E-ACE/xls1'
        with open('input.yaml') as f:
            doc = yaml.safe_load(f)
        doc['ReferenceFolder']['Path'] = path_23
        doc['FolderList'][0]['Path'] = path_15
        with open('input.yaml', 'w') as f:
            yaml.safe_dump(doc, f, default_flow_style=False)
        print(doc['ReferenceFolder']['Path'])
        print(doc['FolderList'][0]['Path'])

        # 调用封装好的比对方法，并生成比对结果
        compare_file()

        # 校对结果文件,计算异常数据数量
        compare_file_path = 'D:/PythonProject/AutoCase/E-ACE/xls1/'
        compare_percent = percent
        compare_file_name = ''
        com_list = os.listdir(compare_file_path)
        for i in com_list:
            if i[0:14] == 'compare_result':
                compare_file_name = str(i)

        compare_xls_result(compare_file_path, compare_file_name, compare_percent)

    def compare_txt(self, percent):
        # 修改input.yaml中的文件路径,23为测试环境，15为生产环境
        path_23 = 'D:/PythonProject/AutoCase/E-ACE/txt2'
        path_15 = 'D:/PythonProject/AutoCase/E-ACE/txt1'
        with open('input.yaml') as f:
            doc = yaml.safe_load(f)
        doc['ReferenceFolder']['Path'] = path_23
        doc['FolderList'][0]['Path'] = path_15
        with open('input.yaml', 'w') as f:
            yaml.safe_dump(doc, f, default_flow_style=False)
        print(doc['ReferenceFolder']['Path'])
        print(doc['FolderList'][0]['Path'])

        # 调用封装好的比对方法，并生成比对结果
        compare_file()

        # 校对结果文件
        compare_file_path = 'D:/PythonProject/AutoCase/E-ACE/txt1/'
        compare_percent = percent
        compare_file_name = ''
        com_list = os.listdir(compare_file_path)
        for i in com_list:
            if i[0:14] == 'compare_result':
                compare_file_name = str(i)

        compare_txt_result(compare_file_path, compare_file_name, compare_percent)

    def compare_csv(self, percent):
        # 修改input.yaml中的文件路径,23为测试环境，15为生产环境
        path_23 = 'D:/PythonProject/AutoCase/E-ACE/csv2'
        path_15 = 'D:/PythonProject/AutoCase/E-ACE/csv1'
        with open('input.yaml') as f:
            doc = yaml.safe_load(f)
        doc['ReferenceFolder']['Path'] = path_23
        doc['FolderList'][0]['Path'] = path_15
        with open('input.yaml', 'w') as f:
            yaml.safe_dump(doc, f, default_flow_style=False)
        print(doc['ReferenceFolder']['Path'])
        print(doc['FolderList'][0]['Path'])

        # 调用封装好的比对方法，并生成比对结果
        compare_file()

        # 校对结果文件
        compare_file_path = 'D:/PythonProject/AutoCase/E-ACE/csv1/compare_result/'
        compare_percent = percent
        compare_csv_result(compare_file_path, compare_percent)


if __name__ == "__main__":
    percent1 = 0.1
    e_compare = EACETestCase()
    e_compare.compare_xls(percent1)
    time.sleep(3)
    e_compare.compare_txt(percent1)
    time.sleep(3)
    e_compare.compare_csv(percent1)
