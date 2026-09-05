
"""
Heatmap Page - Real Folium Heatmap
"""

import streamlit as st
from streamlit_folium import folium_static
from app.backend.heatmap.heatmap_generator import HeatmapGenerator
from app.backend.security.audit import audit_logger
from app.backend.security.rbac import rbac_manager

def render():
    """Render Heatmap page"""
    
    st.markdown("""
    <div style="animation: fadeInUp 0.6s ease-out;">
        <h1 style="font-size: 2.5rem; font-weight: 700; color: #1a1a2e;">
            🗺️ Geographic Heatmap
        </h1>
        <p style="color: #666; margin-top: -0.5rem;">Visualize crime hotspots and patterns on interactive maps</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Check permissions
    if not rbac_manager.has_permission(st.session_state.get('user_role', 'viewer'), 'view_data'):
        st.warning("🔒 You don't have permission to access this feature.")
        return
    
    # Initialize heatmap generator
    heatmap_gen = HeatmapGenerator()
    
    st.info("🌍 Interactive heatmap showing crime hotspots and entity locations")
    
    if st.session_state.get('graph'):
        G = st.session_state.graph
        
        # Generate heatmap
        with st.spinner("🔄 Generating heatmap..."):
            m = heatmap_gen.generate_heatmap_from_graph(G)
            
            if m:
                # Display heatmap
                folium_static(m, width=1000, height=600)
                
                # Log the view
                audit_logger.log(
                    "view_heatmap",
                    st.session_state.get('user_role', 'unknown'),
                    "Heatmap",
                    "Viewed geographic heatmap"
                )
                
                st.markdown("---")
                
                # Legend
                st.markdown("""
                <div style="background: white; padding: 1rem; border-radius: 12px; 
                            box-shadow: 0 2px 10px rgba(0,0,0,0.05);">
                    <h4 style="margin: 0 0 0.5rem 0;">📊
