import numpy as np
import math



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


def do(first, second):
    return calc_pearson_coefficient(first, second)

# print( calc_pearson_coefficient(first, second) )