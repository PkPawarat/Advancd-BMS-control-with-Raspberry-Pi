import serial
import os
import sys
import logging
import binascii
import time
import csv
import RPi.GPIO as GPIO
import sensor_output

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False) 
# Setup Fan pin by usign driver at MA
FAN_PIN_A1 = 26
FAN_PIN_A2 = 19
FAN_PIN_EA = 21
 
GPIO.setup(FAN_PIN_A1, GPIO.OUT)
GPIO.setup(FAN_PIN_A2, GPIO.OUT)
GPIO.setup(FAN_PIN_EA, GPIO.OUT)
GPIO.output(FAN_PIN_A1, GPIO.LOW)
GPIO.output(FAN_PIN_A2, GPIO.LOW)               #turn on
fan = GPIO.PWM(FAN_PIN_EA,1000)             # Set GPIO14 as a PWM output, with 100Hz frequency (we need to make it match the fans specified PWM frequency)
fan.start(50)                               # Generate a PWM signal with a 50% duty cycle (fan on), start on so that it increases humidity of room and then turns it off or slows down

# Setup Relay pin by usign driver at MB
relay_pin_B1 = 13
relay_pin_B2 = 6

GPIO.setup(relay_pin_B1, GPIO.OUT)
GPIO.setup(relay_pin_B2, GPIO.OUT)
GPIO.output(relay_pin_B1, GPIO.LOW)             #turn on
GPIO.output(relay_pin_B2, GPIO.LOW)


def fan_on():
    GPIO.output(FAN_PIN_A1, GPIO.LOW)
    GPIO.output(FAN_PIN_A2, GPIO.HIGH)

def fan_off():
    GPIO.output(FAN_PIN_A1, GPIO.LOW)
    GPIO.output(FAN_PIN_A2, GPIO.LOW)


def relay_on():
    GPIO.output(relay_pin_B1, GPIO.HIGH)
    GPIO.output(relay_pin_B2, GPIO.LOW)

def relay_off():
    GPIO.output(relay_pin_B1, GPIO.LOW)
    GPIO.output(relay_pin_B2, GPIO.LOW)

target_humid = 50
def fan_relay(humid):
    diff_humid = humid - target_humid
    if humid == 0:
        pass

    if diff_humid <= -5 and diff_humid > -target_humid:
        initialize_fan_relay()
        time.sleep(2)
        print("Fan ON on at 100, Relay ON")    
    elif diff_humid >= -5 and diff_humid < 0:
        initialize_fan_relay()
        fan.start(50)
        fan_on()
        relay_on()
        time.sleep(2)
        print("Fan ON on at 50, Relay still ON")
    elif diff_humid >= 0:
        fan.start(0)
        fan_off()
        relay_off()
        time.sleep(2)
        print("Fan OFF, Relay OFF")
def initialize_fan_relay():
    fan.start(100)
    fan_on()
    relay_on()
    time.sleep(2)
            

if __name__ == "__main__":
    initialize_fan_relay()
    while(1):
        current_reading = sensor_output.read_sensor()
        print (current_reading[0], current_reading[1])
        time.sleep(1)
        fan_relay(current_reading[1])
       
