from calc_handler import *

from server import *
import client

start = "20190101"
end = "20201231"


# start = '20180101'
# end = '20191231'

# z = fetch_multiple_matrix_ts(ticker_list, start, end)

# final_maybe = calc_mesh(z)
# print(len(final_maybe))

# server.mesh_collection.create_mesh(final_maybe, start, end)

# a = server.dates_collection.retrieve_date(start, end)
# a = server.mesh_collection.retrieve_mesh(start, end)
a = client.retrieve_mesh(start, end)
b = [x for x in a]
print(len(b))
print(b[1:5])