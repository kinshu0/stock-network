from core_modules.calc_handler import *
from itertools import combinations
import pickle

start = "20190101"
end = "20191231"

z = fetch_multiple_matrix_ts(ticker_list, start, end)

a = link_relatives(z)

data_combinations = list(combinations(a, 2))

# np.savetxt('pairs.dat', data_combinations)
pickle.dump(data_combinations, open('pairs.dat', 'wb'))

# with open('pairs', 'w') as f:
#     f.write(f'{data_combinations}')

# matched = [date_match_pair(x) for x in data_combinations]


# with open('test_temp2', 'w') as f:
#     f.write(f'{matched}')