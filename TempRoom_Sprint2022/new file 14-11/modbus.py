import serial
import os
import sys
import logging
import binascii
import time
import csv
import RPi.GPIO as GPIO
from waveshare_2_CH_RS485_HAT import config
#import sensor

# setup Modbus communcation hat
logging.basicConfig(level=logging.INFO)
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

TXDEN_1 = 27
ser = config.config(dev = "/dev/ttySC0")


## Temp hex code dictionary
temp_hex = {
        18.0: b'\x01\x06\x00\x66\x00\xB4\x69\xA2',
        18.5: b'\x01\x06\x00\x66\x00\xB9\xA8\x67',
        19.0: b'\x01\x06\x00\x66\x00\xBE\xE9\xA5',
        19.5: b'\x01\x06\x00\x66\x00\xC3\x29\x84',
        20.0: b'\x01\x06\x00\x66\x00\xC8\x68\x43',
        20.5: b'\x01\x06\x00\x66\x00\xCD\xA8\x40',
        21.0: b'\x01\x06\x00\x66\x00\xD2\xE9\x88',
        21.5: b'\x01\x06\x00\x66\x00\xD7\x29\x8B',
        22.0: b'\x01\x06\x00\x66\x00\xDC\x68\x4C',
        22.5: b'\x01\x06\x00\x66\x00\xE1\xA9\x9D',
        23.0: b"\x01\x06\x00\x66\x00\xE6\xE8\x5F",
        23.5: b'\x01\x06\x00\x66\x00\xEB\x29\x9A',
        24.0: b'\x01\x06\x00\x66\x00\xF0\x69\x91',
        24.5: b'\x01\x06\x00\x66\x00\xF5\xA9\x92',
        25.0: b'\x01\x06\x00\x66\x00\xFA\xE9\x96',
        25.5: b'\x01\x06\x00\x66\x00\xFF\x29\x95',
        26.0: b'\x01\x06\x00\x66\x01\x04\x69\x86',
        26.5: b'\x01\x06\x00\x66\x01\x09\xA8\x43',
        27.0: b'\x01\x06\x00\x66\x01\x0E\xE9\x81',
        27.5: b'\x01\x06\x00\x66\x01\x13\x29\x88',
        28.0: b'\x01\x06\x00\x66\x01\x18\x68\x4F',
        28.5: b'\x01\x06\x00\x66\x01\x1D\xA8\x4C',
        29.0: b'\x01\x06\x00\x66\x01\x22\xE8\x5C',
        29.5: b'\x01\x06\x00\x66\x01\x27\x28\x5F',
        30.0: b'\x01\x06\x00\x66\x01\x2C\x69\x98'
      }

## Time temp dictionary
time_temp = {
        '0:0'  : 18.0,
        '0:30' : 18.0,
        '1:0'  : 18.0,
        '1:30' : 18.0,
        '2:0'  : 18.0,
        '2:30' : 18.0,
        '3:0'  : 18.0,
        '3:30' : 18.5,
        '4:0'  : 19.0,
        '4:30' : 20.0,
        '5:0'  : 21.0,
        '5:30' : 22.0,
        '6:0'  : 23.0,
        '6:30' : 24.0,
        '7:0'  : 25.0,
        '7:30' : 26.0,
        '8:0'  : 27.0,
        '8:30' : 27.5,
        '9:0'  : 28.0,
        '9:30' : 28.5,
        '10:0' : 29.0,
        '10:30': 29.5,
        '11:0' : 30.0,
        '11:30': 30.0,
        '12:0' : 30.0,
        '12:30': 30.0,
        '13:0' : 30.0,
        '13:30': 30.0,
        '14:0' : 30.0,
        '14:30': 25.0,
        '15:0' : 25.0,
        '15:30': 25.0,
        '16:0' : 30.0,
        '16:30': 29.5,
        '17:0' : 29.0,
        '17:30': 28.5,
        '18:0' : 28.0,
        '18:30': 27.5,
        '19:0' : 27.0,
        '19:30': 26.0,
        '20:0' : 25.0,
        '20:30': 24.0,
        '21:0' : 23.0,
        '21:30': 22.0,
        '22:0' : 21.0,
        '22:30': 20.0,
        '23:0' : 19.0,
        '23:30': 18.5
      }

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
        'OUTSIDE TEMP' : b'\x01\x03\x03\x54\x00\x01\xC5\x9E'
      }
      

time_sleep = 0.0025
time_sleep_receive = 0.0025 
outside_temp = 21.0
room_temp = 21.0
set_temp_modbus = 18.0

def set_AC(string):
    GPIO.output(TXDEN_1, GPIO.LOW) 
    ser.Uart_SendHex(command[str(string)])
    time.sleep(time_sleep)

def set_AC_temp(string):
    GPIO.output(TXDEN_1, GPIO.LOW) 
    ser.Uart_SendHex(temp_hex[float(string)])
    time.sleep(time_sleep)


def get_AC(check):
    GPIO.output(TXDEN_1, GPIO.LOW)
    ser.Uart_SendHex(command[str(check)])
    time.sleep(0.0025)
    GPIO.output(TXDEN_1, GPIO.HIGH)
    s = ser.Uart_ReceiveHex(7) 
    print(s)
    hex_string = binascii.hexlify(s)
    temp_string = hex_string[6:10]
    if(len(temp_string) == 4):
        outside_temp_test = (int(temp_string, 16))/10.0
        return outside_temp_test

def set_up_time_temp():
        now = time.localtime()
        hour = now.tm_hour
        minute = now.tm_min
        ## count back in minutes until the time is in the time_temp dictionary
        for minute_offset in range(30):
            if (str(hour) + ":" + str(minute - minute_offset)) in time_temp:
                # set the temp to the last changeover point
                set_temp = time_temp[str(hour) + ":" + str(minute - minute_offset)]
                # clear the minute countback offset
                minute_offset = 0
                #break the for loop
                break
        return set_temp
        

if __name__ == "__main__":
        try:
                set_AC('OFF')
                #print(command)
                while(1):
                        #set_temp_modbus = set_up_time_temp()
                        #room_temp = get_AC_outside_temp()
                        room_temp = get_AC("ROOM TEMP")
                        print(room_temp)

        except KeyboardInterrupt:
                logging.info("ctrl + c")
                set_AC('OFF')
                GPIO.cleanup()
                exit()