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
import sensor
# Setup Fan pin by usign driver at MA
FAN_PIN_A1 = 37
FAN_PIN_A2 = 35
FAN_PIN_EA = 40 
GPIO.setup(FAN_PIN_A1, GPIO.OUT)
GPIO.setup(FAN_PIN_A2, GPIO.OUT)
GPIO.setup(FAN_PIN_EA, GPIO.OUT)
GPIO.output(FAN_PIN_A1, GPIO.LOW)
GPIO.output(FAN_PIN_A2, GPIO.LOW)
fan = GPIO.PWM(FAN_PIN_EA,100)             # Set GPIO14 as a PWM output, with 100Hz frequency (we need to make it match the fans specified PWM frequency)
fan.start(50)                           # Generate a PWM signal with a 50% duty cycle (fan on), start on so that it increases humidity of room and then turns it off or slows down

# Setup Relay pin by usign driver at MB
relay_pin_B1 = 33
relay_pin_B2 = 31
GPIO.setup(relay_pin_B1, GPIO.OUT)
GPIO.setup(relay_pin_B2, GPIO.OUT)
GPIO.output(relay_pin_B1, GPIO.LOW)
GPIO.output(relay_pin_B2, GPIO.LOW)


def fan(humid = sensor.sensor_get_humid()):
    if int(humid) < 40:
        fan.start(100)
    elif int(humid) > 60:
        fan.start(0)

def relay(humid = sensor.sensor_get_humid()):
    if int(humid) < 60:
        GPIO.output(FAN_PIN_A1, True)
        GPIO.output(FAN_PIN_A2, False)
    elif int(humid) > 60:
        GPIO.output(FAN_PIN_A1, False)
        GPIO.output(FAN_PIN_A2, False)

def relay_on():
    GPIO.output(FAN_PIN_A1, True)
    GPIO.output(FAN_PIN_A2, False)

def relay_off():
    GPIO.output(FAN_PIN_A1, False)
    GPIO.output(FAN_PIN_A2, False)


   
