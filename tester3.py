from calc_handler import *

from server import *
import client

start = "20190101"
end = "20201231"

print(client.retrieve_ticker_attributes())
# for x in client.retrieve_ticker_attributes():
#     print(x.values())
