#! /usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import json
import os
import sqlite3

import re
import requests
from bs4 import BeautifulSoup

class crawler:
    #定义基本属性
    hr = "" #hashrate
    man = "" # Manufacturer
    name = ""

    def __init__(self,name,hr,man,soup):
        self.hr = hr
        self.name = name
        self.soup = soup
        self.man = man # Manufacturer

    def crawl(self):
        croi = 999
        for tr in self.soup.find_all('tr'):
            try:
                #print tr.find_all('td')[2].b.contents[1], tr.find_all('td')[3].a.contents[0]
                if re.search( self.man, tr.find_all('td')[2].b.contents[1], re.I) and re.search( self.hr,tr.find_all('td')[3].a.contents[0],re.I):
                    cprice = int(re.sub(r'\D', "", tr.find_all('td')[4].b.contents[0])) /100 * 6.4
                    croi = re.search( r'\d+',tr.find_all('td')[6].b.contents[0], re.M|re.I).group()
                    #print self.name,"price is ", cprice,"roi is", croi
            except Exception , e:
                continue
        return cprice,int(croi) # crawl price and roi


class miner:
    #定义基本属性
    hs=0
    power=0
    price=0
    btcprice=0
    nhr = 0
    ele = 0 #Electricity

    def __init__(self,name,hs,pw,pr,bpr,nhr,interval):
        self.hs = hs
        self.name = name
        self.power = pw
        self.price = pr # miner price
        self.btcprice = bpr # btc price
        self.nhr = nhr # unit G
        self.interval = float(interval) # average time between blocks in seconds 

    def roi(self):
        i=1
        roi = 720
        total = 0
        cny = self.btcprice *6.4 #btc price CNY
        bestprice = self.price
        btc_daily = 1800.0*600/self.interval * (self.hs * 1000) / self.nhr
        if btc_daily*cny > self.power/1000*24*0.5:
            huangli = "宜开机"
        else :
            huangli = "宜关机"
        
        print "\n",self.name,"当前售价",self.price
        while (i <= 27):
            btc_2weeks_income_per_100T = 1800.0*600/self.interval * 14 * 100000 / self.nhr
            btc_daily_income_per_100T = 1800.0*600/self.interval * 100000 / self.nhr
            total = total + btc_2weeks_income_per_100T
            if (total/100*self.hs*cny >= self.price+self.power/1000*24*0.5*14*i):
                roi = i*14 - ((total/100*13*cny) - self.price)/(btc_daily_income_per_100T*cny)
                #break
            #print i, "th 2weeks total is", total/100*self.hs, total/100*self.hs*cny , "network_hashrate_G is", network_hashrate_G,"cost is", self.price+self.power/1000*24*0.5*14*i
            if i == 2:
                btc_month = total / 100 * self.hs
            if i == 13:
                total_btc_half_year = total/100*self.hs
                total_cny_half_year = total_btc_half_year*cny
                total_ele_half_year = self.power/1000*24*0.5*14*i
                total_cost_cny_half_year = self.power/1000*24*0.5*14*i+self.price
                total_cost_bit_half_year = total_cost_cny_half_year/cny
                bestprice = int(total_cny_half_year - self.power/1000*24*0.5*14*i)
                print self.name,"建议购入价格",bestprice,"RMB"
                #print self.name,"挖矿半年收益：",total_cny_half_year,"RMB (",total_btc_half_year,"btc), 成本",total_cost_cny_half_year,"RMB(", total_cost_bit_half_year,"btc)"
            if i == 26:
                total_btc_one_year = total/100*self.hs
                total_cny_one_year = total/100*self.hs*cny
                total_ele_one_year = self.power/1000*24*0.5*14*i
                total_cost_cny_one_year = self.power/1000*24*0.5*14*i+self.price
                total_cost_bit_one_year = total_cost_cny_one_year/cny
                print self.name,"挖矿一年收益：",total_cny_one_year,"RMB (",total_btc_one_year,"btc), 成本",total_cost_cny_one_year,"RMB(", total_cost_bit_one_year,"btc)"
            self.nhr = self.nhr*1.07
            i = i + 1 
        if roi==720:
            print "回本周期: 无法回本"
        else:
            print "回本周期: ", roi,"天"
        if bestprice == self.price:
            huangli = huangli + " 宜购机"
        return bestprice,roi,btc_daily,btc_month,total_btc_one_year,huangli

    def speak(self):  
        print("%s is speaking: I am %d years old" %(self.hs,self.price))

    def bestprice(self):  
        print ""        



### Crawl price and roi
url = "https://www.asicminervalue.com/opportunities"
response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")
        
crawl_14t = crawler("S9 14T","14T","bitmain",soup)
crawl_13t = crawler("S9 13T","13.5T","bitmain",soup)
crawl_16t = crawler("Halong 16T","T1","Halong",soup)
crawl_t9 = crawler("T9 10.5T","t9","Bitmain",soup)
crawl_v9 = crawler("v9","v9","Bitmain",soup)



### Cauculate bestprice
r = requests.get("https://api.huobipro.com/market/detail?symbol=btcusdt")
#print r.content
hjson = json.loads(r.content)
btcprice = hjson['tick']['close']
#btcprice = requests.get("https://blockchain.info/q/24hrprice")
cny = btcprice *6.4

