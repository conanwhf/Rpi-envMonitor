#!/usr/bin/python3
#-*- coding:utf-8 -*-

import sys,time
from RpiState import RpiNetWork
from RpiState import RpiSystem
from AirQuality import AirQuality
#from DHT11 import DHT11
from PCF8591 import PCF8591
from GpioPower import *
import Adafruit_DHT

class sysState:
	def __init__(self):
		self.sys =  RpiSystem()		# 系统信息类
		self.net = RpiNetWork()		# 网络信息类
		self.cpu_t = 0     			# CPU温度
		self.loading = 0			# CPU loading
		self.mem = ""				# 内存信息
		self.disk = ""				# 磁盘使用率
		self.uptime = ""			# 开机时间
		self.ip = "192.168.0.1"		# IP地址
		self.ping = 0				# ping google

class sensorState:
	def __init__(self):
		self.air = AirQuality()		# 空气质量检测传感器类
		#self.dht11 = DHT11(37)		# 温湿度传感器类
		self.dht = 26
		self.pcf = PCF8591()		# 数模转换、光照传感器类
		self.temperature = 0		# 温度
		self.humidity = 0			# 湿度
		self.pm25 = 0				# PM2.5
		self.pm10 = 0				# PM10
		self.light = 0				# 光照强度
		

# 全局变量，定义状态变量
sys = sysState()
sen = sensorState()

power_init_all()
'''
while True:
	print("power ONNNNNNNN")
	set_backlight_power(on=1)
	set_led_power(green=1, yellow=0, red=0)
	time.sleep(5)
	print("power OFFFFFFF")
	set_backlight_power(on=0)
	set_led_power(green=0, yellow=0, red=1)
	time.sleep(5)
'''

'''
set_backlight_power(on=1)
print("背光打开")
time.sleep(20)
set_backlight_power(on=1)
print("背光关闭")
time.sleep(200)
os.exit()
'''
set_backlight_power(on=1)
while True:
	set_led_power(green=1, yellow=0, red=0)
	
	# get info
	set_sensor_power(on=1)
	(sen.pm25, sen.pm10) = sen.air.getData()
	(sen.humidity, sen.temperature) = Adafruit_DHT.read_retry(Adafruit_DHT.DHT22, sen.dht)
	(temp, sen.light) = sen.pcf.get_light_level()
	print("天气： %d℃，湿度%d%%, 空气质量PM2.5=%d, PM10=%d, 照度=%d-%s" %(sen.temperature,sen.humidity,sen.pm25,sen.pm10, temp, sen.light))
	set_sensor_power(on=0)
	print("传感器关闭，等待背光关闭")
	
	set_backlight_power(on=0)
	set_led_power(green=0, yellow=0, red=1)
	time.sleep(5)
	set_led_power(green=0, yellow=1, red=0)
	set_backlight_power(on=1)
	time.sleep(5)


power_deinit_all()


