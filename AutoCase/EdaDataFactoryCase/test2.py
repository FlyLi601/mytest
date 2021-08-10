#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@file : test2.py
@comment:
@date : 2021/7/28 15:53
@author : fei.li
@version : 1.0
"""
import os
import boto3
import base64

# 配置S3连接环境：PROD | TEST
S3_ENVIRON = 'TEST'
# 需配置的系统环境变量名
OS_ENVIRON_KEY = 'AWS_ACCESS_KEY'

# AWS_ACCESS_KEY = os.environ.get(OS_ENVIRON_KEY)
AWS_ACCESS_KEY = 'SpBBMR/GCi1l307T4vq9BFH/NTDpe0jEtUBA+4+U'
AWS_KEY_ID = 'AKIAR4OQZLPAWPK5WP6K' if S3_ENVIRON == 'PROD' else 'AKIAR4OQZLPAV37J4ZSE'
BUCKETS = "engineeringbigdata" if S3_ENVIRON == 'PROD' else "tcms"
BUCKETS_PATH = "EDA/DigitalTwinFeatureLibs" if S3_ENVIRON == 'PROD' else "eda_test/DigitalTwinFeatureLibs"

s3 = boto3.client(
    's3',
    region_name='cn-north-1',
    aws_access_key_id=AWS_KEY_ID,
    # aws_secret_access_key=base64.b64decode(AWS_ACCESS_KEY).decode("utf-8")
    aws_secret_access_key='SpBBMR/GCi1l307T4vq9BFH/NTDpe0jEtUBA+4+U'
)

print(s3)
