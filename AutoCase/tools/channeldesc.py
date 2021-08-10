#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@file : channeldesc.py
@comment:
@date : 2021/8/2 16:41
@author : fei.li
@version : 1.0
"""
import pandas as pd
import numpy
import csv


filename = r'D:/PythonProject/AutoCase/tools/channeldesc_202105121125.csv'
data = pd.read_csv(filename)
channel_column = data['column_name'].sort_values()
channel_original = data['original_name'].sort_values()
#
# channel_column_1 = numpy.array(channel_column)
# channel_column_2 = channel_column_1.flatten()
# channel_column_3 = channel_column_2.tolist()
#
# print(type(channel_column_3))
# print(channel_column_3)
# print(channel_original)


# 获取线下文档里的标准通道数据column_name为S3存储通道名
def get_column_name(channel_column0):
    channel_column_1 = numpy.array(channel_column0)
    channel_column_2 = channel_column_1.flatten()
    channel_column_3 = channel_column_2.tolist()
    # channel_column_3.sort()
    print(type(channel_column_3), len(channel_column_3))
    print(channel_column_3)
    return channel_column_3


# 获取线下文档里的标准通道数据original_name为源文件存储通道名
def get_original_name(channel_original0):
    channel_original_1 = numpy.array(channel_original0)
    channel_original_2 = channel_original_1.flatten()
    channel_original_3 = channel_original_2.tolist()
    # channel_original_3 = channel_original_1.tolist()
    # channel_original_3.sort()
    print(type(channel_original_3), len(channel_original_3))
    print(channel_original_3)
    return channel_original_3


if __name__ == '__main__':
    get_column_name(channel_column)
    get_original_name(channel_original)
    # print(channel_column)
