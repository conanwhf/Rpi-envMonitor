#!/usr/bin/python3
#-*- coding:utf-8 -*-

import time
import sys 
import datetime
import _thread
from MyDataUpdate import *

''' Main
'''
if __name__ == "__main__":
	special_loop
	# do main process
	_thread.start_new_thread(normal_loop, ())
	_thread.start_new_thread(special_loop, ())
	while True:
		mode = 1
		time.sleep(60)
		mode = 2
		time.sleep(2000)



'''
count = 0 
sys=RpiSystem()
net=RpiNetWork()
air=AirQuality()
dht11=DHT11(24)
sound=SoundDetect(17)


while True:
	#print sys.uptime()
	count += 1
	#TODO: 温度，湿度，气压， PM2.5, PM10, 噪音，CPU，内存 
	(pm25,pm10) = air.getData()
	(humidity, temperature) = dht11.get()
	tooNoise = sound.state()
	
	#(upload,download) = net.net_stat()
	(mem_use, mem_total, mem_per)=sys.memory_stat()
	cpu_t = sys.cpu_temp()
	loading = sys.cpu_load()
	print("天气： %d'C，湿度%d%%" %(temperature,humidity))
	print("环境： 空气质量PM2.5=%d, PM10=%d, 有噪音吗-%d" %(pm25,pm10,tooNoise))
	print("系统： CPU温度%.1f'C，占用率%.1f%%，内存使用 %d%%" %(cpu_t, loading, mem_per))
	if count>=60: # 1Hour
		count = 0
		#TODO: 外网IP, 照度，天气预报
		ip = net.public_ip()
		print("外网IP地址：%s" %(ip))
		print("磁盘使用：%s" %sys.disk_stat())
	time.sleep(60)

'''