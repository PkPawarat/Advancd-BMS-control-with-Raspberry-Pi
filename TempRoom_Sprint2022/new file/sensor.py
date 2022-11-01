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


# Setup sensor function
IIC_MODE         = 0x01                 # default use IIC1
IIC_ADDRESS      = 0x38                 # default i2c device address
dht20 = DFRobot_DHT20(IIC_MODE ,IIC_ADDRESS)
dht20.begin()

def sensor_get_temp():
    return dht20.get_temperature()

def sensor_get_humid():
    return dht20.get_humidity()

