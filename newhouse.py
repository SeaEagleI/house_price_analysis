# 保存到csv文件
import json
import os.path as op
import time
import requests
from config import newhouse_api, newhouse_file, use_cache

# headers
headers = {
    "User-Agent": "Beike2.6.0;Xiaomi MIX+2; Android 8.0.0"
}
# target city
city_id = 110000  # beijing
city_abbr = "bj"
# other params
page_size_limit = 20


# Parse newhouse format api
def get_api_data(url, params):
    res = requests.get(url, params=params, headers=headers)
    # assert res.json()["msg"] == "OK", "Failed on {}\t{}".format(api_url, params)
    return res.json()["data"]["resblock_list"]


# Update $total_houses (totalCount of newhouse)
def update_total_builds(city_id):
    return int(get_api_data(newhouse_api, {"cityId": city_id})["total_count"])


# Crawl & Save all newhouse infos to a dict
def get_newhouse_info(city_id, city_abbr):
    # Glad to find:
    # 1) $total_builds < 3k, no need to divide;
    # 2) no replications are found in this type of mobile-client api data crawling, no need to retry;
    # 3) max result size limit for each page is 20.
    payload = {
        "city_id": 110000,  # "330100",
        "page": 0,
    }
    total_builds = update_total_builds(city_id)
    start_t, total_cnt, repl_cnt, page_id, build_dict = time.perf_counter(), 0, 0, 0, {}
    while True:
        payload["page"] = page_id
        data = get_api_data(newhouse_api, payload)
        build_list = data["list"]
        for build in build_list:
            id = "newhouse-" + build["fb_expo_id"] if "pid" in build \
                else "ershoufang-" + build["ershou_info"]["house_info"]["house_code"]
            build_dict[id] = build
        total_cnt += len(build_list)
        repl_cnt = total_cnt - len(build_dict)
        rest_cnt = total_builds - total_cnt
        speed = total_cnt / (time.perf_counter() - start_t)
        print("\rTotal: {}/{}/{}, Repl {}, Pages {} || Time: {:.1f}s, Speed {:.1f}/s, ETA {}"
              .format(len(build_dict), total_cnt, total_builds, repl_cnt, page_id + 1, time.perf_counter() - start_t,
                      speed, "{:.1f}s".format(rest_cnt / speed) if speed > 0 else "---"), end="")
        if data["has_more_data"] != "1" or len(build_list) < page_size_limit:
            break
        page_id += 1
    print()
    # Calc replication_ratio
    print("repl_ratio: {:.1f}%".format(repl_cnt / len(build_dict) * 100))
    json.dump(build_dict, open(newhouse_file.format(city_abbr), "w+", encoding="utf-8"), ensure_ascii=False, indent=4)
    return build_dict


if __name__ == "__main__":
    json_file = newhouse_file.format(city_abbr)
    house_dict = json.load(open(json_file, encoding="utf-8")) if use_cache and op.exists(json_file) \
        else get_newhouse_info(city_id, city_abbr)
    print("Crawled & Saved {} ershoufang infos.".format(len(house_dict)))
