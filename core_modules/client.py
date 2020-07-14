from core_modules.server import *
from core_modules.calc_handler import *

def initialize_dates_data(start, end):
    # start = str(start)
    # end = str(end)
    x = server.dates_collection.retrieve_date(start, end)
    if x == None:
        data = fetch_multiple_matrix_ts(ticker_list, start, end)
        mesh_data = calc_mesh(data)
        returns_data = calc_returns(data)

        date_id = server.dates_collection.insert({
            'start': start,
            'end': end
        })
        server.mesh_collection.create_mesh(mesh_data, start, end)
        server.returns_collection.create_returns(returns_data, start, end)

def retrieve_mesh(start, end):
    start = str(start)
    end = str(end)
    initialize_dates_data(start, end)
    # x = server.dates_collection.retrieve_date(start, end)
    # if x == None:
        # data = fetch_multiple_matrix_ts(ticker_list, start, end)
        # mesh_data = calc_mesh(data)
        # server.mesh_collection.create_mesh(mesh_data, start, end)

    json_mesh = server.mesh_collection.retrieve_mesh(start, end)
    a = []
    for x in json_mesh:
        a.append(list(x.values()))
    b = []
    for x in a:
        b.append([x[0], x[1], *x[2]])
    return b

def retrieve_returns(start, end):
    start = str(start)
    end = str(end)
    initialize_dates_data(start, end)
    # x = server.dates_collection.retrieve_date(start, end)
    # if x == None:
        # data = fetch_multiple_matrix_ts(ticker_list, start, end)
        # returns_data = link_relatives(data)
        # server.mesh_collection.create_mesh(mesh_data, start, end)
    json_mesh = server.returns_collection.retrieve_returns(start, end)
    a = []
    for x in json_mesh:
        a.append(list(x.values()))
    b = []
    for x in a:
        b.append([x[0], *x[1]])

    return b

def retrieve_ticker_attributes():
    a = server.stock_collection.retrieve_attributes()
    b = [list(x.values()) for x in a]
    return b
