import json

import pandas as pd
import numpy as np
import time
from tqdm import tqdm
from getGeocode import getGeocode_gaode, getGeocode_baidu
from general_config import proc_file, city_abbr, na_values, cluster_file, json_file

task = "ershoufang"
sub_task = "xiaoqu_pos"

def genJsFile(df, col, filepath, interval=0.01, api_provider="gaode"):
    if col not in df.columns:
        return
    str_head = "var heatmapData = ["
    invalid = []  # store invalid address info
    getGeo = getGeocode_gaode if api_provider == "gaode" else getGeocode_baidu
    for name, count in df[col].value_counts().items():
        lng, lat = getGeo("北京市 " + name)
        if lat >= 41.7 or lat <= 39.3 or lng <= 115.6 or lng >= 117.5:
            invalid.append((name, count, lat, lng))
            continue
        str_head += '{' + f'"lng":{lng}, "lat":{lat}, "count":{count}' + '},'
        time.sleep(interval)
    result = str_head[:-1] + "]"
    with open(filepath, 'w') as f:
        f.write(result)
    return invalid


def genJsFile2(df, filepath, interval=0.01, api_provider="gaode"):
    price = df.groupby("小区")[["小区", "小区均价(元/㎡)"]].apply(lambda i: i.iloc[0])
    price["小区均价(元/㎡)"] = price["小区均价(元/㎡)"].apply(getPrice)
    price['geocode'] = price["小区"].apply(getGeocode_gaode)
    maxv = price["小区均价(元/㎡)"].max()
    price["p_std"] = price["小区均价(元/㎡)"].apply(lambda i: i/maxv*100)

    str_head = "var heatmapData = ["
    length = price.shape[0]
    invalid = []
    for i in range(length):
        count = price.iloc[i]['p_std']
        lng, lat = price.iloc[i]['geocode']
        if lat >= 41.7 or lat <= 39.3 or lng <= 115.6 or lng >= 117.5:
            invalid.append((price.iloc[i]['小区'], count, lat, lng))
            continue
        str_head += '{' + f'"lng":{lng}, "lat":{lat}, "count":{count}' + '},'
    result = str_head[:-1] + "]"
    with open(filepath, 'w') as f:
        f.write(result)
    return invalid


def getPrice(raw_str):
    price = raw_str.split("元")[0]
    try:
        num = int(price)
    except:
        num = 0
    return num


# generate map js for cluster geo-display
def genJsFile3(cluster_df, xiaoqu_pos, col):
    for index, data in cluster_df.groupby("cluster"):
        print(index, data.shape[0])
        str_head = "var heatmapData = ["
        for name, count in tqdm(data[col].value_counts().items()):
            if name in xiaoqu_pos:
                lng, lat = xiaoqu_pos[name]
            else:
                print(f"KeyError: {name}")
                continue
            str_head += '{' + f'"lng":{lng}, "lat":{lat}, "count":{count}' + '},'
        result = str_head[:-1] + "]"
        with open("data/cluster{}.js".format(index), 'w') as f:
            f.write(result)


if __name__ == "__main__":
    # df = pd.read_csv(proc_file.format(city_abbr, task), na_values=na_values)
    cluster_df = pd.read_csv(cluster_file.format(city_abbr, task), encoding="gbk", na_values=na_values)
    xiaoqu_pos = json.load(open(json_file.format(city_abbr, sub_task), encoding="utf-8"))
    # invalid = genJsFile(df, "小区", "HeatMap_count.js")
    # invalid = genJsFile2(df, "HeatMap_price.js")
    genJsFile3(cluster_df, xiaoqu_pos, "小区")
