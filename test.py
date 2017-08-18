#!/usr/bin/python3
#-*- coding:utf-8 -*-

import sys,time
from RpiState import RpiNetWork
from RpiState import RpiSystem
from AirQuality import AirQuality
from DHT11 import DHT11
from PCF8591 import PCF8591
from GpioPower import *

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
		self.dht11 = DHT11(23)		# 温湿度传感器类
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

# power on devices
set_sensor_power(on=1)
set_backlight_power(on=1)
set_led_power(green=1, yellow=0, red=1)
# get info
(sen.pm25, sen.pm10) = sen.air.getData()
(sen.humidity, sen.temperature) = sen.dht11.get()
(temp, sen.light) = sen.pcf.get_light_level()
print("天气： %d℃，湿度%d%%, 空气质量PM2.5=%d, PM10=%d, 照度=%d-%s" %(sen.temperature,sen.humidity,sen.pm25,sen.pm10, temp, sen.light))

time.sleep(5)

set_sensor_power(on=0)
set_led_power(green=0, yellow=1, red=0)
time.sleep(2)
set_backlight_power(on=0)
power_deinit_all()


