#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@file : test_channelCheck.py
@comment:
@date : 2021/8/2 11:26
@author : fei.li
@version : 1.0
"""
import sys

import pytest

from tools.channeldesc import *
from tools.mysqlDBConn import red_shift58_conn
import pandas as pd
import numpy
from loguru import logger


# 查询出S3数据库中存储的表中 通道列名，存储成list
def s3_channel_list():
    sql_load = "select column_name FROM information_schema.columns where table_name like '%fact_digitaltwindata_load%' "
    sql_distribution = "select column_name FROM information_schema.columns where table_name " \
                       "like '%fact_digitaltwindata_distribution%'"
    list_load = red_shift58_conn(sql_load)
    list_distribution = red_shift58_conn(sql_distribution)
    # print(len(test))
    # print(list_load)
    # print(list_distribution)
    list_total = list_load + list_distribution
    list_total.sort()
    print(list_total)
    return list_total


# 转化csv源文件中的通道名，存储成list
def csv_channel_tolist():
    source_file = 'D:\\proData\\Galileo\\CN-45_54\\20210517\\CN-45_54-B-001\\DigitalTwin\\Minute\\' \
                  'ad830b2282474cd48840053facf29be4.csv'
    data_csv = pd.read_csv(source_file)
    list1 = data_csv.loc[0:1]
    list2 = numpy.array(list1)
    list3 = list2.flatten()
    list4 = list3.tolist()
    csv_channel_list = list4[4:]
    # print(type(csv_channel_list), csv_channel_list)
    return csv_channel_list


# 校对list_s3 和 list_excel
# 转化本地标准文件中的通道名，存储成list
def test_check_channel():
    column_name = get_column_name(channel_column)
    column_name_len = len(column_name)

    original_name = get_original_name(channel_original)
    original_name_len = len(original_name)

    s3_total_channel_list = s3_channel_list()
    s3_channel_count = 0

    csv_channel_list = csv_channel_tolist()
    csv_channel_count = 0

    s3_not_exist = []
    for i in s3_total_channel_list:
        if i in column_name:
            s3_channel_count += 1
        else:
            s3_not_exist.append(i)

    csv_not_exist = []
    for i in csv_channel_list:
        if i in original_name:
            csv_channel_count += 1
        else:
            csv_not_exist.append(i)

    if s3_channel_count == column_name_len:
        logger.info('s3数仓通道与线下文档匹配，通道数量为：' + str(s3_channel_count))
    else:
        logger.info('s3数仓通道与线下文档不匹配，s3通道数量为：' + str(s3_channel_count), '线下文档通道数量为：' + str(column_name_len))
        logger.info('异常通道为：' + str(s3_not_exist))

    if csv_channel_count == original_name_len:
        logger.info('csv源文件与线下文档匹配，通道数量为：' + str(csv_channel_count))
    else:
        logger.info('csv源文件与线下文档不匹配，s3通道数量为：' + str(csv_channel_count), '线下文档通道数量为：' + str(original_name_len))
        logger.info('异常通道为：' + str(csv_not_exist))


if __name__ == '__main__':
    pytest.main(test_check_channel())
