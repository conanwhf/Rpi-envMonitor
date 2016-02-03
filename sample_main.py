#-*- coding:utf-8 -*-
import MySQLdb
import commands
import sys
import os
import RPi.GPIO as gpio
import time
import sys 
import datetime
import time
from BMP180 import BMP180



def mysqlwriteth():
    (thid,temp,hum)=th11()
    (cputemp)=get_cpu_temp()
    (bmp180temp,bmp180pre,bmp180alt)=bmp180()
    (csb)=0.5
    conn= MySQLdb.connect(
            host='localhost',
            port = 3306,
            user='root',
            passwd='数据库密码',
            db ='hj',
            )
    cur = conn.cursor()
    timestamp=time.time()
    sqli="update data set timestamp='%s',thid='%s', temp='%s', hum='%s',cputemp='%s',bmp180temp='%s',bmp180pre='%s',csb='%s'"
    cur.execute(sqli,(timestamp,thid,temp,hum,cputemp,bmp180temp,bmp180pre,csb))

    cur.close()
    conn.commit()
    conn.close()
#    print thid,temp,hum,cputemp,bmp180temp,bmp180pre,csb,gettime()


def mysqlwritevps():
    (thid,temp,hum)=th11()
    (cputemp)=get_cpu_temp()
    (bmp180temp,bmp180pre,bmp180alt)=bmp180()
    (csb)=0.5
    conn= MySQLdb.connect(
            host='104.251.228.19',
            port = 3306,
            user='root',
            passwd='数据库密码',
            db ='hj',
            )
    cur = conn.cursor()
    print bmp180temp,temp,hum
    timestamp=time.time()
    sqli="update data set timestamp='%s',thid='%s', temp='%s', hum='%s',cputemp='%s',bmp180temp='%s',bmp180pre='%s',csb='%s'"
    cur.execute(sqli,(timestamp,thid,temp,hum,cputemp,bmp180temp,bmp180pre,csb))

    cur.close()
    conn.commit()
    conn.close()
#    print thid,temp,hum,cputemp,bmp180temp,bmp180pre,csb,gettime()

while True :
    mysqlwriteth()
#    print 'OK'
#    mysqlwritevps()
    time.sleep(1)
