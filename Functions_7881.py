from selenium import webdriver
from requests import *
from functools import *
import re
import time
import json
headers = \
    {
'Host':'tools.7881.com',
'Referer':'https://tools.7881.com/publish/b/batch',
'Sec-Fetch-Mode': 'no-cors',
'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36'}
hde = \
    {
'Sec-Fetch-Mode': 'no-cors',
'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36'}
cook_dd373=''
#chromeOption启动函数
def chromedriver():
    driver_path=r'.\chromedriver.exe'
    chromeOptions = webdriver.ChromeOptions()
    chromeOptions.add_argument('disable-infobars')
    chromeOptions.add_experimental_option("excludeSwitches", ['enable-automation']);
    wd=webdriver.Chrome(executable_path=driver_path,options=chromeOptions)
    return wd
#get请求接口返回json
def get_api(url,cook):
    res=get(headers=hde,url=url,cookies=cook)
    ress=res.content.decode()
    return json.loads(ress)
#修改dd373
def set_price(url,data,cook,price,Last):
    cookie=''
    for k,v in cook.items():
        cookie=cookie+k+"="+v+"; "
    headers['cookie']=cookie
    res=post(url=url,data=data,headers=hde)
    rt = json.loads(res.text)
    if rt['StatusData']['ResultCode'] == '4001':
        cook_dd373=get_login_cookies_dd373()
        cookie = ''
        for k, v in cook_dd373.items():
            cookie = cookie + k + "=" + v + "; "
        headers['cookie'] = cookie
        res = post(url=url, data=data, headers=hde)
        rt = json.loads(res.text)
    if rt['StatusData']['ResultMsg']=='操作成功':
        print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+'------'+rt['StatusMsg']+'------'+rt['StatusData']['ResultMsg']+'---'+str(Last)+'---- 1元='+str(price)+"金")
    if rt['StatusData']['ResultMsg']=='全部失败！':
        print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+'------'+rt['StatusMsg']+'------'+rt['StatusData']['ResultMsg']+'---'+str(Last)+'---'+rt['StatusData']['ResultData']['ErrorMsges'][0]['MsgInfo'])
#修改7881
def set_price_7881(url,data,cook,price,Last):
    cookie=''
    hed=hde
    for k,v in cook.items():
        cookie=cookie+k+"="+v+"; "
    hed['cookie']=cookie
    hed['Content-Type']='application/json'
    res=post(url=url,data=json.dumps(data),headers=hed)
    rt=json.loads(res.text)
    if rt['data']['errCount']==0:
        print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+'---'+'修改成功'+'---'+Last+'--- 库存：'+price+"金")
    if rt['data']['errCount']!=0:
        print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+'---出错!数量：'+str(rt['data']['errCount'])+'---'+Last+'---'+rt['data']['errMsg'])


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
    return ck,wd

#获取7881价格
def get_price(url,cook):
    try:
        getprice=[]
        res=get(headers=headers,url=url,cookies=cook)
        restxt=res.content.decode()
        rtcook=res.cookies
        if res.url==url:
            text=re.findall('<table class="resulut_table">(.*?)<div class="table_foot clearfix">',restxt,re.S)
            text=str(text[0]).replace("\n","").replace("\r","").replace(" ","")
            getprice=re.findall(r'<trclass="tr"gameId="(.*?)"gtId="(.*?)"groupId="(.*?)"serverId="(.*?)"tradePlace="(.*?)"campName="(.*?)"><td>',text,re.S)
            restxt=re.findall(r'.*?<tdclass="goodsId">(.*?)</td><tdclass="goodsTradeType".*?"value="(.*?)"maxlength.*?"value="(.*?)"></td>',text,re.S)
            return restxt,getprice
        else:
            return '',''
    except:
        print("爬取数据出错了！")
        return '',''
#修改cookies数据格式
def get_ck(ck):
    cook={}
    for oneCK in ck:
        cook[oneCK['name']]=oneCK['value']
    return cook

#登录获取登录cookies
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

#登录获取登录cookies
def get_login_cookies_dd373():
    wd=chromedriver()
    wd.get('https://goods.dd373.com/usercenter/merchant/mall_management.html')
    user_input=wd.find_element_by_xpath("//div[@class='user-name border-ed']/input")
    pwd_input=wd.find_element_by_xpath("//div[@class='user-pwd border-ed']/input")
    user_input.send_keys("")
    pwd_input.send_keys("")
    print("等待登录")
    while wd.current_url!='https://goods.dd373.com/usercenter/merchant/mall_management.html':
        time.sleep(1)
    ck=wd.get_cookies()
    wd.quit()
    ck=get_ck(ck)
    return ck

#检查cookies是否有效
def examine_ck(cook):
    thiss = get(url='https://tools.7881.com/helper/mallbill/1',cookies=cook)
    if thiss.url.split('?',1)=='https://passport.7881.com/login.html':
        return False
    return True

def get_price_7881(url,cook):
    try:
        cookie = ''
        hed = headers
        #for k, v in cook.items():
            #cookie = cookie + k + "=" + v + "; "
        getprice=[]
        #hed['Cookie'] = cookie
        res=get(url=url,headers=hed,cookies=cook)
        restxt=res.content.decode()
        rtcook=res.cookies
        if res.url==url:
            text=re.findall('<table class="resulut_table">(.*?)<div class="table_foot clearfix">',restxt,re.S)
            text=str(text[0]).replace("\n","").replace("\r","").replace(" ","")
            getprice=re.findall(r'<trclass="tr"gameId="(.*?)"gtId="(.*?)"groupId="(.*?)"serverId="(.*?)"tradePlace="(.*?)"campName="(.*?)"><td>',text,re.S)
            restxt=re.findall(r'.*?<tdclass="goodsId">(.*?)</td><tdclass="goodsTradeType".*?"value="(.*?)"maxlength.*?"value="(.*?)"></td>',text,re.S)
            return restxt,getprice
        else:
            return '',''
    except:
        print('检查cookies，若无误请联系开发人员维护')
        return '', ''

#修改7881
def set_price_7881(url,data,cook,price,Last):
    cookie=''
    hed=hde
    for k,v in cook.items():
        cookie=cookie+k+"="+v+"; "
    hed['cookie']=cookie
    hed['Content-Type']='application/json'
    res=post(url=url,data=json.dumps(data),headers=hed)
    rt=json.loads(res.text)
    if rt['data']['errCount']==0:
        print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+'---'+'修改成功'+'---'+Last+'--- 库存：'+price+"金")
    if rt['data']['errCount']!=0:
        print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+'---出错!数量：'+str(rt['data']['errCount'])+'---'+Last+'---'+rt['data']['errMsg'])