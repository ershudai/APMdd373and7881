from selenium import webdriver
from requests import *
from Functions import *
import re
import threading
import time
import os
import configparser
from Functions_7881 import get_price_7881,set_price_7881


# #出货商品列表
# LastID=[[r'6269ef177fa744a4a2e848804723c6e0',r'https://www.dd373.com/s-eja7u2-c-jk5sj0-0r2mut-bd0hgj-ra3w34.html',r'一区祈福出',r'201612459394375',r'yi'],
#         [r'c2df1dbe8caf464a9a493682344e0852',r'https://www.dd373.com/s-eja7u2-c-jk5sj0-3fk9tg-5acd49-hhtv1m.html',r'一区审判出'],
#         [r'1012cc2bacdc4cf3a4eaafec05e15430',r'https://www.dd373.com/s-eja7u2-c-jk5sj0-3fk9tg-0djqu5-mcr8g9.html',r'五区厄运出'],
#         [r'a7fe8636020440eea976976f70ff9872',r'https://www.dd373.com/s-eja7u2-c-jk5sj0-3fk9tg-nurtuv-507ggw.html',r'五区雷德出'],
#         [r'67efe36548984fb0a4e7f5158e77347e',r'https://www.dd373.com/s-eja7u2-c-jk5sj0-3fk9tg-a2ehmt-pe8vtt.html',r'五区寒冰出'],
#         [r'bd701e52d3174ec990d1a2ab91b8734f',r'https://www.dd373.com/s-eja7u2-c-jk5sj0-3fk9tg-vmkjx3-u66e8b.html',r'五区曼多出'],
#         [r'f3d004a9630e4c98a1995655af4f417e',r'https://www.dd373.com/s-eja7u2-c-jk5sj0-3fk9tg-5n5au3-rrwu40.html',r'五区木喉出'],
#         [r'93108b60d7d54f498d481ddddff4a6ee',r'https://www.dd373.com/s-eja7u2-c-jk5sj0-3fk9tg-2udask-s5kpdw.html',r'五区雷霆出'],
#         [r'9c915dfb6ba24662b7a762cf695587ba',r'https://www.dd373.com/s-eja7u2-c-jk5sj0-3fk9tg-tqb8p3-3dx0xx.html',r'五区狮心出'],
#         [r'3a07ecc92f674752bb8a3f88e6878cc5',r'https://www.dd373.com/s-eja7u2-c-jk5sj0-3fk9tg-swu6xh-c0qukc.html',r'五区法尔出'],
#         [r'e30606803ace4edd8d8e966d55b80ae2',r'https://www.dd373.com/s-eja7u2-c-jk5sj0-3fk9tg-hn3p7w-4wnaq2.html',r'五区安娜出'],
#         [r'0f0b6012aa434603939ded7d55c1b7c2',r'https://www.dd373.com/s-eja7u2-c-jk5sj0-3fk9tg-ptugvs-cv6hv0.html',r'五区匕首出'],
#         [r'203add8455124e95a5c7df674202cff4',r'https://www.dd373.com/s-eja7u2-c-jk5sj0-3fk9tg-dt5vqj-59ckg6.html',r'五区娅尔出'],
#         [r'723c3762667b487d99a216bc9c40b6a7',r'https://www.dd373.com/s-eja7u2-c-jk5sj0-3fk9tg-d4jp31-1us7gu.html',r'五区秩序出'],
#         [r'942dfb856aa84a7c88b9401ed75b49ed',r'https://www.dd373.com/s-eja7u2-c-jk5sj0-3fk9tg-psgfsv-mc61bj.html',r'五区比格出'],
#         [r'8a5ab0cb4dce4251a18d3d4afad41305',r'https://www.dd373.com/s-eja7u2-c-jk5sj0-3fk9tg-tc8umm-67445b.html',r'五区范沃出'],
#         [r'3e17ee47c67245208fa237d31f7d53d4',r'https://www.dd373.com/s-eja7u2-c-jk5sj0-3fk9tg-dm98t9-8qcm9u.html',r'五区湖畔出'],
#         [r'0d3a6912131a40a1a9cdca1f6425234f',r'https://www.dd373.com/s-eja7u2-c-jk5sj0-3fk9tg-pe5bdm-1x48hs.html',r'五区范克出'],
#         [r'68c72878ec914dec80593848a05c5825',r'https://www.dd373.com/s-eja7u2-c-jk5sj0-0r2mut-xht6js-gdx49h.html',r'一区哈霍出'],
#         [r'd5e28ba8a5564d78bb89c9113b721aef',r'https://www.dd373.com/s-eja7u2-c-jk5sj0-0r2mut-0acvkr-67492s.html',r'一区碧玉出'],
#         [r'3d70b58c49214755a3b31e3d14402511',r'https://www.dd373.com/s-eja7u2-c-jk5sj0-0r2mut-xht6js-gdx49h.html',r'一区寒脊出'],
#         [r'fe8eed1be41d4b7b977a74f150940e26',r'https://www.dd373.com/s-eja7u2-c-jk5sj0-0r2mut-ucqwt4-ucb5n3.html',r'一区灰烬出']]
#
# #收获商品列表
# put_LastID=[[r'6269ef177fa744a4a2e848804723c6e0',r'https://www.dd373.com/s-eja7u2-c-jk5sj0-0r2mut-bd0hgj-ra3w34.html',r'一区祈福收'],
#             [r'c2df1dbe8caf464a9a493682344e0852',r'https://www.dd373.com/s-eja7u2-c-jk5sj0-3fk9tg-5acd49-hhtv1m.html',r'一区审判收'],
#             [r'1012cc2bacdc4cf3a4eaafec05e15430',r'https://www.dd373.com/s-eja7u2-c-jk5sj0-3fk9tg-0djqu5-mcr8g9.html',r'五区厄运收'],
#             [r'a7fe8636020440eea976976f70ff9872',r'https://www.dd373.com/s-eja7u2-c-jk5sj0-3fk9tg-nurtuv-507ggw.html',r'五区雷德收'],
#             [r'67efe36548984fb0a4e7f5158e77347e',r'https://www.dd373.com/s-eja7u2-c-jk5sj0-3fk9tg-a2ehmt-pe8vtt.html',r'五区寒冰收'],
#             [r'bd701e52d3174ec990d1a2ab91b8734f',r'https://www.dd373.com/s-eja7u2-c-jk5sj0-3fk9tg-vmkjx3-u66e8b.html',r'五区曼多收'],
#             [r'f3d004a9630e4c98a1995655af4f417e',r'https://www.dd373.com/s-eja7u2-c-jk5sj0-3fk9tg-5n5au3-rrwu40.html',r'五区木喉收'],
#             [r'93108b60d7d54f498d481ddddff4a6ee',r'https://www.dd373.com/s-eja7u2-c-jk5sj0-3fk9tg-2udask-s5kpdw.html',r'五区雷霆收'],
#             [r'9c915dfb6ba24662b7a762cf695587ba',r'https://www.dd373.com/s-eja7u2-c-jk5sj0-3fk9tg-tqb8p3-3dx0xx.html',r'五区狮心收'],
#             [r'3a07ecc92f674752bb8a3f88e6878cc5',r'https://www.dd373.com/s-eja7u2-c-jk5sj0-3fk9tg-swu6xh-c0qukc.html',r'五区法尔收'],
#             [r'e30606803ace4edd8d8e966d55b80ae2',r'https://www.dd373.com/s-eja7u2-c-jk5sj0-3fk9tg-hn3p7w-4wnaq2.html',r'五区安娜收'],
#             [r'0f0b6012aa434603939ded7d55c1b7c2',r'https://www.dd373.com/s-eja7u2-c-jk5sj0-3fk9tg-ptugvs-cv6hv0.html',r'五区匕首收'],
#             [r'203add8455124e95a5c7df674202cff4',r'https://www.dd373.com/s-eja7u2-c-jk5sj0-3fk9tg-dt5vqj-59ckg6.html',r'五区娅尔收'],
#             [r'723c3762667b487d99a216bc9c40b6a7',r'https://www.dd373.com/s-eja7u2-c-jk5sj0-3fk9tg-d4jp31-1us7gu.html',r'五区秩序收'],
#             [r'942dfb856aa84a7c88b9401ed75b49ed',r'https://www.dd373.com/s-eja7u2-c-jk5sj0-3fk9tg-psgfsv-mc61bj.html',r'五区比格收'],
#             [r'8a5ab0cb4dce4251a18d3d4afad41305',r'https://www.dd373.com/s-eja7u2-c-jk5sj0-3fk9tg-tc8umm-67445b.html',r'五区范沃收'],
#             [r'3e17ee47c67245208fa237d31f7d53d4',r'https://www.dd373.com/s-eja7u2-c-jk5sj0-3fk9tg-dm98t9-8qcm9u.html',r'五区湖畔收'],
#             [r'0d3a6912131a40a1a9cdca1f6425234f',r'https://www.dd373.com/s-eja7u2-c-jk5sj0-3fk9tg-pe5bdm-1x48hs.html',r'五区范克收'],
#             [r'68c72878ec914dec80593848a05c5825',r'https://www.dd373.com/s-eja7u2-c-jk5sj0-0r2mut-xht6js-gdx49h.html',r'一区哈霍收'],
#             [r'd5e28ba8a5564d78bb89c9113b721aef',r'https://www.dd373.com/s-eja7u2-c-jk5sj0-0r2mut-0acvkr-67492s.html',r'一区碧玉收'],
#             [r'3d70b58c49214755a3b31e3d14402511',r'https://www.dd373.com/s-eja7u2-c-jk5sj0-0r2mut-xht6js-gdx49h.html',r'一区寒脊收'],
#             [r'fe8eed1be41d4b7b977a74f150940e26',r'https://www.dd373.com/s-eja7u2-c-jk5sj0-0r2mut-ucqwt4-ucb5n3.html',r'一区灰烬收']]
global ck_dd373
ck_dd373={}
#登录获取ck
# curpath = os.path.dirname(os.path.realpath(__file__))
# cfgpath = os.path.join(curpath, "ck.ini")
# 创建管理对象
conf = configparser.RawConfigParser()
#线程登录控制
global login
global login_save
login_save=False
login=False
# 读ini文件
conf.read(".\ck.ini", encoding="utf-8")
sections = conf.sections()
#7881取出ck

