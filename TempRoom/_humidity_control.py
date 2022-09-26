# -*- coding:utf-8 -*-
"""

"""
import sys
import time
import csv
import os
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
filename = "humid_log_cyclic.csv"

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
	
	
	
	
	
	# Check if file exists and wrtite data with/without header
	if os.path.isfile(filename):
			#log data without header
		with open(filename, 'a') as log:
			writer = csv.writer(log)
			# record data to csv file
			data = [str(day)+"/"+str(month)+"/"+str(year), str(hour)+":"+ str(minute), "{:.2f}".format(temp), "{:.2f}".format(humid)]
			writer.writerow(data)
			
			# close the log file
			log.close()
	else:
			#log data with header
		with open(filename, 'a') as log:
			writer = csv.writer(log)
			# record data to csv file
			header = ['Date', 'Time', 'Temp', 'Humidity']
			writer.writerow(header)
			data = [str(day)+"/"+str(month)+"/"+str(year), str(hour)+":"+ str(minute), "{:.2f}".format(temp), "{:.2f}".format(humid)]
			writer.writerow(data)
			
			# close the log file
			log.close()

	
	print("{}/{}/{} - {}:{} | Temperature {:.2f} C | Humidity {:.2f} % RH | Output State {}".format(day, month, year, hour, minute, temp, humid, output_sate))
	

	
	time.sleep(30)