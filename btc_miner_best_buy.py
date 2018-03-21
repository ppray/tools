#! /usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import json

r = requests.get("https://api.huobipro.com/market/detail?symbol=btcusdt")
#print r.content
hjson = json.loads(r.content)
price = hjson['tick']['close']
cny = price *6.4

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
consume_ele_half_year = 13.44*7*26 #1400w

hs = 4
while (hs <=20):
    print hs,"T 矿机价格低于", int(income_cny_half_year_per_T*hs-income_cny_half_year_per_T), "元"
    hs = hs +1

print "\n量化分析参数，当前币价：",cny,"，当前全网算力：",nhg,"G，ROI：182，每次难度增长估算：7%，电费：",consume_ele_half_year,"(1400w, 0.4元计)"
