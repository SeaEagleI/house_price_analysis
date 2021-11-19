#!/usr/bin/env python
# coding: utf-8
import pandas as pd
from preprocess.config import csv_file, proc_file, city_abbr

task = "ershoufang"

# 导入文件
df = pd.read_csv(csv_file.format(city_abbr, task), engine="python", thousands=",")
# 按"/"对列分割, 并重命名新列
df2 = df["bangdanTitle"].str.split("/", expand=True).rename(columns={0: "type", 1: "area", 2: "address"})
df3 = df["recoDesc"].str.split("/", expand=True).rename(columns={0: "region", 1: "floorType", 2: "orientation"})
# 将新列与原表连接，并删除原有聚合列
df4 = df.drop(["bangdanTitle", "recoDesc"], axis=1).join(df2).join(df3)
df4.head()
# 删除面积标签下数据的单位
df4["area"] = df4["area"].map(lambda x: str(x)[:-2])
# 将处理后的数据导出为csv
df4.to_csv(proc_file.format(city_abbr, task))
