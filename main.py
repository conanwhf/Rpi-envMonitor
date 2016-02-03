#!/usr/bin/python
# -*- coding: utf-8 -*-
import sqlite3
import commands
import time
import sys 
import datetime
from MyRpiState import RpiNetWork
from MyRpiState import RpiSystem
from MyAirQuality import AirQuality
from MyGpioDev import DHT11
from MyI2cDev import BMP180
from MyI2cDev import PCF8591

count = 0 
sys=RpiSystem()
net=RpiNetWork()
air=AirQuality()
dht11=DHT11()
bmp=BMP180()
pcf=PCF8591()

while True:
	#print sys.uptime()
	count += 1
	#TODO: 温度，湿度，气压， PM2.5, PM10, 噪音，CPU，内存 
	cpu_t=sys.cpu_temp()
	loading=sys.cpu_load()
	(pm25,pm10)=air.getData()
	(humidity, temperature)=dht11.get()
	pressure = bmp.get_pressure()
	light = 255-pcf.get_sunshine_level()
	noise = pcf.get_noise_level()
	(upload,download) = net.net_stat()
	(mem_use, mem_total, mem_per)=sys.memory_stat()
	print "天气： %d'C，湿度%d%%，气压%dL" %(temperature,humidity,pressure)
	print "环境： 空气质量PM2.5=%d, PM10=%d, 光照强度%d, 噪音%d" %(pm25,pm10,light,noise)
	print "系统： CPU温度%.1f'C，占用率%.1f%%，内存使用 %d%%, 网络上传%.2fKB/s，下载%.2fKB/s" %(cpu_t, loading, mem_per, upload, download)
	if count>=60: # 1Hour
		count = 0
		#TODO: 外网IP, 照度，天气预报
		ip = net.public_ip()
		print "外网IP地址：%s" %(ip)
		print "磁盘使用：%s" %sys.disk_stat()
	time.sleep(60)

	