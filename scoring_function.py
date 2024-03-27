from math import log1p

def __get_common_neighbors(graph, v, u):
    neighbors_of_v = set(graph.neighbors(v))
    return neighbors_of_v.intersection(graph.neighbors(u))

def __get_union_neighbors(graph, v, u):
    neighbors_of_v = set(graph.neighbors(v))
    return neighbors_of_v.union(graph.neighbors(u))

def preferential_attachment(graph, v, u):
    return graph.degree(v) * graph.degree(u)

def common_neighbor(graph, v, u):
    return len(__get_common_neighbors(graph, v, u))

def jaccard(graph, v, u):
    neighbors_intersection = __get_common_neighbors(graph, v, u)
    neighbors_union = __get_union_neighbors(graph, v, u)
    return len(neighbors_intersection) / len(neighbors_union)

def adamic_adar(graph, v, u):
    return sum(
        1/log1p(graph.degree(c_neighbor)) for c_neighbor in __get_common_neighbors(graph, v, u)
    )