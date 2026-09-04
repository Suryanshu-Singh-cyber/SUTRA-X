"""
SUTRA-X: Smart Unified Threat & Relationship Analytics
AI-Powered Criminal Network Investigation & Intelligence Platform
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import json
from pathlib import Path
import sys
import os

# ============================================================================
# FALLBACK FOR NETWORKX (if not installed)
# ============================================================================

try:
    import networkx as nx
    NETWORKX_AVAILABLE = True
except ImportError:
    NETWORKX_AVAILABLE = False

try:
    import plotly.graph_objects as go
    import plotly.express as px
    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False

# ============================================================================
# SIMPLE GRAPH CLASS (Fallback if networkx not available)
# ============================================================================

class SimpleGraph:
    """Simple graph implementation as fallback"""
    
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
# PAGE CONFIGURATION
# ============================================================================

st.set_page_config(
    page_title="SUTRA-X - Criminal Network Intelligence",
    page_icon="🕵️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main-title {
        font-size: 3rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        padding: 1rem 0;
    }
    .sub-title {
        font-size: 1.2rem;
        color: #666;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        border-left: 4px solid #667eea;
    }
    .status-badge {
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
        display: inline-block;
    }
    .status-high {
        background: #ff6b6b;
        color: white;
    }
    .status-medium {
        background: #feca57;
        color: #333;
    }
    .status-low {
        background: #48dbfb;
        color: #333;
    }
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-weight: 600;
        border: none;
        padding: 0.5rem 2rem;
        border-radius: 30px;
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 20px rgba(102, 126, 234, 0.4);
    }
    </style>
""", unsafe_allow_html=True)

# ============================================================================
# SESSION STATE INITIALIZATION
# ============================================================================

if 'data_loaded' not in st.session_state:
    st.session_state.data_loaded = False
if 'graph' not in st.session_state:
    st.session_state.graph = None
if 'selected_entity' not in st.session_state:
    st.session_state.selected_entity = None
if 'current_page' not in st.session_state:
    st.session_state.current_page = "Dashboard"
if 'sample_data_generated' not in st.session_state:
    st.session_state.sample_data_generated = False
if 'entity_list' not in st.session_state:
    st.session_state.entity_list = []

# ============================================================================
# DATA GENERATION FUNCTIONS
# ============================================================================

