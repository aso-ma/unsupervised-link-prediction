import networkx as nx
import random

def auc(graph, train_graph, test_graph, score_function, n=100): 
    nonexistent_edge_list = list(nx.non_edges(graph))
    test_graph_edges = list(test_graph.edges())
    n_prime, n_double_prime = 0, 0 
    for i in range(n):
        test_edge = random.choice(test_graph_edges)
        nonexistent_edge = random.choice(nonexistent_edge_list)
        score1 = score_function(train_graph, test_edge[0], test_edge[1])
        score2 = score_function(train_graph, nonexistent_edge[0], nonexistent_edge[1])
        if score1 > score2:
            n_prime+=1
        if score1 == score2:    
            n_double_prime+=1
    return (n_prime + (0.5*n_double_prime))/n

def precision(test_graph, scored_links):
    n = test_graph.number_of_nodes()
    scored_links.sort(key=lambda e:e[2], reverse=True)
    count = sum(
        1
        for node1, node2, _ in scored_links[:n]
        if test_graph.has_edge(node1, node2)
    )
    return (count*100)/n