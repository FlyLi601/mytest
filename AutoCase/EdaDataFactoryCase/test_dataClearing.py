#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@file : test_dataClearing.py
@comment:
@date : 2021/7/27 10:21
@author : fei.li
@version : 1.0
"""
import boto3
import pytest
from loguru import logger
from botocore.exceptions import ClientError
import dbiz_autotest_sdk
from dbiz_autotest_sdk import s3_operation
from tools import mysqlDBConn, mqInterface
import time


def s3_conn_upload_down():
    aws_region = 'cn-north-1'
    aws_key = 'AKIAR4OQZLPAV37J4ZSE'
    aws_secret = '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'
    bucket_name = 'tcms'
    # 上传的源文件路径&文件上传S3路径
    source_file = 'D:\\proData\\Galileo\\CN-45_54\\20210517\\CN-45_54-B-001\\DigitalTwin\\Minute\\ad830b2282474cd48840053facf29be4.csv.gz'
    upload_key = 'vdm0/Galileo/CN-45_54/20210517/CN-45_54-B-001/DigitalTwin/Minute/ad830b2282474cd48840053facf29be4.csv.gz'
    # 下载的文件路径&下载后存储路径
    target_file = 'D:\\proData\\Galileo\\CN-45_54\\20210517\\CN-45_54-B-002\\DigitalTwin\\Minute\\10a9c62a5ce1402ea5b7fe1f5c52a86e.csv.gz'
    source_file1 = 'vdm0/Galileo/CN-45_54/20210517/CN-45_54-B-002/DigitalTwin/Minute/10a9c62a5ce1402ea5b7fe1f5c52a86e.csv.gz'

    s3 = s3_operation.init_s3(aws_region, aws_key, aws_secret)
    test_upload = s3_operation.upload_file_to_S3(s3, bucket_name, source_file, upload_key)
    # print(test, type(test))
    test_down = s3_operation.download_file_from_S3(s3, bucket_name, source_file1, target_file)
    return test_upload, test_down


def mysqldb_state_check():
    data = mysqlDBConn.digital_conn()
    # print(data)
    datafile_id = data[0]
    status = data[1]

    # 调用重定向接口
    mqInterface.renew_batch(datafile_id)
    logger.info("重定向接口调用成功")
    time.sleep(60)

    print(datafile_id, status)
    if status == 'READY' or 'AGAIN':
        # 调用入仓接口
        mqInterface.copy_data()
        logger.info("入仓接口调用成功")
        time.sleep(120)
    else:
        print("status is %s,please check mysqldb" % status)
    data = mysqlDBConn.digital_conn()
    # print(data)
    status_new = data[1]
    if status_new == 'Success':
        print("Test data claening success")
        return True


if __name__ == '__main__':
    mysqldb_state_check()