import amadeus
from amadeus import Client, ResponseError
import pandas as pd
import requests
from datetime import datetime
import googlemaps


def lat_lon(origin_address):
    apikey = 'l752mUaecNtoAHgIk0xS8FU0PT7Gylhg'
    r = requests.get('https://maps.googleapis.com/maps/api/geocode/json?address="%s"&key=%s'%
                 (origin_address, apikey))
    result_o = r.json()['results']
    location_origin = result_o[0]['geometry']['location']
    o_lat = location_origin['lat']
    o_lon = location_origin['lng']
    origin = [o_lat, o_lon]
    aorigin=(o_lat, o_lon)
    print(origin)
    return origin,aorigin

    # Nearest airport search, put into a result array
    #Need to get live latitude and longitudinal data from Google Maps
def nearest_airport(origin):
    amadeus = Client(client_id='UmuSC0LY9TgqaZoLDpBR2x74yN0GCahI',
        client_secret='9SbiFzopXFTkVOBz')
    origin_address_list = []
    origin_state_list = []
    a_lats = []
    a_lons = []
    a_iata = []
    try:
        response = amadeus.reference_data.locations.airports.get(longitude=origin[1], latitude=origin[0])
        for i in response.data:
            data_dict = i
            origin_address_list.append(data_dict['name'])
            origin_state_list.append(data_dict['address']['stateCode'])
            a_lats.append(data_dict['geoCode']['latitude'])
            a_lons.append(data_dict['geoCode']['longitude'])
            a_iata.append(data_dict['iataCode'])

    except ResponseError as error:
        raise error
    df = pd.DataFrame({'address':origin_address_list,'latitude':a_lats,'longitude':a_lons,'iata code':a_iata,'state':origin_state_list})
    return df

def distance(origin,df):
    apikey = 'AIzaSyDxk6272R8Yu_QDKZRyR27SZBaJKN-_3u0'
    now = datetime.now()
    gmaps = googlemaps.Client(key=apikey)
    dist_from_origin = []
    time_from_origin = []
    origin_str = str(origin[0]) + "," + str(origin[1])
    print(df)
    for idx, row in df.iterrows():
        a_lat = row['latitude']
        a_lon = row['longitude']
        airport_str = str(a_lat) + "," + str(a_lon)
        directions = gmaps.directions(origin = origin_str,destination = airport_str,
                                      mode='driving',departure_time = now)
        dist_from_origin.append(directions[0]['legs'][0]['distance']['text'])
        time_from_origin.append(directions[0]['legs'][0]['duration']['text'])

    df['dist from origin'] = dist_from_origin
    df['time from origin'] = time_from_origin
    return df
