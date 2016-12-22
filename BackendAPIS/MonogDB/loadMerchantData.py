f = open('merchant.json')
from requests import post
import json
# import time

for line in f:

        line = line.strip()
        jsondata = json.loads(line)
        latitude = jsondata['latitude']
        longitude = jsondata['longitude']
        id = jsondata['id']
        categories = jsondata['categories']
        address = jsondata['address']
        name = jsondata['name']
        location = {'lat':latitude,'lon':longitude}
        jsonOut = {'merchantId':id,'name':name,'categories':categories,'address':address,'location':location}
        # print(jsonOut)
        post("http://0.0.0.0:5000/api/merchants", json=jsonOut).json()
        # time.sleep(100)
