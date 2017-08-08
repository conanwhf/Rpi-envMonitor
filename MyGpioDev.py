#!/usr/bin/python3
#-*- coding:utf-8 -*-
import RPi.GPIO as GPIO
import time

DHT11_DATA_LEN = 5

class DHT11(object):
    """docstring for DHT11"""
    def __init__(self, datapin=24, powerpin=25):
        GPIO.setmode(GPIO.BCM)
        self.pin = datapin
        self.power = powerpin
        GPIO.setup( self.power , GPIO.OUT)
        count=0

    def _read_data(self):
        self.data=[]
        # reset        
        GPIO.setup( self.pin , GPIO.OUT)
        GPIO.output( self.pin , GPIO.LOW)
        time.sleep(0.03) # 必须大于18ms
        GPIO.setup( self.pin , GPIO.IN)
        count=0
        while GPIO.input( self.pin ) == GPIO.HIGH:
            continue
        while GPIO.input( self.pin ) == GPIO.LOW:
            continue
        # 固定拉高80us，可用来做基准
        while GPIO.input( self.pin ) == GPIO.HIGH:
            count += 1
            continue
        base = count / 2
        # Get data
        while len(self.data)< DHT11_DATA_LEN*8:
            i = 0
            # 检测50us以上的低位
            while GPIO.input( self.pin ) == GPIO.LOW:
                continue
            # 此时电平为高，持续26-28us表示0，否则持续70us表示1
            while GPIO.input( self.pin ) == GPIO.HIGH:
                i += 1
                if i > 100: #防止死循环
                    break
            if i < base:
                self.data.append(0)
            else:
                self.data.append(1)
        #print("DHT11 get data: ", self.data)


    def _cal(self):
        res=[]
        for i in range( DHT11_DATA_LEN ): # 5个数据分别为 湿度（整数，小数）；温度（整数，小数），校验
            res.append(0)
            for j in range(8):
                res[i] += self.data[i*8+j]<<(7-j)
        #print("DHT11 res: ", res)
        if res[0]+res[2]!=res[4]:  # 数据校验
            print("DHT11: data check error!")
            return -1, -1
        else:
        #    print("humidity: %d, temperature: %d C" %(res[0], res[2]))
            return res[0],res[2]

    def get(self):
        for i in range(5):
            self._read_data()
            (h, t)=self._cal()
            if h>0:
                break
            time.sleep(0.2) 
        return h,t
        
    def _power(self,on=1):
        if on==1:
            GPIO.output( self.power, GPIO.HIGH)
        else :
            GPIO.output( self.power, GPIO.LOW )
        return on
            
    def powerOn(self):
        return self._power(1)
        
    def powerOff(self):
        return self._power(0)

    def __exit__(self):
        GPIO.cleanup()





class SoundDetect(object):
    """docstring for sound detect sensor"""
    def __init__(self, datapin=17):
        GPIO.setmode(GPIO.BCM)
        self.pin = datapin
        GPIO.setup( self.pin , GPIO.IN)
    
    def state(self):
        if GPIO.input( self.pin ) == GPIO.HIGH:
            return 1
        else:
            return 0
        
    def __exit__(self):
        GPIO.cleanup()
        
        
class BackLight(object):
    """docstring for backlight"""
    def __init__(self, powerpin=26):
        GPIO.setmode(GPIO.BCM)
        self.power = powerpin
        GPIO.setup( self.power , GPIO.OUT)
    
    def _power(self,on=1):
        if on==1:
            GPIO.output( self.power, GPIO.HIGH)
        else :
            GPIO.output( self.power, GPIO.LOW )
        return on
            
    def powerOn(self):
        return self._power(1)
        
    def powerOff(self):
        return self._power(0)
                  
    def __exit__(self):
        GPIO.cleanup()
    