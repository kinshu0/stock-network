from feed_data import *
from calc_handler import *
from graph_modeler import *

# API_key = 'HB8BGAK56N2T7BBE'
# file_name = 'symbols.csv'
# n = 25 
# sleep_period = 13

# feed_to_db(file_name, API_key)

start = "20071201"
end = "20090630"
z = fetch_multiple_matrix_ts(ticker_list, start, end)
k = calc_mesh(z)

add_stonks(z, k)

export_graph()
