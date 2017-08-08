#!/usr/bin/python3
#-*- coding:utf-8 -*-

import time
import sys 
import datetime
import _thread
from MyDataUpdate import *
import tkinter as tk
import tkinter.messagebox 
from tkinter import *




def getButtonTitle():
	if getMode() ==2: #当前关闭，等待激活
		return "激活实时监控"
	else:
		return "关闭实时监控"


''' Main
'''
if __name__ == "__main__":
	#添加UI窗口
	win = tk.Tk(screenName=":0.0")
	win.title('环境监控系统')
	win.geometry('800x400')
	
	def buttonListener(event):
		print("切换监控模式")
		if getMode() ==1: #当前激活，需关闭
			setMode(2)
		else: 
			setMode(1)
		switch['text'] = getButtonTitle()
		#tk.messagebox.showinfo("messagebox","mode=%d"%mode)
		
	class infoTexts:
		def __init__(self):
			self.temperature = Label(win, text="温度：30",font = 'Helvetica -32 bold')		# 温度
			self.humidity = Label(win, text="湿度：30",font = 'Helvetica -32 bold')		# 湿度
			self.pm25 = Label(win, text="PM2.5: 100",font = 'Helvetica -32 bold')				# PM2.5
			self.pm10 = Label(win, text="PM10: 100",font = 'Helvetica -32 bold')				# PM10
			self.light = Label(win, text="光照条件：明亮",font = 'Helvetica -24 bold')				# 光照强度
			self.sys = Label(win, text="日常模式，点击按钮切换到实时监控模式hghfgdghfsgdfsgdfs",font = 'Helvetica -20')
			self.uptime = Label(win, text="开机运行时间：1天",font = 'Helvetica -20')
			self.ip = Label(win, text="IP地址:0.0.0.0",font = 'Helvetica -20')	
			self.disk = Label(win, text="磁盘占用：XXXfdasfdsafadsadfsadfsXXXX",font = 'Helvetica -20')

	info = infoTexts()

	# do main process first
	_thread.start_new_thread(normal_loop, (info,))
	_thread.start_new_thread(special_loop, (info,))
	
	
	switch = Button(win, text = getButtonTitle())  
	#switch.pack(expand=1, fill="both")
	switch.bind("<ButtonRelease-1>",buttonListener)
	
	# 调整布局
	win.columnconfigure(0, weight=1)
	#win.rowconfigure(0, weight=1)
	info.temperature.grid(	row = 0,column = 0, padx = 5,pady = 5)
	info.humidity.grid(		row = 0,column = 1, padx = 5,pady = 5)
	info.pm25.grid(			row = 1,column = 0, padx = 5,pady = 5)
	info.pm10.grid(			row = 1,column = 1, padx = 5,pady = 5)	
	info.light.grid(		row = 2,column = 0, padx = 5,pady = 5)
	switch.grid(			row = 2,column = 1, padx = 5,pady = 5)		
	info.sys.grid(			row = 3,column = 1, padx = 5,pady = 5)
	info.uptime.grid(		row = 4,column = 0, padx = 5,pady = 5)	
	info.ip.grid(			row = 4,column = 1, padx = 5,pady = 5)	
	info.disk.grid(			row = 5,column = 1, padx = 5,pady = 5)	
	
	win.mainloop()
	
'''	while True:
		mode = 1
		time.sleep(60)
		mode = 2
		time.sleep(2000)

'''