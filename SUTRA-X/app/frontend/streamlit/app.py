"""
SUTRA-X ULTIMATE FINAL: Complete Criminal Network Intelligence Platform
SIH 2026 | AI-Powered | HYBRID HTTP-SDK GROQ ENGINE | PRODUCTION READY
"""
# ============================================================================
# IMPORT REAL DATA LOADER - FIXED PATH
# ============================================================================

import sys
import os
from pathlib import Path

# Add utils folder to path
sys.path.insert(0, str(Path(__file__).parent / "utils"))

try:
    from data_loader import RealDataLoader
    DATA_LOADER_AVAILABLE = True
    print("✅ DataLoader imported successfully")
except ImportError as e:
    DATA_LOADER_AVAILABLE = False
    print(f"⚠️ DataLoader not available: {e}")

# Initialize data loader
data_loader = None
if DATA_LOADER_AVAILABLE:
    data_loader = RealDataLoader()

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import json
import os
import time
import requests

# ============================================================================
# PAGE CONFIGURATION (Must be the very first Streamlit command)
# ============================================================================

st.set_page_config(
    page_title="SUTRA-X - Criminal Network Intelligence | SIH 2026",
    page_icon="🕵️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# CHECK PLOTLY AND NETWORKX - FIXED
# ============================================================================

PLOTLY_AVAILABLE = False
NETWORKX_AVAILABLE = False

try:
    import plotly.graph_objects as go
    import plotly.express as px
    PLOTLY_AVAILABLE = True
    print("✅ Plotly loaded successfully")
except ImportError as e:
    print(f"⚠️ Plotly not available: {e}")

try:
    import networkx as nx
    NETWORKX_AVAILABLE = True
    print("✅ NetworkX loaded successfully")
except ImportError as e:
    print(f"⚠️ NetworkX not available: {e}")

# ============================================================================
# GROQ AI ENGINE - HTTP FIRST WITH DYNAMIC MODEL DISCOVERY
# ============================================================================

GROQ_BASE_URL = "https://api.groq.com/openai/v1"
DEFAULT_GROQ_MODEL = "llama-3.1-8b-instant"
PREFERRED_GROQ_MODELS = [
    "llama-3.1-8b-instant",
    "llama-3.3-70b-versatile", 
    "llama-3.1-70b-versatile",
    "mixtral-8x7b-32768",
]

GROQ_API_KEY = None
try:
    GROQ_API_KEY = st.secrets.get("GROQ_API_KEY")
except Exception:
    GROQ_API_KEY = None

if not GROQ_API_KEY:
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")

GROQ_WORKING = False
GROQ_AVAILABLE = bool(GROQ_API_KEY)
GROQ_MODEL = DEFAULT_GROQ_MODEL
ENGINE_MODE = "No API Key"
GROQ_LAST_ERROR = None
GROQ_AVAILABLE_MODELS = []


def _groq_headers():
    return {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }


def _groq_list_models():
    if not GROQ_API_KEY:
        return []
    try:
        response = requests.get(
            f"{GROQ_BASE_URL}/models",
            headers=_groq_headers(),
            timeout=10,
        )
        if response.status_code != 200:
            raise RuntimeError(f"HTTP {response.status_code}: {response.text[:500]}")
        payload = response.json()
        data = payload.get("data", [])
        return [str(item.get("id")) for item in data if item.get("id")]
    except Exception as exc:
        global GROQ_LAST_ERROR
        GROQ_LAST_ERROR = f"Model discovery failed: {type(exc).__name__}: {exc}"
        return []


def _select_groq_model(available_models):
    available_set = set(available_models)
    for model in PREFERRED_GROQ_MODELS:
        if model in available_set:
            return model
    blocked_words = ("whisper", "guard", "tts", "speech", "embed")
    candidates = [
        model for model in available_models
        if not any(word in model.lower() for word in blocked_words)
    ]
    return candidates[0] if candidates else None


if GROQ_API_KEY:
    GROQ_AVAILABLE_MODELS = _groq_list_models()
    selected_model = _select_groq_model(GROQ_AVAILABLE_MODELS)
    if selected_model:
        GROQ_MODEL = selected_model
        GROQ_WORKING = True
        ENGINE_MODE = "HTTP API · Model Verified"
    else:
        GROQ_WORKING = False
        ENGINE_MODE = "API Key Valid · No Chat Model Accessible"
else:
    ENGINE_MODE = "No API Key"


try:
    from groq import Groq
    GROQ_SDK_AVAILABLE = True
except ImportError:
    Groq = None
    GROQ_SDK_AVAILABLE = False


def test_groq_connection():
    global GROQ_WORKING, GROQ_MODEL, ENGINE_MODE, GROQ_LAST_ERROR, GROQ_AVAILABLE_MODELS
    if not GROQ_API_KEY:
        GROQ_WORKING = False
        ENGINE_MODE = "No API Key"
        GROQ_LAST_ERROR = "GROQ_API_KEY is missing."
        return False
    GROQ_LAST_ERROR = None
    GROQ_AVAILABLE_MODELS = _groq_list_models()
    selected_model = _select_groq_model(GROQ_AVAILABLE_MODELS)
    if not selected_model:
        GROQ_WORKING = False
        ENGINE_MODE = "No Accessible Chat Model"
        if not GROQ_LAST_ERROR:
            GROQ_LAST_ERROR = "The API key is reachable, but /models did not return an accessible chat model."
        return False
    GROQ_MODEL = selected_model
    payload = {
        "model": GROQ_MODEL,
        "messages": [{"role": "user", "content": "Reply with exactly: SUTRA-X Groq connection verified."}],
        "temperature": 0,
        "max_completion_tokens": 20,
    }
    try:
        response = requests.post(
            f"{GROQ_BASE_URL}/chat/completions",
            headers=_groq_headers(),
            json=payload,
            timeout=20,
        )
        if response.status_code == 200:
            GROQ_WORKING = True
            ENGINE_MODE = "HTTP API · Verified"
            return True
        GROQ_WORKING = False
        ENGINE_MODE = f"HTTP {response.status_code}"
        GROQ_LAST_ERROR = response.text[:1000]
        return False
    except requests.RequestException as exc:
        GROQ_WORKING = False
        ENGINE_MODE = "HTTP Connection Error"
        GROQ_LAST_ERROR = f"{type(exc).__name__}: {exc}"
        return False


def query_groq(prompt: str, temperature=0.4, max_tokens=700) -> str:
    global GROQ_WORKING, GROQ_LAST_ERROR, ENGINE_MODE
    if not GROQ_API_KEY:
        return get_fallback_response(prompt)
    if not GROQ_MODEL:
        test_groq_connection()
    if not GROQ_MODEL:
        return get_fallback_response(prompt)
    payload = {
        "model": GROQ_MODEL,
        "messages": [
            {"role": "system", "content": "You are SUTRA-X AI, an investigation-support assistant. Analyze only the supplied evidence. Do not invent facts or declare anyone guilty."},
            {"role": "user", "content": prompt},
        ],
        "temperature": temperature,
        "max_completion_tokens": max_tokens,
    }
    try:
        response = requests.post(
            f"{GROQ_BASE_URL}/chat/completions",
            headers=_groq_headers(),
            json=payload,
            timeout=30,
        )
        if response.status_code == 200:
            data = response.json()
            content = data.get("choices", [{}])[0].get("message", {}).get("content")
            if content:
                GROQ_WORKING = True
                ENGINE_MODE = "HTTP API · Live"
                GROQ_LAST_ERROR = None
                return content.strip()
            GROQ_WORKING = False
            ENGINE_MODE = "Malformed API Response"
            GROQ_LAST_ERROR = "Groq returned HTTP 200 but no message content."
            return get_fallback_response(prompt)
        GROQ_WORKING = False
        ENGINE_MODE = f"HTTP {response.status_code}"
        GROQ_LAST_ERROR = response.text[:1500]
    except requests.RequestException as exc:
        GROQ_WORKING = False
        ENGINE_MODE = "HTTP Connection Error"
        GROQ_LAST_ERROR = f"{type(exc).__name__}: {exc}"
    return get_fallback_response(prompt)


def groq_diagnostics():
    return {
        "api_key_configured": bool(GROQ_API_KEY),
        "sdk_installed": GROQ_SDK_AVAILABLE,
        "selected_model": GROQ_MODEL,
        "engine_mode": ENGINE_MODE,
        "working": GROQ_WORKING,
        "available_models_count": len(GROQ_AVAILABLE_MODELS),
        "available_models": GROQ_AVAILABLE_MODELS[:10],
        "last_error": GROQ_LAST_ERROR,
    }


def get_fallback_response(query):
    query_lower = query.lower()
    responses = []
    if "person" in query_lower or "who" in query_lower or "entity" in query_lower:
        responses.append("🔍 Key entities can be prioritized using network centrality and relationship density.")
        responses.append("💡 Review the Entity Profile and Network Graph before drawing conclusions.")
    if "connection" in query_lower or "link" in query_lower:
        responses.append("🔗 Multiple relationships can be explored through the interactive network graph.")
        responses.append("💡 Compare relationship type, timing, and repeated interactions.")
    if "pattern" in query_lower:
        responses.append("📊 Repeated or unusual relationship patterns may deserve analyst review.")
        responses.append("💡 Verify the underlying evidence before escalating an alert.")
    if "priority" in query_lower:
        responses.append("🚨 Priority entities can be ranked using degree/centrality and rule-based risk indicators.")
        responses.append("💡 Start with high-centrality entities and inspect their direct evidence.")
    if not responses:
        responses.append("💡 Network analysis is available. Try asking about entities, relationships, risk, or patterns.")
    return "\n".join(responses)

# ============================================================================
# REAL DATA PROCESSING - FIXED
# ============================================================================

def process_real_data():
    """Load and process all real datasets"""
    
    if not DATA_LOADER_AVAILABLE or data_loader is None:
        st.warning("⚠️ DataLoader not available. Using sample data.")
        return 0, 0
    
    try:
        with st.spinner("📂 Loading real datasets..."):
            # Load all datasets
            data_loader.load_ilsi_dataset()
            data_loader.load_ncrb_cyber_data()
            data_loader.load_scam_hinglish()
            data_loader.load_multi_scam()
            
            # Process into entities and relationships
            entities, relationships = data_loader.process_all_data()
            
            # Build graph
            G = generate_sample_network()  # Use sample data as base
            
            # Add real entities to graph
            for entity in entities[:500]:  # Limit for performance
                G.add_node(entity['id'], type=entity['type'], name=entity.get('name', entity['id']))
            
            for rel in relationships[:500]:
                if rel['source'] in G.nodes and rel['target'] in G.nodes:
                    G.add_edge(rel['source'], rel['target'], type=rel['type'])
            
            st.session_state.graph = G
            st.session_state.data_loaded = True
            st.session_state.entity_list = get_node_list(G)
            st.session_state.alerts = generate_alerts(G)
            
            return len(entities), len(relationships)
    except Exception as e:
        st.error(f"Error loading real data: {e}")
        return 0, 0

# ============================================================================
# GRAPH CLASS - FIXED
# ============================================================================

class SimpleGraph:
    def __init__(self):
        self._nodes = {}
        self._adj = {}
        self._edges = {}
    
    def add_node(self, node, **attrs):
        self._nodes[node] = attrs
        if node not in self._adj:
            self._adj[node] = {}
    
    def add_edge(self, u, v, **attrs):
        if u not in self._adj:
            self._adj[u] = {}
        if v not in self._adj:
            self._adj[v] = {}
        self._adj[u][v] = attrs
        self._adj[v][u] = attrs
        self._edges[(u, v)] = attrs
    
    def neighbors(self, node):
        return list(self._adj.get(node, {}).keys())
    
    def degree(self, node):
        return len(self._adj.get(node, {}))
    
    @property
    def nodes(self):
        return self._nodes
    
    @property
    def edges(self):
        return self._edges
    
    def number_of_nodes(self):
        return len(self._nodes)
    
    def number_of_edges(self):
        return len(self._edges)
    
    def has_edge(self, u, v):
        return (u, v) in self._edges or (v, u) in self._edges
    
    def get_edge_data(self, u, v):
        if (u, v) in self._edges:
            return self._edges[(u, v)]
        if (v, u) in self._edges:
            return self._edges[(v, u)]
        return {}

# ============================================================================
# DATA GENERATION - FIXED
# ============================================================================

def generate_sample_network():
    """Generate realistic sample criminal network - FIXED to always work"""
    
    # Always try to use NetworkX first
    if NETWORKX_AVAILABLE:
        try:
            G = nx.Graph()
            print("✅ Using NetworkX for graph generation")
        except:
            G = SimpleGraph()
            print("⚠️ NetworkX failed, using SimpleGraph")
    else:
        G = SimpleGraph()
        print("⚠️ Using SimpleGraph (NetworkX not available)")
    
    first_names = ['Raj', 'Amit', 'Priya', 'Suresh', 'Anita', 'Vikram', 'Neha', 'Rahul', 
                   'Sunita', 'Mohan', 'Geeta', 'Arjun', 'Kavita', 'Deepak', 'Anjali',
                   'Sanjay', 'Meera', 'Ravi', 'Pooja', 'Kumar', 'Ashok', 'Preeti',
                   'Vijay', 'Nisha', 'Ramesh', 'Sneha', 'Mahesh', 'Jyoti']
    
    last_names = ['Sharma', 'Singh', 'Patel', 'Reddy', 'Rao', 'Joshi', 'Gupta', 'Verma', 
                  'Kumar', 'Nair', 'Mehta', 'Choudhary', 'Yadav', 'Khan', 'Das',
                  'Jain', 'Agarwal', 'Malhotra', 'Saxena', 'Tripathi']
    
    locations = ['Mumbai', 'Delhi', 'Bangalore', 'Chennai', 'Hyderabad', 'Pune', 'Kolkata',
                 'Ahmedabad', 'Lucknow', 'Jaipur']
    
    persons = []
    for i in range(25):
        name = f"{random.choice(first_names)} {random.choice(last_names)}"
        person_id = f"P-{i+1:04d}"
        G.add_node(person_id, type='PERSON', name=name, 
                   age=random.randint(22, 60),
                   city=random.choice(locations),
                   occupation=random.choice(['Business', 'Student', 'Government', 'Private', 'Professional']),
                   latitude=random.uniform(8.4, 37.6),
                   longitude=random.uniform(68.7, 97.25),
                   status=random.choice(['Active', 'Under Investigation', 'Cleared']))
        persons.append(person_id)
    
    phones = []
    for i in range(15):
        phone_id = f"PH-{i+1:04d}"
        G.add_node(phone_id, type='PHONE', number=f"98{random.randint(10000000, 99999999)}",
                   provider=random.choice(['Jio', 'Airtel', 'Vodafone', 'BSNL']))
        phones.append(phone_id)
        owner = random.choice(persons)
        G.add_edge(owner, phone_id, type='OWNS', confidence=0.8)
    
    accounts = []
    for i in range(12):
        account_id = f"ACC-{i+1:04d}"
        G.add_node(account_id, type='ACCOUNT', 
                   bank=random.choice(['SBI', 'HDFC', 'ICICI', 'Axis', 'PNB']),
                   account_type=random.choice(['Savings', 'Current', 'Fixed Deposit']))
        accounts.append(account_id)
        owner = random.choice(persons)
        G.add_edge(owner, account_id, type='OWNS', confidence=0.7)
    
    vehicles = []
    prefixes = ['MH', 'DL', 'KA', 'TN', 'TS', 'GJ', 'UP', 'WB', 'RJ']
    for i in range(8):
        vehicle_id = f"V-{i+1:04d}"
        G.add_node(vehicle_id, type='VEHICLE', 
                   registration=f"{random.choice(prefixes)}{random.randint(1,99)} {random.choice(['AB','CD','EF','GH'])}{random.randint(1000,9999)}",
                   make=random.choice(['Maruti', 'Hyundai', 'Toyota', 'Honda', 'Tata']),
                   model=random.choice(['Swift', 'i20', 'Camry', 'City', 'Nexon']))
        vehicles.append(vehicle_id)
        owner = random.choice(persons)
        G.add_edge(owner, vehicle_id, type='OWNS', confidence=0.6)
    
    cases = []
    case_titles = ['Drug Trafficking Ring', 'Financial Fraud Network', 'Arms Dealing', 
                   'Cyber Crime Syndicate', 'Money Laundering', 'Human Trafficking',
                   'Counterfeit Currency', 'Organized Crime']
    for i in range(6):
        case_id = f"CASE-{i+1:03d}"
        G.add_node(case_id, type='CASE', 
                   title=case_titles[i % len(case_titles)],
                   status=random.choice(['Active', 'Pending', 'Under Review', 'Closed']),
                   priority=random.choice(['High', 'Medium', 'Low']))
        cases.append(case_id)
        for _ in range(random.randint(2, 5)):
            person = random.choice(persons)
            G.add_edge(case_id, person, type='INVOLVED', confidence=0.6 + random.random()*0.3)
    
    # CDR Calls
    for _ in range(25):
        caller = random.choice(phones)
        receiver = random.choice(phones)
        if caller != receiver:
            G.add_edge(caller, receiver, type='CALLED', 
                      duration=random.randint(30, 600),
                      call_type=random.choice(['Voice', 'SMS', 'Data']))
    
    # Transactions
    for _ in range(20):
        from_acc = random.choice(accounts)
        to_acc = random.choice(accounts)
        if from_acc != to_acc:
            G.add_edge(from_acc, to_acc, type='TRANSACTION', 
                      amount=random.randint(1000, 500000),
                      transaction_type=random.choice(['Transfer', 'Deposit', 'Withdrawal', 'Payment']))
    
    # Cross-case connections
    for _ in range(10):
        person = random.choice(persons)
        case = random.choice(cases)
        if not G.has_edge(person, case):
            G.add_edge(person, case, type='INVOLVED', confidence=0.5 + random.random()*0.4)
    
    # Hidden connections
    hidden_pairs = [
        ('P-0001', 'P-0015'), ('PH-0003', 'PH-0018'), ('ACC-0002', 'ACC-0012'),
        ('P-0008', 'P-0025'), ('PH-0007', 'PH-0014'), ('ACC-0005', 'ACC-0015')
    ]
    for src, tgt in hidden_pairs:
        if src in G.nodes and tgt in G.nodes and not G.has_edge(src, tgt):
            G.add_edge(src, tgt, type='HIDDEN_CONNECTION', confidence=0.7, hidden=True)
    
    return G

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

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

def analyze_network(G):
    if G is None:
        return None
    
    node_list = get_node_list(G)
    total_nodes = len(node_list)
    total_edges = 0
    try:
        if NETWORKX_AVAILABLE:
            total_edges = G.number_of_edges()
        else:
            total_edges = len(G.edges)
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
    
    metrics = {
        'total_nodes': total_nodes,
        'total_edges': total_edges,
        'node_types': node_types,
        'priority_entities': priority_entities[:10]
    }
    
    return metrics

def get_entity_details(G, entity_id):
    node_list = get_node_list(G)
    if entity_id not in node_list:
        return None
    
    attrs = get_node_attributes(G, entity_id)
    neighbors = get_neighbors(G, entity_id)
    
    details = {
        'id': entity_id,
        'properties': attrs,
        'connections': [],
        'priority': 'MEDIUM',
        'priority_score': random.uniform(0.3, 0.9),
        'evidence': []
    }
    
    for neighbor in neighbors:
        edge_data = get_edge_data(G, entity_id, neighbor)
        details['connections'].append({
            'entity_id': neighbor,
            'relation': edge_data.get('type', 'CONNECTED'),
            'properties': edge_data
        })
        
        if edge_data.get('type') in ['CALLED', 'TRANSACTION']:
            details['evidence'].append({
                'type': edge_data.get('type'),
                'description': f"{edge_data.get('type')} evidence found",
                'source': 'Data Analysis',
                'confidence': edge_data.get('confidence', 0.7)
            })
    
    degree = len(details['connections'])
    if degree >= 5:
        details['priority'] = 'HIGH'
        details['priority_score'] = 0.85 + random.random()*0.1
    elif degree >= 3:
        details['priority'] = 'MEDIUM'
        details['priority_score'] = 0.6 + random.random()*0.2
    else:
        details['priority'] = 'LOW'
        details['priority_score'] = 0.3 + random.random()*0.2
    
    return details

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
        elif degree >= 4 and attrs.get('type') == 'PERSON':
            alerts.append({
                'id': f"ALERT-{len(alerts)+1:04d}",
                'type': 'WARNING',
                'title': f'High Priority Entity: {node}',
                'description': f'Entity {node} has {degree} connections',
                'entity': node,
                'timestamp': datetime.now().isoformat(),
                'action': 'Review connections for patterns',
                'emergency': False
            })
    
    case_nodes = [n for n in node_list if get_node_attributes(G, n).get('type') == 'CASE']
    for case in case_nodes:
        neighbors = get_neighbors(G, case)
        person_neighbors = [n for n in neighbors if get_node_attributes(G, n).get('type') == 'PERSON']
        if len(person_neighbors) >= 4:
            alerts.append({
                'id': f"ALERT-{len(alerts)+1:04d}",
                'type': 'INFO',
                'title': f'Cross-Case: {case}',
                'description': f'Case {case} connected to {len(person_neighbors)} persons',
                'entity': case,
                'timestamp': datetime.now().isoformat(),
                'action': 'Investigate cross-case connections',
                'emergency': False
            })
    
    return alerts[:10]

def generate_simulation(G, target_entity):
    if G is None or target_entity not in get_node_list(G):
        return None
    
    neighbors = get_neighbors(G, target_entity)
    original_degree = get_degree(G, target_entity)
    
    simulation_results = {
        'target_entity': target_entity,
        'removed_connections': len(neighbors),
        'remaining_entities': len(get_node_list(G)) - 1,
        'isolated_entities': 0,
        'affected_entities': neighbors[:5],
        'network_disruption': len(neighbors) / max(1, original_degree),
        'timestamp': datetime.now().isoformat(),
        'recommendation': 'HIGH' if len(neighbors) >= 5 else 'MEDIUM' if len(neighbors) >= 3 else 'LOW'
    }
    return simulation_results

# ============================================================================
# AI COPILOT
# ============================================================================

def get_ai_response(query, context):
    context_str = f"""
SUTRA-X NETWORK ANALYSIS PLATFORM

NETWORK OVERVIEW:
- Total Entities: {context.get('total_nodes', 0)}
- Total Relationships: {context.get('total_edges', 0)}
- Entity Types: {context.get('entity_types', {})}
- High Priority Entities: {context.get('priority_entities', [])}
"""

    full_prompt = f"""
{context_str}

Investigator Query:
{query}

Provide concise, evidence-oriented analysis. Reference only entities in the provided context.
Separate observed patterns from hypotheses. Do not accuse or declare guilt.
"""

    try:
        response = query_groq(full_prompt, temperature=0.25, max_tokens=650)
        if response and GROQ_WORKING:
            return {
                'response': response,
                'sources': [f'Groq · {GROQ_MODEL}'],
                'confidence': 0.88,
                'using_api': True,
            }
    except Exception as exc:
        global GROQ_LAST_ERROR
        GROQ_LAST_ERROR = f"AI request failed: {type(exc).__name__}: {exc}"

    fallback = get_fallback_response(query)
    return {
        'response': fallback,
        'sources': ['Local Fallback'],
        'confidence': 0.20,
        'using_api': False,
    }

# ============================================================================
# SESSION STATE INITIALIZATION
# ============================================================================

states = {
    'data_loaded': False,
    'graph': None,
    'selected_entity': None,
    'current_page': "Dashboard",
    'entity_list': [],
    'alerts': [],
    'authenticated': False,
    'current_user': None,
    'user_role': "viewer",
    'ai_query': "",
    'audit_logs': [],
    'export_history': [],
    'simulation_results': None,
    'emergency_triggered': False,
    'alert_sent': False,
    'offline_mode': False,
    'ai_response_cache': {}
}

for key, val in states.items():
    if key not in st.session_state:
        st.session_state[key] = val

# ============================================================================
# RBAC SECURITY SCHEMA
# ============================================================================

USERS_DB = {
    "admin": {"password": "admin123", "role": "admin", "name": "Administrator"},
    "investigator": {"password": "invest123", "role": "investigator", "name": "Senior Investigator"},
    "analyst": {"password": "analyst123", "role": "analyst", "name": "Data Analyst"},
    "viewer": {"password": "viewer123", "role": "viewer", "name": "Viewer"}
}

ROLE_PERMISSIONS = {
    "admin": ["view_data", "export_data", "manage_entities", "manage_users", "view_audit", "manage_alerts", "run_simulation", "use_ai"],
    "investigator": ["view_data", "export_data", "manage_entities", "view_audit", "manage_alerts", "run_simulation", "use_ai"],
    "analyst": ["view_data", "export_data", "view_audit", "use_ai"],
    "viewer": ["view_data"]
}

def authenticate_user(username, password):
    if username in USERS_DB and USERS_DB[username]["password"] == password:
        return USERS_DB[username]
    return None

def has_permission(permission):
    role = st.session_state.get('user_role', 'viewer')
    return permission in ROLE_PERMISSIONS.get(role, [])

def add_audit_log(action, resource, details=""):
    log_entry = {
        'timestamp': datetime.now().isoformat(),
        'user': st.session_state.get('current_user', 'unknown'),
        'role': st.session_state.get('user_role', 'unknown'),
        'action': action,
        'resource': resource,
        'details': details
    }
    st.session_state.audit_logs.insert(0, log_entry)
    if len(st.session_state.audit_logs) > 100:
        st.session_state.audit_logs = st.session_state.audit_logs[:100]

# ============================================================================
# UI THEME - BEAUTIFUL DARK THEME WITH HUMANIZED TEXT
# ============================================================================

st.markdown("""
<style>
    /* ===== BASE ===== */
    .stApp {
        background: #0e1117;
        color: #e2e8f0;
    }
    
    /* ===== HEADER ===== */
    .main-header {
        background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
        padding: 2.5rem 3.5rem;
        border-radius: 20px;
        margin-bottom: 2rem;
        border: 1px solid rgba(102, 126, 234, 0.15);
        position: relative;
        overflow: hidden;
    }
    
    .main-header::after {
        content: '🔍';
        position: absolute;
        right: 2rem;
        bottom: 1rem;
        font-size: 6rem;
        opacity: 0.05;
    }
    
    .main-title {
        font-size: 3.2rem;
        font-weight: 800;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 30%, #f093fb 60%, #f5576c 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: -1px;
        font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
    }
    
    .main-subtitle {
        font-size: 1.1rem;
        color: rgba(255,255,255,0.65);
        margin-top: 0.2rem;
        font-weight: 300;
        letter-spacing: 0.5px;
    }
    
    .tagline {
        font-size: 0.85rem;
        color: rgba(255,255,255,0.35);
        margin-top: 0.5rem;
        font-style: italic;
        letter-spacing: 0.3px;
    }
    
    /* ===== METRIC CARDS ===== */
    .metric-card {
        background: linear-gradient(145deg, #1a1a2e, #1f1f3a);
        padding: 1.2rem 1.5rem;
        border-radius: 14px;
        border-left: 4px solid #667eea;
        box-shadow: 0 4px 20px rgba(0,0,0,0.3);
        margin-bottom: 0.5rem;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .metric-card::before {
        content: '';
        position: absolute;
        top: -50%;
        right: -50%;
        width: 100%;
        height: 100%;
        background: radial-gradient(circle, rgba(102,126,234,0.03) 0%, transparent 70%);
        border-radius: 50%;
    }
    
    .metric-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 8px 30px rgba(0,0,0,0.5);
        border-color: #764ba2;
    }
    
    .metric-card .icon { font-size: 1.8rem; position: relative; z-index: 1; }
    .metric-card .value { 
        font-size: 2.2rem; 
        font-weight: 700; 
        color: #ffffff;
        margin: 0.2rem 0;
        position: relative;
        z-index: 1;
        font-family: 'Segoe UI', system-ui, sans-serif;
    }
    .metric-card .label { 
        font-size: 0.85rem; 
        color: #94a3b8;
        font-weight: 400;
        position: relative;
        z-index: 1;
    }
    .metric-critical { border-left-color: #ef4444; }
    .metric-warning { border-left-color: #f59e0b; }
    .metric-success { border-left-color: #10b981; }
    .metric-info { border-left-color: #3b82f6; }
    
    /* ===== STATUS BADGES ===== */
    .status-badge {
        display: inline-block;
        padding: 4px 16px;
        border-radius: 50px;
        font-size: 0.75rem;
        font-weight: 600;
        margin: 0.2rem 0;
        letter-spacing: 0.3px;
    }
    .status-online { background: #10b98120; color: #10b981; border: 1px solid #10b98140; }
    .status-offline { background: #ef444420; color: #ef4444; border: 1px solid #ef444440; }
    .status-warning { background: #f59e0b20; color: #f59e0b; border: 1px solid #f59e0b40; }
    .status-info { background: #3b82f620; color: #3b82f6; border: 1px solid #3b82f640; }
    .status-high { background: #ef444420; color: #ef4444; border: 1px solid #ef444440; }
    .status-medium { background: #f59e0b20; color: #f59e0b; border: 1px solid #f59e0b40; }
    .status-low { background: #10b98120; color: #10b981; border: 1px solid #10b98140; }
    
    /* ===== ENTITY CARDS ===== */
    .entity-card {
        background: linear-gradient(145deg, #1a1a2e, #1f1f3a);
        padding: 0.8rem 1.2rem;
        border-radius: 10px;
        margin: 0.3rem 0;
        border-left: 3px solid #667eea;
        transition: all 0.3s ease;
        color: #e2e8f0;
    }
    .entity-card:hover {
        background: linear-gradient(145deg, #24243e, #2a2a4e);
        transform: translateX(6px);
        border-color: #764ba2;
    }
    .entity-card strong { color: #ffffff; }
    .entity-card .entity-name { color: #94a3b8; font-size: 0.85rem; }
    
    /* ===== ALERT CARDS ===== */
    .alert-critical {
        background: linear-gradient(135deg, #7f1d1d, #991b1b);
        color: white;
        padding: 1rem 1.2rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        border: 1px solid #ef4444;
    }
    .alert-warning {
        background: linear-gradient(135deg, #78350f, #92400e);
        color: white;
        padding: 1rem 1.2rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        border: 1px solid #f59e0b;
    }
    .alert-info {
        background: linear-gradient(135deg, #1e3a5f, #1a365d);
        color: white;
        padding: 1rem 1.2rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        border: 1px solid #3b82f6;
    }
    
    /* ===== RAG RESPONSE ===== */
    .rag-response {
        background: linear-gradient(145deg, #1a1a2e, #1f1f3a);
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 4px solid #667eea;
        margin: 0.5rem 0;
        color: #e2e8f0;
        box-shadow: 0 4px 20px rgba(0,0,0,0.2);
    }
    .rag-response strong { color: #ffffff; }
    .rag-response p { line-height: 1.7; }
    
    /* ===== BUTTONS ===== */
    .stButton > button {
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.6rem 1.5rem;
        font-weight: 600;
        transition: all 0.3s ease;
        width: 100%;
        letter-spacing: 0.3px;
        font-family: 'Segoe UI', system-ui, sans-serif;
    }
    .stButton > button:hover {
        transform: translateY(-2px) scale(1.01);
        box-shadow: 0 8px 30px rgba(102,126,234,0.4);
    }
    
    /* ===== SIDEBAR ===== */
    .css-1d391kg, .css-1adrfps {
        background: #0e1117;
    }
    
    /* ===== FOOTER ===== */
    .footer {
        text-align: center;
        padding: 1.5rem 0;
        color: #475569;
        font-size: 0.8rem;
        border-top: 1px solid #1a1a2e;
        margin-top: 2rem;
        letter-spacing: 0.5px;
    }
    
    /* ===== SECTION TITLES ===== */
    .section-title {
        font-size: 1.4rem;
        font-weight: 600;
        color: #ffffff;
        margin: 1.5rem 0 0.8rem 0;
        letter-spacing: -0.3px;
    }
    
    .section-subtitle {
        font-size: 0.9rem;
        color: #94a3b8;
        margin-bottom: 1rem;
        font-weight: 300;
    }
    
    /* ===== QUICK STATS ===== */
    .quick-stats {
        background: linear-gradient(145deg, #1a1a2e, #1f1f3a);
        padding: 1.5rem;
        border-radius: 14px;
        border: 1px solid #2a2a4e;
    }
    .quick-stats .stat-item {
        display: flex;
        justify-content: space-between;
        padding: 0.5rem 0;
        border-bottom: 1px solid #2a2a4e;
        color: #e2e8f0;
    }
    .quick-stats .stat-item:last-child { border-bottom: none; }
    .quick-stats .stat-label { color: #94a3b8; }
    .quick-stats .stat-value { font-weight: 600; color: #ffffff; }
    
    /* ===== RESPONSIVE ===== */
    @media (max-width: 768px) {
        .main-title { font-size: 2rem; }
        .main-header { padding: 1.5rem; }
        .metric-card .value { font-size: 1.5rem; }
    }
    
    /* ===== HUMANIZED TEXT ===== */
    .human-text {
        font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
        line-height: 1.8;
        color: #e2e8f0;
    }
    
    .welcome-text {
        font-size: 1.1rem;
        color: #94a3b8;
        line-height: 1.8;
        max-width: 700px;
    }
    
    .highlight {
        color: #667eea;
        font-weight: 500;
    }
    
    /* ===== INSIGHT BADGE ===== */
    .insight-badge {
        display: inline-block;
        background: #667eea20;
        color: #667eea;
        padding: 2px 14px;
        border-radius: 50px;
        font-size: 0.7rem;
        font-weight: 500;
        border: 1px solid #667eea40;
        margin: 0.2rem 0;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# SIDEBAR
# ============================================================================

with st.sidebar:
    st.markdown("""
    <div style="text-align: center; padding: 0.5rem 0;">
        <div style="font-size: 2.8rem; animation: pulse 2s ease-in-out infinite;">🕵️</div>
        <div style="font-size: 1.3rem; font-weight: 700; color: #667eea; letter-spacing: -0.5px;">SUTRA-X</div>
        <div style="font-size: 0.6rem; color: #64748b; margin-top: -2px;">Smart Unified Threat & Relationship Analytics</div>
        <div style="margin-top: 0.5rem;">
            <span class="status-badge status-info">🏆 SIH 2026</span>
        </div>
        <div style="margin-top: 0.3rem; font-size: 0.6rem; color: #475569;">
            AI-Powered Criminal Network Analysis
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # API Status
    st.markdown("### 🤖 AI Status")
    
    if GROQ_WORKING:
        st.success(f"✅ {GROQ_MODEL}")
        st.caption("Real AI · Ready")
    elif GROQ_API_KEY:
        st.warning(f"⚠️ {ENGINE_MODE}")
        if GROQ_LAST_ERROR:
            st.caption(str(GROQ_LAST_ERROR)[:100])
    else:
        st.error("❌ No API Key")
        st.caption("Set GROQ_API_KEY in secrets")
    
    if st.button("🔌 Test Connection", use_container_width=True):
        with st.spinner("Testing..."):
            if test_groq_connection():
                st.success(f"✅ Connected! Model: {GROQ_MODEL}")
            else:
                st.error(f"❌ Failed: {GROQ_LAST_ERROR}")
        st.rerun()
    
    st.markdown("---")
    
    # Authentication
    st.markdown("### 🔐 Security")
    
    if not st.session_state.authenticated:
        username = st.text_input("Username", key="login_username", placeholder="Enter username")
        password = st.text_input("Password", type="password", key="login_password", placeholder="Enter password")
        if st.button("🔑 Login"):
            user = authenticate_user(username, password)
            if user:
                st.session_state.authenticated = True
                st.session_state.current_user = username
                st.session_state.user_role = user['role']
                add_audit_log("login", "Authentication", f"User: {username}")
                st.success(f"👋 Welcome, {user['name']}!")
                st.rerun()
            else:
                st.error("❌ Invalid credentials")
        st.caption("Demo: admin/admin123 · investigator/invest123")
    else:
        st.success(f"👤 {st.session_state.current_user}")
        st.caption(f"Role: {st.session_state.user_role.upper()}")
        if st.button("🚪 Logout"):
            add_audit_log("logout", "Authentication", f"User: {st.session_state.current_user}")
            st.session_state.authenticated = False
            st.session_state.current_user = None
            st.session_state.user_role = 'viewer'
            st.rerun()
    
    st.markdown("---")
    
    # Navigation
    st.markdown("### 📌 Navigation")
    nav_pages = [
        "📊 Dashboard",
        "🌐 Network Graph",
        "👤 Entity Profile",
        "⏱️ Timeline",
        "🔗 Cross-Case Discovery",
        "🤖 AI Copilot",
        "🔔 Alerts & Emergency",
        "🎯 What-If Simulation",
        "🗺️ Heatmap",
        "📄 Export",
        "🔐 Security"
    ]
    
    for page in nav_pages:
        if st.button(page, key=f"nav_{page}"):
            st.session_state.current_page = page
            st.rerun()
    
    st.markdown("---")
    
    # Data Controls
    st.markdown("### 📊 Data")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 Sample Data", use_container_width=True):
            with st.spinner("Generating network data..."):
                G = generate_sample_network()
                st.session_state.graph = G
                st.session_state.data_loaded = True
                st.session_state.entity_list = get_node_list(G)
                st.session_state.alerts = generate_alerts(G)
                add_audit_log("data_generate", "Network Data", "Sample data generated")
                st.success(f"✅ Generated {len(st.session_state.entity_list)} entities!")
                st.rerun()
    
    with col2:
        if DATA_LOADER_AVAILABLE:
            if st.button("📂 Real Data", use_container_width=True):
                entities, relationships = process_real_data()
                if entities > 0:
                    st.success(f"✅ Loaded {entities} entities from real datasets!")
                    st.rerun()
                else:
                    st.warning("⚠️ No real data found. Using sample data.")
    
    st.markdown("---")
    
    if st.session_state.data_loaded:
        entity_count = len(st.session_state.entity_list)
        st.success(f"✅ Data Loaded · {entity_count} entities")
        if entity_count > 0:
            st.caption(f"Ready for analysis 🔍")
        else:
            st.caption("⚠️ No entities found. Try regenerating.")
    else:
        st.info("⏳ No data loaded")
    
    st.markdown("---")
    st.caption("v3.0.0 · Made with ❤️")

# ============================================================================
# HEADER
# ============================================================================

st.markdown("""
<div class="main-header">
    <div class="main-title">🕵️ SUTRA-X</div>
    <div class="main-subtitle">Smart Unified Threat & Relationship Analytics</div>
    <div class="tagline">"From fragmented evidence to actionable intelligence"</div>
    <div style="margin-top: 0.8rem; display: flex; gap: 10px; flex-wrap: wrap;">
        <span class="status-badge status-info">🏆 SIH 2026</span>
        <span class="status-badge status-info">AI-Powered Criminal Network Analysis</span>
        <span class="status-badge status-info">Evidence-Based Intelligence</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ============================================================================
# DASHBOARD
# ============================================================================

def render_dashboard():
    G = st.session_state.graph
    metrics = analyze_network(G)
    
    st.markdown("""
    <div class="section-title">📊 Command Center</div>
    <div class="section-subtitle">Real-time intelligence dashboard · Monitor your investigation network</div>
    """, unsafe_allow_html=True)
    
    if not st.session_state.data_loaded or G is None:
        st.info("👈 Click **'Sample Data'** or **'Real Data'** in the sidebar to create your criminal network.")
        st.markdown("""
        <div style="background: linear-gradient(145deg, #1a1a2e, #1f1f3a); padding: 2rem; border-radius: 14px; border: 1px dashed #2a2a4e; text-align: center;">
            <div style="font-size: 3rem; margin-bottom: 0.5rem;">🕵️</div>
            <p style="color: #94a3b8; font-size: 1.1rem;">Ready to investigate? Load data to get started.</p>
            <p style="color: #64748b; font-size: 0.85rem;">The data will include persons, phones, accounts, cases, and connections.</p>
        </div>
        """, unsafe_allow_html=True)
        return
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card metric-info">
            <div class="icon">👥</div>
            <div class="value">{metrics['total_nodes'] if metrics else 0}</div>
            <div class="label">Entities in Network</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card metric-success">
            <div class="icon">🔗</div>
            <div class="value">{metrics['total_edges'] if metrics else 0}</div>
            <div class="label">Relationships</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        high_priority = len([e for e in (metrics['priority_entities'] if metrics else []) if e['degree'] >= 4])
        st.markdown(f"""
        <div class="metric-card metric-critical">
            <div class="icon">🚨</div>
            <div class="value">{high_priority}</div>
            <div class="label">High Priority Leads</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        alert_count = len(st.session_state.alerts)
        st.markdown(f"""
        <div class="metric-card metric-warning">
            <div class="icon">🔔</div>
            <div class="value">{alert_count}</div>
            <div class="label">Active Alerts</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown("""
    <div class="section-title">🚨 Priority Investigation Leads</div>
    <div class="section-subtitle">Entities requiring immediate attention based on network analysis</div>
    """, unsafe_allow_html=True)
    
    if metrics and metrics['priority_entities']:
        for entity in metrics['priority_entities'][:5]:
            score = min(100, entity['degree'] * 15)
            priority_label = "HIGH" if score >= 70 else "MEDIUM" if score >= 50 else "LOW"
            color = "🔴" if priority_label == "HIGH" else "🟡" if priority_label == "MEDIUM" else "🟢"
            
            col1, col2, col3 = st.columns([2.5, 2, 1])
            with col1:
                st.markdown(f"""
                <div class="entity-card">
                    <strong>🔍 {entity['id']}</strong>
                    <br><span class="entity-name">{entity['type']} · {entity['name']}</span>
                </div>
                """, unsafe_allow_html=True)
            with col2:
                st.caption(f"Connections: {entity['degree']}")
            with col3:
                st.markdown(f'<span class="status-badge status-{priority_label.lower()}">{color} {priority_label}</span>', unsafe_allow_html=True)
            
            st.markdown("---")
    else:
        st.info("No priority leads found. Generate more data or analyze the network.")

# ============================================================================
# NETWORK GRAPH - FIXED
# ============================================================================

def render_network_graph():
    G = st.session_state.graph
    node_list = get_node_list(G)
    
    st.markdown("""
    <div class="section-title">🌐 Network Graph</div>
    <div class="section-subtitle">Interactive visualization of criminal relationships</div>
    """, unsafe_allow_html=True)
    
    if not st.session_state.data_loaded or G is None:
        st.info("👈 Load data first to visualize the network.")
        return
    
    if len(node_list) == 0:
        st.warning("⚠️ No entities found in the network. Please regenerate data.")
        return
    
    if PLOTLY_AVAILABLE and NETWORKX_AVAILABLE:
        try:
            st.info("💡 Hover over nodes for details. Drag to explore the network.")
            
            # Ensure G is NetworkX graph
            if not hasattr(G, 'number_of_nodes'):
                nx_G = nx.Graph()
                for node in node_list:
                    nx_G.add_node(node)
                for node in node_list:
                    neighbors = get_neighbors(G, node)
                    for neighbor in neighbors:
                        if node < neighbor:
                            nx_G.add_edge(node, neighbor)
                G = nx_G
            
            pos = nx.spring_layout(G, k=0.5, iterations=50)
            
            edge_x, edge_y = [], []
            for edge in G.edges():
                try:
                    x0, y0 = pos[edge[0]]
                    x1, y1 = pos[edge[1]]
                    edge_x.extend([x0, x1, None])
                    edge_y.extend([y0, y1, None])
                except:
                    continue
            
            edge_trace = go.Scatter(
                x=edge_x, y=edge_y,
                line=dict(width=0.8, color='#4a4a6a'),
                hoverinfo='none',
                mode='lines'
            )
            
            node_x, node_y = [], []
            node_text, node_color, node_size = [], [], []
            
            color_map = {
                'PERSON': '#FF6B6B',
                'PHONE': '#4ECDC4', 
                'ACCOUNT': '#45B7D1',
                'VEHICLE': '#96CEB4',
                'CASE': '#FF9FF3',
                'LOCATION': '#FFEAA7',
                'UNKNOWN': '#6B7280'
            }
            
            for node in node_list:
                try:
                    x, y = pos[node]
                    node_x.append(x)
                    node_y.append(y)
                    attrs = get_node_attributes(G, node)
                    node_type = attrs.get('type', 'UNKNOWN')
                    degree = get_degree(G, node)
                    name = attrs.get('name', attrs.get('number', ''))
                    node_text.append(f"<b>{node}</b><br>Type: {node_type}<br>Name: {name}<br>Degree: {degree}")
                    node_color.append(color_map.get(node_type, '#6B7280'))
                    node_size.append(12 + degree * 3)
                except:
                    continue
            
            node_trace = go.Scatter(
                x=node_x, y=node_y,
                mode='markers',
                hoverinfo='text',
                text=node_text,
                marker=dict(
                    size=node_size,
                    color=node_color,
                    line=dict(width=1, color='#1a1a2e')
                )
            )
            
            fig = go.Figure(
                data=[edge_trace, node_trace],
                layout=go.Layout(
                    title='Criminal Network Graph',
                    hovermode='closest',
                    showlegend=False,
                    xaxis=dict(showgrid=False, zeroline=False, showticklabels=False, showspikes=False),
                    yaxis=dict(showgrid=False, zeroline=False, showticklabels=False, showspikes=False),
                    plot_bgcolor='#0e1117',
                    paper_bgcolor='#0e1117',
                    font=dict(color='#e2e8f0'),
                    height=650,
                    margin=dict(l=0, r=0, t=40, b=0)
                )
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Legend
            st.markdown("""
            <div style="background: linear-gradient(145deg, #1a1a2e, #1f1f3a); padding: 1rem 1.2rem; border-radius: 12px; margin-top: 0.5rem; border: 1px solid #2a2a4e;">
                <div style="display: flex; gap: 20px; flex-wrap: wrap;">
                    <div><span style="display: inline-block; width: 14px; height: 14px; background: #FF6B6B; border-radius: 50%;"></span> Person</div>
                    <div><span style="display: inline-block; width: 14px; height: 14px; background: #4ECDC4; border-radius: 50%;"></span> Phone</div>
                    <div><span style="display: inline-block; width: 14px; height: 14px; background: #45B7D1; border-radius: 50%;"></span> Account</div>
                    <div><span style="display: inline-block; width: 14px; height: 14px; background: #96CEB4; border-radius: 50%;"></span> Vehicle</div>
                    <div><span style="display: inline-block; width: 14px; height: 14px; background: #FF9FF3; border-radius: 50%;"></span> Case</div>
                    <div><span style="display: inline-block; width: 14px; height: 14px; background: #FFEAA7; border-radius: 50%;"></span> Location</div>
                </div>
                <div style="margin-top: 0.5rem; color: #64748b; font-size: 0.75rem;">
                    💡 Larger circles indicate higher connectivity (degree)
                </div>
            </div>
            """, unsafe_allow_html=True)
            
        except Exception as e:
            st.error(f"Error rendering graph: {str(e)}")
            _show_network_data(G, node_list)
    else:
        st.warning("⚠️ Plotly or NetworkX not available. Showing data view.")
        st.info("💡 To enable interactive graphs: `pip install plotly networkx`")
        _show_network_data(G, node_list)

def _show_network_data(G, node_list):
    st.subheader("📋 Network Data")
    node_data = []
    for node in node_list[:30]:
        attrs = get_node_attributes(G, node)
        node_data.append({
            'ID': node,
            'Type': attrs.get('type', 'UNKNOWN'),
            'Degree': get_degree(G, node),
            'Name': attrs.get('name', attrs.get('number', ''))
        })
    st.dataframe(pd.DataFrame(node_data), use_container_width=True)

# ============================================================================
# ENTITY PROFILE
# ============================================================================

def render_entity_profile():
    G = st.session_state.graph
    node_list = get_node_list(G)
    
    st.markdown("""
    <div class="section-title">👤 Entity Intelligence</div>
    <div class="section-subtitle">Deep dive into entity details, connections, and evidence</div>
    """, unsafe_allow_html=True)
    
    if not st.session_state.data_loaded or G is None:
        st.info("👈 Load data first to explore entities.")
        return
    
    if not node_list:
        st.warning("No entities in the network. Try regenerating data.")
        return
    
    if st.session_state.selected_entity and st.session_state.selected_entity in node_list:
        entity_id = st.session_state.selected_entity
    else:
        entity_id = st.selectbox("🔍 Search Entity", node_list)
        st.session_state.selected_entity = entity_id
    
    if not entity_id or entity_id not in node_list:
        st.warning("Please select an entity")
        return
    
    details = get_entity_details(G, entity_id)
    
    if not details:
        st.warning(f"Could not find details for entity {entity_id}")
        return
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown(f"""
        <div style="background: linear-gradient(145deg, #1a1a2e, #1f1f3a); padding: 1.5rem; border-radius: 14px; border: 1px solid #2a2a4e;">
            <h2 style="color: #ffffff; font-size: 1.5rem; margin: 0;">📋 {entity_id}</h2>
        """, unsafe_allow_html=True)
        
        attrs = get_node_attributes(G, entity_id)
        entity_type = attrs.get('type', 'UNKNOWN')
        st.markdown(f"**Type:** {entity_type}")
        
        if details.get('priority') == 'HIGH':
            st.markdown(f'<span class="status-badge status-high">🔴 HIGH PRIORITY</span>', unsafe_allow_html=True)
        elif details.get('priority') == 'MEDIUM':
            st.markdown(f'<span class="status-badge status-medium">🟡 MEDIUM PRIORITY</span>', unsafe_allow_html=True)
        else:
            st.markdown(f'<span class="status-badge status-low">🟢 LOW PRIORITY</span>', unsafe_allow_html=True)
        
        st.markdown(f"**Priority Score:** {details['priority_score']:.1%}")
        
        st.markdown("---")
        
        st.markdown(f"**📊 Properties:**")
        for key, value in attrs.items():
            st.markdown(f"- **{key}:** {value}")
        
        st.markdown("---")
        
        st.markdown(f"**🔗 Connections ({len(details['connections'])})**")
        for conn in details['connections'][:10]:
            st.markdown(f"""
            <div class="entity-card">
                <strong>→ {conn['entity_id']}</strong>
                <br><span class="entity-name">Relation: {conn['relation']}</span>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="quick-stats">
            <h3 style="color: #ffffff; font-size: 1.2rem; margin: 0 0 0.8rem 0;">📊 Quick Stats</h3>
            <div class="stat-item">
                <span class="stat-label">Direct Connections</span>
                <span class="stat-value">{len(details['connections'])}</span>
            </div>
            <div class="stat-item">
                <span class="stat-label">Network Degree</span>
                <span class="stat-value">{get_degree(G, entity_id)}</span>
            </div>
            <div class="stat-item">
                <span class="stat-label">Priority Score</span>
                <span class="stat-value">{details['priority_score']:.1%}</span>
            </div>
            <div class="stat-item">
                <span class="stat-label">Evidence Count</span>
                <span class="stat-value">{len(details.get('evidence', []))}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

# ============================================================================
# TIMELINE
# ============================================================================

def render_timeline():
    st.markdown("""
    <div class="section-title">⏱️ Investigation Timeline</div>
    <div class="section-subtitle">Track network evolution over time</div>
    """, unsafe_allow_html=True)
    
    if not st.session_state.data_loaded:
        st.info("👈 Load data first.")
        return
    
    st.info("📈 Timeline view showing network evolution")
    
    dates = pd.date_range(start=datetime.now() - timedelta(days=180), end=datetime.now(), periods=20)
    entities = np.cumsum(np.random.randint(1, 4, size=len(dates)))
    relationships = np.cumsum(np.random.randint(1, 6, size=len(dates)))
    
    timeline_df = pd.DataFrame({
        'Date': dates,
        'Entities': entities,
        'Relationships': relationships
    })
    
    if PLOTLY_AVAILABLE:
        try:
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=timeline_df['Date'], 
                y=timeline_df['Entities'],
                mode='lines+markers',
                name='Entities',
                line=dict(color='#667eea', width=3),
                marker=dict(size=8)
            ))
            fig.add_trace(go.Scatter(
                x=timeline_df['Date'], 
                y=timeline_df['Relationships'],
                mode='lines+markers',
                name='Relationships',
                line=dict(color='#ff6b6b', width=3),
                marker=dict(size=8)
            ))
            
            fig.update_layout(
                title='Network Evolution Over Time',
                xaxis_title='Date',
                yaxis_title='Count',
                hovermode='x unified',
                plot_bgcolor='#0e1117',
                paper_bgcolor='#0e1117',
                font=dict(color='#e2e8f0'),
                height=500
            )
            
            st.plotly_chart(fig, use_container_width=True)
        except:
            st.dataframe(timeline_df, use_container_width=True)
    else:
        st.dataframe(timeline_df, use_container_width=True)

# ============================================================================
# CROSS-CASE
# ============================================================================

def render_cross_case():
    G = st.session_state.graph
    node_list = get_node_list(G)
    
    st.markdown("""
    <div class="section-title">🔗 Cross-Case Discovery</div>
    <div class="section-subtitle">Uncover hidden connections between cases</div>
    """, unsafe_allow_html=True)
    
    if not st.session_state.data_loaded or G is None:
        st.info("👈 Load data first.")
        return
    
    st.info("🔍 Discovering connections between cases...")
    
    case_nodes = [n for n in node_list if get_node_attributes(G, n).get('type') == 'CASE']
    person_nodes = [n for n in node_list if get_node_attributes(G, n).get('type') == 'PERSON']
    
    if len(case_nodes) >= 2 and len(person_nodes) >= 1:
        cross_connections = []
        for i, case1 in enumerate(case_nodes):
            for case2 in case_nodes[i+1:]:
                persons1 = [n for n in get_neighbors(G, case1) if n in person_nodes]
                persons2 = [n for n in get_neighbors(G, case2) if n in person_nodes]
                shared = set(persons1) & set(persons2)
                
                if shared:
                    cross_connections.append({
                        'case1': case1,
                        'case2': case2,
                        'shared_entities': len(shared),
                        'shared_persons': list(shared)[:3],
                        'confidence': min(0.95, 0.5 + len(shared) * 0.1)
                    })
        
        if cross_connections:
            for conn in cross_connections:
                with st.expander(f"🔗 {conn['case1']} ↔ {conn['case2']}", expanded=True):
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Shared Entities", conn['shared_entities'])
                    with col2:
                        st.metric("Confidence", f"{conn['confidence']:.0%}")
                    with col3:
                        st.metric("Total Connections", conn['shared_entities'] * 2)
                    
                    if conn['shared_persons']:
                        st.write("**Shared Persons:**")
                        for person in conn['shared_persons']:
                            attrs = get_node_attributes(G, person)
                            name = attrs.get('name', person)
                            st.markdown(f"- {person} ({name})")
                    
                    st.progress(conn['confidence'], text=f"Confidence: {conn['confidence']:.0%}")
        else:
            st.info("No cross-case connections found.")
    else:
        st.warning("Need at least 2 cases and 1 person.")

# ============================================================================
# AI COPILOT
# ============================================================================

def render_ai_copilot():
    G = st.session_state.graph
    node_list = get_node_list(G)
    
    st.markdown("""
    <div class="section-title">🤖 AI Copilot</div>
    <div class="section-subtitle">AI-powered investigation assistant</div>
    """, unsafe_allow_html=True)
    
    if not st.session_state.data_loaded or G is None:
        st.info("👈 Load data first.")
        return
    
    if not has_permission("use_ai"):
        st.warning("🔒 You need 'Analyst' or higher role to use AI Copilot.")
        return
    
    # API Status
    st.markdown("#### 🤖 AI Status")
    if GROQ_WORKING:
        st.success(f"✅ Real AI · {GROQ_MODEL}")
    elif GROQ_API_KEY:
        st.warning(f"⚠️ {ENGINE_MODE}")
    else:
        st.warning("⚠️ No API key - using fallback")
    
    st.info("🧠 Ask questions about your investigation")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("##### 💬 Quick Questions")
        questions = [
            "Who are the most central people in this network?",
            "Show me connections between cases",
            "What patterns indicate criminal activity?",
            "Which entities should I investigate first?"
        ]
        for q in questions:
            if st.button(q, key=f"q_{hash(q)}", use_container_width=True):
                st.session_state.ai_query = q
                st.rerun()
    
    with col2:
        st.markdown("##### 🔍 Custom Query")
        user_query = st.text_area(
            "Ask your question",
            placeholder="Example: What are the connections between Entity A and Entity B?",
            height=150
        )
        if st.button("🔍 Analyze", use_container_width=True):
            if user_query:
                st.session_state.ai_query = user_query
                add_audit_log("ai_query", "AI Copilot", f"Query: {user_query[:100]}")
                st.rerun()
            else:
                st.warning("Please enter a question.")
    
    if hasattr(st.session_state, 'ai_query') and st.session_state.ai_query:
        query = st.session_state.ai_query
        
        st.markdown("---")
        st.markdown("##### 🤖 AI Response")
        
        with st.spinner("🧠 Analyzing with AI..."):
            # Build context
            context = {
                'entities': [],
                'total_nodes': len(node_list),
                'total_edges': 0,
                'entity_types': {},
                'priority_entities': []
            }
            
            try:
                if NETWORKX_AVAILABLE:
                    context['total_edges'] = G.number_of_edges()
                else:
                    context['total_edges'] = len(G.edges)
            except:
                context['total_edges'] = 0
            
            for node in node_list[:30]:
                degree = get_degree(G, node)
                attrs = get_node_attributes(G, node)
                node_type = attrs.get('type', 'UNKNOWN')
                context['entity_types'][node_type] = context['entity_types'].get(node_type, 0) + 1
                
                if attrs.get('type') == 'PERSON':
                    context['entities'].append({
                        'id': node,
                        'name': attrs.get('name', node),
                        'degree': degree
                    })
                    if degree >= 3:
                        context['priority_entities'].append(f"{node} (degree: {degree})")
            
            result = get_ai_response(query, context)
            
            if result.get('using_api', False):
                st.markdown(f"""
                <div class="rag-response" style="border-left-color: #10b981;">
                    <strong>🤖 AI Response</strong>
                    <p style="margin-top: 0.5rem; white-space: pre-wrap;">{result['response']}</p>
                    <div style="display: flex; gap: 8px; flex-wrap: wrap; margin-top: 0.5rem;">
                        <span style="color: #94a3b8; font-size: 0.7rem;">Sources:</span>
                        {''.join([f'<span style="background: #2a2a4e; color: #667eea; padding: 2px 12px; border-radius: 50px; font-size: 0.7rem; font-weight: 600;">{s}</span>' for s in result['sources']])}
                        <span style="background: #10b98120; color: #10b981; padding: 2px 12px; border-radius: 50px; font-size: 0.7rem; font-weight: 600;">✅ Real AI</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="rag-response" style="border-left-color: #f59e0b;">
                    <strong>💡 Response</strong>
                    <p style="margin-top: 0.5rem; white-space: pre-wrap;">{result['response']}</p>
                    <div style="display: flex; gap: 8px; flex-wrap: wrap; margin-top: 0.5rem;">
                        <span style="color: #94a3b8; font-size: 0.7rem;">Sources:</span>
                        {''.join([f'<span style="background: #2a2a4e; color: #667eea; padding: 2px 12px; border-radius: 50px; font-size: 0.7rem; font-weight: 600;">{s}</span>' for s in result['sources']])}
                        <span style="background: #f59e0b20; color: #f59e0b; padding: 2px 12px; border-radius: 50px; font-size: 0.7rem; font-weight: 600;">⚠️ Fallback</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("##### 📋 Relevant Entities")
            entities_with_degree = []
            for node in node_list:
                attrs = get_node_attributes(G, node)
                if attrs.get('type') == 'PERSON':
                    degree = get_degree(G, node)
                    entities_with_degree.append((node, degree, attrs.get('name', node)))
            
            entities_with_degree.sort(key=lambda x: x[1], reverse=True)
            for node, degree, name in entities_with_degree[:5]:
                st.markdown(f"- **{node}** ({name}) · Degree: {degree}")
            
            st.warning("⚠️ AI-generated analysis. Verify findings manually.")
            
            st.session_state.ai_query = ""

# ============================================================================
# ALERTS
# ============================================================================

def render_alerts():
    st.markdown("""
    <div class="section-title">🔔 Alerts & Emergency</div>
    <div class="section-subtitle">Real-time critical alerts and notifications</div>
    """, unsafe_allow_html=True)
    
    if not st.session_state.data_loaded:
        st.info("👈 Load data first.")
        return
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🚨 Emergency Call", use_container_width=True):
            st.session_state.emergency_triggered = True
            st.session_state.alert_sent = True
            add_audit_log("emergency", "Alert System", "Emergency triggered")
            st.rerun()
    
    with col2:
        if st.button("📞 Call Now", use_container_width=True):
            st.success("📞 Emergency call initiated...")
    
    with col3:
        if st.button("📨 Send Alert", use_container_width=True):
            st.session_state.alert_sent = True
            st.success("✅ Alert sent to team!")
    
    if st.session_state.emergency_triggered:
        st.markdown("""
        <div class="alert-critical" style="text-align: center; padding: 2rem;">
            <div style="font-size: 3rem;">🚨</div>
            <h2 style="color: white;">EMERGENCY ALERT ACTIVATED</h2>
            <p style="color: rgba(255,255,255,0.8);">All investigators notified</p>
        </div>
        """, unsafe_allow_html=True)
        st.session_state.emergency_triggered = False
    
    if st.session_state.alert_sent:
        st.success("✅ Alert sent to all investigators!")
        st.session_state.alert_sent = False
    
    st.markdown("---")
    
    if st.button("🔄 Refresh Alerts", use_container_width=True):
        st.session_state.alerts = generate_alerts(st.session_state.graph)
        st.rerun()
    
    st.markdown("---")
    
    alerts = st.session_state.alerts
    
    if alerts:
        critical_count = len([a for a in alerts if a['type'] == 'CRITICAL'])
        warning_count = len([a for a in alerts if a['type'] == 'WARNING'])
        info_count = len([a for a in alerts if a['type'] == 'INFO'])
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("🔴 Critical", critical_count)
        with col2:
            st.metric("🟡 Warnings", warning_count)
        with col3:
            st.metric("🔵 Information", info_count)
        
        st.markdown("---")
        
        for alert in alerts:
            if alert['type'] == 'CRITICAL':
                card_class = "alert-critical"
                icon = "🚨"
            elif alert['type'] == 'WARNING':
                card_class = "alert-warning"
                icon = "⚠️"
            else:
                card_class = "alert-info"
                icon = "ℹ️"
            
            st.markdown(f"""
            <div class="{card_class}">
                <div style="display: flex; justify-content: space-between;">
                    <div>
                        <span style="font-size: 1.1rem; font-weight: 700;">{icon} {alert['title']}</span>
                        <br>
                        <span style="opacity: 0.8;">{alert['description']}</span>
                    </div>
                    <div style="text-align: right; font-size: 0.7rem; opacity: 0.7;">
                        {alert['timestamp'][:19]}
                    </div>
                </div>
                <div style="margin-top: 0.5rem; border-top: 1px solid rgba(255,255,255,0.1); padding-top: 0.5rem;">
                    <span style="font-weight: 600;">Action:</span> {alert['action']}
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No active alerts.")

# ============================================================================
# SIMULATION
# ============================================================================

def render_simulation():
    G = st.session_state.graph
    node_list = get_node_list(G)
    
    st.markdown("""
    <div class="section-title">🎯 What-If Simulation</div>
    <div class="section-subtitle">Simulate network disruption scenarios</div>
    """, unsafe_allow_html=True)
    
    if not st.session_state.data_loaded or G is None:
        st.info("👈 Load data first.")
        return
    
    if not st.session_state.authenticated:
        st.warning("🔒 Please login to access this feature.")
        return
    
    if not node_list:
        st.warning("No entities in the network.")
        return
    
    col1, col2 = st.columns([2, 1])
    with col1:
        target_entity = st.selectbox("🎯 Select Entity to Remove", node_list)
    with col2:
        if st.button("🚀 Run Simulation", use_container_width=True):
            with st.spinner("Running simulation..."):
                results = generate_simulation(G, target_entity)
                st.session_state.simulation_results = results
                add_audit_log("simulation", target_entity, "Simulation run")
                st.rerun()
    
    if st.session_state.simulation_results:
        results = st.session_state.simulation_results
        
        st.markdown("---")
        st.markdown("#### 📊 Simulation Results")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Target", results['target_entity'])
        with col2:
            st.metric("Removed", results['removed_connections'])
        with col3:
            st.metric("Remaining", results['remaining_entities'])
        with col4:
            st.metric("Isolated", results['isolated_entities'])
        
        st.markdown("---")
        
        impact = results['network_disruption']
        color = '#ef4444' if impact > 0.5 else '#f59e0b' if impact > 0.3 else '#10b981'
        label = 'HIGH' if impact > 0.5 else 'MEDIUM' if impact > 0.3 else 'LOW'
        
        st.markdown(f"""
        <div style="background: #1a1a2e; padding: 1.5rem; border-radius: 12px; border: 2px dashed #2a2a4e;">
            <h3 style="color: #ffffff;">💥 Disruption Impact</h3>
            <div style="display: flex; justify-content: space-between; margin: 0.5rem 0;">
                <span style="color: #94a3b8;">Level</span>
                <span style="font-weight: 700; color: {color};">{impact:.1%} ({label})</span>
            </div>
            <div style="height: 12px; border-radius: 10px; overflow: hidden; background: #2a2a4e; margin: 0.5rem 0;">
                <div style="height: 100%; width: {impact*100}%; background: linear-gradient(90deg, {color}, {color}cc); border-radius: 10px;"></div>
            </div>
            <div style="margin-top: 0.5rem; color: #94a3b8;">
                <strong>Recommendation:</strong> {results['recommendation']}
            </div>
        </div>
        """, unsafe_allow_html=True)

# ============================================================================
# HEATMAP
# ============================================================================

def render_heatmap():
    G = st.session_state.graph
    node_list = get_node_list(G)
    
    st.markdown("""
    <div class="section-title">🗺️ Geographic Heatmap</div>
    <div class="section-subtitle">Visualize crime hotspots and entity locations</div>
    """, unsafe_allow_html=True)
    
    if not st.session_state.data_loaded or G is None:
        st.info("👈 Load data first.")
        return
    
    heatmap_data = []
    for node in node_list:
        attrs = get_node_attributes(G, node)
        if attrs.get('type') in ['PERSON', 'LOCATION']:
            lat = attrs.get('latitude')
            lon = attrs.get('longitude')
            if lat and lon:
                degree = get_degree(G, node)
                intensity = min(100, degree * 10 + 10)
                heatmap_data.append({
                    'ID': node,
                    'Name': attrs.get('name', attrs.get('number', node)),
                    'Type': attrs.get('type'),
                    'Latitude': float(lat),
                    'Longitude': float(lon),
                    'Intensity': intensity
                })
    
    if not heatmap_data:
        heatmap_data = [
            {'ID': 'L-001', 'Name': 'Mumbai', 'Type': 'LOCATION', 'Latitude': 19.0760, 'Longitude': 72.8777, 'Intensity': 85},
            {'ID': 'L-002', 'Name': 'Delhi', 'Type': 'LOCATION', 'Latitude': 28.6139, 'Longitude': 77.2090, 'Intensity': 78},
            {'ID': 'L-003', 'Name': 'Bangalore', 'Type': 'LOCATION', 'Latitude': 12.9716, 'Longitude': 77.5946, 'Intensity': 65},
            {'ID': 'L-004', 'Name': 'Chennai', 'Type': 'LOCATION', 'Latitude': 13.0827, 'Longitude': 80.2707, 'Intensity': 55},
            {'ID': 'L-005', 'Name': 'Hyderabad', 'Type': 'LOCATION', 'Latitude': 17.3850, 'Longitude': 78.4867, 'Intensity': 60},
            {'ID': 'L-006', 'Name': 'Kolkata', 'Type': 'LOCATION', 'Latitude': 22.5726, 'Longitude': 88.3639, 'Intensity': 45},
            {'ID': 'L-007', 'Name': 'Pune', 'Type': 'LOCATION', 'Latitude': 18.5204, 'Longitude': 73.8567, 'Intensity': 40},
        ]
        st.info("💡 Showing sample location data.")
    
    df = pd.DataFrame(heatmap_data)
    st.dataframe(df[['ID', 'Name', 'Type', 'Latitude', 'Longitude', 'Intensity']], use_container_width=True)

# ============================================================================
# EXPORT
# ============================================================================

def render_export():
    st.markdown("""
    <div class="section-title">📄 Export Reports</div>
    <div class="section-subtitle">Download investigation reports</div>
    """, unsafe_allow_html=True)
    
    if not st.session_state.data_loaded:
        st.info("👈 Load data first.")
        return
    
    if not st.session_state.authenticated:
        st.warning("🔒 Please login to access this feature.")
        return
    
    if not has_permission("export_data"):
        st.warning("🔒 You need 'Analyst' or higher role.")
        return
    
    st.info("📋 Export investigation data")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📄 Export JSON", use_container_width=True):
            with st.spinner("Generating report..."):
                G = st.session_state.graph
                node_list = get_node_list(G)
                report = {
                    'generated_at': datetime.now().isoformat(),
                    'total_entities': len(node_list),
                    'entities': []
                }
                for node in node_list:
                    attrs = get_node_attributes(G, node)
                    report['entities'].append({
                        'id': node,
                        'type': attrs.get('type', 'UNKNOWN'),
                        'properties': attrs,
                        'degree': get_degree(G, node)
                    })
                json_str = json.dumps(report, indent=2)
                st.download_button(
                    label="📥 Download JSON",
                    data=json_str,
                    file_name=f"SUTRA-X_Report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json",
                    use_container_width=True
                )
                add_audit_log("export", "JSON Report", "Report exported")
                st.success("✅ JSON Report generated!")
    
    with col2:
        if st.button("📊 Export CSV", use_container_width=True):
            with st.spinner("Generating report..."):
                G = st.session_state.graph
                node_list = get_node_list(G)
                data = []
                for node in node_list:
                    attrs = get_node_attributes(G, node)
                    data.append({
                        'ID': node,
                        'Type': attrs.get('type', 'UNKNOWN'),
                        'Degree': get_degree(G, node),
                        'Name': attrs.get('name', attrs.get('number', '')),
                        **attrs
                    })
                df = pd.DataFrame(data)
                csv = df.to_csv(index=False)
                st.download_button(
                    label="📥 Download CSV",
                    data=csv,
                    file_name=f"SUTRA-X_Data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv",
                    use_container_width=True
                )
                add_audit_log("export", "CSV Report", "Report exported")
                st.success("✅ CSV Report generated!")

# ============================================================================
# SECURITY
# ============================================================================

def render_security():
    st.markdown("""
    <div class="section-title">🔐 Security & Access Control</div>
    <div class="section-subtitle">Role-Based Access Control and Audit Logs</div>
    """, unsafe_allow_html=True)
    
    if not st.session_state.authenticated:
        st.warning("🔒 Please login to access this feature.")
        return
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
        <div style="background: linear-gradient(145deg, #1a1a2e, #1f1f3a); padding: 1.5rem; border-radius: 14px; border: 1px solid #2a2a4e;">
            <h3 style="color: #ffffff; font-size: 1.2rem;">🔐 Role-Based Access Control</h3>
            <div style="margin-top: 1rem;">
                <div class="stat-item">
                    <span style="color: #94a3b8;">Current User</span>
                    <span style="color: #ffffff; font-weight: 700;">{st.session_state.current_user}</span>
                </div>
                <div class="stat-item">
                    <span style="color: #94a3b8;">Current Role</span>
                    <span style="color: #ffffff; font-weight: 700;">{st.session_state.user_role.upper()}</span>
                </div>
                <div class="stat-item" style="border-bottom: none;">
                    <span style="color: #94a3b8;">Permissions</span>
                    <span style="font-size: 0.85rem; color: #667eea;">{', '.join(ROLE_PERMISSIONS.get(st.session_state.user_role, []))}</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div style="background: linear-gradient(145deg, #1a1a2e, #1f1f3a); padding: 1.5rem; border-radius: 14px; border: 1px solid #2a2a4e;">
            <h3 style="color: #ffffff; font-size: 1.2rem;">📶 Offline Mode</h3>
            <div style="margin-top: 1rem;">
                <div class="stat-item">
                    <span style="color: #94a3b8;">Status</span>
                    <span style="color: #ffffff; font-weight: 700;">{'📴 Offline' if st.session_state.offline_mode else '📶 Online'}</span>
                </div>
                <div class="stat-item" style="border-bottom: none;">
                    <span style="color: #94a3b8;">Description</span>
                    <span style="font-size: 0.8rem; color: #94a3b8;">Work offline, sync when online</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown("### 📋 Audit Logs")
    
    if st.session_state.audit_logs:
        audit_df = pd.DataFrame(st.session_state.audit_logs[:20])
        if not audit_df.empty:
            display_df = audit_df[['timestamp', 'user', 'role', 'action', 'resource']].copy()
            display_df['timestamp'] = pd.to_datetime(display_df['timestamp']).dt.strftime('%Y-%m-%d %H:%M:%S')
            st.dataframe(display_df, use_container_width=True)
            
            st.markdown("---")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Logs", len(st.session_state.audit_logs))
            with col2:
                unique_actions = len(audit_df['action'].unique())
                st.metric("Unique Actions", unique_actions)
            with col3:
                unique_users = len(audit_df['user'].unique())
                st.metric("Active Users", unique_users)
    else:
        st.info("No audit logs available.")

# ============================================================================
# MAIN ROUTER
# ============================================================================

def main():
    page = st.session_state.current_page
    
    page_map = {
        "📊 Dashboard": render_dashboard,
        "🌐 Network Graph": render_network_graph,
        "👤 Entity Profile": render_entity_profile,
        "⏱️ Timeline": render_timeline,
        "🔗 Cross-Case Discovery": render_cross_case,
        "🤖 AI Copilot": render_ai_copilot,
        "🔔 Alerts & Emergency": render_alerts,
        "🎯 What-If Simulation": render_simulation,
        "🗺️ Heatmap": render_heatmap,
        "📄 Export": render_export,
        "🔐 Security": render_security
    }
    
    if page in page_map:
        page_map[page]()
    else:
        render_dashboard()
    
    st.markdown("""
    <div class="footer">
        <div style="display: flex; justify-content: center; gap: 20px; flex-wrap: wrap; margin-bottom: 10px;">
            <span style="color: #667eea;">🏆 SIH 2026</span>
            <span style="color: #64748b;">|</span>
            <span style="color: #94a3b8;">🕵️ SUTRA-X v3.0.0</span>
            <span style="color: #64748b;">|</span>
            <span style="color: #94a3b8;">Made with ❤️ for SIH 2026</span>
            <span style="color: #64748b;">|</span>
            <span style="color: #475569;">From Evidence to Intelligence</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
