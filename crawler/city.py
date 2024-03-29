import json
import time
import os.path as op
import utils
from config import city_info_api, use_cache
from general_config import json_file

# params
task = "city_info"


class City:
    __tablename__ = "cities"

    def __init__(self, info):
        self.id = info["city_id"]  # 主键
        self.name = info["city_name"]
        self.abbr = info["city_abbr"]
        self.districts_count = len(info["district"])


class District():
    __tablename__ = "districts"

    def __init__(self, city_id, info):
        self.city_id = city_id  # 外键

        self.id = int(info["district_id"])  # 主键
        self.name = info["district_name"]
        self.quan_pin = info["district_quanpin"]
        self.biz_circles_count = len(info["bizcircle"])
        self.last_update = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())


## 一个商圈可能靠近多个行政区, 如: 西城区、东城区下都出现了安定门
class BizCircle():
    __tablename__ = "biz_circles"

    def __init__(self, city_id, district_id, info):
        self.city_id = city_id            # 外键
        self.district_id = [district_id]  # 外键: 不唯一

        self.id = int(info["bizcircle_id"])  # 主键
        self.name = info["bizcircle_name"]
        self.quan_pin = info["bizcircle_quanpin"]


# Crawl & Save city_info, including abbr & districts/biz-circles through city_id
def get_city_info(city_id):
    payload = {
        "params": {"city_id": city_id, "mobile_type": "android", "version": "8.0.1"},
        "fields": {"city_info": "", "city_config_all": ""}
    }
    data = utils.get_data(city_info_api, payload, method="POST")
    city_info = data["city_info"]["info"][0]
    # 查找城市名称缩写
    for a_city in data["city_config_all"]["list"]:
        if a_city["city_id"] == city_id:
            city_info["city_abbr"] = a_city["abbr"]
            break
    assert "city_abbr" in city_info, "抱歉, 链家网暂未收录该城市~"
    json.dump(city_info, open(json_file.format(city_info["city_abbr"]), "w+", encoding="utf-8"), ensure_ascii=False, indent=4)
    return city_info


# Save city_info to $city, $district_dict, $bizcircle_list
def update_city(city_id, city_abbr):
    print("Initializing & Updating city info ... city_id={}".format(city_id))
    city_info_json = json_file.format(city_abbr, task)
    city_info = json.load(open(city_info_json, encoding="utf-8")) if use_cache and op.exists(city_info_json) \
        else get_city_info(city_id)
    city = City(city_info)
    district_dict, bizcircle_dict = {}, {}
    for district_info in city_info["district"]:
        district = District(city.id, district_info)
        district_dict[district.id] = district
        for biz_circle_info in district_info["bizcircle"]:
            bizcircle_id = biz_circle_info["bizcircle_id"]
            # Note: a bizcircle may have more than 2 father districts, so use LIST DataType to store
            # bizcircle"s outer key $district_id, and append new id when necessary
            if bizcircle_id in bizcircle_dict.keys():
                bizcircle_dict[bizcircle_id].district_id += [district.id]
            else:
                bizcircle_dict[bizcircle_id] = BizCircle(city.id, district.id, biz_circle_info)
        # print("city={}, district={}, total_bizcircles={}".format(city.name, district.name, district.biz_circles_count))
    print("Crawled CityInfo of {}: {} districts, {} bizcircles.\n".format(city.abbr, len(district_dict),
                                                                        len(bizcircle_dict)))
    return city, district_dict, list(bizcircle_dict.values())