def generate_sample_network():
    """Generate a sample criminal network with realistic Indian data"""
    
    # Use NetworkX if available, otherwise use SimpleGraph
    if NETWORKX_AVAILABLE:
        G = nx.Graph()
    else:
        G = SimpleGraph()
    
    # Indian names
    first_names = ['Raj', 'Amit', 'Priya', 'Suresh', 'Anita', 'Vikram', 'Neha', 'Rahul', 
                   'Sunita', 'Mohan', 'Geeta', 'Arjun', 'Kavita', 'Deepak', 'Anjali', 
                   'Sanjay', 'Meera', 'Ravi', 'Pooja', 'Kumar', 'Ashok', 'Preeti',
                   'Vijay', 'Nisha', 'Ramesh', 'Sneha', 'Mahesh', 'Jyoti']
    
    last_names = ['Sharma', 'Singh', 'Patel', 'Reddy', 'Rao', 'Joshi', 'Gupta', 'Verma', 
                  'Kumar', 'Nair', 'Mehta', 'Choudhary', 'Yadav', 'Khan', 'Das']
    
    # Create core criminal network
    num_persons = 25
    persons = []
    for i in range(num_persons):
        name = f"{random.choice(first_names)} {random.choice(last_names)}"
        person_id = f"P-{i+1:04d}"
        G.add_node(person_id, type='PERSON', name=name, 
                   age=random.randint(22, 60),
                   city=random.choice(['Mumbai', 'Delhi', 'Bangalore', 'Chennai', 'Hyderabad', 'Pune']))
        persons.append(person_id)
    
    # Add phones
    phones = []
    for i in range(20):
        phone_id = f"PH-{i+1:04d}"
        number = f"98{random.randint(10000000, 99999999)}"
        G.add_node(phone_id, type='PHONE', number=number)
        phones.append(phone_id)
        owner = random.choice(persons)
        G.add_edge(owner, phone_id, type='OWNS', confidence=0.8)
    
    # Add accounts
    accounts = []
    for i in range(15):
        account_id = f"ACC-{i+1:04d}"
        G.add_node(account_id, type='ACCOUNT', 
                   bank=random.choice(['SBI', 'HDFC', 'ICICI', 'Axis', 'PNB']))
        accounts.append(account_id)
        owner = random.choice(persons)
        G.add_edge(owner, account_id, type='OWNS', confidence=0.7)
    
    # Add vehicles
    vehicles = []
    vehicle_prefixes = ['MH', 'DL', 'KA', 'TN', 'TS', 'GJ']
    for i in range(10):
        vehicle_id = f"V-{i+1:04d}"
        reg = f"{random.choice(vehicle_prefixes)}{random.randint(1,99)} {random.choice(['AB','CD','EF','GH'])}{random.randint(1000,9999)}"
        G.add_node(vehicle_id, type='VEHICLE', registration=reg,
                   make=random.choice(['Maruti', 'Hyundai', 'Toyota', 'Honda']))
        vehicles.append(vehicle_id)
        owner = random.choice(persons)
        G.add_edge(owner, vehicle_id, type='OWNS', confidence=0.6)
    
    # Add locations
    locations = []
    location_names = ['Connaught Place', 'Bandra West', 'Indiranagar', 'T. Nagar', 
                      'Hitech City', 'Juhu', 'Koramangala', 'Marine Drive']
    for i in range(8):
        loc_id = f"L-{i+1:04d}"
        G.add_node(loc_id, type='LOCATION', 
                   name=location_names[i] if i < len(location_names) else f"Location {i+1}",
                   city=random.choice(['Mumbai', 'Delhi', 'Bangalore', 'Chennai', 'Hyderabad']))
        locations.append(loc_id)
    
    # Add cases
    cases = []
    case_titles = ['Drug Trafficking Ring', 'Financial Fraud Network', 'Arms Dealing', 
                   'Cyber Crime Syndicate', 'Money Laundering', 'Human Trafficking']
    for i in range(6):
        case_id = f"CASE-{i+1:03d}"
        G.add_node(case_id, type='CASE', 
                   title=case_titles[i] if i < len(case_titles) else f"Case {i+1}",
                   status=random.choice(['Active', 'Pending', 'Under Review']))
        cases.append(case_id)
        for _ in range(random.randint(2, 5)):
            person = random.choice(persons)
            G.add_edge(case_id, person, type='INVOLVED', confidence=0.6 + random.random()*0.3)
    
    # Add phone calls (CDR)
    for _ in range(30):
        caller = random.choice(phones)
        receiver = random.choice(phones)
        if caller != receiver:
            G.add_edge(caller, receiver, type='CALLED', 
                      duration=random.randint(30, 600),
                      timestamp=(datetime.now() - timedelta(days=random.randint(1, 30))).isoformat())
    
    # Add financial transactions
    for _ in range(25):
        from_acc = random.choice(accounts)
        to_acc = random.choice(accounts)
        if from_acc != to_acc:
            amount = random.randint(5000, 500000)
            G.add_edge(from_acc, to_acc, type='TRANSACTION',
                      amount=amount,
                      timestamp=(datetime.now() - timedelta(days=random.randint(1, 60))).isoformat())
    
    # Add location visits
    for _ in range(20):
        person = random.choice(persons)
        location = random.choice(locations)
        G.add_edge(person, location, type='VISITED',
                  timestamp=(datetime.now() - timedelta(days=random.randint(1, 90))).isoformat())
    
    # Create some cross-case connections
    for _ in range(8):
        person = random.choice(persons)
        case = random.choice(cases)
        try:
            if not G.has_edge(person, case):
                G.add_edge(person, case, type='INVOLVED', confidence=0.5 + random.random()*0.4)
        except:
            G.add_edge(person, case, type='INVOLVED', confidence=0.5 + random.random()*0.4)
    
    return G

