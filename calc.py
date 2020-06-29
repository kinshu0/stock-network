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
# # # def calc_pearson_coefficient(first, second):

# # #     numerator = len(first) * sum(  np.multiply(first, second)) - sum(first) * sum(second)
# # #     denominator  = (
# # #         math.sqrt(  len(first) * sum( np.square(first) ) - math.pow( sum(first), 2 )  ) * 
# # #         math.sqrt(  len(first) * sum( np.square(second) ) - math.pow( sum(second), 2 )  )
# # #         )
# # #     return numerator/denominator
def calc_pearson_coefficient(first, second):
    n = len(first)
    numerator = n * np.sum(np.multiply(first, second), axis=0) - np.sum(first, axis=0) * np.sum(second, axis=0)
    # d1 = np.sqrt(  n * np.sum(np.square(first), axis=0) - np.square( np.sum(first, axis=0) )  )
    # d2 = np.sqrt(  n * np.sum(np.square(second), axis=0) - np.square( np.sum(second, axis=0) )  )
    d1 =  n * np.sum(np.square(first), axis=0) - np.square( np.sum(first, axis=0) )
    d2 =  n * np.sum(np.square(second), axis=0) - np.square( np.sum(second, axis=0) )
    a = np.multiply(d1, d2)
    b = [math.sqrt(x) for x in a]
    r = numerator/b
    return r

'''
Data de-trending using Link Relatives
'''
# # # def link_relatives(rows):
# # #     end = len(rows) - 1
# # #     result = []
# # #     for x in range(end):
# # #         result.append(rows[x+1]/rows[x])
# # #     return result
def link_relatives(data):
    for j in range(len(data)):
    # for i in data:
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
        # # # ab = data[j][1][-1] 
        del data[j][1][-1]
        # # # work = np.asarray(data[j][1])[:, 1:]
        k = np.asarray(data[j][1])
        k[:, 1:] = result
        # # # np.asarray(data[j][1])[:, 1:] = result
        # # # data[j][1][:][1:] = result
        # # # data[j][1][:, 1:] = result
        data[j][1] = k
    return data
        


def do(first, second):
    detrending = link_relatives(first), link_relatives(second)
    return calc_pearson_coefficient(*detrending)

'''
Inserts None for date that doesn't exist and sorts the time series data by date
'''
def date_match_multiple(data):
    data = np.asarray(data)
    a = data[:, 1]
    b = []
    for x in a:
        # # # x = np.asarray(x)
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
    # # # data = np.asarray(data)
    # # # x = type(data)
    raw_indices = []
    a = len(data)
    b = len(data[0][1])
    for x in range(a):
        for y in range(b):
            if None in data[x][1][y]:
                for z in range(a):
                    # # # data[z][1][y] = np.ma.masked
                    raw_indices.append(y)
    indices = list(set().union(raw_indices))
    # # # mask_on = np.zeros(b)
    # # # for i in indices:
    # # #     mask_on[i] = 1
    for p in range(a):
        data[p][1] = np.delete(data[p][1], indices, axis=0)
    return data

# # # def calc_mesh(data):#, start, end):
# # #     data_combinations = list(combinations(data, 2))
# # #     '''
# # #     [
# # #         [symbol, [ts_data]], [symbol, [ts_data]]
# # #         ...
# # #     ]
# # #     '''
# # #     result = []
# # #     for i in data_combinations:
# # #         ts1 = i[0][1]
# # #         ts2 = i[1][1]

# # #         '''
# # #         temp: fix this later
# # #         -----------------
# # #         '''
# # #         if len(ts1) == 0 or len(ts2) == 0:
# # #             continue
# # #         if not len(ts1) == len(ts2):
# # #             # raise Exception("Yeaaaa...Nahhh. They don't correspond bro")
# # #             continue
# # #         '''
# # #         -----------------
# # #         '''
# # #         '''
# # #         temp fix 1: Only perform calculations on matching dates
# # #         -----------------
# # #         '''
# # #         close_1 = [x[4] for x in ts1]
# # #         close_2 = [x[4] for x in ts2]
# # #         # close_1 = []
# # #         # close_2 = []
# # #         # for x, y in ts1, ts2:

# # #         '''
# # #         -----------------
# # #         '''


# # #         r = do(close_1, close_2)
# # #         result.append( [i[0][0], i[1][0], r] )

# # #     return result

def calc_mesh(data):###, start, end):
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
        # # # '''
        # # # temp: fix this later
        # # # -----------------
        # # # '''
        # # # if len(ts1) == 0 or len(ts2) == 0:
        # # #     continue
        # # # if not len(ts1) == len(ts2):
        # # #     # raise Exception("Yeaaaa...Nahhh. They don't correspond bro")
        # # #     continue
        # # # '''
        # # # -----------------
        # # # '''
        # # # '''
        # # # temp fix 1: Only perform calculations on matching dates
        # # # -----------------
        # # # '''
        # close_1 = [x[4] for x in ts1]
        # close_2 = [x[4] for x in ts2]
        # close_1 = []
        # close_2 = []
        # for x, y in ts1, ts2:

        # # # '''
        # # # -----------------
        # # # '''


        # r = do(close_1, close_2)
        result.append( [i[0][0], i[1][0], r] )

    return result

# print(calc_pearson_coefficient(first, second))
# print(do(first, second))