import core_modules.feed_data as feed_data

API_key = 'HB8BGAK56N2T7BBE'
file_name = 'symbols.csv'
# n = 25 
sleep_period = 13

feed_data.feed_to_db(file_name, API_key, start=93)