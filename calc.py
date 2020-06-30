import numpy as np
import math
from itertools import combinations



# first = [0, 32, 2, 230, 32]
# second = [2, 32, 4, 54, 2]


'''
Pearson Correlation Definition:
This takes two lists and calculates the coefficient
PRE PROCESS THE DATA BEFORE PERFORMING THIS
'''
def calc_pearson_coefficient(first, second):
    n = len(first)
    numerator = n * np.sum(np.multiply(first, second), axis=0) - np.sum(first, axis=0) * np.sum(second, axis=0)
    d1 =  n * np.sum(np.square(first), axis=0) - np.square( np.sum(first, axis=0) )
    d2 =  n * np.sum(np.square(second), axis=0) - np.square( np.sum(second, axis=0) )
    a = np.multiply(d1, d2)
    b = [math.sqrt(x) for x in a]
    r = numerator/b
    return r

'''
Data de-trending using Link Relatives
'''
def link_relatives(data):
    for j in range(len(data)):
        end = len(data[j][1]) - 1
        result = []
        for x in range(end):
            r = np.array(data[j][1][x+1][1:])
            q = np.array(data[j][1][x][1:])
            try:
                s = q/r
            except TypeError:
                s = [None, None, None, None, None]
            result.append( s )
        del data[j][1][-1]
        k = np.asarray(data[j][1])
        k[:, 1:] = result
        data[j][1] = k
    return data

'''
Inserts None for date that doesn't exist and sorts the time series data by date
'''
def date_match_multiple(data):
    data = np.asarray(data)
    a = data[:, 1]
    b = []
    for x in a:
        b.append(np.asarray(x)[:, 0])
    c = set().union(*b)
    d = [int(x) for x in sorted(c, reverse=True)]
    
    for i in d:
        for j in range(len(b)):
            if not i in b[j]:
                data[j][1].append([i, None, None, None, None, None])

    for x in data:
        to_sort = x[1]
        x[1] = sorted(to_sort, key=lambda date: date[0], reverse=True)

    return data

def remove_nones(data):
    raw_indices = []
    a = len(data)
    b = len(data[0][1])
    for x in range(a):
        for y in range(b):
            if None in data[x][1][y]:
                for z in range(a):
                    raw_indices.append(y)
    indices = list(set().union(raw_indices))
    for p in range(a):
        data[p][1] = np.delete(data[p][1], indices, axis=0)
    return data

def calc_mesh(data):
    a = date_match_multiple(data)
    b = link_relatives(a)
    c = remove_nones(b)

    data_combinations = list(combinations(c, 2))
    '''
    [
        [symbol, [ts_data]], [symbol, [ts_data]]
        ...
    ]
    '''
    result = []
    for i in data_combinations:
        ts1 = i[0][1]
        ts2 = i[1][1]
        r = calc_pearson_coefficient(ts1, ts2)
        result.append( [i[0][0], i[1][0], r] )

    return result