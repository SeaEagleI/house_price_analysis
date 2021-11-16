#!/usr/bin/env python
# coding: utf-8
import pandas as pd

#导入文件
df = pd.read_csv('C:\\Users\\Messy XUE\\Desktop\\bj_ershoufang.csv',engine="python",thousands=',')


#按'/'对两列进行分割
df2=df['bangdanTitle'].str.split('/',expand=True)
df3=df['recoDesc'].str.split('/',expand=True)


#对分割出来的新列命名
df2.rename(columns={0:'type',1:'area',2:'address'},inplace=True)
df3.rename(columns={0:'region',1:'floorType',2:'orientation'},inplace=True)


#将新列与原表连接，并删除原有聚合列
df4=df.drop('bangdanTitle',axis=1).drop('recoDesc',axis=1).join(df2).join(df3)
df4.head()


#删除面积标签下数据的单位
df4['area']=df4['area'].map(lambda x: str(x)[:-2])


#将处理后的数据导出为csv
df4.to_csv("C:\\Users\\Messy XUE\\Desktop\\ershoufang.csv")