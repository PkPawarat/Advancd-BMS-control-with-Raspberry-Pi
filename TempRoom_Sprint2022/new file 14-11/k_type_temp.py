import time
import RPi.GPIO as GPIO

import max6675

# set the pin for communicate with MAX6675
cs = 25
sck = 24
so = 23

# max6675.set_pin(CS, SCK, SO, unit)   [unit : 0 - raw, 1 - Celsius, 2 - Fahrenheit]
max6675.set_pin(cs, sck, so, 1)

# class k_type_temp(object):
def read_temp():
    return max6675.read_temp(cs)

if __name__ == "__main__":
        while(1):
            print(read_temp())
            time.sleep(1)