last = conf.items('Last')
LastID=str(last[0][1])
put_LastID=str(last[1][1])
LastID=eval(LastID)
put_LastID=eval(put_LastID)

cookies = conf.items('cookies')
ck_7881=str(cookies[1][1])
ck_7881=eval(ck_7881)
ck_dd373=str(cookies[0][1])
ck_dd373=eval(ck_dd373)
global web

ck_dd373,web=get_login_cookies()

conf.set("cookies", "DD373", str(ck_dd373))
conf.write(open(".\ck.ini", "w", encoding="utf-8"))
print("cookies储存成功！")
while_control=1
while_time=300
while_time_put=300
#控制收货 金币最少=热卖的第一+put_price_spread
put_price_spread=1.8

print('间隔时间:'+str(while_time)+'秒')

# class login_dd373(threading.Thread):
#     def __init__(self,ck,pd):
#         super(login_dd373, self).__init__()
#         self.ifpd=pd
#         self.ck=ck
#         self.myprice=''
#         self.lock=threading.RLock()
#     def run(self):
#         global login_save
#         global ck_dd373
#         self.lock.acquire()
#         if login_save == True:
#             cookies = conf.items('cookies')
#             ck_dd373 = str(cookies[0][1])
#             ck_dd373 = eval(ck_dd373)
#             self.ck=ck_dd373
#             login_save = False
#         if self.ifpd==1:
#             myprice=get_api('https://goods.dd373.com/Api/MallGoods/UserCenter/List?MerchantType=1&LastId=&GoodsType=&Status=-1&PageIndex=1&PageSize=20',self.ck)
#         if self.ifpd == 2:
#             self.myprice=get_api('https://goods.dd373.com/Api/Receive/UserCenter/List?LastId=&GoodsType=&Status=-1&PageIndex=1&PageSize=40',self.ck)
#
#         if self.myprice['StatusData']['ResultCode'] == '4001':
#             print("dd373---" + self.myprice['StatusData']['ResultMsg'])
#             self.ck = get_ck(get_login_cookies())
#             ck_dd373=self.ck
#             conf.set("cookies", "DD373", str(self.ck))
#             conf.write(open(cfgpath, "w", encoding="utf-8"))
#             with open("ck.txt", "w") as f:
#                 f.write(str(self.ck))
#                 login_save= True
#         self.lock.release()
#     def get(self):
#             return self.ck,self.myprice


