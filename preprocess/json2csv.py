import json
import pandas as pd
import copy
from tqdm import tqdm
import pyperclip

from general_config import json_file, city_abbr


# flatten dict to multiple list: enumerate all path to leave values in dict_data
# dict_data structure: 1) key->dict_type3; 2) key->list->dict_type3; 3) key->str/int/bool/null; 4) key->list->str.
# example for type4: field "coupon_template_id" in file bj_zufang.json .etc
# yield/return once for each str/int/bool/null leave value recursively.
def flatten_dict(data, pre=None):
    pre = pre if pre else []
    if isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value, dict):
                if len(value) == 0:
                    yield pre + [key, None]
                else:
                    for d in flatten_dict(value, pre + [key]):
                        yield d
            elif isinstance(value, list):
                if len(value) == 0:
                    yield pre + [key, None]
                else:
                    for idx, v in enumerate(value):
                        for d in flatten_dict(v, pre + [key, str(idx + 1)]):  # avoid overlap
                            yield d
            # process dict's single values/items
            elif value in ["", None]:
                yield pre + [key, None]
            else:
                yield pre + [key, value]
    # process list's single values/items
    elif data in ["", None]:
        yield pre + [None]
    else:
        assert isinstance(data, str), \
            f"Another data structure of sample found: ...key->list->{type(data)}\n{data}"
        yield pre + [data]


def json2csv(json_file):
    json_data = json.load(open(json_file, encoding="utf-8"))
    csv_data = []
    for idx, sample in tqdm(json_data.items()):
        line = {}
        for i in flatten_dict(sample):
            line[".".join(i[:-1])] = i[-1]
        csv_data.append(copy.deepcopy(line))
    df = pd.DataFrame(csv_data)
    pyperclip.copy('\n'.join(df.columns.values))
    print(df.head())
    print(df.info())
    csv_file = json_file.replace(".json", ".csv")
    df.to_csv(csv_file, encoding="utf-8")


if __name__ == "__main__":
    # 二手房/租房/新房
    json2csv(json_file.format(city_abbr, "ershoufang"))
    # json2csv(json_file.format(city_abbr, "zufang"))

