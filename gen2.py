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
    print html
    return html

def html_table(usd,name,p1,p2,p3,p4,p5):
    p1 = str(round(p1,6))+" BTC ($"+str(round(p1*float(usd),2))+")"
    p2 = str(round(p2,6))+" BTC ($"+str(round(p2*float(usd),2))+")"
    p3 = str(round(p3,6))+" BTC ($"+str(round(p3*float(usd),2))+")"
    p4 = str(round(p4,6))+" BTC ($"+str(round(p4*float(usd),2))+")"
    p5 = str(round(p5,6))+" BTC ($"+str(round(p5*float(usd),2))+")"
    html = '''
          <h6 class="aya">
            %s
          </h6>
            <a class="pu rs xj ux" href="#">
              <span>Halong 16T</span>
              <span class="awy">%s</span>
            </a>

            <a class="pu rs xj ux" href="#">
              <span>AntMiner S9 14T</span>
              <span class="awy">%s</span>
            </a>

            <a class="pu rs xj ux" href="#">
              <span>AntMiner S9 13.5T</span>
              <span class="awy">%s</span>
            </a>

            <a class="pu rs xj ux" href="#">
              <span>AntMiner T9 10.5T</span>
              <span class="awy">%s</span>
            </a>

            <a class="pu rs xj ux" href="#">
              <span>AntMiner v9 4T</span>
              <span class="awy">%s</span>
            </a> ''' % (name,p1,p2,p3,p4,p5)
    #print html
    return html

### Write into DB
conn = sqlite3.connect('/home/ec2-user/btcminer.db')
c = conn.cursor()
cursor2 =c.execute("select * from btcstats order by ID desc limit 2")
btcprice = []
ngh = []

for row in cursor2:
    btcprice.append(int(row[2]))
    ngh.append(round(row[3]/1000000000.0,2))

cursor =c.execute("select * from minerprice order by ID desc limit 50")

halong_numb = ""
v9_numb = ""
t9_numb = ""
s9_13_numb = ""
s9_14_numb = ""
datetime = ""

v9_cprice = []
t9_cprice = []
s9_13_cprice = []
s9_14_cprice = []
halong_cprice = []

v9_income = ""
t9_income = "" 
s9_13_income = "" 
s9_14_income = "" 
halong_income = ""


v9_income_day = 0
t9_income_day = 0 
s9_13_income_day = 0
s9_14_income_day = 0 
halong_income_day = 0

v9_income_month = 0
t9_income_month = 0 
s9_13_income_month = 0
s9_14_income_month = 0 
halong_income_month = 0

v9_income_year = 0
t9_income_year = 0 
s9_13_income_year = 0
s9_14_income_year = 0 
halong_income_year = 0

roi = {}


    
for row in cursor:
    ID=row[0]
    if row[1] == "halong":
        halong_numb = str(int(row[2]/6.4))+", "+halong_numb
        halong_income = str(round(float(row[10])*float(btc_price_usdt),2))+", "+halong_income #Year
        if halong_income_day == 0:
            halong_income_day = row[8]
            halong_income_month = row[9]
            halong_income_year = row[10]
        halong_cprice.append(row[3])
        datetime = "'"+str(row[6])+"', "+datetime
        if not  roi.has_key("halong"):
            roi["halong"] = str(row[7])
            print "halong roi is ", roi["halong"]
    if row[1] == "v9":
        if row[2] < 0:
            v9_numb = "1, "+v9_numb
        else:
            v9_numb = str(int(row[2]/6.4))+", "+v9_numb
        v9_income = str(round(row[10]*float(btc_price_usdt),2))+", "+v9_income
        if v9_income_day == 0:
            v9_income_day = row[8]
            v9_income_month = row[9]
            v9_income_year = row[10]
        v9_cprice.append(row[3])
        if not  roi.has_key("v9"):
            roi["v9"] = str(row[7])
    if row[1] == "t9":
        t9_numb = str(int(row[2]/6.4))+", "+t9_numb
        t9_income = str(round(row[10]*float(btc_price_usdt),2))+", "+t9_income
        if t9_income_day == 0:
            t9_income_day = row[8]
            t9_income_month = row[9]
            t9_income_year = row[10]
        t9_cprice.append(row[3])
        if not  roi.has_key("t9"):
            roi["t9"] = str(row[7])
    if row[1] == "s9_13":
        s9_13_numb = str(int(row[2]/6.4))+", "+s9_13_numb
        s9_13_income = str(round(row[10]*float(btc_price_usdt),2))+", "+s9_13_income
        if s9_13_income_day == 0:
            s9_13_income_day = row[8]
            s9_13_income_month = row[9]
            s9_13_income_year = row[10]
        s9_13_cprice.append(row[3])
        if not  roi.has_key("s9_13"):
            roi["s9_13"] = str(row[7])
    if row[1] == "s9_14":
        s9_14_numb = str(int(row[2]/6.4))+", "+s9_14_numb
        s9_14_income = str(round(row[10]*float(btc_price_usdt),2))+", "+s9_14_income
        if s9_14_income_day == 0:
            s9_14_income_day = row[8]
            s9_14_income_month = row[9]
            s9_14_income_year = row[10]
        s9_14_cprice.append(row[3])
        if not  roi.has_key("s9_14"):
            roi["s9_14"] = str(row[7])


