import RPi.GPIO as GPIO
import dht11
import time
import sqlite3
import sys
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.cleanup()
instance = dht11.DHT11(pin = 17)
sampleFreq = 30
dbname='sensorsData_1.db'
conn=sqlite3.connect(dbname)
curs=conn.cursor()
curs.execute("DROP TABLE IF EXISTS DHT_data_output")
curs.execute("CREATE TABLE  DHT_data_output(timestamp DATETIME, temp NUMERIC, hum NUMERIC)")
def initialize_table():
  
    conn.close()
def read_sensor():	
		result = instance.read()
		try: 
			return [result.temperature, result.humidity]
			time.sleep(sampleFreq)
		except:
			pass
# log sensor data on database
def logData (temp, hum):
	dbname='sensorsData_1.db'
	conn=sqlite3.connect(dbname)
	curs=conn.cursor()
	if temp > 0 and hum > 0:
		curs.execute("INSERT INTO DHT_data_output values(datetime('now'), (?), (?))", (temp, hum))
		conn.commit()
	conn.close()
# main function
def printTable():
	dbname='sensorsData_1.db'
	conn=sqlite3.connect(dbname)
	curs=conn.cursor()
	print ("\nEntire database contents:\n")
	for row in curs.execute("SELECT * FROM DHT_data_output"):
			   print(row)
	conn.close()
def lastData():
	dbname='sensorsData_1.db'
	conn=sqlite3.connect(dbname)
	curs=conn.cursor()
	print(" Last Data logged on database: ")
	for row in curs.execute("SELECT * FROM DHT_data_output ORDER BY timestamp DESC LIMIT 1"):
		print(row)
	conn.close()
if __name__ == "__main__":
		while True:
			#initialize_table()
			current_sensor = read_sensor()
			logData(current_sensor[0], current_sensor[1])
			#lastData()
			time.sleep(sampleFreq)
			#lastData()
		#printData()
conn.close()			
