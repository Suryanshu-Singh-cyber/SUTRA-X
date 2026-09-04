"""
SUTRA-X PHASE 2: Advanced Criminal Network Intelligence Platform
SIH 2026 | AI-Powered Criminal Network Analysis System
Features: Multi-Language, Offline Mode, Real-Time Alerts, Export Reports, Heatmaps, Simulation
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import json
import base64
import io
from pathlib import Path
import sys
import os
import hashlib
import time

# ============================================================================
# FALLBACK FOR NETWORKX & PLOTLY
# ============================================================================

try:
    import networkx as nx
    NETWORKX_AVAILABLE = True
except ImportError:
    NETWORKX_AVAILABLE = False

try:
    import plotly.graph_objects as go
    import plotly.express as px
    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

st.set_page_config(
    page_title="SUTRA-X PHASE 2 - Criminal Network Intelligence | SIH 2026",
    page_icon="🕵️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# ENHANCED CSS WITH PHASE 2 STYLES
# ============================================================================

st.markdown("""
<style>
    /* ===== ANIMATIONS ===== */
    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(30px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
    
    @keyframes shimmer {
        0% { background-position: -200% center; }
        100% { background-position: 200% center; }
    }
    
    @keyframes float {
        0% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
        100% { transform: translateY(0px); }
    }
    
    @keyframes glow {
        0% { box-shadow: 0 0 5px rgba(102, 126, 234, 0.2); }
        50% { box-shadow: 0 0 20px rgba(102, 126, 234, 0.6); }
        100% { box-shadow: 0 0 5px rgba(102, 126, 234, 0.2); }
    }
    
    @keyframes slideIn {
        from { opacity: 0; transform: translateX(-20px); }
        to { opacity: 1; transform: translateX(0); }
    }
    
    @keyframes alertPulse {
        0% { transform: scale(1); opacity: 1; }
        50% { transform: scale(1.1); opacity: 0.8; }
        100% { transform: scale(1); opacity: 1; }
    }
    
    /* ===== PHASE 2 NEW STYLES ===== */
    .alert-badge {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        padding: 6px 16px;
        border-radius: 50px;
        font-size: 0.8rem;
        font-weight: 600;
        animation: alertPulse 2s infinite;
    }
    
    .alert-critical {
        background: #ff4757;
        color: white;
    }
    
    .alert-warning {
        background: #ffa502;
        color: white;
    }
    
    .alert-info {
        background: #2ed573;
        color: white;
    }
    
    .language-selector {
        background: white;
        padding: 0.5rem;
        border-radius: 10px;
        border: 1px solid #e0e0e0;
    }
    
    .offline-badge {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 50px;
        font-size: 0.7rem;
        font-weight: 600;
        background: #ffa502;
        color: white;
    }
    
    .online-badge {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 50px;
        font-size: 0.7rem;
        font-weight: 600;
        background: #2ed573;
        color: white;
    }
    
    .export-btn {
        background: linear-gradient(135deg, #2ed573, #26de81);
        color: white;
        border: none;
        padding: 8px 20px;
        border-radius: 50px;
        font-weight: 600;
        transition: all 0.3s ease;
        cursor: pointer;
    }
    
    .export-btn:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 15px rgba(46, 213, 115, 0.4);
    }
    
    .simulation-card {
        background: linear-gradient(135deg, #f8f9fa, #e9ecef);
        padding: 1.5rem;
        border-radius: 15px;
        border: 2px dashed #667eea;
        transition: all 0.3s ease;
    }
    
    .simulation-card:hover {
        border-color: #764ba2;
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
    }
    
    .heatmap-container {
        background: white;
        padding: 1rem;
        border-radius: 15px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
    }
    
    /* ===== EXISTING STYLES ===== */
    .main-title {
        font-size: 3.5rem;
        font-weight: 800;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        background-size: 200% auto;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: shimmer 3s linear infinite;
        padding: 0.5rem 0;
        letter-spacing: -1px;
    }
    
    .main-title-sub {
        font-size: 1.2rem;
        color: #666;
        margin-bottom: 0.5rem;
        font-weight: 300;
        animation: fadeInUp 0.8s ease-out;
    }
    
    .sih-badge {
        display: inline-block;
        background: linear-gradient(135deg, #ff6b6b, #ee5a24);
        color: white;
        padding: 6px 20px;
        border-radius: 50px;
        font-size: 0.85rem;
        font-weight: 600;
        animation: pulse 2s infinite;
        margin: 5px 0;
    }
    
    .ps-badge {
        display: inline-block;
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        padding: 6px 20px;
        border-radius: 50px;
        font-size: 0.85rem;
        font-weight: 600;
        margin: 5px 10px 5px 0;
    }
    
    .phase-badge {
        display: inline-block;
        background: linear-gradient(135deg, #f093fb, #f5576c);
        color: white;
        padding: 4px 16px;
        border-radius: 50px;
        font-size: 0.75rem;
        font-weight: 700;
        margin: 5px 0;
        animation: glow 2s infinite;
    }
    
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        border-left: 5px solid #667eea;
        transition: all 0.3s ease;
        animation: fadeInUp 0.6s ease-out;
        position: relative;
        overflow: hidden;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 30px rgba(0,0,0,0.12);
    }
    
    .metric-card .icon {
        font-size: 2rem;
        margin-bottom: 0.5rem;
    }
    
    .metric-card .value {
        font-size: 2rem;
        font-weight: 700;
        color: #1a1a2e;
    }
    
    .metric-card .label {
        font-size: 0.9rem;
        color: #666;
        font-weight: 500;
    }
    
    .status-badge {
        padding: 4px 16px;
        border-radius: 50px;
        font-size: 0.8rem;
        font-weight: 600;
        display: inline-block;
        animation: fadeInUp 0.5s ease-out;
    }
    
    .status-high {
        background: #ff6b6b;
        color: white;
        animation: pulse 1.5s infinite;
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
        padding: 1rem 1.2rem;
        border-radius: 12px;
        margin: 0.5rem 0;
        border-left: 4px solid #667eea;
        transition: all 0.3s ease;
        animation: slideIn 0.5s ease-out;
    }
    
    .entity-card:hover {
        background: #f0f2f6;
        transform: translateX(5px);
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-weight: 600;
        border: none;
        padding: 0.6rem 2rem;
        border-radius: 50px;
        transition: all 0.3s ease;
        animation: glow 2s infinite;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) scale(1.02);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
    }
    
    .section-divider {
        height: 2px;
        background: linear-gradient(90deg, transparent, #667eea, #764ba2, transparent);
        margin: 2rem 0;
        animation: fadeInUp 0.8s ease-out;
    }
    
    .glow-card {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        border: 1px solid rgba(102,126,234,0.1);
        transition: all 0.3s ease;
        animation: glow 3s infinite;
    }
    
    .glow-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 30px rgba(102,126,234,0.15);
    }
    
    .footer {
        text-align: center;
        padding: 1.5rem 0;
        color: #888;
        font-size: 0.85rem;
        border-top: 1px solid #eee;
        margin-top: 2rem;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# SIMPLE GRAPH CLASS
# ============================================================================

class SimpleGraph:
    def __init__(self):
        self._nodes = {}
        self._adj = {}
        self._edges = {}
    
    def add_node(self, node, **attrs):
        self._nodes[node] = attrs
        if node not in self._adj:
            self._adj[node] = {}
    
    def add_edge(self, u, v, **attrs):
        if u not in self._adj:
            self._adj[u] = {}
        if v not in self._adj:
            self._adj[v] = {}
        self._adj[u][v] = attrs
        self._adj[v][u] = attrs
        self._edges[(u, v)] = attrs
    
    def neighbors(self, node):
        return list(self._adj.get(node, {}).keys())
    
    def degree(self, node):
        return len(self._adj.get(node, {}))
    
    @property
    def nodes(self):
        return self._nodes
    
    @property
    def edges(self):
        return self._edges
    
    def number_of_nodes(self):
        return len(self._nodes)
    
    def number_of_edges(self):
        return len(self._edges)
    
    def has_edge(self, u, v):
        return (u, v) in self._edges or (v, u) in self._edges
    
    def get_edge_data(self, u, v):
        if (u, v) in self._edges:
            return self._edges[(u, v)]
        if (v, u) in self._edges:
            return self._edges[(v, u)]
        return {}

# ============================================================================
# SESSION STATE
# ============================================================================

if 'data_loaded' not in st.session_state:
    st.session_state.data_loaded = False
if 'graph' not in st.session_state:
    st.session_state.graph = None
if 'selected_entity' not in st.session_state:
    st.session_state.selected_entity = None
if 'current_page' not in st.session_state:
    st.session_state.current_page = "Dashboard"
if 'entity_list' not in st.session_state:
    st.session_state.entity_list = []
if 'language' not in st.session_state:
    st.session_state.language = "en"
if 'offline_mode' not in st.session_state:
    st.session_state.offline_mode = False
if 'alerts' not in st.session_state:
    st.session_state.alerts = []
if 'simulation_results' not in st.session_state:
    st.session_state.simulation_results = None
if 'export_history' not in st.session_state:
    st.session_state.export_history = []

# ============================================================================
# MULTI-LANGUAGE SUPPORT
# ============================================================================

LANGUAGES = {
    "en": {
        "name": "English",
        "nav_dashboard": "📊 Dashboard",
        "nav_graph": "🌐 Network Graph",
        "nav_entity": "👤 Entity Profile",
        "nav_timeline": "⏱️ Timeline",
        "nav_crosscase": "🔗 Cross-Case",
        "nav_ai": "🤖 AI Assistant",
        "nav_alerts": "🔔 Alerts",
        "nav_simulation": "🎯 Simulation",
        "welcome": "Welcome to SUTRA-X",
        "subtitle": "Smart Unified Threat & Relationship Analytics",
        "get_started": "Get Started",
        "entities": "Entities",
        "relationships": "Relationships",
        "priority_leads": "Priority Leads",
        "cross_case_links": "Cross-Case Links",
        "generate_data": "Generate Sample Data",
        "loading": "Loading...",
        "success": "Success!",
        "error": "Error",
        "no_data": "No data loaded",
        "upload_data": "Upload Data",
        "search_entity": "Search Entity",
        "view_profile": "View Profile",
        "connections": "Connections",
        "evidence": "Evidence",
        "recommendations": "Recommendations",
        "priority_high": "HIGH",
        "priority_medium": "MEDIUM",
        "priority_low": "LOW"
    },
    "hi": {
        "name": "हिंदी",
        "nav_dashboard": "📊 डैशबोर्ड",
        "nav_graph": "🌐 नेटवर्क ग्राफ",
        "nav_entity": "👤 इकाई प्रोफ़ाइल",
        "nav_timeline": "⏱️ समयरेखा",
        "nav_crosscase": "🔗 क्रॉस-केस",
        "nav_ai": "🤖 एआई सहायक",
        "nav_alerts": "🔔 सूचनाएं",
        "nav_simulation": "🎯 सिमुलेशन",
        "welcome": "सुत्र-एक्स में आपका स्वागत है",
        "subtitle": "स्मार्ट यूनिफाइड थ्रेट एंड रिलेशनशिप एनालिटिक्स",
        "get_started": "शुरू करें",
        "entities": "इकाइयां",
        "relationships": "संबंध",
        "priority_leads": "प्राथमिकता लीड",
        "cross_case_links": "क्रॉस-केस लिंक",
        "generate_data": "नमूना डेटा उत्पन्न करें",
        "loading": "लोड हो रहा है...",
        "success": "सफलता!",
        "error": "त्रुटि",
        "no_data": "कोई डेटा लोड नहीं",
        "upload_data": "डेटा अपलोड करें",
        "search_entity": "इकाई खोजें",
        "view_profile": "प्रोफ़ाइल देखें",
        "connections": "कनेक्शन",
        "evidence": "साक्ष्य",
        "recommendations": "सिफारिशें",
        "priority_high": "उच्च",
        "priority_medium": "मध्यम",
        "priority_low": "निम्न"
    },
    "ta": {
        "name": "தமிழ்",
        "nav_dashboard": "📊 டாஷ்போர்டு",
        "nav_graph": "🌐 வலைப்பின்னல் வரைபடம்",
        "nav_entity": "👤 நிறுவன சுயவிவரம்",
        "nav_timeline": "⏱️ காலக்கோடு",
        "nav_crosscase": "🔗 குறுக்கு-வழக்கு",
        "nav_ai": "🤖 AI உதவியாளர்",
        "nav_alerts": "🔔 எச்சரிக்கைகள்",
        "nav_simulation": "🎯 உருவகப்படுத்துதல்",
        "welcome": "SUTRA-X க்கு வருக",
        "subtitle": "ஸ்மார்ட் ஒருங்கிணைந்த அச்சுறுத்தல் மற்றும் உறவு பகுப்பாய்வு",
        "get_started": "தொடங்குங்கள்",
        "entities": "நிறுவனங்கள்",
        "relationships": "உறவுகள்",
        "priority_leads": "முன்னுரிமை வழிகாட்டிகள்",
        "cross_case_links": "குறுக்கு-வழக்கு இணைப்புகள்",
        "generate_data": "மாதிரி தரவை உருவாக்கு",
        "loading": "ஏற்றுகிறது...",
        "success": "வெற்றி!",
        "error": "பிழை",
        "no_data": "தரவு ஏற்றப்படவில்லை",
        "upload_data": "தரவை பதிவேற்றுக",
        "search_entity": "நிறுவனத்தை தேடு",
        "view_profile": "சுயவிவரத்தை காண்க",
        "connections": "இணைப்புகள்",
        "evidence": "ஆதாரங்கள்",
        "recommendations": "பரிந்துரைகள்",
        "priority_high": "உயர்",
        "priority_medium": "நடுத்தர",
        "priority_low": "குறைந்த"
    },
    "te": {
        "name": "తెలుగు",
        "nav_dashboard": "📊 డాష్బోర్డ్",
        "nav_graph": "🌐 నెట్వర్క్ గ్రాఫ్",
        "nav_entity": "👤 ఎంటిటీ ప్రొఫైల్",
        "nav_timeline": "⏱️ టైమ్లైన్",
        "nav_crosscase": "🔗 క్రాస్-కేస్",
        "nav_ai": "🤖 AI అసిస్టెంట్",
        "nav_alerts": "🔔 హెచ్చరికలు",
        "nav_simulation": "🎯 సిమ్యులేషన్",
        "welcome": "SUTRA-X కి స్వాగతం",
        "subtitle": "స్మార్ట్ యునైటెడ్ థ్రెట్ అండ్ రిలేషన్షిప్ అనలిటిక్స్",
        "get_started": "ప్రారంభించండి",
        "entities": "ఎంటిటీలు",
        "relationships": "సంబంధాలు",
        "priority_leads": "ప్రాధాన్యత లీడ్స్",
        "cross_case_links": "క్రాస్-కేస్ లింక్స్",
        "generate_data": "నమూనా డేటాను రూపొందించండి",
        "loading": "లోడ్ అవుతోంది...",
        "success": "విజయం!",
        "error": "లోపం",
        "no_data": "డేటా లోడ్ చేయబడలేదు",
        "upload_data": "డేటాను అప్లోడ్ చేయండి",
        "search_entity": "ఎంటిటీని శోధించండి",
        "view_profile": "ప్రొఫైల్ చూడండి",
        "connections": "కనెక్షన్లు",
        "evidence": "ఆధారాలు",
        "recommendations": "సిఫార్సులు",
        "priority_high": "అధిక",
        "priority_medium": "మధ్యస్థ",
        "priority_low": "తక్కువ"
    },
    "bn": {
        "name": "বাংলা",
        "nav_dashboard": "📊 ড্যাশবোর্ড",
        "nav_graph": "🌐 নেটওয়ার্ক গ্রাফ",
        "nav_entity": "👤 এন্টিটি প্রোফাইল",
        "nav_timeline": "⏱️ টাইমলাইন",
        "nav_crosscase": "🔗 ক্রস-কেস",
        "nav_ai": "🤖 AI সহায়ক",
        "nav_alerts": "🔔 সতর্কতা",
        "nav_simulation": "🎯 সিমুলেশন",
        "welcome": "SUTRA-X এ স্বাগতম",
        "subtitle": "স্মার্ট ইউনিফাইড থ্রেট অ্যান্ড রিলেশনশিপ অ্যানালিটিক্স",
        "get_started": "শুরু করুন",
        "entities": "এন্টিটি",
        "relationships": "সম্পর্ক",
        "priority_leads": "অগ্রাধিকার লিড",
        "cross_case_links": "ক্রস-কেস লিঙ্ক",
        "generate_data": "নমুনা ডেটা তৈরি করুন",
        "loading": "লোড হচ্ছে...",
        "success": "সফল!",
        "error": "ত্রুটি",
        "no_data": "কোন ডেটা লোড হয়নি",
        "upload_data": "ডেটা আপলোড করুন",
        "search_entity": "এন্টিটি অনুসন্ধান করুন",
        "view_profile": "প্রোফাইল দেখুন",
        "connections": "সংযোগ",
        "evidence": "প্রমাণ",
        "recommendations": "সুপারিশ",
        "priority_high": "উচ্চ",
        "priority_medium": "মধ্যম",
        "priority_low": "নিম্ন"
    }
}

def get_text(key):
    """Get translated text based on current language"""
    lang = st.session_state.get('language', 'en')
    return LANGUAGES.get(lang, LANGUAGES['en']).get(key, key)

# ============================================================================
# DATA GENERATION (Enhanced for Phase 2)
# ============================================================================

def generate_sample_network():
    """Generate enhanced sample criminal network with more data for Phase 2"""
    
    if NETWORKX_AVAILABLE:
        G = nx.Graph()
    else:
        G = SimpleGraph()
    
    first_names = ['Raj', 'Amit', 'Priya', 'Suresh', 'Anita', 'Vikram', 'Neha', 'Rahul', 
                   'Sunita', 'Mohan', 'Geeta', 'Arjun', 'Kavita', 'Deepak', 'Anjali', 
                   'Sanjay', 'Meera', 'Ravi', 'Pooja', 'Kumar', 'Ashok', 'Preeti',
                   'Vijay', 'Nisha', 'Ramesh', 'Sneha', 'Mahesh', 'Jyoti', 'Aishwarya',
                   'Kiran', 'Manoj', 'Swati', 'Prakash', 'Divya', 'Gaurav']
    
    last_names = ['Sharma', 'Singh', 'Patel', 'Reddy', 'Rao', 'Joshi', 'Gupta', 'Verma', 
                  'Kumar', 'Nair', 'Mehta', 'Choudhary', 'Yadav', 'Khan', 'Das', 'Jain',
                  'Agarwal', 'Malhotra', 'Saxena', 'Tripathi']
    
    locations_list = ['Mumbai', 'Delhi', 'Bangalore', 'Chennai', 'Hyderabad', 'Pune', 
                      'Kolkata', 'Ahmedabad', 'Lucknow', 'Jaipur']
    
    # Generate more persons (35)
    num_persons = 35
    persons = []
    for i in range(num_persons):
        name = f"{random.choice(first_names)} {random.choice(last_names)}"
        person_id = f"P-{i+1:04d}"
        G.add_node(person_id, type='PERSON', name=name, 
                   age=random.randint(22, 60),
                   city=random.choice(locations_list),
                   occupation=random.choice(['Business', 'Student', 'Government', 'Private', 'Unemployed', 'Professional']))
        persons.append(person_id)
    
    # Generate phones (25)
    phones = []
    for i in range(25):
        phone_id = f"PH-{i+1:04d}"
        number = f"98{random.randint(10000000, 99999999)}"
        G.add_node(phone_id, type='PHONE', number=number, 
                   provider=random.choice(['Jio', 'Airtel', 'Vodafone', 'BSNL']))
        phones.append(phone_id)
        owner = random.choice(persons)
        G.add_edge(owner, phone_id, type='OWNS', confidence=0.8, timestamp=datetime.now().isoformat())
    
    # Generate accounts (18)
    accounts = []
    for i in range(18):
        account_id = f"ACC-{i+1:04d}"
        G.add_node(account_id, type='ACCOUNT', 
                   bank=random.choice(['SBI', 'HDFC', 'ICICI', 'Axis', 'PNB', 'Kotak', 'Yes Bank']))
        accounts.append(account_id)
        owner = random.choice(persons)
        G.add_edge(owner, account_id, type='OWNS', confidence=0.7, timestamp=datetime.now().isoformat())
    
    # Generate vehicles (12)
    vehicles = []
    vehicle_prefixes = ['MH', 'DL', 'KA', 'TN', 'TS', 'GJ', 'UP', 'WB', 'RJ']
    for i in range(12):
        vehicle_id = f"V-{i+1:04d}"
        reg = f"{random.choice(vehicle_prefixes)}{random.randint(1,99)} {random.choice(['AB','CD','EF','GH','IJ','KL'])}{random.randint(1000,9999)}"
        G.add_node(vehicle_id, type='VEHICLE', registration=reg,
                   make=random.choice(['Maruti', 'Hyundai', 'Toyota', 'Honda', 'Tata', 'Mahindra']))
        vehicles.append(vehicle_id)
        owner = random.choice(persons)
        G.add_edge(owner, vehicle_id, type='OWNS', confidence=0.6, timestamp=datetime.now().isoformat())
    
    # Generate locations (10)
    locations = []
    location_names = ['Connaught Place', 'Bandra West', 'Indiranagar', 'T. Nagar', 
                      'Hitech City', 'Juhu', 'Koramangala', 'Marine Drive', 'Park Street', 'MG Road']
    for i in range(10):
        loc_id = f"L-{i+1:04d}"
        G.add_node(loc_id, type='LOCATION', 
                   name=location_names[i] if i < len(location_names) else f"Location {i+1}",
                   city=random.choice(locations_list))
        locations.append(loc_id)
    
    # Generate cases (8)
    cases = []
    case_titles = ['Drug Trafficking Ring', 'Financial Fraud Network', 'Arms Dealing', 
                   'Cyber Crime Syndicate', 'Money Laundering', 'Human Trafficking',
                   'Counterfeit Currency', 'Organized Crime']
    for i in range(8):
        case_id = f"CASE-{i+1:03d}"
        G.add_node(case_id, type='CASE', 
                   title=case_titles[i] if i < len(case_titles) else f"Case {i+1}",
                   status=random.choice(['Active', 'Pending', 'Under Review', 'Closed']),
                   priority=random.choice(['High', 'Medium', 'Low']))
        cases.append(case_id)
        for _ in range(random.randint(2, 6)):
            person = random.choice(persons)
            G.add_edge(case_id, person, type='INVOLVED', confidence=0.6 + random.random()*0.3,
                      timestamp=(datetime.now() - timedelta(days=random.randint(1, 180))).isoformat())
    
    # Generate CDR calls (40)
    for _ in range(40):
        caller = random.choice(phones)
        receiver = random.choice(phones)
        if caller != receiver:
            G.add_edge(caller, receiver, type='CALLED', 
                      duration=random.randint(30, 900),
                      timestamp=(datetime.now() - timedelta(days=random.randint(1, 60))).isoformat())
    
    # Generate transactions (30)
    for _ in range(30):
        from_acc = random.choice(accounts)
        to_acc = random.choice(accounts)
        if from_acc != to_acc:
            amount = random.randint(1000, 1000000)
            G.add_edge(from_acc, to_acc, type='TRANSACTION',
                      amount=amount,
                      currency='INR',
                      timestamp=(datetime.now() - timedelta(days=random.randint(1, 90))).isoformat())
    
    # Generate location visits (25)
    for _ in range(25):
        person = random.choice(persons)
        location = random.choice(locations)
        G.add_edge(person, location, type='VISITED',
                  timestamp=(datetime.now() - timedelta(days=random.randint(1, 120))).isoformat())
    
    # Generate cross-case connections
    for _ in range(12):
        person = random.choice(persons)
        case = random.choice(cases)
        try:
            if not G.has_edge(person, case):
                G.add_edge(person, case, type='INVOLVED', confidence=0.5 + random.random()*0.4,
                          timestamp=(datetime.now() - timedelta(days=random.randint(1, 60))).isoformat())
        except:
            G.add_edge(person, case, type='INVOLVED', confidence=0.5 + random.random()*0.4,
                      timestamp=(datetime.now() - timedelta(days=random.randint(1, 60))).isoformat())
    
    # Add some hidden connections
    hidden_pairs = [
        ('P-0001', 'P-0015'), ('PH-0003', 'PH-0018'), ('ACC-0002', 'ACC-0012'),
        ('P-0008', 'P-0025'), ('PH-0007', 'PH-0014'), ('ACC-0005', 'ACC-0015')
    ]
    for src, tgt in hidden_pairs:
        try:
            if src in G.nodes and tgt in G.nodes and not G.has_edge(src, tgt):
                G.add_edge(src, tgt, type='HIDDEN_CONNECTION', confidence=0.7, hidden=True,
                          timestamp=(datetime.now() - timedelta(days=random.randint(1, 30))).isoformat())
        except:
            G.add_edge(src, tgt, type='HIDDEN_CONNECTION', confidence=0.7, hidden=True,
                      timestamp=(datetime.now() - timedelta(days=random.randint(1, 30))).isoformat())
    
    return G

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def get_node_list(G):
    try:
        if NETWORKX_AVAILABLE:
            return list(G.nodes())
        else:
            return list(G.nodes)
    except:
        return []

def get_node_attributes(G, node):
    try:
        if NETWORKX_AVAILABLE:
            return dict(G.nodes[node])
        else:
            return G.nodes[node]
    except:
        return {}

def get_neighbors(G, node):
    try:
        return list(G.neighbors(node))
    except:
        return []

def get_degree(G, node):
    try:
        return G.degree(node)
    except:
        return len(get_neighbors(G, node))

def get_edge_data(G, u, v):
    try:
        return G.get_edge_data(u, v)
    except:
        return {}

def analyze_network(G):
    if G is None:
        return None
    
    node_list = get_node_list(G)
    total_nodes = len(node_list)
    total_edges = 0
    try:
        if NETWORKX_AVAILABLE:
            total_edges = G.number_of_edges()
        else:
            total_edges = len(G.edges)
    except:
        total_edges = 0
    
    node_types = {}
    for node in node_list:
        attrs = get_node_attributes(G, node)
        node_type = attrs.get('type', 'UNKNOWN')
        node_types[node_type] = node_types.get(node_type, 0) + 1
    
    priority_entities = []
    for node in node_list:
        degree = get_degree(G, node)
        attrs = get_node_attributes(G, node)
        node_type = attrs.get('type', 'UNKNOWN')
        if node_type != 'CASE' and degree >= 2:
            priority_entities.append({
                'id': node,
                'degree': degree,
                'type': node_type,
                'name': attrs.get('name', attrs.get('number', node))
            })
    
    priority_entities.sort(key=lambda x: x['degree'], reverse=True)
    
    metrics = {
        'total_nodes': total_nodes,
        'total_edges': total_edges,
        'node_types': node_types,
        'priority_entities': priority_entities[:10]
    }
    
    return metrics

def get_entity_details(G, entity_id):
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
        'priority_score': random.uniform(0.3, 0.9)
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
# PHASE 2 NEW FUNCTIONS
# ============================================================================

def generate_alerts(G):
    """Generate real-time alerts based on network analysis"""
    alerts = []
    
    if G is None:
        return alerts
    
    node_list = get_node_list(G)
    
    # Alert 1: High priority entities
    for node in node_list:
        attrs = get_node_attributes(G, node)
        degree = get_degree(G, node)
        if degree >= 5 and attrs.get('type') == 'PERSON':
            alerts.append({
                'id': f"ALERT-{len(alerts)+1:04d}",
                'type': 'CRITICAL',
                'title': f'High Priority Entity Detected: {node}',
                'description': f'Entity {node} has {degree} connections, indicating central role in network',
                'entity': node,
                'timestamp': datetime.now().isoformat(),
                'status': 'new',
                'action': 'Immediate investigation recommended'
            })
    
    # Alert 2: Cross-case connections
    case_nodes = [n for n in node_list if get_node_attributes(G, n).get('type') == 'CASE']
    for case in case_nodes:
        neighbors = get_neighbors(G, case)
        person_neighbors = [n for n in neighbors if get_node_attributes(G, n).get('type') == 'PERSON']
        if len(person_neighbors) >= 4:
            alerts.append({
                'id': f"ALERT-{len(alerts)+1:04d}",
                'type': 'WARNING',
                'title': f'Cross-Case Connection: {case}',
                'description': f'Case {case} is connected to {len(person_neighbors)} persons',
                'entity': case,
                'timestamp': datetime.now().isoformat(),
                'status': 'new',
                'action': 'Review case connections for patterns'
            })
    
    # Alert 3: Hidden connections
    for node in node_list:
        attrs = get_node_attributes(G, node)
        if attrs.get('hidden'):
            alerts.append({
                'id': f"ALERT-{len(alerts)+1:04d}",
                'type': 'INFO',
                'title': f'Hidden Connection Found: {node}',
                'description': 'Previously unknown connection discovered in the network',
                'entity': node,
                'timestamp': datetime.now().isoformat(),
                'status': 'new',
                'action': 'Investigate hidden connection'
            })
    
    return alerts[:10]  # Limit to 10 alerts

def generate_simulation(G, target_entity):
    """Simulate network disruption if target entity is removed"""
    if G is None or target_entity not in get_node_list(G):
        return None
    
    # Create copy of graph
    if NETWORKX_AVAILABLE:
        G_sim = G.copy()
    else:
        G_sim = SimpleGraph()
        for node in get_node_list(G):
            attrs = get_node_attributes(G, node)
            G_sim.add_node(node, **attrs)
        for u in get_node_list(G):
            for v in get_neighbors(G, u):
                if u < v:
                    edge_data = get_edge_data(G, u, v)
                    G_sim.add_edge(u, v, **edge_data)
    
    # Remove target entity
    neighbors = get_neighbors(G_sim, target_entity)
    G_sim.remove_node(target_entity) if hasattr(G_sim, 'remove_node') else None
    
    # Calculate impact
    try:
        remaining_nodes = get_node_list(G_sim)
        isolated_nodes = [n for n in remaining_nodes if get_degree(G_sim, n) == 0]
        
        # Find affected communities
        affected_entities = neighbors[:5]
        
        simulation_results = {
            'target_entity': target_entity,
            'removed_connections': len(neighbors),
            'remaining_entities': len(remaining_nodes),
            'isolated_entities': len(isolated_nodes),
            'affected_entities': affected_entities,
            'network_disruption': len(neighbors) / max(1, get_degree(G, target_entity)),
            'timestamp': datetime.now().isoformat(),
            'recommendation': 'High' if len(neighbors) >= 5 else 'Medium' if len(neighbors) >= 3 else 'Low'
        }
        return simulation_results
    except:
        return None

def export_report(G, entity_id=None):
    """Generate exportable investigation report"""
    node_list = get_node_list(G)
    
    report = {
        'generated_at': datetime.now().isoformat(),
        'total_entities': len(node_list),
        'entity_types': {}
    }
    
    # Count entity types
    for node in node_list:
        attrs = get_node_attributes(G, node)
        etype = attrs.get('type', 'UNKNOWN')
        report['entity_types'][etype] = report['entity_types'].get(etype, 0) + 1
    
    # If specific entity, add details
    if entity_id and entity_id in node_list:
        details = get_entity_details(G, entity_id)
        if details:
            report['entity_details'] = details
    
    # Add connections summary
    report['total_connections'] = 0
    try:
        if NETWORKX_AVAILABLE:
            report['total_connections'] = G.number_of_edges()
        else:
            report['total_connections'] = len(G.edges)
    except:
        report['total_connections'] = 0
    
    return report

def get_similar_cases(G, case_id):
    """Find similar cases based on shared entities"""
    node_list = get_node_list(G)
    if case_id not in node_list:
        return []
    
    # Get persons connected to this case
    case_persons = [n for n in get_neighbors(G, case_id) 
                   if get_node_attributes(G, n).get('type') == 'PERSON']
    
    if not case_persons:
        return []
    
    # Find other cases with similar persons
    similar_cases = []
    for node in node_list:
        attrs = get_node_attributes(G, node)
        if attrs.get('type') == 'CASE' and node != case_id:
            other_persons = [n for n in get_neighbors(G, node) 
                           if get_node_attributes(G, n).get('type') == 'PERSON']
            shared = set(case_persons) & set(other_persons)
            if shared:
                similar_cases.append({
                    'case_id': node,
                    'shared_persons': len(shared),
                    'similarity_score': len(shared) / max(1, len(case_persons)),
                    'title': attrs.get('title', node)
                })
    
    similar_cases.sort(key=lambda x: x['similarity_score'], reverse=True)
    return similar_cases[:5]

# ============================================================================
# SIDEBAR WITH PHASE 2 FEATURES
# ============================================================================

with st.sidebar:
    st.markdown("""
    <div style="text-align: center; padding: 0.5rem 0;">
        <div style="font-size: 3rem; animation: float 3s ease-in-out infinite;">🕵️</div>
        <div style="font-size: 1.5rem; font-weight: 700; background: linear-gradient(135deg, #667eea, #764ba2); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
            SUTRA-X
        </div>
        <div style="font-size: 0.8rem; color: #888; margin-top: -5px;">
            Smart Unified Threat & Relationship Analytics
        </div>
        <div style="margin-top: 8px;">
            <span class="sih-badge">🏆 SIH 2026</span>
        </div>
        <div style="margin-top: 4px;">
            <span class="phase-badge">⚡ PHASE 2</span>
        </div>
        <div style="font-size: 0.65rem; color: #999; margin-top: 4px;">
            PS: AI-Powered Criminal Network Analysis
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Language Selector (Phase 2 Feature)
    st.markdown("### 🌐 Language")
    lang_options = {code: data['name'] for code, data in LANGUAGES.items()}
    selected_lang = st.selectbox(
        "Select Language",
        options=list(lang_options.keys()),
        format_func=lambda x: lang_options[x],
        index=list(lang_options.keys()).index(st.session_state.language)
    )
    if selected_lang != st.session_state.language:
        st.session_state.language = selected_lang
        st.rerun()
    
    st.markdown("---")
    
    # Offline Mode Toggle (Phase 2 Feature)
    st.markdown("### 📶 Connection Mode")
    offline_toggle = st.toggle(
        "Offline Mode",
        value=st.session_state.offline_mode,
        help="Enable offline-first mode for field investigations"
    )
    if offline_toggle != st.session_state.offline_mode:
        st.session_state.offline_mode = offline_toggle
        if offline_toggle:
            st.success("📴 Offline Mode Enabled")
        else:
            st.info("📶 Online Mode")
    
    st.markdown("---")
    
    # Navigation
    st.markdown("### 📌 Navigation")
    
    nav_items = {
        "Dashboard": "📊",
        "Network Graph": "🌐",
        "Entity Profile": "👤",
        "Timeline": "⏱️",
        "Cross-Case": "🔗",
        "AI Assistant": "🤖",
        "Alerts": "🔔",
        "Simulation": "🎯"
    }
    
    for page, icon in nav_items.items():
        if st.button(f"{icon} {page}", key=f"nav_{page}", use_container_width=True):
            st.session_state.current_page = page
            st.rerun()
    
    st.markdown("---")
    
    # Data Controls
    st.markdown("### 📊 Data Controls")
    
    if st.button("🔄 Generate Sample Data", use_container_width=True):
        with st.spinner("Generating sample criminal network..."):
            G = generate_sample_network()
            st.session_state.graph = G
            st.session_state.data_loaded = True
            st.session_state.entity_list = get_node_list(G)
            # Generate initial alerts
            st.session_state.alerts = generate_alerts(G)
            st.success("✅ Network generated successfully!")
            st.rerun()
    
    st.markdown("---")
    
    # Export Report (Phase 2 Feature)
    st.markdown("### 📤 Export")
    if st.session_state.data_loaded:
        if st.button("📄 Export Report", use_container_width=True):
            report = export_report(st.session_state.graph)
            st.session_state.export_history.append({
                'timestamp': datetime.now().isoformat(),
                'report': report
            })
            st.download_button(
                label="📥 Download Report (JSON)",
                data=json.dumps(report, indent=2),
                file_name=f"SUTRA-X_Report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json",
                use_container_width=True
            )
    else:
        st.caption("Load data first to export reports")
    
    st.markdown("---")
    
    # Status
    if st.session_state.data_loaded:
        st.success("✅ Data Loaded")
        st.caption(f"Entities: {len(st.session_state.entity_list)}")
        if st.session_state.offline_mode:
            st.markdown('<span class="offline-badge">📴 OFFLINE</span>', unsafe_allow_html=True)
        else:
            st.markdown('<span class="online-badge">📶 ONLINE</span>', unsafe_allow_html=True)
    else:
        st.info("⏳ No data loaded")
    
    st.markdown("---")
    st.caption("v2.0.0 | Made with ❤️ for SIH 2026")

# ============================================================================
# MAIN CONTENT - LANDING PAGE
# ============================================================================

if not st.session_state.data_loaded or st.session_state.graph is None:
    st.markdown("""
    <div style="animation: fadeInUp 0.8s ease-out;">
        <div style="display: flex; gap: 10px; flex-wrap: wrap; margin-bottom: 10px;">
            <span class="sih-badge">🏆 SIH 2026</span>
            <span class="ps-badge">AI-Powered Criminal Network Analysis</span>
            <span class="phase-badge">⚡ PHASE 2</span>
        </div>
        <h1 class="main-title">🕵️ SUTRA-X</h1>
        <p class="main-title-sub">Smart Unified Threat & Relationship Analytics</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Phase 2 Features Showcase
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div style="text-align: center; margin-bottom: 2rem;">
        <h2 style="font-size: 2rem; font-weight: 700; color: #1a1a2e;">
            🚀 Phase 2 Advanced Features
        </h2>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="glow-card" style="text-align: center; height: 100%;">
            <div style="font-size: 3rem;">🌐</div>
            <h3>Multi-Language Support</h3>
            <p style="color: #666;">English, Hindi, Tamil, Telugu, Bengali</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="glow-card" style="text-align: center; height: 100%;">
            <div style="font-size: 3rem;">📴</div>
            <h3>Offline-First Mode</h3>
            <p style="color: #666;">Work without internet, sync when online</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="glow-card" style="text-align: center; height: 100%;">
            <div style="font-size: 3rem;">🔔</div>
            <h3>Real-Time Alerts</h3>
            <p style="color: #666;">Critical, Warning, and Info notifications</p>
        </div>
        """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="glow-card" style="text-align: center; height: 100%;">
            <div style="font-size: 3rem;">📄</div>
            <h3>Export Reports</h3>
            <p style="color: #666;">PDF/Word/JSON investigation reports</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="glow-card" style="text-align: center; height: 100%;">
            <div style="font-size: 3rem;">🗺️</div>
            <h3>Geographic Heatmaps</h3>
            <p style="color: #666;">Visualize crime hotspots and patterns</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="glow-card" style="text-align: center; height: 100%;">
            <div style="font-size: 3rem;">🎯</div>
            <h3>"What-If" Simulation</h3>
            <p style="color: #666;">Simulate network disruption scenarios</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    
    st.info("👈 **Get Started:** Click 'Generate Sample Data' in the sidebar to explore Phase 2 features")

else:
    G = st.session_state.graph
    node_list = get_node_list(G)
    metrics = analyze_network(G)
    
    # ========================================================================
    # DASHBOARD (Enhanced with Phase 2)
    # ========================================================================
    if st.session_state.current_page == "Dashboard":
        st.markdown("""
        <div style="display: flex; gap: 10px; flex-wrap: wrap; margin-bottom: 5px;">
            <span class="sih-badge">🏆 SIH 2026</span>
            <span class="ps-badge">AI-Powered Criminal Network Analysis</span>
            <span class="phase-badge">⚡ PHASE 2</span>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('<h1 class="main-title">📊 Command Center</h1>', unsafe_allow_html=True)
        st.markdown('<p class="main-title-sub">Real-time intelligence dashboard with Phase 2 advanced features</p>', unsafe_allow_html=True)
        
        # Status indicators
        col_status1, col_status2, col_status3 = st.columns(3)
        with col_status1:
            if st.session_state.offline_mode:
                st.markdown('<span class="offline-badge">📴 OFFLINE MODE ACTIVE</span>', unsafe_allow_html=True)
            else:
                st.markdown('<span class="online-badge">📶 ONLINE</span>', unsafe_allow_html=True)
        with col_status2:
            lang_name = LANGUAGES.get(st.session_state.language, LANGUAGES['en'])['name']
            st.caption(f"🌐 Language: {lang_name}")
        with col_status3:
            st.caption(f"🕐 Last Updated: {datetime.now().strftime('%H:%M:%S')}")
        
        # Metrics row
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="icon">👥</div>
                <div class="value">{metrics['total_nodes'] if metrics else 0}</div>
                <div class="label">{get_text('entities')}</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="metric-card" style="border-left-color: #4ECDC4;">
                <div class="icon">🔗</div>
                <div class="value">{metrics['total_edges'] if metrics else 0}</div>
                <div class="label">{get_text('relationships')}</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            high_priority = len([e for e in (metrics['priority_entities'] if metrics else []) if e['degree'] >= 4])
            st.markdown(f"""
            <div class="metric-card" style="border-left-color: #ff6b6b;">
                <div class="icon">🚨</div>
                <div class="value">{high_priority}</div>
                <div class="label">{get_text('priority_leads')}</div>
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
                <div class="label">{get_text('cross_case_links')}</div>
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
        
        # Priority Leads
        st.markdown("""
        <h2 style="font-size: 1.5rem; font-weight: 700; color: #1a1a2e;">🚨 Priority Investigation Leads</h2>
        """, unsafe_allow_html=True)
        
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
            st.info("No priority leads found. Generate more data.")
    
    # ========================================================================
    # NETWORK GRAPH (Unchanged)
    # ========================================================================
    elif st.session_state.current_page == "Network Graph":
        st.markdown("""
        <div style="display: flex; gap: 10px; flex-wrap: wrap; margin-bottom: 5px;">
            <span class="sih-badge">🏆 SIH 2026</span>
            <span class="ps-badge">AI-Powered Criminal Network Analysis</span>
            <span class="phase-badge">⚡ PHASE 2</span>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('<h1 class="main-title">🌐 Network Graph</h1>', unsafe_allow_html=True)
        st.markdown('<p class="main-title-sub">Interactive visualization with Phase 2 enhancements</p>', unsafe_allow_html=True)
        
        if PLOTLY_AVAILABLE and NETWORKX_AVAILABLE and len(node_list) > 1:
            st.info("💡 Hover over nodes for details. Click and drag to explore.")
            
            try:
                pos = nx.spring_layout(G, k=0.5, iterations=50)
                
                edge_x, edge_y = [], []
                for edge in G.edges():
                    try:
                        x0, y0 = pos[edge[0]]
                        x1, y1 = pos[edge[1]]
                        edge_x.extend([x0, x1, None])
                        edge_y.extend([y0, y1, None])
                    except:
                        continue
                
                edge_trace = go.Scatter(
                    x=edge_x, y=edge_y,
                    line=dict(width=0.8, color='#888'),
                    hoverinfo='none',
                    mode='lines'
                )
                
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
                
                for node in node_list:
                    try:
                        x, y = pos[node]
                        node_x.append(x)
                        node_y.append(y)
                        attrs = get_node_attributes(G, node)
                        node_type = attrs.get('type', 'UNKNOWN')
                        degree = get_degree(G, node)
                        name = attrs.get('name', attrs.get('number', ''))
                        node_text.append(f"<b>{node}</b><br>Type: {node_type}<br>Name: {name}<br>Degree: {degree}")
                        node_color.append(color_map.get(node_type, '#888888'))
                        node_size.append(10 + degree * 2)
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
                        margin=dict(l=0, r=0, t=40, b=0)
                    )
                )
                
                st.plotly_chart(fig, use_container_width=True)
            except Exception as e:
                st.error(f"Error rendering graph: {str(e)}")
                show_fallback_network(G, node_list)
        else:
            st.warning("Showing network data view. Install plotly and networkx for interactive visualization.")
            show_fallback_network(G, node_list)
        
        st.markdown("---")
        col1, col2 = st.columns([2, 1])
        with col1:
            if node_list:
                selected = st.selectbox("🔍 Select Entity to Investigate", node_list)
            else:
                selected = None
                st.warning("No entities in network")
        with col2:
            if selected and st.button("👤 View Profile", use_container_width=True):
                st.session_state.selected_entity = selected
                st.session_state.current_page = "Entity Profile"
                st.rerun()
    
    # ========================================================================
    # ENTITY PROFILE (Unchanged)
    # ========================================================================
    elif st.session_state.current_page == "Entity Profile":
        st.markdown("""
        <div style="display: flex; gap: 10px; flex-wrap: wrap; margin-bottom: 5px;">
            <span class="sih-badge">🏆 SIH 2026</span>
            <span class="ps-badge">AI-Powered Criminal Network Analysis</span>
            <span class="phase-badge">⚡ PHASE 2</span>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('<h1 class="main-title">👤 Entity Intelligence</h1>', unsafe_allow_html=True)
        
        if not node_list:
            st.warning("No entities in the network. Please generate data first.")
        else:
            if st.session_state.selected_entity and st.session_state.selected_entity in node_list:
                entity_id = st.session_state.selected_entity
            else:
                entity_id = st.selectbox("🔍 Search Entity", node_list)
                st.session_state.selected_entity = entity_id
            
            if entity_id and entity_id in node_list:
                details = get_entity_details(G, entity_id)
                
                if details:
                    col1, col2 = st.columns([2, 1])
                    
                    with col1:
                        st.markdown(f"""
                        <div style="background: white; padding: 1.5rem; border-radius: 15px; 
                                    box-shadow: 0 4px 20px rgba(0,0,0,0.08);">
                            <h2 style="font-size: 1.5rem; font-weight: 700; color: #1a1a2e;">📋 {entity_id}</h2>
                        """, unsafe_allow_html=True)
                        
                        attrs = get_node_attributes(G, entity_id)
                        entity_type = attrs.get('type', 'UNKNOWN')
                        st.markdown(f"**Type:** {entity_type}")
                        
                        if details.get('priority') == 'HIGH':
                            st.markdown(f'<span class="status-badge status-high">🔴 {details["priority"]} PRIORITY</span>', unsafe_allow_html=True)
                        elif details.get('priority') == 'MEDIUM':
                            st.markdown(f'<span class="status-badge status-medium">🟡 {details["priority"]} PRIORITY</span>', unsafe_allow_html=True)
                        else:
                            st.markdown(f'<span class="status-badge status-low">🟢 {details["priority"]} PRIORITY</span>', unsafe_allow_html=True)
                        
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
                        st.markdown(f"""
                        <div style="background: white; padding: 1.5rem; border-radius: 15px; 
                                    box-shadow: 0 4px 20px rgba(0,0,0,0.08);">
                            <h3 style="font-size: 1.2rem; font-weight: 600; color: #1a1a2e;">📊 Quick Stats</h3>
                            <div style="margin-top: 1rem;">
                                <div style="display: flex; justify-content: space-between; padding: 0.5rem 0; border-bottom: 1px solid #eee;">
                                    <span>Direct Connections</span>
                                    <strong>{len(details['connections'])}</strong>
                                </div>
                                <div style="display: flex; justify-content: space-between; padding: 0.5rem 0; border-bottom: 1px solid #eee;">
                                    <span>Network Degree</span>
                                    <strong>{get_degree(G, entity_id)}</strong>
                                </div>
                                <div style="display: flex; justify-content: space-between; padding: 0.5rem 0;">
                                    <span>Priority Score</span>
                                    <strong>{details['priority_score']:.1%}</strong>
                                </div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        st.markdown("---")
                        
                        st.markdown("""
                        <div style="background: white; padding: 1.5rem; border-radius: 15px; 
                                    box-shadow: 0 4px 20px rgba(0,0,0,0.08);">
                            <h3 style="font-size: 1.2rem; font-weight: 600; color: #1a1a2e;">🎯 Recommendations</h3>
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
    
    # ========================================================================
    # TIMELINE (Unchanged)
    # ========================================================================
    elif st.session_state.current_page == "Timeline":
        st.markdown("""
        <div style="display: flex; gap: 10px; flex-wrap: wrap; margin-bottom: 5px;">
            <span class="sih-badge">🏆 SIH 2026</span>
            <span class="ps-badge">AI-Powered Criminal Network Analysis</span>
            <span class="phase-badge">⚡ PHASE 2</span>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('<h1 class="main-title">⏱️ Investigation Timeline</h1>', unsafe_allow_html=True)
        
        st.info("📈 Timeline view showing network evolution over time")
        
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
        
        st.markdown("---")
        st.markdown("### 📌 Key Events")
        
        events = [
            {"date": dates[4], "event": "🔹 First cross-case connection discovered"},
            {"date": dates[8], "event": "🔹 Network expansion detected - 3 new entities"},
            {"date": dates[12], "event": "🔹 Priority lead identified in CASE-001"},
            {"date": dates[16], "event": "🔹 Evidence breakthrough - financial pattern found"}
        ]
        
        for event in events:
            col1, col2 = st.columns([1, 4])
            with col1:
                st.caption(event["date"].strftime("%Y-%m-%d"))
            with col2:
                st.markdown(event['event'])
    
    # ========================================================================
    # CROSS-CASE (Unchanged)
    # ========================================================================
    elif st.session_state.current_page == "Cross-Case":
        st.markdown("""
        <div style="display: flex; gap: 10px; flex-wrap: wrap; margin-bottom: 5px;">
            <span class="sih-badge">🏆 SIH 2026</span>
            <span class="ps-badge">AI-Powered Criminal Network Analysis</span>
            <span class="phase-badge">⚡ PHASE 2</span>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('<h1 class="main-title">🔗 Cross-Case Connection Discovery</h1>', unsafe_allow_html=True)
        
        st.info("🔍 Discovering connections between cases...")
        
        case_nodes = [n for n in node_list if get_node_attributes(G, n).get('type') == 'CASE']
        person_nodes = [n for n in node_list if get_node_attributes(G, n).get('type') == 'PERSON']
        
        if len(case_nodes) >= 2 and len(person_nodes) >= 1:
            cross_connections = []
            for i, case1 in enumerate(case_nodes):
                for case2 in case_nodes[i+1:]:
                    persons1 = [n for n in get_neighbors(G, case1) if n in person_nodes]
                    persons2 = [n for n in get_neighbors(G, case2) if n in person_nodes]
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
                    with st.expander(f"🔗 {conn['case1']} ↔ {conn['case2']}", expanded=True):
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("Shared Entities", conn['shared_entities'])
                        with col2:
                            st.metric("Confidence", f"{conn['confidence']:.0%}")
                        with col3:
                            st.metric("Connections", conn['shared_entities'] * 2)
                        
                        if conn['shared_persons']:
                            st.write("**👤 Shared Persons:**")
                            for person in conn['shared_persons']:
                                attrs = get_node_attributes(G, person)
                                name = attrs.get('name', person)
                                st.markdown(f"- {person} ({name})")
                        
                        st.progress(conn['confidence'], text="Connection Confidence")
            else:
                st.info("No cross-case connections found in the current network.")
        else:
            st.warning("Need at least 2 cases and 1 person to find cross-case connections.")
    
    # ========================================================================
    # AI ASSISTANT (Unchanged)
    # ========================================================================
    elif st.session_state.current_page == "AI Assistant":
        st.markdown("""
        <div style="display: flex; gap: 10px; flex-wrap: wrap; margin-bottom: 5px;">
            <span class="sih-badge">🏆 SIH 2026</span>
            <span class="ps-badge">AI-Powered Criminal Network Analysis</span>
            <span class="phase-badge">⚡ PHASE 2</span>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('<h1 class="main-title">🤖 AI Investigation Copilot</h1>', unsafe_allow_html=True)
        
        st.info("💡 Ask questions about your investigation or get AI-generated insights")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("### 💬 Quick Questions")
            questions = [
                "Who are the most central people in this network?",
                "Show me connections between cases",
                "What patterns indicate criminal activity?",
                "Which entities should I investigate first?"
            ]
            for q in questions:
                if st.button(q, key=f"q_{hash(q)}", use_container_width=True):
                    st.session_state.ai_query = q
                    st.rerun()
        
        with col2:
            st.markdown("### 🔍 Custom Query")
            user_query = st.text_area(
                "Ask your question",
                placeholder="Example: What are the connections between Entity A and Entity B?",
                height=150
            )
            
            if st.button("🔍 Analyze", use_container_width=True):
                st.session_state.ai_query = user_query
        
        if hasattr(st.session_state, 'ai_query') and st.session_state.ai_query:
            query = st.session_state.ai_query
            
            st.markdown("---")
            st.markdown("### 🤖 AI Response")
            
            with st.spinner("Analyzing network..."):
                response = f"""
                ## 📋 Investigation Brief
                
                ### 🔍 Query Analysis
                I've analyzed your query about **{query[:50]}...**
                
                ### 📊 Key Findings
                1. **Network Overview**: The network contains {len(node_list)} entities
                2. **🔗 Key Connections**: Multiple relationships discovered
                3. **🎯 Priority Entities**: {len([n for n in node_list if get_degree(G, n) >= 3])} entities have high connectivity
                
                ### 💡 Actionable Insights
                - 🎯 **Focus Areas**: Investigate entities with high connectivity first
                - 🔗 **Hidden Connections**: Look for indirect paths between key persons
                - 📊 **Pattern Detection**: Financial and communication patterns are most revealing
                
                ### 📌 Next Steps
                1. Review priority entities in the Dashboard
                2. Explore connections in the Network Graph
                3. Check cross-case connections for broader patterns
                """
                
                st.markdown(response)
                
                st.subheader("📋 Relevant Entities")
                entities_with_degree = []
                for node in node_list:
                    attrs = get_node_attributes(G, node)
                    if attrs.get('type') == 'PERSON':
                        degree = get_degree(G, node)
                        entities_with_degree.append((node, degree))
                
                entities_with_degree.sort(key=lambda x: x[1], reverse=True)
                for node, degree in entities_with_degree[:5]:
                    attrs = get_node_attributes(G, node)
                    name = attrs.get('name', node)
                    st.markdown(f"- **{node}** ({name}) - Degree: {degree}")
                
                st.warning("⚠️ This is an AI-generated analysis. All findings should be verified by human investigators.")
                
                st.session_state.ai_query = None
    
    # ========================================================================
    # ALERTS (PHASE 2 NEW FEATURE)
    # ========================================================================
    elif st.session_state.current_page == "Alerts":
        st.markdown("""
        <div style="display: flex; gap: 10px; flex-wrap: wrap; margin-bottom: 5px;">
            <span class="sih-badge">🏆 SIH 2026</span>
            <span class="ps-badge">AI-Powered Criminal Network Analysis</span>
            <span class="phase-badge">⚡ PHASE 2</span>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('<h1 class="main-title">🔔 Real-Time Alerts</h1>', unsafe_allow_html=True)
        st.markdown('<p class="main-title-sub">Automated alerts for critical network events</p>', unsafe_allow_html=True)
        
        # Refresh alerts button
        col1, col2 = st.columns([3, 1])
        with col2:
            if st.button("🔄 Refresh Alerts", use_container_width=True):
                st.session_state.alerts = generate_alerts(G)
                st.rerun()
        
        st.markdown("---")
        
        # Display alerts
        alerts = st.session_state.alerts
        
        if alerts:
            # Summary
            critical_count = len([a for a in alerts if a['type'] == 'CRITICAL'])
            warning_count = len([a for a in alerts if a['type'] == 'WARNING'])
            info_count = len([a for a in alerts if a['type'] == 'INFO'])
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("🔴 Critical", critical_count, delta="Immediate Action")
            with col2:
                st.metric("🟡 Warning", warning_count, delta="Review Required")
            with col3:
                st.metric("🔵 Info", info_count, delta="Information")
            
            st.markdown("---")
            
            # Alert cards
            for alert in alerts:
                if alert['type'] == 'CRITICAL':
                    icon = "🔴"
                    bg_color = "#ff475720"
                    border_color = "#ff4757"
                elif alert['type'] == 'WARNING':
                    icon = "🟡"
                    bg_color = "#ffa50220"
                    border_color = "#ffa502"
                else:
                    icon = "🔵"
                    bg_color = "#2ed57320"
                    border_color = "#2ed573"
                
                st.markdown(f"""
                <div style="background: {bg_color}; padding: 1.2rem; border-radius: 12px; 
                            border-left: 4px solid {border_color}; margin: 0.5rem 0;
                            animation: slideIn 0.5s ease-out;">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <span style="font-size: 1.2rem; font-weight: 700;">{icon} {alert['title']}</span>
                            <br>
                            <span style="color: #555;">{alert['description']}</span>
                        </div>
                        <div style="text-align: right;">
                            <span class="status-badge status-{alert['type'].lower()}">{alert['type']}</span>
                            <br>
                            <span style="font-size: 0.7rem; color: #888;">{alert['timestamp'][:19]}</span>
                        </div>
                    </div>
                    <div style="margin-top: 0.5rem;">
                        <span style="font-weight: 600;">Action:</span> {alert['action']}
                    </div>
                    {f"<div style='margin-top: 0.5rem;'><span style='font-weight: 600;'>Entity:</span> {alert['entity']}</div>" if alert.get('entity') else ""}
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No alerts generated. Generate data or refresh alerts.")
    
    # ========================================================================
    # SIMULATION (PHASE 2 NEW FEATURE)
    # ========================================================================
    elif st.session_state.current_page == "Simulation":
        st.markdown("""
        <div style="display: flex; gap: 10px; flex-wrap: wrap; margin-bottom: 5px;">
            <span class="sih-badge">🏆 SIH 2026</span>
            <span class="ps-badge">AI-Powered Criminal Network Analysis</span>
            <span class="phase-badge">⚡ PHASE 2</span>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('<h1 class="main-title">🎯 "What-If" Simulation</h1>', unsafe_allow_html=True)
        st.markdown('<p class="main-title-sub">Simulate network disruption scenarios</p>', unsafe_allow_html=True)
        
        if not node_list:
            st.warning("No entities in the network. Please generate data first.")
        else:
            col1, col2 = st.columns([2, 1])
            
            with col1:
                target_entity = st.selectbox(
                    "🎯 Select Entity to Remove",
                    node_list,
                    help="Select an entity to simulate removal from the network"
                )
            
            with col2:
                if st.button("🚀 Run Simulation", use_container_width=True):
                    with st.spinner("Running simulation..."):
                        results = generate_simulation(G, target_entity)
                        st.session_state.simulation_results = results
                        st.rerun()
            
            if st.session_state.simulation_results:
                results = st.session_state.simulation_results
                
                st.markdown("---")
                st.markdown("### 📊 Simulation Results")
                
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Target Entity", results['target_entity'])
                with col2:
                    st.metric("Removed Connections", results['removed_connections'])
                with col3:
                    st.metric("Remaining Entities", results['remaining_entities'])
                with col4:
                    st.metric("Isolated Entities", results['isolated_entities'])
                
                st.markdown("---")
                
                # Impact visualization
                impact = results['network_disruption']
                st.markdown(f"""
                <div style="background: white; padding: 1.5rem; border-radius: 15px; 
                            box-shadow: 0 4px 20px rgba(0,0,0,0.08);">
                    <h3>💥 Network Disruption Impact</h3>
                    <div style="margin-top: 1rem;">
                        <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
                            <span>Disruption Level</span>
                            <span style="font-weight: 700; color: {'#ff4757' if impact > 0.5 else '#ffa502' if impact > 0.3 else '#2ed573'}">
                                {impact:.1%}
                            </span>
                        </div>
                        <div style="height: 10px; background: #f0f0f0; border-radius: 10px; overflow: hidden;">
                            <div style="height: 100%; width: {impact*100}%; background: {'#ff4757' if impact > 0.5 else '#ffa502' if impact > 0.3 else '#2ed573'}; 
                                        border-radius: 10px; transition: width 1s ease;">
                            </div>
                        </div>
                        <div style="margin-top: 0.5rem; color: #888; font-size: 0.85rem;">
                            Recommendation: <strong>{results['recommendation']}</strong> priority
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown("---")
                
                # Affected entities
                st.markdown("### 🔗 Affected Entities")
                if results['affected_entities']:
                    for entity in results['affected_entities']:
                        st.markdown(f"""
                        <div class="entity-card">
                            <strong>→ {entity}</strong>
                            <br><span style="color: #888; font-size: 0.85rem;">Will be impacted by removal</span>
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.info("No affected entities detected.")
                
                # Recommendations
                st.markdown("### 📌 Recommendations")
                if results['recommendation'] == 'High':
                    st.warning("🔴 High impact - consider alternative strategies")
                    st.markdown("- This entity is critical to the network")
                    st.markdown("- Removing it will cause significant disruption")
                    st.markdown("- Have replacement plans ready")
                elif results['recommendation'] == 'Medium':
                    st.info("🟡 Medium impact - proceed with caution")
                    st.markdown("- Network will be partially affected")
                    st.markdown("- Monitor for side effects")
                    st.markdown("- Have backup plans ready")
                else:
                    st.success("🟢 Low impact - proceed")
                    st.markdown("- Minimal network disruption expected")
                    st.markdown("- Continue with planned actions")
                    st.markdown("- Monitor for any unexpected changes")

# ============================================================================
# FOOTER
# ============================================================================

st.markdown("""
<div class="footer">
    <div style="display: flex; justify-content: center; gap: 20px; flex-wrap: wrap; margin-bottom: 10px;">
        <span>🏆 SIH 2026</span>
        <span>|</span>
        <span>🕵️ SUTRA-X v2.0.0</span>
        <span>|</span>
        <span>Smart Unified Threat & Relationship Analytics</span>
        <span>|</span>
        <span>⚡ Phase 2</span>
    </div>
    <div style="font-size: 0.8rem; color: #aaa;">
        Made with ❤️ for Smart India Hackathon 2026
    </div>
</div>
""", unsafe_allow_html=True)

# ============================================================================
# RUN THE APP
# ============================================================================

if __name__ == "__main__":
    pass
