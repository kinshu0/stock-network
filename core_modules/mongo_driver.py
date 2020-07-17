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

    def retrieve_attributes(self):
        return self.collection.find({}, {'_id': 0, 'ts': 0})


class Dates:
    def __init__(self, database):
        self.db = database
        self.collection = self.db['dates']
    def insert(self, post):
        return self.collection.insert_one(post).inserted_id
    def retrieve_date(self, start, end):
        query = {
            'start': start,
            'end': end
        }
        return self.collection.find_one(query, {'_id': 1})

class Mesh:
    def __init__(self, database, dates):
        self.db = database
        self.collection = self.db['mesh']
        self.dates_collection = dates
        
    def insert(self, post):
        self.collection.insert_one(post)

    def create_mesh(self, data, start, end):
        date_id = self.dates_collection.retrieve_date(start, end)['_id']
        for x in data:
            post = {
                'a': x[0],
                'b': x[1],
                'r': [y for y in x[2]],
                'ref': date_id
            }
            self.insert(post)
            
    def retrieve_mesh(self, start, end):
        date = self.dates_collection.retrieve_date(start, end)
        query = {'ref': date['_id']}
        return self.collection.find(query, {'_id': 0, 'ref': 0})
        

class Returns:
    def __init__(self, database, dates):
        self.db = database
        self.collection = self.db['returns']
        self.dates_collection = dates

    def insert(self, post):
        self.collection.insert_one(post)

    def create_returns(self, data, start, end):
        date_id = self.dates_collection.retrieve_date(start, end)['_id']
        for x in data:
            post = {
                'a': x[0],
                'returns': [y for y in x[1:]],
                'ref': date_id
            }
            self.insert(post)
    def retrieve_returns(self, start, end):
        date = self.dates_collection.retrieve_date(start, end)
        query = {'ref': date['_id']}
        return self.collection.find(query, {'_id': 0, 'ref': 0})

    '''
    Inserts data or updates the correlation data
    if it already exists
    '''


'''
Define and instantiate database schema
'''
class Default_Server:
    def __init__(self):
        self.url = 'mongodb://localhost:27017/'
        self.database_name = 'dev3'
        self.mongo_connection = Database(self.url, self.database_name)
        self.db = self.mongo_connection.db

        '''
        Collections:
        '''
        self.stock_collection = Stock(self.db)
        self.dates_collection = Dates(self.db)
        self.mesh_collection = Mesh(self.db, self.dates_collection)
        self.returns_collection = Returns(self.db, self.dates_collection)

server = Default_Server()