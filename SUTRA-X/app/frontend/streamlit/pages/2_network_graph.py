"""
Network Graph Page - 3D Visualization
"""

import streamlit as st
import pandas as pd
import networkx as nx
import plotly.graph_objects as go
from app.backend.graph_engine.graph_builder import get_node_list, get_node_attributes, get_degree, get_edge_data, get_neighbors

def render():
    """Render Network Graph page with 3D visualization"""
    
    G = st.session_state.graph
    node_list = get_node_list(G)
    
    st.markdown("""
    <div style="animation: fadeInUp 0.6s ease-out;">
        <h1 style="font-size: 2.5rem; font-weight: 700; color: #1a1a2e;">🌐 Network Graph</h1>
        <p style="color: #666; margin-top: -0.5rem;">Interactive 3D network visualization</p>
    </div>
    """, unsafe_allow_html=True)
    
    if not st.session_state.data_loaded or G is None:
        st.info("👈 Click 'Generate Sample Data' in the sidebar to get started")
        return
    
    if not node_list or len(node_list) < 2:
        st.warning("Not enough data for graph visualization. Please generate sample data.")
        return
    
    try:
        import networkx as nx
        import plotly.graph_objects as go
        
        st.info("💡 Hover over nodes for details. Drag to rotate the 3D view. Scroll to zoom.")
        
        # ===== 3D LAYOUT =====
        pos = nx.spring_layout(G, dim=3, k=0.5, iterations=50)
        
        # ===== NODE DATA =====
        node_x = []
        node_y = []
        node_z = []
        node_text = []
        node_color = []
        node_size = []
        
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
                x, y, z = pos[node]
                node_x.append(x)
                node_y.append(y)
                node_z.append(z)
                attrs = get_node_attributes(G, node)
                node_type = attrs.get('type', 'UNKNOWN')
                degree = get_degree(G, node)
                name = attrs.get('name', attrs.get('number', ''))
                node_text.append(f"<b>{node}</b><br>Type: {node_type}<br>Name: {name}<br>Degree: {degree}")
                node_color.append(color_map.get(node_type, '#888888'))
                node_size.append(10 + degree * 3)
            except:
                continue
        
        # ===== EDGE DATA =====
        edge_x = []
        edge_y = []
        edge_z = []
        
        for edge in G.edges():
            try:
                x0, y0, z0 = pos[edge[0]]
                x1, y1, z1 = pos[edge[1]]
                edge_x.extend([x0, x1, None])
                edge_y.extend([y0, y1, None])
                edge_z.extend([z0, z1, None])
            except:
                continue
        
        # ===== CREATE FIGURE =====
        edge_trace = go.Scatter3d(
            x=edge_x, y=edge_y, z=edge_z,
            line=dict(width=1, color='rgba(136, 136, 136, 0.3)'),
            hoverinfo='none',
            mode='lines'
        )
        
        node_trace = go.Scatter3d(
            x=node_x, y=node_y, z=node_z,
            mode='markers',
            hoverinfo='text',
            text=node_text,
            marker=dict(
                size=node_size,
                color=node_color,
                opacity=0.9,
                line=dict(width=1, color='#fff')
            )
        )
        
        fig = go.Figure(
            data=[edge_trace, node_trace],
            layout=go.Layout(
                title='3D Criminal Network Graph',
                scene=dict(
                    xaxis=dict(showgrid=False, showticklabels=False, title=''),
                    yaxis=dict(showgrid=False, showticklabels=False, title=''),
                    zaxis=dict(showgrid=False, showticklabels=False, title=''),
                    bgcolor='#f8f9fa',
                    camera=dict(
                        eye=dict(x=1.5, y=1.5, z=1.5)
                    )
                ),
                height=700,
                margin=dict(l=0, r=0, t=40, b=0),
                paper_bgcolor='#f8f9fa'
            )
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # ===== LEGEND =====
        st.markdown("""
        <div style="background: white; padding: 1rem; border-radius: 12px; margin-top: 1rem; box-shadow: 0 2px 10px rgba(0,0,0,0.05);">
            <h4 style="margin: 0 0 0.5rem 0;">📊 Legend</h4>
            <div style="display: flex; gap: 20px; flex-wrap: wrap;">
                <div><span style="display: inline-block; width: 20px; height: 20px; background: #FF6B6B; border-radius: 50%;"></span> Person</div>
                <div><span style="display: inline-block; width: 20px; height: 20px; background: #4ECDC4; border-radius: 50%;"></span> Phone</div>
                <div><span style="display: inline-block; width: 20px; height: 20px; background: #45B7D1; border-radius: 50%;"></span> Account</div>
                <div><span style="display: inline-block; width: 20px; height: 20px; background: #96CEB4; border-radius: 50%;"></span> Vehicle</div>
                <div><span style="display: inline-block; width: 20px; height: 20px; background: #FFEAA7; border-radius: 50%;"></span> Location</div>
                <div><span style="display: inline-block; width: 20px; height: 20px; background: #FF9FF3; border-radius: 50%;"></span> Case</div>
            </div>
            <div style="margin-top: 0.5rem; font-size: 0.85rem; color: #888;">
                💡 Larger circles indicate higher degree (more connections)
            </div>
        </div>
        """, unsafe_allow_html=True)
        
    except ImportError as e:
        st.warning(f"⚠️ {str(e)}. Please install: pip install networkx plotly")
        _show_fallback(G, node_list)
    except Exception as e:
        st.error(f"Error rendering 3D graph: {str(e)}")
        _show_fallback(G, node_list)
    
    # ===== ENTITY SELECTOR =====
    st.markdown("---")
    col1, col2 = st.columns([2, 1])
    with col1:
        if node_list:
            selected = st.selectbox("🔍 Select Entity to Investigate", node_list)
        else:
            selected = None
    with col2:
        if selected and st.button("👤 View Profile", use_container_width=True):
            st.session_state.selected_entity = selected
            st.session_state.current_page = "Entity Profile"
            st.rerun()

def _show_fallback(G, node_list):
    """Show fallback data view"""
    st.subheader("📋 Network Data")
    
    st.write("**Entities:**")
    node_data = []
    for node in node_list:
        attrs = get_node_attributes(G, node)
        node_data.append({
            'ID': node,
            'Type': attrs.get('type', 'UNKNOWN'),
            'Degree': get_degree(G, node),
            'Name': attrs.get('name', attrs.get('number', ''))
        })
    st.dataframe(pd.DataFrame(node_data), use_container_width=True)
    
    st.write("**Relationships:**")
    edge_data = []
    for u in node_list[:50]:
        for v in get_neighbors(G, u):
            if (u, v) not in [(e['Source'], e['Target']) for e in edge_data]:
                edge_data.append({
                    'Source': u,
                    'Target': v,
                    'Type': get_edge_data(G, u, v).get('type', 'CONNECTED')
                })
    if edge_data:
        st.dataframe(pd.DataFrame(edge_data), use_container_width=True)
