import networkx as nx
import pandas as pd
from typing import Dict, List, Tuple, Optional, Any
from collections import defaultdict
import logging
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class CriminalGraphBuilder:
    """Build and manage criminal network graphs"""
    
    def __init__(self):
        self.graph = nx.Graph()
        self.entity_properties = {}
        self.edge_properties = {}
        self.timeline = defaultdict(list)
        
        # Entity types and their display properties
        self.entity_styles = {
            'PERSON': {'color': '#FF6B6B', 'shape': 'circle', 'size': 30},
            'PHONE': {'color': '#4ECDC4', 'shape': 'diamond', 'size': 20},
            'ACCOUNT': {'color': '#45B7D1', 'shape': 'square', 'size': 25},
            'VEHICLE': {'color': '#96CEB4', 'shape': 'triangle', 'size': 22},
            'LOCATION': {'color': '#FFEAA7', 'shape': 'star', 'size': 28},
            'ORGANIZATION': {'color': '#DDA0DD', 'shape': 'hexagon', 'size': 30},
            'CASE': {'color': '#FF9FF3', 'shape': 'rectangle', 'size': 35},
        }
    
    def add_entity(self, entity_id: str, entity_type: str, properties: Dict = None):
        """Add entity to graph"""
        if properties is None:
            properties = {}
        
        self.graph.add_node(entity_id, type=entity_type, **properties)
        self.entity_properties[entity_id] = {
            'type': entity_type,
            'properties': properties,
            'style': self.entity_styles.get(entity_type, {})
        }
    
    def add_relationship(self, source: str, target: str, rel_type: str, 
                         properties: Dict = None, timestamp: datetime = None):
        """Add relationship between entities"""
        if properties is None:
            properties = {}
        
        if timestamp:
            properties['timestamp'] = timestamp
            self.timeline[timestamp].append((source, target, rel_type))
        
        self.graph.add_edge(source, target, type=rel_type, **properties)
        
        edge_key = f"{source}_{target}"
        self.edge_properties[edge_key] = {
            'type': rel_type,
            'properties': properties
        }
    
    def build_from_dataframes(self, dataframes: Dict[str, pd.DataFrame]) -> nx.Graph:
        """Build graph from multiple dataframes"""
        
        # 1. Add persons
        if 'persons' in dataframes:
            for _, row in dataframes['persons'].iterrows():
                person_id = str(row.get('person_id', ''))
                if person_id:
                    properties = row.to_dict()
                    self.add_entity(person_id, 'PERSON', properties)
        
        # 2. Add phones
        if 'phones' in dataframes:
            for _, row in dataframes['phones'].iterrows():
                phone_id = str(row.get('phone_id', ''))
                if phone_id:
                    properties = row.to_dict()
                    self.add_entity(phone_id, 'PHONE', properties)
                    
                    # Connect phone to owner
                    owner_id = str(row.get('owner_id', ''))
                    if owner_id and owner_id in self.graph.nodes:
                        self.add_relationship(owner_id, phone_id, 'OWNS', {'confidence': 0.8})
        
        # 3. Add CDR (call data)
        if 'cdr' in dataframes:
            for _, row in dataframes['cdr'].iterrows():
                caller = str(row.get('caller_number', ''))
                receiver = str(row.get('receiver_number', ''))
                
                if caller and receiver:
                    call_time = row.get('call_time')
                    duration = row.get('duration', 0)
                    
                    # Add phone nodes if they don't exist
                    if caller not in self.graph.nodes:
                        self.add_entity(caller, 'PHONE', {'number': caller})
                    if receiver not in self.graph.nodes:
                        self.add_entity(receiver, 'PHONE', {'number': receiver})
                    
                    # Add relationship
                    self.add_relationship(
                        caller, receiver, 'CALLED',
                        {
                            'duration': duration,
                            'call_time': call_time
                        },
                        timestamp=call_time
                    )
        
        # 4. Add transactions
        if 'transactions' in dataframes:
            for _, row in dataframes['transactions'].iterrows():
                from_account = str(row.get('from_account', ''))
                to_account = str(row.get('to_account', ''))
                amount = row.get('amount', 0)
                transaction_date = row.get('transaction_date')
                
                if from_account and to_account:
                    if from_account not in self.graph.nodes:
                        self.add_entity(from_account, 'ACCOUNT', {'account': from_account})
                    if to_account not in self.graph.nodes:
                        self.add_entity(to_account, 'ACCOUNT', {'account': to_account})
                    
                    self.add_relationship(
                        from_account, to_account, 'TRANSACTION',
                        {
                            'amount': amount,
                            'transaction_date': transaction_date
                        },
                        timestamp=transaction_date
                    )
        
        # 5. Add vehicles
        if 'vehicles' in dataframes:
            for _, row in dataframes['vehicles'].iterrows():
                vehicle_id = str(row.get('vehicle_id', ''))
                owner_id = str(row.get('owner_id', ''))
                
                if vehicle_id:
                    properties = row.to_dict()
                    self.add_entity(vehicle_id, 'VEHICLE', properties)
                    
                    if owner_id and owner_id in self.graph.nodes:
                        self.add_relationship(owner_id, vehicle_id, 'OWNS', {'confidence': 0.8})
        
        # 6. Add locations
        if 'locations' in dataframes:
            for _, row in dataframes['locations'].iterrows():
                location_id = str(row.get('location_id', ''))
                if location_id:
                    properties = row.to_dict()
                    self.add_entity(location_id, 'LOCATION', properties)
        
        # 7. Add cases
        if 'cases' in dataframes:
            for _, row in dataframes['cases'].iterrows():
                case_id = str(row.get('case_id', ''))
                if case_id:
                    properties = row.to_dict()
                    self.add_entity(case_id, 'CASE', properties)
        
        logger.info(f"Built graph with {len(self.graph.nodes)} nodes and {len(self.graph.edges)} edges")
        return self.graph

