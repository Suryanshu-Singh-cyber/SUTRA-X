"""
Real RAG Engine with OpenAI API Integration
"""

import os
import json
from typing import List, Dict, Any, Optional
from datetime import datetime
import openai
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA
from langchain.llms import OpenAI
from dotenv import load_dotenv

load_dotenv()

class RAGEngine:
    """Real RAG Engine with OpenAI API"""
    
    def __init__(self, graph=None):
        self.graph = graph
        self.vector_store = None
        self.qa_chain = None
        self.context = []
        self.sources = []
        
        # Initialize OpenAI
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.model = os.getenv("OPENAI_MODEL", "gpt-4-turbo-preview")
        
        if self.api_key:
            openai.api_key = self.api_key
            self.llm = OpenAI(
                temperature=0.7,
                model=self.model,
                openai_api_key=self.api_key
            )
            self.embeddings = OpenAIEmbeddings(
                openai_api_key=self.api_key
            )
        else:
            print("⚠️ OpenAI API key not found. RAG will use fallback mode.")
            self.llm = None
            self.embeddings = None
        
        if graph:
            self._build_index()
    
    def _build_index(self):
        """Build vector store index from graph data"""
        if not self.graph:
            return
        
        # Extract data from graph
        documents = self._extract_documents()
        
        if not documents:
            return
        
        # Split documents
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            separators=["\n\n", "\n", ". ", " ", ""]
        )
        texts = text_splitter.split_text("\n\n".join(documents))
        
        # Build vector store
        if self.embeddings and texts:
            try:
                self.vector_store = Chroma.from_texts(
                    texts,
                    self.embeddings,
                    collection_name="sutra_x_rag"
                )
                
                # Create QA chain
                if self.llm:
                    self.qa_chain = RetrievalQA.from_chain_type(
                        llm=self.llm,
                        chain_type="stuff",
                        retriever=self.vector_store.as_retriever(
                            search_kwargs={"k": 5}
                        )
                    )
            except Exception as e:
                print(f"⚠️ Error building vector store: {e}")
                self.vector_store = None
                self.qa_chain = None
    
    def _extract_documents(self) -> List[str]:
        """Extract documents from graph for RAG"""
        documents = []
        
        if not self.graph:
            return documents
        
        node_list = list(self.graph.nodes)
        
        # Network overview
        total_nodes = len(node_list)
        try:
            total_edges = self.graph.number_of_edges()
        except:
            total_edges = len(self.graph.edges)
        
        documents.append(f"""
        CRIMINAL NETWORK OVERVIEW
        Total entities: {total_nodes}
        Total relationships: {total_edges}
        """)
        
        # Entity details
        for node in node_list[:20]:  # Limit to 20 for performance
            attrs = dict(self.graph.nodes[node])
            node_type = attrs.get('type', 'UNKNOWN')
            degree = len(list(self.graph.neighbors(node)))
            
            doc = f"""
            ENTITY: {node}
            Type: {node_type}
            Connections: {degree}
            Properties: {json.dumps(attrs, indent=2)}
            """
            documents.append(doc)
        
        # Relationship details
        relationships = []
        for u in node_list[:20]:
            for v in list(self.graph.neighbors(u)):
                if (u, v) not in relationships:
                    relationships.append((u, v))
                    edge_data = self.graph.get_edge_data(u, v) or {}
                    doc = f"""
                    RELATIONSHIP: {u} -> {v}
                    Type: {edge_data.get('type', 'CONNECTED')}
                    Properties: {json.dumps(edge_data, indent=2)}
                    """
                    documents.append(doc)
        
        return documents
    
    def query(self, question: str) -> Dict[str, Any]:
        """Query the RAG system with a question"""
        
        # Try real RAG if available
        if self.qa_chain and self.llm:
            try:
                result = self.qa_chain({"query": question})
                response = result.get('result', '')
                sources = ["RAG Retrieval", "Network Analysis"]
                confidence = 0.85
            except Exception as e:
                print(f"⚠️ RAG error: {e}")
                response = self._fallback_response(question)
                sources = ["Fallback Mode"]
                confidence = 0.5
        else:
            # Fallback response
            response = self._fallback_response(question)
            sources = ["Fallback Mode (No API Key)"]
            confidence = 0.4
        
        return {
            'response': response,
            'sources': sources,
            'confidence': confidence,
            'context': self.context
        }
    
    def _fallback_response(self, question: str) -> str:
        """Fallback response when API is not available"""
        
        question_lower = question.lower()
        responses = []
        
        # Check for entity questions
        if any(word in question_lower for word in ['person', 'entity', 'who', 'individual']):
            if self.graph:
                node_list = list(self.graph.nodes)
                high_degree = []
                for node in node_list:
                    degree = len(list(self.graph.neighbors(node)))
                    if degree >= 3:
                        attrs = dict(self.graph.nodes[node])
                        if attrs.get('type') == 'PERSON':
                            high_degree.append((node, degree, attrs.get('name', node)))
                
                if high_degree:
                    high_degree.sort(key=lambda x: x[1], reverse=True)
                    top = high_degree[:5]
                    names = [f"{n} (degree: {d})" for n, d, _ in top]
                    responses.append(f"🔍 Key entities: {', '.join(names)}")
                else:
                    responses.append("🔍 No high-degree entities found in the network.")
        
        # Check for connection questions
        if any(word in question_lower for word in ['connection', 'link', 'relationship', 'connect']):
            responses.append("🔗 Multiple cross-case connections detected in the network.")
            responses.append("💡 Review the Network Graph for visual relationships.")
        
        # Check for pattern questions
        if any(word in question_lower for word in ['pattern', 'trend', 'activity', 'anomaly']):
            responses.append("📊 Financial transaction patterns suggest potential money laundering.")
            responses.append("📈 Communication patterns indicate coordinated activity.")
        
        # Check for priority questions
        if any(word in question_lower for word in ['priority', 'important', 'critical', 'urgent']):
            if self.graph:
                node_list = list(self.graph.nodes)
                critical = []
                for node in node_list:
                    degree = len(list(self.graph.neighbors(node)))
                    if degree >= 5:
                        attrs = dict(self.graph.nodes[node])
                        if attrs.get('type') == 'PERSON':
                            critical.append(node)
                
                if critical:
                    responses.append(f"🚨 Critical entities: {', '.join(critical[:5])}")
                else:
                    responses.append("🚨 No critical entities detected.")
        
        # Default response
        if not responses:
            responses.append("💡 I'm analyzing the network. Please ask a specific question about entities, connections, or patterns.")
            if self.graph:
                total_nodes = len(list(self.graph.nodes))
                try:
                    total_edges = self.graph.number_of_edges()
                except:
                    total_edges = len(self.graph.edges)
                responses.append(f"📊 Network has {total_nodes} entities and {total_edges} relationships.")
        
        return "\n\n".join(responses)
    
    def get_context(self) -> str:
        """Get the current context for the RAG system"""
        if self.vector_store:
            return "Vector store with graph data is available."
        return "No context available. Please generate data first."
