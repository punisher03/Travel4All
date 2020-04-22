# dictionary to get full name of state from abbreviation
import pandas as pd

def calc_gas_price(state, city_mpg, highway_mpg, fuel_type, trip_length):

    gas_prices = pd.read_csv('gasprices.csv', index_col=0)
    cost_per_gallon = float(gas_prices[gas_prices['State'] == state][fuel_type])
    avg_mpg = 0.5*(city_mpg + highway_mpg)
    price = (trip_length/avg_mpg)*cost_per_gallon
    return price

def gas_cost(df):
    states = {
        'AK': 'Alaska',
        'AL': 'Alabama',
        'AR': 'Arkansas',
        'AS': 'American Samoa',
        'AZ': 'Arizona',
        'CA': 'California',
        'CO': 'Colorado',
        'CT': 'Connecticut',
        'DC': 'District of Columbia',
        'DE': 'Delaware',
        'FL': 'Florida',
        'GA': 'Georgia',
        'GU': 'Guam',
        'HI': 'Hawaii',
        'IA': 'Iowa',
        'ID': 'Idaho',
        'IL': 'Illinois',
        'IN': 'Indiana',
        'KS': 'Kansas',
        'KY': 'Kentucky',
        'LA': 'Louisiana',
        'MA': 'Massachusetts',
        'MD': 'Maryland',
        'ME': 'Maine',
        'MI': 'Michigan',
        'MN': 'Minnesota',
        'MO': 'Missouri',
        'MP': 'Northern Mariana Islands',
        'MS': 'Mississippi',
        'MT': 'Montana',
        'NA': 'National',
        'NC': 'North Carolina',
        'ND': 'North Dakota',
        'NE': 'Nebraska',
        'NH': 'New Hampshire',
        'NJ': 'New Jersey',
        'NM': 'New Mexico',
        'NV': 'Nevada',
        'NY': 'New York',
        'OH': 'Ohio',
        'OK': 'Oklahoma',
        'OR': 'Oregon',
        'PA': 'Pennsylvania',
        'PR': 'Puerto Rico',
        'RI': 'Rhode Island',
        'SC': 'South Carolina',
        'SD': 'South Dakota',
        'TN': 'Tennessee',
        'TX': 'Texas',
        'UT': 'Utah',
        'VA': 'Virginia',
        'VI': 'Virgin Islands',
        'VT': 'Vermont',
        'WA': 'Washington',
        'WI': 'Wisconsin',
        'WV': 'West Virginia',
        'WY': 'Wyoming'
        }
    gas_prices = pd.read_csv('../gasprices.csv', index_col=0)
    city_mpg=48
    highway_mpg=43
    gas_type="Regular Price"
    costs = []
    for idx, row in df.iterrows():
        state = row['state']
        trip_length = float(row['dist from origin'][:-3].replace(',',''))
        cost = calc_gas_price(states[state], city_mpg, highway_mpg, gas_type, trip_length)
        costs.append(cost)
    df['cost'] = costs
    return df
