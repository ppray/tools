#! /usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import json
import sqlite3
import datetime
import os
import re
import types


def html_table(lol,name,price):
    html = '  <tr><td>'+name
    for sublist in lol:
        if type(sublist) is types.StringType:
            html = html+ '    </td><td>'+str(sublist)
        else:
            html = html+ '    </td><td>'+str(sublist)+'('+str(round(sublist*float(price),2))+'美元)'
    html = html + '  </td></tr>'
    print html
    return html

### Write into DB
conn = sqlite3.connect('/home/ec2-user/btcminer.db')
c = conn.cursor()
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

v9_income = []
t9_income = []
s9_13_income = []
s9_14_income = []
halong_income = []

roi = {}

btc_price_usdt = requests.get("https://blockchain.info/q/24hrprice").content

for row in cursor:
    ID=row[0]
    if row[1] == "halong":
        halong_numb = str(row[2])+", "+halong_numb
        halong_cprice.append(row[3])
        datetime = "'"+str(row[6])+"', "+datetime
        if not  roi.has_key("halong"):
            roi["halong"] = str(row[7])
        if halong_income == []:
            halong_income.append(row[8])
            halong_income.append(row[9])
            halong_income.append(row[10])
            halong_income.append(row[11].encode('utf-8').strip())
            table_16t = html_table(halong_income,"Halong 16T",btc_price_usdt)
    if row[1] == "v9":
        v9_numb = str(row[2])+", "+v9_numb
        v9_cprice.append(row[3])
        if not  roi.has_key("v9"):
            roi["v9"] = str(row[7])
        if v9_income == []:
            v9_income.append(row[8])
            v9_income.append(row[9])
            v9_income.append(row[10])
            v9_income.append(row[11].encode('utf-8').strip())
            table_v9 = html_table(v9_income,"蚂蚁v9 4T",btc_price_usdt)
    if row[1] == "t9":
        t9_numb = str(row[2])+", "+t9_numb
        t9_cprice.append(row[3])
        if not  roi.has_key("t9"):
            roi["t9"] = str(row[7])
        if t9_income == []:
            t9_income.append(row[8])
            t9_income.append(row[9])
            t9_income.append(row[10])
            t9_income.append(row[11].encode('utf-8').strip())
            table_t9 = html_table(t9_income,"蚂蚁T9 10.5T",btc_price_usdt)
    if row[1] == "s9_13":
        s9_13_numb = str(row[2])+", "+s9_13_numb
        s9_13_cprice.append(row[3])
        if not  roi.has_key("s9_13"):
            roi["s9_13"] = str(row[7])
        if s9_13_income == []:
            s9_13_income.append(row[8])
            s9_13_income.append(row[9])
            s9_13_income.append(row[10])
            s9_13_income.append(row[11].encode('utf-8').strip())
            table_13t = html_table(s9_13_income,"蚂蚁S9 13.5T",btc_price_usdt)
    if row[1] == "s9_14":
        s9_14_numb = str(row[2])+", "+s9_14_numb
        s9_14_cprice.append(row[3])
        if not  roi.has_key("s9_14"):
            roi["s9_14"] = str(row[7])
        if s9_14_income == []:
            s9_14_income.append(row[8])
            s9_14_income.append(row[9])
            s9_14_income.append(row[10])
            s9_14_income.append(row[11].encode('utf-8').strip())
            table_14t = html_table(s9_14_income,"蚂蚁S9 14T",btc_price_usdt)
    # print "row0 is ID:", row[0]
    # print "NAME is:", row[1]
    # print "bestprice is:", row[2]
    # print "date time is:", row[6]
print "halong best price is", halong_numb
print "v9 best price is", v9_numb
print "t9 best price is", t9_numb
print "s9 13T best price is", s9_13_numb
print "s9 14T best price is", s9_14_numb
print "HTML was generated in /var/www/html/index4.html"

roi_html = roi["halong"]+", "+roi["s9_14"]+", "+roi["s9_13"]+", "+roi["t9"]+", "+roi["v9"]

f_path = r'/var/www/html/template.html'
f = open (f_path, "r+")
html = re.sub(r'{t9}', t9_numb, f.read())
html = re.sub(r'{v9}', v9_numb, html)
html = re.sub(r'{s9_13}', s9_13_numb, html)
html = re.sub(r'{s9_14}', s9_14_numb, html)
html = re.sub(r'{halong}', halong_numb, html)
html = re.sub(r'{datetime}', datetime, html)

html = re.sub(r'{table_v9}', table_v9, html)
html = re.sub(r'{table_t9}', table_t9, html)
html = re.sub(r'{table_13t}', table_13t, html)
html = re.sub(r'{table_14t}', table_14t, html)
html = re.sub(r'{table_16t}', table_16t, html)

html = re.sub(r'{roi}', roi_html, html)

### Creat Bar
bar_bestprice = re.sub(r',',"",halong_numb).split( )[-1]
bar_bestprice = bar_bestprice+", "+re.sub(r',',"",s9_14_numb).split( )[-1]
bar_bestprice = bar_bestprice+", "+re.sub(r',',"",s9_13_numb).split( )[-1]
bar_bestprice = bar_bestprice+", "+re.sub(r',',"",t9_numb).split( )[-1]
bar_bestprice = bar_bestprice+", "+re.sub(r',',"",v9_numb).split( )[-1]

bar_cprice = str(halong_cprice[0])+","+str(s9_14_cprice[0])+","+str(s9_13_cprice[0])+","+str(t9_cprice[0])+","+str(v9_cprice[0])
print "bar_bestprice is ", bar_bestprice
print "bar_cprice is ", bar_cprice

html = re.sub(r'{bestprice}', bar_bestprice, html)
html = re.sub(r'{cprice}', bar_cprice, html)
open('/var/www/html/index4.html', 'w').write(html)

conn.close()
