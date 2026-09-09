"""
Fast Engine for handling large datasets
Location: app/frontend/streamlit/utils/fast_engine.py
"""

import networkx as nx
from collections import defaultdict
import pickle
import os

class FastCriminalNetwork:
    """Optimized for speed with large datasets"""
    
    def __init__(self):
        self.graph = nx.Graph()
        self.node_index = {}
        self.edge_index = {}
        self.cache = {}
    
    def add_node_fast(self, node_id, **attrs):
        self.graph.add_node(node_id, **attrs)
        self.node_index[node_id] = attrs
    
    def add_edge_fast(self, u, v, **attrs):
        self.graph.add_edge(u, v, **attrs)
        self.edge_index[(u, v)] = attrs
        self.edge_index[(v, u)] = attrs
    
    def find_connections_fast(self, node_id, max_depth=2):
        cache_key = f"{node_id}_{max_depth}"
        if cache_key in self.cache:
            return self.cache[cache_key]
        
        result = {}
        if node_id in self.graph:
            neighbors = list(self.graph.neighbors(node_id))
            result['direct'] = neighbors
            if max_depth >= 2:
                secondary = []
                for n in neighbors:
                    secondary.extend(list(self.graph.neighbors(n)))
                result['secondary'] = list(set(secondary) - set(neighbors) - {node_id})
        
        self.cache[cache_key] = result
        return result
    
    def get_centrality_fast(self, top_n=20):
        cache_key = f"centrality_{top_n}"
        if cache_key in self.cache:
            return self.cache[cache_key]
        
        try:
            centrality = nx.degree_centrality(self.graph)
            sorted_nodes = sorted(centrality.items(), key=lambda x: x[1], reverse=True)
            result = sorted_nodes[:top_n]
            self.cache[cache_key] = result
            return result
        except:
            return []