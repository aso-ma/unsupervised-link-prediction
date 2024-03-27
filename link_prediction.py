from networkx import non_edges

def edge_scoring(graph, scoring_function):
    scored_links = [] 
    for v, u in non_edges(graph):
        scored_links.append(
            (
                v, u, scoring_function(graph, v, u)
            )
        )  
    return scored_links