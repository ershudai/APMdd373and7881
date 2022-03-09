import configparser

from selenium import webdriver
from requests import *
from Functions import *
import re
import time
import json
import os

header_dd373_save=\
    {
'content-type': 'application/json; charset=utf-8',
'date': 'Thu, 24 Feb 2022 08:21:58 GMT',
'ohc-cache-hit': r"mzun60 [1], bduncache82 [1], czix74 [1]",
'server': 'JSP3/2.0.14',
'set-cookie': "SERVERID=eec4d5b891f0590f40956ddc2c543c06|1645690917|1645690509;Path=/,",
'timing-allow-origin': "*"
}

headers = \
    {
'Sec-Fetch-Mode': 'no-cors',
'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36'}
headers2=\
{
"Accept-Encoding": "gzip, deflate, br",
"Accept-Language": "zh-CN,zh;q=0.9",
"Cache-Control": "max-age=0",
"Connection": "keep-alive",
"Host": "tools.7881.com",
"sec-ch-ua-mobile": "?0",
"Sec-Fetch-Dest": "document",
"Sec-Fetch-Mode": "navigate",
"Sec-Fetch-Site": "none",
"Sec-Fetch-User": "?1",
"Upgrade-Insecure-Requests": "1",
"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}
#chromeOption启动函数
def chromedriver():
    driver_path=r'.\chromedriver.exe'
    chromeOptions = webdriver.ChromeOptions()
    chromeOptions.add_argument('disable-infobars')
    chromeOptions.add_experimental_option("excludeSwitches", ['enable-automation']);
    wd=webdriver.Chrome(executable_path=driver_path,options=chromeOptions)
    return wd

def chromedriver_hide():
    driver_path=r'.\chromedriver.exe'
    chromeOptions = webdriver.ChromeOptions()
    chromeOptions.add_argument('--no-sandbox')
    chromeOptions.add_argument('--disable-dev-shm-usage')
    wd=webdriver.Chrome(executable_path=driver_path,options=chromeOptions)
    wd.get('https://www.dd373.com/s-eja7u2-c-jk5sj0-0r2mut-0acvkr-67492s.html')
    ck=wd.get_cookies()
    print(ck)
    print(wd)
    return wd
#获取7881价格

#获取当前排行价格及库存
def get_price(url,cook,header):
    res=get(headers=header,url=url,cookies=cook)
    restxt=res.content.decode()
    rtcook=res.cookies
    text=re.findall('<div id="slides"(.*?)<div class="all-look">',restxt,re.S)
    try:
        text=str(text[0]).replace("\n","").replace("\r","").replace(" ","")
        text=re.findall('<pclass="font12colorFF5">(.*?)</p><pclass="font12color666m-t5">(.*?)</p></div></li><liclass="width364p-l40">.*?</span><spanclass="font12colorFF5f-left">(.*?)</span><spanclass="font12color666f-left">',text,re.S)
    except:
        return []
    retxt=[]
    for rt in range(len(text)):
        lt=[]
        xx=float(str(text[rt][0]).split("=")[1].replace("金",""))
        lt.append(xx)
        lt.append(int(text[rt][2]))
        retxt.append(lt)
    return retxt

def get_price_put(url,cook,header):
    res=get(headers=header,url=url,cookies=cook)
    restxt=res.content.decode()
    rtcook=res.cookies
    text=re.findall('<div class="swiper-container">(.*?)<div class="bussiness-num p-lr16">',restxt,re.S)
    text=str(text[0]).replace("\n","").replace("\r","").replace(" ","")
    text=re.findall('<pclass="line-height14font12colorFF5t-m4center"style="text-align:left">(.*?)</p><pclass="font12color666line-height14t-m4"style="text-align:left">(.*?)</p></div><divclass="receive-number">.*?</span><spanclass="font12colorFF5">(.*?)</span><spanclass="font12color666">金</span></p></div>',text,re.S)

    come_text=re.findall('<div id="slides"(.*?)<div class="all-look">',restxt,re.S)
    try:
        come_text=str(come_text[0]).replace("\n","").replace("\r","").replace(" ","")
        come_text=re.findall('<pclass="font12colorFF5">(.*?)</p><pclass="font12color666m-t5">(.*?)</p></div></li><liclass="width364p-l40">.*?</span><spanclass="font12colorFF5f-left">(.*?)</span><spanclass="font12color666f-left">',come_text,re.S)
    except:
        come_text=[]

    p_txt=[]
    c_text=[]
    for rt in range(len(text)):
        lt=[]
        xx=float(str(text[rt][0]).split("=")[1].replace("金",""))
        lt.append(xx)
        lt.append(int(text[rt][2]))
        p_txt.append(lt)

    for rt in range(len(come_text)):
        lt=[]
        xx=float(str(come_text[rt][0]).split("=")[1].replace("金",""))
        lt.append(xx)
        lt.append(int(come_text[rt][2]))
        c_text.append(lt)
    return p_txt,c_text

#将cookies转为字典类型
def get_ck(ck):
    cook={}
    for oneCK in ck:
        cook[oneCK['name']]=oneCK['value']
    return cook

#将字典类型ck中需要的list对应字段取出
def get_cookies(list,ck):
    cookies={}
    for lt in list:
        if lt in ck:
            cookies[lt]=ck[lt]
    return cookies

#获取api中json数据
def get_api(url,cook):
    res=get(headers=headers,url=url,cookies=cook)
    ress=res.content.decode()
    return json.loads(ress)

#登录获取登录cookies
def get_login_cookies():
    wd=chromedriver()
    wd.get('https://goods.dd373.com/usercenter/merchant/mall_management.html')
    user_input=wd.find_element_by_xpath("//div[@class='user-name border-ed']/input")
    pwd_input=wd.find_element_by_xpath("//div[@class='user-pwd border-ed']/input")
    user_input.send_keys("")
    pwd_input.send_keys("")
    print("等待登录")
    time.sleep(6)
    while wd.current_url!='https://goods.dd373.com/usercenter/merchant/mall_management.html':
        time.sleep(1)
    ck=wd.get_cookies()
    ck=get_ck(ck)
    print("登录成功")
    time.sleep(1.5)
    return ck,wd

def get_wd_cookies(wd):
    ck=wd.get_cookies()
    ck=get_ck(ck)
    print("登录成功")
    time.sleep(1.5)
    return ck

def refresh_ck(wd):
    wd.get('https://goods.dd373.com/usercenter/merchant/mall_management.html')
    if wd.current_url!='https://goods.dd373.com/usercenter/merchant/mall_management.html':
        user_input = wd.find_element_by_xpath("//div[@class='user-name border-ed']/input")
        pwd_input = wd.find_element_by_xpath("//div[@class='user-pwd border-ed']/input")
        user_input.send_keys("")
        pwd_input.send_keys("")
    while wd.current_url!='https://goods.dd373.com/usercenter/merchant/mall_management.html':
        time.sleep(1)
    ck = wd.get_cookies()
    ck=get_ck(ck)
    return ck


#提交修改数据
def set_price(url,data,cook,price,Last):
    cookie=''
    for k,v in cook.items():
        cookie=cookie+k+"="+v+"; "
    header_dd373_save['cookie']=cookie
    data=json.dumps(data)
    res=post(url=url,data=data,headers=header_dd373_save)
    rt=json.loads(res.text)
    if rt['StatusData']['ResultMsg']=='操作成功':
        print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+'------'+rt['StatusMsg']+'------'+rt['StatusData']['ResultMsg']+'---'+Last+'---- 1元='+str(price)+"金")
        return True
    if rt['StatusData']['ResultMsg']=='全部失败！':
        print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+'------'+rt['StatusMsg']+'------'+rt['StatusData']['ResultMsg']+'---'+Last+'---'+rt['StatusData']['ResultData']['ErrorMsges'][0]['MsgInfo'])
        return False
    return False
