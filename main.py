#!/usr/bin/python3
#-*- coding:utf-8 -*-

import time
import sys 
import datetime
import _thread
from DataUpdate import *
import tkinter as tk
import tkinter.messagebox
from tkinter import *

'''for test only
mode =2
def setMode(new):
	global mode
	mode = new
	return mode
	
def getMode():
	return mode
'''	
	
#Global
WinSize = '680x400+60+0'	
BgColor = 'grey'
DataFont = 'Helvetica -60 bold'
StaticFont = 'Helvetica -20'	
NormalModeInfo = "日常模式，部分数据停止刷新，点击按钮切换"
SpecialModeInfo = "监控模式，数据每秒刷新，点击按钮切换"


''' Main
'''
if __name__ == "__main__":
	#添加UI窗口
	win = tk.Tk(screenName=":0.0")
	win.title('环境监控系统')
	win.geometry(WinSize)
	win['bg'] = BgColor
	
	class infoTexts:
		def __init__(self):
			self.temperature = 	Label(win,	text="N/A",	font = DataFont)
			self.humidity = 	Label(win,	text="N/A",	font = DataFont)
			self.pm25 = 		Label(win,	text="N/A",	font = DataFont)		
			self.pm10 = 		Label(win, 	text="N/A",	font = DataFont)		
			self.light = 		Label(win,	font = 'Helvetica -32 bold',	text="明亮")
			self.ip = 	Label(win, font = 'Helvetica -24 bold', text="IP地址:0.0.0.0")
			self.ping = Label(win, font = 'Helvetica -24 bold', text="ping回应：N/A")
			self.uptime=Label(win, font = 'Helvetica -20',		text="开机：N/A")
			self.disk = Label(win, font = 'Helvetica -20',		text="磁盘占用：N/A")
			self.sys = 	Label(win, font = 'Helvetica -20',		text="CPU温度 N/A'C,占用率 N/A%\t\t内存使用 N/A%")
	info = infoTexts()

	# do main process first
	_thread.start_new_thread(normal_loop, (info,))
	_thread.start_new_thread(special_loop, (info,))
	
	# static wiget
	switch = Button(win, text = "激活实时模式", bg=BgColor, font = StaticFont, wraplength = 80)
	l1 = Label(win, text="温度：",font = StaticFont)
	l2 = Label(win, text="湿度：",font = StaticFont)
	l3 = Label(win, text="PM2.5：",font = StaticFont)
	l4 = Label(win, text="PM10：",font = StaticFont)	
	l5 = Label(win, text="光照条件：",font = StaticFont)
	l6 = Label(win, text=NormalModeInfo,font = StaticFont, fg='blue')
	
	# 调整布局
	win.columnconfigure(3, weight=1)
	win.grid_rowconfigure(6, weight=1)
	for child in win.winfo_children(): 
		child.grid_configure(padx=5, pady=5)
		child['bg'] = BgColor
	# part1, 传感器数据，大
	l1.grid(				row = 1,column = 0, sticky = E+N)
	info.temperature.grid(	row = 0,column = 1, columnspan = 3, rowspan=2, sticky = W)
	l2.grid(				row = 1,column = 4, sticky = E+N)
	info.humidity.grid(		row = 0,column = 5, columnspan = 3, rowspan=2, sticky = W)
	l3.grid(				row = 3,column = 0, sticky = E+N)
	info.pm25.grid(			row = 2,column = 1, columnspan = 3, rowspan=2, sticky = W)
	l4.grid(				row = 3,column = 4, sticky = E+N)
	info.pm10.grid(			row = 2,column = 5, columnspan = 3, rowspan=2, sticky = W)
	l5.grid(				row = 5,column = 0, sticky = E+N)
	info.light.grid(		row = 4,column = 1, columnspan = 3, rowspan=2, sticky = W)
	switch.grid(			row = 5,column = 5, columnspan = 2, rowspan=3, sticky = E+W+S+N)
	# part2, 系统数据
	l6.grid(				row = 7,column = 0, columnspan = 5)
	info.ip.grid(			row = 8,column = 0, columnspan = 4, sticky = W)
	info.ping.grid(			row = 8,column = 4, columnspan = 3, sticky = W)
	info.disk.grid(			row = 9,column = 0, columnspan = 4, sticky = W)
	info.uptime.grid(		row = 9,column = 4, columnspan = 3, sticky = W)
	info.sys.grid(			row = 10,column = 0, columnspan = 8, sticky = W)
	
	# Callback函数
	def buttonListener(event):
		print("切换监控模式")
		if getMode() ==1: #之前激活状态，现在关闭
			setMode(2)
			l6['text']=NormalModeInfo
			switch['text'] = "激活实时模式"
		else: 			 #之前日常状态，现在激活
			setMode(1)
			l6['text']=SpecialModeInfo
			switch['text'] = "关闭实时模式"
		#tk.messagebox.showinfo("messagebox","mode=%d"%mode)
	def eventListener(event):
		print("eventListener, %s" %event)
		resetBacklightTimer()
	def closeWindow():
		if tkinter.messagebox.askokcancel("退出", "确认退出?"):
			setMode(0)
			time.sleep(2)
			win.destroy()

	# 注册callback
	switch.bind("<ButtonRelease-1>",buttonListener)
	win.bind("<Button-1>",eventListener)
	win.bind("<FocusIn>",eventListener)
	win.bind("<FocusOut>",eventListener)
	win.protocol('WM_DELETE_WINDOW', closeWindow)
	
	win.mainloop()