class GraphAnalyzer:
    """Graph analysis and metrics"""
    
    def __init__(self, graph: nx.Graph):
        self.graph = graph
    
    def calculate_centrality(self) -> Dict:
        """Calculate various centrality measures"""
        results = {}
        
        # Degree centrality
        degree_cent = nx.degree_centrality(self.graph)
        results['degree'] = degree_cent
        
        # Betweenness centrality (calculate only for connected graph)
        if nx.is_connected(self.graph):
            betweenness_cent = nx.betweenness_centrality(self.graph)
            results['betweenness'] = betweenness_cent
        else:
            # For disconnected graph, calculate on largest component
            components = list(nx.connected_components(self.graph))
            if components:
                largest = self.graph.subgraph(max(components, key=len))
                if len(largest.nodes()) > 1:
                    betweenness_cent = nx.betweenness_centrality(largest)
                    results['betweenness'] = betweenness_cent
        
        # Closeness centrality
        if nx.is_connected(self.graph):
            closeness_cent = nx.closeness_centrality(self.graph)
            results['closeness'] = closeness_cent
        
        # Eigenvector centrality
        try:
            eigenvector_cent = nx.eigenvector_centrality(self.graph, max_iter=1000)
            results['eigenvector'] = eigenvector_cent
        except:
            pass
        
        return results
    
    def find_communities(self, algorithm: str = 'louvain') -> List[List[str]]:
        """Find communities in the graph"""
        communities = []
        
        try:
            if algorithm == 'louvain':
                from networkx.algorithms.community import louvain_communities
                communities = louvain_communities(self.graph)
            elif algorithm == 'girvan_newman':
                from networkx.algorithms.community import girvan_newman
                communities = list(girvan_newman(self.graph))
            else:
                logger.warning(f"Unknown community algorithm: {algorithm}")
        except ImportError:
            logger.warning("Community detection libraries not available")
        except Exception as e:
            logger.error(f"Error finding communities: {str(e)}")
        
        return communities
    
    def find_shortest_path(self, source: str, target: str) -> List[str]:
        """Find shortest path between two entities"""
        try:
            if source in self.graph.nodes and target in self.graph.nodes:
                path = nx.shortest_path(self.graph, source, target)
                return path
        except nx.NetworkXNoPath:
            pass
        except Exception as e:
            logger.error(f"Error finding shortest path: {str(e)}")
        return []
    
    def find_bridges(self) -> List[Tuple[str, str]]:
        """Find bridge edges (critical connections)"""
        try:
            bridges = list(nx.bridges(self.graph))
            return bridges
        except:
            return []
    
    def get_entity_type_distribution(self) -> Dict[str, int]:
        """Get distribution of entity types"""
        distribution = defaultdict(int)
        for node, data in self.graph.nodes(data=True):
            entity_type = data.get('type', 'UNKNOWN')
            distribution[entity_type] += 1
        return dict(distribution)
    
    def get_central_entities(self, metric: str = 'degree', top_n: int = 10) -> List[Tuple[str, float]]:
        """Get top N entities by centrality metric"""
        centrality = self.calculate_centrality()
        if metric in centrality:
            sorted_entities = sorted(centrality[metric].items(), key=lambda x: x[1], reverse=True)
            return sorted_entities[:top_n]
        return []

class TemporalGraphAnalyzer:
    """Time-based graph analysis"""
    
    def __init__(self, graph: nx.Graph, timeline: Dict):
        self.graph = graph
        self.timeline = timeline
    
    def analyze_temporal_patterns(self, time_window: timedelta = timedelta(days=30)) -> Dict:
        """Analyze patterns over time"""
        patterns = {
            'activity_spikes': [],
            'emerging_connections': [],
            'community_changes': []
        }
        
        sorted_timeline = sorted(self.timeline.keys())
        if not sorted_timeline:
            return patterns
        
        # Detect activity spikes
        window_counts = defaultdict(int)
        for timestamp in sorted_timeline:
            window_key = timestamp.date()
            window_counts[window_key] += len(self.timeline[timestamp])
        
        # Find spikes (events > 2x average)
        avg_activity = sum(window_counts.values()) / len(window_counts) if window_counts else 0
        if avg_activity > 0:
            for date, count in window_counts.items():
                if count > 2 * avg_activity:
                    patterns['activity_spikes'].append({
                        'date': date,
                        'activity_count': count,
                        'spike_ratio': count / avg_activity
                    })
        
        return patterns
    
    def get_network_evolution(self, start_date: datetime, end_date: datetime) -> Dict:
        """Get network evolution over time period"""
        evolution = {
            'nodes_over_time': [],
            'edges_over_time': [],
            'timeline_graphs': []
        }
        
        # Build subgraphs for each time period
        current_date = start_date
        while current_date <= end_date:
            period_graph = nx.Graph()
            
            for timestamp, events in self.timeline.items():
                if start_date <= timestamp <= current_date:
                    for source, target, rel_type in events:
                        if source in self.graph.nodes and target in self.graph.nodes:
                            period_graph.add_edge(source, target, type=rel_type)
            
            evolution['nodes_over_time'].append({
                'date': current_date,
                'nodes': len(period_graph.nodes()),
                'edges': len(period_graph.edges())
            })
            
            evolution['timeline_graphs'].append({
                'date': current_date,
                'graph': period_graph
            })
            
            current_date += timedelta(days=7)  # Weekly snapshots
        
        return evolution