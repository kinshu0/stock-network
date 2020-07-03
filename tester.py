from calc_handler import *

start = "20190101"
end = "20203131"
z = fetch_multiple_matrix_ts(ticker_list, start, end)
# k = date_sort(z)

def just_dates(data, q, n):
    for x in range(n):
        # print(data[q][1][x][0])
        print(data[q][1][x][0:2])

# just_dates(k, 0, 10)


k = link_relatives(z)


# print(len(z[0][1]))
# print(len(k[0][1]))

# just_dates(k,0,10)

'''
Use with one edge at a time, if used for multiple nodes,
there will be data loss
'''
# def date_match_multiple(data):

#     # extract from dates out of data

#     data = np.asarray(data)
#     '''
#     [
#         [
#             [ts1],
#             [ts2]
#         ],
#         [
#             [ts1],
#             [ts2],
#             [ts3]
#         ]
#     ]
#     '''
#     a = data[:, 1]
#     b = []
#     # end = 0
#     for x in a:
#         b.append(np.asarray(x)[:, 0])
#         # end = max(end, len(x))

#     c = []
#     for x in a:
#         c.append(np.asarray(x)[:, 1])
#     # -----------------------
#     # get first matching indices

#     first_matching_indices = []
#     smallest_start = min([q[0] for q in b])

#     for x in range( len(b)):
#         done = False
#         for i in range(len(b[x])):
#             if smallest_start == b[x][i]:
#                 first_matching_indices.append(i)
#                 done = True
#                 break
#         if not done:
#             raise Exception('Gas gas gas')

#     # ----------------------------------

#     last_matching_indices = []
#     largest_end = max([q[-1] for q in c])
    
#     for x in range( len(c)):
#             done = False
#             for i in range(-1, -len(c[x]), -1):
#                 if largest_end == c[x][i]:
#                     last_matching_indices.append(i + len(c[x]) + 1)
#                     done = True
#                     break
#             if not done:
#                 raise Exception('Gas gas gas v2')

#     # -----------------------------
#     trimmed_data = []
#     wee = 0
#     for k in a:
#         trimmed_data.append(k[ first_matching_indices[wee]:last_matching_indices[wee] ])
#         wee += 1

#     # -------------------------------
    
#     return trimmed_data


def diff(first, second):
    second = set(second)
    return [item for item in first if item not in second]

# def date_match_multiple(data):
#     data = np.asarray(data)
#     a = data[:, 1]
#     b = []
#     for x in a:
#         b.append((np.asarray(x)[:, 0]))
#     c = []
#     for x in a:
#         c.append((np.asarray(x)[:, 1]))

#     good_len = min([len(x) for x in a])
#     # b = list(b)
#     same1 = set(b[0]).intersection(*b)
#     same2 = set(c[0]).intersection(*c)

#     indices = []
#     for x in range(len(a)):
#         state = len(a[x])
#         if len(a[x]) == good_len:
#             continue
#         for y in range(len(a[x])):
#             if 

#     return same1, same2


# d = date_match_multiple(k[0:10])


def date_match_pair(data):
    data = np.asarray(data)
    a = data[:, 1]
    f = []
    t = []
    # d = [np.asarray(x)[:, 0:2] for x in a]
    for x in a:
        f.append((np.asarray(x)[:, 0]))
    for x in a:
        t.append((np.asarray(x)[:, 1]))
    d = []
    for x in range(len(f)):
        d.append(list(zip(f[x], t[x])))

    differences = diff(d[0], d[1])
    # return differences
    # return f, t
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
    # te = a[0]
    if len(i1) > 0:
        final1 = np.delete(a[0], i1, axis=0)
    else:
        final1 = a[0]
    if len(i2) > 0:
        final2 = np.delete(a[1], i2, axis=0)
    else:
        final2 = a[1]
    
    data[:, 1] = [final1, final2]
        # return indices1, indices2
    return data

z = date_match_pair(k[0:2])
# print(list(zip(z[0][0], z[1][0])))
# print()
for x in z:
    print(len(x[1]))

# # x = 1

# # # print(f'{len(b[0])}         {len(b[1])}')
# # # print(f'First: {[int(x) for x in b[0][0][0:2]]} Last: {[int(x) for x in b[0][-1][0:2]]}\nFirst: {[int(x) for x in b[1][0][0:2]]} Last: {[int(x) for x in b[1][-1][0:2]]}')
# # # print(b[x][1:]==b[x+1])


# # a = [x[0] for x in d[0]]
# # aE = [x[1] for x in d[0]]
# # b = [x[0] for x in d[1]]
# # bE = [x[1] for x in d[1]]
# # #[x for x in b[0]]
# # # a_ = [int(x[1]) for x in b[0]]
# # # j = zip(a, a_)
# # # b = [int(x[0]) for x in b[1]]
# # # b_ = [int(x[1]) for x in b[1]]
# # # t = zip(b, b_)

# # # print(a, aE, b, bE)
# # # print(len(a), len(aE), len(b), len(bE))
# # print(diff(a, b))