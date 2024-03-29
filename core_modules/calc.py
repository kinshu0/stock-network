import numpy as np
import math
from itertools import combinations


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
    b = np.sqrt(a)
    r = numerator/b
    return r


'''
Sort Raw data based on date 
'''
def date_sort(data):
    data = np.asarray(data)
    a = data[:, 1]
    for i in range(len(a)):
        b = a[i]
        a[i] = sorted(b, reverse=True, key= lambda date: date[0])
    data[:, 1] = a
    return data

'''
Data de-trending using Link Relatives
NEW
'''
def link_relatives(data):
    data = date_sort(data)

    for j in range(len(data)):
        end = len(data[j][1]) - 1
        result = []
        for x in range(end):
            r = np.array(data[j][1][x+1][1:])
            q = np.array(data[j][1][x][1:])
            if r[-1] == 0:
                r[-1] = 1
            a = np.divide(q, r)
            s = [data[j][1][x][0], data[j][1][x+1][0], *a]
            result.append( s )
        del data[j][1][-1]
        k = np.resize(np.asarray(data[j][1]), (len(result),7))
        k[:, 0:] = result
        data[j][1] = k
    return data

'''
Inserts None for date that doesn't exist and sorts the time series data by date
NEW
'''
def diff(first, second):
    second = set(second)
    return [item for item in first if item not in second]

def date_match_pair(data):
    data = np.asarray(data)
    a = data[:, 1]
    f = []
    t = []
    for x in a:
        f.append((np.asarray(x)[:, 0]))
    for x in a:
        t.append((np.asarray(x)[:, 1]))
    d = []
    for x in range(len(f)):
        d.append(list(zip(f[x], t[x])))

    d1 = diff(d[0], d[1])
    d2 = diff(d[1], d[0])
    if len(d1) > len(d2):
        differences = d1
    else:
        differences = d2

    indices1 = []
    indices2 = []
    for x in differences:
        for i in range(len(d[0])):
            if x[0]==d[0][i][1] or x[0]==d[0][i][0] or x[1]==d[0][i][1] or x[1]==d[0][i][0]:
                indices1.append(i)
        for i in range(len(d[1])):
            if x[0]==d[1][i][0] or x[0]==d[1][i][1] or x[1]==d[1][i][1] or x[1]==d[1][i][0]:
                indices2.append(i)

    i1 = list(set().union(indices1))
    i2 = list(set().union(indices2))
    
    if len(i1) > 0:
        final1 = np.delete(a[0], i1, axis=0)
    else:
        final1 = a[0]
    if len(i2) > 0:
        final2 = np.delete(a[1], i2, axis=0)
    else:
        final2 = a[1]
        
    if not len(final1) == len(final2):
        raise Exception('PP')
    
    data[:, 1] = [final1, final2]
    
    return data


def calc_mesh(data):
    a = link_relatives(data)
    data_combinations = list(combinations(a, 2))
    matched = [date_match_pair(x) for x in data_combinations]

    '''
    [
        [symbol, [ts_data]], [symbol, [ts_data]]
        ...
    ]
    '''
    result = []
    for i in matched:
        ts1 = i[0][1][:, 2:]
        ts2 = i[1][1][:, 2:]
        r = calc_pearson_coefficient(ts1, ts2)
        result.append( [i[0][0], i[1][0], r] )

    return result

# from numba import jit_module
# jit_module(nopython=True)#, error_model='numpy')