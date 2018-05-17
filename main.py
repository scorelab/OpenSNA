import pandas as pd
from OpenSNA import Graph

edge_list = 'edges.csv'

df = pd.read_csv(edge_list, sep=',')

g = Graph()
g.load_graph(edge_list)
# g.set_graph(df)

print (len(list(g.get_graph().Nodes())))