def get_node_list(G):
    """Safely get list of nodes from graph"""
    try:
        if NETWORKX_AVAILABLE:
            return list(G.nodes())
        else:
            return list(G.nodes)
    except:
        return []

def get_node_attributes(G, node):
    """Safely get node attributes"""
    try:
        if NETWORKX_AVAILABLE:
            return dict(G.nodes[node])
        else:
            return G.nodes[node]
    except:
        return {}

def get_neighbors(G, node):
    """Safely get neighbors of a node"""
    try:
        return list(G.neighbors(node))
    except:
        return []

def get_degree(G, node):
    """Safely get degree of a node"""
    try:
        return G.degree(node)
    except:
        return len(get_neighbors(G, node))

def get_edge_data(G, u, v):
    """Safely get edge data"""
    try:
        return G.get_edge_data(u, v)
    except:
        return {}

# ============================================================================
# ANALYZER FUNCTIONS
# ============================================================================

def analyze_network(G):
    """Analyze the network and return metrics"""
    
    if G is None:
        return None
    
    node_list = get_node_list(G)
    
    # Get counts
    total_nodes = len(node_list)
    total_edges = 0
    try:
        if NETWORKX_AVAILABLE:
            total_edges = G.number_of_edges()
        else:
            total_edges = len(G.edges)
    except:
        total_edges = 0
    
    # Count node types
    node_types = {}
    for node in node_list:
        attrs = get_node_attributes(G, node)
        node_type = attrs.get('type', 'UNKNOWN')
        node_types[node_type] = node_types.get(node_type, 0) + 1
    
    # Find high-degree entities
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
    """Get detailed information about an entity"""
    
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
        'priority_score': random.uniform(0.3, 0.9)
    }
    
    # Get connections
    for neighbor in neighbors:
        edge_data = get_edge_data(G, entity_id, neighbor)
        if not edge_data:
            edge_data = get_edge_data(G, neighbor, entity_id)
        
        details['connections'].append({
            'entity_id': neighbor,
            'relation': edge_data.get('type', 'CONNECTED'),
            'properties': edge_data
        })
    
    # Calculate priority based on degree
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

# ============================================================================
# SIDEBAR
# ============================================================================

with st.sidebar:
    st.markdown("## 🕵️ SUTRA-X")
    st.caption("Smart Unified Threat & Relationship Analytics")
    st.markdown("---")
    
    # Navigation
    st.subheader("📌 Navigation")
    pages = ["Dashboard", "Network Graph", "Entity Profile", "Timeline", "Cross-Case", "AI Assistant"]
    selected_page = st.radio("Go to", pages, index=pages.index(st.session_state.current_page))
    st.session_state.current_page = selected_page
    
    st.markdown("---")
    
    # Data controls
    st.subheader("📊 Data Controls")
    
    if st.button("🔄 Generate Sample Data", use_container_width=True):
        with st.spinner("Generating sample criminal network..."):
            G = generate_sample_network()
            st.session_state.graph = G
            st.session_state.data_loaded = True
            st.session_state.sample_data_generated = True
            st.session_state.entity_list = get_node_list(G)
            st.success(f"✅ Generated network with data")
            st.rerun()
    
    st.markdown("---")
    st.caption("v1.0.0 | AI-Powered Investigation")

# ============================================================================
# MAIN CONTENT
# ============================================================================

