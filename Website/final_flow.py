import json
from amadeus import Client, ResponseError
import pandas as pd
def finall_flow(df,df1,origin_address,dest_address,date):
    amadeus = Client(client_id='UmuSC0LY9TgqaZoLDpBR2x74yN0GCahI',
        client_secret='9SbiFzopXFTkVOBz')
    total_costs = {}
    flight_costs = {}
    print(df)
    print(df1)
    for idx, row in df[:3].iterrows():
        a_code = row['iata code']
        for idx, row2 in df1[:3].iterrows():
            b_code = row2['iata code']

            try:
                response = amadeus.shopping.flight_offers_search.get(
                    originLocationCode=a_code,
                    destinationLocationCode=b_code,
                    departureDate=date,
                    adults=1)
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
    print("Start at", origin_address, "and drive to", origin_airport + ".",
     "The cost of this portion of the trip:", df[df['iata code']==origin_airport]['cost'].iloc[0])
    print()
    print("Take flight from", origin_airport, 'to', dest_airport + ".",
     "The cost of this portion of the trip:", flight_costs[(origin_airport, dest_airport)])
    print()
    print("Drive from", dest_airport, "to", dest_address + ".",
     "The cost of this portion of the trip:", df1[df1['iata code']==dest_airport]['cost'].iloc[0])
    print()
    print("The total cost of the trip is:", total_costs[cheapest_a])
    return total_costs[cheapest_a]
