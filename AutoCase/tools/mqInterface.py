#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@file : mqInterface.py
@comment:
@date : 2021/7/29 16:44
@author : fei.li
@version : 1.0
"""
import requests
import json


# 重定向接口
def renew_batch(datafile_id):
    url = "http://10.93.200.58:9012/eda_factory/renewBatch"
    headers = {'Content-Type': 'application/json'}
    form_data = json.dumps({"toHead": 'true', "dataFileIds": datafile_id, "redshiftFlag": 'true'})
    response = requests.post(url, data=form_data, headers=headers)
    res = response.json()
    print(res)
    return res


# 入仓接口
def copy_data():
    url = "http://10.93.200.58:9013/eda_factory_redshift/copyData"
    params = {'dataType': 'DT', 'count':'1'}
    response = requests.get(url, params=params)
    res = response.json()
    print(res)
    return res


if __name__ == '__main__':
    datafile_id = 294296
    # renew_batch(datafile_id)
    copy_data()
    # headers = {'Content-Type': 'application/json'}
    # url = "http://10.93.200.58:9012/eda_factory/renewBatch"
    # form_data = json.dumps({"toHead": 'true', "dataFileIds": datafile_id, "redshiftFlag": 'true'})
    # print('form_data', form_data)
    # response = requests.post(url, data=form_data, headers=headers)
    # print(response.json())
