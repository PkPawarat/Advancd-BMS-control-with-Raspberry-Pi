import sqlite3
import sys
from datetime import datetime
from datetime import date
conn=sqlite3.connect('sensorsData.db')
curs=conn.cursor()
curs.execute("DROP TABLE IF EXISTS DHT_data_input")
curs.execute("CREATE TABLE DHT_data_input(timestamp DATETIME, temp NUMERIC, hum NUMERIC)")
def add_data():
    for x in range (0,2):
        for y in range (0,2):
                today = date.today()
                a = datetime(today.year,today.month, today.day, x, y*30, 00)
                temp , humid = int(input("Input temp for "+ str(x) + ":" + str(y*30) + " : ")), int(input("Input humid for "+ str(x) + ":" + str(y*30) + " : "))
                curs.execute("INSERT INTO DHT_data_input values((?), (?), (?))", (a,temp, humid))
                conn.commit()
# function to insert data on a table

# call the function to insert data
add_data()
# print database content
print ("\nEntire database contents:\n")
for row in curs.execute("SELECT * FROM DHT_data_input"):
    print (row)
# close the database after use

conn.close()