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
app = Flask(__name__)

@app.route("/<name>")
def home(name):
	return render_template("index.html", content = name)

if __name__ == "__main__":
	app.run()
   