import wordcloud
from tqdm import tqdm
import json
import pandas as pd
from general_config import city_abbr, proc_file
from preprocess.config import value_counter

task = "ershoufang"

# TODO List item 1: 所有房源分析（哪些类型/特点的房子最多: 楼层？价格？房屋类型 ==> 词云/词频统计）
df = pd.read_csv(proc_file.format(city_abbr, task))
counts_dict = value_counter(df)
for field, value_counts in counts_dict.items():
    print(field, len(value_counts), list(value_counts.items())[:5])
