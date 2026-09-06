"""
Graph Builder Utilities
"""

import sys
from pathlib import Path

# Try to import networkx
try:
    import networkx as nx
    NETWORKX_AVAILABLE = True
except ImportError:
    NETWORKX_AVAILABLE = False

def get_node_list(G):
    try:
        if NETWORKX_AVAILABLE:
            return list(G.nodes())
        else:
            return list(G.nodes)
    except:
        return []

def get_node_attributes(G, node):
    try:
        if NETWORKX_AVAILABLE:
            return dict(G.nodes[node])
        else:
            return G.nodes[node]
    except:
        return {}

def get_neighbors(G, node):
    try:
        if NETWORKX_AVAILABLE:
            return list(G.neighbors(node))
        else:
            return G.neighbors(node)
    except:
        return []

def get_degree(G, node):
    try:
        if NETWORKX_AVAILABLE:
            return G.degree(node)
        else:
            return G.degree(node)
    except:
        return len(get_neighbors(G, node))

def get_edge_data(G, u, v):
    try:
        if NETWORKX_AVAILABLE:
            return G.get_edge_data(u, v)
        else:
            return G.get_edge_data(u, v)
    except:
        return {}