def getck(ifpd,ck):
    global login
    global web
    if ifpd==1:
        myprice = get_api('https://goods.dd373.com/Api/MallGoods/UserCenter/List?MerchantType=1&LastId=&GoodsType=&Status=-1&PageIndex=1&PageSize=20',ck)
    if ifpd == 2:
        myprice = get_api('https://goods.dd373.com/Api/Receive/UserCenter/List?LastId=&GoodsType=&Status=-1&PageIndex=1&PageSize=40',ck)
    if myprice['StatusData']['ResultCode'] == '4001':
        cook=refresh_ck(web)
        conf.set("cookies", "dd373", str(cook))
        conf.write(open(".\ck.ini", "w", encoding="utf-8"))
        if ifpd == 1:
            myprice = get_api('https://goods.dd373.com/Api/MallGoods/UserCenter/List?MerchantType=1&LastId=&GoodsType=&Status=-1&PageIndex=1&PageSize=20',ck)
        if ifpd == 2:
            myprice = get_api('https://goods.dd373.com/Api/Receive/UserCenter/List?LastId=&GoodsType=&Status=-1&PageIndex=1&PageSize=40',ck)
        return myprice,cook
    return myprice,ck

def come_price(while_time,cook):
    global ck_dd373
    global login
    print("开启出货")
    while while_control:
        #获取本人的商品信息
        myprice,ck_dd373=getck(1,ck_dd373)
        try:
            Goods=myprice['StatusData']['ResultData']['PageResult']
        except:
            ck_dd373=get_wd_cookies(web)
            myprice,ck_dd373=getck(1,ck_dd373)
            try:
                Goods=myprice['StatusData']['ResultData']['PageResult']
            except:
                print("读取不到有效登录信息！")
                break
        for gd in Goods:
            for LI in LastID: #判断大区是否与要改的相等
                if gd['LastId']==LI[0]: #判断当大区与所设的大区相同时进行修改操作
                    post_data={}
                    post_json={}
                    list=[]
                    res=get_price(LI[1],ck_dd373,headers)
                    if len(res)>0:  #确保爬取到了热卖信息
                        if int(gd['Inventory'])!=res[0][1]:
                            post_data['Inventory']=int(gd['Inventory'])
                            post_data['IsTrusteeship']=gd['IsTrusteeship']
                            post_data['ShopNumber']=gd['ShopNumber']
                            post_data['UnitPrice']=res[0][0]+0.01
                            post_json['Goods']=[post_data]
                            # post_data=post_data+r'Goods%5B0%5D%5BShopNumber%5D'+'='+gd['ShopNumber']+r'&'
                            # post_data=post_data+r'Goods%5B0%5D%5BInventory%5D'+'='+str(int(gd['Inventory']))+r'&'
                            # post_data=post_data+r'Goods%5B0%5D%5BUnitPrice%5D'+'='+str(res[0][0]+0.01)+r'&'
                            # post_data=post_data+r'Goods%5B0%5D%5BIsTrusteeship%5D'+'='+str(gd['IsTrusteeship'])+r'&'
                            set_price(r"https://goods.dd373.com/Api/MallGoods/UserCenter/Save",post_json,ck_dd373,(res[0][0]+0.02),LI[2])
                        if int(gd['Inventory'])==res[0][1]:
                            post_data['Inventory'] = int(gd['Inventory'])
                            post_data['IsTrusteeship'] = gd['IsTrusteeship']
                            post_data['ShopNumber'] = gd['ShopNumber']
                            post_data['UnitPrice'] = res[1][0]+0.02
                            post_json['Goods'] = [post_data]
                            print(LI[2]+'----'+'当前已经是第一了')
                            # post_data=post_data+r'Goods%5B0%5D%5BShopNumber%5D'+'='+gd['ShopNumber']+r'&'
                            # post_data=post_data+r'Goods%5B0%5D%5BInventory%5D'+'='+str(int(gd['Inventory']))+r'&'
                            # post_data=post_data+r'Goods%5B0%5D%5BUnitPrice%5D'+'='+str(res[1][0]+0.02)+r'&'
                            # post_data=post_data+r'Goods%5B0%5D%5BIsTrusteeship%5D'+'='+str(gd['IsTrusteeship'])+r'&'
                            set_price(r"https://goods.dd373.com/Api/MallGoods/UserCenter/Save",post_json,ck_dd373,(res[1][0]+0.02),LI[2])
                    time.sleep(2)
        time.sleep(while_time)

