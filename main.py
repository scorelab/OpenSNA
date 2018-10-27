import pandas as pd
from OpenSNA import Graph

edge_list = 'data/power.csv'

g = Graph()
g.load_graph(edge_list, False)

# print (len(list(g.get_graph().Nodes())))

params_mlp = {
    "solver": 'lbfgs',
    "alpha": 1e-5,
    "hidden_layer_sizes": (10, 10),
    "random_state": 1
    }
params_svn = {
    "kernel": 'rbf',
    "random_state": 0,
    "gamma": 1,
    "C": 1
    }

g.link_predict(params_mlp, "MLP")
