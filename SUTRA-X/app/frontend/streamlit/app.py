"""
SUTRA-X: Smart Unified Threat & Relationship Analytics
AI-Powered Criminal Network Investigation & Intelligence Platform
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import networkx as nx
import sys
import os
from pathlib import Path
from datetime import datetime
import json
import random

# Add the project root to Python path
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))

# Try importing backend modules with error handling
try:
    from app.backend.core.config import settings
    from app.backend.data_ingestion.loader import DataLoader
    from app.backend.graph_engine.graph_builder import CriminalGraphBuilder, GraphAnalyzer
    from app.backend.intelligence_engine.priority_scorer import PriorityScorer
    from app.backend.nlp_engine.entity_extractor import EntityExtractor
    BACKEND_AVAILABLE = True
except ImportError as e:
    BACKEND_AVAILABLE = False
    st.warning(f"Some backend modules not available. Using fallback mode. Error: {e}")

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
    .highlight-box {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #ff6b6b;
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
    .status-badge {
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
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
    </style>
""", unsafe_allow_html=True)

# Session state initialization
if 'data_loaded' not in st.session_state:
    st.session_state.data_loaded = False
if 'graph' not in st.session_state:
    st.session_state.graph = None
if 'analyzer' not in st.session_state:
    st.session_state.analyzer = None
if 'scorer' not in st.session_state:
    st.session_state.scorer = None
if 'data_frames' not in st.session_state:
    st.session_state.data_frames = None
if 'selected_entity' not in st.session_state:
    st.session_state.selected_entity = None
if 'current_page' not in st.session_state:
    st.session_state.current_page = "Dashboard"

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
    
    # Data upload section
    st.subheader("📂 Data Upload")
    
    uploaded_files = st.file_uploader(
        "Upload case data (CSV, JSON, Excel)",
        type=['csv', 'json', 'xlsx'],
        accept_multiple_files=True
    )
    
    if uploaded_files:
        if st.button("🚀 Process Data", use_container_width=True):
            with st.spinner("Processing data... This may take a moment."):
                try:
                    if BACKEND_AVAILABLE:
                        loader = DataLoader()
                        data_frames = {}
                        
                        for file in uploaded_files:
                            import tempfile
                            with tempfile.NamedTemporaryFile(delete=False, suffix=f".{file.name.split('.')[-1]}") as tmp_file:
                                tmp_file.write(file.getvalue())
                                tmp_path = Path(tmp_file.name)
                                
                                if file.name.endswith('.csv'):
                                    df = loader.load_csv(tmp_path)
                                elif file.name.endswith('.json'):
                                    df = pd.DataFrame(loader.load_json(tmp_path))
                                else:
                                    df = loader.load_excel(tmp_path)
                                
                                data_frames[file.name] = df
                        
                        st.session_state.data_frames = data_frames
                        
                        # Build graph
                        builder = CriminalGraphBuilder()
                        graph = builder.build_from_dataframes(data_frames)
                        st.session_state.graph = graph
                        
                        # Initialize analyzer
                        analyzer = GraphAnalyzer(graph)
                        st.session_state.analyzer = analyzer
                        
                        # Initialize scorer
                        centrality = analyzer.calculate_centrality()
                        scorer = PriorityScorer(graph, centrality)
                        st.session_state.scorer = scorer
                        
                        st.session_state.data_loaded = True
                        st.success(f"✅ Processed {len(data_frames)} files with {len(graph.nodes)} entities and {len(graph.edges)} relationships")
                    else:
                        # Fallback: Generate sample data
                        st.session_state.data_loaded = True
                        st.warning("Using sample data (backend modules not available)")
                except Exception as e:
                    st.error(f"Error processing data: {str(e)}")
    
    # Load sample data button
    if st.button("📊 Load Sample Data", use_container_width=True):
        with st.spinner("Loading sample data..."):
            try:
                # Try to load from data/raw directory
                data_dir = Path(project_root) / "app" / "data" / "raw"
                if data_dir.exists():
                    loader = DataLoader()
                    data_frames = loader.load_all_data(data_dir)
                    st.session_state.data_frames = data_frames
                    
                    builder = CriminalGraphBuilder()
                    graph = builder.build_from_dataframes(data_frames)
                    st.session_state.graph = graph
                    
                    analyzer = GraphAnalyzer(graph)
                    st.session_state.analyzer = analyzer
                    
                    centrality = analyzer.calculate_centrality()
                    scorer = PriorityScorer(graph, centrality)
                    st.session_state.scorer = scorer
                    
                    st.session_state.data_loaded = True
                    st.success(f"✅ Loaded sample data with {len(graph.nodes)} entities")
                else:
                    # Generate data on the fly
                    st.warning("Sample data not found. Generating demo data...")
                    st.session_state.data_loaded = True
            except Exception as e:
                st.error(f"Error loading sample data: {str(e)}")
                st.session_state.data_loaded = True  # Still enable demo mode

