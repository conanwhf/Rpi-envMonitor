#!/usr/bin/python3
#-*- coding:utf-8 -*-

import sys
import os
import time
import socket 
import struct 
import fcntl 
import random,re
from urllib import request


def _file_output(arg, line=0):
    f = open(arg)
    res = f.readlines()
    f.close()
    if line==-1:#需要全部数据
        return res
    else:
        return res[line]
    #return res

def _cmd_output(args, line=0):
    f = os.popen(args)  
    res = f.readlines()  
    f.close()
    if line==-1:#需要全部数据
        return res
    else:
        return res[line]
        

######################################################################################

class RpiNetWork(object):
    def __init__(self):
        pass

    def public_ip(self):
        ip_regex = re.compile("(([0-9]{1,3}\.){3}[0-9]{1,3})")
        # List of host which return the public IP address:
        hosts = """http://www.whatismyip.com/
            http://adresseip.com
            http://www.aboutmyip.com/
            http://www.ipchicken.com/
            http://www.showmyip.com/
            http://monip.net/
            http://checkrealip.com/
            http://ipcheck.rehbein.net/
            http://checkmyip.com/
            http://www.raffar.com/checkip/
            http://www.thisip.org/
            http://www.lawrencegoetz.com/programs/ipinfo/
            http://www.mantacore.se/whoami/
            http://www.edpsciences.org/htbin/ipaddress
            http://mwburden.com/cgi-bin/getipaddr
            http://checkipaddress.com/
            http://www.glowhost.com/support/your.ip.php
            http://www.tanziars.com/
            http://www.naumann-net.org/
            http://www.godwiz.com/
            http://checkip.eurodyndns.org/""".split("\n")
        for i in hosts:
            host = i.strip()
            print(host)
            try:
                response = request.urlopen(host).read()
                result = ip_regex.findall(response.decode('utf-8'))
                if result: 
                    return result[0][0]
            except:
                pass
        return ""


    def local_ip(self, ethname='eth0'): 
    	s=socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 
    	return socket.inet_ntoa(fcntl.ioctl(s.fileno(), 0X8915, struct.pack('256s', ethname[:15]))[20:24]) 


    def net_stat(self):
        #选择eth0数据，第四行
        data1 = _file_output("/proc/net/dev", 3)
        time.sleep(1)
        data2 = _file_output("/proc/net/dev", 3)
        before = data1.split()
        after = data2.split()
        down = int(after[1])-int(before[1])
        up = int(after[9])-int(before[9])
        return float(up)/1024.0, float(down)/1024.0
        
    def ping(self):
        data = _cmd_output("ping google.com -c 1", -1)
        try:
            res = data[5].split('/')[5]
            res = res.rjust(9)
            return ("%sms" %res)
        except:
            res = "Timeout"
            return res

    def __exit__(self):
        pass
    
######################################################################################


class RpiSystem(object):
    def __init__(self):
        pass

    def cpu_temp(self):
        cpu_temp = _file_output("/sys/class/thermal/thermal_zone0/temp")
        return float(cpu_temp)/1000

    def disk_stat(self):
        #根据树莓派系统，选择/dev/root，第2行
        data = _cmd_output("df -h", 1)
        info = data.split()
        # 0-Filesystem 1-Size  2-Used 3-Avail 4-Use% 5-Mounted on
        return "已使用%s，可用空间%s"%(info[4], info[3])
        

    def uptime(self):
        uptime = {}
        all_sec = float(_file_output("/proc/uptime").split()[0])
        MINUTE,HOUR,DAY = 60,3600,86400
        uptime['day'] = int(all_sec / DAY )
        uptime['hour'] = int((all_sec % DAY) / HOUR)
        uptime['minute'] = int((all_sec % HOUR) / MINUTE)
        uptime['second'] = int(all_sec % MINUTE)
        print("%d天%d小时%d分%d秒" %(uptime['day'],uptime['hour'],uptime['minute'],uptime['second']))
        return "%d天%d小时"%(uptime['day'],uptime['hour'])

    def cpu_load(self):
        loading = _cmd_output("top -n1 | awk '/Cpu\(s\):/ {print $2}'")
        return float(loading)

    def memory_stat(self):
        mem = {}
        lines = _file_output("/proc/meminfo", -1)
        for line in lines:
            if len(line) < 2: continue
            name = line.split(':')[0]
            var = line.split(':')[1].split()[0]
            # 单位：MB
            mem[name] = int(var)/1000 
        mem['MemUsed'] = mem['MemTotal'] - mem['MemFree'] - mem['Buffers'] - mem['Cached']
        return int(mem['MemUsed']), int(mem['MemTotal']), int(mem['MemUsed']*100/mem['MemTotal'])

    def __exit__(self):
        pass
