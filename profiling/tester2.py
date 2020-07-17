from core_modules.calc_handler import *
import pickle

data = pickle.load(open('pairs.dat', 'rb'))

# matched = [date_match_pair(x) for x in data]
print(len(data))