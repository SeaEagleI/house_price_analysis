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
