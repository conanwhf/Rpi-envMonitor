#!/usr/bin/python3
#-*- coding:utf-8 -*-

import time
import smbus
import RPi.GPIO as GPIO

# Operating Modes
BMP180_ULTRALOWPOWER     = 0
BMP180_STANDARD          = 1
BMP180_HIGHRES           = 2
BMP180_ULTRAHIGHRES      = 3
# BMP085 Registers
BMP180_CAL_REGS_START    = 0xAA
BMP180_CAL_REGS_COUNT    = 11
BMP180_CONTROL_ADDR      = 0xF4
BMP180_RAWDATA_ADDR      = 0xF6
# Commands
BMP180_READ_TEMPCMD      = 0x2E
BMP180_READ_PRESSURECMD  = 0x34
#便于对应spec，留出ac[0] & b[0] 不用
BMP180_CAL_DEF  = -32767
bmp180_ac   = [BMP180_CAL_DEF, 8153,-1069,-14370,33272,26213,13876]      # AC1-AC6
bmp180_b    = [BMP180_CAL_DEF, 6515,37, BMP180_CAL_DEF,BMP180_CAL_DEF,BMP180_CAL_DEF,BMP180_CAL_DEF,BMP180_CAL_DEF]    # B1-B7
bmp180_x    = [BMP180_CAL_DEF, BMP180_CAL_DEF,BMP180_CAL_DEF,BMP180_CAL_DEF]            # X1-X3
bmp180_mb   = -32768
bmp180_mc   = -11786
bmp180_md   = 2081

class BMP180(object):
    """docstring for BMP180"""
    def __init__(self, i2c_adddr=0x77):
        self.addr = i2c_adddr
        self.bus = smbus.SMBus(1)
        self._load_calibration()

    def _read(self, cmd):
        return self.bus.read_byte_data(self.addr, cmd)

    def _write(self, cmd, val):
        return self.bus.write_byte_data(self.addr, cmd, val)

    def _load_calibration(self):
        cal=[]
        for i in range(0,BMP180_CAL_REGS_COUNT):
            MSB = self._read(BMP180_CAL_REGS_START+i*2)
            LSB = self._read(BMP180_CAL_REGS_START+i*2+1)
            value = (MSB << 8) + LSB
            if i in {0, 1, 2, 6, 7, 8, 9, 10}:# signed short
                if value > 32767:value -= 65536
            cal.append(value)
        # fill the regs
        for i in range(1,6):
            bmp180_ac[i]=cal[i-1]
        bmp180_b[1] = cal[6]
        bmp180_b[2] = cal[7]
        bmp180_mb = cal[8]
        bmp180_mc = cal[9]
        bmp180_md = cal[10]
        #print(bmp180_ac, bmp180_b)


    def get_temperature(self):
        # for temperature
        self._write(BMP180_CONTROL_ADDR, BMP180_READ_TEMPCMD)
        time.sleep(0.005)  # Wait 4.5(in fact is 5)ms
        MSB = self._read(BMP180_RAWDATA_ADDR)
        LSB = self._read(BMP180_RAWDATA_ADDR+1)
        ut = (MSB << 8) + LSB
        # Calculate it
        bmp180_x[1] = ((ut-bmp180_ac[6])*bmp180_ac[5])>>15
        bmp180_x[2] = (bmp180_mc <<11) / (bmp180_x[1]+bmp180_md)
        bmp180_b[5] = bmp180_x[1] + bmp180_x[2]
        self.temperature = float( ((bmp180_b[5]+8) >>4)/10.0 )
        #print("IN temp: ut=%d, x1=%d, x2=%d, b5=%d, t=%d " %( ut, bmp180_x[1], bmp180_x[2], bmp180_b[5], t))
        return self.temperature


    def get_pressure(self, oss=BMP180_STANDARD):
        if bmp180_b[5]==BMP180_CAL_DEF:  #没有调用温度计算过
            self.get_temperature()
        # for pressure
        self._write(BMP180_CONTROL_ADDR, BMP180_READ_PRESSURECMD + (oss << 6))
        if oss == BMP180_ULTRALOWPOWER:
            time.sleep(0.005)
        elif oss == BMP180_STANDARD:
            time.sleep(0.008)
        elif oss == BMP180_HIGHRES:
            time.sleep(0.014)
        elif oss == BMP180_ULTRAHIGHRES:
            time.sleep(0.026)
        else:
            print("BMP180: error input for pressure oss")
        MSB = self._read(BMP180_RAWDATA_ADDR)
        LSB = self._read(BMP180_RAWDATA_ADDR+1)
        XLSB = self._read(BMP180_RAWDATA_ADDR+2)
        up = ((MSB << 16) + (LSB << 8) + XLSB) >> (8 - oss)

        # Calculate it
        bmp180_b[6] = bmp180_b[5]-4000
        temp = bmp180_b[6]*bmp180_b[6]>>12
        bmp180_x[1] = (bmp180_b[2] * temp ) >> 11
        bmp180_x[2] = (bmp180_ac[2] * bmp180_b[6]) >> 11
        bmp180_x[3] = bmp180_x[1]+bmp180_x[2]
        bmp180_b[3] = (((bmp180_ac[1]*4 + bmp180_x[3])<<oss) +2) /4
     
        bmp180_x[1] = (bmp180_ac[3] * bmp180_b[6]) >> 13
        bmp180_x[2] = (bmp180_b[1] * temp ) >> 16
        bmp180_x[3] = (bmp180_x[1]+bmp180_x[2] +2 )>>2
        bmp180_b[4] = (bmp180_ac[4]* (bmp180_x[3]+32768)) >> 15
        bmp180_b[7] = (up - bmp180_b[3]) * (50000>>oss)

        if bmp180_b[7] < 0x80000000:
            p = bmp180_b[7]*2/bmp180_b[4]
        else:
            p = bmp180_b[7]/bmp180_b[4]*2
        bmp180_x[1] = (p>>8) * (p>>8)
        bmp180_x[1] = (bmp180_x[1]*3038) >>16
        bmp180_x[2] = (-7357*p) >>16
        self.pressure = p + ((bmp180_x[1] + bmp180_x[2] + 3791) >> 4)

        return self.pressure


    def get_altitude(self, sealevel_pa=101325.0):
        self.get_pressure()#重新计算气压
        self.altitude = 44330.0 * (1.0 - pow(self.pressure / sealevel_pa, (1.0/5.255)))
        return self.altitude

    def cal_sealevel_pressure(self, altitude=0.0):
        p0 = self.pressure / pow(1.0 - altitude/44330.0, 5.255)
        return p0

    def __exit__(self):
        self.bus.close()

###############################################################################

class PCF8591(object):
    """docstring for PCF8591"""
    def __init__(self, i2c_adddr=0x48, powerpin=4):
        self.addr = i2c_adddr
        self.bus = smbus.SMBus(1)
        GPIO.setmode(GPIO.BCM)
        self.power = powerpin
        GPIO.setup( self.power , GPIO.OUT)

    def _read_data(self,i):
        A=[0x40, 0x41, 0x42, 0x43]
        #power=3.3
        self.bus.write_byte(self.addr,A[i])
        value = self.bus.read_byte(self.addr)
        value = self.bus.read_byte(self.addr)
        #print("A%d OUT: %3d, %1.3f, in %1.2fV power-%1.3f " %(i, value,value/255.0, power, value*power/255.0))
        return value

    def get_light_level(self):
        value = self._read_data(1)
        #0-255，越高越黑
        return value

    def get_warm_level(self):
        value = self._read_data(2)
        return value
        
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
        self.bus.close()
        GPIO.cleanup()