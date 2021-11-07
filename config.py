import os, os.path as op

# User Infos to generate authorization key
user_agent = "HomeLink7.7.6; Android 7.0"
app_id = "20161001_android"
app_secret = "7df91ff794c67caee14c3dacd5549b35"

# APIs (all in GET method)
city_info_api = "http://app.api.lianjia.com/config/config/initData"
ershoufang_api = "https://m.ke.com/liverpool/api/ershoufang/getList"
zufang_api = "https://app.api.ke.com/Rentplat/v2/house/list"
newhouse_api = "https://app.api.ke.com/newhouse/shellapp/feed"

# Files
data_dir = "data"
city_info_file = op.join(data_dir, "{}_city_info.json")
ershoufang_file = op.join(data_dir, "{}_ershoufang.json")
zufang_file = op.join(data_dir, "{}_zufang.json")
newhouse_file = op.join(data_dir, "{}_newhouse.json")
# Create dir
if not op.exists(data_dir):
    os.makedirs(data_dir)

# Other Params
use_cache = True
turn_delay = 0.2
max_pages = 100
max_retry_turns = 3
page_size_limit = 30

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
