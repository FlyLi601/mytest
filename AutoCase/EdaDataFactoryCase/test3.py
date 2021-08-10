#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@file : test3.py
@comment:
@date : 2021/7/28 17:14
@author : fei.li
@version : 1.0
"""
import re
import io
import pandas as pd
from test2 import s3, BUCKETS, BUCKETS_PATH


def _deal_file(list_file, detail):
    if not detail:
        lib_list = list(set([i["Key"].split("/")[-1].split("_")[0] for i in list_file if i["Size"]]))
    else:
        lib_list = [i["Key"].split("/")[-1] for i in list_file if i["Size"]]
    lib_list.sort(reverse=True)
    return lib_list


def query_features_list(detail=False):
    list_file = s3.list_objects(Prefix=BUCKETS_PATH, Bucket=BUCKETS).get("Contents")
    return _deal_file(list_file, detail=detail)


def upload_file(file_path, time_flag, data_type):
    exist_file = query_features_list(detail=True)
    exist_file_match_list = [i for i in exist_file if time_flag in i and data_type in i]
    if exist_file_match_list:
        exist_file_match_list.sort()
        version_name = "v" + str(int(exist_file_match_list[-1].split("_")[-1].split(".")[0][1:]) + 1)
    else:
        version_name = "v1"
    name_list = re.split(r'[/\\]', file_path)
    name = name_list[-1]
    name_suffix = name.split(".")[-1]
    try:
        s3.upload_file(file_path, BUCKETS,
                       BUCKETS_PATH + f"/{'_'.join([time_flag, data_type, version_name]) + '.' + name_suffix}")
        return '_'.join([time_flag, data_type, version_name]) + '.' + name_suffix
    except Exception as up_err:
        print(f"上传源文件失败！原因如下：{up_err}")
        return


def _read_file_to_data_frame(path):
    try:
        result = s3.get_object(Bucket=BUCKETS, Key=path)
        data = result["Body"].read()
    except Exception as e:
        print(f"S3读取失败,原因如下：{e}")
        return pd.DataFrame()
    fp_res = io.BytesIO(data)
    # noinspection PyBroadException
    try:
        result = pd.read_excel(fp_res)
        return result
    except Exception:
        try:
            result = pd.read_csv(fp_res)
            return result
        except Exception as err_csv:
            print(f"特征库文件读取失败,请检查文件类型方式{err_csv}")
            return pd.DataFrame()


def _download(time_choice, file_type, version="latest"):
    file_flag = time_choice + "_" + file_type
    exist_file = query_features_list(detail=True)
    if version != "latest":
        file_flag += "_" + version
        exist_file_match_list = [i for i in exist_file if file_flag in i]
        if exist_file_match_list:
            data_frame = _read_file_to_data_frame(BUCKETS_PATH + "/" + exist_file_match_list[0])
        else:
            print("选取的版本不存在")
            return []
    else:
        exist_file_match_list = [i for i in exist_file if file_flag in i]
        exist_file_match_list.sort()
        data_frame = _read_file_to_data_frame(BUCKETS_PATH + "/" + exist_file_match_list[-1])
    if not data_frame.empty:
        return data_frame
    else:
        return []


def read_current_features(time_choice, version="latest"):
    return _download(time_choice, "current", version=version)


def read_history_features(time_choice, version="latest"):
    return _download(time_choice, "history", version=version)