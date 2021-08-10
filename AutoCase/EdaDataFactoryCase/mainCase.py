#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@file : mainCase.py
@comment:
@date : 2021/7/27 10:21
@author : fei.li
@version : 1.0
"""

# 调用登录S3生产环境，下载原始文件数据，建立对应层级目录
# 上传原始文件到S3测试环境，建立对应层级目录
# 连接mysql数据查看数据清洗状态
import sys
import logging
import boto3
from boto3.session import Session
from botocore.exceptions import ClientError
from AutoCase.tools.ProgressPercentage import ProgressPercentage
import dbiz_autotest_sdk


def connect_bigdata():
    bucket = 'engineeringbigdata'
    bucket_path = 'Galileo'
    # bigdata
    aws_key = 'AKIAR4OQZLPAWPK5WP6K'
    aws_secret = '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'
    # 测试环境
    # aws_key = 'AKIAR4OQZLPAV37J4ZSE'
    # aws_secret = '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'

    client = boto3.client('s3', aws_access_key_id=aws_key, aws_secret_access_key=aws_secret, region_name='cn-north-1')
    print('connect to client successfully!')
    list_file = client.list_objects(Prefix=bucket_path, Bucket=bucket).get("Contents")
    print(list_file)


def upload_file(file_name, bucket, object_name=None):
    if object_name is None:
        object_name = file_name

    s3_client = boto3.client('s3')
    try:
        response = s3_client.upload_file(file_name, bucket, object_name)
        s3_client.upload_file(file_name, bucket, object_name, Callback=ProgressPercentage(file_name))
    except ClientError as e:
        logging.error(e)
        return False
    return True


def download_file(file_name, bucket, object_nmae):
    s3 = boto3.client('s3')
    s3.download_file(file_name, bucket, object_nmae)

    with open(file_name, 'wb') as f:
        s3.download_fileobj(bucket, object_nmae, f)


if __name__ == '__main__':
    connect_bigdata()
