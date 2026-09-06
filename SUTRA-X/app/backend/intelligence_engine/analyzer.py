
"""
Network Analysis
"""

from app.backend.graph_engine.graph_builder import get_node_list, get_node_attributes, get_degree

def analyze_network(G):
    if G is None:
        return None
    
    node_list = get_node_list(G)
    total_nodes = len(node_list)
    total_edges = 0
    try:
        total_edges = G.number_of_edges()
    except:
        total_edges = 0
    
    node_types = {}
    for node in node_list:
        attrs = get_node_attributes(G, node)
        node_type = attrs.get('type', 'UNKNOWN')
        node_types[node_type] = node_types.get(node_type, 0) + 1
    
    priority_entities = []
    for node in node_list:
        degree = get_degree(G, node)
        attrs = get_node_attributes(G, node)
        node_type = attrs.get('type', 'UNKNOWN')
        if node_type != 'CASE' and degree >= 2:
            priority_entities.append({
                'id': node,
                'degree': degree,
                'type': node_type,
                'name': attrs.get('name', attrs.get('number', node))
            })
    
    priority_entities.sort(key=lambda x: x['degree'], reverse=True)
    
    return {
        'total_nodes': total_nodes,
        'total_edges': total_edges,
        'node_types': node_types,
        'priority_entities': priority_entities[:10]
    }

def generate_alerts(G):
    alerts = []
    if G is None:
        return alerts
    
    node_list = get_node_list(G)
    
    for node in node_list:
        attrs = get_node_attributes(G, node)
        degree = get_degree(G, node)
        if degree >= 5 and attrs.get('type') == 'PERSON':
            alerts.append({
                'id': f"ALERT-{len(alerts)+1:04d}",
                'type': 'CRITICAL',
                'title': f'Critical Entity: {node}',
                'description': f'Entity {node} has {degree} connections',
                'entity': node,
                'timestamp': datetime.now().isoformat(),
                'action': 'Immediate investigation required',
                'emergency': True
            })
    
    return alerts[:10]
