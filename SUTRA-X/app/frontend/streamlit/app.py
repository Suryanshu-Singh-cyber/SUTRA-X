"""
SUTRA-X: Smart Unified Threat & Relationship Analytics
AI-Powered Criminal Network Investigation & Intelligence Platform
"""

import streamlit as st
import pandas as pd
import numpy as np
import networkx as nx
from datetime import datetime, timedelta
import random
import json
from pathlib import Path
import sys

# Add project root to path
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))

# Try importing plotly with error handling
try:
    import plotly.graph_objects as go
    import plotly.express as px
    PLOTLY_AVAILABLE = True
except ImportError as e:
    PLOTLY_AVAILABLE = False
    st.warning(f"⚠️ Plotly not available: {e}. Using fallback visualizations.")

# Page configuration
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
    .entity-card {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
        border-left: 4px solid #667eea;
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

# Session state initialization
if 'data_loaded' not in st.session_state:
    st.session_state.data_loaded = False
if 'graph' not in st.session_state:
    st.session_state.graph = None
if 'data_frames' not in st.session_state:
    st.session_state.data_frames = None
if 'selected_entity' not in st.session_state:
    st.session_state.selected_entity = None
if 'current_page' not in st.session_state:
    st.session_state.current_page = "Dashboard"
if 'sample_data_generated' not in st.session_state:
    st.session_state.sample_data_generated = False

# ============================================================================
# DATA GENERATION FUNCTIONS
# ============================================================================

def generate_sample_network():
    """Generate a sample criminal network with realistic data"""
    
    # Create graph
    G = nx.Graph()
    
    # Define entity types and their colors
    entity_types = {
        'PERSON': {'color': '#FF6B6B', 'size': 30},
        'PHONE': {'color': '#4ECDC4', 'size': 20},
        'ACCOUNT': {'color': '#45B7D1', 'size': 25},
        'VEHICLE': {'color': '#96CEB4', 'size': 22},
        'LOCATION': {'color': '#FFEAA7', 'size': 28},
        'CASE': {'color': '#FF9FF3', 'size': 35}
    }
    
    # Generate persons (Indian names)
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
        # Connect to random person
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
        # Connect case to some persons
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
    
    # Create some cross-case connections (bridges)
    # Make some persons involved in multiple cases
    for _ in range(8):
        person = random.choice(persons)
        case = random.choice(cases)
        if not G.has_edge(person, case):
            G.add_edge(person, case, type='INVOLVED', confidence=0.5 + random.random()*0.4)
    
    # Add some hidden connections (for discovery)
    hidden_connections = [
        ('P-0001', 'P-0012'),
        ('PH-0005', 'PH-0015'),
        ('ACC-0003', 'ACC-0010'),
    ]
    for src, tgt in hidden_connections:
        if src in G.nodes and tgt in G.nodes and not G.has_edge(src, tgt):
            G.add_edge(src, tgt, type='HIDDEN_CONNECTION', confidence=0.6, hidden=True)
    
    return G

# ============================================================================
# ANALYZER FUNCTIONS
# ============================================================================

def analyze_network(G):
    """Analyze the network and return metrics"""
    
    if G is None or len(G.nodes) == 0:
        return None
    
    metrics = {
        'total_nodes': len(G.nodes),
        'total_edges': len(G.edges),
        'node_types': {},
        'central_entities': [],
        'communities': [],
        'bridges': []
    }
    
    # Count node types
    for node, data in G.nodes(data=True):
        node_type = data.get('type', 'UNKNOWN')
        metrics['node_types'][node_type] = metrics['node_types'].get(node_type, 0) + 1
    
    # Calculate centrality (for connected components)
    if len(G.nodes) > 1:
        try:
            # Get largest connected component
            components = list(nx.connected_components(G))
            if components:
                largest = G.subgraph(max(components, key=len))
                if len(largest.nodes) > 2:
                    centrality = nx.degree_centrality(largest)
                    top_entities = sorted(centrality.items(), key=lambda x: x[1], reverse=True)[:5]
                    metrics['central_entities'] = [(node, round(score, 3)) for node, score in top_entities]
        except:
            pass
    
    # Find bridges (critical connections)
    try:
        if len(G.nodes) > 2:
            bridges = list(nx.bridges(G))
            metrics['bridges'] = bridges[:5]
    except:
        pass
    
    return metrics

def get_entity_details(G, entity_id):
    """Get detailed information about an entity"""
    
    if entity_id not in G.nodes:
        return None
    
    details = {
        'id': entity_id,
        'properties': dict(G.nodes[entity_id]),
        'connections': [],
        'priority_score': random.uniform(0.3, 0.9),
        'evidence': []
    }
    
    # Get connections
    for neighbor in G.neighbors(entity_id):
        edge_data = G.get_edge_data(entity_id, neighbor)
        details['connections'].append({
            'entity_id': neighbor,
            'relation': edge_data.get('type', 'CONNECTED'),
            'properties': edge_data
        })
    
    # Generate evidence (sample)
    evidence_types = ['CDR Analysis', 'Financial Records', 'Location Tracking', 
                     'Witness Statements', 'Surveillance Reports', 'Call Records']
    for _ in range(min(3, len(details['connections']))):
        details['evidence'].append({
            'type': random.choice(evidence_types),
            'description': f'Evidence linking {entity_id} to connections',
            'source': random.choice(['Field Report', 'Digital Forensics', 'Financial Audit']),
            'confidence': random.uniform(0.5, 0.95)
        })
    
    # Calculate priority
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
# MAIN APPLICATION
# ============================================================================

# Sidebar
with st.sidebar:
    col1, col2 = st.columns([1, 3])
    with col1:
        st.markdown("🕵️")
    with col2:
        st.title("SUTRA-X")
    st.caption("v1.0.0 | AI-Powered Investigation")
    
    st.markdown("---")
    
    # Language selector
    language = st.selectbox(
        "🌐 Language",
        ["English", "हिंदी", "தமிழ்", "తెలుగు", "বাংলা"]
    )
    
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
            st.success(f"✅ Generated network with {len(G.nodes)} entities and {len(G.edges)} relationships")
            st.rerun()
    
    st.markdown("---")
    
    # Upload section
    st.subheader("📂 Upload Data")
    uploaded_files = st.file_uploader(
        "Upload CSV files",
        type=['csv'],
        accept_multiple_files=True
    )
    
    if uploaded_files and st.button("📥 Process Uploaded Data", use_container_width=True):
        st.warning("CSV upload functionality is being implemented. Use 'Generate Sample Data' for demo.")

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
    
    with st.expander("🎯 How SUTRA-X Works", expanded=True):
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
    
    # ========================================================================
    # PAGE: Dashboard
    # ========================================================================
    if selected_page == "Dashboard":
        st.markdown('<h1 class="main-title">📊 Command Center</h1>', unsafe_allow_html=True)
        
        # Analyze network
        metrics = analyze_network(G)
        
        # Metrics row
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Entities", len(G.nodes()))
        with col2:
            st.metric("Relationships", len(G.edges()))
        with col3:
            # Count high-priority entities
            high_priority = 0
            for node in G.nodes():
                degree = G.degree(node)
                if degree >= 4:
                    high_priority += 1
            st.metric("High Priority Leads", high_priority, delta="🚨 Immediate")
        with col4:
            # Count cross-case connections
            cross_case = 0
            for node in G.nodes():
                if G.nodes[node].get('type') == 'PERSON':
                    case_connections = sum(1 for n in G.neighbors(node) if G.nodes[n].get('type') == 'CASE')
                    if case_connections >= 2:
                        cross_case += 1
            st.metric("Cross-Case Links", cross_case, delta="🔗 Connections")
        
        st.markdown("---")
        
        # Priority Leads
        st.subheader("🚨 Priority Investigation Leads")
        
        # Find entities with high degree
        priority_entities = []
        for node in G.nodes():
            degree = G.degree(node)
            node_type = G.nodes[node].get('type', 'UNKNOWN')
            if node_type != 'CASE' and degree >= 2:
                priority_entities.append({
                    'id': node,
                    'degree': degree,
                    'type': node_type,
                    'name': G.nodes[node].get('name', G.nodes[node].get('number', node)),
                    'score': min(100, degree * 15 + random.randint(0, 20))
                })
        
        # Sort by degree
        priority_entities.sort(key=lambda x: x['degree'], reverse=True)
        
        if priority_entities:
            for entity in priority_entities[:5]:
                col1, col2, col3, col4 = st.columns([2, 2, 1, 1])
                with col1:
                    st.markdown(f"**🔍 {entity['id']}**")
                    st.caption(f"Type: {entity['type']} | {entity['name']}")
                with col2:
                    st.caption(f"Connections: {entity['degree']}")
                with col3:
                    score_color = "🟢" if entity['score'] < 50 else "🟡" if entity['score'] < 70 else "🔴"
                    st.caption(f"Priority: {score_color} {entity['score']:.0f}%")
                with col4:
                    if st.button("View", key=f"view_dash_{entity['id']}"):
                        st.session_state.selected_entity = entity['id']
                        st.session_state.current_page = "Entity Profile"
                        st.rerun()
                
                st.markdown("---")
        else:
            st.info("No priority leads found. Generate more data or upload case files.")
        
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
            st.subheader("🔗 Key Connections")
            if metrics and metrics.get('bridges'):
                for bridge in metrics['bridges'][:3]:
                    st.markdown(f"- **{bridge[0]}** ↔ **{bridge[1]}** (Critical Connection)")
            else:
                st.info("No critical bridges detected in the network.")
    
    # ========================================================================
    # PAGE: Network Graph
    # ========================================================================
    elif selected_page == "Network Graph":
        st.markdown('<h1 class="main-title">🌐 Network Graph</h1>', unsafe_allow_html=True)
        
        if PLOTLY_AVAILABLE:
            # Interactive graph with plotly
            st.info("🌐 Interactive network visualization. Click nodes for details.")
            
            # Prepare graph data
            try:
                # Use spring layout for visualization
                if len(G.nodes) > 1:
                    pos = nx.spring_layout(G, k=0.5, iterations=50)
                    
                    # Create edge traces
                    edge_x, edge_y, edge_text = [], [], []
                    for edge in G.edges():
                        try:
                            x0, y0 = pos[edge[0]]
                            x1, y1 = pos[edge[1]]
                            edge_x.extend([x0, x1, None])
                            edge_y.extend([y0, y1, None])
                            edge_text.append(f"{edge[0]} → {edge[1]}")
                        except:
                            continue
                    
                    edge_trace = go.Scatter(
                        x=edge_x, y=edge_y,
                        line=dict(width=0.8, color='#888'),
                        hoverinfo='none',
                        mode='lines'
                    )
                    
                    # Create node traces
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
                    
                    for node in G.nodes():
                        try:
                            x, y = pos[node]
                            node_x.append(x)
                            node_y.append(y)
                            node_type = G.nodes[node].get('type', 'UNKNOWN')
                            node_text.append(f"{node}<br>Type: {node_type}<br>Degree: {G.degree(node)}")
                            node_color.append(color_map.get(node_type, '#888888'))
                            node_size.append(10 + G.degree(node) * 2)
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
                            height=600,
                            clickmode='event+select'
                        )
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.warning("Graph has too few nodes for visualization.")
            except Exception as e:
                st.error(f"Error rendering graph: {str(e)}")
                st.info("Showing fallback graph view...")
                
                # Fallback: Simple node list
                st.subheader("📋 Network Nodes")
                node_data = []
                for node in G.nodes():
                    node_data.append({
                        'ID': node,
                        'Type': G.nodes[node].get('type', 'UNKNOWN'),
                        'Properties': str(G.nodes[node])[:100] + '...' if len(str(G.nodes[node])) > 100 else str(G.nodes[node])
                    })
                st.dataframe(pd.DataFrame(node_data), use_container_width=True)
        else:
            # Fallback without plotly
            st.warning("Plotly not available. Showing network data as tables.")
            
            st.subheader("📊 Network Overview")
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Total Nodes", len(G.nodes()))
            with col2:
                st.metric("Total Edges", len(G.edges()))
            
            st.subheader("📋 Entity List")
            entity_data = []
            for node in G.nodes():
                entity_data.append({
                    'ID': node,
                    'Type': G.nodes[node].get('type', 'UNKNOWN'),
                    'Degree': G.degree(node)
                })
            st.dataframe(pd.DataFrame(entity_data), use_container_width=True)
        
        # Entity selector
        st.markdown("---")
        col1, col2 = st.columns([2, 1])
        with col1:
            selected = st.selectbox("🔍 Select Entity to Investigate", list(G.nodes()))
        with col2:
            if st.button("View Profile", use_container_width=True):
                st.session_state.selected_entity = selected
                st.session_state.current_page = "Entity Profile"
                st.rerun()
    
    # ========================================================================
    # PAGE: Entity Profile
    # ========================================================================
    elif selected_page == "Entity Profile":
        st.markdown('<h1 class="main-title">👤 Entity Intelligence</h1>', unsafe_allow_html=True)
        
        if st.session_state.selected_entity and st.session_state.selected_entity in G.nodes:
            entity_id = st.session_state.selected_entity
        else:
            entity_id = st.selectbox("Search Entity", list(G.nodes()))
            st.session_state.selected_entity = entity_id
        
        if entity_id and entity_id in G.nodes:
            details = get_entity_details(G, entity_id)
            
            if details:
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.subheader(f"📋 Entity: {entity_id}")
                    
                    # Entity type badge
                    entity_type = G.nodes[entity_id].get('type', 'UNKNOWN')
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
                    
                    # Properties
                    st.subheader("📊 Properties")
                    for key, value in G.nodes[entity_id].items():
                        st.markdown(f"**{key}:** {value}")
                    
                    st.markdown("---")
                    
                    # Connections
                    st.subheader(f"🔗 Connections ({len(details['connections'])})")
                    for conn in details['connections'][:10]:
                        with st.container():
                            st.markdown(f"**→ {conn['entity_id']}**")
                            st.caption(f"Relation: {conn['relation']}")
                            if conn.get('properties'):
                                st.json(conn['properties'])
                            st.markdown("---")
                
                with col2:
                    st.subheader("📊 Quick Stats")
                    st.metric("Direct Connections", len(details['connections']))
                    st.metric("Network Degree", G.degree(entity_id))
                    
                    st.markdown("---")
                    
                    # Evidence
                    st.subheader("📄 Evidence")
                    if details.get('evidence'):
                        for ev in details['evidence']:
                            st.markdown(f"**{ev['type']}**")
                            st.caption(ev['description'])
                            st.caption(f"Source: {ev['source']} | Confidence: {ev['confidence']:.0%}")
                            st.markdown("---")
                    else:
                        st.info("No evidence available")
                    
                    st.markdown("---")
                    
                    # Recommendations
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
        else:
            st.warning("Please select an entity to investigate")
    
    # ========================================================================
    # PAGE: Timeline
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
        
        # Key events
        st.subheader("📌 Key Events")
        events = [
            {"date": dates[4], "event": "First cross-case connection discovered"},
            {"date": dates[8], "event": "Network expansion detected - 3 new entities"},
            {"date": dates[12], "event": "Priority lead identified in Case #27"},
            {"date": dates[16], "event": "Evidence breakthrough - financial pattern found"}
        ]
        
        for event in events:
            col1, col2 = st.columns([1, 4])
            with col1:
                st.caption(event["date"].strftime("%Y-%m-%d"))
            with col2:
                st.markdown(f"🔹 {event['event']}")
    
    # ========================================================================
    # PAGE: Cross-Case
    # ========================================================================
    elif selected_page == "Cross-Case":
        st.markdown('<h1 class="main-title">🔗 Cross-Case Connection Discovery</h1>', unsafe_allow_html=True)
        
        st.info("🔍 Discovering connections between cases...")
        
        # Find cross-case connections
        case_nodes = [n for n in G.nodes() if G.nodes[n].get('type') == 'CASE']
        person_nodes = [n for n in G.nodes() if G.nodes[n].get('type') == 'PERSON']
        
        if len(case_nodes) >= 2:
            cross_connections = []
            for i, case1 in enumerate(case_nodes):
                for case2 in case_nodes[i+1:]:
                    # Find shared persons
                    persons1 = [n for n in G.neighbors(case1) if n in person_nodes]
                    persons2 = [n for n in G.neighbors(case2) if n in person_nodes]
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
                                st.markdown(f"- {person} ({G.nodes[person].get('name', person)})")
                        
                        st.progress(conn['confidence'])
            else:
                st.info("No cross-case connections found in the current network.")
        else:
            st.warning("Need at least 2 cases to find cross-case connections.")
        
        # Network visualization of cross-case connections
        if PLOTLY_AVAILABLE and len(case_nodes) >= 2:
            st.markdown("---")
            st.subheader("📊 Cross-Case Network Map")
            
            # Create a simpler graph for visualization
            cross_graph = nx.Graph()
            for case in case_nodes:
                cross_graph.add_node(case, type='CASE')
                for person in G.neighbors(case):
                    if person in person_nodes:
                        cross_graph.add_node(person, type='PERSON')
                        cross_graph.add_edge(case, person)
            
            if len(cross_graph.nodes) > 2:
                try:
                    pos = nx.spring_layout(cross_graph)
                    edge_x, edge_y = [], []
                    for edge in cross_graph.edges():
                        x0, y0 = pos[edge[0]]
                        x1, y1 = pos[edge[1]]
                        edge_x.extend([x0, x1, None])
                        edge_y.extend([y0, y1, None])
                    
                    edge_trace = go.Scatter(
                        x=edge_x, y=edge_y,
                        line=dict(width=1, color='#888'),
                        hoverinfo='none',
                        mode='lines'
                    )
                    
                    node_x, node_y, node_text, node_color = [], [], [], []
                    for node in cross_graph.nodes():
                        x, y = pos[node]
                        node_x.append(x)
                        node_y.append(y)
                        node_type = cross_graph.nodes[node].get('type', 'UNKNOWN')
                        node_text.append(f"{node}<br>Type: {node_type}")
                        node_color.append('#FF9FF3' if node_type == 'CASE' else '#FF6B6B')
                    
                    node_trace = go.Scatter(
                        x=node_x, y=node_y,
                        mode='markers',
                        hoverinfo='text',
                        text=node_text,
                        marker=dict(
                            size=25 if node_type == 'CASE' else 15,
                            color=node_color,
                            line=dict(width=2, color='#fff')
                        )
                    )
                    
                    fig = go.Figure(
                        data=[edge_trace, node_trace],
                        layout=go.Layout(
                            title='Case-Person Network',
                            hovermode='closest',
                            showlegend=False,
                            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                            plot_bgcolor='#f8f9fa',
                            height=400
                        )
                    )
                    st.plotly_chart(fig, use_container_width=True)
                except:
                    st.info("Could not render cross-case network visualization.")
    
    # ========================================================================
    # PAGE: AI Assistant
    # ========================================================================
    elif selected_page == "AI Assistant":
        st.markdown('<h1 class="main-title">🤖 AI Investigation Copilot</h1>', unsafe_allow_html=True)
        
        st.info("💡 Ask questions about your investigation or get AI-generated insights")
        
        # Sample questions
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("💬 Quick Questions")
            questions = [
                "Who are the most central people in this network?",
                "Show me connections between Case-001 and Case-002",
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
                placeholder="Example: What are the strongest connections between Entity A and Case 17?",
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
                # Simple analysis based on query
                response = f"""
                ## Investigation Brief
                
                ### Query Analysis
                I've analyzed your query about **{query[:50]}...**
                
                ### Key Findings
                1. **Network Overview**: The current network contains {len(G.nodes())} entities and {len(G.edges())} relationships
                2. **Key Connections**: Multiple relationships discovered across different entity types
                3. **Priority Entities**: {len([n for n in G.nodes() if G.degree(n) >= 3])} entities have high connectivity
                
                ### Actionable Insights
                - 🎯 **Focus Areas**: Investigate entities with degree > 3 first
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
                relevant = sorted([(n, G.degree(n)) for n in G.nodes() if G.nodes[n].get('type') == 'PERSON'], 
                                 key=lambda x: x[1], reverse=True)[:5]
                for node, degree in relevant:
                    st.markdown(f"- **{node}** (Degree: {degree})")
                
                st.warning("⚠️ This is an AI-generated analysis. All findings should be verified by human investigators.")
                
                # Clear query after processing
                st.session_state.ai_query = None

# Footer
st.markdown("---")
st.caption("🕵️ SUTRA-X v1.0.0 | Smart Unified Threat & Relationship Analytics | Powered by AI")

# ============================================================================
# RUN THE APP
# ============================================================================
if __name__ == "__main__":
    # This is handled by Streamlit
    pass
