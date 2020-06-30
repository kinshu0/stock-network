import networkx as nx
import matplotlib.pyplot as plt

G = nx.Graph()

def add_stonks(list_of_tickers, correlation_list, threshold = 0.6):
    G.add_nodes_from(list_of_tickers)
    for y in correlation_list:
        if y[2][4] >= threshold:
            post = (y[0], y[1])
            G.add_edge(*post)

def export_graph():
    nx.write_gexf(G, 'works.gexf')