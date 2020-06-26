import numpy as np
import time

from fetch_api import *
from server import *


'''
Loading symbol, name, sector data from csv file
'''
def read_index_data(file_name):
    with open(file_name) as f:
        file_contents = f.read()
    lines = file_contents.splitlines()

    symbols = []
    names = []
    sector = []

    for x in lines:
        symbols.append( x.split(',')[0] )
        names.append( x.split(',')[1] )
        sector.append( x.split(',')[2] )

    return symbols, names, sector



'''
Fetcher to obtain data
----------------------
Environment Variables:
n is the number of symbols to sample, sample size
'''

file_name = 'symbols.csv'
n = 25 
key = 'HB8BGAK56N2T7BBE'


# Implemented because of API restriction on number of possible calls per minute
sleep_period = 13

url = 'mongodb://localhost:27017/'
database_name = 'dev2'
# Define databse
mongo_connection = Database(url, database_name)
db = mongo_connection.db
# Define stocks collection
stocks_collection = Stock(db)
'''
^^^ Replace with the default_instantiate method in server
'''

index_data = read_index_data(file_name)

fetcher = Fetch(key)

'''
Format data fetched through API into entry for database
'''
def api_to_db_format(ticker, sector, ts, comp):
    for key in ts:
        val = ts[key]
        new = [
            float(val['1. open']),
            float(val['2. high']),
            float(val['3. low']),
            float(val['4. close']),
            int(val['5. volume'])
        ]
        ts[key] = new

    ts_processed = {}

    for x in ts:
        new_key = x.replace('-', '') #int(x.replace('-', ''))  # date key to int
        ts_processed.update({ new_key: ts[x]})

    ts_processed2 = []
    for x in ts_processed:
        ts_processed2.append(       # convert dict to array of dicts
            {x: ts_processed[x]}
        )

    stocks_post = {
        'ticker': ticker,
        'sector': sector,
        'ts': ts_processed2,
        'comp': comp
    }
    return stocks_post

counter = 0
for i in np.linspace(0, len(index_data[0]), num=n, dtype=int):

    ticker = index_data[0][i]
    sector = index_data[2][i]
    ts = fetcher.alpha(ticker)[0]
    comp = index_data[1][i]

    stocks_post = api_to_db_format(ticker, sector, ts, comp)
    

    # stocks_post_id = db['stocks'].insert_one(stocks_post)
    stocks_collection.insert(stocks_post)
    counter += 1
    print(f'{comp} -> {counter}/{n} done...')
    time.sleep(sleep_period)

