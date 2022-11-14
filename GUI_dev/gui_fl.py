#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  appDhtWebHist_v2.py
#  
#  Created by MJRoBot.org 
#  10Jan18

'''
	RPi WEb Server for DHT captured data with Gage and Graph plot  
'''



from flask import Flask, render_template
import datetime
app = Flask(__name__)

@app.route("/")
def home():
		now = datetime.datetime.now()
		timeString = now.strftime("%Y-%m-%d %H:%M")
		templateData = {
			'title' : 'HELLO!',
			'time': timeString
			}
		return render_template('index.html', **templateData)
if __name__ == "__main__":
	app.run()
   