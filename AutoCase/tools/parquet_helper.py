import re
import pandas as pd

# 获取parquet文件绝对路径
parquet_fp = r"D:\proData\Galileo\CN-81_08\20210520\CN-81_08-B-050\2021-05-20_08-00-47.505__IPC.parquet"
test_list = ["gbx_affldd_hss_pinion", "gbx_affldd_hss_wheel", "gbx_affldd_ims_pg"]
# 读取parquet文件，存储为dataFrame形式
df = pd.read_parquet(parquet_fp)
df.to_excel(r"D:\proData\Galileo\CN-81_08\20210520\CN-81_08-B-050\2021-05-20_08-00-47.505__IPC.xlsx",
            index=False)

# # 获取xlsx文件的绝对路径
# column_excel_fp = r"D:\生产环境数据\channeldesc_202105121125.csv"
# # 读取xlsx文件，存储为df形式
# column_df = pd.read_csv(column_excel_fp, usecols=["column_name"])
# # 获取df中的第一列数据
# all_names_str = column_df.columns[0]
#
# # re.split(r'[;,\s]\s*', line)
# # 将获取到的df数据，按照正则表达式进行分割，分隔符号','
# # all_names = re.split(r'[;,\s]\s*', all_names_str)
# # 在数据最后添加公共列的数据
# all_names.extend(["digital_twin_data_id","wind_farm_key","assets_wind_turbine_key","design_wind_turbine_key","calendar_key","wind_farm_time","plc_time","ts_file"])
# # 将获取到的数据输出为xlsx文件形式
# excel_df = df[all_names].to_excel('load_regression_lmt.xlsx')
# # 打印df
# print(df)
