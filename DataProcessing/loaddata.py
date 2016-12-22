f = open('merchants.json')
from requests import post
import json
# import time

for line in f:

                line = line.strip()
                try:
                        jsondata = json.loads(line)
                        latitude = jsondata['latitude']
                        longitude = jsondata['longitude']
                        address = jsondata['address']
                        add = ''
                        num = len(address)
                        i=0
                        for a in address:
                                if(i < num-1):
                                        add = add+a+", "
                                        i=i+1
                                else:
                                        add = add+a
                #print (address)
                        name = jsondata['name']
                        lon=longitude
                        lat=latitude
                        jsonOut = {"name":name,"address":add,"lon":lon,"lat":lat,"password":"1234"}
                        print(jsonOut)
                        post("http://54.173.234.214:5000/api/merchants/register=True", json=jsonOut).json()
                except:
                        continue
        # time.sleep(100)