if not st.session_state.data_loaded or st.session_state.graph is None:
    # Landing page
    st.markdown('<h1 class="main-title">🕵️ SUTRA-X</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-title">Smart Unified Threat & Relationship Analytics</p>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <h3>📊 Multi-Source</h3>
            <p>Ingest data from FIR, CDR, transactions, vehicles, and more</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <h3>🧠 AI-Powered</h3>
            <p>Entity extraction, relationship discovery, and intelligent prioritization</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <h3>🎯 Actionable</h3>
            <p>Evidence-backed leads with investigation briefs in 30 seconds</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.info("👈 **Get Started:** Click 'Generate Sample Data' in the sidebar to explore the platform.")
    
    with st.expander("🎯 What SUTRA-X Does", expanded=True):
        st.markdown("""
        **SUTRA-X helps investigators:**
        
        1. **🔍 Connect the dots** across multiple cases and evidence sources
        2. **🕵️ Discover hidden relationships** that traditional methods miss
        3. **🎯 Prioritize investigation** with AI-powered scoring
        4. **📋 Explain every insight** with supporting evidence
        5. **🌐 Work in multiple languages** (English, Hindi, Tamil, Telugu, Bengali)
        
        **💡 USP:** *From fragmented evidence to explainable investigative leads in 30 seconds*
        """)

else:
    G = st.session_state.graph
    node_list = get_node_list(G)
    metrics = analyze_network(G)
    
    # ========================================================================
    # DASHBOARD
    # ========================================================================
    if selected_page == "Dashboard":
        st.markdown('<h1 class="main-title">📊 Command Center</h1>', unsafe_allow_html=True)
        
        # Metrics row
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Entities", metrics['total_nodes'] if metrics else 0)
        with col2:
            st.metric("Relationships", metrics['total_edges'] if metrics else 0)
        with col3:
            high_priority = len([e for e in (metrics['priority_entities'] if metrics else []) if e['degree'] >= 4])
            st.metric("High Priority Leads", high_priority, delta="🚨 Immediate")
        with col4:
            cross_case = 0
            for node in node_list:
                attrs = get_node_attributes(G, node)
                if attrs.get('type') == 'PERSON':
                    neighbors = get_neighbors(G, node)
                    case_connections = sum(1 for n in neighbors if get_node_attributes(G, n).get('type') == 'CASE')
                    if case_connections >= 2:
                        cross_case += 1
            st.metric("Cross-Case Links", cross_case, delta="🔗 Connections")
        
        st.markdown("---")
        
        # Priority Leads
        st.subheader("🚨 Priority Investigation Leads")
        
        if metrics and metrics['priority_entities']:
            for entity in metrics['priority_entities'][:5]:
                col1, col2, col3, col4 = st.columns([2, 2, 1, 1])
                with col1:
                    st.markdown(f"**🔍 {entity['id']}**")
                    st.caption(f"Type: {entity['type']} | {entity['name']}")
                with col2:
                    st.caption(f"Connections: {entity['degree']}")
                with col3:
                    score = min(100, entity['degree'] * 15)
                    color = "🟢" if score < 50 else "🟡" if score < 70 else "🔴"
                    st.caption(f"Priority: {color} {score}%")
                with col4:
                    if st.button("View", key=f"view_dash_{entity['id']}"):
                        st.session_state.selected_entity = entity['id']
                        st.session_state.current_page = "Entity Profile"
                        st.rerun()
                
                st.markdown("---")
        else:
            st.info("No priority leads found. Generate more data.")
        
        # Network Stats
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📈 Network Statistics")
            if metrics:
                stats_data = {
                    'Metric': ['Total Nodes', 'Total Edges', 'Node Types'],
                    'Value': [
                        metrics.get('total_nodes', 0),
                        metrics.get('total_edges', 0),
                        ', '.join([f"{k}: {v}" for k, v in metrics.get('node_types', {}).items()])
                    ]
                }
                st.table(pd.DataFrame(stats_data))
        
        with col2:
            st.subheader("🔗 Recent Activity")
            activities = [
                "New connection discovered in the network",
                "Cross-case link identified",
                "Priority lead updated",
                "Network analysis complete"
            ]
            for activity in activities:
                st.markdown(f"• {activity}")

    # ========================================================================
    # NETWORK GRAPH
    # ========================================================================
    elif selected_page == "Network Graph":
        st.markdown('<h1 class="main-title">🌐 Network Graph</h1>', unsafe_allow_html=True)
        
        if PLOTLY_AVAILABLE and NETWORKX_AVAILABLE and len(node_list) > 1:
            st.info("🌐 Interactive network visualization.")
            
            try:
                # Use spring layout
                pos = nx.spring_layout(G, k=0.5, iterations=50)
                
                # Edge traces
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
                    line=dict(width=0.8, color='#888'),
                    hoverinfo='none',
                    mode='lines'
                )
                
                # Node traces
                node_x, node_y = [], []
                node_text, node_color, node_size = [], [], []
                
                color_map = {
                    'PERSON': '#FF6B6B',
                    'PHONE': '#4ECDC4', 
                    'ACCOUNT': '#45B7D1',
                    'VEHICLE': '#96CEB4',
                    'LOCATION': '#FFEAA7',
                    'CASE': '#FF9FF3',
                    'UNKNOWN': '#888888'
                }
                
                for node in node_list:
                    try:
                        x, y = pos[node]
                        node_x.append(x)
                        node_y.append(y)
                        attrs = get_node_attributes(G, node)
                        node_type = attrs.get('type', 'UNKNOWN')
                        degree = get_degree(G, node)
                        node_text.append(f"{node}<br>Type: {node_type}<br>Degree: {degree}")
                        node_color.append(color_map.get(node_type, '#888888'))
                        node_size.append(10 + degree * 2)
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
                        line=dict(width=1, color='#fff')
                    )
                )
                
                fig = go.Figure(
                    data=[edge_trace, node_trace],
                    layout=go.Layout(
                        title='Criminal Network Graph',
                        hovermode='closest',
                        showlegend=False,
                        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                        plot_bgcolor='#f8f9fa',
                        height=600
                    )
                )
                
                st.plotly_chart(fig, use_container_width=True)
            except Exception as e:
                st.error(f"Error rendering graph: {str(e)}")
                _show_fallback_network(G, node_list)
        else:
            st.warning("Showing network data view.")
            _show_fallback_network(G, node_list)
        
        # Entity selector - FIXED: Using node_list directly
        st.markdown("---")
        col1, col2 = st.columns([2, 1])
        with col1:
            if node_list:
                selected = st.selectbox("🔍 Select Entity to Investigate", node_list)
            else:
                selected = None
                st.warning("No entities in network")
        with col2:
            if selected and st.button("View Profile", use_container_width=True):
                st.session_state.selected_entity = selected
                st.session_state.current_page = "Entity Profile"
                st.rerun()

    # ========================================================================
    # ENTITY PROFILE
    # ========================================================================
    elif selected_page == "Entity Profile":
        st.markdown('<h1 class="main-title">👤 Entity Intelligence</h1>', unsafe_allow_html=True)
        
        # FIXED: Using node_list directly
        if not node_list:
            st.warning("No entities in the network. Please generate data first.")
        else:
            if st.session_state.selected_entity and st.session_state.selected_entity in node_list:
                entity_id = st.session_state.selected_entity
            else:
                entity_id = st.selectbox("Search Entity", node_list)
                st.session_state.selected_entity = entity_id
            
            if entity_id and entity_id in node_list:
                details = get_entity_details(G, entity_id)
                
                if details:
                    col1, col2 = st.columns([2, 1])
                    
                    with col1:
                        st.subheader(f"📋 Entity: {entity_id}")
                        attrs = get_node_attributes(G, entity_id)
                        entity_type = attrs.get('type', 'UNKNOWN')
                        st.markdown(f"**Type:** {entity_type}")
                        
                        # Priority badge
                        if details.get('priority') == 'HIGH':
                            st.markdown(f'<span class="status-badge status-high">🔴 {details["priority"]} PRIORITY</span>', unsafe_allow_html=True)
                        elif details.get('priority') == 'MEDIUM':
                            st.markdown(f'<span class="status-badge status-medium">🟡 {details["priority"]} PRIORITY</span>', unsafe_allow_html=True)
                        else:
                            st.markdown(f'<span class="status-badge status-low">🟢 {details["priority"]} PRIORITY</span>', unsafe_allow_html=True)
                        
                        st.markdown(f"**Priority Score:** {details['priority_score']:.1%}")
                        
                        st.markdown("---")
                        
                        st.subheader("📊 Properties")
                        for key, value in attrs.items():
                            st.markdown(f"**{key}:** {value}")
                        
                        st.markdown("---")
                        
                        st.subheader(f"🔗 Connections ({len(details['connections'])})")
                        for conn in details['connections'][:10]:
                            st.markdown(f"**→ {conn['entity_id']}**")
                            st.caption(f"Relation: {conn['relation']}")
                            st.markdown("---")
                    
                    with col2:
                        st.subheader("📊 Quick Stats")
                        st.metric("Direct Connections", len(details['connections']))
                        st.metric("Network Degree", get_degree(G, entity_id))
                        
                        st.markdown("---")
                        
                        st.subheader("🎯 Recommendations")
                        degree = len(details['connections'])
                        if degree >= 5:
                            st.warning("🔴 Immediate investigation required")
                            st.markdown("- Assign to senior investigator")
                            st.markdown("- Conduct surveillance")
                            st.markdown("- Coordinate with other cases")
                        elif degree >= 3:
                            st.info("🟡 Schedule within 48 hours")
                            st.markdown("- Gather additional evidence")
                            st.markdown("- Interview connected persons")
                        else:
                            st.success("🟢 Low priority")
                            st.markdown("- Monitor for new connections")
                            st.markdown("- Document findings")
                else:
                    st.warning(f"Could not find details for entity {entity_id}")

    # ========================================================================
    # TIMELINE
    # ========================================================================
    elif selected_page == "Timeline":
        st.markdown('<h1 class="main-title">⏱️ Investigation Timeline</h1>', unsafe_allow_html=True)
        
        st.info("📈 Timeline view showing network evolution over time")
        
        # Generate sample timeline data
        dates = pd.date_range(start=datetime.now() - timedelta(days=180), end=datetime.now(), periods=20)
        entities = np.cumsum(np.random.randint(1, 4, size=len(dates)))
        relationships = np.cumsum(np.random.randint(1, 6, size=len(dates)))
        
        timeline_df = pd.DataFrame({
            'Date': dates,
            'Entities': entities,
            'Relationships': relationships
        })
        
        if PLOTLY_AVAILABLE:
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
                plot_bgcolor='#f8f9fa',
                height=500
            )
            
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.dataframe(timeline_df, use_container_width=True)
        
        st.subheader("📌 Key Events")
        events = [
            {"date": dates[4], "event": "First cross-case connection discovered"},
            {"date": dates[8], "event": "Network expansion detected"},
            {"date": dates[12], "event": "Priority lead identified"},
            {"date": dates[16], "event": "Evidence breakthrough found"}
        ]
        
        for event in events:
            col1, col2 = st.columns([1, 4])
            with col1:
                st.caption(event["date"].strftime("%Y-%m-%d"))
            with col2:
                st.markdown(f"🔹 {event['event']}")

    # ========================================================================
    # CROSS-CASE
    # ========================================================================
    elif selected_page == "Cross-Case":
        st.markdown('<h1 class="main-title">🔗 Cross-Case Connection Discovery</h1>', unsafe_allow_html=True)
        
        st.info("🔍 Discovering connections between cases...")
        
        # Find cross-case connections
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
                    with st.expander(f"🔗 {conn['case1']} ↔ {conn['case2']}"):
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("Shared Entities", conn['shared_entities'])
                        with col2:
                            st.metric("Confidence", f"{conn['confidence']:.0%}")
                        with col3:
                            st.metric("Connections", conn['shared_entities'] * 2)
                        
                        if conn['shared_persons']:
                            st.write("**Shared Persons:**")
                            for person in conn['shared_persons']:
                                attrs = get_node_attributes(G, person)
                                name = attrs.get('name', person)
                                st.markdown(f"- {person} ({name})")
                        
                        st.progress(conn['confidence'])
            else:
                st.info("No cross-case connections found in the current network.")
        else:
            st.warning("Need at least 2 cases and 1 person to find cross-case connections.")

    # ========================================================================
    # AI ASSISTANT
    # ========================================================================
    elif selected_page == "AI Assistant":
        st.markdown('<h1 class="main-title">🤖 AI Investigation Copilot</h1>', unsafe_allow_html=True)
        
        st.info("💡 Ask questions about your investigation or get AI-generated insights")
        
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("💬 Quick Questions")
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
            st.subheader("🔍 Custom Query")
            user_query = st.text_area(
                "Ask your question",
                placeholder="Example: What are the connections between Entity A and Entity B?",
                height=150
            )
            
            if st.button("🔍 Analyze", use_container_width=True):
                st.session_state.ai_query = user_query
        
        # Process AI query
        if hasattr(st.session_state, 'ai_query') and st.session_state.ai_query:
            query = st.session_state.ai_query
            
            st.markdown("---")
            st.markdown("### 🤖 AI Response")
            
            with st.spinner("Analyzing network..."):
                response = f"""
                ## Investigation Brief
                
                ### Query Analysis
                I've analyzed your query about **{query[:50]}...**
                
                ### Key Findings
                1. **Network Overview**: The network contains {len(node_list)} entities
                2. **Key Connections**: Multiple relationships discovered
                3. **Priority Entities**: {len([n for n in node_list if get_degree(G, n) >= 3])} entities have high connectivity
                
                ### Actionable Insights
                - 🎯 **Focus Areas**: Investigate entities with high connectivity first
                - 🔗 **Hidden Connections**: Look for indirect paths between key persons
                - 📊 **Pattern Detection**: Financial and communication patterns are most revealing
                
                ### Next Steps
                1. Review priority entities in the Dashboard
                2. Explore connections in the Network Graph
                3. Check cross-case connections for broader patterns
                """
                
                st.markdown(response)
                
                # Show relevant entities
                st.subheader("📋 Relevant Entities")
                entities_with_degree = []
                for node in node_list:
                    attrs = get_node_attributes(G, node)
                    if attrs.get('type') == 'PERSON':
                        degree = get_degree(G, node)
                        entities_with_degree.append((node, degree))
                
                entities_with_degree.sort(key=lambda x: x[1], reverse=True)
                for node, degree in entities_with_degree[:5]:
                    attrs = get_node_attributes(G, node)
                    name = attrs.get('name', node)
                    st.markdown(f"- **{node}** ({name}) - Degree: {degree}")
                
                st.warning("⚠️ This is an AI-generated analysis. All findings should be verified by human investigators.")
                
                st.session_state.ai_query = None

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def _show_fallback_network(G, node_list):
    """Show network data in table format when plotly is not available"""
    st.subheader("📋 Network Data")
    
    # Show nodes
    st.write("**Entities:**")
    node_data = []
    for node in node_list:
        attrs = get_node_attributes(G, node)
        node_data.append({
            'ID': node,
            'Type': attrs.get('type', 'UNKNOWN'),
            'Degree': get_degree(G, node)
        })
    st.dataframe(pd.DataFrame(node_data), use_container_width=True)
    
    # Show edges
    st.write("**Relationships:**")
    edge_data = []
    for u in node_list:
        for v in get_neighbors(G, u):
            if (u, v) not in [(e['Source'], e['Target']) for e in edge_data]:
                edge_data.append({
                    'Source': u,
                    'Target': v,
                    'Type': get_edge_data(G, u, v).get('type', 'CONNECTED')
                })
    if edge_data:
        st.dataframe(pd.DataFrame(edge_data), use_container_width=True)

# ============================================================================
# FOOTER
# ============================================================================

st.markdown("---")
st.caption("🕵️ SUTRA-X v1.0.0 | Smart Unified Threat & Relationship Analytics | Powered by AI")

# ============================================================================
# RUN THE APP
# ============================================================================

if __name__ == "__main__":
    pass
