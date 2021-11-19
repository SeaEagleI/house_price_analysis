import os, os.path as op

# City
city_id = 110000
city_abbr = "bj"

# Task
main_tasks = ["ershoufang", "zufang"]    # including json/csv/preprocess files
sub_tasks = ["city_info", "complement"]  # including json file only

# Files
data_dir = "../data"
json_file = op.join(data_dir, "{}_{}.json")               # 1 for city_abbr, 2 for task from main_tasks & sub_tasks
csv_file = op.join(data_dir, "{}_{}.csv")
proc_file = op.join(data_dir, "{}_{}_preprocessed.csv")
# Create dir
if not op.exists(data_dir):
    os.makedirs(data_dir)

# Other Params
use_config = True
nan_values = ["None", "nan", "未知", "暂无数据"]

# Fields: {ershoufang: 46, }
sel_fields = {
    "ershoufang": ['community', 'evaluation', 'framePicture.1.url', 'houseCode', 'jumpUrl', 'marketBooth.title',
                   'monthPay', 'monthPayWithInterest', 'monthReduce', 'priceInfoList.unitPriceStr', 'pureShoufuDesc',
                   'recoDesc', 'statusSwitch.isKey', 'statusSwitch.isNew', 'statusSwitch.isVr',
                   'taxResult.taxTotalDesc', 'title', 'totalPriceInfo.title', 'totalShoufuDesc',
                   '上次交易', '交易权属', '产权所属', '供暖方式', '别墅类型', '套内面积', '小区均价', '建筑年代', '建筑类型',
                   '建筑结构', '建筑面积', '户型结构', '房屋年限', '房屋户型', '房屋朝向', '房屋用途', '所在楼层', '抵押信息',
                   '挂牌时间', '梯户比例', '楼栋总数', '燃气价格', '用水类型', '用电类型', '装修情况', '近地铁', '配备电梯'
                   ],
}
tag_fields = ['colorTags.1.key', 'colorTags.1.title', 'colorTags.2.key', 'colorTags.2.title',
              'colorTags.3.key', 'colorTags.3.title', 'colorTags.4.key', 'colorTags.4.title',
              'tags.1', 'tags.2', 'tags.3', 'tags.4']


# Basic Funcs
# Check if a value is nan
def is_NaN(value):
    return str(value) in nan_values


# Value counts for a df.series (diff from df.series.value_counts)
def li_value_counts(values):
    value_counts = {}
    for v in values:
        if is_NaN(v):
            value_counts["None"] = value_counts.get("None", 0) + 1
        else:
            value_counts[v] = value_counts.get(v, 0) + 1
    return value_counts


# Merge results of df column value_counts
def value_counter(df):
    columns = df.columns.to_list()[1:]
    value_counts = {col: li_value_counts(df[col]) for col in columns}
    return value_counts


# Filter fields by cond (for fields selection)
def filter_keys(value_counts, cond):
    return [key for key, counts in value_counts.items() if cond(key, counts)]


# Filter fields & value_counts by cond (for display)
def filter_counts(value_counts, cond):
    return {key: sorted(list(counts.items()), key=lambda x: x[1], reverse=True)
            for key, counts in value_counts.items() if cond(counts)}


