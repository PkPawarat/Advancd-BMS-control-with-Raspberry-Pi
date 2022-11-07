import time
<<<<<<< HEAD
import csv
import RPi.GPIO as GPIO
from waveshare_2_CH_RS485_HAT import config
from DFRobot_DHT20 import *
=======
>>>>>>> cd7dc2d3c452b3443cec633b91c60196dafe97d7

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

<<<<<<< HEAD
=======
if __name__ == "__main__":
       while(1):
              print(read_temp())
              time.sleep(1)
            #   pass
>>>>>>> cd7dc2d3c452b3443cec633b91c60196dafe97d7
