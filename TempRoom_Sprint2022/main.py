from imp import init_builtin
from this import d
import serial
import os
import sys
import logging
import binascii
import time
import csv
import RPi.GPIO as GPIO
# import RPi.GPIO as GPIO_AC #setup a new improt system cause we going to separate it into 2 system 
# import RPi.GPIO as GPIO_Sensor

from DFRobot_DHT20 import *
from waveshare_2_CH_RS485_HAT import config

sys.path.append("../")

logging.basicConfig(level=logging.INFO)
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
if os.path.exists(libdir):
  sys.path.append(libdir)

TXDEN_1 = 27
ser = config.config(dev = "/dev/ttySC0")


#set temp with hex code dictionary
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

## Command dictionary
command = {
  'ON': '\x01\x06\x00\x01\x00\x01\x19\xCA',
  'OFF': '\x01\x06\x00\x01\x00\x00\xD8\x0A',
  'LOW': '\x01\x06\x00\x04\x00\x01\x09\xCB',
  'MEDIUM': '\x01\x06\x00\x04\x00\x02\x49\xCA',
  'HIGH': '\x01\x06\x00\x04\x00\x03\x88\x0A',
  'STANDARD': '\x01\x06\x00\x69\x00\x00\x59\xD6',
  'CONTINUOUS': '\x01\x06\x00\x69\x00\x01\x98\x16',
  'HEAT ONLY': '\x01\x06\x00\x65\x00\x01\x58\x15',
  'COOL ONLY': '\x01\x06\x00\x65\x00\x02\x18\x14',
  'AUTO CHANGEOVER': '\x01\x06\x00\x65\x00\x03\xD9\xD4',
  'FAN ONLY': '\x01\x06\x00\x65\x00\x04\x98\x16',
  'ROOM TEMP' : '\x01\x03\x03\x53\x00\x01\x74\x5F',
  'OUTSIDE TEMP' : '\x01\x03\x03\x54\x00\x01\xC5\x9E'
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


room_temp = 'ROOM TEMP'
outside_temp = 'OUTSIDE TEMP'
humid = 'Humid'

class message:
  def __init__(self, Command):
    self.Command = Command

  def message_temp(self):
    GPIO.output(TXDEN_1, GPIO.LOW)                    #set output as LOW before setpu a new command
    ser.Uart_SendHex(command[self.Command])           #setup a new command
    time.sleep(0.0025)
    GPIO.output(TXDEN_1, GPIO.HIGH)                   #Trun on a Command
    s = ser.Uart_ReceiveHex(7)                        #set 's' as receiveHex
    hex_string = binascii.hexlify(s)                  #covert hex represent to binary data
    temp_string = "0x" + hex_string[6:10]
    
    if(len(temp_string) == 6):
      temp_num = (int(temp_string, 16))/10.0    
      # if(temp_num < 40.0):                       #try not to check if temp >
      return temp_num

  def send_message(self):
    GPIO.output(TXDEN_1, GPIO.LOW)
    ser.Uart_SendHex(temp_hex[set_temp])
    time.sleep(0.2)#Allow time for the message to be sent

class Modbus:          #modbus communicate with AC, by sending a command to AC in order to sensor a temp (inside&outside)
  
  # def __init__(self):
  #   pass
  def set_temperature(self):
        

  def get_room_temp(self):              
    message.message_temp(room_temp)

  def get_outside_temp(self):
    message.message_temp(outside_temp)


class Sensor:          #an external Sensor (Humidity and Temperature Sensor - DHT20)
  
  def __init__(self):
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(16, GPIO.OUT)
    IIC_MODE         = 0x01            # default use IIC1
    IIC_ADDRESS      = 0x38           # default i2c device address
    dht20 = DFRobot_DHT20(IIC_MODE ,IIC_ADDRESS)
    dht20.begin()
    pass
    

  def get_temp(self):
    try:
      temp = dht20.get_temperature()
      return temp
    except:
		    return print("Had trouble grabbing the Temperature Sensor (DHT20), trying again...")
  
  def get_humid(self):
    try:
      humid = dht20.get_humidity()
      return humid
    except:
		    return print("Had trouble grabbing the Humidity Sensor (DHT20), trying again...")


class humidify:
  def __init__(self) -> None:
      pass


class flap_motor:
  def __init__(self) -> None:
    pass



#AC setup 

#AC state:

#FAN SPEED:

#SUPPLY FAN

#MODE:

#SET TEMP



##MAIN LOOP 

  #Get Temp (inside & outside)
  #Get Humid

  #set funciton turn ON&OFF Humidify

  ### these value setup in web interface
    #try set temp manually 
    #try set humid manually 
    #try set AC FAN manually 
    #try set AC MODE manually 
    #try set AC SUPPLY FAN manually 
  ###

  #write data to file (temp, humid)

if __name__ == "__main__":
  try:
    while(1):

      #get current time
      now = time.localtime()
      hour = now.tm_hour
      minute = now.tm_min
      day = now.tm_mday
      month = now.tm_mon
      year = now.tm_year

      pass
  
  except KeyboardInterrupt:
      #check if the user pressed control + C
      logging.info("ctrl + c")
      exit()
