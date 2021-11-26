# reference: https://github.com/CaoZ/Fast-LianJia-Crawler
# 每组查询最多拿到3k个结果, 而二手房总数在91k+,
# 故需要通过条件组合对结果进行细粒度分流, 确保每个组合条件下的结果在3k以内, 且所有组合加起来没有遗漏, 最后再将所有结果合并.
# 组合条件: <区域>, 将区域降到商圈级别即可保证每个筛选结果均在3k以内.
import json
import time
import requests
import random
import os.path as op
import numpy as np
import multiprocessing
from tqdm import tqdm
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from city import update_city
from config import ershoufang_api, turn_delays, use_cache, page_size_limit, repl_dict, ershoufang_detail_page, \
    num_workers, max_retry_turns, user_agent_pc
from general_config import json_file, city_id, city_abbr

# params
task = "ershoufang"
headers = {"User-Agent": ""}


# Get ershoufang List via general api
## Parse liverpool format api
def get_api_data(url, params):
    # Measures to avoid lock-down: 1) set random delay to avoid high-parallelism collisions.
    time.sleep(random.choice(turn_delays))
    # Measures to avoid lock-down: 2) set random UA to simulate different manual access.
    headers["User-Agent"] = UserAgent().random
    res = requests.get(url, params=params, headers=headers)
    try:
        data = res.json()["data"]["data"]["getErShouFangList"]
        return data
    # Exit program if ip lock-down occurs
    except:
        if "封禁原因" in res.text:
            print("\nip因访问频繁被封,", url)
        exit(1)


## Update $total_houses or $bc_total_houses (totalCount of ershoufang, frequently changes)
def update_total_houses(city_id, bc_quan_pin=""):
    payload = {"cityId": city_id, "condition": bc_quan_pin} if bc_quan_pin else {"cityId": city_id}
    return get_api_data(ershoufang_api, payload)["totalCount"]


# Get more specific infos from house detail page
## Process strings
def pre(s):
    s = str(s)
    for k, v in repl_dict.items():
        s = s.replace(k, v)
    return s


## Get soup (PC UA required)
def get_soup(url, turn_id=0):
    if turn_id >= max_retry_turns:
        print("RETRY {} times, Failed to load {}".format(turn_id, url))
        exit(1)
    headers["User-Agent"] = user_agent_pc
    r = requests.get(url, headers=headers)
    # assert r.status_code == 200, "ConnectionError for {}".format(url)
    if r.status_code != 200:
        print("TURN {}, StatusCodeError {} for {}".format(turn_id, r.status_code, url))
        time.sleep(2)
        return get_soup(url, turn_id + 1)
    if "封禁原因" in r.text:
        print("\nip因访问频繁被封,", url)
        exit(1)
    return BeautifulSoup(r.text, "html.parser")


## Parse webpage
def parse_ershoufang_page(page_url):
    data = {}
    soup = get_soup(page_url)
    # 2) 房源基本信息 (电梯、装修等)
    intro_divs = soup("div", attrs={"class": "introContent"})
    intro_data = {pre(k): pre(v) for k, v in [list(li.strings) for li in intro_divs[0]("li")]}
    if len(intro_divs) == 2:
        intro_data["tags"] = [pre(s) for s in intro_divs[1]("div", attrs={"class": "content"})[0].strings if pre(s)]
    data.update(intro_data)
    # 3) 房源特色的文字描述 (核心卖点等)         **不处理**
    # 4) 户型分间信息 (每个房间面积、是否有窗户等) **不处理**
    # 5) 小区信息 (建筑时间、均价等)
    xiaoqu_div = soup("div", attrs={"class": "xiaoqu_main fl"})[0]
    xiaoqu_spans = [span for span in xiaoqu_div("span") if span.has_attr("class")]
    xiaoqu_data = {pre(l.string): pre(s.string) for l, s in zip(xiaoqu_div("label"), xiaoqu_spans)}
    # 1) 小区名
    xiaoqu_data["community"] = pre(soup("a", attrs={"class": "info no_resblock_a"})[0].string)
    data.update(xiaoqu_data)
    # 6) 首付信息
    calc_divs = soup("div", attrs={"class": "m-calculator"})
    if calc_divs:
        shoufu_data = json.loads(calc_divs[0]["data-shoufu"])
        shoufu_data.pop("mzAgent")
        data.update(shoufu_data)
    return data


