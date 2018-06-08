#! /usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import json
import sqlite3
import datetime
import os
import re
import types


btc_price_usdt = requests.get("https://blockchain.info/q/24hrprice").content

def html_stats(name,number,delta,tag):
    if tag == 1:
        class1 = "aws"
        class2 = "bpk"
    else:
        class1 = "awv"
        class2 = "bpl"
    html = '''
        <h3 class="bph %s">
          %s
          <small class="bpj %s">%s</small>
        </h3>
        <span class="bpi">%s</span>
    ''' % (class1,number,class2,delta,name)
    #print html
    return html

## Gengerate string like "0.000931 BTC ($6.95)"
def profit_string(usd,profit):
    return str(round(profit,6))+" BTC ($"+str(round(profit*float(usd),2))+")"

## Generate profit table
def html_table(usd,table_name,device_list,device_name,profit_list):
    html = '''
          <h6 class="aya">
            %s
          </h6>''' % (table_name)
    a = {} 
    for miner in device_list:
        a[miner] = '''
               <a class="pu rs xj ux" href="#">
                 <span>%s</span>
                 <span class="awy">%s</span>
               </a> ''' % (device_name[miner],profit_string(usd,profit_list[miner]))
        html = html+a[miner]

    #print html
    return html

### Read data from DB
conn = sqlite3.connect('/home/ec2-user/btcminer.db')
c = conn.cursor()
##### Get market price, network hashrate and difficulty
stats_cursor =c.execute("select * from btcstats order by ID desc limit 2")
btcprice = []
ngh = []

for row in stats_cursor:
    btcprice.append(int(row[2]))
    ngh.append(round(row[3]/1000000000.0,2))

##### Get ROI and price.
miner_cursor =c.execute("select * from minerprice order by ID desc limit 50")

##### Initial #####
device_list = []
device_name_list = []
device_name = {}
txt= open("device_list.txt", "r").readlines()
for line in txt:
    miners = line.split(",")
    device_name[miners[0].strip()] = miners[1].strip()
    device_list.append( miners[0].strip())
    device_name_list.append( miners[1].strip())


#print "device_list is ", device_list
#print "device_name is ", device_name

datetime = ""
roi = {}

## Initial string for best price
bestprice = {}
## Initial string for year_income_usd
year_income_usd = {}
## Initial number for day_income
day_income = {}
## Initial number for month_income
month_income = {}
## Initial number for year_income
year_income = {}
## Initial number for cprice
cprice = {}
## Initial string for roi_dataset
roi_dataset = ""
roi_dataset_y = ""
for i in device_list:
    roi_dataset_y = "'"+device_name[i]+"', "+roi_dataset_y
## Initial string for cprice_list
cprice_list = ""
bar_bestprice = ""

for miner in device_list:
    bestprice[miner] = ""
    year_income_usd[miner] = ""
    day_income[miner] = 0
    month_income[miner] = 0
    year_income[miner] = 0
    cprice[miner] = []

for row in miner_cursor:
    ID=row[0]
    for miner in device_list:
        if miner == row[1]:
            bestprice[miner] = str(int(row[2]/6.4))+", "+bestprice[miner]
            year_income_usd[miner] = str(round(float(row[10])*float(btc_price_usdt),2))+", "+year_income_usd[miner] #Year
             
            if day_income[miner] == 0:
                day_income[miner] = row[8]
                month_income[miner] = row[9]
                year_income[miner] = row[10]
            if not re.search(str(row[6]),datetime):
                datetime = "'"+str(row[6])+"', "+datetime
            cprice[miner].append(row[3])
            if not  roi.has_key(miner):
                roi[miner] = str(row[7])
                #print miner, "roi is ", roi[miner]

## check data for graphic 
for miner in device_list:
    print miner, " best price is", bestprice[miner]
    print miner, " year income is", year_income_usd[miner], "\n"
    roi_dataset = roi[miner]+", "+roi_dataset
    print miner, " roi is ", roi[miner]
    ### Creat Bar
    if bar_bestprice == "":
        bar_bestprice = re.sub(r',',"",bestprice[miner]).split( )[-1]
    else:
        bar_bestprice = bar_bestprice+", "+re.sub(r',',"",bestprice[miner]).split( )[-1]
    if cprice_list == "":
        cprice_list = str(cprice[miner][0])
    else:
        cprice_list = cprice_list+", "+str(cprice[miner][0])
print "roi_dataset is " , roi_dataset
print "roi_dataset_y is ", roi_dataset_y
print "bar_bestprice is ", bar_bestprice
print "cprice_list is ", cprice_list



### Creat table

day_income_table = html_table(btc_price_usdt,"Profit /day",device_list,device_name,day_income)
month_income_table = html_table(btc_price_usdt,"Profit /month",device_list,device_name,month_income)
year_income_table = html_table(btc_price_usdt,"Profit /year",device_list,device_name,year_income)

tag = 0
if btcprice[0] > btcprice[1]:
    tag = 1
    delta = "%.2f%%" %(float(btcprice[0]-btcprice[1])/btcprice[1] * 100)
else:
    delta = "%.2f%%" %(float(btcprice[1]-btcprice[0])/btcprice[0] * 100)

print "delta is ", delta, btcprice[1], btcprice[0], float(btcprice[1]-btcprice[0])/btcprice[0] * 100
price_stats = html_stats("Market Price","$"+str(btcprice[0]),delta,tag)


if ngh[0] > ngh[1]:
    tag = 1
    delta = "%.2f%%" %((ngh[0]-ngh[1])/ngh[1] * 100)
else:
    delta = "%.2f%%" %((ngh[1]-ngh[0])/ngh[0] * 100)
    tag = 0

NetworkHash = str(ngh[0])+" E"
NH_stats = html_stats("Network Hashrate",NetworkHash,delta,tag)

difficulty =  requests.get("https://blockchain.info/q/getdifficulty").content

### Wirte html
f_path = r'/var/www/html/temp2.html'
f = open (f_path, "r+")
#html = re.sub(r'{t9}', year_income_usd["t9"], f.read())
#html = re.sub(r'{v9}', year_income_usd["v9"], html)
#html = re.sub(r'{13t}', year_income_usd["s9_13"], html)
#html = re.sub(r'{14t}', year_income_usd["s9_14"], html)
#html = re.sub(r'{16t}', year_income_usd["halong"], html)

html = re.sub(r'{datetime}', datetime, f.read())

html = re.sub(r'{market_price}', price_stats, html)
html = re.sub(r'{network_hash}', NH_stats, html)

html = re.sub(r'{bestprice}', bar_bestprice, html)
html = re.sub(r'{device_list}', str(device_name_list), html)
html = re.sub(r'{marketprice}', cprice_list, html)
html = re.sub(r'{diffi}', difficulty, html)

html = re.sub(r'{roi}', roi_dataset, html)
html = re.sub(r'{roi_y}', roi_dataset_y, html)

html = re.sub(r'{day_income}', day_income_table, html)
html = re.sub(r'{month_income}', month_income_table, html)
html = re.sub(r'{year_income}', year_income_table, html)

open('/var/www/html/index.html', 'w').write(html)
print "HTML was generated in /var/www/html/index.html"

conn.close()
