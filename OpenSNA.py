import random
import networkx as nx
from utils.link_prediction import link_prediction


class Graph:
    def __init__(self):
        self.g = nx.Graph()

    def set_graph(self, g):
        self.g = g

    def get_graph(self):
        return self.g

    def load_graph(self, edge_list, directed=False):
        self.g = nx.read_edgelist(edge_list, delimiter=',')

    def link_predict(self, params, classifier='MLP'):
        return link_prediction.predict(self.g, params, classifier)
        
