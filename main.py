from feed_data import *
from calc_handler import *
from graph_modeler import *

# API_key = 'HB8BGAK56N2T7BBE'
# file_name = 'symbols.csv'
# n = 25 
# sleep_period = 13

# feed_to_db(file_name, API_key)

start = "20190101"
end = "20203131"
z = fetch_multiple_matrix_ts(ticker_list, start, end)
k = calc_mesh(z)

add_stonks(ticker_list, k)

export_graph()
