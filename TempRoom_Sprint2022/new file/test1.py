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

import sensor, k_type_temp, modbus, driver


filename = "main_new_test.csv"

set_temp = 21.0
output_sate = ""

modbus.set_AC('ON')
modbus.set_AC('MEDIUM')
modbus.set_AC('CONTINUOUS')
modbus.set_AC('AUTO CHANGEOVER')
modbus.set_AC_temp(str(set_temp))

if __name__ == "__main__":
    try:
        while(1):
            room_temp_AC = modbus.get_AC_room_temp()
            outside_temp_AC = modbus.get_AC_outside_temp()
            sensor_temp = sensor.sensor_get_temp()
            sensor_humid = sensor.sensor_get_humid()
            water_temp = k_type_temp.read_temp()

            driver.Fan()
            driver.relay()
            
            print("AC_Room_Temp {}, AC_Outside_Temp {}".format(room_temp_AC, outside_temp_AC))
            time.sleep(1)
            print("Sensor_Temperature {:.2f} C | Sensor_Humidity {:.2f} % RH, ".format(sensor_temp, sensor_humid))
            time.sleep(1)
            print("water_temp {}".format(water_temp))


            #log data
            with open(filename, 'a') as log:
                writer = csv.writer(log)
                # record data to csv file
                header = ['AC_Room_Temp', 'AC_Outside_Temp', 'Sensor_Temperature', 'Sensor_Humidity', 'water_temp']
                writer.writerow(header)
                data = ["AC_Room_Temp {}, AC_Outside_Temp {}".format(room_temp_AC, outside_temp_AC) + " " + "Sensor_Temperature {:.2f} C | Sensor_Humidity {:.2f} % RH, ".format(sensor_temp, sensor_humid) + " " + "water_temp {}".format(water_temp)]
                writer.writerow(data)
                log.close()

    except KeyboardInterrupt:
        logging.info("ctrl + c")
        modbus.set_AC('OFF')
        driver.relay_off()
        exit()
