import pandas as pd
from OpenSNA import Graph

edge_list = 'edges.csv'

g = Graph()
g.load_graph(edge_list, False)

print (len(list(g.get_graph().Nodes())))

