import networkx as nx
import random

def __train_test_split(graph, train_edge_proportion=0.7):
    train_graph = nx.Graph()
    test_graph = nx.Graph()
    train_graph.add_nodes_from(graph.nodes())
    test_graph.add_nodes_from(graph.nodes())

    edge_list = list(graph.edges())
    train_edges_count = int(len(edge_list) * train_edge_proportion)
    train_edges = set(random.sample(edge_list, train_edges_count))
    test_edges = set(edge_list) - train_edges
    train_graph.add_edges_from(train_edges)
    test_graph.add_edges_from(test_edges)
    
    return train_graph, test_graph

def __preferential_attachment(graph, edge):
    node1, node2 = edge
    return graph.degree(node1) * graph.degree(node2)

def auc(graph, score_function, n=100): 
    # Splitting the input graph into train and test graphs
    train_graph, test_graph = __train_test_split(graph)

    # AUC Calculation
    nonexistent_edge_list = list(nx.non_edges(graph))
    test_graph_edges = list(test_graph.edges())
    n_prime, n_double_prime = 0, 0 
    for i in range(n):
        test_edge = random.choice(test_graph_edges)
        nonexistent_edge = random.choice(nonexistent_edge_list)
        score1 = score_function(train_graph, test_edge)
        score2 = score_function(train_graph, nonexistent_edge)
        if score1 > score2:
            n_prime+=1
        if score1 == score2:    
            n_double_prime+=1
    return (n_prime + (0.5*n_double_prime))/n

def link_prediction(graph, scoring_function):
    scored_links = [] 
    for v, u in nx.non_edges(graph):
        scored_links.append(
            (
                v, u, scoring_function(graph, (v, u))
            )
        )  
    return scored_links

def precision(test_graph, scored_links):
    n = test_graph.number_of_nodes()
    scored_links.sort(key=lambda e:e[2], reverse=True)
    count = sum(
        1
        for node1, node2, _ in scored_links[:n]
        if test_graph.has_edge(node1, node2)
    )
    return (count*100)/n

if __name__ == '__main__':
    g_karate = nx.karate_club_graph()
    g_train, g_test = __train_test_split(g_karate)
    scored_links = link_prediction(g_train, __preferential_attachment)
    print('Precis ->', precision(g_test, scored_links))
    print('AUC ->', auc(g_karate, __preferential_attachment))