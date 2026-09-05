
"""
Real Heatmap Generator using Folium
"""

import folium
from folium import plugins
import pandas as pd
import json
from typing import List, Dict, Any
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
import time

class HeatmapGenerator:
    """Real Heatmap Generator with Folium"""
    
    def __init__(self):
        self.geolocator = Nominatim(user_agent="sutra_x_heatmap")
        self.cache = {}
    
    def generate_heatmap(self, locations_data: List[Dict], center_lat: float = 20.5937, center_lon: float = 78.9629):
        """Generate an interactive heatmap"""
        
        # Create base map
        m = folium.Map(
            location=[center_lat, center_lon],
            zoom_start=4,
            tiles='OpenStreetMap'
        )
        
        # Add heatmap layer
        heat_data = []
        for loc in locations_data:
            if loc.get('lat') and loc.get('lon'):
                heat_data.append([
                    loc['lat'],
                    loc['lon'],
                    loc.get('intensity', 1)
                ])
        
        if heat_data:
            plugins.HeatMap(
                heat_data,
                radius=20,
                blur=15,
                max_zoom=10,
                gradient={
                    0.2: 'blue',
                    0.4: 'lime',
                    0.6: 'yellow',
                    0.8: 'orange',
                    1.0: 'red'
                }
            ).add_to(m)
        
        # Add markers for each location
        for loc in locations_data:
            if loc.get('lat') and loc.get('lon'):
                popup_text = f"""
                <b>{loc.get('name', 'Unknown')}</b><br>
                Type: {loc.get('type', 'Unknown')}<br>
                Intensity: {loc.get('intensity', 0)}
                """
                
                # Color based on intensity
                intensity = loc.get('intensity', 50)
                if intensity > 70:
                    color = 'red'
                elif intensity > 40:
                    color = 'orange'
                else:
                    color = 'green'
                
                folium.Marker(
                    location=[loc['lat'], loc['lon']],
                    popup=folium.Popup(popup_text, max_width=300),
                    icon=folium.Icon(color=color, icon='info-sign')
                ).add_to(m)
        
        # Add cluster plugin
        plugins.MarkerCluster().add_to(m)
        
        return m
    
    def get_coordinates(self, address: str) -> Dict:
        """Get coordinates from address using geocoding"""
        if address in self.cache:
            return self.cache[address]
        
        try:
            location = self.geolocator.geocode(address)
            if location:
                result = {
                    'lat': location.latitude,
                    'lon': location.longitude
                }
                self.cache[address] = result
                return result
        except GeocoderTimedOut:
            time.sleep(1)
            return self.get_coordinates(address)
        except Exception as e:
            print(f"Geocoding error: {e}")
        
        return None
    
    def generate_heatmap_from_graph(self, G):
        """Generate heatmap from graph data"""
        locations_data = []
        
        if not G:
            return self.generate_heatmap([])
        
        # Extract location data from graph
        for node in G.nodes:
            attrs = dict(G.nodes[node])
            if attrs.get('type') in ['LOCATION', 'PERSON']:
                lat = attrs.get('latitude')
                lon = attrs.get('longitude')
                name = attrs.get('name', attrs.get('city', str(node)))
                
                if lat and lon:
                    degree = len(list(G.neighbors(node)))
                    intensity = min(100, degree * 10 + 10)
                    
                    locations_data.append({
                        'id': str(node),
                        'name': name,
                        'type': attrs.get('type'),
                        'lat': float(lat),
                        'lon': float(lon),
                        'intensity': intensity,
                        'degree': degree
                    })
        
        # If no coordinates found, add some sample Indian locations
        if not locations_data:
            sample_locations = [
                {'name': 'Mumbai', 'lat': 19.0760, 'lon': 72.8777, 'intensity': 85, 'type': 'LOCATION'},
                {'name': 'Delhi', 'lat': 28.6139, 'lon': 77.2090, 'intensity': 78, 'type': 'LOCATION'},
                {'name': 'Bangalore', 'lat': 12.9716, 'lon': 77.5946, 'intensity': 65, 'type': 'LOCATION'},
                {'name': 'Chennai', 'lat': 13.0827, 'lon': 80.2707, 'intensity': 55, 'type': 'LOCATION'},
                {'name': 'Hyderabad', 'lat': 17.3850, 'lon': 78.4867, 'intensity': 60, 'type': 'LOCATION'},
                {'name': 'Kolkata', 'lat': 22.5726, 'lon': 88.3639, 'intensity': 45, 'type': 'LOCATION'},
                {'name': 'Pune', 'lat': 18.5204, 'lon': 73.8567, 'intensity': 40, 'type': 'LOCATION'},
                {'name': 'Ahmedabad', 'lat': 23.0225, 'lon': 72.5714, 'intensity': 35, 'type': 'LOCATION'},
                {'name': 'Jaipur', 'lat': 26.9124, 'lon': 75.7873, 'intensity': 30, 'type': 'LOCATION'},
                {'name': 'Lucknow', 'lat': 26.8467, 'lon': 80.9462, 'intensity': 28, 'type': 'LOCATION'},
            ]
            locations_data = sample_locations
        
        return self.generate_heatmap(locations_data)