def set_price_in(url,data,cook,price,Last):
    cookie=''
    for k,v in cook.items():
        cookie=cookie+k+"="+v+"; "
    headers['cookie']=cookie
    res=post(url=url,data=data,headers=headers)
    rt=json.loads(res.text)
    if rt['StatusData']['ResultMsg']=='操作成功':
        print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+'------'+rt['StatusMsg']+'------'+rt['StatusData']['ResultMsg']+'---' +str(price)+str(Last)+"金")
        return True
    if rt['StatusData']['ResultMsg']=='全部失败！':
        print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+'------'+rt['StatusMsg']+'------'+rt['StatusData']['ResultMsg']+'---'+rt['StatusData']['ResultData']['ErrorMsges'][0]['MsgInfo'])
        return False
    return False


def get_login_cookies_7881():
    wd=chromedriver()
    wd.get('https://passport.7881.com/login.html')
    user_input=wd.find_element_by_xpath("//input[@class='iptAct']")
    pwd_input=wd.find_element_by_xpath("//input[@class='iptPwd eyeclose']")
    user_input.send_keys("")
    pwd_input.send_keys("")
    print("等待登录！")
    while wd.current_url=='https://passport.7881.com/login.html':
        time.sleep(1)
    print(wd.current_url)
    ck=wd.get_cookies()
    print('登录成功！')
    wd.quit()
    return ck

