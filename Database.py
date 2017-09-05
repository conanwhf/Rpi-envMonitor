#!/usr/bin/python3
#-*- coding:utf-8 -*-

import time
import json
import requests

#yeelink api配置
apiUrl='http://api.yeelink.net/v1.1/device/%s/sensor/%s/datapoints'
apiKey='123456' #请填入专属的api key
apiHeaders={'U-ApiKey':apiKey,'content-type': 'application/json'}
deviceID = 344511
sensorID = {'pm25':411264, 'pm10': 411265,'temperature':411219, 'humidity':411220}



#上传CPU温度到yeelink
def upload_to_yeelink(name, value):
	url= apiUrl % (deviceID,sensorID[name])
	strftime=time.strftime("%Y-%m-%dT%H:%M:%S")
	print(url, strftime)
	data={"timestamp":strftime , "value": value}
	try:
		res=requests.post(url,headers=apiHeaders,data=json.dumps(data))
		if res.status_code!=200:
			print("status_code:",res.status_code)
		else:
			pass
	except:
		print("report to yeelink fail")
	