from calc_handler import *

from server import *
# import client

start = "20190101"
end = "20201231"


# start = '20180101'
# end = '20191231'

z = fetch_multiple_matrix_ts(ticker_list, start, end)

# final_maybe = calc_mesh(z)
# print(len(final_maybe))

# server.mesh_collection.create_mesh(final_maybe, start, end)

# a = server.dates_collection.retrieve_date(start, end)
# a = server.mesh_collection.retrieve_mesh(start, end)
# a = client.retrieve_mesh(start, end)
# b = [x for x in a]
# print(len(b))
# print(a[1:5])


# import pandas as pd
# df = pd.DataFrame(a, columns=['Symbol1', 'Symbol2', 'r_open', 'r_high', 'r_low', 'r_close', 'r_volume'])
# print(df)

# a = link_relatives(z)
# # b = a[:, 1]
# c = []
# for x in a[:, 1]:
#     c.append([y[2:] for y in x])
# a[:, 1] = c
# b = a[:, 1]
# b = 
# print(a[0])


# a = date_sort(z)
# print(len(a[0][1]))
# c = []

# for x in a:
#     op = np.array(x[1][0])[1:]/np.array(x[1][-1])[1:]
#     c.append(op)

# a[:, 1] = c
# q = []
# for i in range(len(a)):
#     # a[i] = list([a[i][0], *a[i][1]])
#     q.append(([a[i][0], *a[i][1]]))
# print(q)
print(calc_returns(z))