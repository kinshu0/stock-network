from alpha_vantage.timeseries import TimeSeries

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
        stock = ts.get_daily(symbol=symbol)

        return stock
        

    def __init__(self, key, api_name=alpha):
        self.fetch = api_name
        self.key = key