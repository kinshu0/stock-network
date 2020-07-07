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
        z = x.split(',')
        symbols.append( z[0] )
        names.append( z[1] )
        sector.append( z[2] )

    return symbols, names, sector

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
        new_key = x.replace('-', '')
        ts_processed.update({ new_key: ts[x]})

    ts_processed2 = []
    for x in ts_processed:
        ts_processed2.append(       # convert dict of dicts to array of dicts
            {x: ts_processed[x]}
        )

    stocks_post = {
        'ticker': ticker,
        'sector': sector,
        'ts': ts_processed2,
        'comp': comp
    }
    return stocks_post


# # url = 'mongodb://localhost:27017/'
# # database_name = 'dev2'
# # mongo_connection = Database(url, database_name)
# # db = mongo_connection.db
# # stocks_collection = Stock(db)


# API_key = 'HB8BGAK56N2T7BBE'
# file_name = 'symbols.csv'
# n = 25 
# sleep_period = 13

'''
Fetches data about the specified tickers in file_name and feeds
to the database, sleep_period is the amount of time to wait before
fetching next ticker from API, n is the number of tickers to fetch from
file
'''
def feed_to_db(file_name, API_key, n=None, stocks_collection=server.stock_collection, sleep_period=13):
    fetcher = Fetch(API_key)

    index_data = read_index_data(file_name)

    counter = 1

    if not n==None:
        indices = np.linspace(0, len(index_data[0]), num=n, dtype=int)
    else:
        n = len(index_data[0])
        indices = range(n)

    for i in indices:
        ticker = index_data[0][i]
        comp = index_data[1][i]
        sector = index_data[2][i]
        ts = fetcher.alpha(ticker)[0]
        stocks_post = api_to_db_format(ticker, sector, ts, comp)
        # stocks_post_id = db['stocks'].insert_one(stocks_post)
        stocks_collection.insert(stocks_post)
        print(f'{comp} -> {counter}/{n} done...')
        time.sleep(sleep_period)
        counter += 1