def put_price(while_time,cook):
    global ck_dd373
    global login
    global web
    print("开启收货")
    while while_control:
        #获取本人的商品信息
        myprice,ck_dd373=getck(2,ck_dd373)
        try:
            Goods=myprice['StatusData']['ResultData']['PageResult']
        except:
            ck_dd373=get_wd_cookies(web)
            myprice, ck_dd373 = getck(2, ck_dd373)
            try:
                Goods = myprice['StatusData']['ResultData']['PageResult']
            except:
                print("读取不到有效登录信息！")
                break


        for gd in Goods:
            for LI in put_LastID: #判断大区是否与要改的相等
                if gd['LastId']==LI[0]: #判断当大区与所设的大区相同时进行修改操作
                    post_data=''
                    res,res_come=get_price_put(LI[1],ck_dd373,headers)#获取收获现价
                    if len(res)>0:  #确保爬取到了热卖信息
                        post_data = {}
                        post_json = {}
                        list = []
                        if len(res_come)>=1:
                            come_pr=res_come[0][0]+float(put_price_spread)
                            put_pr=res[0][0]
                            if come_pr >= put_pr:

                                post_data['MaxQuantity'] = gd['MaxQuantity']
                                post_data['MinQuantity'] = gd['MinQuantity']
                                post_data['ShopNumber'] = gd['ShopNo']
                                post_data['TotalQuantity'] = int(gd['TotalQuantity'])
                                post_data['UnitPrice'] = res_come[0][0]+put_price_spread
                                post_json['Goods'] = [post_data]
                                print(LI[2] + '----' + '收获价格太高——暂时定价:出货最低价+'+str(put_price_spread)+'金')
                                # post_data=post_data+r'Goods%5B0%5D%5BShopNumber%5D'+'='+gd['ShopNo']+r'&'
                                # post_data=post_data+r'Goods%5B0%5D%5BTotalQuantity%5D'+'='+str(int(gd['TotalQuantity']))+r'&'
                                # post_data=post_data+r'Goods%5B0%5D%5BUnitPrice%5D'+'='+str(res_come[0][0]+put_price_spread)+r'&'
                                # post_data=post_data+r'Goods%5B0%5D%5BMinQuantity%5D'+'='+str(gd['MinQuantity'])+r'&'
                                # post_data=post_data+r'Goods%5B0%5D%5BMaxQuantity%5D'+'='+str(gd['MaxQuantity'])+r'&'
                                set_price(r"https://goods.dd373.com/Api/Receive/UserCenter/Save",post_data,ck_dd373,(res_come[0][0]+put_price_spread),LI[2])
                            else :
                                if int(gd['TotalQuantity']) != res[0][1]:
                                    post_data['MaxQuantity'] = gd['MaxQuantity']
                                    post_data['MinQuantity'] = gd['MinQuantity']
                                    post_data['ShopNumber'] = gd['ShopNo']
                                    post_data['TotalQuantity'] = int(gd['TotalQuantity'])
                                    post_data['UnitPrice'] =  res[0][0] - 0.0100
                                    post_json['Goods'] = [post_data]
                                    # post_data = post_data + r'Goods%5B0%5D%5BShopNumber%5D' + '=' + gd['ShopNo'] + r'&'
                                    # post_data = post_data + r'Goods%5B0%5D%5BTotalQuantity%5D' + '=' + str(
                                    #     int(gd['TotalQuantity'])) + r'&'
                                    # post_data = post_data + r'Goods%5B0%5D%5BUnitPrice%5D' + '=' + str(
                                    #     res[0][0] - 0.0100) + r'&'
                                    # post_data = post_data + r'Goods%5B0%5D%5BMinQuantity%5D' + '=' + str(
                                    #     gd['MinQuantity']) + r'&'
                                    # post_data = post_data + r'Goods%5B0%5D%5BMaxQuantity%5D' + '=' + str(
                                    #     gd['MaxQuantity']) + r'&'

                                    set_price(r"https://goods.dd373.com/Api/Receive/UserCenter/Save", post_json, ck_dd373,
                                              (res[0][0] - 0.01), LI[2])
                                if int(gd['TotalQuantity']) == res[0][1]:
                                    post_data['MaxQuantity'] = gd['MaxQuantity']
                                    post_data['MinQuantity'] = gd['MinQuantity']
                                    post_data['ShopNumber'] = gd['ShopNo']
                                    post_data['TotalQuantity'] = int(gd['TotalQuantity'])
                                    post_data['UnitPrice'] =  res[1][0] - 0.0100
                                    post_json['Goods'] = [post_data]
                                    print(LI[2] + '----' + '当前已经是第一了')

                                    # post_data = post_data + r'Goods%5B0%5D%5BShopNumber%5D' + '=' + gd['ShopNo'] + r'&'
                                    # post_data = post_data + r'Goods%5B0%5D%5BTotalQuantity%5D' + '=' + str(
                                    #     int(gd['TotalQuantity'])) + r'&'
                                    # post_data = post_data + r'Goods%5B0%5D%5BUnitPrice%5D' + '=' + str(
                                    #     res[1][0] - 0.0100) + r'&'
                                    # post_data = post_data + r'Goods%5B0%5D%5BMinQuantity%5D' + '=' + str(
                                    #     int(gd['MinQuantity'])) + r'&'
                                    # post_data = post_data + r'Goods%5B0%5D%5BMaxQuantity%5D' + '=' + str(
                                    #     int(gd['MaxQuantity'])) + r'&'
                                    set_price(r"https://goods.dd373.com/Api/Receive/UserCenter/Save", post_json, ck_dd373,
                                              (res[1][0] - 0.01), LI[2])
                        else:
                            if int(gd['TotalQuantity']) != res[0][1]:
                                post_data['MaxQuantity'] = gd['MaxQuantity']
                                post_data['MinQuantity'] = gd['MinQuantity']
                                post_data['ShopNumber'] = gd['ShopNo']
                                post_data['TotalQuantity'] = int(gd['TotalQuantity'])
                                post_data['UnitPrice'] = res[0][0] - 0.0100
                                post_json['Goods'] = [post_data]

                                # post_data = post_data + r'Goods%5B0%5D%5BShopNumber%5D' + '=' + gd['ShopNo'] + r'&'
                                # post_data = post_data + r'Goods%5B0%5D%5BTotalQuantity%5D' + '=' + str(
                                #     int(gd['TotalQuantity'])) + r'&'
                                # post_data = post_data + r'Goods%5B0%5D%5BUnitPrice%5D' + '=' + str(
                                #     res[0][0] - 0.0100) + r'&'
                                # post_data = post_data + r'Goods%5B0%5D%5BMinQuantity%5D' + '=' + str(
                                #     gd['MinQuantity']) + r'&'
                                # post_data = post_data + r'Goods%5B0%5D%5BMaxQuantity%5D' + '=' + str(
                                #     gd['MaxQuantity']) + r'&'
                                set_price(r"https://goods.dd373.com/Api/Receive/UserCenter/Save", post_json, ck_dd373,
                                          (res[0][0] - 0.01), LI[2])
                            if int(gd['TotalQuantity']) == res[0][1]:
                                post_data['MaxQuantity'] = gd['MaxQuantity']
                                post_data['MinQuantity'] = gd['MinQuantity']
                                post_data['ShopNumber'] = gd['ShopNo']
                                post_data['TotalQuantity'] = int(gd['TotalQuantity'])
                                post_data['UnitPrice'] = res[1][0] - 0.0100
                                post_json['Goods'] = [post_data]

                                print(LI[2] + '----' + '当前已经是第一了')
                                # post_data = post_data + r'Goods%5B0%5D%5BShopNumber%5D' + '=' + gd['ShopNo'] + r'&'
                                # post_data = post_data + r'Goods%5B0%5D%5BTotalQuantity%5D' + '=' + str(
                                #     int(gd['TotalQuantity'])) + r'&'
                                # post_data = post_data + r'Goods%5B0%5D%5BUnitPrice%5D' + '=' + str(
                                #     res[1][0] - 0.0100) + r'&'
                                # post_data = post_data + r'Goods%5B0%5D%5BMinQuantity%5D' + '=' + str(
                                #     int(gd['MinQuantity'])) + r'&'
                                # post_data = post_data + r'Goods%5B0%5D%5BMaxQuantity%5D' + '=' + str(
                                #     int(gd['MaxQuantity'])) + r'&'
                                set_price(r"https://goods.dd373.com/Api/Receive/UserCenter/Save", post_json, ck_dd373,
                                          (res[1][0] - 0.01), LI[2])
                        time.sleep(10)

        time.sleep(while_time_put)


