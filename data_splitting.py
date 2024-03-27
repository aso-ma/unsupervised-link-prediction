from networkx import Graph
from random import sample, shuffle

def train_test_split(graph, train_edge_proportion=0.7):
    train_graph = Graph()
    test_graph = Graph()
    train_graph.add_nodes_from(graph.nodes())
    test_graph.add_nodes_from(graph.nodes())

    edge_list = list(graph.edges())
    train_edges_count = int(len(edge_list) * train_edge_proportion)
    train_edges = set(sample(edge_list, train_edges_count))
    test_edges = set(edge_list) - train_edges
    train_graph.add_edges_from(train_edges)
    test_graph.add_edges_from(test_edges)
    
    return train_graph, test_graph


def k_fold_cross_validation(graph, k=3, shuffle_edges=True):
    edges = list(graph.edges())
    if shuffle_edges:
        shuffle(edges)
    fold_size = len(edges)//k
    fold_data = dict()
    for i in range(1, k+1, 1):
        if i == k:
            fold_data[i] = edges
        else:
            fold_edges = sample(edges, fold_size)
            edges = [e for e in edges if e not in fold_edges]
            fold_data[i] = fold_edges
    return fold_data


def get_train_test_graphs_for(graph, fold_edges):
    train_graph = Graph()
    test_graph = Graph()
    train_graph.add_nodes_from(graph.nodes())
    test_graph.add_nodes_from(graph.nodes())
    test_edges = set(fold_edges)
    train_edges = set(graph.edges()) - test_edges
    test_graph.add_edges_from(test_edges)
    train_graph.add_edges_from(train_edges)

    return train_graph, test_graph