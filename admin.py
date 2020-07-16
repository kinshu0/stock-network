import core_modules.feed_data as feed_data

API_key = 'HB8BGAK56N2T7BBE'
file_name = 'symbols.csv'
# n = 25 
sleep_period = 13

feed_data.feed_to_db(file_name, API_key)

import core_modules.client as client
from itertools import combinations

print('Data Fetched, Next: Calculations')
dates = list(range(2010, 2020))
date_combinations = combinations(dates, 2)
date_ranges = []

for x in date_combinations:
    if x[1] > x[0]:
        date_ranges.append( (x[1], x[0]) )
    else:
        date_ranges.append( x )

date_ranges_final = []
for x in date_ranges:
    date_ranges_final.append( (f'{x[0]}0101', f'{x[1]}1231') )

c = 1
for x in date_ranges_final:
    client.retrieve_mesh(x[0], x[1])
    print(f'{x[0]} -> {x[1]} {c}/{len(date_ranges_final)} done')
    c += 1