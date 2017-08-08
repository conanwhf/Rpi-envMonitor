#!/usr/bin/python3
#-*- coding:utf-8 -*-

import sqlite3
import time
import sys 
import datetime
from MyRpiState import RpiNetWork
from MyRpiState import RpiSystem
from MyAirQuality import AirQuality
from MyGpioDev import DHT11
from MyGpioDev import BackLight
from MyI2cDev import PCF8591

class sysState:
	def __init__(self):
		self.sys =  RpiSystem()		# 系统信息类
		self.net = RpiNetWork()		# 网络信息类
		self.cpu_t = 0     			# CPU温度
		self.loading = 0			# CPU loading
		self.mem = ""				# 内存信息
		self.disk = ""				# 磁盘使用率
		self.uptime = ""			# 开机时间
		self.IP = "192.168.0.1"		# IP地址
		self.ping = 0				# ping google

class sensorState:
	def __init__(self):
		self.air = AirQuality(18)		# 空气质量检测传感器类
		self.dht11 = DHT11(24,25)		# 温湿度传感器类
		self.bl = BackLight(26)		# 背光类
		self.pcf = PCF8591(4)		# 数模转换、光照传感器类
		self.temperature = 0		# 温度
		self.humidity = 0			# 湿度
		self.pm25 = 0				# PM2.5
		self.pm10 = 0				# PM10
		self.light = 0				# 光照强度
		

# 全局变量，定义状态变量
sys = sysState()
sen = sensorState()
mode = 2	# 0-静止状态（什么都不做），1-激活状态，2-日常状态

def normal_loop():
	while mode > 0:
		sys.uptime = sys.sys.uptime()
		sys.IP = sys.net.public_ip()
		print("开机时间：%s， IP地址:%s" %(sys.uptime,sys.IP))
		time.sleep(3000) #30min
	print("normal loop stopped")
	
	
def special_loop():
	while mode > 0:
		print('mode=%d' %mode)
		# power on devices
		#sen.air.power(1)
		sen.dht11.power(1)
		#sen.pcf.power(1)
		
		# get info
		(sen.pm25, sen.pm10) = sen.air.getData()
		(sen.humidity, sen.temperature) = sen.dht11.get()
		sys.disk = sys.sys.disk_stat()
		print("天气： %d℃，湿度%d%%, 空气质量PM2.5=%d, PM10=%d" %(sen.temperature,sen.humidity,sen.pm25,sen.pm10))
		print("磁盘使用：%s" %sys.disk)
		if mode==1:		# 激活状态
			(_, _, sys.mem)=sys.sys.memory_stat()
			sys.cpu_t = sys.sys.cpu_temp()
			sys.loading = sys.sys.cpu_load()
			sys.ping = sys.net.ping()
			print("系统： CPU温度%.1f'C，占用率%.1f%%，内存使用 %d%%, ping回应：%.2fms" %(sys.cpu_t, sys.loading, sys.mem, sys.ping))
		
		#休眠
		if mode==1:
			time.sleep(1)	# 1s
		else:
			time.sleep(600)	#10min
	
	print("special loop stopped")

