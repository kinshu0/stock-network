import networkx as nx
import matplotlib.pyplot as plt

G = nx.Graph()

def add_stonks(list_of_tickers, correlation_list, threshold = 0.6):
    for x in list_of_tickers:
        G.add_node(x)
    for y in correlation_list:
        if y[3][4] >= threshold:
            post = (y[0], y[1])

def export_graph():
    nx.write_gexf(G, 'works')