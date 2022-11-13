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

import sensor
import k_type_temp
import modbus
import driver

filename = "main_new_test_14-11-22_test1.csv"

set_temp = 21.0

modbus.set_AC('ON')
modbus.set_AC('MEDIUM')
modbus.set_AC('CONTINUOUS')
modbus.set_AC('AUTO CHANGEOVER')
modbus.set_AC_temp(float(set_temp))

# now = time.localtime()

with open(filename, 'a') as log:
    writer = csv.writer(log)
    # record data to csv file
    header = ['D-M\tTime\tS_Temp\tS_Humid\tW_temp\tSet_temp']
    writer.writerow(header)
    log.close()

if __name__ == "__main__":
    try: 
        while(1): 
            now = time.localtime()
            hour = now.tm_hour
            minute = now.tm_min
            day = now.tm_mday
            month = now.tm_mon
            year = now.tm_year
            
            room_temp = modbus.get_AC("ROOM TEMP")
            outside_temp = modbus.get_AC("OUTSIDE TEMP")

            set_temp = modbus.set_up_time_temp()
            modbus.set_AC_temp(set_temp)
            
            current_sensor = sensor.read_sensor()
            sensor_temp = current_sensor[0]
            sensor_humid = current_sensor[1]

            water_temp = k_type_temp.read_temp()

            second = True

            #log data
            if next_minute == minute:
                with open(filename, 'a') as log:
                    writer = csv.writer(log)
                    data = ["{}-{}\t{}:{}\t{:.2f} C\t{:.2f} % RH\t{} C\tS Temp {:.2f}C".format(day, month, hour, minute, sensor_temp, sensor_humid, water_temp, set_temp)]
                    writer.writerow(data)
                    log.close()
            print("{}-{}\t{}:{}\t{:.2f} C\t{:.2f} % RH\t{} C\tS Temp {:.2f}C".format(day, month, hour, minute, sensor_temp, sensor_humid, water_temp, set_temp))

            # while(second):
            #     # Check Global variable on Changing temp
            #     # if input():
            #     # hr = input(Enter hour: )
            #     # min = input(Enter minute: )#
            #     # modbus.command[str(input())]
            #     # modbus.time_temp[str(hr) + ":" + str(min)]
                # second = False#


            #     pass
            next_minute = minute + 1


    except KeyboardInterrupt:
        #check if the user pressed control + C
        logging.info("ctrl + c")
        modbus.set_AC('OFF')
        driver.relay_off()
        driver.fan_off()
        GPIO.cleanup()
        exit()
