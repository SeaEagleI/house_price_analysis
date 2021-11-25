import pandas as pd
import numpy as np
import time
from getGeocode import getGeocode_gaode, getGeocode_baidu


def genJsFile(src, col, filepath, interval=0.01, api_provider="gaode"):
    df = pd.read_csv(src)
    if (col not in df.columns):
        return
    str_head = "var heatmapData = ["
    invalid = []  # store invalid address info
    getGeo = getGeocode_gaode if api_provider == "gaode" else getGeocode_baidu
    for name, count in df[col].value_counts().items():
        lng, lat = getGeo("北京市 " + name)
        if (lat >= 41.7 or lat <= 39.3 or lng <= 115.6 or lng >= 117.5):
            invalid.append((name, count, lat, lng))
            continue
        item = '{' + \
            '"lng":{0}, "lat":{1}, "count":{2}'.format(
                lng, lat, count) + '},'
        str_head += item
        time.sleep(interval)
    result = str_head[:-1] + "]"
    with open(filepath, 'w') as f:
        f.write(result)
    return invalid


def genJsFile2(src, filepath, interval=0.01, api_provider="gaode"):
    df = pd.read_csv(src)
    price = df.groupby("小区")[["小区", "小区均价"]].apply(lambda i: i.iloc[0])
    price["小区均价"] = price["小区均价"].apply(getPrice)
    price['geocode'] = price["小区"].apply(getGeocode_gaode)
    maxv = price["小区均价"].max()
    price["p_std"] = price["小区均价"].apply(lambda i: i/maxv*100)

    str_head = "var heatmapData = ["
    length = price.shape[0]
    invalid = []
    for i in range(length):
        count = price.iloc[i]['p_std']
        lng, lat = price.iloc[i]['geocode']
        if (lat >= 41.7 or lat <= 39.3 or lng <= 115.6 or lng >= 117.5):
            invalid.append((price.iloc[i]['小区'], count, lat, lng))
            continue
        item = '{' + \
            '"lng":{0}, "lat":{1}, "count":{2}'.format(
                lng, lat, count) + '},'
        str_head += item
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

if __name__ == "__main__":
    # invalid = genJsFile("../data/bj_ershoufang_preprocessed.csv", "小区", "HeatMap_count.js")
    invalid = genJsFile2(
        "../data/bj_ershoufang_preprocessed.csv", "HeatMap_price.js")
