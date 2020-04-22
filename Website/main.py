from flask import Flask, render_template, request
import pandas as pd
import requests
from datetime import datetime
import json
import amadeus
from amadeus import Client
import googlemaps
from gas import  calc_gas_price,gas_cost
from amadeus1 import lat_lon,nearest_airport,distance
from final_flow import finall_flow
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField

app = Flask(__name__)




@app.route('/')
def index():


	return render_template('index.html')

@app.route('/login',methods=['GET','POST'], endpoint = 'flight_search')
def flight_search():

	t1=request.form['FROM']
	t2=request.form['TO']
	t3=request.form['DATE']
	origin=lat_lon(t1)
	df_o=nearest_airport(origin)
	df_o1=distance(origin,df_o)
	df_o2=gas_cost(df_o1)
	destination=lat_lon(t2)
	df_d=nearest_airport(destination)
	df_d1=distance(destination,df_d)
	df_d2=gas_cost(df_d1)
	totalcost=finall_flow(df_o2,df_d2,t1,t2,t3)

	return render_template('searching.html', data=totalcost)

if __name__ == '__main__':
    app.run(debug=True)
