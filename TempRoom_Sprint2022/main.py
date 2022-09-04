import serial
import os
import sys
import logging
import binascii
import time
import csv
import RPi.GPIO as GPIO
from waveshare_2_CH_RS485_HAT import config

#test
TXDEN_1 = 27
ser = config.config(dev = "/dev/ttySC0")

#set temp with hex code dictionary

# Command dictionary

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
  
  
