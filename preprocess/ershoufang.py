import re
import pandas as pd
from preprocess.config import csv_file, proc_file, sel_fields, tag_fields, city_abbr, use_config, is_NaN, value_counter, \
    filter_keys, filter_counts

# params
task = "ershoufang"


# Check if a field's head matches some head in $head_list
def in_heads(key, head_list):
    for head in head_list:
        if key.startswith(head):
            return True
    return False


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


# Main proc for ershoufang preprocessing
def preprocess(df):
    modify_values = {
        "recoDesc": lambda x: str(x).split("/")[0] if not is_NaN(x) else x,  # => 区域名 商圈名
        "所在楼层": lambda x: str(x).replace(")", "") if not is_NaN(x) else x,
        "framePicture.1.url": lambda x: re.sub(r"w_.*?$", "w_1000", str(x)) if not is_NaN(x) else x,
        "jumpUrl": lambda x: str(x).replace("m.ke.com/bj", "bj.ke.com").split("?")[0] if not is_NaN(x) else x,
        "pureShoufuDesc": lambda x: str(x) + "万" if not is_NaN(x) else x,
        "taxResult.taxTotalDesc": lambda x: str(x) + "万" if not is_NaN(x) else x,
        "totalPriceInfo.title": lambda x: str(x) + "万" if not is_NaN(x) else x,
        "totalShoufuDesc": lambda x: str(x) + "万" if not is_NaN(x) else x,
    }
    split_fields = {
        "recoDesc": [" ", {0: "区域", 1: "商圈"}],
        "所在楼层": ["(", {0: "所在楼层", 1: "楼层总数"}],
    }
    rename_fields = {
        "title": "房源标题",
        "community": "小区",
        "totalPriceInfo.title": "总价(成交价)",
        "priceInfoList.unitPriceStr": "单价",
        "framePicture.1.url": "户型图",
        "jumpUrl": "详情页",
        "marketBooth.title": "榜单标题",
        "statusSwitch.isKey": "随时可看",
        "statusSwitch.isNew": "新上房源",
        "statusSwitch.isVr": "VR房源",
        "evaluation": "评估价",
        "monthPay": "月供(等额本金)",
        "monthPayWithInterest": "月供(等额本息)",
        "monthReduce": "每月递减",
        "pureShoufuDesc": "净首付",
        "taxResult.taxTotalDesc": "税费合计",
        "totalShoufuDesc": "首付总计",
    }
    # use_config = False
    # 创建新列（含新列修改值）
    df["近地铁"] = df.apply(lambda row: "地铁" in "".join([str(i) for i in row[tag_fields]]), axis=1)
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
    df = pd.read_csv(open(csv_file.format(city_abbr, task), encoding="utf-8"))
    df = preprocess(df)
    print(df.head())
    print(df.info())
    df.to_csv(proc_file.format(city_abbr, task))

