import random
import snap

class Graph:
    def __init__(self):
        self.g = snap.TNEANet();

    def set_graph(self, g):
        self.g = g

    def get_graph(self):
        return self.g

    def load_graph(self, edge_list, directed=False):
        if directed:
            self.g = snap.LoadEdgeList(snap.PNGraph, edge_list, 0, 1, ',')
        else:
            self.g = snap.LoadEdgeList(snap.PUNGraph, edge_list, 0, 1, ',')

