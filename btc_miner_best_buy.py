#! /usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import json
import os
import sqlite3

class miner:
    #定义基本属性
    hs=0
    power=0
    price=0
    btcprice=0
    nhr = 0
    ele = 0 #Electricity

    def __init__(self,name,hs,pw,pr,bpr,nhr):
        self.hs = hs
        self.name = name
        self.power = pw
        self.price = pr # miner price
        self.btcprice = bpr # btc price
        self.nhr = nhr # unit G

    def roi(self):
        i=1
        roi = 720
        total = 0
        cny = self.btcprice *6.4 #btc price CNY
        bestprice = self.price
        
        print "\n",self.name,"当前售价",self.price
        while (i <= 102):
            btc_2weeks_income_per_100T = 1800.0 * 14 * 100000 / self.nhr
            btc_daily_income_per_100T = 1800.0 * 100000 / self.nhr
            total = total + btc_2weeks_income_per_100T
            if (total/100*self.hs*cny >= self.price+self.power/1000*24*0.5*14*i):
                roi = i*14 - ((total/100*13*cny) - self.price)/(btc_daily_income_per_100T*cny)
                break
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
        return bestprice,roi

    def speak(self):  
        print("%s is speaking: I am %d years old" %(self.hs,self.price))

    def bestprice(self):  
        print ""        

r = requests.get("https://api.huobipro.com/market/detail?symbol=btcusdt")
#print r.content
hjson = json.loads(r.content)
price = hjson['tick']['close']
cny = price *6.4

difficulty =  requests.get("https://blockchain.info/q/getdifficulty").content
network_hashrate_G =  int(requests.get("https://blockchain.info/q/hashrate").content)
network_hashrate_p =  round(network_hashrate_G/1000000000.0,2)
cost_ele_half_year = 13.44*7*26 #1400w

##     hashrate power minerprice btcprice, nh, 
t9 = miner("T9 10.5T",10.5,1432,5600,price,network_hashrate_G)

s9_13 = miner("S9 13T",13,1280,9000,price,network_hashrate_G)

s9_14 = miner("S9 14T",14,1372,10500,price,network_hashrate_G)

t1 = miner("T1 16T",16,1480,17500,price,network_hashrate_G)

v9 = miner("V9 4T",4,1027,1710,price,network_hashrate_G)


print "\n量化分析参数，当前币价：",cny,"，当前难度", difficulty, " 全网算力：",network_hashrate_p,"P，每次难度增长估算：7%，电费：0.5\n"



btc_balance_of_bigboss =  int(requests.get("https://blockchain.info/q/addressbalance/3Cbq7aT1tY8kMxWLbitaG7yT6bPbKChq64").content)
if btc_balance_of_bigboss < 10105598648665:
    print "Big boss sell", (10105598648665-btc_balance_of_bigboss)/100000000, "BTC"
else:
    print "Big boss buy", (btc_balance_of_bigboss-10105598648665)/100000000, "BTC"

### Write into DB
conn = sqlite3.connect('/home/ec2-user/btcminer.db')
c = conn.cursor()
cursor =c.execute("select * from btcstats order by ID desc limit 1")
for row in cursor:
    ID=row[0]

#print "current ID is", ID

import datetime
now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

ID = ID +1

qstr = "INSERT INTO btcstats (ID,date,price,hashrate) VALUES (%s,'%s',%s,%s)" % (ID,now,price,network_hashrate_G)
print "qstr is ", qstr
c.execute(qstr);

conn.commit()
print "Records created successfully";
conn.close()
