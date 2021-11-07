import base64
import hashlib
import time
import requests
import config


def get_data(url, payload, method='GET', session=None):
    payload['request_ts'] = int(time.time())
    headers = {
        'User-Agent': config.user_agent,
        'Authorization': get_token(payload)
    }
    if session:
        if method == 'GET':
            r = session.get(url, params=payload, headers=headers)
        else:
            r = session.post(url, data=payload, headers=headers)
    else:
        func = requests.get if method == 'GET' else requests.post
        r = func(url, payload, headers=headers)
    return parse_data(r)


def parse_data(response):
    as_json = response.json()
    if as_json['errno']:
        # 发生了错误
        raise Exception('请求出错了: ' + as_json['error'])
    else:
        return as_json['data']


def get_token(params):
    data = list(params.items())
    data.sort()
    token = config.app_secret
    for entry in data:
        token += '{}={}'.format(*entry)
    token = hashlib.sha1(token.encode()).hexdigest()
    token = '{}:{}'.format(config.app_id, token)
    token = base64.b64encode(token.encode()).decode()
    return token


# Convert json files => encoding='utf-8', ensure_ascii=False (display chinese characters normally under utf-8)
# def convert_jsons():
#     json_files = [f for f in os.listdir() if f.startswith('bj') and f.endswith('.json')]
#     print(json_files)
#     for file in json_files:
#         try:
#             data = json.load(open(file, encoding='utf-8'))
#             print(file, 'utf-8')
#             json.dump(data, open(file, 'w+', encoding='utf-8'), ensure_ascii=False, indent=4)
#             print('converted {}'.format(file))
#         except:
#             data = json.load(open(file, encoding='gbk'))
#             print(file, 'gbk')
#             continue

