from pymongo import MongoClient


class Database:
    def __init__(self, url, DB_name):
        self.client = MongoClient(url)
        self.db = self.client[DB_name]


class Stock:
    def __init__(self, database):
        self.db = database
        self.collection = self.db['stocks']
    
    def retrieve_ticker(self, ticker):
        return self.collection.find_one({'ticker':ticker})

    def tickers_list(self):
        stuff = []
        for x in self.collection.find({}, {'_id': 0, 'ticker': 1}):
            stuff.append(x['ticker'])
        return stuff

    def retrieve_ts(self, ticker, start_date=None, stop_date=None):
        untrimmed = self.collection.find_one(
            {'ticker':ticker},
            {'_id': 0, 'ts': 1}
            )['ts']
        return self.trim_data(untrimmed, start_date, stop_date)

    '''
    Inserts data or updates the time series
    if the ticker data already exists
    '''
    def insert(self, post):
        if self.collection.count( {'ticker': post['ticker']} ) == 0:
            return self.collection.insert_one(post)
        
        else:
            return self.collection.update(
                {'ticker': post['ticker']}, #query
                {'$addToSet': {'ts': { '$each': post['ts'] } } }
            )

    
    '''
    Internal Functions, probably not gonna be used outside of this
    '''
    def trim_data(self, thing, start=None, end=None):
        if start == end == None:
            return thing

        t = []
        for x in thing:
            b = list(x.keys())[0]
            if b>= start and b <= end:
                t.append(x)
        return t


class Association:
    def __init__(self, database):
        self.db = database
        self.collection = self.db['associations']

    def tickers_list(self):
        stuff_and_things = self.collection.find()
        result = []
        for x in stuff_and_things:
            for i in x['xy']:
                if not i in result:
                    result.append(i)
        return result
    
    def retrieve_association(self, ticker1):
        stuff_and_things = self.collection.find()
        result = []
        for x in stuff_and_things:
            if ticker1 in x['xy']:
                result.append(x)
        return result

    def retrieve_association(self, ticker1, ticker2):
        stuff_and_things = self.collection.find()
        for x in stuff_and_things:
            if ticker1 in x['xy'] and ticker2 in x['xy'] and not ticker1 == ticker2:
                return x
        return None

    '''
    Inserts data or updates the correlation data
    if it already exists
    '''
    def insert(self, post):
        self.collection.insert_one(post)


'''
Define and instantiate database schema
'''
class Default_Server:
    def __init__(self):
        self.url = 'mongodb://localhost:27017/'
        self.database_name = 'dev2'
        self.mongo_connection = Database(self.url, self.database_name)
        self.db = self.mongo_connection.db

        '''
        Collections:
        '''
        self.stock_collection = Stock(self.db)
        self.association_collection = Association(self.db)

