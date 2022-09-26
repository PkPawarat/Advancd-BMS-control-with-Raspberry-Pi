import serial
import os
import sys
import logging
import binascii
import time
import csv
import RPi.GPIO as GPIO
from waveshare_2_CH_RS485_HAT import config
from DFRobot_DHT20 import *
sys.path.append("../") 

# setup Modbus communcation hat
logging.basicConfig(level=logging.INFO)
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)  
TXDEN_1 = 27
ser = config.config(dev = "/dev/ttySC0")

filename = "temp_log_cyclic.csv"

set_temp = 21.0

GPIO.setmode(GPIO.BOARD)
GPIO.setup(16, GPIO.OUT)            # set pin for sensor at pin 16 GPIO
IIC_MODE         = 0x01             # default use IIC1
IIC_ADDRESS      = 0x38             # default i2c device address

dht20 = DFRobot_DHT20(IIC_MODE ,IIC_ADDRESS)
dht20.begin()

target_humid = 50
output_sate = "On"

## Temp hex code dictionary
temp_hex = {
        18.0: '\x01\x06\x00\x66\x00\xB4\x69\xA2',
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

## Time temp dictionary
time_temp = {
        '0:0': 18.0,
        '0:30': 18.0,
        '1:0': 18.0,
        '1:30': 18.0,
        '2:0': 18.0,
        '2:30': 18.0,
        '3:0': 18.0,
        '3:30': 18.5,
        '4:0': 19.0,
        '4:30': 20.0,
        '5:0': 21.0,
        '5:30': 22.0,
        '6:0': 23.0,
        '6:30': 24.0,
        '7:0': 25.0,
        '7:30': 26.0,
        '8:0': 27.0,
        '8:30': 27.5,
        '9:0': 28.0,
        '9:30': 28.5,
        '10:0': 29.0,
        '10:30': 29.5,
        '11:0': 30.0,
        '11:30': 30.0,
        '12:0': 30.0,
        '12:30': 30.0,
        '13:0': 30.0,
        '13:30': 30.0,
        '14:0': 30.0,
        '14:30': 30.0,
        '15:0': 30.0,
        '15:30': 30.0,
        '16:0': 30.0,
        '16:30': 29.5,
        '17:0': 29.0,
        '17:30': 28.5,
        '18:0': 28.0,
        '18:30': 27.5,
        '19:0': 27.0,
        '19:30': 26.0,
        '20:0': 25.0,
        '20:30': 24.0,
        '21:0': 23.0,
        '21:30': 22.0,
        '22:0': 21.0,
        '22:30': 20.0,
        '23:0': 19.0,
        '23:30': 18.5
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
        
        'ROOM TEMP' :           '\x01\x03\x03   \x53            \x00\x01       \x74\x5F',
        'OUTSIDE TEMP' :        '\x01\x03\x03   \x54            \x00\x01       \xC5\x9E'
      }



def set_AC(string):
    GPIO.output(TXDEN_1, GPIO.LOW) 
    ser.Uart_SendHex(command[string])
    time.sleep(0.2)

def set_AC_temp(string):
    GPIO.output(TXDEN_1, GPIO.LOW) 
    ser.Uart_SendHex(temp_hex[string])
    time.sleep(0.2)

def get_infor_AC(string):
    set_AC(string)
    GPIO.output(TXDEN_1, GPIO.HIGH) #set to receive mode
    s = ser.Uart_ReceiveHex(7)
    hex_string = binascii.hexlify(s)
    temp_string = "0x" + hex_string[6:10]
    if(len(temp_string) == 6):
        room_temp_test = (int(temp_string, 16))/10.0
        if(room_temp_test < 40.0):
            return room_temp_test

def sensor_get_temp():
    return dht20.get_temperature()
def sensor_get_humid():
    return dht20.get_humidity()

def sensor(state):

    if state < 50:
        output_sate = "On"
        GPIO.output(16,True)
    elif state > 50:
        output_sate = "Off"
        GPIO.output(16,False)

#AC STATE: ON, OFF
set_AC('ON')
#FAN SPEED: LOW, MEDIUM, HIGH
set_AC('MEDIUM')
#SUPPLY FAN: STANDARD, CONTINUOUS
set_AC('CONTINUOUS')
#MODE: HEAT ONLY, COOL ONLY, AUTO CHANGEOVER, FAN ONLY
set_AC('AUTO CHANGEOVER')
#SET TEMP to set_temp
set_AC_temp(set_temp)


# Repeating code
try:
    while(1):
        #get current time
        now = time.localtime()
        hour = now.tm_hour
        minute = now.tm_min
        day = now.tm_mday
        month = now.tm_mon
        year = now.tm_year

        room_temp_AC = get_infor_AC('ROOM TEMP')
        outside_temp_AC = get_infor_AC('OUTSIDE TEMP')

        sensor_temp = sensor_get_temp()
        sensor_humid = sensor_get_humid()

        print(room_temp_AC, outside_temp_AC, sensor_temp, sensor_humid)


        time.sleep(1)

except KeyboardInterrupt:
    #check if the user pressed control + C
    logging.info("ctrl + c")
    exit()        