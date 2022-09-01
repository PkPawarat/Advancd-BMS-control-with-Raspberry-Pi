# -*- coding:utf-8 -*-
"""
  *@file get_data.ino
  *@brief Read ambient temperature and relative humidity and print them to serial port.
  *@copyright  Copyright (c) 2010 DFRobot Co.Ltd (http://www.dfrobot.com)
  *@licence     The MIT License (MIT)
  *@author [fengli](li.feng@dfrobot.com)
  *@version  V1.0
  *@date  2020-12-02
  *@get from https://www.dfrobot.com
  *@https://github.com/DFRobot/DFRobot_DHT20
"""
import sys
import time
sys.path.append("../")
from DFRobot_DHT20 import *
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setup(16, GPIO.OUT)

IIC_MODE         = 0x01            # default use IIC1
IIC_ADDRESS      = 0x38           # default i2c device address

dht20 = DFRobot_DHT20(IIC_MODE ,IIC_ADDRESS)
dht20.begin()

target_humid = 50
output_sate = "On"

while True:
	try:
		temp = dht20.get_temperature()
		humid = dht20.get_humidity()
	except:
		print("Had trouble grabbing the humidity data, trying again...")
	
	
	if humid < 50:
		output_sate = "On"
		GPIO.output(16,True)
	if humid > 50:
		output_sate = "Off"
		GPIO.output(16,False)
	
	#get current time
        now = time.localtime()
        hour = now.tm_hour
        minute = now.tm_min
        day = now.tm_mday
        month = now.tm_mon
        year = now.tm_year
	
		
	
	print("{}/{}/{} - {}:{} | Temperature {:.1f} C | Humidity {:.1f} % RH | Output State {}".format(day, month, year, hour, minute, temp, humid, output_sate))
	

	
	time.sleep(1)

