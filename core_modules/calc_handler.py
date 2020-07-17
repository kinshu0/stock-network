from core_modules.calc import *
from core_modules.mongo_driver import *
# from core_modules.server import *

from itertools import combinations

server = Default_Server()

ticker_list = server.stock_collection.tickers_list()


def feed_to_dict(booolla):
    haha = dict()
    for x in booolla:
        haha.update(x)
    return haha

def fetch_matrix_ts(ticker, start=None, end=None):
    a = server.stock_collection.retrieve_ts(ticker, start, end)
    b = feed_to_dict(a)
    c = []
    for x in b.keys():
        k = b[x]
        k.insert(0, int(x))
        c.append(k)
    return c

'''
Format of output:
[
    [
        symbol, [
                    [date, open, high, low, close, volume]
                    ...
                ]
    ]
    ...
]
'''
def fetch_multiple_matrix_ts(tickers, start=None, end=None):
    a = []
    excluded_indices = []
    for x in range(len(tickers)):
        single_ts_matrix = fetch_matrix_ts(tickers[x], start, end)
        '''
        Remove tickers that don't have data for the start to end time range,
        affects: stock_returns and correlation stuff
        '''
        if len(single_ts_matrix) == 0:
            excluded_indices.append(x)
            continue
        a.append( single_ts_matrix )
    tickers_b = np.delete(tickers, excluded_indices)
    b = list(zip(tickers_b, a))
    return b

def calc_returns(data):
    a = date_sort(data)
    c = []
    for x in a:
        op = np.array(x[1][0])[1:]/np.array(x[1][-1])[1:]
        c.append(op)
    a[:, 1] = c
    q = []
    for i in range(len(a)):
        q.append(([a[i][0], *a[i][1]]))
    return q
