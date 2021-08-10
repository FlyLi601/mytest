#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@file : test_case_galileo_V110.py
@comment:
@date : 2021/8/4 10:21
@author : fei.li
@version : 1.0
"""
import pytest
from tools.mysqlDBConn import *
from loguru import logger
from dbiz_autotest_sdk import s3_operation
from tools.s3_client import s3, BUCKETS, BUCKETS_PATH
from datetime import *


class TestEdaAutoCase:
    """
    EDA数据工厂伽利略云-云功能测试用例,验证站端DT,SOE,HighSpeed三种类型文件上传S3清洗场景
    """
    def test_check_dt(self):
        """
        检查DT数据文件是否成功上传s3，上传成功则触发清洗流程，copy_status != null
        """
        new_sql = "SELECT id,copy_status FROM tbl_datafile where raw_file_path like '%CN-81_08-B-050/DigitalTwin%' " \
                  "order by id desc limit 1"
        data = digital_conn_sql(new_sql)
        status = data[1]
        if status is not None:
            logger.info("DT文件成功上传S3测试桶,触发数据清洗")
        elif status is None:
            logger.info("DT文件成功上传S3测试桶,未触发数据清洗,请检查")

    def test_check_dt_s3_filepath(self):
        """
        检查DT文件清洗后存储的parquet文件路径，是否正常存储清洗后的文件
        """
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
            logger.info("DT文件清洗后的产生的parquet文件存储路径正常")

    def test_dt_etl_error(self):
        """
        验证ETL失败的DT文件，ready_file_path字段，字段值为ERROR
        """
        file_id = 293114
        new_sql = "select id,ready_file_path from tbl_datafile where id='293114'"
        data = digital_conn_sql(new_sql)
        ready_file_path = data[1]
        assert ready_file_path == 'error'
        logger.info("DT文件ETL失败，ready_file_path等于error，符合预期")

    def test_dt_etl_success(self):
        """
        验证ETL成功的DT文件，status字段，字段值为success
        """
        new_sql = "select id,copy_status from tbl_datafile td where copy_status ='success' " \
                  "and raw_file_path like '%CN-81_08-B-050/DigitalTwin%' order by id desc limit 1"
        data = digital_conn_sql(new_sql)
        status = data[1]
        assert status == 'SUCCESS'
        logger.info("DT文件ETL成功，status字段等于success")

    def test_check_soe(self):
        """
        检查SOE数据文件是否成功上传s3，上传成功则触发清洗流程，copy_status != null
        """
        new_sql = "SELECT id,copy_status FROM tbl_datafile where raw_file_path like '%CN-81_08-B-050/SOE%' " \
                  "order by id desc limit 1"
        data = digital_conn_sql(new_sql)
        status = data[1]
        if status is not None:
            logger.info("SOE文件成功上传S3测试桶,触发数据清洗")
        elif status is None:
            logger.info("SOE文件成功上传S3测试桶,未触发数据清洗,请检查")

    def test_check_soe_s3_filepath(self):
        """
        检查SOE文件清洗后存储的parquet文件路径，是否正常存储清洗后的文件
        """
        sql = "SELECT id , ready_file_path FROM tbl_datafile where raw_file_path like '%CN-81_08-B-050/SOE%' " \
              "and ready_file_path not in ('error') order by id desc limit 1"
        data = digital_conn_sql(sql)
        ready_file_path = data[1]
        # print(ready_file_path)
        now = datetime.now()
        date_month = now.strftime("%Y%m")
        ready_file_path1 = "SOE/HNQJ/HNQJ.T2_L5.WTG050/" + date_month
        # print(ready_file_path1)

        list_file = s3.list_objects(Prefix=ready_file_path1, Bucket=BUCKETS).get("Contents")
        # print(list_file)
        list_parquet = []
        for i in list_file:
            list_parquet.append(i['Key'])

        if ready_file_path in list_parquet:
            logger.info("SOE文件清洗后的产生的parquet文件存储路径正常")

    def test_soe_etl_error(self):
        """
        验证ETL失败的SOE文件，ready_file_path字段，字段值为ERROR
        """
        file_id = 294160
        new_sql = "select id,ready_file_path from tbl_datafile where id='294160'"
        data = digital_conn_sql(new_sql)
        ready_file_path = data[1]
        assert ready_file_path == 'error'
        logger.info("SOE文件ETL失败，ready_file_path等于error，符合预期")

    def test_soe_etl_success(self):
        """
        验证ETL成功的SOE文件，status字段，字段值为success
        """
        new_sql = "select id,copy_status from tbl_datafile td where copy_status ='success' " \
                  "and raw_file_path like '%CN-81_08-B-050/SOE%' order by id desc limit 1"
        data = digital_conn_sql(new_sql)
        status = data[1]
        assert status == 'SUCCESS'
        logger.info("SOE文件ETL成功，status字段等于success")

    def test_check_high_speed(self):
        """
        检查HighSpeed数据文件是否成功上传s3，上传成功则触发清洗流程，copy_status != null
        """
        new_sql = "SELECT id,copy_status FROM tbl_datafile where raw_file_path like '%CN-81_08-B-050/HighSpeed%' " \
                  "order by id desc limit 1"
        data = digital_conn_sql(new_sql)
        status = data[1]
        if status is not None:
            logger.info("HighSpeed文件成功上传S3测试桶,触发数据清洗")
        elif status is None:
            logger.info("HighSpeed文件成功上传S3测试桶,未触发数据清洗,请检查")

    def test_check_high_speed_s3_filepath(self):
        """
        检查HighSpeed文件清洗后存储的parquet文件路径，是否正常存储清洗后的文件
        """
        sql = "SELECT id , ready_file_path FROM tbl_datafile where raw_file_path like '%CN-81_08-B-050/HighSpeed%' " \
              "and ready_file_path not in ('error') order by id desc limit 1"
        data = digital_conn_sql(sql)
        ready_file_path = 'tcms/' + data[1]

        list_file = s3.list_objects(Prefix=ready_file_path, Bucket=BUCKETS).get("Contents")
        file_path = list_file[0]['Key']

        a = file_path[:-8:-1]
        b = a[::-1]
        print(b)
        assert b == 'parquet'
        logger.info("HighSpeed文件清洗后的产生的parquet文件存储路径正常")

    def test_high_speed_etl_error(self):
        """
        验证ETL失败的HighSpeed文件，ready_file_path字段，字段值为ERROR
        """
        file_id = 294179
        new_sql = "select id,ready_file_path from tbl_datafile where id='294179'"
        data = digital_conn_sql(new_sql)
        ready_file_path = data[1]
        assert ready_file_path == 'error'
        logger.info("HighSpeed文件ETL失败，ready_file_path等于error，符合预期")

    def test_high_speed_etl_success(self):
        """
        验证ETL成功的HighSpeed文件，status字段，字段值为success
        """
        new_sql = "select id,copy_status from tbl_datafile td where copy_status ='success' " \
                  "and raw_file_path like '%CN-81_08-B-050/HighSpeed%' order by id desc limit 1"
        data = digital_conn_sql(new_sql)
        status = data[1]
        assert status == 'SUCCESS'
        logger.info("HighSpeed文件ETL成功，status字段等于success")

    '''
    def test_3(self):
        pass
    
    def test_check_hs_ipc(self):
        """
        
        """
        new_sql = "select ready_file_path from tbl_datafile td where raw_file_path like '%CN-81_08-B-050/HighSpeed%'" \
                  " order by id desc limit 1"
        data = digital_conn_sql(new_sql)
        ready_file_path = data[0]
    '''


if __name__ == "__main__":
    pytest.main(['-s -v', 'test_case_galileo_V110.py'])
    # pytest.main(['-s -v', 'test_case_galileo_V110.py::TestEdaAutoCase::test_high_speed_etl_error'])
    # pytest.main('-s -v test_case_galileo_V110.py::TestEdaAutoCase::test_high_speed_etl_error')
