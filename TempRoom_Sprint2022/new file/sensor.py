import time
<<<<<<< HEAD
import csv
=======
>>>>>>> cd7dc2d3c452b3443cec633b91c60196dafe97d7
import RPi.GPIO as GPIO
from DFRobot_DHT20 import *


# Setup sensor function
IIC_MODE         = 0x01                 # default use IIC1
IIC_ADDRESS      = 0x38                 # default i2c device address
dht20 = DFRobot_DHT20(IIC_MODE ,IIC_ADDRESS)
dht20.begin()
time.sleep(1)
def sensor_get_temp():
    return dht20.get_temperature()

def sensor_get_humid():
    return dht20.get_humidity()

if __name__ == "__main__":
       while(1):
            print("Temperature {:.2f} C | Humidity {:.2f} % RH ".format(sensor_get_humid(), sensor_get_temp()))
            time.sleep(1)
        #    pass
