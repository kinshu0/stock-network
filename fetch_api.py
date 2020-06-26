
# 

from alpha_vantage.timeseries import TimeSeries

# ts = TimeSeries(key)

# goog = ts.get_weekly(symbol='GOOG')
# msft = ts.get_weekly(symbol='MSFT')

# with open('temp.txt', 'w') as f:
#     f.write(f'{[goog, msft]}')
# f.close()


'''
Created this class with intention to expand to
usage of multiple APIs.
'''
class Fetch:

    '''
    Alpha Vantage API
    Format of the unmodified return for this is going to be:
    (
        {da data},
        {da metadata}
    )
    '''
    def alpha(self, symbol, time_interval=0):
        ts = TimeSeries(self.key)
        stock = ts.get_weekly(symbol=symbol)

        return stock

        

    def __init__(self, key, api_name=alpha):
        self.fetch = api_name
        self.key = key


