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
TXDEN_1 = 27
ser = config.config(dev = "/dev/ttySC0")


#give the outside temp reading a initial value
outside_temp = 21.0
room_temp = 21.0
set_temp = 21.0 #only use increments of 0.5C between 18C and 30C


## Temp hex code dictionary
temp_hex = {
        18.0: '\x01\x06\x00\x66\x00\xB4\x69\xA2',             #convert dicimal to hex by 18.0 degree to 180 (dicimal) to 00B4 (hex)
        18.5: '\x01\x06\x00\x66\x00\xB9\xA8\x67',
        19.0: '\x01\x06\x00\x66\x00\xBE\xE9\xA5',
        19.5: '\x01\x06\x00\x66\x00\xC3\x29\x84',
        20.0: '\x01\x06\x00\x66\x00\xC8\x68\x43',
        20.5: '\x01\x06\x00\x66\x00\xCD\xA8\x40',
        21.0: '\x01\x06\x00\x66\x00\xD2\xE9\x88',
        21.5: '\x01\x06\x00\x66\x00\xD7\x29\x8B',
        22.0: '\x01\x06\x00\x66\x00\xDC\x68\x4C',
        22.5: '\x01\x06\x00\x66\x00\xE1\xA9\x9D',
        23.0: "\x01\x06\x00\x66\x00\xE6\xE8\x5F",
        23.5: '\x01\x06\x00\x66\x00\xEB\x29\x9A',
        24.0: '\x01\x06\x00\x66\x00\xF0\x69\x91',
        24.5: '\x01\x06\x00\x66\x00\xF5\xA9\x92',
        25.0: '\x01\x06\x00\x66\x00\xFA\xE9\x96',
        25.5: '\x01\x06\x00\x66\x00\xFF\x29\x95',
        26.0: '\x01\x06\x00\x66\x01\x04\x69\x86',
        26.5: '\x01\x06\x00\x66\x01\x09\xA8\x43',
        27.0: '\x01\x06\x00\x66\x01\x0E\xE9\x81',
        27.5: '\x01\x06\x00\x66\x01\x13\x29\x88',
        28.0: '\x01\x06\x00\x66\x01\x18\x68\x4F',
        28.5: '\x01\x06\x00\x66\x01\x1D\xA8\x4C',
        29.0: '\x01\x06\x00\x66\x01\x22\xE8\x5C',
        29.5: '\x01\x06\x00\x66\x01\x27\x28\x5F',
        30.0: '\x01\x06\x00\x66\x01\x2C\x69\x98'
      }

## Command dictionary   
command = {                      #board         Modbut register  Hex           CRC
        'ON':                   '\x01\x06\x00   \x01            \x00\x01       \x19\xCA',
        'OFF':                  '\x01\x06\x00   \x01            \x00\x00       \xD8\x0A',

        'LOW':                  '\x01\x06\x00   \x04            \x00\x01       \x09\xCB',
        'MEDIUM':               '\x01\x06\x00   \x04            \x00\x02       \x49\xCA',
        'HIGH':                 '\x01\x06\x00   \x04            \x00\x03       \x88\x0A',

        'STANDARD':             '\x01\x06\x00   \x69            \x00\x00       \x59\xD6',
        'CONTINUOUS':           '\x01\x06\x00   \x69            \x00\x01       \x98\x16',

        'HEAT ONLY':            '\x01\x06\x00   \x65            \x00\x01       \x58\x15',
        'COOL ONLY':            '\x01\x06\x00   \x65            \x00\x02       \x18\x14',
        'AUTO CHANGEOVER':      '\x01\x06\x00   \x65            \x00\x03       \xD9\xD4',
        'FAN ONLY':             '\x01\x06\x00   \x65            \x00\x04       \x98\x16',
        
        'ROOM TEMP' :           '\x01\x03\x03\x53       \x00\x01\x74\x5F',
        'OUTSIDE TEMP' :        '\x01\x03\x03\x54       \x00\x01\xC5\x9E'
      }



## AC start up code
                                #GPIO.LOW mean commanding mode,  GPIO.HIGH = receiving data
#AC STATE: ON, OFF
GPIO.output(TXDEN_1, GPIO.LOW) 
ser.Uart_SendHex(command['ON'])
time.sleep(0.2)#Allow time for the message to be sent
 

#FAN SPEED: LOW, MEDIUM, HIGH
GPIO.output(TXDEN_1, GPIO.LOW) 
ser.Uart_SendHex(command['MEDIUM']) 
time.sleep(0.2)#Allow time for the message to be sent
 

#SUPPLY FAN: STANDARD, CONTINUOUS
GPIO.output(TXDEN_1, GPIO.LOW) 
ser.Uart_SendHex(command['STANDARD']) 
time.sleep(0.2)#Allow time for the message to be sent

#MODE: HEAT ONLY, COOL ONLY, AUTO CHANGEOVER, FAN ONLY
GPIO.output(TXDEN_1, GPIO.LOW) 
ser.Uart_SendHex(command['AUTO CHANGEOVER']) 
time.sleep(0.2)#Allow time for the message to be sent

#SET TEMP to set_temp
GPIO.output(TXDEN_1, GPIO.LOW) 
ser.Uart_SendHex(temp_hex[set_temp])  
time.sleep(0.2)#Allow time for the message to be sent


try:
        while(1):
        #get current time
        now = time.localtime()
        hour = now.tm_hour
        minute = now.tm_min
        day = now.tm_mday
        month = now.tm_mon
        year = now.tm_year
        
        
        # Get room temp
        GPIO.output(TXDEN_1, GPIO.LOW) 
        ser.Uart_SendHex(command['ROOM TEMP'])
        time.sleep(0.0025)#Waiting to send
        GPIO.output(TXDEN_1, GPIO.HIGH) #set to receive mode
        s = ser.Uart_ReceiveHex(7) 
        hex_string = binascii.hexlify(s)
        temp_string = "0x" + hex_string[6:10]
        if(len(temp_string) == 6):
                room_temp_test = (int(temp_string, 16))/10.0
                if(room_temp_test < 40.0):
                        room_temp = room_temp_test
                        

        # Get outside temp
        GPIO.output(TXDEN_1, GPIO.LOW) 
        ser.Uart_SendHex(command['OUTSIDE TEMP'])
        time.sleep(0.0025)#Waiting to send
        GPIO.output(TXDEN_1, GPIO.HIGH) #set to receive mode
        s = ser.Uart_ReceiveHex(7) 
        hex_string = binascii.hexlify(s)
        temp_string = "0x" + hex_string[6:10]
        if(len(temp_string) == 6):
                outside_temp_test = (int(temp_string, 16))/10.0
                if(outside_temp_test < 40.0):
                        outside_temp = outside_temp_test

        
        print("Time:" + str(day) + "/" + str(month) + " - " + str(hour) + ":" + str(minute) + " | Room temp:" + str(room_temp) + " | Outside temp:" + str(outside_temp) + " | Set temp:" + str(set_temp) + "    | To exit press 'ctrl + c'")
	# Print on terminal

        #log data
        with open('log_static.csv', 'a') as log:
            writer = csv.writer(log)
            # record data to csv file
            #header = ['Date', 'Time', 'Room temp', 'Set temp', 'Outside temp']
            data = [str(day)+"/"+str(month)+"/"+str(year), str(hour)+":"+str(minute), room_temp, set_temp, outside_temp]
            writer.writerow(data)
            # close the log file
            log.close()


        time.sleep(30)



except KeyboardInterrupt:
    #check if the user pressed control + C
    logging.info("ctrl + c")
    exit()
