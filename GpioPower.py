#!/usr/bin/python3
#-*- coding:utf-8 -*-
import RPi.GPIO as GPIO

sensor_pins={'air':12,'dht':35,'pcf':7}
led_pins={'green':40,'yellow':38,'red':36}
bl_pin=23

def _GPIO_Power_Regist(pins):
    GPIO.setmode(GPIO.BOARD)
    GPIO.setwarnings(False)
    GPIO.setup( pins , GPIO.OUT)
    return
    
def _GPIO_Power_UnRegist(pins):
    GPIO.cleanup(pins)
    return
    
def _GPIO_Power_Set(pins, on):
    if on==1:
        GPIO.output( pins, GPIO.HIGH)
    else :
        GPIO.output( pins, GPIO.LOW )
    return

#=====================================
def power_init_all():
    _GPIO_Power_Regist(list(sensor_pins.values()))
    _GPIO_Power_Regist(list(led_pins.values()))
    _GPIO_Power_Regist(bl_pin)
    return
    
def power_deinit_all():
    _GPIO_Power_UnRegist(list(sensor_pins.values()))
    _GPIO_Power_UnRegist(list(led_pins.values()))
    #_GPIO_Power_UnRegist(bl_pin)
    return
    
def set_led_power(green, yellow, red):
    _GPIO_Power_Set(led_pins['green'], green)
    _GPIO_Power_Set(led_pins['yellow'], yellow)
    _GPIO_Power_Set(led_pins['red'], red)
    return
    
def set_backlight_power(on):  
    _GPIO_Power_Set(bl_pin, on)
    return

def set_sensor_power(on):
    _GPIO_Power_Set(list(sensor_pins.values()), on)
    return
    