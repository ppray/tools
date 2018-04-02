#! /usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import json
import sqlite3
import datetime
import os
import re

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

for row in cursor:
    ID=row[0]
    if row[1] == "halong":
        halong_numb = str(row[2])+", "+halong_numb
        datetime = "'"+str(row[6])+"', "+datetime
    if row[1] == "v9":
        v9_numb = str(row[2])+", "+v9_numb
    if row[1] == "t9":
        t9_numb = str(row[2])+", "+t9_numb
    if row[1] == "s9_13":
        s9_13_numb = str(row[2])+", "+s9_13_numb
    if row[1] == "s9_14":
        s9_14_numb = str(row[2])+", "+s9_14_numb
    # print "row0 is ID:", row[0]
    # print "NAME is:", row[1]
    # print "bestprice is:", row[2]
    # print "date time is:", row[6]
print "halong best price is", halong_numb
print "v9 best price is", v9_numb
print "t9 best price is", t9_numb
print "s9 13T best price is", s9_13_numb
print "s9 14T best price is", s9_14_numb
print "HTML was generated in /var/www/html/index.html"

f_path = r'/var/www/html/template.html'
f = open (f_path, "r+")
html = re.sub(r'{t9}', t9_numb, f.read())
html = re.sub(r'{v9}', v9_numb, html)
html = re.sub(r'{s9_13}', s9_13_numb, html)
html = re.sub(r'{s9_14}', s9_14_numb, html)
html = re.sub(r'{halong}', halong_numb, html)
html = re.sub(r'{datetime}', datetime, html)

### Creat Bar
bar_bestprice = re.sub(r',',"",halong_numb).split( )[-1]
bar_bestprice = bar_bestprice+", "+re.sub(r',',"",s9_14_numb).split( )[-1]
bar_bestprice = bar_bestprice+", "+re.sub(r',',"",s9_13_numb).split( )[-1]
bar_bestprice = bar_bestprice+", "+re.sub(r',',"",t9_numb).split( )[-1]
bar_bestprice = bar_bestprice+", "+re.sub(r',',"",v9_numb).split( )[-1]

print "bar_bestprice is ", bar_bestprice

html = re.sub(r'{bestprice}', bar_bestprice, html)
open('/var/www/html/index.html', 'w').write(html)

###### Record s9 14t #####
#ID = ID +1
##print "s9 ID is", ID
#price = int(income_cny_half_year_per_T*14 - consume_ele_half_year)
#qstr="INSERT INTO minerprice (ID,NAME,bestprice,date) VALUES (%s,'s9_14',%s,'%s')" % (ID,price,now)
#print qstr
#c.execute(qstr);
#
###### Record s9 13t #####
#ID = ID +1
#price = int(income_cny_half_year_per_T*13 - consume_ele_half_year)
#qstr="INSERT INTO minerprice (ID,NAME,bestprice,date) VALUES (%s,'s9_13',%s,'%s')" % (ID,price,now)
#c.execute(qstr);
#
###### Record t9 10.5t #####
#ID = ID +1
#price = int(income_cny_half_year_per_T*10.5 - consume_ele_half_year)
#qstr="INSERT INTO minerprice (ID,NAME,bestprice,date) VALUES (%s,'t9',%s,'%s')" % (ID,price,now)
#c.execute(qstr);
#
###### Record v9 4t #####
#ID = ID +1
#price = int(income_cny_half_year_per_T*4 - consume_ele_half_year)
#qstr="INSERT INTO minerprice (ID,NAME,bestprice,date) VALUES (%s,'v9',%s,'%s')" % (ID,price,now)
#c.execute(qstr);
#
###### Record Halong 16t #####
#ID = ID +1
#price = int(income_cny_half_year_per_T*16 - consume_ele_half_year)
#qstr="INSERT INTO minerprice (ID,NAME,bestprice,date) VALUES (%s,'halong',%s,'%s')" % (ID,price,now)
#c.execute(qstr);
#
#
#conn.commit()
#print "Records created successfully";
conn.close()













