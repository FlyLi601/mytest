#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@file : mysqlDBConn.py
@comment:
@date : 2021/7/29 15:16
@author : fei.li
@version : 1.0
"""
import pymysql
import psycopg2
import pandas
import numpy


def digital_conn():
    conn = pymysql.connect(host='172.16.34.102', port=3307, user='root', passwd='u$fJPBsleiU4M', db='digital_twin0',
                           charset='utf8')
    cursor = conn.cursor()
    sql = "SELECT id,copy_status FROM tbl_datafile where raw_file_path like '%CN-45_54-B-001%' " \
          "order by id desc limit 1;"
    # sql1 = "SELECT id,copy_status FROM tbl_datafile where id=293886;"
    cursor.execute(sql)
    data = cursor.fetchall()[0]
    # print(data)
    cursor.close()
    conn.close()
    return data


def digital_conn_sql(new_sql):
    conn = pymysql.connect(host='172.16.34.102', port=3307, user='root', passwd='u$fJPBsleiU4M', db='digital_twin0',
                           charset='utf8')
    cursor = conn.cursor()
    sql = new_sql
    # sql1 = "SELECT id,copy_status FROM tbl_datafile where id=293886;"
    cursor.execute(sql)
    data = cursor.fetchall()[0]
    # print(data)
    cursor.close()
    conn.close()
    return data


def red_shift58_conn(sql):
    conn = psycopg2.connect(dbname='edabigdatadb', host='vdmtest.cob7npogfgfg.cn-north-1.redshift.amazonaws.com.cn',
                            port='5439', user='vdmadmin', password='oPsGrgbw0n#2020')
    cursor = conn.cursor()
    cursor.execute(sql)
    data = cursor.fetchall()
    x = pandas.DataFrame(data)
    x1 = numpy.array(x)
    x2 = x1.flatten()
    x3 = x2.tolist()
    cursor.close()
    conn.close()
    return x3


if __name__ == '__main__':
    sql_load = "select column_name FROM information_schema.columns where table_name like '%fact_digitaltwindata_load%' "
    sql_distribution = "select column_name FROM information_schema.columns where table_name like " \
                       "'%fact_digitaltwindata_distribution%'"
    list_load = red_shift58_conn(sql_load)
    list_distribution = red_shift58_conn(sql_distribution)
    # print(len(test))
    print(list_load)
    print(list_distribution)
    list_total = list_load + list_distribution
    list_total.sort()
    print(list_total)
