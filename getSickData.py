# coding:utf-8
import time, json, requests
from datetime import datetime, date, timedelta
import pyecharts
#from pyecharts.charts import Map, Bar, Line, Page
from pyecharts import Map, Bar, Line, Page

'''
i get this code from:https://blog.csdn.net/isapi/article/details/104162932
requrire: pip install pyecharts==0.1.9.4
'''
import os
if os.path.exists('data') is not True:
    os.mkdir('data')

url = 'https://view.inews.qq.com/g2/getOnsInfo?name=disease_h5&callback=&_=%d' % int(
    time.time() * 1000)
data = json.loads(requests.get(url=url).json()['data'])
yesterday = date.today() + timedelta(days = -1)
lastUpdate = data['lastUpdateTime']
total = data['chinaTotal']
areaTree = data['areaTree']
DayList = data['chinaDayAddList']
#读取福建数据
fujian = dict()
for item in areaTree:
    if (item['name'] == '中国'):
        for item in item['children']:
            if (item['name'] == '福建'):
               fujian = item['children']
               break
        break

#读取各市数据
fjcity = []
confirm = []
todayConfirm = []
for item in fujian:
    fjcity.append(item['name'] + '市') #省级地图里各地级市名称必须以“市”字结尾，否则Map无法正确显示
    ctotal = item['total']
    confirm.append(int(ctotal['confirm']))
    ct = item['today']
    todayConfirm.append(int(ct['confirm']))
#读取全国新增数据
dates = []
dc = []
ds = []
#dd = []
dh = []
for item in DayList:
    dates.append(item['date'])
    dc.append(int(item['confirm']))
    ds.append(int(item['suspect']))
    #dd.append(int(item['dead']))
    dh.append(int(item['heal']))
#图表生成
map = Map('福建省2019-nCoV疫情(' + yesterday.strftime("%Y-%m-%d") + ')', '注：省卫健委每日11时发布前一天疫情通报\n更新时间：' + lastUpdate, width=1024, height=768)
map.add("确诊病例", fjcity, confirm, maptype='福建',visual_range=[0, max(confirm)], is_visualmap=True, visual_text_color='#000',is_label_show=True)

bar = Bar()
bar.add('确诊病例',fjcity,confirm,is_label_show=True)
bar.add('新增确诊病例',fjcity,todayConfirm,is_label_show=True)

l = len(dates)
line = Line('附：全国疫情','最近7天数据（来源：腾讯新闻疫情动态）')
line.add('新增确诊',dates[l-7:l],dc[l-7:l],is_label_show=True)
line.add('新增疑似',dates[l-7:l],ds[l-7:l],is_label_show=True)
#line.add('新增死亡',dates[l-7:l],dd[l-7:l],is_label_show=True)
line.add('新增治愈',dates[l-7:l],dh[l-7:l],is_label_show=True)
#页面生成
page = Page()#'福建省2019-nCoV疫情'
print('type(page)',type(page))
page.add(map)
page.add(bar)
page.add(line)
page.render(path=u'.\\data\\map2019.html') #保存为HTML文件，该文件可直接在浏览器中打开，也可发布到Web服务器上
