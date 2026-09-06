"""
Graph Builder Utilities
"""

def get_node_list(G):
    try:
        return list(G.nodes())
    except:
        return []

def get_node_attributes(G, node):
    try:
        return dict(G.nodes[node])
    except:
        return {}

def get_neighbors(G, node):
    try:
        return list(G.neighbors(node))
    except:
        return []

def get_degree(G, node):
    try:
        return G.degree(node)
    except:
        return len(get_neighbors(G, node))

def get_edge_data(G, u, v):
    try:
        return G.get_edge_data(u, v)
    except:
        return {}
