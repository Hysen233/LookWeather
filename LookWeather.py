import requests
import json

HelpMessage = '''------LookWeather-----
一个可以在服务器查看城市天气的插件
!!LW 显示帮助信息
!!LW [城市名] 查看城市天气情况
by laoliu
'''
# 参数 city
url = "http://t.weather.itboy.net/api/weather/city/"
citycode = {}
def display_weather(server, cityName):
    if citycode == {}:
        load_citycodejson()
    req = requests.get(url + str(countyandcity(server,cityName)))
    city_weatherStr = json.dumps(req.json(), ensure_ascii=False, sort_keys=True)
    city_weather = json.loads(city_weatherStr)

    server.say(city_weather['cityInfo']['city'] + '天气未来情况：')
    conut = 0;
    for today in city_weather['data']['forecast']:
        server.say('时间：'+today['ymd']+' '+today['week']+' 气温:'+today['high'].split()[1]+'~'+today['low'].split()[1]+
                   ' 天气：'+today['type']+' 风向：'+today['fx']+today['fl']
                   )
        conut+=1
        if conut > 5:
            break
def countyandcity(server,cityName):
    key = list(citycode.keys())
    print(key.count(cityName))
    if not key.count(cityName) <= 0:
        return citycode[cityName]
    else:
        if not key.count(cityName+'市') <= 0:
            return citycode[cityName+'市']
        elif not key.count(cityName+'县') <= 0:
            return citycode[cityName+'县']
        elif not key.count(cityName[0:len(cityName)-1]) <= 0:
            return citycode[cityName[0:len(cityName)-1]]
        else:
            server.say("请输入一个正确的城市")
def on_info(server, info):
    if info.is_player == 1:
        if info.content == '!!LW':
            server.say(HelpMessage)
        content = info.content;
        command = content.split();
        if len(command) >= 2:
            display_weather(server,command[1])
def load_citycodejson() :
    citycodefile = open('./plugins/citycode.json','rb')
    citycodejson = json.load(citycodefile)
    for cityinfo in citycodejson:
        citycode[cityinfo['city_name']] = cityinfo['city_code']
def on_load(server, old):
    load_citycodejson()