def set_inventory(list):
    global ck_dd373
    global ck_7881
    print("开始查询需要修改的数据。")
    myprice = get_api('https://goods.dd373.com/Api/MallGoods/UserCenter/List?MerchantType=1&LastId=&GoodsType=&Status=-1&PageIndex=1&PageSize=40',ck_dd373)
    while(myprice['StatusData']['ResultCode'] == '4001'):
        print("dd373登录参数失效！")
        myprice,ck_dd373=getck(2,ck_dd373)
        time.sleep(3)
        print("dd373登录成功！")
    # try:
    #     restxt, prices = get_price_7881('https://tools.7881.com/helper/mallbill/1', ck_7881)
    # except:
    #     print("请确认7881登录了！")
    # shop_DD373 = myprice['StatusData']['ResultData']['PageResult']
    # if restxt == '' and prices == '':
    #     ck_7881 =get_ck(get_login_cookies_7881())
    #     time.sleep(0.5)
    #     restxt, prices = get_price_7881('https://tools.7881.com/helper/mallbill/1', ck_7881)
    #     if restxt == '' and prices == '':
    #         time.sleep(0.5)
    #         restxt, prices = get_price_7881('https://tools.7881.com/helper/mallbill/1', ck_7881)
    #         if restxt == '' and prices == '':
    #             time.sleep(0.5)
    #             restxt, prices = get_price_7881('https://tools.7881.com/helper/mallbill/1', ck_7881)
    #             if restxt == '' and prices == '':
    #                 time.sleep(0.5)
    #                 restxt, prices = get_price_7881('https://tools.7881.com/helper/mallbill/1', ck_7881)
    #                 if restxt == '' and prices == '':
    #                     print("7881—--没有爬取到数据")
    #                     return ''

    print("开始寻找指定的数据。")
    for LI in LastID:
        if len(LI)>=5:
            if list[0] == LI[0]:
                for dd in shop_DD373:
                    # if dd['LastId'] == LI[0]:
                    #     Inv_dd373 = dd
                    #     inventory=list[2]
                    #     Inv_7881 = []
                    #     if len(restxt) > 0:
                    #         for res_7881 in restxt:
                    #             if res_7881[0] == list[1]:
                    #                 Inv_7881 = res_7881
                    #                 continue
                    #     try:
                    #         dataPrice = {}
                    #         dataPrice["goodsId"] = Inv_7881[0]
                    #         dataPrice["stock"] = int(inventory)  # 库存
                    #         dataPrice["price"] = Inv_7881[2]
                    #         listprice = [dataPrice]
                    #         set_price_7881(r'https://tools.7881.com/helper/listbill/goods/1/price/edit',listprice, ck_7881, "--7881--" + str(inventory), LI[2])
                    #     except:
                    #         print("7881_修改失败")

                        try:
                            myprice = get_api('https://goods.dd373.com/Api/MallGoods/UserCenter/List?MerchantType=1&LastId=&GoodsType=&Status=-1&PageIndex=1&PageSize=40',ck_dd373)
                            if myprice['StatusData']['ResultCode'] == '4001':
                                print("dd373登录参数失效！")
                                myprice,ck_dd373=getck(2,ck_dd373)
                            post_data = ''
                            post_data=post_data+r'Goods%5B0%5D%5BShopNumber%5D'+'='+Inv_dd373['ShopNumber']+r'&'
                            post_data=post_data+r'Goods%5B0%5D%5BInventory%5D'+'='+str(int(inventory))+r'&'
                            post_data=post_data+r'Goods%5B0%5D%5BUnitPrice%5D'+'='+str(Inv_dd373['SingleUnitPrice'])+r'&'
                            post_data=post_data+r'Goods%5B0%5D%5BIsTrusteeship%5D'+'='+str(Inv_dd373['IsTrusteeship']).lower()
                            setprice=set_price_in(r"https://goods.dd373.com/Api/MallGoods/UserCenter/Save", post_data, ck_dd373,"---dd373---库存：", inventory)
                            intst=1
                            while setprice == False:
                                if intst>=50:
                                    print("修改次数过多！结束此次修改！")
                                myprice,ck_dd373=getck(2,ck_dd373)
                                setprice = set_price_in(r"https://goods.dd373.com/Api/MallGoods/UserCenter/Save",post_data, ck_dd373, "dd373---库存：", inventory)
                                print("重改延迟20秒")
                                intst=intst+1
                                time.sleep(5)
                        except:
                            print("dd373_修改失败")




def cmd(put,come):
    global while_control
    while while_control:
        txt=input()
        if txt!='':
            if txt=='quit':
                while_control=0
                put.join()
                print('关闭收货')
                come.join()
                print('关闭出货')
            cm=txt.split(" ")
        if len(cm)==3:
            print()
            if cm[0]=='set':
                for last in LastID:
                    if len(last)>=5:
                        if last[4]==cm[1]:
                            print('正在修改！')
                            set_inventory([last[0],last[3],cm[2]])

            else:
                print("修改命令有误！")

        else:
            print("命令有误！")
        txt=''

come_thread_put=threading.Thread(target=put_price,args=(while_time,ck_dd373))
come_thread=threading.Thread(target=come_price,args=(while_time,ck_dd373))
cmd=threading.Thread(target=cmd,args=(come_thread_put,come_thread))
cmd.start()
come_thread_put.start()
come_thread.start()

#come_price(while_time,cook)
#put_price(while_time,cook)

#StatusData》ResultData》PageResult  全部商品列表    //GoodsType商品类型如金币
#LastId 区服信息
#StatusData》ResultData》TotalRecord 货架商品数量

