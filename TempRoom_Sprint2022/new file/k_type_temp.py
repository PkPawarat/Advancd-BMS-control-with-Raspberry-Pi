import serial
import os
import sys
import logging
import binascii
import time
import csv
import keyboard
import RPi.GPIO as GPIO
from waveshare_2_CH_RS485_HAT import config
from DFRobot_DHT20 import *

import max6675

# set the pin for communicate with MAX6675
cs = 22
sck = 18
so = 16

# max6675.set_pin(CS, SCK, SO, unit)   [unit : 0 - raw, 1 - Celsius, 2 - Fahrenheit]
max6675.set_pin(cs, sck, so, 1)

# class k_type_temp(object):
def read_temp():
    return max6675.read_temp(cs)
