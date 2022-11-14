import time
import sqlite3
import Adafruit_DHT
dbname='sensorsData.db'
conn=sqlite3.connect(dbname)
curs=conn.cursor()
curs.execute("DROP TABLE IF EXISTS DHT_data_output")
curs.execute("CREATE TABLE DHT_data_output(timestamp DATETIME, temp NUMERIC, hum NUMERIC)")
sampleFreq = 1*60 # time in seconds ==> Sample each 1 min
# get data from DHT sensor
def getDHTdata():	
	DHT22Sensor = Adafruit_DHT.DHT22
	DHTpin = 16
	hum, temp = Adafruit_DHT.read_retry(DHT22Sensor, DHTpin)
	if hum is not None and temp is not None:
		hum = round(hum)
		temp = round(temp, 1)
	return temp, hum
# log sensor data on database
def logData (temp, hum):
	
	curs.execute("INSERT INTO DHT_data values(datetime('now'), (?), (?))", (temp, hum))
	conn.commit()
	conn.close()
# main function
def printData():
    print ("\nEntire database contents:\n")
    for row in curs.execute("SELECT * FROM DHT_data"):
    print (row)
def main():
	while True:
		temp, hum = getDHTdata()
		logData (temp, hum)
		time.sleep(sampleFreq)
# ------------ Execute program 
main()