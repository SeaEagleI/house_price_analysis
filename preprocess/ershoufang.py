import json
import re
import os, os.path as op
import pandas as pd
from tqdm import tqdm
from map.getGeocode import getGeocode_gaode
from preprocess.config import sel_fields, tag_fields, use_config, is_NaN, value_counter, filter_keys, filter_counts
from general_config import city_abbr, city_name, csv_file, proc_file, na_values, json_file

# Params
task = "ershoufang"
sub_task = "xiaoqu_pos"

# Check if a field's head matches some head in $head_list
def in_heads(key, head_list):
    for head in head_list:
        if key.startswith(head):
            return True
    return False


# Remove all words in $word_list from $s
def remove_words(s, word_list):
    s = str(s)
    for w in word_list:
        s = s.replace(w, "")
    return s


# Del fields for ershoufang
def select_fields(df):
    counts = value_counter(df)
    all_fields = df.columns.to_list()[1:]
    useless_heads = ["agent.", "taxResult.taxFees.", "loanConfig.", "found"]
    del_fields = [key for key in all_fields if in_heads(key, useless_heads)]\
               + filter_keys(counts, lambda x, y: len(y) == 1) \
               + filter_keys(counts, lambda x, y: 1 < len(y) <= 10 and
                             ("color" in x.lower() and not re.findall(r"^colorTags.*?(key|title)$", x) or
                              "color" not in x.lower() and "Url" in x)) \
               + filter_keys(counts, lambda x, y: 0.01 < len(y) / len(df) <= 0.1 and x == "resblockId") \
               + filter_keys(counts, lambda x, y: 0.1 < len(y) / len(df) < 1 and x == "listPictureUrl") \
               + filter_keys(counts, lambda x, y: len(y) == len(df) and x in ["delegateId", "fbExpoId"]) \
               + ["framePicture.1.type", "marketBooth.type", "totalPrice", "unitPrice", "desc", "houseStatus",
                  "bangdanTitle", "房本备件", "brandTags.title", "businessInterest", "businessLoan", "price",
                  "priceInfoList.totalPriceStr", "pureShoufu", "statusSwitch.isHaofang", "taxResult.taxTotal",
                  "taxStatus", "totalInterest", "totalLoan", "totalShoufu", "unitPriceInfo.title"] \
               + tag_fields
    selected_fields = sorted(list(set(all_fields) - set(del_fields)))
    print(f"DEL {len(set(del_fields))}, SEL {len(selected_fields)}\n{selected_fields}")
    # filtered_counts = filter_counts(counts, lambda x: True)     # type2
    # for idx, (col_head, counts) in enumerate(filtered_counts.items()):
    #     print(idx + 1, col_head, "\n", counts[:10])
    return selected_fields


# Get longitude & latitude of houses using $小区 from GaoDe api
def get_house_positions(xiaoqu_series):
    addr_tplt = "{}市{}小区"
    xiaoqu_pos_json = json_file.format(city_abbr, sub_task)
    xiaoqu_dict = json.load(open(xiaoqu_pos_json, encoding="utf-8")) if op.exists(xiaoqu_pos_json) else {}
    for xiaoqu in tqdm(set(xiaoqu_series) - set(xiaoqu_dict), desc="Get XiaoQu Positions"):
        xiaoqu_dict.update({xiaoqu: getGeocode_gaode(addr_tplt.format(city_name, xiaoqu))})
    for xiaoqu in set(xiaoqu_dict) - set(xiaoqu_series):
        xiaoqu_dict.remove(xiaoqu)
    json.dump(xiaoqu_dict, open(xiaoqu_pos_json, "w+", encoding="utf-8"), ensure_ascii=False, indent=4)
    print("Get {} xiaoqu positions".format(len(xiaoqu_dict)))
    longitudes = [xiaoqu_dict[xiaoqu][0] for xiaoqu in xiaoqu_series]
    latitudes = [xiaoqu_dict[xiaoqu][1] for xiaoqu in xiaoqu_series]
    return longitudes, latitudes