difficulty =  requests.get("https://blockchain.info/q/getdifficulty").content
interval =  requests.get("https://blockchain.info/q/interval").content   #average time between blocks in seconds 
#network_hashrate_G =  int(requests.get("https://blockchain.info/q/hashrate").content)
r2 = requests.get("https://chain.so/api/v2/get_info/btc")

hr_json = json.loads(r2.content)
network_hashrate_G = float(hr_json['data']['hashrate'])/1000000000
nhg=network_hashrate_G

cost_ele_half_year = 13.44*7*26 #1400w


print "\n量化分析参数，当前币价：",cny,"，当前难度", difficulty, " 全网算力：",nhg,"G，每次难度增长估算：7%，电费：0.5\n"

btc_balance_of_bigboss =  int(requests.get("https://blockchain.info/q/addressbalance/3Cbq7aT1tY8kMxWLbitaG7yT6bPbKChq64").content)

if btc_balance_of_bigboss < 9234706170247:
    print "Big boss sell", (9234706170247-btc_balance_of_bigboss)/100000000, "BTC"
else:
    print "Big boss buy", (btc_balance_of_bigboss-9234706170247)/100000000, "BTC"



### Write into DB
conn = sqlite3.connect('/home/ec2-user/btcminer.db')
c = conn.cursor()
cursor =c.execute("select * from minerprice order by ID desc limit 1")
for row in cursor:
    ID=row[0]
    print "date time is:", row[6]

#print "current ID is", ID
import datetime
now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

##### Record s9 14t #####
ID = ID +1
#print "s9 ID is", ID
cprice = 0
croi = 0

cprice,croi = crawl_14t.crawl()  # crawl price and roi
print "crawl_14t get cprice,croi ", cprice,croi 

s9_14 = miner("S9 14T",14,1372,cprice,btcprice,network_hashrate_G,interval)
price,roi,btc_day,btc_month,btc_year,huangli = s9_14.roi()

qstr="INSERT INTO minerprice (ID,NAME,bestprice,cprice,date,roi,day,month,year,huangli) VALUES (%s,'s9_14',%s,%s,'%s',%s,%s,%s,%s,'%s')" % (ID,price,int(cprice),now,int(croi),btc_day,btc_month,btc_year,huangli)
c.execute(qstr);

##### Record s9 13t #####
ID = ID +1
cprice,croi = crawl_13t.crawl()  # crawl price and roi
print "crawl_13t get cprice,croi ", cprice,croi 

s9_13 = miner("S9 13T",13,1280,cprice,btcprice,network_hashrate_G,interval)
price,roi,btc_day,btc_month,btc_year,huangli = s9_13.roi()
qstr="INSERT INTO minerprice (ID,NAME,bestprice,cprice,date,roi,day,month,year,huangli) VALUES (%s,'s9_13',%s,%s,'%s',%s,%s,%s,%s,'%s')" % (ID,price,int(cprice),now,int(croi),btc_day,btc_month,btc_year,huangli)
c.execute(qstr);

##### Record t9 10.5t #####
ID = ID +1
cprice,croi = crawl_t9.crawl()  # crawl price and roi
print "crawl_t9 get cprice,croi ", cprice,croi 

##     hashrate power minerprice btcprice, nh, 
t9 = miner("T9 10.5T",10.5,1432,cprice,btcprice,network_hashrate_G,interval)
price,roi,btc_day,btc_month,btc_year,huangli = t9.roi()

qstr="INSERT INTO minerprice (ID,NAME,bestprice,cprice,date,roi,day,month,year,huangli) VALUES (%s,'t9',%s,%s,'%s',%s,%s,%s,%s,'%s')" % (ID,price,int(cprice),now,int(croi),btc_day,btc_month,btc_year,huangli)
c.execute(qstr);

##### Record v9 4t #####
ID = ID +1
cprice,croi = crawl_v9.crawl()  # crawl price and roi
print "crawl_v9 get cprice,croi ", cprice,croi 

v9 = miner("V9 4T",4,1027,cprice,btcprice,network_hashrate_G,interval)
price,roi,btc_day,btc_month,btc_year,huangli = v9.roi()
qstr="INSERT INTO minerprice (ID,NAME,bestprice,cprice,date,roi,day,month,year,huangli) VALUES (%s,'v9',%s,%s,'%s',%s,%s,%s,%s,'%s')" % (ID,price,int(cprice),now,int(croi),btc_day,btc_month,btc_year,huangli)
c.execute(qstr);

##### Record Halong 16t #####
ID = ID +1
cprice,croi = crawl_16t.crawl()  # crawl price and roi
print "crawl_16t get cprice,croi ", cprice,croi 

t1 = miner("T1 16T",16,1480,cprice,btcprice,network_hashrate_G,interval)
price,roi,btc_day,btc_month,btc_year,huangli = t1.roi()

qstr="INSERT INTO minerprice (ID,NAME,bestprice,cprice,date,roi,day,month,year,huangli) VALUES (%s,'halong',%s,%s,'%s',%s,%s,%s,%s,'%s')" % (ID,price,int(cprice),now,int(croi),btc_day,btc_month,btc_year,huangli)
c.execute(qstr);


conn.commit()
print "Records created successfully";
conn.close()
