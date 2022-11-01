#!/usr/bin/python
# -*- coding:utf-8 -*-
import serial
import os
import sys
import logging
import binascii
import time
import csv

## setup Modbus communcation hat
logging.basicConfig(level=logging.INFO)
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)   
import RPi.GPIO as GPIO
from waveshare_2_CH_RS485_HAT import config
TXDEN_1 = 27                                            #AC connecting board at RPI pin 27
ser = config.config(dev = "/dev/ttySC0")

## Command dictionary
command = {
        'ON': b'\x01\x06\x00\x01\x00\x01\x19\xCA',	#work
        'OFF': b'\x01\x06\x00\x01\x00\x00\xD8\x0A',	#work
        'LOW': b'\x01\x06\x00\x04\x00\x01\x09\xCB',
        'MEDIUM': b'\x01\x06\x00\x04\x00\x02\x49\xCA',
        'HIGH': b'\x01\x06\x00\x04\x00\x03\x88\x0A',
        'STANDARD': b'\x01\x06\x00\x69\x00\x00\x59\xD6',
        'CONTINUOUS': b'\x01\x06\x00\x69\x00\x01\x98\x16',
        'HEAT ONLY': b'\x01\x06\x00\x65\x00\x01\x58\x15',
        'COOL ONLY': b'\x01\x06\x00\x65\x00\x02\x18\x14',
        'AUTO CHANGEOVER': b'\x01\x06\x00\x65\x00\x03\xD9\xD4',
        'FAN ONLY': b'\x01\x06\x00\x65\x00\x04\x98\x16',
        'ROOM TEMP' : b'\x01\x03\x03\x53\x00\x01\x74\x5F',               #sensoring temp inside
        'OUTSIDE TEMP' : b'\x01\x03\x03\x54\x00\x01\xC5\x9E'             #sensoring temp outside
      }


#arr2 = bytearray(command['ON'],'ascii')
#for byte in arr2:
#    print(byte)
#print(arr2)    
########## AC start up code
#AC STATE: ON, OFF


GPIO.output(TXDEN_1, GPIO.LOW)
time.sleep(0.5)
ser.Uart_SendHex(command['OFF'])
time.sleep(0.5)#Allow time for the message to be sent



while(1):
	GPIO.output(TXDEN_1, GPIO.LOW) 
	ser.Uart_SendHex(command['ROOM TEMP'])
	time.sleep(0.0025)#Waiting to send
	GPIO.output(TXDEN_1, GPIO.HIGH) #set to receive mode
	s = ser.Uart_ReceiveHex(7) 
	hex_string = binascii.hexlify(s)
	temp_string = hex_string[6:10]
	if(len(temp_string) == 4):
			room_temp_test = (int(temp_string, 16))/10.0
			if(room_temp_test < 40.0):
					print(room_temp_test)
                        

