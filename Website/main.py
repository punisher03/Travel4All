
from flask import Flask, request, session, g, redirect,url_for, abort, render_template, flash
import pandas as pd
import requests
from datetime import datetime
import json
import iso8601
import amadeus
from amadeus import Client
import googlemaps
from gas import  calc_gas_price,gas_cost,get_lat_lon,distance_between
from amadeus1 import lat_lon,nearest_airport,distance
from final_flow import finall_flow
import gmaps
from geojson import Feature
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField

app = Flask(__name__)
apikey='AIzaSyDxk6272R8Yu_QDKZRyR27SZBaJKN-_3u0'
MAPBOX_ACCESS_KEY = 'pk.eyJ1IjoicmlzaGkxMzQyIiwiYSI6ImNrOWc1dXVtYTBraTMzaHF0NDVpaThwbG0ifQ.uvgtGnygTWTUgzBkzZwnPQ'
a=[]


ROUTE_URL = "https://api.mapbox.com/directions/v5/mapbox/driving/{0}.json?access_token={1}&overview=full&geometries=geojson"

def create_route_url(i):
    print(a)
    ROUTE = [{"lat":a[8][0] , "long": a[8][1]},{"lat":a[10][0] , "long": a[10][1]},
        {"lat":a[9][0] , "long": a[9][1]},
        {"lat":a[11][0], "long":a[11][1]},
    ]
    # Create a string with all the geo coordinates
    lat_longs = ";".join(["{0},{1}".format(ROUTE[i-2]["long"], ROUTE[i-2]["lat"]),"{0},{1}".format(ROUTE[i]["long"], ROUTE[i]["lat"])])
    print(lat_longs)
    # Create a url with the geo coordinates and access token
    url = ROUTE_URL.format(lat_longs, MAPBOX_ACCESS_KEY)
    return url

def get_route_data(i):
    # Get the route url
    route_url = create_route_url(i)
    print(route_url)
    # Perform a GET request to the route API
    result = requests.get(route_url)
    print(result)
    # Convert the return value to JSON
    data = result.json()
    print(data)
    # Create a geo json object from the routing data
    geometry = data["routes"][0]["geometry"]
    route_data = Feature(geometry = geometry, properties = {})

    return route_data


def getDuration(t1, t2):
    t1 = iso8601.parse_date(t1)
    t2 = iso8601.parse_date(t2)
    diff = t2-t1
    days, seconds = diff.days, diff.seconds
    hours = days * 24 + seconds // 3600
    minutes = (seconds % 3600) // 60
    return [str(hours)+"H "+str(minutes)+"M"]

def dateWords(d):
    return str(iso8601.parse_date(d).strftime('%A %d %B %Y')).title()

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/login',methods=['GET','POST'], endpoint = 'flight_search')
def flight_search():
    global a
    a=[]
    t1=request.form['FROM']
    t2=request.form['TO']
    t3=request.form['DATE']
    origin,aorigin=lat_lon(t1)
    df_o=nearest_airport(origin)
    df_o1=distance(origin,df_o)
    df_o2=gas_cost(df_o1)
    destination,adestination=lat_lon(t2)
    df_d=nearest_airport(destination)
    df_d1=distance(destination,df_d)
    df_d2=gas_cost(df_d1)
    o,oa,da,d,response_final,totalcost,c1,f,c2,longo,lato,longd,latd=finall_flow(df_o2,df_d2,t1,t2,t3)
    x=[longo,lato]
    x1=[longd,latd]
    a.append(totalcost)
    a.append(response_final)
    a.append(len(response_final))
    a.append(c1)
    a.append(c2)
    a.append(o)
    a.append(oa)
    a.append(da)
    a.append(origin)
    a.append(x)
    a.append(x1)
    a.append(destination)
    a.append(d)
    return render_template('card.html',o=o,oa=oa,da=da,d=d,totalcost=totalcost)

@app.route('/drivedetails',methods=['GET','POST'], endpoint = 'drive_search')
def drive_search():
    t1=request.form['FROM1']
    t2=request.form['TO1']
    t3=request.form['MPG']
    t4=request.form['HIGHWAY']
    t5=request.form['FUEL']
    t6=request.form['STATE']

    origin=get_lat_lon(t1)
    destination=get_lat_lon(t2)
    j=distance_between(origin,destination)
    gassy_price=calc_gas_price(t6,int(t3),int(t4),t5,j[0])

    return render_template('drive_results.html',prices=gassy_price,diss=j[0],time=j[1])


@app.route('/flights')
def flight_display():
	return render_template('searching.html',data=a[0],flights=a[1],len=a[2],leng=len,getDuration=getDuration,dateWords=dateWords,getDate=iso8601.parse_date)

@app.route('/carorigin')
def car1_display():
    route_data = get_route_data(2)
    return render_template('car.html',ACCESS_KEY=MAPBOX_ACCESS_KEY,route_data=route_data,thisorigin=a[8],o=a[5],oa=a[6],c1=a[3])

@app.route('/landingpage')
def landing1():
    return render_template('landing.html')

@app.route('/drivepage')
def drive1():
    return render_template('drive.html')

@app.route('/cardestination')

def car2_diplay():
    route_data = get_route_data(3)
    return render_template('car1.html',ACCESS_KEY=MAPBOX_ACCESS_KEY,route_data=route_data,thisorigin=a[10],da=a[7],d=a[12],c2=a[4])




if __name__ == '__main__':
    app.run(debug=True)
