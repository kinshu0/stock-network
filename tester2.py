from calc_handler import *

start = "20190101"
end = "20203131"
z = fetch_multiple_matrix_ts(ticker_list, start, end)

final_maybe = calc_mesh(z)
print(len(final_maybe))