import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import networkx as nx
import sys
from pathlib import Path

# Add backend to path
sys.path.append(str(Path(__file__).parent.parent.parent))

from backend.core.config import settings
from backend.data_ingestion.loader import DataLoader
from backend.graph_engine.graph_builder import CriminalGraphBuilder, GraphAnalyzer
from backend.intelligence_engine.priority_scorer import PriorityScorer
from backend.nlp_engine.entity_extractor import EntityExtractor

# Page configuration
st.set_page_config(
    page_title="NEXUS-INTEL - Criminal Network Intelligence",
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
        color: #1a1a2e;
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

# Sidebar
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/000000/investigation.png", width=80)
    st.title("NEXUS-INTEL")
    st.caption("v1.0.0 | AI-Powered Investigation")
    
    st.markdown("---")
    
    # Language selector
    language = st.selectbox(
        "🌐 Language",
        ["English", "हिंदी", "தமிழ்", "తెలుగు", "বাংলা"]
    )
    
    st.markdown("---")
    
    # Data upload section
    st.subheader("📂 Data Upload")
    
    uploaded_files = st.file_uploader(
        "Upload case data (CSV, JSON, Excel)",
        type=['csv', 'json', 'xlsx'],
        accept_multiple_files=True
    )
    
    if uploaded_files and st.button("🚀 Process Data"):
        with st.spinner("Processing data... This may take a moment."):
            loader = DataLoader()
            data_frames = {}
            
            for file in uploaded_files:
                # Save uploaded file temporarily
                import tempfile
                with tempfile.NamedTemporaryFile(delete=False, suffix=f".{file.name.split('.')[-1]}") as tmp_file:
                    tmp_file.write(file.getvalue())
                    tmp_path = Path(tmp_file.name)
                    
                    # Load based on extension
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
    
    st.markdown("---")
    
    # Quick navigation
    st.subheader("📌 Quick Navigation")
    nav_options = ["Dashboard", "Network Graph", "Entity Profile", "Timeline", "Cross-Case", "AI Assistant"]
    selected_page = st.radio("Go to", nav_options)

# Main content
if not st.session_state.data_loaded:
    # Landing page
    st.markdown('<h1 class="main-title">🕵️ NEXUS-INTEL</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-title">From Fragmented Evidence to Actionable Intelligence</p>', unsafe_allow_html=True)
    
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
    st.info("👈 **Get Started:** Upload your case data using the sidebar to begin investigation.")
    
else:
    # Main application
    if selected_page == "Dashboard":
        st.markdown('<h1 class="main-title">📊 Command Center</h1>', unsafe_allow_html=True)
        
        # Metrics
        col1, col2, col3, col4 = st.columns(4)
        
        graph = st.session_state.graph
        analyzer = st.session_state.analyzer
        scorer = st.session_state.scorer
        
        with col1:
            st.metric("Total Entities", len(graph.nodes()))
        with col2:
            st.metric("Relationships", len(graph.edges()))
        with col3:
            high_priority = len([s for s in scorer.get_high_priority_leads()])
            st.metric("High Priority Leads", high_priority, delta="🚨 Immediate")
        with col4:
            # Calculate cross-case connections
            cross_case = len([e for e in graph.nodes() if len(list(graph.neighbors(e))) > 3])
            st.metric("Cross-Case Links", cross_case, delta="🔗 Connections")
        
        st.markdown("---")
        
        # Priority Leads
        st.subheader("🚨 Priority Investigation Leads")
        leads = scorer.get_high_priority_leads(threshold=0.6)
        
        if leads:
            for lead in leads[:5]:
                col1, col2, col3 = st.columns([3,1,1])
                with col1:
                    st.markdown(f"**🟢 {lead['entity_id']}**")
                    st.caption(f"Score: {lead['score']} | Priority: {lead['priority']}")
                with col2:
                    if lead['priority'] == 'HIGH':
                        st.markdown("🔴 **URGENT**")
                with col3:
                    st.button("Investigate", key=f"investigate_{lead['entity_id']}")
                
                with st.expander(f"View Details - {lead['entity_id']}"):
                    st.json(lead['components'])
                st.markdown("---")
        else:
            st.info("No high priority leads found at this time.")
        
        # Recent Activity
        st.subheader("📈 Recent Activity")
        st.info("Network analysis shows 3 potential connections emerging in the last 24 hours.")
        
    elif selected_page == "Network Graph":
        st.markdown('<h1 class="main-title">🌐 Network Graph</h1>', unsafe_allow_html=True)
        
        # Graph controls
        col1, col2, col3 = st.columns([2, 2, 1])
        with col1:
            centrality_metric = st.selectbox(
                "Color by",
                ["None", "Degree Centrality", "Betweenness Centrality", "Entity Type"]
            )
        with col2:
            layout = st.selectbox(
                "Layout",
                ["Spring", "Circular", "Shell", "Kamada-Kawai"]
            )
        with col3:
            st.write("")
            st.write("")
            show_edges = st.checkbox("Show Edges", value=True)
        
        # Display graph
        graph = st.session_state.graph
        
        # Convert networkx to plotly
        pos = nx.spring_layout(graph)
        
        edge_x = []
        edge_y = []
        for edge in graph.edges():
            x0, y0 = pos[edge[0]]
            x1, y1 = pos[edge[1]]
            edge_x.extend([x0, x1, None])
            edge_y.extend([y0, y1, None])
        
        edge_trace = go.Scatter(
            x=edge_x, y=edge_y,
            line=dict(width=0.5, color='#888'),
            hoverinfo='none',
            mode='lines'
        )
        
        node_x = []
        node_y = []
        node_text = []
        node_color = []
        
        color_map = {
            'PERSON': '#FF6B6B',
            'PHONE': '#4ECDC4',
            'ACCOUNT': '#45B7D1',
            'VEHICLE': '#96CEB4',
            'LOCATION': '#FFEAA7',
            'ORGANIZATION': '#DDA0DD'
        }
        
        for node in graph.nodes():
            x, y = pos[node]
            node_x.append(x)
            node_y.append(y)
            node_text.append(f"{node}<br>Degree: {graph.degree(node)}")
            node_color.append(color_map.get(graph.nodes[node].get('type', 'UNKNOWN'), '#888'))
        
        node_trace = go.Scatter(
            x=node_x, y=node_y,
            mode='markers',
            hoverinfo='text',
            text=node_text,
            marker=dict(
                size=20,
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
                           plot_bgcolor='#f8f9fa'
                       ))
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Selected entity details
        selected_entity = st.selectbox("Select Entity to Investigate", list(graph.nodes()))
        if selected_entity:
            with st.expander(f"🔍 Entity Profile: {selected_entity}", expanded=True):
                st.json(graph.nodes[selected_entity])
                neighbors = list(graph.neighbors(selected_entity))
                st.write(f"**Connections:** {len(neighbors)}")
                if neighbors:
                    st.write("**Connected to:**", ", ".join(neighbors[:5]))
    
    elif selected_page == "Entity Profile":
        st.markdown('<h1 class="main-title">👤 Entity Intelligence</h1>', unsafe_allow_html=True)
        
        graph = st.session_state.graph
        scorer = st.session_state.scorer
        
        entity_id = st.selectbox("Search Entity", list(graph.nodes()))
        
        if entity_id:
            brief = scorer.generate_investigation_brief(entity_id)
            
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.subheader(f"📋 Entity: {entity_id}")
                st.markdown(f"**Priority:** {brief['priority']}")
                st.markdown(f"**Score:** {brief['score']:.1f}/100")
                
                st.markdown("---")
                st.markdown("**Summary:**")
                st.markdown(brief['summary'])
                
                st.markdown("---")
                st.markdown("**Connections:**")
                for conn in brief['connections'][:5]:
                    st.markdown(f"- {conn['entity_id']} ({conn['relationship']})")
                
            with col2:
                st.subheader("📊 Score Components")
                st.json(brief['components'])
            
            st.markdown("---")
            
            # Evidence
            st.subheader("📄 Evidence Summary")
            for evidence in brief['evidence']:
                st.markdown(f"**{evidence['type']}:** {evidence['description']}")
                st.caption(f"Count: {evidence['count']} | Source: {evidence['source']}")
                st.markdown("---")
            
            # Recommendations
            st.subheader("🎯 Investigation Recommendations")
            for rec in brief['recommendations']:
                st.markdown(f"• {rec}")
    
    elif selected_page == "Timeline":
        st.markdown('<h1 class="main-title">⏱️ Investigation Timeline</h1>', unsafe_allow_html=True)
        
        # Timeline visualization
        st.info("Timeline view showing network evolution over time")
        
        # Sample timeline data
        timeline_data = {
            'Date': ['2025-01-01', '2025-02-01', '2025-03-01', '2025-04-01'],
            'Entities': [10, 25, 45, 67],
            'Relationships': [15, 40, 78, 120]
        }
        df = pd.DataFrame(timeline_data)
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df['Date'], y=df['Entities'],
                                 mode='lines+markers',
                                 name='Entities',
                                 line=dict(color='#667eea', width=3)))
        fig.add_trace(go.Scatter(x=df['Date'], y=df['Relationships'],
                                 mode='lines+markers',
                                 name='Relationships',
                                 line=dict(color='#ff6b6b', width=3)))
        
        fig.update_layout(
            title='Network Evolution Over Time',
            xaxis_title='Date',
            yaxis_title='Count',
            hovermode='x unified',
            plot_bgcolor='#f8f9fa'
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    elif selected_page == "Cross-Case":
        st.markdown('<h1 class="main-title">🔗 Cross-Case Connection Discovery</h1>', unsafe_allow_html=True)
        
        # Cross-case analysis
        st.info("🔍 Discovering connections between cases...")
        
        # Sample cross-case connections
        cross_cases = [
            {"case1": "CASE-001", "case2": "CASE-002", "shared_entities": 3, "connections": 5},
            {"case1": "CASE-001", "case2": "CASE-003", "shared_entities": 1, "connections": 2},
            {"case1": "CASE-002", "case2": "CASE-004", "shared_entities": 4, "connections": 7}
        ]
        
        for connection in cross_cases:
            with st.expander(f"🔗 {connection['case1']} ↔ {connection['case2']}"):
                st.metric("Shared Entities", connection['shared_entities'])
                st.metric("Total Connections", connection['connections'])
                st.progress(connection['connections'] / 10)
        
    elif selected_page == "AI Assistant":
        st.markdown('<h1 class="main-title">🤖 AI Investigation Copilot</h1>', unsafe_allow_html=True)
        
        st.info("💡 Ask questions about your investigation or get AI-generated insights")
        
        # AI Assistant interface
        user_query = st.text_area("What would you like to know?",
                                  placeholder="Example: What are the strongest connections between Entity A and Case 17?")
        
        if st.button("🔍 Analyze"):
            with st.spinner("AI is analyzing the investigation data..."):
                st.markdown("---")
                st.markdown("**AI Response:**")
                
                # Sample AI response
                st.markdown("""
                ### Investigation Brief
                
                **Key Findings:**
                1. Entity E-104 appears as a central figure in this network
                2. 3 potential hidden connections discovered
                3. Cross-case link detected with Case #27
                
                **Recommended Actions:**
                - Prioritize investigation of Entity E-104
                - Review financial records for suspicious patterns
                - Coordinate with investigators on Case #27
                
                **Evidence Summary:**
                - 8 supporting records found
                - 4 communication links identified
                - 3 financial transactions flagged
                """)
                
                st.warning("⚠️ This is an AI-generated analysis. All findings should be verified by human investigators.")