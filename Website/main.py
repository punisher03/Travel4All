from flask import Flask, render_template, request
import pandas as pd
import requests
from datetime import datetime
import json
from amadeus import Client
import googlemaps
from gas import gas_prices

app = Flask(__name__)

amadeus = Client(
    client_id='N41sZfq8FmoigGxFpX4S60rgbVRy4uJM',
    client_secret='Kiieanv4cCeaIhRT'
)
apikey = 'AIzaSyDxk6272R8Yu_QDKZRyR27SZBaJKN-_3u0'


@app.route('/')
def index():
	return render_template('index.html')

@app.route('/login',methods=['GET','POST'], endpoint = 'flight_search')
def flight_search():
	t1=request.form['FROM']
	t2=request.form['TO']
	t3=request.form['DATE']
	t4=request.form['ADULTS']
	origin_address = '1512 Shattuck Ave, Berkeley, CA 94709'
	dest_address = 'New York University,New York, NY 10003'
	response = amadeus.shopping.flight_offers_search.get(originLocationCode=t1, destinationLocationCode=t2, departureDate=t3, adults=t4)
	r=requests.get('https://maps.googleapis.com/maps/api/geocode/json?address="%s"&key=%s'% (origin_address, apikey))
	r1=requests.get('https://maps.googleapis.com/maps/api/geocode/json?address="%s"&key=%s'% (dest_address, apikey))
	result_o=r.json()['results']
	result_d=r1.json()['results']
	location_origin=result_o[0]['geometry']['location']
	location_destination=result_d[0]['geometry']['location']
	o_lat=location_origin['lat']
	o_lon=location_origin['lng']
	d_lat=location_destination['lat']
	d_lon=location_destination['lng']
	origin=[o_lat, o_lon]
	destination=[d_lat,d_lon]
	return render_template('searching.html', data=response.data , origin = origin , destination = destination,tables=[gas_prices.to_html()]) 

if __name__ == '__main__':
    app.run(debug=True)
