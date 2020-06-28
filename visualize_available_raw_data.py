from server import *
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

lot = server.stock_collection.tickers_list()

ts = {}

'''
Cast date keys to integers
'''
for x in lot:
    y = server.stock_collection.retrieve_ts(x)
    ud = {}
    for k in y:
        haha = int(list(k.keys())[0])
        ud.update({
            int(list(k.keys())[0]): list(k.values())[0]
        })

    ts.update({
        x: ud
    })

# with open('temp', 'w') as f:
#     f.write(f'{ts}')

'''
Separate Variables:
tickers = holds the x lables of each ticker,
dates = [
    [], Holds all the dates each ticker
    []  has available data for
]
'''

tickers = list(ts.keys())

vals = ts.values()

dates = []
for x in vals:
    dates.append(
        list(x.keys())
    )
c = 0
for x in dates:
    print(f'{tickers[c]}: {len(x)}')
    c += 1


okay = list(zip(tickers, dates))

final = []

for i in okay:
    for j in i[1]:
        final.append((i[0], j))

df = pd.DataFrame(data=final, columns=['Ticker', 'Date'])

sns.catplot(x='Ticker', y='Date', jitter= False, data=df)
plt.show()