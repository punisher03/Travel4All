import json
from amadeus import Client, ResponseError
import pandas as pd
def finall_flow(df,df1,origin_address,dest_address,date):
    amadeus = Client(client_id='l752mUaecNtoAHgIk0xS8FU0PT7Gylhg',
        client_secret='XorPUhfQAf0owoI4')
    total_costs = {}
    flight_costs = {}
    print(df)
    print(df1)
    for idx, row in df[:2].iterrows():
        a_code = row['iata code']
        for idx, row2 in df1[:2].iterrows():
            b_code = row2['iata code']

            try:
                response = amadeus.shopping.flight_offers_search.get(
                    originLocationCode=a_code,
                    destinationLocationCode=b_code,
                    departureDate=date,
                    adults=1)
                print(response.data[0]['price']['total'])
                flight_cost=response.data[0]['price']['total']
                flight_costs[(a_code, b_code)] = flight_cost

                driving_cost = row['cost'] + row2['cost']
                total = float(flight_cost) + float(driving_cost)
                total_costs[(a_code, b_code)] = total


            except ResponseError as error:
                print(error)
    cheapest_a = min(total_costs, key=total_costs.get)
    origin_airport = cheapest_a[0]
    dest_airport = cheapest_a[1]
    response_final = amadeus.shopping.flight_offers_search.get(
        originLocationCode=origin_airport,
        destinationLocationCode=dest_airport,
        departureDate=date,
        adults=1)
    car_cost1=df[df['iata code']==origin_airport]['cost'].iloc[0]
    flightt_cost=flight_costs[(origin_airport, dest_airport)]
    car_cost2=df1[df1['iata code']==dest_airport]['cost'].iloc[0]
    longo=df[df['iata code']==origin_airport]['latitude'].iloc[0]
    lato=df[df['iata code']==origin_airport]['longitude'].iloc[0]
    longd=df1[df1['iata code']==dest_airport]['latitude'].iloc[0]
    latd=df1[df1['iata code']==dest_airport]['longitude'].iloc[0]
    print("Start at", origin_address, "and drive to", origin_airport + ".",
     "The cost of this portion of the trip:", car_cost1)
    print()
    print("Take flight from", origin_airport, 'to', dest_airport + ".",
     "The cost of this portion of the trip:", flightt_cost)
    print()
    print("Drive from", dest_airport, "to", dest_address + ".",
     "The cost of this portion of the trip:", car_cost2)
    print()
    print("The total cost of the trip is:", total_costs[cheapest_a])
    return [origin_address,origin_airport,dest_airport,dest_address,response_final.data,total_costs[cheapest_a],car_cost1,flightt_cost,car_cost2,longo,lato,longd,latd]