# Main proc for ershoufang preprocessing
def preprocess(df):
    modify_values = {
        "recoDesc": lambda x: str(x).split("/")[0] if not is_NaN(x) else x,  # => 区域名 商圈名
        "所在楼层": lambda x: str(x).replace("共", "").replace("层)", "") if not is_NaN(x) else x,
        "framePicture.1.url": lambda x: re.sub(r"w_.*?$", "w_1000", str(x)) if not is_NaN(x) else x,
        "jumpUrl": lambda x: str(x).replace("m.ke.com/bj", "bj.ke.com").split("?")[0] if not is_NaN(x) else x,
        "priceInfoList.unitPriceStr": lambda x: eval(remove_words(x, ["元/平", ","])) if not is_NaN(x) else x,
        "套内面积": lambda x: eval(remove_words(x, ["㎡", ","])) if not is_NaN(x) else x,
        "建筑面积": lambda x: eval(remove_words(x, ["㎡", ","])) if not is_NaN(x) else x,
        "小区均价": lambda x: eval(remove_words(x, ["元/㎡", ","])) if not is_NaN(x) else x,
        "建筑年代": lambda x: eval(remove_words(x, ["年建成", ","])) if not is_NaN(x) else x,
        "燃气价格": lambda x: eval(remove_words(x, ["元/m3", ","])) if not is_NaN(x) else x,
        "楼栋总数": lambda x: remove_words(x, ["栋"]) if not is_NaN(x) else x,
    }
    split_fields = {
        "recoDesc": [" ", {0: "区域", 1: "商圈"}],
        "所在楼层": ["(", {0: "所在楼层", 1: "楼层总数(层)"}],
    }
    rename_fields = {
        "title": "房源标题",
        "community": "小区",
        "framePicture.1.url": "户型图",
        "jumpUrl": "详情页",
        "marketBooth.title": "榜单标题",
        "statusSwitch.isKey": "随时可看",
        "statusSwitch.isNew": "新上房源",
        "statusSwitch.isVr": "VR房源",
        "上次交易": "上次交易时间",
        "evaluation": "评估价(元)",
        "monthPay": "月供-等额本金(元)",
        "monthPayWithInterest": "月供-等额本息(元)",
        "monthReduce": "每月递减(元)",
        "pureShoufuDesc": "净首付(万元)",
        "taxResult.taxTotalDesc": "税费合计(万元)",
        "totalShoufuDesc": "首付总计(万元)",
        "totalPriceInfo.title": "总价(万元)", # 成交价
        "priceInfoList.unitPriceStr": "单价(元/㎡)",
        "套内面积": "套内面积(㎡)",
        "建筑面积": "建筑面积(㎡)",
        "小区均价": "小区均价(元/㎡)",
        "燃气价格": "燃气价格(元/m³)",
        "建筑年代": "建成年份",
        "楼栋总数": "小区楼栋总数(栋)",
    }
    # use_config = False
    # 创建新列（含新列修改值）
    df["近地铁"] = df.apply(lambda row: "地铁" in "".join([str(i) for i in row[tag_fields]]), axis=1)
    df["经度"], df["纬度"] = get_house_positions(df["community"])
    # 字段筛选
    fields = sel_fields[task] if use_config and sel_fields[task] else select_fields(df)
    print("Reduced Cols: {} -> {}".format(len(df.columns), len(df[fields].columns)))
    df = df[fields]
    # 修改值
    for col, func in modify_values.items():
        df[col] = df[col].map(func)
    # 列分解（含新列重命名）
    for col, (sep, rename_dict) in split_fields.items():
        df_split = df[col].str.split(sep, expand=True).rename(columns=rename_dict)
        df = df.drop([col], axis=1).join(df_split)
    # 列重命名
    for k, v in rename_fields.items():
        df.rename(columns={k: v}, inplace=True)
    return df


if __name__ == "__main__":
    df = pd.read_csv(csv_file.format(city_abbr, task), na_values=na_values)
    df = preprocess(df)
    print(df.info())
    df.to_csv(proc_file.format(city_abbr, task))

