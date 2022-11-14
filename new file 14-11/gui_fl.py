

from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import io
from flask import Flask, render_template, send_file, make_response, request
import datetime
import sqlite3
app = Flask(__name__)

def getLastData():
		conn=sqlite3.connect('sensorsData_1.db')
		curs=conn.cursor()
		for row in curs.execute("SELECT * FROM DHT_data_output ORDER BY timestamp DESC LIMIT 1"):
			time = str(row[0])
			temp = row[1]
			hum = row [2]
		conn.close()
		return time, temp, hum
def getHistData (numSamples):
		conn=sqlite3.connect('sensorsData_1.db')
		curs=conn.cursor()
		curs.execute("SELECT * FROM DHT_data_output ORDER BY timestamp DESC LIMIT "+ str(numSamples))
		data = curs.fetchall()
		dates = []
		temps = []
		hums =[]
		for row in reversed(data):
			dates.append(row[0])
			temps.append(row[1])
			hums.append(row[2])
		conn.close()
		return dates, temps, hums
def maxRowsTable():
		conn=sqlite3.connect('sensorsData_1.db')
		curs=conn.cursor()
		for row in curs.execute("select COUNT(temp) from DHT_data_output"):
				maxNumberRows = row[0]
		conn.close()
		return maxNumberRows
global numSamples
numSamples = maxRowsTable()
if (numSamples >101):
		numSamples = 100
@app.route("/")
def index():
		time, temp, hum = getLastData()
		templateData = {
			'time': time,
			'temp': temp,
			'hum': hum,
			'numSamples' : numSamples
		}
		return render_template('index.html', **templateData)
@app.route('/', methods=['POST'])
def my_form_post():
		global numSamples
		numSamples = int(request.form['numSamples'])
		numMaxSamples = maxRowsTable()
		if (numSamples > numMaxSamples):
			numSamples = (numMaxSamples -1)
		time,temp, hum = getLastData()
		templateData = {
			'time': time,
			'temp': temp,
			'hum': hum,
			'numSamples' : numSamples
			}
		return render_template('index.html', **templateData)
@app.route('/plot/temp')
def plot_temp():
			times, temps, hums = getHistData(numSamples)
			ys = temps
			fig = Figure()
			axis = fig.add_subplot(1,1,1)
			axis.set_title("Temperature [oC]")
			axis.set_xlabel("Samples")
			axis.grid(True)
			xs = range(numSamples)
			axis.plot(xs, ys)
			canvas = FigureCanvas(fig)
			output = io.BytesIO()
			canvas.print_png(output)
			response = make_response(output.getvalue())
			response.mimetype = 'image/png'
			return response
@app.route('/plot/hum')
def plot_hum():
			times, temps, hums = getHistData(numSamples)
			ys = hums
			fig = Figure()
			axis = fig.add_subplot(1,1,1)
			axis.set_title("Humidity [%]")
			axis.set_xlabel("Samples")
			axis.grid(True)
			xs = range(numSamples)
			axis.plot(xs, ys)
			canvas = FigureCanvas(fig)
			output = io.BytesIO()
			canvas.print_png(output)
			response = make_response(output.getvalue())
			response.mimetype = 'image/png'
			return response
if __name__ == "__main__":
	app.run(host ='0.0.0.0', port = 80,debug = True)
   
