from calc import *
from server import *

from itertools import combinations

server = Default_Server()

ticker_list = server.stock_collection.tickers_list()

start = "20071201"
end = "20090630"

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

def calculate_insert_mesh(list_of_tickers, start, end):
    ticker_combinations = list(combinations(list_of_tickers, 2))
    
    c = 0
    n = len(ticker_combinations)

    result = []
    '''
    This part is for processing the data so it's a single matrix formatted as
    columns: open high low close volume
    rows: each corresponding time
    '''
    for i in ticker_combinations:
        first = server.stock_collection.retrieve_ts(i[0], start, end)
        second = server.stock_collection.retrieve_ts(i[1], start, end)

        first_dict = feed_to_dict(first)
        second_dict = feed_to_dict(second)


        if len(first_dict) == 0 or len(second_dict) == 0:
            continue
        if not len(first_dict) == len(second_dict):
            # raise Exception("Yeaaaa...Nahhh. They don't correspond bro")
            continue
        
        keys = first_dict.keys()

        vals_1 = []
        vals_2 = []

        for x in keys:
            try:
                vals_2.append(second_dict[x])
                vals_1.append(first_dict[x])
            except KeyError:
                continue

        '''
        For now I'm only performing analysis on the closing price,
        add more later
        '''
        close_prices_1 = [x[3] for x in vals_1]
        close_prices_2 = [x[3] for x in vals_2]

        r = do(close_prices_1, close_prices_2)

        post = {
            'xy': i,
            'r': r
        }
        result.append(post)
    return result

        # server.association_collection.insert(post)

        # c += 1
        # print(f'{c}/{n} {i} Done')

# calculate_insert_mesh(ticker_list, start, end)

def insert_mesh(calculated_mesh):
    for post in calculated_mesh:
        server.association_collection.insert(post)

z = fetch_multiple_matrix_ts(ticker_list, start, end)
k = calc_mesh(z)
print(k)

