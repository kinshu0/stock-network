from calc import *
from server import *

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
    for x in tickers:
        a.append( fetch_matrix_ts(x, start, end) )
    b = list(zip(tickers, a))
    return b

# def insert_mesh(calculated_mesh):
#     for x in calculated_mesh:
#         post = {
#             'xy': [x[0], x[1]],
#             'r': x[2][1:]
#         }
#         server.association_collection.insert(post)

# def new_mesh_insert(calculated_mesh):
#     data = {}
#     for x in calculated_mesh:
#         post = {
#             'a': x[0],
#             'b': x[1],
#             'r': [y for y in x[2]]
#         }
#         data.update(post)

# start = "20071201"
# end = "20090630"
# z = fetch_multiple_matrix_ts(ticker_list)#, start, end)
# k = calc_mesh(z)
# print(k)