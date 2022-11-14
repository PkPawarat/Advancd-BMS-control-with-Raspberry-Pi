import serial
import os
import sys
import logging
import binascii
import time
import csv
import RPi.GPIO as GPIO
from waveshare_2_CH_RS485_HAT import config

#sys.path.append("../") 
#import sensor_input
import sensor_output
#import k_type_temp
import modbus
import driver
import sqlite3
sampleFreq = 2
dbname='sensorsData_1.db'
conn=sqlite3.connect(dbname)
curs=conn.cursor()
curs.execute("DROP TABLE IF EXISTS DHT_data_input")
curs.execute("CREATE TABLE DHT_data_input(timestamp DATETIME, temp NUMERIC, hum NUMERIC)")

curs.execute("DROP TABLE IF EXISTS DHT_data_output")
curs.execute("CREATE TABLE  DHT_data_output(timestamp DATETIME, temp NUMERIC, hum NUMERIC)")
#filename = "main_new_test_14-11-22_test1.csv"

set_temp = 21.0



# now = time.localtime()

#with open(filename, 'a') as log:
 #   writer = csv.writer(log)
    # record data to csv file
  #  header = ['D-M\tTime\tS_Temp\tS_Humid\tW_temp\tSet_temp']
  #  writer.writerow(header)
   # log.close()

if __name__ == "__main__":
    try:
        modbus.set_AC('ON')
        modbus.set_AC('COOL ONLY')
        
        #modbus.set_AC('CONTINUOUS')
        #modbus.set_AC('AUTO CHANGEOVER')
        #modbus.set_AC_temp(float(set_temp))
        #sensor_input.add_data()
        while(1): 
                now = time.localtime()
                hour = now.tm_hour
                minute = now.tm_min
                day = now.tm_mday
                month = now.tm_mon
                year = now.tm_year
                
                #set_temp = modbus.set_up_time_temp()
                #modbus.set_AC_temp(set_temp)
                
                sensor_reading = sensor_output.read_sensor()
                sensor_temp = sensor_reading[0]
                sensor_humid = sensor_reading[1]
                sensor_output.logData(sensor_temp,sensor_humid)

                #water_temp = k_type_temp.read_temp()
                
                driver.fan_relay(sensor_humid)
                #modbus.check_AC()
                #print( sensor_temp , sensor_humid) 
            #log data
            #if next_minute == minute:
            #with open(filename, 'a') as log:
             #   writer = csv.writer(log)
             #   data = ["{}-{}\t{}:{}\t{:.2f} C\t{:.2f} % RH\t{} C\tS Temp {:.2f}C".format(day, month, hour, minute, sensor_temp, sensor_humid, water_temp, set_temp)]
              #  writer.writerow(data)
            #    log.close()
          #  print("{}-{}\t{}:{}\t{:.2f} C\t{:.2f} % RH\t{} C\tS Temp {:.2f}C".format(day, month, hour, minute, sensor_temp, sensor_humid, water_temp, set_temp))
            
           # time.sleep(5)
            
            
            # while(second):
            #     # Check Global variable on Changing temp
            #     # if input():
            #     # hr = input(Enter hour: )
            #     # min = input(Enter minute: )#
            #     # modbus.command[str(input())]
            #     # modbus.time_temp[str(hr) + ":" + str(min)]
                # second = False#
            #     pass
            #next_minute = minute + 1

    except KeyboardInterrupt:
        #check if the user pressed control + C
        logging.info("ctrl + c")
        modbus.set_AC('OFF')
        driver.relay_off()
        driver.fan_off()
        GPIO.cleanup()
        exit()