print "halong best price is", halong_numb
print "v9 best price is", v9_numb
print "t9 best price is", t9_numb
print "s9 13T best price is", s9_13_numb
print "s9 14T best price is", s9_14_numb
print "HTML was generated in /var/www/html/index.html"

print "halong daily income is", halong_income
roi_html = roi["halong"]+", "+roi["s9_14"]+", "+roi["s9_13"]+", "+roi["t9"]+", "+roi["v9"]

### Creat Bar
bar_bestprice = re.sub(r',',"",halong_numb).split( )[-1]
bar_bestprice = bar_bestprice+", "+re.sub(r',',"",s9_14_numb).split( )[-1]
bar_bestprice = bar_bestprice+", "+re.sub(r',',"",s9_13_numb).split( )[-1]
bar_bestprice = bar_bestprice+", "+re.sub(r',',"",t9_numb).split( )[-1]
bar_bestprice = bar_bestprice+", "+re.sub(r',',"",v9_numb).split( )[-1]

cprice_list = str(halong_cprice[0])+", "+str(s9_14_cprice[0])+", "+str(s9_13_cprice[0])+", "+str(t9_cprice[0])+", "+str(v9_cprice[0])

print "bar_bestprice is ", bar_bestprice
print "cprice_list is ", cprice_list

### Creat table

day_income = html_table(btc_price_usdt,"Profit /day",halong_income_day,s9_14_income_day,s9_13_income_day,t9_income_day,v9_income_day)
month_income = html_table(btc_price_usdt,"Profit /month",halong_income_month,s9_14_income_month,s9_13_income_month,t9_income_month,v9_income_month)
year_income = html_table(btc_price_usdt,"Profit /year",halong_income_year,s9_14_income_year,s9_13_income_year,t9_income_year,v9_income_year)

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
html = re.sub(r'{t9}', t9_income, f.read())
html = re.sub(r'{v9}', v9_income, html)
html = re.sub(r'{13t}', s9_13_income, html)
html = re.sub(r'{14t}', s9_14_income, html)
html = re.sub(r'{16t}', halong_income, html)
html = re.sub(r'{datetime}', datetime, html)

html = re.sub(r'{market_price}', price_stats, html)
html = re.sub(r'{network_hash}', NH_stats, html)

html = re.sub(r'{bestprice}', bar_bestprice, html)
html = re.sub(r'{marketprice}', cprice_list, html)
html = re.sub(r'{diffi}', difficulty, html)

html = re.sub(r'{roi}', roi_html, html)

html = re.sub(r'{day_income}', day_income, html)
html = re.sub(r'{month_income}', month_income, html)
html = re.sub(r'{year_income}', year_income, html)

open('/var/www/html/index.html', 'w').write(html)

conn.close()
