# reference: https://github.com/CaoZ/Fast-LianJia-Crawler
# 每组查询最多拿到3k个结果, 而二手房总数在91k+,
# 故需要通过条件组合对结果进行细粒度分流, 确保每个组合条件下的结果在3k以内, 且所有组合加起来没有遗漏, 最后再将所有结果合并.
# 组合条件: <区域>, 将区域降到商圈级别即可保证每个筛选结果均在3k以内.
import json
import re
import time
import requests
import os.path as op
from fake_useragent import UserAgent
from city import update_city
from config import ershoufang_api, ershoufang_file, turn_delay, use_cache, page_size_limit

# set random User-Agent
headers = {"User-Agent": ""}
# target city
city_id = 110000  # beijing
city_abbr = "bj"


# Parse liverpool format api
def get_api_data(url, params):
    # Measures to avoid lock-down: 1) set random UA to simulate different manual access.
    headers["User-Agent"] = UserAgent().random
    res = requests.get(url, params=params, headers=headers)
    try:
        data = res.json()["data"]["data"]["getErShouFangList"]
        return data
    # Exit program if ip lock-down occurs
    except:
        if re.findall(r"封禁原因", res.text):
            print("\nip因访问频繁被封")
        exit(1)


# Update $total_houses (totalCount of ershoufang, which changes frequently)
def update_total_houses(city_id):
    return get_api_data(ershoufang_api, {"cityId": city_id})["totalCount"]


# Crawl & Save all ershoufang house infos to a dict
def get_ershoufang_info(city_id, city, district_dict, bizcircle_list):
    # Patterns: (Complexity: Medium)
    # 1) Σ$bc_total_houses == $total_houses;
    # 2) every $bc_total_houses is less than 3k (the result size upper bound in a conditional search);
    # 3) no replications are found when crawling api data;
    # 4) results are certain (not randomized), no need to retry.
    payload = {
        "cityId": city_id,
        "condition": "",
        "curPage": 1,
    }
    start_t, total_cnt, repl_cnt, house_dict = time.perf_counter(), 0, 0, {}
    for idx, bizcircle in enumerate(bizcircle_list):
        total_houses = update_total_houses(city_id)
        payload["condition"] = bizcircle.quan_pin
        data = get_api_data(ershoufang_api, payload)
        bc_total_houses = data["totalCount"]
        district_name = ",".join(district_dict[did].name for did in bizcircle.district_id)
        bc_start_t, bc_total_cnt, page_id = time.perf_counter(), 0, 1
        while True:
            payload["curPage"] = page_id
            data = get_api_data(ershoufang_api, payload)
            house_list = data["list"]
            for house in house_list:
                house_dict[house["houseCode"]] = house
            bc_total_cnt += len(house_list)
            total_cnt += len(house_list)
            repl_cnt = total_cnt - len(house_dict)
            rest_cnt = total_houses - total_cnt
            speed = bc_total_cnt / (time.perf_counter() - bc_start_t)
            print("\r{:>3}) [{}-{}] Total: {}/{}/{}, Repl {} || Current: {}/{}, Pages {} "
                  "|| Time: {:.1f}s/{:.1f}s, Speed {:.1f}/s, ETA {}"
                  .format(idx + 1, bizcircle.name, district_name,
                          len(house_dict), total_cnt, total_houses, repl_cnt,
                          bc_total_cnt, bc_total_houses, page_id,
                          time.perf_counter() - bc_start_t, time.perf_counter() - start_t,
                          speed, "{:.1f}s".format(rest_cnt / speed) if speed > 0 else "---",
                          ), end="")
            if data["hasMoreData"] != 1 or len(house_list) < page_size_limit:
                break
            page_id += 1
            # Measures to avoid lock-down: 2) set crawl delay to simulate manual access.
            time.sleep(turn_delay)
        print()
    # Calc replication_ratio
    print("repl_ratio: {:.1f}%".format(repl_cnt / len(house_dict) * 100))
    json.dump(house_dict, open(ershoufang_file.format(city.abbr), "w+", encoding="utf-8"), ensure_ascii=False, indent=4)
    return house_dict


if __name__ == "__main__":
    city, district_dict, bizcircle_list = update_city(city_id, city_abbr)
    print()
    json_file = ershoufang_file.format(city_abbr)
    house_dict = json.load(open(json_file, encoding="utf-8")) if use_cache and op.exists(json_file) \
        else get_ershoufang_info(city_id, city, district_dict, bizcircle_list)
    print("Crawled & Saved {} ershoufang infos.".format(len(house_dict)))

