#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os
import json
import requests

os.system('fibos claim_reward.js')
os.system('fibos account.js')

### check voter
r = requests.get("http://explorer.fibos.rocks/api/voter?producer=ukfiboooooos")
hjson = json.loads(r.content)
length = len(hjson)
index = 0

r2 = requests.get("https://explorer.fibos.rocks/api/vote?producer=ukfiboooooos")
vote = float(r2.content)
while index < length:
    voter = hjson[index]['owner']
    stake = float(hjson[index]['staked'])
    weight = round(stake/vote, 2)
    print voter, stake, weight
    index = index + 1
