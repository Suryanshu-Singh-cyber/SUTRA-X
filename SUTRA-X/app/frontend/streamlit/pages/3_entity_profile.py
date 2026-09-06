"""
Entity Profile Page
"""

import streamlit as st
import random
from app.backend.graph_engine.graph_builder import get_node_list, get_node_attributes, get_neighbors, get_degree, get_edge_data

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
        'priority_score': random.uniform(0.3, 0.9),
        'evidence': []
    }
    
    for neighbor in neighbors:
        edge_data = get_edge_data(G, entity_id, neighbor)
        if not edge_data:
            edge_data = get_edge_data(G, neighbor, entity_id)
        
        details['connections'].append({
            'entity_id': neighbor,
            'relation': edge_data.get('type', 'CONNECTED'),
            'properties': edge_data
        })
        
        if edge_data.get('type') in ['CALLED', 'TRANSACTION', 'VISITED']:
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

def render():
    """Render Entity Profile page"""
    
    G = st.session_state.graph
    node_list = get_node_list(G)
    
    st.markdown("""
    <div style="animation: fadeInUp 0.6s ease-out;">
        <h1 style="font-size: 2.5rem; font-weight: 700; color: #1a1a2e;">👤 Entity Intelligence</h1>
        <p style="color: #666; margin-top: -0.5rem;">Deep dive into entity details and connections</p>
    </div>
    """, unsafe_allow_html=True)
    
    if not st.session_state.data_loaded or G is None:
        st.info("👈 Click 'Generate Sample Data' in the sidebar to get started")
        return
    
    if not node_list:
        st.warning("No entities in the network.")
        return
    
    # ===== ENTITY SELECTOR =====
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
    
    # ===== MAIN CONTENT =====
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown(f"""
        <div style="background: white; padding: 1.5rem; border-radius: 15px; box-shadow: 0 4px 20px rgba(0,0,0,0.08);">
            <h2 style="font-size: 1.5rem; font-weight: 700; color: #1a1a2e;">📋 {entity_id}</h2>
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
        
        st.markdown("**📊 Properties:**")
        for key, value in attrs.items():
            st.markdown(f"- **{key}:** {value}")
        
        st.markdown("---")
        
        st.markdown(f"**🔗 Connections ({len(details['connections'])})**")
        for conn in details['connections'][:10]:
            st.markdown(f"""
            <div class="entity-card">
                <strong>→ {conn['entity_id']}</strong>
                <br><span style="color: #888; font-size: 0.85rem;">Relation: {conn['relation']}</span>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        # ===== QUICK STATS - FIXED DARK TEXT =====
        st.markdown(f"""
        <div class="quick-stats">
            <h3 style="font-size: 1.2rem; font-weight: 600; color: #1a1a2e; margin-top: 0;">📊 Quick Stats</h3>
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
                <span class="stat-label">Entity Type</span>
                <span class="stat-value">{attrs.get('type', 'UNKNOWN')}</span>
            </div>
            <div class="stat-item" style="border-bottom: none;">
                <span class="stat-label">Evidence Count</span>
                <span class="stat-value">{len(details.get('evidence', []))}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # ===== EVIDENCE =====
        st.markdown("""
        <div style="background: white; padding: 1.5rem; border-radius: 15px; box-shadow: 0 4px 20px rgba(0,0,0,0.08);">
            <h3 style="font-size: 1.2rem; font-weight: 600; color: #1a1a2e; margin-top: 0;">📄 Evidence</h3>
        """, unsafe_allow_html=True)
        
        if details.get('evidence'):
            for ev in details['evidence'][:3]:
                st.markdown(f"""
                <div style="padding: 0.5rem 0; border-bottom: 1px solid #eee;">
                    <strong>{ev['type']}</strong>
                    <br><span style="color: #888; font-size: 0.85rem;">{ev['description']}</span>
                    <br><span style="color: #666; font-size: 0.75rem;">Confidence: {ev['confidence']:.0%}</span>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No evidence available")
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown("---")
        
        # ===== RECOMMENDATIONS =====
        st.markdown("""
        <div style="background: white; padding: 1.5rem; border-radius: 15px; box-shadow: 0 4px 20px rgba(0,0,0,0.08);">
            <h3 style="font-size: 1.2rem; font-weight: 600; color: #1a1a2e; margin-top: 0;">🎯 Recommendations</h3>
        """, unsafe_allow_html=True)
        
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
        
        st.markdown("</div>", unsafe_allow_html=True)
