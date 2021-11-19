import base64
import hashlib
import time

import requests
import json
from logzero import logger

http_app_id = 'XXXXXXXX'
http_app_secret = 'XXXXXXXXXXXX'
params = {'houseCode': '101111010102',
          'cityId': '110000',
          'fb_expo_id': '462726273153150977',
          }
url = 'https://app.api.ke.com/house/ershoufang/detailpart1v2'


# def get_authorization(params):
#     p_list = [f"{key}={val}" for key, val in params.items()]
#     p_list.sort()
#     sb = http_app_secret + "".join(p_list)
#     logger.info(sb)
#     instance = hashlib.sha1(sb.encode()).hexdigest()
#     logger.info(instance)
#     bs = http_app_id + ":" + instance
#     logger.info(bs)
#     encoder = base64.b64encode(bs.encode("utf-8"))
#     logger.info(encoder)
#     return encoder


def get_authorization():
    date_s = time.strftime("%Y%M%D", time.localtime())
    os_type = "android"
    given_key = "d5e343d453aecca8b14b2dc687c381ca"
    phone = "18810721592"
    password = "wdj1234567"
    time_s = int(time.time())
    raw_comb = given_key + f"mobile_phone_no={phone}&password={password}&request_ts={time_s}"
    raw_key = f"{date_s}_{os_type}:" + hashlib.sha1(raw_comb.encode('utf-8')).hexdigest()
    auth = base64.b64encode(raw_key.encode("utf-8"))
    return auth

# headers = {'Host': 'app.api.ke.com',
#            'Authorization': get_authorization(params),
#            # 'x-req-id': 'c33e78e2-94d8-4c87-b09e-6cd22f3973c1',
#            # 'Page-Schema': 'ershou%2Fdetail',
#            # 'Referer': 'community%2Fershoulist',
#            # 'Cookie': 'lianjia_udid=fd6275273712c97c;lianjia_ssid=db0ad3c2-da83-4806-a726-b87c3a7be016;algo_session_id=0c935a9e-5ad2-40c3-b383-08ceff3e929c;lianjia_uuid=4f514342-8349-4596-a4df-ad6540d45db8', 'Dynamic-SDK-VERSION': '1.1.0', 'Lianjia-City-Id': '110000',
#            # 'parentSceneId': '5640895386532073216',
#            # 'source-global': '{}',
#            # 'User-Agent': 'Beike2.58.0;google Pixel+3; Android 9',
#            # 'Lianjia-Channel': 'Android_ke_tencentd',
#            # 'Lianjia-Device-Id': 'fd6275273712c97c',
#            # 'Lianjia-Version': '2.58.0',
#            # 'Lianjia-Im-Version': '2.34.0',
#            # 'Lianjia-Recommend-Allowable': '1',
#            # 'Authorization':'MjAxODAxMTFfYW5kcm9pZDo5ODkxZjQxYTA2YjVmZWRmMjU4NzI5NTMxZDUzNDZiZDkxM2NjZDEz',
#            # 'extension': 'lj_duid=null&ketoken=TxocRRR8gdDCVkmPzjVOxyC1kVuGFdhcKiYL7BO9nXwObhtCPKKsYdYziLCFcFDw0XluhtsgqwRrzuB5clwZTWE5REOJERbG1rQQJ8aA8AiZK1wHLb3SIBzz6OAz2zIw&lj_android_id=fd6275273712c97c&lj_device_id_android=fd6275273712c97c&mac_id=F0:5C:77:E7:91:6B',
#            # 'ip': '182.140.153.28',
#            # 'wifi_name': 'Tencent-WiFi',
#            # 'lat': '30.552499',
#            # 'lng': '104.068037',
#            # 'beikeBaseData': '%7B%22duid%22%3A%22%22%7D',
#            # 'WLL-KGSA':'LJAPPVA accessKeyId=sjoe98HI099dhdD7; nonce=PiLT6U8QIR8JAZtPbmtRDHbiUF1BEmzc; timestamp=1625123574; signature=q3pLpmpHmDiWCcOArtYFrWULD2ues5EB2bTOHhEl6/U=',
#            # 'Host':'app.api.ke.com',
#            # 'Connection':'Keep-Alive',
#            # 'Accept-Encoding':'gzip',
#            # 'If-Modified-Since': 'Wed, 30 Jun 2021 13:17:18 GMT'
#            }
# r = requests.get(url, params=params, headers=headers)
# logger.info(r.json())


# 每日统计数据
# 分析market层级下数据
# "market": {
#   "title": "贝壳指数",
#   "list": [{
#     "name": "全市均价",
#     "count": "14694",
#     "unit": "元\/平"
#   }, {
#     "name": "昨日成交",
#     "count": "56",
#     "unit": "套"
#   }],
#   "m_url": "https:\/\/m.ke.com\/cd\/fangjia",
#   "more_desc": "查看更多"
# }
# api_url = 'https://app.api.ke.com/config/home/content?city_id=510100'
# auth = get_authorization()

# 新上房源
# 分析 data.list数组中某项数据houseCode存在, 获取infoList中的name为挂牌的获取挂牌时间, 按天归类数据
api_url = 'https://app.api.ke.com/house/ershoufang/searchv4?cityId=510100&condition=tt2&fullFilters=1&hasRecommend=0&limitOffset=0&limitCount=20&request_ts=1539825002'
auth = get_authorization()
# 每日成交数据
# limit_count为每页数量, limit_offset为那一条数据开始查询 request_ts为每次访问时间
# 直接分析data.list数组中数据即可
# {
#   "house_code": "106101510602",
#   "title": "仁厚街38号 3室1厅",
#   "desc": "东南\/高楼层\/7层\/65.88㎡",
#   "resblock_id": "1611061558346",
#   "sign_date": "2018.10.03",
#   "price_str": "86",
#   "price_unit": "万",
#   "unit_price_str": "13055元\/平",
#   "require_login": 0
# }
# api_url = 'https://app.api.ke.com/house/chengjiao/searchv2?channel=sold&city_id=510100&limit_offset=0&limit_count=20&request_ts={}'.format(int(time.time()))
# auth = get_authorization()
headers = {'Authorization': auth}
r = requests.get(api_url, headers=headers)
print(r.json())


