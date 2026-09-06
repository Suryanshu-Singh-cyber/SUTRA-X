"""
Dashboard Page
"""

import streamlit as st
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))

from backend.graph_engine.graph_builder import get_node_list, get_node_attributes, get_neighbors
from backend.intelligence_engine.analyzer import analyze_network
import pandas as pd

def render():
    """Render Dashboard page"""
    
    G = st.session_state.graph
    node_list = get_node_list(G)
    metrics = analyze_network(G)
    
    st.markdown("""
    <div style="animation: fadeInUp 0.6s ease-out;">
        <h1 style="font-size: 2.5rem; font-weight: 700; color: #1a1a2e;">📊 Command Center</h1>
        <p style="color: #666; margin-top: -0.5rem;">Real-time intelligence dashboard</p>
    </div>
    """, unsafe_allow_html=True)
    
    if not st.session_state.data_loaded or G is None:
        st.info("👈 Click 'Generate Sample Data' in the sidebar to get started")
        return
    
    # ===== METRICS ROW =====
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="icon">👥</div>
            <div class="value">{metrics['total_nodes'] if metrics else 0}</div>
            <div class="label">Total Entities</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card" style="border-left-color: #4ECDC4;">
            <div class="icon">🔗</div>
            <div class="value">{metrics['total_edges'] if metrics else 0}</div>
            <div class="label">Relationships</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        high_priority = len([e for e in (metrics['priority_entities'] if metrics else []) if e['degree'] >= 4])
        st.markdown(f"""
        <div class="metric-card" style="border-left-color: #ff6b6b;">
            <div class="icon">🚨</div>
            <div class="value">{high_priority}</div>
            <div class="label">Priority Leads</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        cross_case = 0
        for node in node_list:
            attrs = get_node_attributes(G, node)
            if attrs.get('type') == 'PERSON':
                neighbors = get_neighbors(G, node)
                case_connections = sum(1 for n in neighbors if get_node_attributes(G, n).get('type') == 'CASE')
                if case_connections >= 2:
                    cross_case += 1
        st.markdown(f"""
        <div class="metric-card" style="border-left-color: #feca57;">
            <div class="icon">🔍</div>
            <div class="value">{cross_case}</div>
            <div class="label">Cross-Case Links</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col5:
        alert_count = len(st.session_state.alerts)
        st.markdown(f"""
        <div class="metric-card" style="border-left-color: #ff4757;">
            <div class="icon">🔔</div>
            <div class="value">{alert_count}</div>
            <div class="label">Active Alerts</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    
    # ===== PRIORITY LEADS =====
    st.markdown("## 🚨 Priority Investigation Leads")
    
    if metrics and metrics['priority_entities']:
        for entity in metrics['priority_entities'][:5]:
            score = min(100, entity['degree'] * 15)
            priority_label = "HIGH" if score >= 70 else "MEDIUM" if score >= 50 else "LOW"
            color = "🔴" if priority_label == "HIGH" else "🟡" if priority_label == "MEDIUM" else "🟢"
            
            col1, col2, col3, col4 = st.columns([2.5, 2, 1.5, 1])
            with col1:
                st.markdown(f"""
                <div class="entity-card">
                    <strong>🔍 {entity['id']}</strong>
                    <br><span style="color: #888; font-size: 0.85rem;">{entity['type']} | {entity['name']}</span>
                </div>
                """, unsafe_allow_html=True)
            with col2:
                st.caption(f"Connections: {entity['degree']}")
            with col3:
                st.markdown(f'<span class="status-badge status-{priority_label.lower()}">{color} {priority_label}</span>', unsafe_allow_html=True)
            with col4:
                if st.button("View", key=f"view_dash_{entity['id']}"):
                    st.session_state.selected_entity = entity['id']
                    st.session_state.current_page = "Entity Profile"
                    st.rerun()
            
            st.markdown("---")
    else:
        st.info("No priority leads found. Generate sample data to see leads.")
    
    # ===== RECENT ACTIVITY =====
    st.markdown("## 📋 Recent Activity")
    
    activities = [
        "🔄 Network analysis completed - 3 new patterns found",
        "🔗 Cross-case link discovered between CASE-001 and CASE-002",
        "🚨 Priority lead updated for Entity P-0012",
        "📊 Evidence correlation detected in financial records",
        "🔍 New entity added to the network"
    ]
    
    for activity in activities:
        st.markdown(f"<div style='padding: 0.3rem 0; animation: slideInLeft 0.5s ease-out;'>{activity}</div>", unsafe_allow_html=True)
    
    # ===== NETWORK STATS =====
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📈 Network Statistics")
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
        st.markdown("### 🔗 Quick Insights")
        insights = [
            f"🔹 {metrics['total_nodes'] if metrics else 0} entities in the network",
            f"🔹 {metrics['total_edges'] if metrics else 0} relationships detected",
            f"🔹 {len([e for e in (metrics['priority_entities'] if metrics else []) if e['degree'] >= 4])} high priority leads",
            f"🔹 {cross_case} cross-case connections found"
        ]
        for insight in insights:
            st.markdown(f"<div style='padding: 0.3rem 0;'>{insight}</div>", unsafe_allow_html=True)
