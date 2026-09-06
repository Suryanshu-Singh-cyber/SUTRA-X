"""
Heatmap Page - Interactive Map
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from app.backend.graph_engine.graph_builder import get_node_list, get_node_attributes, get_degree

def render():
    """Render Heatmap page with interactive map"""
    
    G = st.session_state.graph
    node_list = get_node_list(G)
    
    st.markdown("""
    <div style="animation: fadeInUp 0.6s ease-out;">
        <h1 style="font-size: 2.5rem; font-weight: 700; color: #1a1a2e;">🗺️ Geographic Heatmap</h1>
        <p style="color: #666; margin-top: -0.5rem;">Visualize crime hotspots and entity locations</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Collect location data
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
                    'Intensity': intensity,
                    'Degree': degree
                })
    
    if not heatmap_data:
        # Sample data for demo
        heatmap_data = [
            {'ID': 'L-001', 'Name': 'Mumbai', 'Type': 'LOCATION', 'Latitude': 19.0760, 'Longitude': 72.8777, 'Intensity': 85, 'Degree': 12},
            {'ID': 'L-002', 'Name': 'Delhi', 'Type': 'LOCATION', 'Latitude': 28.6139, 'Longitude': 77.2090, 'Intensity': 78, 'Degree': 9},
            {'ID': 'L-003', 'Name': 'Bangalore', 'Type': 'LOCATION', 'Latitude': 12.9716, 'Longitude': 77.5946, 'Intensity': 65, 'Degree': 7},
            {'ID': 'L-004', 'Name': 'Chennai', 'Type': 'LOCATION', 'Latitude': 13.0827, 'Longitude': 80.2707, 'Intensity': 55, 'Degree': 5},
            {'ID': 'L-005', 'Name': 'Hyderabad', 'Type': 'LOCATION', 'Latitude': 17.3850, 'Longitude': 78.4867, 'Intensity': 60, 'Degree': 6},
            {'ID': 'L-006', 'Name': 'Kolkata', 'Type': 'LOCATION', 'Latitude': 22.5726, 'Longitude': 88.3639, 'Intensity': 45, 'Degree': 4},
            {'ID': 'L-007', 'Name': 'Pune', 'Type': 'LOCATION', 'Latitude': 18.5204, 'Longitude': 73.8567, 'Intensity': 40, 'Degree': 3},
            {'ID': 'L-008', 'Name': 'Ahmedabad', 'Type': 'LOCATION', 'Latitude': 23.0225, 'Longitude': 72.5714, 'Intensity': 35, 'Degree': 2},
        ]
        st.info("💡 Showing sample location data. Generate data with coordinates for full experience.")
    
    # Display data table
    df = pd.DataFrame(heatmap_data)
    st.dataframe(df[['ID', 'Name', 'Type', 'Latitude', 'Longitude', 'Intensity']], use_container_width=True)
    
    st.markdown("---")
    
    # Interactive Map
    st.markdown("### 🗺️ Location Map")
    
    try:
        fig = go.Figure()
        
        # Add scatter map
        fig.add_trace(go.Scattergeo(
            lon=df['Longitude'],
            lat=df['Latitude'],
            text=[f"{row['Name']}<br>Type: {row['Type']}<br>Intensity: {row['Intensity']}<br>Degree: {row['Degree']}" for _, row in df.iterrows()],
            mode='markers',
            marker=dict(
                size=[d['Intensity']/10 + 5 for d in heatmap_data],
                color=df['Intensity'],
                colorscale='Reds',
                showscale=True,
                colorbar=dict(title="Intensity"),
                line=dict(width=1, color='white'),
                opacity=0.9
            ),
            hoverinfo='text'
        ))
        
        fig.update_layout(
            title='Entity Locations Map',
            geo=dict(
                scope='asia',
                projection_type='mercator',
                center=dict(lat=20.5937, lon=78.9629),
                lonaxis_range=[68, 98],
                lataxis_range=[8, 38],
                showland=True,
                landcolor='#f0f0f0',
                coastlinecolor='#ccc',
                countrycolor='#ddd'
            ),
            height=600,
            margin=dict(l=0, r=0, t=40, b=0),
            paper_bgcolor='#f8f9fa'
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Legend
        st.markdown("""
        <div style="background: white; padding: 1rem; border-radius: 12px; margin-top: 1rem; box-shadow: 0 2px 10px rgba(0,0,0,0.05);">
            <h4 style="margin: 0 0 0.5rem 0;">📊 Legend</h4>
            <div style="display: flex; gap: 20px; flex-wrap: wrap;">
                <div><span style="display: inline-block; width: 20px; height: 20px; background: #ff4757; border-radius: 50%;"></span> High Intensity (70-100)</div>
                <div><span style="display: inline-block; width: 20px; height: 20px; background: #ffa502; border-radius: 50%;"></span> Medium Intensity (40-70)</div>
                <div><span style="display: inline-block; width: 20px; height: 20px; background: #2ed573; border-radius: 50%;"></span> Low Intensity (0-40)</div>
                <div><span style="display: inline-block; width: 20px; height: 20px; border-radius: 50%; border: 2px solid #667eea;"></span> Entity Location</div>
            </div>
            <div style="margin-top: 0.5rem; font-size: 0.85rem; color: #888;">
                💡 Larger circles indicate higher investigation priority
            </div>
        </div>
        """, unsafe_allow_html=True)
        
    except Exception as e:
        st.error(f"Error rendering map: {str(e)}")
        st.info("Showing data table instead.")
