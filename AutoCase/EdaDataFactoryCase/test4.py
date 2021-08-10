#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@file : test4.py
@comment:
@date : 2021/8/5 10:28
@author : fei.li
@version : 1.0
"""
from dbiz_autotest_sdk import s3_operation
from tools.mysqlDBConn import *
from datetime import *
from test2 import s3, BUCKETS, BUCKETS_PATH

aws_region = 'cn-north-1'
aws_key = 'AKIAR4OQZLPAV37J4ZSE'
aws_secret = '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'
bucket_name = 'tcms'


sql = "SELECT id , ready_file_path FROM tbl_datafile where raw_file_path like '%CN-81_08-B-050/DigitalTwin%' " \
              "and ready_file_path not in ('error') order by id desc limit 1"
data = digital_conn_sql(sql)
ready_file_path = data[1]
# print(ready_file_path)
now = datetime.now()
date_month = now.strftime("%Y%m")
ready_file_path1 = "DigitalTwin/HNQJ/HNQJ.T2_L5.WTG050/" + date_month
# print(ready_file_path1)

list_file = s3.list_objects(Prefix=ready_file_path1, Bucket=BUCKETS).get("Contents")
# print(list_file)
list_parquet = []
for i in list_file:
    list_parquet.append(i['Key'])

if ready_file_path in list_parquet:
    print("ok")



