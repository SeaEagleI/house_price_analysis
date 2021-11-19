import os, os.path as op

# City
city_id = 110000
city_abbr = "bj"

# Task
main_tasks = ["ershoufang", "zufang"]    # including json/csv/preprocess files
sub_tasks = ["city_info", "complement"]  # including json file only

# User Infos to generate authorization key
user_agent = "HomeLink7.7.6; Android 7.0"
app_id = "20161001_android"
app_secret = "7df91ff794c67caee14c3dacd5549b35"

# APIs (all in GET method)
city_info_api = "http://app.api.lianjia.com/config/config/initData"
ershoufang_api = "https://m.ke.com/liverpool/api/ershoufang/getList"
zufang_api = "https://app.api.ke.com/Rentplat/v2/house/list"
newhouse_api = "https://app.api.ke.com/newhouse/shellapp/feed"

# Detail Urls
ershoufang_detail_page = "https://bj.ke.com/ershoufang/{}.html"

# Files
data_dir = "../data"
json_file = op.join(data_dir, "{}_{}.json")               # 1 for city_abbr, 2 for task from main_tasks & sub_tasks
csv_file = op.join(data_dir, "{}_{}.csv")
proc_file = op.join(data_dir, "{}_{}_preprocessed.csv")
# Create dir
if not op.exists(data_dir):
    os.makedirs(data_dir)

# User-Agent
user_agent_pc = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36"
# Multi-Process
num_workers = 30
# Other Params
use_cache = True
max_pages = 100
max_retry_turns = 3
page_size_limit = 30
turn_delays = [0, 0.1, 0.2, 0.3, 0.4, 0.5]
repl_dict = {r: "" for r in ["\n", "\t", "\r", " "]}

# CSV fields for newhouse
fields = ["item_type", "pid", "id", "city_id", "city_name", "cover_pic", "min_frame_area", "max_frame_area",
          "district_name", "district", "district_id", "bizcircle_name", "build_id", "process_status",
          "resblock_frame_area", "resblock_frame_area_range", "resblock_frame_area_desc", "decoration", "longitude",
          "latitude", "frame_rooms_desc", "title", "resblock_name", "resblock_alias", "address", "store_addr",
          "avg_unit_price", "average_price", "address_remark", "project_name", "special_tags", "frame_rooms",
          "converged_rooms", "tags", "project_tags", "house_type", "sale_status", "has_evaluate", "has_vr_aerial",
          "has_vr_house", "has_short_video", "open_date", "has_virtual_view", "lowest_total_price", "show_price",
          "show_price_unit", "show_price_desc", "status", "subway_distance", "evaluate_status", "show_price_info",
          "brand_id", "preload_detail_image", "reference_avg_price", "reference_avg_price_unit",
          "reference_avg_price_desc", "new_sale_tags", "sale_status_color", "house_type_color", "total_price_start",
          "total_price_start_unit", "avg_price_start", "avg_price_start_unit", "on_time", "project_desc",
          "has_car_activity", "is_new_sale", "first_tags", "recommend_log_info", "recommend_reason"]
