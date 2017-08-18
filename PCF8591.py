#!/usr/bin/python3
#-*- coding:utf-8 -*-

import time
import smbus
import RPi.GPIO as GPIO

light_level = {0:'刺眼',1:'刺眼',2:'刺眼',3:'刺眼',
				4:'明亮',5:'普通',6:'普通',7:'偏暗',
				8:'昏暗',9:'黑暗',10:'漆黑'}
light_step = 25

class PCF8591(object):
	"""docstring for PCF8591"""
	def __init__(self, i2c_adddr=0x48):
		self.addr = i2c_adddr
		self.bus = smbus.SMBus(1)

	def _read_data(self,i):
		A=[0x40, 0x41, 0x42, 0x43]
		#power=3.3
		self.bus.write_byte(self.addr,A[i])
		value = self.bus.read_byte(self.addr)
		value = self.bus.read_byte(self.addr)
		#print("A%d OUT: %3d, %1.3f, in %1.2fV power-%1.3f " %(i, value,value/255.0, power, value*power/255.0))
		return value

	def get_light_level(self):
		#0-255，越高越黑
		value = self._read_data(1)
		level = light_level[int(value/light_step)]
		return (value, level)

	def get_warm_level(self):
		value = self._read_data(2)
		return value
		
	def __exit__(self):
		self.bus.close()
		GPIO.cleanup()