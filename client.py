from server import *
from calc_handler import *

def retrieve_mesh(start, end):
    x = server.dates_collection.retrieve_date(start, end)
    if x == None:
        data = fetch_multiple_matrix_ts(ticker_list, start, end)
        mesh_data = calc_mesh(data)
        server.mesh_collection.create_mesh(mesh_data, start, end)
    return server.mesh_collection.retrieve_mesh(start, end)
