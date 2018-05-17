import random
import snap

class Graph:
    def __init__(self):
        self.g = snap.TNEANet();

    def set_graph(self, g):
        self.g = g

    def get_graph(self):
        return self.g

    def load_graph(self, edge_list):
        self.g = snap.LoadEdgeList(snap.PNGraph, edge_list, 0, 1, ',')
