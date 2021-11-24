import pandas as pd
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


if __name__ == "__main__":
    invalid = genJsFile("../data/bj_ershoufang_preprocessed.csv", "小区", "test.js")
