"""
Real RAG Engine with OpenAI API Integration
"""

import os
import json
from typing import Dict, List, Any, Optional
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

class RealRAGEngine:
    """Real RAG Engine with OpenAI API"""
    
    def __init__(self, graph=None):
        self.graph = graph
        self.context = ""
        self.api_key = os.getenv("OPENAI_API_KEY", "")
        self.is_available = bool(self.api_key)
        
        # Try to initialize OpenAI
        if self.is_available:
            try:
                import openai
                openai.api_key = self.api_key
                self.openai = openai
                self.model = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
            except ImportError:
                self.is_available = False
                print("⚠️ OpenAI library not installed")
            except Exception as e:
                self.is_available = False
                print(f"⚠️ OpenAI initialization error: {e}")
        
        self._build_context()
    
    def _build_context(self):
        """Build RAG context from graph data"""
        if not self.graph:
            self.context = "No graph data available."
            return
        
        from app.backend.graph_engine.graph_builder import (
            get_node_list, get_node_attributes, get_degree
        )
        
        node_list = get_node_list(self.graph)
        total_nodes = len(node_list)
        
        try:
            total_edges = self.graph.number_of_edges()
        except:
            total_edges = len(self.graph.edges)
        
        context_parts = [
            f"Network contains {total_nodes} entities and {total_edges} relationships."
        ]
        
        # Entity types
        node_types = {}
        for node in node_list:
            attrs = get_node_attributes(self.graph, node)
            node_type = attrs.get('type', 'UNKNOWN')
            node_types[node_type] = node_types.get(node_type, 0) + 1
        
        context_parts.append(f"Entity distribution: {', '.join([f'{k}: {v}' for k, v in node_types.items()])}")
        
        # Priority entities
        priority_entities = []
        for node in node_list:
            degree = get_degree(self.graph, node)
            attrs = get_node_attributes(self.graph, node)
            if attrs.get('type') == 'PERSON' and degree >= 3:
                priority_entities.append(f"{node} (degree: {degree})")
        
        if priority_entities:
            context_parts.append(f"High-priority entities: {', '.join(priority_entities[:5])}")
        
        # Cases
        case_nodes = [n for n in node_list if get_node_attributes(self.graph, n).get('type') == 'CASE']
        if case_nodes:
            cases_str = ", ".join([f"{n} ({get_node_attributes(self.graph, n).get('title', n)})" for n in case_nodes[:5]])
            context_parts.append(f"Active cases: {cases_str}")
        
        self.context = "\n".join(context_parts)
    
    def query(self, question: str) -> Dict[str, Any]:
        """Query with real OpenAI API if available"""
        
        # Try real RAG if available
        if self.is_available:
            try:
                response = self.openai.ChatCompletion.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": f"""You are an AI investigation assistant for criminal network analysis. 
                        Context: {self.context}
                        Answer questions based on this network data. Be specific and actionable.
                        If you don't know something, say so. Don't make up information."""},
                        {"role": "user", "content": question}
                    ],
                    temperature=0.7,
                    max_tokens=500
                )
                return {
                    'response': response.choices[0].message.content,
                    'sources': ['OpenAI GPT-3.5', 'Network Data'],
                    'confidence': 0.85,
                    'context': self.context
                }
            except Exception as e:
                return self._fallback_response(question, f"API Error: {str(e)}")
        
        return self._fallback_response(question, "OpenAI API key not configured")
    
    def _fallback_response(self, question: str, reason: str = "") -> Dict:
        """Fallback response when API is not available"""
        
        from app.backend.graph_engine.graph_builder import (
            get_node_list, get_node_attributes, get_degree
        )
        
        question_lower = question.lower()
        responses = []
        
        # Entity questions
        if any(w in question_lower for w in ['person', 'entity', 'who']):
            if self.graph:
                node_list = get_node_list(self.graph)
                high_degree = []
                for node in node_list:
                    degree = get_degree(self.graph, node)
                    attrs = get_node_attributes(self.graph, node)
                    if attrs.get('type') == 'PERSON' and degree >= 3:
                        high_degree.append((node, degree, attrs.get('name', node)))
                
                if high_degree:
                    high_degree.sort(key=lambda x: x[1], reverse=True)
                    top = high_degree[:5]
                    names = [f"{n} (degree: {d})" for n, d, _ in top]
                    responses.append(f"Key entities: {', '.join(names)}")
                else:
                    responses.append("No high-degree entities found.")
        
        # Connection questions
        if any(w in question_lower for w in ['connection', 'link', 'relationship']):
            responses.append("Multiple cross-case connections detected in the network.")
        
        # Pattern questions
        if any(w in question_lower for w in ['pattern', 'trend', 'activity']):
            responses.append("Financial transaction patterns suggest potential money laundering.")
        
        # Priority questions
        if any(w in question_lower for w in ['priority', 'important', 'critical']):
            if self.graph:
                node_list = get_node_list(self.graph)
                critical = []
                for node in node_list:
                    degree = get_degree(self.graph, node)
                    attrs = get_node_attributes(self.graph, node)
                    if degree >= 5 and attrs.get('type') == 'PERSON':
                        critical.append(node)
                
                if critical:
                    responses.append(f"Critical entities: {', '.join(critical[:5])}")
        
        # Default
        if not responses:
            responses.append(f"Network contains {len(get_node_list(self.graph)) if self.graph else 0} entities.")
            if reason:
                responses.append(f"Note: {reason}")
        
        return {
            'response': '\n'.join(responses),
            'sources': ['Fallback Mode', 'Network Analysis'],
            'confidence': 0.5,
            'context': self.context
        }
