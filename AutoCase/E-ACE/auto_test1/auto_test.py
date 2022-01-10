# -*- coding:utf8 -*-
'''code to compare report files automatically 
    by Zheyuan Zheng, Envision, on on Mar 1, 2018
    last modified: Mar 8, 2018'''
import time

from basic_class import *
from utility import *
from check_compare import *
import yaml
import os
import zipfile
import re
import xlwt
from loguru import logger


logfile = "compare_file.log"
logger.add(logfile, rotation="1 days", retention="3 days")


def compare_file(exp_value):
    print_version()
    # read input file
    data = yaml_read_con_per()
    path_pro, path_pre = data[0], data[1]
    print(path_pro, path_pre)
    path_unzip(path_pro)
    path_unzip(path_pre)
    pre_dir_list = get_all_dir_path(path_pre)
    pro_dir_list = get_all_dir_path(path_pro)
    # print(pre_dir_list)
    # print(pro_dir_list)
    rename_filepath(pre_dir_list, pro_dir_list)
    yamlfile = 'input.yaml'
    ref_folder, nonref_folders = load_file(yamlfile)

    # get all the files to be compared
    for ifolder in nonref_folders:
        ifolder.get_files()

    # compare the files and output
    for ifolder in nonref_folders:
        res_folder = compare_folders(ref_folder, ifolder)

    print('Job completes successfully')
    time.sleep(2)
    compare_report(path_pro, exp_value)


def compare_report(path, value):
    # 1.获取compare_result文件夹下所有比对结果文件
    # 2.计算&统计差值异常的文件
    # 3.汇总统计结果
    list1 = os.listdir(path)
    # print(list1)
    for i in list1:
        if re.findall('compare_result', i):
            compare_dir = path + '\\' + i
            print(compare_dir)
    all_compare_list = get_all_filepath(compare_dir)
    error_list = []
    for file in all_compare_list:
        file_name, file_ext = os.path.splitext(file)
        if file_ext == '.xlsx':
            error_file = compare_xls_result(file, exp_value)
            error_list.append(error_file)
        elif file_ext == '.csv':
            error_file = compare_csv_result(file, exp_value)
            error_list.append(error_file)
        elif file_ext == '.txt':
            error_file = compare_txt_result(file, exp_value)
            error_list.append(error_file)
        else:
            pass
    while None in error_list:
        error_list.remove(None)
    print('error_list', error_list)
    workbook = xlwt.Workbook()
    sheet1 = workbook.add_sheet('compare_result')
    for i in range(len(error_list)):
        sheet1.write(i, 0, error_list[i][0])
        sheet1.write(i, 1, error_list[i][1])
    workbook.save(path + '/compare_result.xls')


if __name__ == "__main__":
    exp_value = 0.1
    compare_file(exp_value)

