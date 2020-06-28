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

    numerator = len(first) * sum(  np.multiply(first, second)) - sum(first) * sum(second)
    denominator  = (
        math.sqrt(  len(first) * sum( np.square(first) ) - math.pow( sum(first), 2 )  ) * 
        math.sqrt(  len(first) * sum( np.square(second) ) - math.pow( sum(second), 2 )  )
        )
    return numerator/denominator


'''
Data de-trending using Link Relatives
'''
def link_relatives(rows):
    end = len(rows) - 1
    result = []
    for x in range(end):
        result.append(rows[x+1]/rows[x])
    return result


def do(first, second):
    detrending = link_relatives(first), link_relatives(second)
    return calc_pearson_coefficient(*detrending)

def calc_mesh(data):#, start, end):
    data_combinations = list(combinations(data, 2))
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

        '''
        temp: fix this later
        -----------------
        '''
        if len(ts1) == 0 or len(ts2) == 0:
            continue
        if not len(ts1) == len(ts2):
            # raise Exception("Yeaaaa...Nahhh. They don't correspond bro")
            continue
        '''
        -----------------
        '''

        close_1 = [x[4] for x in ts1]
        close_2 = [x[4] for x in ts2]

        r = do(close_1, close_2)
        result.append( [i[0][0], i[1][0], r] )

    return result

# print(calc_pearson_coefficient(first, second))
# print(do(first, second))