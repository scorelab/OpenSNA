import networkx as nx
import numpy as np
import random
from sklearn.neural_network import MLPClassifier
from sklearn import svm
from sklearn.metrics import accuracy_score, precision_recall_fscore_support, roc_curve, auc
from sklearn.model_selection import cross_val_predict

def gml_to_edgelist(f):
    g = nx.read_gml(f)
    nx.write_edgelist(g, 'power.csv', delimiter=',')

# gml_to_edgelist('power.gml')

def load_data(path):
    g = nx.read_edgelist(path, delimiter=',')
    return g

def partition(data):
    return data[:len(data)*2/3], data[len(data)*2/3:]

def generate_non_edge_list(g):
    n = len(g.edges()) # Negative edge list size is same as positive list size
    non_edges = []
    for u in g.nodes():
        for v in g.nodes():
            if u == v: continue
            if g.has_edge(u, v): continue
            non_edges.append((u, v))
    neg_sample = random.sample(non_edges, n)
    return neg_sample

def generate_class_labels(g, edges):
    y = []
    for edge in edges:
        if g.has_edge(edge[0], edge[1]):
            y.append(1)
        else:
            y.append(0)
    return y

def adamic_adar(g, X):
    preds = nx.adamic_adar_index(g, X)
    lst = []
    for u, v, p in preds:
        lst.append(p)

    max_p = max(lst)
    return [x/max_p for x in lst]

def jaccard(g, X):
    preds = nx.jaccard_coefficient(g, X)
    lst = []
    for u, v, p in preds:
        lst.append(p)

    max_p = max(lst)
    return [x/max_p for x in lst]

def common_neighbors(g, X):
    lst = []
    for x in X:
        cn = nx.common_neighbors(g, x[0], x[1])
        lst.append(len(list(cn)))
    max_p = float(max(lst))

    return [x/max_p for x in lst]

def concat_features(X, features):
    lst = [[] for x in range(len(X))]
    for feature in features:
        for i in range(len(X)):
            feature_value = feature[i]
            lst[i].append(feature_value)
    return lst

g = load_data('power.csv')

# Generate positive training and testing edge list
EDGES_POSITIVE = g.edges()
print len(list(g.edges()))
print len(list(g.))

# Generate negative edge list
EDGES_NEGATIVE = generate_non_edge_list(g)

EDGES = EDGES_POSITIVE + EDGES_NEGATIVE
random.shuffle(EDGES)

Y = generate_class_labels(g, EDGES)

feature1 = adamic_adar(g, EDGES)
feature2 = jaccard(g, EDGES)
feature3 = common_neighbors(g, EDGES)

features = [feature1, feature2, feature3]
feature_values = concat_features(EDGES, features)


print "Total nodes", len(g.nodes())
print "Total edges", len(g.edges())

### MLP ###
clf = MLPClassifier(solver='lbfgs', alpha=1e-5, hidden_layer_sizes=(10, 10), random_state=1)
# clf = svm.SVC(kernel='rbf', random_state=0, gamma=1, C=1)
clf.fit(feature_values, Y)


### Validation ###
pred = cross_val_predict(clf, feature_values, Y, cv=6)


### Results ###
print "Accuracy:", accuracy_score(Y, pred)
precision, recall, fscore, support = precision_recall_fscore_support(Y, pred, average='binary')
print "Precision:", precision
print "Recall:", recall
print "f-score:", fscore


### SVN ###
clf = svm.SVC(kernel='rbf', random_state=0, gamma=1, C=1)
clf.fit(feature_values, Y)


### Validation ###
pred = cross_val_predict(clf, feature_values, Y, cv=6)


### Results ###
print "Accuracy:", accuracy_score(Y, pred)
precision, recall, fscore, support = precision_recall_fscore_support(Y, pred, average='binary')
print "Precision:", precision
print "Recall:", recall
print "f-score:", fscore
