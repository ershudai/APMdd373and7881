from selenium import webdriver
from requests import *
from Functions7881 import *
import re
import time
import html
import urllib.parse
import threading
import os
import configparser

curpath = os.path.dirname(os.path.realpath(__file__))
cfgpath = os.path.join(curpath, "ck.ini")
# 创建管理对象
conf = configparser.RawConfigParser()
# 读ini文件
conf.read(".\ck.ini", encoding="utf-8")
cookies = conf.items('cookies')
ck_7881=str(cookies[1][1])
if ck_7881=="":
    ck_7881 = get_ck(get_login_cookies())
    conf.set("cookies", "7881", str(ck_7881))
    conf.write(open(".\ck.ini", "w", encoding="utf-8"))
else:
    ck_7881=eval(ck_7881)

#每次全部修改的间隔时间
while_time=60
#不要改，这是用来关闭程序的
while_pd=1

def cmd():
    global while_pd
    while while_pd:
        txt=input()
        if txt=='quit':
            while_pd=0
            print('关闭出货,关闭程序')
#开启关闭线程
come_thread_put=threading.Thread(target=cmd)
come_thread_put.start()
web=""
while while_pd:
    if examine_ck(ck_7881) == True:
        print("7881---" + "登录ck参数失效")
        ck,web=get_login_cookies()
        ck_7881 = get_ck(ck)
        conf.set("cookies", "7881", str(ck_7881))
        conf.write(open(cfgpath, "w", encoding="utf-8"))

    restxt,prices=get_price('https://tools.7881.com/helper/mallbill/1',ck_7881)
    if restxt=='' and prices=='':
        print("没有爬取到数据")
        time.sleep(while_time)
        continue
    for i in range(0,len(restxt)):
        gametype=str(html.unescape(prices[i][5]))
        data='gameId='+prices[i][0]+'&gtId='+prices[i][1]+'&serverId='+prices[i][3]+'&groupId='+prices[i][2]+'&tradePlace='+prices[i][4]+'&campName='+urllib.parse.quote(gametype)
        getprice=get_api(r'https://tools.7881.com/helper/mallbill/queryShopGoodsBySort',ck_7881,data)
        ltPrice=get_api_price(getprice)
        if int(restxt[i][1])!=int(ltPrice[0][1]):
            dataPrice=getPrice1(restxt,ltPrice,i)
            set_price('https://tools.7881.com/helper/listbill/goods/1/price/edit',[dataPrice],ck_7881,str(int(1.0/float(format(1/((1/ltPrice[0][0])+0.01),'.5f')))),ltPrice[0][2])
        if int(restxt[i][1])==int(ltPrice[0][1]):
            dataPrice=getPrice1(restxt,ltPrice,i)
            print(ltPrice[0][2]+'----'+"当前已经是第一了")
            set_price('https://tools.7881.com/helper/listbill/goods/1/price/edit',[dataPrice],ck_7881,str(int(1.0/float(format(1/((1/ltPrice[2][0])+0.01),'.5f')))),ltPrice[0][2])
    time.sleep(while_time)

