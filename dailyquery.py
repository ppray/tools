#! /usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import json
import sqlite3


r = requests.get("https://api.huobipro.com/market/detail?symbol=btcusdt")
#print r.content
hjson = json.loads(r.content)
price = hjson['tick']['close']
cny = price *6.4

difficulty =  requests.get("https://blockchain.info/q/getdifficulty").content
network_hashrate_G =  int(requests.get("https://blockchain.info/q/hashrate").content)
nhg=network_hashrate_G
btc_2weeks_income_per_100T = 1800.0 * 14 * 100000 / network_hashrate_G

i=1
sum = 0

while (i <=13 ):
    btc_2weeks_income_per_100T = 1800.0 * 14 * 100000 / network_hashrate_G
    sum = sum + btc_2weeks_income_per_100T
    #print i, "th 2weeks sum is", sum, "network_hashrate_G is", network_hashrate_G
    network_hashrate_G = network_hashrate_G*1.07
    i = i + 1 

income_cny_half_year_per_T = sum *cny /100
income_btc_half_year_per_T = sum /100
consume_ele_half_year = 13.44*7*26 #1400w

print "比特币矿机购买价格指南：\n"

hs = 4
while (hs <=20):
    #print income_cny_half_year_per_T, hs, consume_ele_half_year
    print hs,"T 矿机价格低于", int(income_cny_half_year_per_T*hs - consume_ele_half_year), "元"
    hs = hs +1

print "\n量化分析参数，当前币价：",cny,"，当前难度", difficulty, " 全网算力：",nhg,"G，ROI：182，每次难度增长估算：7%，产量：",income_btc_half_year_per_T, "btc/T，电费：",consume_ele_half_year,"(1400w, 0.4元计)\n"


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
    print "date time is:", row[5]
    print "date time is:", row[4]
    print "date time is:", row[6]

#print "current ID is", ID
import datetime
now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

##### Record s9 14t #####
ID = ID +1
#print "s9 ID is", ID
price = int(income_cny_half_year_per_T*14 - consume_ele_half_year)
if price<0:
    price = 0
qstr="INSERT INTO minerprice (ID,NAME,bestprice,date) VALUES (%s,'s9_14',%s,'%s')" % (ID,price,now)
print qstr
c.execute(qstr);

##### Record s9 13t #####
ID = ID +1
price = int(income_cny_half_year_per_T*13 - consume_ele_half_year)
qstr="INSERT INTO minerprice (ID,NAME,bestprice,date) VALUES (%s,'s9_13',%s,'%s')" % (ID,price,now)
c.execute(qstr);

##### Record t9 10.5t #####
ID = ID +1
price = int(income_cny_half_year_per_T*10.5 - consume_ele_half_year)
qstr="INSERT INTO minerprice (ID,NAME,bestprice,date) VALUES (%s,'t9',%s,'%s')" % (ID,price,now)
c.execute(qstr);

##### Record v9 4t #####
ID = ID +1
price = int(income_cny_half_year_per_T*4 - consume_ele_half_year)
qstr="INSERT INTO minerprice (ID,NAME,bestprice,date) VALUES (%s,'v9',%s,'%s')" % (ID,price,now)
c.execute(qstr);

##### Record Halong 16t #####
ID = ID +1
price = int(income_cny_half_year_per_T*16 - consume_ele_half_year)
qstr="INSERT INTO minerprice (ID,NAME,bestprice,date) VALUES (%s,'halong',%s,'%s')" % (ID,price,now)
c.execute(qstr);


conn.commit()
print "Records created successfully";
conn.close()

