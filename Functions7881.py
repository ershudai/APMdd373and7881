from selenium import webdriver
from requests import *
from Functions import *
import re
import time
import json
headers = \
    {
'Sec-Fetch-Mode': 'no-cors',
'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36'}
hde= \
    {
'Sec-Fetch-Mode': 'no-cors',
'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36'}

#chromeOption启动函数
def chromedriver():
    driver_path=r'.\chromedriver.exe'
    chromeOptions = webdriver.ChromeOptions()
    chromeOptions.add_argument('disable-infobars')
    chromeOptions.add_experimental_option("excludeSwitches", ['enable-automation']);
    wd=webdriver.Chrome(executable_path=driver_path,options=chromeOptions)
    return wd
#检查cookies是否有效
def examine_ck(cook):
    thiss = get(url='https://tools.7881.com/helper/mallbill/1',cookies=cook)
    this1=thiss.url.split('?',1)

    if this1[0]=='https://passport.7881.com/login.html':
        return True
    return False
#获取当前排行价格及库存
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
        return '', ''

def get_cook(cook):
    i=1
    lit=[13,9,2,10,6,12,1]
    dic={}
    for ck in cook:
        for lt in lit:
            if lt==i:
                dic[ck] = cook[ck]
            continue
        i=i+1
    return dic

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
def get_api(url,cook,data):
    res=post(headers=hde,url=url,cookies=cook,data=data)
    res.cookies
    time.sleep(2)
    ress=res.content.decode()
    return json.loads(ress)
#筛选api中需要的参数
def get_api_price(json):
    lists=[]
    for jn in json:
        lt=[]
        lt.append(jn['price'])
        lt.append(jn['totalStock'])
        lt.append(jn['goodsTypeName']+'--'+jn['gameName']+'/'+jn['groupName']+'/'+jn['serverName'])
        lists.append(lt)
    return lists

#登录获取登录cookies
def get_login_cookies():
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
    #wd.quit()
    return ck,wd
#提交修改数据
def set_price(url,data,cook,price,Last):
    cookie=''
    hed=headers
    for k,v in cook.items():
        cookie=cookie+k+"="+v+"; "
    hed['cookie']=cookie
    hed['Content-Type']='application/json'
    res=post(url=url,data=json.dumps(data),headers=hed)
    rt=json.loads(res.text)
    if rt['data']['errCount']==0:
        print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+'----'+'修改成功'+'----'+Last+'---- 1元='+str(price)+"金")
    if rt['data']['errCount']!=0:
        print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+'----出错!数量：'+str(rt['data']['errCount'])+'---'+Last+'----'+rt['data']['errMsg'])

def getPrice1(restxt,ltPrice,i):
    dataPrice={}
    dataPrice["goodsId"] = str(restxt[i][0])
    dataPrice["stock"] = int(restxt[i][1])
    dataPrice["price"] = str(format(1 / ((1 / ltPrice[0][0]) + 0.01), '.5f'))
    return dataPrice

def getPrice2(restxt,ltPrice,i):
    dataPrice={}
    dataPrice["goodsId"] = str(restxt[i][0])
    dataPrice["stock"] = int(restxt[i][1])
    dataPrice["price"] = str(format(1 / ((1 / ltPrice[2][0]) + 0.01), '.5f'))
    return dataPrice