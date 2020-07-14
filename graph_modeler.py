
import networkx as nx
import plotly.graph_objs as go

import numpy as np
import pandas as pd
from colour import Color

import client


stock_attributes = client.retrieve_ticker_attributes()

palette = [
    'rgb(254,255,88)',
    'rgb(255,170,40)',
    'rgb(255,25,95)',
    'rgb(176,77,221)',
    'rgb(80,233,255)',
    'rgb(126,234,188)',
    'rgb(255,201,216)',
    'rgb(0.9,0.859,0.039)',
    'rgb(0.918,0.988,0.039)',
    'rgb(0.9,0.714,0.039)',
    'rgb(0.565,0.925,0.035)',
    'rgb(255, 255, 255)'
]


def diff(first, second):
    second = set(second)
    return [item for item in first if item not in second]

def network_graph(yearRange, ticker_to_search, threshold=0.6, mode='Sector'):

    start = int(f'{yearRange[0]}0101')
    end = int(f'{yearRange[1]}1231')
    # start = yearRange[0]
    # end = yearRange[1]

    mesh = client.retrieve_mesh(start, end)

    stock_returns = client.retrieve_returns(start, end)
    return_atts = pd.DataFrame(stock_returns, columns=['Ticker', 'open', 'high', 'low', 'close', 'volume'])


    
    yuh = []
    for x in stock_attributes:
        bruh = list(return_atts['Ticker'])
        if x[0] in bruh:
            yuh.append(x)

    
    stock_atts = pd.DataFrame(yuh, columns=['Ticker', 'Sector', 'Company_Name'])


    edges_df = pd.DataFrame(mesh, columns=['Symbol1', 'Symbol2', 'r_open', 'r_high', 'r_low', 'r_close', 'r_volume'])
    
    #drop edges with correlation less than threshold
    indices = []
    for index in range(0,len(edges_df)):
        if edges_df['r_close'][index] < threshold:
            indices.append(index)
            # edges_df.drop(axis=0, index=index, inplace=True)
            # continue
    edges_df.drop(indices, inplace=True)


    
    # for index in range(len(stock_atts)):
    #     if not stock_atts['Ticker'][index] in node_atts['Ticker']

    node_atts = return_atts

    # missing_data = diff(stock_atts['Ticker'], node_atts['Ticker'])

    # matching_data = pd.DataFrame(stock_atts.Ticker != missing_data)
    # matching_data = stock_atts
    # indices = []
    # for index in range(0,len(matching_data)):
        # for x in missing_data:
            # if matching_data['Ticker'][index] == x:
                # indices.append(index)
    # matching_data.drop(indices, inplace=True)

    # matching_data.sort_values('Ticker')
    # node_atts.sort_values('Ticker')

    # test = node_atts['Ticker'] == stock_atts['Ticker']

    # node_atts['Sector'] = matching_data['Sector']
    # node_atts['Company_Name'] = matching_data['Company_Name']
    # z = [x for x in node_atts['Sector']]
    # places = z.count(np.nan)
    # kt = matching_data['Ticker'][87]
    node_atts['Sector'] = stock_atts['Sector']
    node_atts['Company_Name'] = stock_atts['Company_Name']

    
    if not mode == 'close':
        uniques = set(node_atts[mode])
        color_key = {}
        i = 0
        for x in uniques:
            color_key.update({
                x: palette[i]
            })
            i+=1
    elif mode == 'close':
        uniques = set(node_atts[mode])

        l = 0.6

        neutral = Color('gray', luminance = l)
        positive = Color('green', luminance = l)
        negative = Color('red', luminance = l)
        color_step = 10
        color_range = [*list(negative.range_to(neutral, int(color_step/2))), *list(neutral.range_to(positive, int(color_step/2)))]

        # val_middle = 1
        # val_end = max( abs(max(uniques)-val_middle), abs(min(uniques) - val_middle) )

        # a = np.linspace(-val_end, val_end, color_step)

        a = np.linspace(-2, 2, color_step)

        # b = np.linspace(-val_end, val_middle, int(color_step/2))
        # c = np.linspace(val_middle, val_end, int(color_step/2))
        # a = [*b, *c]

        color_key = {}

        for k in uniques:
            color_key.update({
                k: min(a, key=lambda x:abs(x-k))
            })
        for z in color_key:
            # color_key[z] = f'rgb{color_range[int(  min(a, key=lambda x:abs(x-z)))].rgb}'
            # color_key[z] = f'rgb{color_range[  min(a, key=lambda x:abs(x-z)))].rgb}'
            color_key[z] = f'rgb{color_range[  list(a).index( color_key[z] )  ].rgb}'
            # color_key[z] = f'rgb{Color("orange").rgb}'
        
        




    ticker_set = set(client.ticker_list)


    
    G = nx.from_pandas_edgelist(edges_df, 'Symbol1', 'Symbol2', edge_attr=True)

    for col in node_atts.columns:
        if col == 'Ticker':
            continue
        nx.set_node_attributes(G, node_atts.set_index('Ticker')[col].to_dict(), col)

    # if ticker_to_search in G.nodes:
    #     pos = nx.layout.spring_layout(G, center=ticker_to_search)
    # else:
    #     pos = nx.layout.spring_layout(G)

    
    pos = nx.layout.spring_layout(G)

    for node in G.nodes:
        G.nodes[node]['pos'] = list(pos[node])



    traceRecode = []  # contains edge_trace, node_trace, middle_node_trace
    ############################################################################################################################################################
    colors = list(Color('lightcoral').range_to(Color('darkred'), len(G.edges())))
    colors = ['rgb' + str(x.rgb) for x in colors]
    colors = ['rgb(0, 0, 0)' for x in colors]



    index = 0
    for edge in G.edges:

        x0, y0 = G.nodes[edge[0]]['pos']
        x1, y1 = G.nodes[edge[1]]['pos']


        weight = float(G.edges[edge]['r_close']) / max(edges_df['r_close']) * 10

        trace = go.Scatter(x=tuple([x0, x1, None]), y=tuple([y0, y1, None]),
                           mode='lines',
                           line={'width': weight},
                           marker=dict(color=colors[index]),
                           line_shape='spline',
                           opacity=1)
        traceRecode.append(trace)
        index = index + 1
    ###############################################################################################################################################################
    node_trace = go.Scatter(x=[], y=[], hovertext=[], text=[], mode='markers+text', textposition="middle center",
                            hoverinfo="text", marker={'size': 50, 'color': []})

    index = 0
    for node in G.nodes():
        x, y = G.nodes[node]['pos']
        each_stock_return = '{:.2f}'.format((G.nodes[node]["close"] - 1) * 100)
        hovertext = (
            f'Company Name: {G.nodes[node]["Company_Name"]}<br>'
            f'Sector: {G.nodes[node]["Sector"]}<br>'
            f'Return: {each_stock_return}%'
        )

        text = node

        node_trace['marker']['color'] += tuple( [color_key[G.nodes[node][mode]]] )

        node_trace['x'] += tuple([x])
        node_trace['y'] += tuple([y])
        node_trace['hovertext'] += tuple([hovertext])
        node_trace['text'] += tuple([text])
        index = index + 1

    traceRecode.append(node_trace)
    ################################################################################################################################################################
    middle_hover_trace = go.Scatter(x=[], y=[], hovertext=[], mode='markers', hoverinfo="text",
                                    marker={'size': 20, 'color': 'LightSkyBlue'},
                                    opacity=0)

    index = 0
    for edge in G.edges:
        x0, y0 = G.nodes[edge[0]]['pos']
        x1, y1 = G.nodes[edge[1]]['pos']
        
        # hovertext = f'close r: {str(G.edges[edge]["r_close"])}<br>volume r:{str(G.edges[edge]["r_volume"])}'
        hovertext = (
            f'r_coefficient: {G.edges[edge]["r_close"]}'
        )

        middle_hover_trace['x'] += tuple([(x0 + x1) / 2])
        middle_hover_trace['y'] += tuple([(y0 + y1) / 2])
        middle_hover_trace['hovertext'] += tuple([hovertext])
        index = index + 1

    traceRecode.append(middle_hover_trace)
    #################################################################################################################################################################
    figure = {
        "data": traceRecode,
        "layout": go.Layout(title='Stock Network Correlation', showlegend=False, hovermode='closest',
                            margin={'b': 40, 'l': 40, 'r': 40, 't': 40},
                            xaxis={'showgrid': False, 'zeroline': False, 'showticklabels': False},
                            yaxis={'showgrid': False, 'zeroline': False, 'showticklabels': False},
                            height=600,
                            # annotations=[
                            #     dict(
                            #         ax=(G.nodes[edge[0]]['pos'][0] + G.nodes[edge[1]]['pos'][0]) / 2,
                            #         ay=(G.nodes[edge[0]]['pos'][1] + G.nodes[edge[1]]['pos'][1]) / 2, axref='x', ayref='y',
                            #         x=(G.nodes[edge[1]]['pos'][0] * 3 + G.nodes[edge[0]]['pos'][0]) / 4,
                            #         y=(G.nodes[edge[1]]['pos'][1] * 3 + G.nodes[edge[0]]['pos'][1]) / 4, xref='x', yref='y',
                            #         showarrow=False,
                            #         # arrowhead=3,
                            #         # arrowsize=4,
                            #         # arrowwidth=1,
                            #         opacity=1
                            #     ) for edge in G.edges]
                            )}
    # figure = {
    #     "data": traceRecode,
    #     "layout": go.Layout(title='Interactive Transaction Visualization', showlegend=False, hovermode='closest',
    #                         margin={'b': 40, 'l': 40, 'r': 40, 't': 40},
    #                         xaxis={'showgrid': False, 'zeroline': False, 'showticklabels': False},
    #                         yaxis={'showgrid': False, 'zeroline': False, 'showticklabels': False},
    #                         height=600,
    #                         clickmode='event+ssymbolct',
    #                         annotations=[
    #                             dict(
    #                                 ax=(G.nodes[edge[0]]['pos'][0] + G.nodes[edge[1]]['pos'][0]) / 2,
    #                                 ay=(G.nodes[edge[0]]['pos'][1] + G.nodes[edge[1]]['pos'][1]) / 2, axref='x', ayref='y',
    #                                 x=(G.nodes[edge[1]]['pos'][0] * 3 + G.nodes[edge[0]]['pos'][0]) / 4,
    #                                 y=(G.nodes[edge[1]]['pos'][1] * 3 + G.nodes[edge[0]]['pos'][1]) / 4, xref='x', yref='y',
    #                                 showarrow=True,
    #                                 arrowhead=3,
    #                                 arrowsize=4,
    #                                 arrowwidth=1,
    #                                 opacity=1
    #                             ) for edge in G.edges]
    #                         )}
    return figure