# Main process of Crawler, including API & WebPage
def get_ershoufang_info(city_id, district_dict, proc_bizcircle_list, total_houses, pid, queue=None):
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
    start_t, total_cnt, repl_cnt, proc_house_dict = time.perf_counter(), 0, 0, {}
    for idx, bizcircle in enumerate(proc_bizcircle_list):
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
                detail_data = parse_ershoufang_page(ershoufang_detail_page.format(house["houseCode"]))
                house.update(detail_data)
                proc_house_dict[house["houseCode"]] = house
            bc_total_cnt += len(house_list)
            total_cnt += len(house_list)
            repl_cnt = total_cnt - len(proc_house_dict)
            rest_cnt = total_houses - total_cnt
            speed = bc_total_cnt / (time.perf_counter() - bc_start_t)
            print("[{}] [{}/{}][{}-{}] Total: {}/{}/{}, Repl {} || Current: {}/{}, Pages {} "
                  "|| Time: {:.1f}s/{:.1f}s, Speed {:.1f}/s, ETA {}"
                  .format(pid, idx + 1, len(proc_bizcircle_list), bizcircle.name, district_name,
                          len(proc_house_dict), total_cnt, total_houses, repl_cnt,
                          bc_total_cnt, bc_total_houses, page_id,
                          time.perf_counter() - bc_start_t, time.perf_counter() - start_t,
                          speed, "{:.1f}s".format(rest_cnt / speed) if speed > 0 else "---",
                          ))
            if data["hasMoreData"] != 1 or len(house_list) < page_size_limit:
                break
            page_id += 1
        print()
    if queue is not None:
        queue.put(proc_house_dict)
    print("END Proc {}, {} bizcircles, {} houses".format(pid, len(proc_bizcircle_list), len(proc_house_dict)))
    return proc_house_dict


# Coarse-grained Scheduler to balance payload among processes
def scheduler(bizcircle_list, num_procs):
    total_houses = update_total_houses(city_id)
    bizcircle_dict = {b.id: b for b in bizcircle_list}
    length_dict = dict(sorted([[b.id, update_total_houses(city_id, b.quan_pin)] for b in
                               tqdm(bizcircle_list, desc="Update bc houses")], key=lambda x: x[1], reverse=True))
    print("Bizcircle_Lens: ", length_dict, "\n")
    sum_bc_total_houses = sum(length_dict.values())
    schedule_list, proc_lens, unit = [[] for i in range(num_procs)], [0] * num_procs, sum_bc_total_houses / num_procs
    for pid in range(num_procs - 1):
        # 选length_dict和不超过unit的前k个, k尽可能大
        k, sum_ = 0, 0
        for bid, l in length_dict.items():
            k, sum_ = k + 1, sum_ + l
            if sum_ > unit:
                k, sum_ = k - 1, sum_ - l
                break
        for bid in list(length_dict.keys())[:k]:
            length_dict.pop(bid)
            schedule_list[pid].append(bizcircle_dict[bid])
        rest = unit - sum_
        proc_lens[pid] = sum_
        # 从剩余length_dict中选abs与rest差最小的
        if length_dict and rest >= 1:
            length_list = list(length_dict.items())
            bid, l = length_list[np.argmin(np.abs(np.array(list(length_dict.values())) - rest))]
            length_dict.pop(bid)
            schedule_list[pid].append(bizcircle_dict[bid])
            proc_lens[pid] = sum_ + l
        if not length_dict:
            break
    schedule_list[num_procs - 1] = [bizcircle_dict[bid] for bid in length_dict]
    proc_lens[num_procs - 1] = sum(length_dict.values())
    print(f"Scheduler:\nT{total_houses}, S{sum_bc_total_houses}, P{sum(proc_lens)}")
    # Metrics
    avg_abs = np.mean(np.abs(np.array(proc_lens) - unit))
    print("Unit {:.1f}, Avg_ABS {:.1f}, Proc_Lens {}".format(unit, avg_abs, proc_lens))
    for pid, schedule in enumerate(schedule_list):
        print(f"[{pid}] L{len(schedule)} {[(b.id, b.name) for b in schedule]}")
    print()
    return schedule_list, proc_lens


# Controller for multi-process
def run_crawler():
    city, district_dict, bizcircle_list = update_city(city_id, city_abbr)
    schedule_list, proc_lens = scheduler(bizcircle_list, num_workers)
    house_dict, jobs = {}, []
    q = multiprocessing.Queue()
    for pid in range(num_workers):
        p = multiprocessing.Process(target=get_ershoufang_info,
                                    args=(city_id, district_dict, schedule_list[pid], proc_lens[pid], pid, q))
        jobs.append(p)
        p.start()
    print("Jobs:", len(jobs))
    for idx, p in enumerate(jobs):
        proc_data = q.get()
        house_dict.update(proc_data)
        print("GOT {}, Len {}, Total {}".format(idx + 1, len(proc_data), len(house_dict)))
    json.dump(house_dict, open(json_file.format(city_abbr, task), "w+", encoding="utf-8"), ensure_ascii=False, indent=4)
    return house_dict


if __name__ == "__main__":
    use_cache = False
    ershoufang_json = json_file.format(city_abbr, task)
    house_dict = json.load(open(ershoufang_json, encoding="utf-8")) if use_cache and op.exists(json_file) \
        else run_crawler()
    print("Crawled & Saved {} ershoufang infos.".format(len(house_dict)))
