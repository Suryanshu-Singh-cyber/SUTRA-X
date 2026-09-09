"""
Real Data Upload Page
Location: app/frontend/streamlit/pages/data_upload.py
"""

import streamlit as st
import pandas as pd
import time
from pathlib import Path

# Import our data loader
import sys
sys.path.append(str(Path(__file__).parent.parent))
from utils.data_loader import RealDataLoader
from utils.fast_engine import FastCriminalNetwork

def render():
    """Render Real Data Upload page"""
    
    st.markdown("""
    <div style="animation: fadeInUp 0.6s ease-out;">
        <h1 style="font-size: 2.5rem; font-weight: 700; color: #1a1a2e;">📁 Real Data Upload</h1>
        <p style="color: #666; margin-top: -0.5rem;">Load and process real criminal datasets</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.info("""
    🚀 **Available Real Datasets:**
    
    | Dataset | Description | Size |
    |---------|-------------|------|
    | 📜 ILSI | Indian Supreme Court Cases with IPC Sections | 66,090 cases |
    | 📊 NCRB | Cyber Crime Data (15 years) | 15+ years |
    | 📱 Scam Hinglish | Indian Scam Communications | 1000+ records |
    | 🏛️ Multi-Scam | Multi-Class Scam Classification | 14,000 messages |
    | 📝 HIFIRE | FIR Handwritten Documents | 20,078 images |
    """)
    
    # Initialize data loader
    loader = RealDataLoader()
    
    # ========================================================================
    # STEP 1: Load Datasets
    # ========================================================================
    
    st.markdown("---")
    st.subheader("📂 Step 1: Load Datasets")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📜 Load ILSI Dataset", use_container_width=True):
            with st.spinner("Loading ILSI (66,090 cases)..."):
                cases = loader.load_ilsi_dataset()
                if cases:
                    st.success(f"✅ Loaded {len(cases)} cases!")
                else:
                    st.error("❌ ILSI not found. Clone: git clone https://github.com/Law-AI/LeSICiN.git datasets/ilsil")
    
    with col2:
        if st.button("📊 Load NCRB Data", use_container_width=True):
            with st.spinner("Loading NCRB Cyber Crime data..."):
                ncrb = loader.load_ncrb_cyber_data()
                if ncrb is not None:
                    st.success(f"✅ Loaded {len(ncrb)} records!")
                else:
                    st.error("❌ NCRB not found. Download from Kaggle.")
    
    with col3:
        if st.button("📱 Load Scam Data", use_container_width=True):
            with st.spinner("Loading Scam Hinglish data..."):
                scam = loader.load_scam_hinglish()
                if scam is not None:
                    st.success(f"✅ Loaded {len(scam)} records!")
                else:
                    st.error("❌ Scam data not found.")
    
    # Load Multi-Scam
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🏛️ Load Multi-Scam Dataset", use_container_width=True):
            with st.spinner("Loading Multi-Scam from Hugging Face..."):
                multi = loader.load_multi_scam()
                if multi:
                    st.success(f"✅ Loaded {len(multi['train'])} messages!")
                else:
                    st.error("❌ Install: pip install datasets huggingface-hub")
    
    # ========================================================================
    # STEP 2: Process Data
    # ========================================================================
    
    st.markdown("---")
    st.subheader("🔄 Step 2: Process Data")
    
    if st.button("🚀 Process All Data", use_container_width=True):
        with st.spinner("Processing all datasets..."):
            start_time = time.time()
            
            entities, relationships = loader.process_all_data()
            
            end_time = time.time()
            duration = end_time - start_time
            
            st.success(f"✅ Processed in {duration:.2f} seconds!")
            
            # Display summary
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Entities Extracted", len(entities))
            with col2:
                st.metric("Relationships Found", len(relationships))
            
            # Save to session state
            st.session_state.processed_entities = entities
            st.session_state.processed_relationships = relationships
            
            # Build graph
            from backend.graph_engine.graph_builder import build_graph_from_entities
            G = build_graph_from_entities(entities, relationships)
            st.session_state.graph = G
            st.session_state.data_loaded = True
            st.session_state.entity_list = list(G.nodes())
    
    # ========================================================================
    # STEP 3: View Data
    # ========================================================================
    
    st.markdown("---")
    st.subheader("📊 Step 3: View Data")
    
    if hasattr(st.session_state, 'processed_entities') and st.session_state.processed_entities:
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 📋 Entities")
            df_entities = pd.DataFrame(st.session_state.processed_entities[:100])
            if not df_entities.empty:
                st.dataframe(df_entities[['id', 'type', 'name', 'source']], use_container_width=True)
            else:
                st.info("No entities to display")
        
        with col2:
            st.markdown("#### 🔗 Relationships")
            df_rels = pd.DataFrame(st.session_state.processed_relationships[:100])
            if not df_rels.empty:
                st.dataframe(df_rels[['source', 'target', 'type']], use_container_width=True)
            else:
                st.info("No relationships to display")
        
        # Entity type distribution
        st.markdown("#### 📈 Entity Type Distribution")
        if st.session_state.processed_entities:
            types = {}
            for e in st.session_state.processed_entities:
                types[e.get('type', 'UNKNOWN')] = types.get(e.get('type', 'UNKNOWN'), 0) + 1
            st.bar_chart(pd.DataFrame(list(types.items()), columns=['Type', 'Count']).set_index('Type'))
    
    else:
        st.info("Process data first to view results.")
    
    # ========================================================================
    # STEP 4: Summary
    # ========================================================================
    
    st.markdown("---")
    st.subheader("📊 Dataset Summary")
    
    summary = loader.get_summary()
    if summary:
        st.json(summary)
    else:
        st.info("No datasets loaded yet.")
    
    # Quick stats
    if hasattr(st.session_state, 'graph') and st.session_state.graph:
        G = st.session_state.graph
        st.metric("Total Nodes", len(G.nodes()))
        st.metric("Total Edges", len(G.edges()))