import core_modules.server as server
# from server import *

file_name = 'lol.csv'

initiate_default_dance = server.Default_Server()

googoogaagaa = initiate_default_dance.association_collection.tickers_list()


rows = []

rows.append(f';{";".join(googoogaagaa)}')

for x in googoogaagaa:
    haha = []
    for y in googoogaagaa:
        z = initiate_default_dance.association_collection.retrieve_association(x, y)
        if z == None:
            z = {'r': 0}
        haha.append(z['r'])
        
    gurl = [x]
    gurl.extend(haha)
    gurl = [str(k) for k in gurl]
    bill = ';'.join(gurl)
    rows.append(bill)
    

final = '\n'.join(rows)

with open(file_name, 'w') as f:
    f.write(final)