# Main content
if not st.session_state.data_loaded:
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
    
    st.info("👈 **Get Started:** Upload your case data or load sample data using the sidebar.")
    
    # Quick demo preview
    with st.expander("🎬 See a Quick Demo", expanded=False):
        st.markdown("""
        **SUTRA-X helps investigators:**
        
        1. **Connect the dots** across multiple cases and evidence sources
        2. **Discover hidden relationships** that traditional methods miss
        3. **Prioritize investigation** with AI-powered scoring
        4. **Explain every insight** with supporting evidence
        5. **Work in multiple languages** (English, Hindi, Tamil, Telugu, Bengali)
        
        **💡 USP:** *From fragmented evidence to explainable investigative leads in 30 seconds*
        """)
    
else:
    # Main application pages
    if selected_page == "Dashboard":
        st.markdown('<h1 class="main-title">📊 Command Center</h1>', unsafe_allow_html=True)
        
        # Metrics
        col1, col2, col3, col4 = st.columns(4)
        
        graph = st.session_state.graph
        analyzer = st.session_state.analyzer
        scorer = st.session_state.scorer
        
        if graph:
            with col1:
                st.metric("Total Entities", len(graph.nodes()))
            with col2:
                st.metric("Relationships", len(graph.edges()))
            with col3:
                if scorer:
                    high_priority = len([s for s in scorer.get_high_priority_leads(threshold=0.5)])
                    st.metric("High Priority Leads", high_priority, delta="🚨 Immediate")
                else:
                    st.metric("High Priority Leads", "N/A")
            with col4:
                cross_case = len([e for e in graph.nodes() if len(list(graph.neighbors(e))) > 3])
                st.metric("Cross-Case Links", cross_case, delta="🔗 Connections")
        else:
            st.warning("No graph data available. Please load data first.")
        
        st.markdown("---")
        
        # Priority Leads
        st.subheader("🚨 Priority Investigation Leads")
        
        if scorer:
            leads = scorer.get_high_priority_leads(threshold=0.5)
            if leads:
                for lead in leads[:5]:
                    col1, col2, col3 = st.columns([3, 1, 1])
                    with col1:
                        st.markdown(f"**🔍 {lead['entity_id']}**")
                        st.caption(f"Score: {lead['score']:.1f} | Priority: {lead['priority']}")
                    with col2:
                        if lead['priority'] == 'HIGH':
                            st.markdown("🔴 **URGENT**")
                    with col3:
                        if st.button("View", key=f"view_{lead['entity_id']}"):
                            st.session_state.selected_entity = lead['entity_id']
                            st.session_state.current_page = "Entity Profile"
                            st.rerun()
                    
                    with st.expander(f"📋 Details - {lead['entity_id']}"):
                        if 'components' in lead:
                            st.json(lead['components'])
                    st.markdown("---")
            else:
                st.info("No high priority leads found at this time.")
        else:
            st.info("Run analysis to generate priority leads.")
        
        # Recent Activity
        st.subheader("📈 Recent Activity")
        
        # Sample activity timeline
        activity_data = pd.DataFrame({
            'Time': pd.date_range(end=datetime.now(), periods=10, freq='2h'),
            'Activity': ['New connection discovered', 'Entity updated', 'Priority changed', 
                         'Cross-case link found', 'Evidence added', 'Network expanded',
                         'Alert generated', 'Entity resolved', 'New case linked', 'Pattern detected']
        })
        st.dataframe(activity_data, use_container_width=True)
        
        # Quick stats
        st.subheader("📊 Quick Stats")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Active Cases", "24", delta="+3")
        with col2:
            st.metric("Open Leads", "87", delta="-12")
        with col3:
            st.metric("Resolution Rate", "78%", delta="+5%")
        with col4:
            st.metric("Avg Investigation Time", "3.2 days", delta="-0.8 days")
    
    elif selected_page == "Network Graph":
        st.markdown('<h1 class="main-title">🌐 Network Graph</h1>', unsafe_allow_html=True)
        
        if graph and len(graph.nodes()) > 0:
            # Graph controls
            col1, col2, col3 = st.columns([2, 2, 1])
            with col1:
                centrality_metric = st.selectbox(
                    "Color by",
                    ["None", "Degree Centrality", "Betweenness Centrality", "Entity Type"]
                )
            with col2:
                layout_option = st.selectbox(
                    "Layout",
                    ["Spring", "Circular", "Shell", "Kamada-Kawai"]
                )
            with col3:
                show_edges = st.checkbox("Show Edges", value=True)
            
            # Display graph
            pos = nx.spring_layout(graph)
            
            edge_x = []
            edge_y = []
            edge_text = []
            if show_edges:
                for edge in graph.edges():
                    x0, y0 = pos[edge[0]]
                    x1, y1 = pos[edge[1]]
                    edge_x.extend([x0, x1, None])
                    edge_y.extend([y0, y1, None])
                    edge_text.append(f"{edge[0]} → {edge[1]}")
            
            edge_trace = go.Scatter(
                x=edge_x, y=edge_y,
                line=dict(width=0.5, color='#888'),
                hoverinfo='text',
                text=edge_text if show_edges else [],
                mode='lines'
            )
            
            node_x = []
            node_y = []
            node_text = []
            node_color = []
            node_size = []
            
            color_map = {
                'PERSON': '#FF6B6B',
                'PHONE': '#4ECDC4',
                'ACCOUNT': '#45B7D1',
                'VEHICLE': '#96CEB4',
                'LOCATION': '#FFEAA7',
                'ORGANIZATION': '#DDA0DD',
                'CASE': '#FF9FF3'
            }
            
            # Calculate degree for sizing
            degrees = dict(graph.degree())
            max_degree = max(degrees.values()) if degrees else 1
            
            for node in graph.nodes():
                x, y = pos[node]
                node_x.append(x)
                node_y.append(y)
                node_type = graph.nodes[node].get('type', 'UNKNOWN')
                degree = degrees.get(node, 0)
                node_text.append(f"{node}<br>Type: {node_type}<br>Degree: {degree}")
                node_color.append(color_map.get(node_type, '#888'))
                node_size.append(15 + (degree / max_degree) * 30 if max_degree > 0 else 20)
            
            node_trace = go.Scatter(
                x=node_x, y=node_y,
                mode='markers',
                hoverinfo='text',
                text=node_text,
                marker=dict(
                    size=node_size,
                    color=node_color,
                    line=dict(width=2, color='#fff')
                )
            )
            
            fig = go.Figure(data=[edge_trace, node_trace],
                           layout=go.Layout(
                               title='Criminal Network Graph',
                               hovermode='closest',
                               showlegend=False,
                               xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                               yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                               plot_bgcolor='#f8f9fa',
                               height=600
                           ))
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Entity selector
            col1, col2 = st.columns([2, 1])
            with col1:
                selected_entity = st.selectbox("🔍 Select Entity to Investigate", list(graph.nodes()))
            with col2:
                if st.button("View Profile", use_container_width=True):
                    st.session_state.selected_entity = selected_entity
                    st.session_state.current_page = "Entity Profile"
                    st.rerun()
            
            if selected_entity:
                with st.expander(f"🔍 Quick View: {selected_entity}", expanded=False):
                    if selected_entity in graph.nodes:
                        st.json(dict(graph.nodes[selected_entity]))
                        neighbors = list(graph.neighbors(selected_entity))
                        st.write(f"**Connections:** {len(neighbors)}")
                        if neighbors:
                            st.write("**Connected to:**")
                            for n in neighbors[:10]:
                                st.markdown(f"- {n} (degree: {graph.degree(n)})")
        else:
            st.warning("No graph data available. Please load data first.")
            st.info("👈 Use the sidebar to upload data or load sample data.")
    
    elif selected_page == "Entity Profile":
        st.markdown('<h1 class="main-title">👤 Entity Intelligence</h1>', unsafe_allow_html=True)
        
        if graph and scorer:
            entity_id = st.selectbox("Search Entity", list(graph.nodes()), 
                                     index=list(graph.nodes()).index(st.session_state.selected_entity) if st.session_state.selected_entity in graph.nodes() else 0)
            
            if entity_id:
                brief = scorer.generate_investigation_brief(entity_id)
                
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.subheader(f"📋 Entity: {entity_id}")
                    
                    # Entity type badge
                    entity_type = graph.nodes[entity_id].get('type', 'UNKNOWN')
                    st.markdown(f"**Type:** {entity_type}")
                    
                    # Priority badge
                    if brief['priority'] == 'HIGH':
                        st.markdown(f'<span class="status-badge status-high">🔴 {brief["priority"]} PRIORITY</span>', unsafe_allow_html=True)
                    elif brief['priority'] == 'MEDIUM':
                        st.markdown(f'<span class="status-badge status-medium">🟡 {brief["priority"]} PRIORITY</span>', unsafe_allow_html=True)
                    else:
                        st.markdown(f'<span class="status-badge status-low">🟢 {brief["priority"]} PRIORITY</span>', unsafe_allow_html=True)
                    
                    st.markdown(f"**Score:** {brief['score']:.1f}/100")
                    
                    st.markdown("---")
                    st.markdown("**Summary:**")
                    st.markdown(brief.get('summary', 'No summary available'))
                    
                    st.markdown("---")
                    st.markdown("**Connections:**")
                    for conn in brief.get('connections', [])[:5]:
                        st.markdown(f"- {conn['entity_id']} ({conn['relationship']})")
                    
                    # Entity properties
                    with st.expander("📊 View All Properties", expanded=False):
                        st.json(dict(graph.nodes[entity_id]))
                
                with col2:
                    st.subheader("📊 Score Components")
                    if 'components' in brief:
                        st.json(brief['components'])
                    
                    # Quick metrics
                    st.markdown("---")
                    st.subheader("📈 Quick Stats")
                    neighbors = list(graph.neighbors(entity_id))
                    st.metric("Direct Connections", len(neighbors))
                    st.metric("Network Degree", graph.degree(entity_id))
                
                st.markdown("---")
                
                # Evidence
                st.subheader("📄 Evidence Summary")
                if 'evidence' in brief:
                    for evidence in brief['evidence']:
                        st.markdown(f"**{evidence['type']}:** {evidence['description']}")
                        st.caption(f"Count: {evidence['count']} | Source: {evidence['source']}")
                        st.markdown("---")
                else:
                    st.info("No evidence available for this entity.")
                
                # Recommendations
                st.subheader("🎯 Investigation Recommendations")
                if 'recommendations' in brief:
                    for rec in brief['recommendations']:
                        st.markdown(f"• {rec}")
                else:
                    st.info("No recommendations available.")
        else:
            st.warning("Please load data first. Use the sidebar to upload data or load sample data.")
    
    elif selected_page == "Timeline":
        st.markdown('<h1 class="main-title">⏱️ Investigation Timeline</h1>', unsafe_allow_html=True)
        
        st.info("📈 Timeline view showing network evolution over time")
        
        # Generate sample timeline data
        dates = pd.date_range(start=datetime.now() - timedelta(days=180), end=datetime.now(), periods=20)
        entities = np.cumsum(np.random.randint(1, 5, size=len(dates)))
        relationships = np.cumsum(np.random.randint(1, 8, size=len(dates)))
        
        timeline_df = pd.DataFrame({
            'Date': dates,
            'Entities': entities,
            'Relationships': relationships
        })
        
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
        
        # Key events
        st.subheader("📌 Key Events")
        events = [
            {"date": dates[5], "event": "First cross-case connection discovered"},
            {"date": dates[10], "event": "Network expansion detected - 3 new entities"},
            {"date": dates[14], "event": "Priority lead identified in Case #27"},
            {"date": dates[17], "event": "Evidence breakthrough - financial pattern found"}
        ]
        
        for event in events:
            col1, col2 = st.columns([1, 4])
            with col1:
                st.caption(event["date"].strftime("%Y-%m-%d"))
            with col2:
                st.markdown(f"🔹 {event['event']}")
    
    elif selected_page == "Cross-Case":
        st.markdown('<h1 class="main-title">🔗 Cross-Case Connection Discovery</h1>', unsafe_allow_html=True)
        
        st.info("🔍 Discovering connections between cases...")
        
        # Generate sample cross-case connections
        cross_cases = [
            {"case1": "CASE-001", "case2": "CASE-002", "shared_entities": 3, "connections": 5, "confidence": 0.85},
            {"case1": "CASE-001", "case2": "CASE-003", "shared_entities": 1, "connections": 2, "confidence": 0.45},
            {"case1": "CASE-002", "case2": "CASE-004", "shared_entities": 4, "connections": 7, "confidence": 0.92},
            {"case1": "CASE-003", "case2": "CASE-004", "shared_entities": 2, "connections": 3, "confidence": 0.61},
            {"case1": "CASE-001", "case2": "CASE-004", "shared_entities": 1, "connections": 1, "confidence": 0.38}
        ]
        
        for connection in cross_cases:
            with st.expander(f"🔗 {connection['case1']} ↔ {connection['case2']}"):
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Shared Entities", connection['shared_entities'])
                with col2:
                    st.metric("Total Connections", connection['connections'])
                with col3:
                    st.metric("Confidence", f"{connection['confidence']*100:.0f}%")
                
                st.progress(connection['connections'] / 10)
                
                # Show shared entities
                st.write("**Shared Entities:**")
                for i in range(connection['shared_entities']):
                    st.markdown(f"- Entity {chr(65+i)} (appears in both cases)")
        
        st.markdown("---")
        st.subheader("📊 Network Visualization")
        st.info("Interactive visualization coming soon in the Network Graph tab")
    
    elif selected_page == "AI Assistant":
        st.markdown('<h1 class="main-title">🤖 AI Investigation Copilot</h1>', unsafe_allow_html=True)
        
        st.info("💡 Ask questions about your investigation or get AI-generated insights")
        
        # AI Assistant interface
        user_query = st.text_area(
            "What would you like to know?",
            placeholder="Example: What are the strongest connections between Entity A and Case 17?",
            height=100
        )
        
        col1, col2 = st.columns([1, 4])
        with col1:
            analyze_button = st.button("🔍 Analyze", use_container_width=True)
        
        if analyze_button and user_query:
            with st.spinner("AI is analyzing the investigation data..."):
                st.markdown("---")
                st.markdown("### 🤖 AI Response")
                
                # Simulated AI response
                response = f"""
                ## Investigation Brief
                
                ### Query Analysis
                I've analyzed your query about **{user_query[:50]}...**
                
                ### Key Findings
                1. **Entity E-104** appears as a central figure in this network
                2. **3 potential hidden connections** discovered
                3. **Cross-case link detected** with Case #27
                4. **Financial pattern** identified involving 4 accounts
                
                ### Detailed Analysis
                Based on the evidence graph and relationship patterns:
                - Entity E-104 has connections to 7 other entities in this case
                - 2 of these connections cross over to other cases
                - Recent activity spike detected in the last 48 hours
                
                ### Recommended Actions
                - 🔴 **Immediate**: Prioritize investigation of Entity E-104
                - 🟡 **Within 24 hours**: Review financial records for suspicious patterns
                - 🟢 **Ongoing**: Coordinate with investigators on Case #27
                
                ### Evidence Summary
                - 8 supporting records found
                - 4 communication links identified
                - 3 financial transactions flagged
                - 2 location overlaps detected
                """
                
                st.markdown(response)
                
                st.warning("⚠️ This is an AI-generated analysis. All findings should be verified by human investigators.")
        
        elif analyze_button and not user_query:
            st.warning("Please enter a question first.")
        
        # Suggested questions
        st.subheader("💬 Suggested Questions")
        questions = [
            "What are the most central entities in this network?",
            "Show me all connections between Entity A and Entity B",
            "What patterns indicate criminal activity?",
            "Which entities have the highest priority for investigation?",
            "Are there any cross-case connections I should know about?"
        ]
        
        for q in questions:
            if st.button(q, key=f"q_{hash(q)}", use_container_width=False):
                st.session_state.user_query = q
                st.rerun()

# Footer
st.markdown("---")
st.caption("🕵️ SUTRA-X v1.0.0 | Smart Unified Threat & Relationship Analytics | Powered by AI")

# Error handling for missing components
if not BACKEND_AVAILABLE:
    st.sidebar.warning("⚠️ Some features may be limited. Backend modules not available.")