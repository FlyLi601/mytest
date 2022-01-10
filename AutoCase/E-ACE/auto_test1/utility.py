# -*- coding:utf8 -*-
'''contains the functions used in the script
    last modified March 14, 2018'''
import logging
import os
import zipfile


def print_version():
    print('***************************************************************************')
    print('*             This is a tool used to compare two set of files             *')
    print('*   support format: .xlsx, .csv, .txt, developed by Digital Product Team  *')
    print('*           version 1.2   contact: zheyuan.zheng@envisioncn.com           *')
    print('***************************************************************************')


def extract_zip(path):
    '''unzip all files in path'''
    import zipfile
    import os
    for ifile in os.listdir(path):
        file_name, file_ext = os.path.splitext(ifile)
        if file_ext == '.zip':
            file_zip = zipfile.ZipFile(path + '\\' + ifile)
            file_zip.extractall(path)


def search_folders(folder, file):
    '''return the corresponding File object in Folder object'''
    path_list_1 = file.fname.split('\\')
    xfile = None
    for ifile in folder.files:
        path_list_2 = ifile.fname.split('\\')
        is_same_path = True
        for ipath in range(2, len(path_list_1)):
            if path_list_1[ipath] != path_list_2[ipath]:
                is_same_path = False
                break
        if is_same_path:
            xfile = ifile
            break
    return xfile


def is_value(s):
    '''determine wether s is a value (int or float)'''
    s = str(s)
    # if a decimal
    if is_decimal(s):
        return True
    # if scientific notation
    elif s.lower().count('e') == 1:
        new_s = s.lower().split('e')
        left_num = new_s[0]
        right_num = new_s[1]
        if is_decimal(left_num):
            sign = right_num[0]
            if sign == '+' or sign == '-':
                tmp_num = right_num[1:]
                if tmp_num.isdigit():
                    return True
            elif right_num.isdigit():
                return True
    elif s.startswith('-'):
        tmp_num = s.split('-')[-1]
        if tmp_num.isdigit():
            return True
    elif s.endswith('%'):
        tmp_num = s.split('%')[0]
        if is_decimal(tmp_num):
            return True
    # if integer
    if s.isdigit():
        return True
    return False


def is_decimal(s):
    s = str(s)
    if s.count('.') == 1:
        new_s = s.split('.')
        left_num = new_s[0]
        right_num = new_s[1]
        if right_num.isdigit():
            if left_num.isdigit():
                return True
            elif left_num.count('-') == 1 and left_num.startswith('-'):
                tmp_num = left_num.split('-')[-1]
                if tmp_num.isdigit():
                    return True
    return False


def cal_difference(value_a, value_b):
    '''return the relative difference of value_b reference to value_a'''
    if isinstance(value_a, str) and value_a.endswith('%'):
        value_a = value_a.split('%')[0]
    if isinstance(value_b, str) and value_b.endswith('%'):
        value_b = value_b.split('%')[0]
    value_a = float(value_a)
    value_b = float(value_b)
    if abs(value_a) <= 1.0E-5:
        diff = (value_b - value_a)
    else:
        diff = ((value_b - value_a) / value_a) * 100.0
    return '%.4f%s' % (diff, '%')


def text_to_list(text):
    text_tmp = text.rstrip('\n')
    if text_tmp.find('\t') != -1:
        text_tmp = text_tmp.split('\t')
    elif text_tmp.find(',') != -1:
        text_tmp = text_tmp.split(',')
    return text_tmp


def create_folder(path):
    import os
    if not os.path.exists(path):
        os.makedirs(path)


def get_all_filepath(file_path):
    list_name = []
    for (dir_path, dir_names, filenames) in os.walk(file_path):
        for filename in filenames:
            list_name += [os.path.join(dir_path, filename)]
    return list_name


def get_all_dir_path(file_path):
    list_name = []
    for (dir_path, dir_names, filenames) in os.walk(file_path):
        for dir_name in dir_names:
            list_name += [os.path.join(dir_path, dir_name)]
    return list_name


def get_xct_filepath(path_names):
    file_list = []
    for file in path_names:
        file_name, file_ext = os.path.splitext(file)
        if file_ext in ('.xlsx', '.csv', '.txt'):
            file_list.append(file)
    return file_list


def unzip_file(zip_src, dst_dir):
    r = zipfile.is_zipfile(zip_src)
    if r:
        fz = zipfile.ZipFile(zip_src, 'r')
        for file in fz.namelist():
            fz.extract(file, dst_dir)
        print(zip_src + '  unzip success')


def path_unzip(f_path):
    path_names = get_all_filepath(f_path)
    # print(path_names)
    for file_zip in path_names:
        dst_dir = file_zip.rsplit('\\', 1)[0]
        # print(dst_dir)
        file_name, file_ext = os.path.splitext(file_zip)
        if file_ext in '.zip':
            fz = zipfile.ZipFile(file_zip, 'r')
            for file in fz.namelist():
                fz.extract(file, dst_dir)
    return None


def rename_filepath(pre_dir_list, pro_dir_list):
    list_len = len(pre_dir_list)
    # 替换pro的目录路径
    try:
        for i in range(list_len):
            dir_path1, dir_name1 = pre_dir_list[i].rsplit('\\', 1)[0], pre_dir_list[i].rsplit('\\', 1)[1]
            dir_path2, dir_name2 = pro_dir_list[i].rsplit('\\', 1)[0], pro_dir_list[i].rsplit('\\', 1)[1]
            if dir_name2 != dir_name1:
                os.rename(os.path.join(dir_path2, dir_name2), os.path.join(dir_path2, dir_name1))
                print(dir_path2 + dir_name2 + "已重命名")
                logging.info(dir_path2 + dir_name2 + "已重命名")
    except FileNotFoundError as e:
        logging.info('FileNotFoundError')
    return None


if __name__ == '__main__':
    path = r'D:\Users\20211220\test\1220pro\01_Basic_at12201'
    path_unzip(path)

