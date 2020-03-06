# coding:utf-8
import os

from getWeatherData import getWeather

monitorCityList='monitorCityList1.csv'
nlist=['北京',
'首尔',
'东京',
'新加坡',
'马尼拉',
'雅加达',
'河内',
'新加坡',
'悉尼',
'华盛顿',
'新德里',
'曼谷',
'德黑兰',
'罗马',
'巴黎',
'柏林',
'伦敦']
# with open(monitorCityList,'w+') as fp:
#     for i in nlist:
#         fp.write(i)
#         fp.write('\n')
import pandas as pd
import requests
import json

#主要关心这三个数据：温度 感染 死亡
def get_data():
    url = 'https://view.inews.qq.com/g2/getOnsInfo?name=disease_h5'
    area = requests.get(url).json()
    data = json.loads(area['data'])
    update_time = data['lastUpdateTime']

    all_counties = data['areaTree']
    for country_data in all_counties:
        print(country_data)

    all_list = []
    for country_data in all_counties:
        if country_data['name'] != '中国':
            continue
        else:
            all_provinces = country_data['children']
            for province_data in all_provinces:
                province_name = province_data['name']
                all_cities = province_data['children']
                for city_data in all_cities:
                    city_name = city_data['name']
                    city_total = city_data['total']
                    province_result = {'province': province_name, 'city': city_name, 'update_time': update_time}
                    province_result.update(city_total)
                    all_list.append(province_result)

    df = pd.DataFrame(all_list)
    df.to_csv('data.csv', index=False, encoding="utf_8_sig")

import csv
if __name__ == '__main__':
    #get_data()
    cityList = []
    with open(monitorCityList, 'r') as f:
        rawinfos = list(csv.reader(f))
        for i in rawinfos:
            cityList.append(i[0])
    print(cityList)
    for city in cityList:
        t,country=getWeather(city)
        print(t,country)
