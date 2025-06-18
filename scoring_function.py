from math import log1p, sqrt
from networkx import is_weighted

def __get_common_neighbors(graph, v, u):
    neighbors_of_v = set(graph.neighbors(v))
    return neighbors_of_v.intersection(graph.neighbors(u))

def __get_union_neighbors(graph, v, u):
    neighbors_of_v = set(graph.neighbors(v))
    return neighbors_of_v.union(graph.neighbors(u))

def __node_strength(graph, z):
    if not is_weighted(graph):
        return 0.0
    return graph.degree(z, weight='weight') 

def __get_edge_weight(graph, v, u):
    return graph[v][u]['weight']  

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

def resource_allocation(graph, v, u):
    common_neighbors = __get_common_neighbors(graph, v, u)
    s = 0 
    for n in common_neighbors:
        s+= 1/graph.degree(n)
    return s

def salton(graph, v, u):
    common_neighbors = __get_common_neighbors(graph, v, u)
    try:
        s = len(common_neighbors) / sqrt(graph.degree(v) * graph.degree(u))
    except ZeroDivisionError:
        s = 0
    return s

def sorensen(graph, v, u):
    common_neighbors = __get_common_neighbors(graph, v, u)
    try:
        s = 2 * len(common_neighbors) / (graph.degree(v) + graph.degree(u))
    except ZeroDivisionError:
        s = 0
    return s

def hub_promoted_index(graph, v, u):
    common_neighbors = __get_common_neighbors(graph, v, u)
    try:
        s = len(common_neighbors) / min(graph.degree(v), graph.degree(u))
    except ZeroDivisionError:
        s = 0
    return s

def hub_depressed_index(graph, v, u):
    common_neighbors = __get_common_neighbors(graph, v, u)
    try:
        s = len(common_neighbors) / max(graph.degree(v), graph.degree(u))
    except ZeroDivisionError:
        s = 0
    return s

def weighted_preferential_attachment(graph, v, u):
    common_neighbors = __get_common_neighbors(graph, v, u)
    s = 0
    for z in common_neighbors:
        s += (__get_edge_weight(graph, v, z) * __get_edge_weight(graph, z, u))
    return s 
  
def weighted_common_neighbor(graph, v, u):
    common_neighbors = __get_common_neighbors(graph, v, u)
    s = 0
    for z in common_neighbors:
        s += (__get_edge_weight(graph, v, z) + __get_edge_weight(graph, z, u))
    return s 

def weighted_adamic_adar(graph, v, u):
  common_neighbors = __get_common_neighbors(graph, v, u)
  s = 0
  for z in common_neighbors:
    s += (
      (__get_edge_weight(graph, v, z) + __get_edge_weight(graph, z, u)) 
      / log1p(__node_strength(graph, z))
    )
  return s

def weighted_jaccard(graph, v, u):
    s1 = weighted_common_neighbor(graph, v, u)
    s2 = __node_strength(graph, v) + __node_strength(graph, u)
    return s1 / s2

def weighted_resource_allocation(graph, v, u):
    common_neighbors = __get_common_neighbors(graph, v, u)
    s = 0
    for z in common_neighbors:
        s += (
            (__get_edge_weight(graph, v, z) + __get_edge_weight(graph, z, u))
            / __node_strength(graph, z)
        )
    return s