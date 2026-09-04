import numpy as np
from typing import Dict, List, Tuple, Optional
import networkx as nx
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

class PriorityScorer:
    """Intelligent priority scoring for investigation leads"""
    
    def __init__(self, graph: nx.Graph, centrality_scores: Dict = None):
        self.graph = graph
        self.centrality_scores = centrality_scores or {}
        self.weights = {
            'network_importance': 0.25,
            'cross_case_relevance': 0.20,
            'temporal_correlation': 0.20,
            'suspicious_activity': 0.20,
            'evidence_strength': 0.15
        }
    
    def score_entity(self, entity_id: str, cross_case_counts: Dict = None,
                     temporal_data: Dict = None, evidence_scores: Dict = None) -> Dict:
        """Calculate comprehensive score for an entity"""
        
        score_components = {}
        final_score = 0
        
        # 1. Network Importance
        network_score = self._calculate_network_importance(entity_id)
        score_components['network_importance'] = network_score
        final_score += network_score * self.weights['network_importance']
        
        # 2. Cross-case Relevance
        cross_case_score = self._calculate_cross_case_relevance(entity_id, cross_case_counts)
        score_components['cross_case_relevance'] = cross_case_score
        final_score += cross_case_score * self.weights['cross_case_relevance']
        
        # 3. Temporal Correlation
        temporal_score = self._calculate_temporal_correlation(entity_id, temporal_data)
        score_components['temporal_correlation'] = temporal_score
        final_score += temporal_score * self.weights['temporal_correlation']
        
        # 4. Suspicious Activity
        suspicious_score = self._calculate_suspicious_activity(entity_id)
        score_components['suspicious_activity'] = suspicious_score
        final_score += suspicious_score * self.weights['suspicious_activity']
        
        # 5. Evidence Strength
        evidence_score = self._calculate_evidence_strength(entity_id, evidence_scores)
        score_components['evidence_strength'] = evidence_score
        final_score += evidence_score * self.weights['evidence_strength']
        
        # Normalize to 0-100 scale
        final_score = min(100, final_score * 100)
        
        # Determine priority level
        if final_score >= 70:
            priority = 'HIGH'
        elif final_score >= 40:
            priority = 'MEDIUM'
        else:
            priority = 'LOW'
        
        return {
            'entity_id': entity_id,
            'score': round(final_score, 2),
            'priority': priority,
            'components': score_components
        }
    
    def _calculate_network_importance(self, entity_id: str) -> float:
        """Calculate entity's importance in the network"""
        score = 0.5  # Default middle score
        
        if entity_id in self.graph.nodes:
            # Degree centrality
            if 'degree' in self.centrality_scores:
                degree = self.centrality_scores['degree'].get(entity_id, 0)
                score += degree * 0.3
            
            # Betweenness centrality (bridge importance)
            if 'betweenness' in self.centrality_scores:
                betweenness = self.centrality_scores['betweenness'].get(entity_id, 0)
                score += betweenness * 0.3
            
            # Check if entity is a bridge
            if self._is_bridge_entity(entity_id):
                score += 0.2
            
            # Community bridging
            if self._is_community_bridge(entity_id):
                score += 0.2
        
        return min(1.0, score)
    
    def _is_bridge_entity(self, entity_id: str) -> bool:
        """Check if entity is a bridge (critical connection)"""
        try:
            bridges = list(nx.bridges(self.graph))
            for u, v in bridges:
                if u == entity_id or v == entity_id:
                    return True
        except:
            pass
        return False
    
    def _is_community_bridge(self, entity_id: str) -> bool:
        """Check if entity connects different communities"""
        try:
            from networkx.algorithms.community import louvain_communities
            communities = list(louvain_communities(self.graph))
            if len(communities) > 1:
                community_id = None
                for idx, community in enumerate(communities):
                    if entity_id in community:
                        community_id = idx
                        break
                
                if community_id is not None:
                    # Count connections to other communities
                    other_connections = 0
                    for neighbor in self.graph.neighbors(entity_id):
                        for idx, community in enumerate(communities):
                            if idx != community_id and neighbor in community:
                                other_connections += 1
                    return other_connections >= 2
        except:
            pass
        return False
    
    def _calculate_cross_case_relevance(self, entity_id: str, 
                                        cross_case_counts: Dict = None) -> float:
        """Calculate cross-case relevance score"""
        if not cross_case_counts:
            return 0.3
        
        count = cross_case_counts.get(entity_id, 0)
        if count >= 3:
            return 1.0
        elif count >= 2:
            return 0.7
        elif count >= 1:
            return 0.4
        return 0.2
    
    def _calculate_temporal_correlation(self, entity_id: str,
                                        temporal_data: Dict = None) -> float:
        """Calculate temporal correlation score"""
        if not temporal_data:
            return 0.3
        
        activity = temporal_data.get(entity_id, {})
        recent_activity = activity.get('recent_activity', 0)
        activity_spike = activity.get('activity_spike', False)
        
        score = 0.3
        if recent_activity > 5:
            score += 0.3
        if activity_spike:
            score += 0.4
        
        return min(1.0, score)
    
    def _calculate_suspicious_activity(self, entity_id: str) -> float:
        """Calculate suspicious activity score"""
        suspicious_factors = []
        
        # Check for unusual degree
        if entity_id in self.graph.nodes:
            degree = self.graph.degree(entity_id)
            avg_degree = sum(dict(self.graph.degree()).values()) / max(1, len(self.graph.nodes))
            if degree > 3 * avg_degree:
                suspicious_factors.append(0.3)
            elif degree > 2 * avg_degree:
                suspicious_factors.append(0.2)
        
        # Check for recent activity (would need actual temporal data)
        # For now, just add a small random factor to demo
        suspicious_factors.append(np.random.uniform(0, 0.2))
        
        return min(1.0, sum(suspicious_factors))
    
    def _calculate_evidence_strength(self, entity_id: str,
                                     evidence_scores: Dict = None) -> float:
        """Calculate evidence strength score"""
        if not evidence_scores:
            return 0.4
        
        score = evidence_scores.get(entity_id, 0.4)
        return min(1.0, score)
    
    def prioritize_entities(self, entity_ids: List[str] = None) -> List[Dict]:
        """Get priority ranking for all entities or specific ones"""
        if entity_ids is None:
            entity_ids = list(self.graph.nodes())
        
        scores = []
        for entity_id in entity_ids:
            score = self.score_entity(entity_id)
            scores.append(score)
        
        # Sort by score descending
        scores.sort(key=lambda x: x['score'], reverse=True)
        return scores
    
    def get_high_priority_leads(self, threshold: float = 0.7) -> List[Dict]:
        """Get high priority investigation leads"""
        all_scores = self.prioritize_entities()
        high_priority = [s for s in all_scores if s['score'] / 100 >= threshold]
        return high_priority
    
    def generate_investigation_brief(self, entity_id: str) -> Dict:
        """Generate comprehensive investigation brief for an entity"""
        score = self.score_entity(entity_id)
        
        brief = {
            'entity_id': entity_id,
            'priority': score['priority'],
            'score': score['score'],
            'summary': self._generate_summary(entity_id, score),
            'connections': self._get_important_connections(entity_id),
            'evidence': self._get_evidence_summary(entity_id),
            'recommendations': self._generate_recommendations(entity_id, score)
        }
        
        return brief
    
    def _generate_summary(self, entity_id: str, score: Dict) -> str:
        """Generate natural language summary"""
        summary_parts = []
        
        # Network position
        if score['components']['network_importance'] > 0.7:
            summary_parts.append("central to the network with critical connections")
        elif score['components']['network_importance'] > 0.4:
            summary_parts.append("well-connected within the network")
        else:
            summary_parts.append("peripheral but with relevant connections")
        
        # Cross-case
        if score['components']['cross_case_relevance'] > 0.7:
            summary_parts.append("appears in multiple cases suggesting broader involvement")
        
        # Suspicious activity
        if score['components']['suspicious_activity'] > 0.7:
            summary_parts.append("exhibits suspicious patterns warranting immediate attention")
        elif score['components']['suspicious_activity'] > 0.4:
            summary_parts.append("shows unusual activity patterns")
        
        return "This entity is " + " and ".join(summary_parts)
    
    def _get_important_connections(self, entity_id: str) -> List[Dict]:
        """Get important connections for an entity"""
        connections = []
        
        if entity_id in self.graph.nodes:
            neighbors = list(self.graph.neighbors(entity_id))
            
            # Get top 5 most connected neighbors
            neighbor_degrees = [(n, self.graph.degree(n)) for n in neighbors]
            neighbor_degrees.sort(key=lambda x: x[1], reverse=True)
            
            for neighbor, degree in neighbor_degrees[:5]:
                edge_data = self.graph.get_edge_data(entity_id, neighbor)
                connections.append({
                    'entity_id': neighbor,
                    'relationship': edge_data.get('type', 'CONNECTED'),
                    'strength': degree / max(1, len(self.graph.nodes)),
                    'properties': edge_data
                })
        
        return connections
    
    def _get_evidence_summary(self, entity_id: str) -> List[Dict]:
        """Get evidence summary for entity"""
        # This would come from actual evidence database
        # For demo, generate sample evidence
        evidence = [
            {
                'type': 'Communication',
                'description': f'Multiple calls detected from entity {entity_id}',
                'count': np.random.randint(1, 20),
                'source': 'CDR Analysis'
            },
            {
                'type': 'Financial',
                'description': f'Financial transactions associated with entity {entity_id}',
                'count': np.random.randint(1, 10),
                'source': 'Bank Records'
            },
            {
                'type': 'Location',
                'description': f'Location data linked to entity {entity_id}',
                'count': np.random.randint(1, 5),
                'source': 'Geolocation'
            }
        ]
        
        # Filter out zero-count evidence
        return [e for e in evidence if e['count'] > 0]
    
    def _generate_recommendations(self, entity_id: str, score: Dict) -> List[str]:
        """Generate investigation recommendations"""
        recommendations = []
        
        if score['priority'] == 'HIGH':
            recommendations.append("Immediate investigation priority - assign to senior investigator")
            recommendations.append("Conduct thorough background check and surveillance")
            if score['components']['cross_case_relevance'] > 0.7:
                recommendations.append("Coordinate with investigators handling connected cases")
        elif score['priority'] == 'MEDIUM':
            recommendations.append("Schedule for investigation within 48 hours")
            recommendations.append("Gather additional evidence before proceeding")
        
        recommendations.append("Document all findings in case management system")
        
        return recommendations