import requests
import urllib
import hashlib


def getGeocode_baidu(address):
    # 计算校验SN(百度API文档说明需要此步骤)
    ak = "G5MBCV9mqQ72slnMQgFy7hxGMvGkDFbL"  # 参照自己的应用
    sk = "py0kOwWshoE7FxlE3cXTqW7f9zkZpTUq"  # 参照自己的应用
    url = "http://api.map.baidu.com"
    query = "/geocoder/v2/?address={0}&ak={1}&output=json".format(address, ak)
    encodedStr = urllib.parse.quote(query, safe="/:=&?#+!$,;'@()*[]")
    sn = hashlib.md5(urllib.parse.quote_plus(
        encodedStr + sk).encode()).hexdigest()
    # 使用requests获取返回的json
    try:
        response = requests.get("{0}{1}&sn={2}".format(url, query, sn))
        data = eval(response.text)
        lat = data["result"]["location"]["lat"]
        lon = data["result"]["location"]["lng"]
    except:
        lat = 0
        lon = 0
    return [lon, lat]


def getGeocode_gaode(address):
    parameters = {'address': address,
                  'key': '2c819296021954877f97bdee73877818'}
    base = 'http://restapi.amap.com/v3/geocode/geo'
    response = requests.get(base, parameters)
    answer = response.json()
    try:
        res = [float(i) for i in answer['geocodes'][0]['location'].split(',')]
    except:
        res = [0, 0]
    return res


if __name__ == "__main__":
    print("baidu-北京大学软件与微电子学院经纬度信息 " + str(getGeocode_baidu("北京大学软件与微电子学院")))
    print("gaode-北京大学软件与微电子学院经纬度信息 " + str(getGeocode_gaode("北京大学软件与微电子学院")))
