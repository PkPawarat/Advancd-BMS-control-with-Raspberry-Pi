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

import sensor, modbus, k_type_temp, driver

filename = "main_new_test.csv"

set_temp = 21.0
output_sate = ""
modbus.set_AC('ON')
modbus.set_AC('MEDIUM')
modbus.set_AC('CONTINUOUS')
modbus.set_AC('AUTO CHANGEOVER')
modbus.set_AC_temp(set_temp)

try: 
    while(1): 
        now = time.localtime()
        hour = now.tm_hour
        minute = now.tm_min
        day = now.tm_mday
        month = now.tm_mon
        year = now.tm_year

        room_temp_AC = modbus.get_AC_room_temp()
        outside_temp_AC = modbus.get_AC_outside_temp()


        second = 0 
        sum_temp = 0
        sum_humid = 0
        
        for second in range(60):

            sensor_temp =   sensor.sensor_get_temp()
            sensor_humid =  sensor.sensor_get_humid()

            water_temp = k_type_temp.read_temp()

            modbus.check_temp()

            driver.fan()

            if water_temp <= 40:
                driver.relay_on()
                output_sate = "ON"
                # GPIO.output(HUMIDIFIER_PIN, True)
                # # return "On"
            elif water_temp > 40:
                driver.relay_off()
                output_sate = "OFF"
                # return "Off"


            sum_temp += sensor_temp
            sum_humid += sensor_humid
            if second == 59:        # for every minute return sensor Temp & humidify, and setting set_time from Ditionary time_temp
                sum_temp = sum_temp / (second+1)
                sum_humid = sum_humid / (second+1)
                set_temp = modbus.time_temp[str(hour) + ":" + str(minute)]

            time.sleep(1)

        modbus.set_AC_temp(set_temp)

        #log data
        with open(filename, 'a') as log:
            writer = csv.writer(log)
            # record data to csv file
            header = ['Date', 'Time', 'Room temp', 'Set temp', 'Outside temp', 'Sensor Temp', 'Sensor humid']
            writer.writerow(header)
            data = [str(day)+"/"+str(month)+"/"+str(year), str(hour)+":"+str(minute), +" "+ room_temp_AC, +" "+ set_temp, +" "+ outside_temp_AC, +" "+ sum_temp, +" "+ sum_humid]
            writer.writerow(data)
            # close the log file
            log.close()


        print("AC_Room_Temp {}, AC_Outside_Temp {}, Temperature {:.2f} C | Humidity {:.2f} % RH, Stage of Humidify: {} ".format(room_temp_AC, outside_temp_AC, sensor_temp, sensor_humid, output_sate))




except KeyboardInterrupt:
    #check if the user pressed control + C
    logging.info("ctrl + c")
    modbus.set_AC('OFF')
    driver.relay_off()
    exit()