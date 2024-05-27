from networkx import non_edges
from networkx import complement

def edge_scoring(graph, scoring_function):
    scored_links = [] 
    for v, u in non_edges(graph):
        scored_links.append(
            (v, u, scoring_function(graph, v, u))
        )  
    return scored_links

def reverse_link_prediction(graph, scoring_function):
    scored_links = [] 
    for v, u in graph.edges():
        scored_links.append(
            (v, u, scoring_function(graph, v, u))
        )  
    return scored_links

def negative_link_prediction(graph, scoring_function):
    complement_graph = complement(graph)
    return edge_scoring(complement_graph, scoring_function)