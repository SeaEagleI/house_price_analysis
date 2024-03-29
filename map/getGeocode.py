import requests
import urllib
import hashlib


# 通过百度地图API获得$address字段的经纬度
def getGeocode_baidu(address):
    # 计算校验SN(百度API文档说明需要此步骤)
    ak = "G5MBCV9mqQ72slnMQgFy7hxGMvGkDFbL"  # 参照自己的应用
    sk = "py0kOwWshoE7FxlE3cXTqW7f9zkZpTUq"  # 参照自己的应用
    url = "http://api.map.baidu.com"
    query = "/geocoder/v2/?address={0}&ak={1}&output=json&city=北京市".format(
        address, ak)
    encodedStr = urllib.parse.quote(query, safe="/:=&?#+!$,;'@()*[]")
    sn = hashlib.md5(urllib.parse.quote_plus(
        encodedStr + sk).encode()).hexdigest()
    # 使用requests获取返回的json
    response = requests.get("{0}{1}&sn={2}".format(url, query, sn))
    data = eval(response.text)
    lat = data["result"]["location"]["lat"]
    lon = data["result"]["location"]["lng"]
    return [lon, lat]


# 通过高德地图API获得$address字段的经纬度
def getGeocode_gaode(address):
    params = {'address': address,
              'key': '2c819296021954877f97bdee73877818',
              'city': '010'}
    base = 'http://restapi.amap.com/v3/geocode/geo'
    answer = requests.get(base, params).json()
    try:
        res = [float(i) for i in answer['geocodes'][0]['location'].split(',')]
        return res
    except Exception as e:
        print(params, "\n", answer)
        print(e)
        exit(1)


if __name__ == "__main__":
    print("baidu-北京大学软件与微电子学院经纬度信息 " + str(getGeocode_baidu("北京大学软件与微电子学院")))
    print("gaode-北京大学软件与微电子学院经纬度信息 " + str(getGeocode_gaode("北京大学软件与微电子学院")))
