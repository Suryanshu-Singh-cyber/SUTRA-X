"""
SUTRA-X: Smart Unified Threat & Relationship Analytics
AI-Powered Criminal Network Analysis System
SIH 2026
Complete Single-File Version - No Import Errors
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import json
import os
import sys
from pathlib import Path

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
    page_title="SUTRA-X - Criminal Network Intelligence | SIH 2026",
    page_icon="🕵️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# MULTI-LANGUAGE SUPPORT - 7 LANGUAGES
# ============================================================================

LANGUAGES = {
    "en": {
        "name": "English",
        "flag": "🇬🇧",
        "nav_dashboard": "Dashboard",
        "nav_graph": "Network Graph",
        "nav_entity": "Entity Profile",
        "nav_timeline": "Timeline",
        "nav_crosscase": "Cross-Case Discovery",
        "nav_ai": "AI Copilot",
        "nav_alerts": "Alerts & Emergency",
        "nav_simulation": "What-If Simulation",
        "nav_heatmap": "Heatmap",
        "nav_export": "Export",
        "nav_security": "Security",
        "dashboard_title": "Command Center",
        "dashboard_sub": "Real-time intelligence dashboard",
        "total_entities": "Total Entities",
        "relationships": "Relationships",
        "priority_leads": "Priority Leads",
        "cross_case_links": "Cross-Case Links",
        "active_alerts": "Active Alerts",
        "priority_leads_title": "Priority Investigation Leads",
        "no_priority": "No priority leads found",
        "recent_activity": "Recent Activity",
        "search_entity": "Search Entity",
        "view_profile": "View Profile",
        "connections": "Connections",
        "properties": "Properties",
        "recommendations": "Recommendations",
        "evidence": "Evidence",
        "priority_high": "HIGH",
        "priority_medium": "MEDIUM",
        "priority_low": "LOW",
        "generate_data": "Generate Sample Data",
        "loading": "Loading...",
        "success": "Success!",
        "error": "Error",
        "no_data": "No data loaded",
        "view": "View",
        "alerts_title": "Alerts & Emergency Response",
        "alerts_sub": "Real-time critical alerts and emergency notifications",
        "critical_alerts": "Critical Alerts",
        "warning_alerts": "Warnings",
        "info_alerts": "Information",
        "emergency_call": "Emergency Call",
        "call_now": "Call Now",
        "send_alert": "Send Alert to Team",
        "alert_sent": "Alert sent to all investigators!",
        "call_initiated": "Emergency call initiated...",
        "online": "Online",
        "offline": "Offline",
        "data_loaded": "Data Loaded",
        "no_data_loaded": "No data loaded",
        "heatmap_title": "Geographic Heatmap",
        "heatmap_sub": "Visualize crime hotspots and patterns",
        "export_title": "Export Reports",
        "export_sub": "Generate and download investigation reports",
        "export_json": "Export as JSON",
        "security_title": "Security & Access Control",
        "security_sub": "Role-Based Access Control and Audit Logs",
        "user_role": "User Role",
        "audit_logs": "Audit Logs",
        "rbac_info": "Role-Based Access Control",
        "offline_mode": "Offline Mode",
        "offline_desc": "Work without internet, sync when online",
        "login": "Login",
        "username": "Username",
        "password": "Password",
        "logout": "Logout",
        "heatmap_intensity": "Intensity",
        "heatmap_locations": "Locations",
        "export_history": "Export History",
        "generated_at": "Generated At",
        "file_name": "File Name",
        "download": "Download",
        "security_roles": {
            "admin": "Administrator",
            "investigator": "Investigator",
            "analyst": "Analyst",
            "viewer": "Viewer"
        },
        "audit_actions": {
            "login": "Login",
            "logout": "Logout",
            "view": "View Entity",
            "export": "Export Report",
            "update": "Update Data",
            "delete": "Delete Entity",
            "alert": "Alert Triggered",
            "simulation": "Simulation Run",
            "ai_query": "AI Query"
        },
        "made_with": "Made with ❤️ for Smart India Hackathon 2026",
        "version": "v3.0.0",
        "disclaimer": "This is an AI-generated analysis. All findings should be verified by human investigators.",
        "quick_questions": "Quick Questions",
        "custom_query": "Custom Query",
        "analyze": "Analyze",
        "ask_question": "Ask your question",
        "ai_response": "AI Response",
        "key_findings": "Key Findings",
        "actionable_insights": "Actionable Insights",
        "next_steps": "Next Steps",
        "relevant_entities": "Relevant Entities",
        "ai_title": "AI Copilot",
        "ai_sub": "Intelligent investigation assistant",
        "simulation_title": "What-If Simulation",
        "simulation_sub": "Simulate network disruption scenarios",
        "select_entity": "Select Entity to Remove",
        "run_simulation": "Run Simulation",
        "simulation_results": "Simulation Results",
        "target_entity": "Target Entity",
        "removed_connections": "Removed Connections",
        "remaining_entities": "Remaining Entities",
        "isolated_entities": "Isolated Entities",
        "disruption_impact": "Network Disruption Impact",
        "disruption_level": "Disruption Level",
        "affected_entities": "Affected Entities",
        "recommendation_label": "Recommendation",
        "crosscase_title": "Cross-Case Connection Discovery",
        "crosscase_sub": "Uncover hidden connections between cases",
        "shared_entities": "Shared Entities",
        "confidence": "Confidence",
        "total_connections": "Total Connections",
        "shared_persons": "Shared Persons",
        "entity_intelligence": "Entity Intelligence",
        "quick_stats": "Quick Stats",
        "direct_connections": "Direct Connections",
        "network_degree": "Network Degree",
        "priority_score": "Priority Score",
        "timeline_title": "Investigation Timeline",
        "timeline_sub": "Track network evolution over time",
        "key_events": "Key Events"
    },
    "hi": {
        "name": "हिंदी",
        "flag": "🇮🇳",
        "nav_dashboard": "डैशबोर्ड",
        "nav_graph": "नेटवर्क ग्राफ",
        "nav_entity": "इकाई प्रोफ़ाइल",
        "nav_timeline": "समयरेखा",
        "nav_crosscase": "क्रॉस-केस खोज",
        "nav_ai": "एआई सहायक",
        "nav_alerts": "अलर्ट और आपातकाल",
        "nav_simulation": "क्या-अगर सिमुलेशन",
        "nav_heatmap": "हीटमैप",
        "nav_export": "निर्यात",
        "nav_security": "सुरक्षा",
        "dashboard_title": "कमांड सेंटर",
        "dashboard_sub": "वास्तविक समय खुफिया डैशबोर्ड",
        "total_entities": "कुल इकाइयां",
        "relationships": "संबंध",
        "priority_leads": "प्राथमिकता लीड",
        "cross_case_links": "क्रॉस-केस लिंक",
        "active_alerts": "सक्रिय अलर्ट",
        "priority_leads_title": "प्राथमिकता जांच लीड",
        "no_priority": "कोई प्राथमिकता लीड नहीं मिली",
        "recent_activity": "हाल की गतिविधि",
        "search_entity": "इकाई खोजें",
        "view_profile": "प्रोफ़ाइल देखें",
        "connections": "कनेक्शन",
        "properties": "गुण",
        "recommendations": "सिफारिशें",
        "evidence": "साक्ष्य",
        "priority_high": "उच्च",
        "priority_medium": "मध्यम",
        "priority_low": "निम्न",
        "generate_data": "नमूना डेटा उत्पन्न करें",
        "loading": "लोड हो रहा है...",
        "success": "सफलता!",
        "error": "त्रुटि",
        "no_data": "कोई डेटा लोड नहीं",
        "view": "देखें",
        "alerts_title": "अलर्ट और आपातकालीन प्रतिक्रिया",
        "alerts_sub": "वास्तविक समय महत्वपूर्ण अलर्ट और आपातकालीन सूचनाएं",
        "critical_alerts": "गंभीर अलर्ट",
        "warning_alerts": "चेतावनी",
        "info_alerts": "सूचना",
        "emergency_call": "आपातकालीन कॉल",
        "call_now": "अभी कॉल करें",
        "send_alert": "टीम को अलर्ट भेजें",
        "alert_sent": "सभी जांचकर्ताओं को अलर्ट भेजा गया!",
        "call_initiated": "आपातकालीन कॉल शुरू की गई...",
        "online": "ऑनलाइन",
        "offline": "ऑफलाइन",
        "data_loaded": "डेटा लोड हुआ",
        "no_data_loaded": "कोई डेटा लोड नहीं",
        "heatmap_title": "भौगोलिक हीटमैप",
        "heatmap_sub": "अपराध हॉटस्पॉट और पैटर्न देखें",
        "export_title": "रिपोर्ट निर्यात",
        "export_sub": "जांच रिपोर्ट जनरेट और डाउनलोड करें",
        "export_json": "JSON के रूप में निर्यात करें",
        "security_title": "सुरक्षा और पहुंच नियंत्रण",
        "security_sub": "रोल-आधारित पहुंच नियंत्रण और ऑडिट लॉग",
        "user_role": "उपयोगकर्ता भूमिका",
        "audit_logs": "ऑडिट लॉग",
        "rbac_info": "रोल-आधारित पहुंच नियंत्रण",
        "offline_mode": "ऑफलाइन मोड",
        "offline_desc": "इंटरनेट के बिना काम करें, ऑनलाइन होने पर सिंक करें",
        "login": "लॉगिन",
        "username": "उपयोगकर्ता नाम",
        "password": "पासवर्ड",
        "logout": "लॉगआउट",
        "heatmap_intensity": "तीव्रता",
        "heatmap_locations": "स्थान",
        "export_history": "निर्यात इतिहास",
        "generated_at": "जनरेट किया गया",
        "file_name": "फ़ाइल नाम",
        "download": "डाउनलोड",
        "security_roles": {
            "admin": "प्रशासक",
            "investigator": "जांचकर्ता",
            "analyst": "विश्लेषक",
            "viewer": "दर्शक"
        },
        "audit_actions": {
            "login": "लॉगिन",
            "logout": "लॉगआउट",
            "view": "इकाई देखें",
            "export": "रिपोर्ट निर्यात",
            "update": "डेटा अपडेट",
            "delete": "इकाई हटाएं",
            "alert": "अलर्ट ट्रिगर",
            "simulation": "सिमुलेशन चलाएं",
            "ai_query": "AI प्रश्न"
        },
        "made_with": "स्मार्ट इंडिया हैकथॉन 2026 के लिए ❤️ के साथ बनाया गया",
        "version": "v3.0.0",
        "disclaimer": "यह एक एआई-जनित विश्लेषण है। सभी निष्कर्षों को मानव जांचकर्ताओं द्वारा सत्यापित किया जाना चाहिए।",
        "quick_questions": "त्वरित प्रश्न",
        "custom_query": "कस्टम प्रश्न",
        "analyze": "विश्लेषण करें",
        "ask_question": "अपना प्रश्न पूछें",
        "ai_response": "एआई प्रतिक्रिया",
        "key_findings": "मुख्य निष्कर्ष",
        "actionable_insights": "कार्रवाई योग्य अंतर्दृष्टि",
        "next_steps": "अगले कदम",
        "relevant_entities": "प्रासंगिक इकाइयां",
        "ai_title": "एआई सहायक",
        "ai_sub": "बुद्धिमान जांच सहायक",
        "simulation_title": "क्या-अगर सिमुलेशन",
        "simulation_sub": "नेटवर्क व्यवधान परिदृश्यों का अनुकरण करें",
        "select_entity": "हटाने के लिए इकाई चुनें",
        "run_simulation": "सिमुलेशन चलाएं",
        "simulation_results": "सिमुलेशन परिणाम",
        "target_entity": "लक्ष्य इकाई",
        "removed_connections": "हटाए गए कनेक्शन",
        "remaining_entities": "शेष इकाइयां",
        "isolated_entities": "पृथक इकाइयां",
        "disruption_impact": "नेटवर्क व्यवधान प्रभाव",
        "disruption_level": "व्यवधान स्तर",
        "affected_entities": "प्रभावित इकाइयां",
        "recommendation_label": "सिफारिश",
        "crosscase_title": "क्रॉस-केस कनेक्शन खोज",
        "crosscase_sub": "मामलों के बीच छिपे कनेक्शन का पता लगाएं",
        "shared_entities": "साझा इकाइयां",
        "confidence": "विश्वास",
        "total_connections": "कुल कनेक्शन",
        "shared_persons": "साझा व्यक्ति",
        "entity_intelligence": "इकाई खुफिया",
        "quick_stats": "त्वरित आंकड़े",
        "direct_connections": "प्रत्यक्ष कनेक्शन",
        "network_degree": "नेटवर्क डिग्री",
        "priority_score": "प्राथमिकता स्कोर",
        "timeline_title": "जांच समयरेखा",
        "timeline_sub": "समय के साथ नेटवर्क विकास ट्रैक करें",
        "key_events": "मुख्य घटनाएं"
    }
}

# Add all languages with English fallback
for lang in ["ta", "te", "bn", "ml", "ur"]:
    if lang not in LANGUAGES:
        LANGUAGES[lang] = LANGUAGES["en"].copy()
        LANGUAGES[lang]["name"] = lang
        LANGUAGES[lang]["flag"] = "🇮🇳"

def get_text(key):
    lang = st.session_state.get('language', 'en')
    if lang in LANGUAGES and key in LANGUAGES[lang] and LANGUAGES[lang][key]:
        return LANGUAGES[lang][key]
    return LANGUAGES['en'].get(key, key)

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
if 'alerts' not in st.session_state:
    st.session_state.alerts = []
if 'simulation_results' not in st.session_state:
    st.session_state.simulation_results = None
if 'emergency_triggered' not in st.session_state:
    st.session_state.emergency_triggered = False
if 'alert_sent' not in st.session_state:
    st.session_state.alert_sent = False
if 'offline_mode' not in st.session_state:
    st.session_state.offline_mode = False
if 'user_role' not in st.session_state:
    st.session_state.user_role = "viewer"
if 'audit_logs' not in st.session_state:
    st.session_state.audit_logs = []
if 'export_history' not in st.session_state:
    st.session_state.export_history = []
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'current_user' not in st.session_state:
    st.session_state.current_user = None
if 'ai_query' not in st.session_state:
    st.session_state.ai_query = ""

# ============================================================================
# RBAC SYSTEM
# ============================================================================

USERS_DB = {
    "admin": {"password": "admin123", "role": "admin", "name": "Administrator"},
    "investigator": {"password": "invest123", "role": "investigator", "name": "Senior Investigator"},
    "analyst": {"password": "analyst123", "role": "analyst", "name": "Data Analyst"},
    "viewer": {"password": "viewer123", "role": "viewer", "name": "Viewer"}
}

ROLE_PERMISSIONS = {
    "admin": ["view_data", "export_data", "manage_entities", "manage_users", "view_audit", "manage_alerts", "run_simulation", "use_ai"],
    "investigator": ["view_data", "export_data", "manage_entities", "view_audit", "manage_alerts", "run_simulation", "use_ai"],
    "analyst": ["view_data", "export_data", "view_audit", "use_ai"],
    "viewer": ["view_data"]
}

def authenticate_user(username, password):
    if username in USERS_DB and USERS_DB[username]["password"] == password:
        return USERS_DB[username]
    return None

def has_permission(permission):
    role = st.session_state.get('user_role', 'viewer')
    return permission in ROLE_PERMISSIONS.get(role, [])

def add_audit_log(action, resource, details=""):
    log_entry = {
        'timestamp': datetime.now().isoformat(),
        'user': st.session_state.get('current_user', 'unknown'),
        'role': st.session_state.get('user_role', 'unknown'),
        'action': action,
        'resource': resource,
        'details': details
    }
    st.session_state.audit_logs.insert(0, log_entry)
    if len(st.session_state.audit_logs) > 100:
        st.session_state.audit_logs = st.session_state.audit_logs[:100]

# ============================================================================
# GRAPH CLASS (Fallback if networkx not available)
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
# DATA GENERATION
# ============================================================================

def generate_sample_network():
    if NETWORKX_AVAILABLE:
        G = nx.Graph()
    else:
        G = SimpleGraph()
    
    first_names = ['Raj', 'Amit', 'Priya', 'Suresh', 'Anita', 'Vikram', 'Neha', 'Rahul', 
                   'Sunita', 'Mohan', 'Geeta', 'Arjun', 'Kavita', 'Deepak', 'Anjali', 
                   'Sanjay', 'Meera', 'Ravi', 'Pooja', 'Kumar', 'Ashok', 'Preeti',
                   'Vijay', 'Nisha', 'Ramesh', 'Sneha', 'Mahesh', 'Jyoti']
    
    last_names = ['Sharma', 'Singh', 'Patel', 'Reddy', 'Rao', 'Joshi', 'Gupta', 'Verma', 
                  'Kumar', 'Nair', 'Mehta', 'Choudhary', 'Yadav', 'Khan', 'Das']
    
    locations = ['Mumbai', 'Delhi', 'Bangalore', 'Chennai', 'Hyderabad', 'Pune', 'Kolkata']
    
    persons = []
    for i in range(30):
        name = f"{random.choice(first_names)} {random.choice(last_names)}"
        person_id = f"P-{i+1:04d}"
        G.add_node(person_id, type='PERSON', name=name, 
                   age=random.randint(22, 60),
                   city=random.choice(locations),
                   occupation=random.choice(['Business', 'Student', 'Government', 'Private', 'Professional']),
                   latitude=8.4 + random.random() * 29.2,
                   longitude=68.7 + random.random() * 28.6)
        persons.append(person_id)
    
    phones = []
    for i in range(20):
        phone_id = f"PH-{i+1:04d}"
        number = f"98{random.randint(10000000, 99999999)}"
        G.add_node(phone_id, type='PHONE', number=number)
        phones.append(phone_id)
        owner = random.choice(persons)
        G.add_edge(owner, phone_id, type='OWNS', confidence=0.8)
    
    accounts = []
    for i in range(15):
        account_id = f"ACC-{i+1:04d}"
        G.add_node(account_id, type='ACCOUNT', bank=random.choice(['SBI', 'HDFC', 'ICICI', 'Axis', 'PNB']))
        accounts.append(account_id)
        owner = random.choice(persons)
        G.add_edge(owner, account_id, type='OWNS', confidence=0.7)
    
    vehicles = []
    prefixes = ['MH', 'DL', 'KA', 'TN', 'TS', 'GJ', 'UP']
    for i in range(10):
        vehicle_id = f"V-{i+1:04d}"
        reg = f"{random.choice(prefixes)}{random.randint(1,99)} {random.choice(['AB','CD','EF','GH'])}{random.randint(1000,9999)}"
        G.add_node(vehicle_id, type='VEHICLE', registration=reg,
                   make=random.choice(['Maruti', 'Hyundai', 'Toyota', 'Honda', 'Tata']))
        vehicles.append(vehicle_id)
        owner = random.choice(persons)
        G.add_edge(owner, vehicle_id, type='OWNS', confidence=0.6)
    
    locs = []
    loc_names = ['Connaught Place', 'Bandra West', 'Indiranagar', 'T. Nagar', 'Hitech City', 
                 'Juhu', 'Koramangala', 'Marine Drive']
    for i in range(8):
        loc_id = f"L-{i+1:04d}"
        G.add_node(loc_id, type='LOCATION', 
                   name=loc_names[i % len(loc_names)],
                   city=random.choice(locations),
                   latitude=8.4 + random.random() * 29.2,
                   longitude=68.7 + random.random() * 28.6)
        locs.append(loc_id)
    
    cases = []
    case_titles = ['Drug Trafficking Ring', 'Financial Fraud Network', 'Arms Dealing', 
                   'Cyber Crime Syndicate', 'Money Laundering', 'Human Trafficking']
    for i in range(6):
        case_id = f"CASE-{i+1:03d}"
        G.add_node(case_id, type='CASE', 
                   title=case_titles[i % len(case_titles)],
                   status=random.choice(['Active', 'Pending', 'Under Review']))
        cases.append(case_id)
        for _ in range(random.randint(2, 5)):
            person = random.choice(persons)
            G.add_edge(case_id, person, type='INVOLVED', confidence=0.6 + random.random()*0.3)
    
    for _ in range(30):
        caller = random.choice(phones)
        receiver = random.choice(phones)
        if caller != receiver:
            G.add_edge(caller, receiver, type='CALLED', duration=random.randint(30, 600))
    
    for _ in range(25):
        from_acc = random.choice(accounts)
        to_acc = random.choice(accounts)
        if from_acc != to_acc:
            G.add_edge(from_acc, to_acc, type='TRANSACTION', amount=random.randint(5000, 500000))
    
    for _ in range(20):
        person = random.choice(persons)
        loc = random.choice(locs)
        G.add_edge(person, loc, type='VISITED')
    
    for _ in range(8):
        person = random.choice(persons)
        case = random.choice(cases)
        G.add_edge(person, case, type='INVOLVED', confidence=0.5 + random.random()*0.4)
    
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
        if NETWORKX_AVAILABLE:
            return list(G.neighbors(node))
        else:
            return G.neighbors(node)
    except:
        return []

def get_degree(G, node):
    try:
        if NETWORKX_AVAILABLE:
            return G.degree(node)
        else:
            return G.degree(node)
    except:
        return len(get_neighbors(G, node))

def get_edge_data(G, u, v):
    try:
        if NETWORKX_AVAILABLE:
            return G.get_edge_data(u, v)
        else:
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

def generate_alerts(G):
    alerts = []
    if G is None:
        return alerts
    
    node_list = get_node_list(G)
    
    for node in node_list:
        attrs = get_node_attributes(G, node)
        degree = get_degree(G, node)
        if degree >= 5 and attrs.get('type') == 'PERSON':
            alerts.append({
                'id': f"ALERT-{len(alerts)+1:04d}",
                'type': 'CRITICAL',
                'title': f'Critical Entity: {node}',
                'description': f'Entity {node} has {degree} connections',
                'entity': node,
                'timestamp': datetime.now().isoformat(),
                'action': 'Immediate investigation required',
                'emergency': True
            })
        elif degree >= 4 and attrs.get('type') == 'PERSON':
            alerts.append({
                'id': f"ALERT-{len(alerts)+1:04d}",
                'type': 'WARNING',
                'title': f'High Priority Entity: {node}',
                'description': f'Entity {node} has {degree} connections',
                'entity': node,
                'timestamp': datetime.now().isoformat(),
                'action': 'Review connections for patterns',
                'emergency': False
            })
    
    case_nodes = [n for n in node_list if get_node_attributes(G, n).get('type') == 'CASE']
    for case in case_nodes:
        neighbors = get_neighbors(G, case)
        person_neighbors = [n for n in neighbors if get_node_attributes(G, n).get('type') == 'PERSON']
        if len(person_neighbors) >= 4:
            alerts.append({
                'id': f"ALERT-{len(alerts)+1:04d}",
                'type': 'INFO',
                'title': f'Cross-Case: {case}',
                'description': f'Case {case} connected to {len(person_neighbors)} persons',
                'entity': case,
                'timestamp': datetime.now().isoformat(),
                'action': 'Investigate cross-case connections',
                'emergency': False
            })
    
    return alerts[:10]

def generate_simulation(G, target_entity):
    if G is None or target_entity not in get_node_list(G):
        return None
    
    neighbors = get_neighbors(G, target_entity)
    original_degree = get_degree(G, target_entity)
    
    simulation_results = {
        'target_entity': target_entity,
        'removed_connections': len(neighbors),
        'remaining_entities': len(get_node_list(G)) - 1,
        'isolated_entities': 0,
        'affected_entities': neighbors[:5],
        'network_disruption': len(neighbors) / max(1, original_degree),
        'timestamp': datetime.now().isoformat(),
        'recommendation': 'HIGH' if len(neighbors) >= 5 else 'MEDIUM' if len(neighbors) >= 3 else 'LOW'
    }
    return simulation_results

# ============================================================================
# CUSTOM CSS
# ============================================================================

st.markdown("""
<style>
    /* ===== ANIMATIONS ===== */
    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(40px); }
        to { opacity: 1; transform: translateY(0); }
    }
    @keyframes fadeInDown {
        from { opacity: 0; transform: translateY(-40px); }
        to { opacity: 1; transform: translateY(0); }
    }
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
    @keyframes float {
        0% { transform: translateY(0px); }
        50% { transform: translateY(-15px); }
        100% { transform: translateY(0px); }
    }
    @keyframes shimmer {
        0% { background-position: -200% center; }
        100% { background-position: 200% center; }
    }
    @keyframes glow {
        0% { box-shadow: 0 0 5px rgba(102, 126, 234, 0.2); }
        50% { box-shadow: 0 0 25px rgba(102, 126, 234, 0.5); }
        100% { box-shadow: 0 0 5px rgba(102, 126, 234, 0.2); }
    }
    @keyframes slideInLeft {
        from { opacity: 0; transform: translateX(-30px); }
        to { opacity: 1; transform: translateX(0); }
    }
    
    /* ===== HERO SECTION ===== */
    .hero-section {
        background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
        padding: 3rem 4rem;
        border-radius: 25px;
        margin-bottom: 2rem;
        position: relative;
        overflow: hidden;
        border: 1px solid rgba(102, 126, 234, 0.2);
        min-height: 280px;
        display: flex;
        align-items: center;
    }
    
    .hero-section::before {
        content: '';
        position: absolute;
        top: -50%;
        right: -20%;
        width: 60%;
        height: 200%;
        background: radial-gradient(circle, rgba(102, 126, 234, 0.08) 0%, transparent 70%);
        animation: float 8s ease-in-out infinite;
    }
    
    .hero-section::after {
        content: '🔍';
        position: absolute;
        right: 3rem;
        bottom: 1rem;
        font-size: 8rem;
        opacity: 0.06;
        animation: float 6s ease-in-out infinite;
    }
    
    .hero-content {
        position: relative;
        z-index: 1;
        animation: fadeInUp 0.8s ease-out;
    }
    
    .hero-title {
        font-size: 3.8rem;
        font-weight: 800;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 30%, #f093fb 60%, #f5576c 100%);
        background-size: 300% auto;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: shimmer 4s linear infinite;
        letter-spacing: -1px;
        line-height: 1.1;
    }
    
    .hero-subtitle {
        font-size: 1.3rem;
        color: rgba(255,255,255,0.8);
        margin-top: 0.5rem;
        font-weight: 300;
    }
    
    .hero-description {
        color: rgba(255,255,255,0.6);
        margin-top: 1rem;
        font-size: 1rem;
        max-width: 600px;
        line-height: 1.6;
    }
    
    .hero-badges {
        display: flex;
        gap: 12px;
        flex-wrap: wrap;
        margin-top: 1.2rem;
    }
    
    .sih-badge-hero {
        display: inline-block;
        background: linear-gradient(135deg, #ff6b6b, #ee5a24);
        color: white;
        padding: 8px 24px;
        border-radius: 50px;
        font-size: 0.9rem;
        font-weight: 700;
        animation: pulse 2s infinite;
        box-shadow: 0 4px 15px rgba(238, 90, 36, 0.3);
    }
    
    .ps-badge-hero {
        display: inline-block;
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        padding: 8px 24px;
        border-radius: 50px;
        font-size: 0.9rem;
        font-weight: 700;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    }
    
    .feature-tag {
        display: inline-block;
        background: rgba(255,255,255,0.1);
        backdrop-filter: blur(10px);
        color: rgba(255,255,255,0.8);
        padding: 6px 16px;
        border-radius: 50px;
        font-size: 0.75rem;
        border: 1px solid rgba(255,255,255,0.1);
    }
    
    /* ===== METRIC CARDS ===== */
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        border-left: 5px solid #667eea;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        animation: fadeInUp 0.6s ease-out;
        position: relative;
        overflow: hidden;
    }
    
    .metric-card:hover {
        transform: translateY(-8px) scale(1.01);
        box-shadow: 0 12px 40px rgba(0,0,0,0.15);
    }
    
    .metric-card .icon {
        font-size: 2.2rem;
        margin-bottom: 0.5rem;
        display: inline-block;
        animation: float 4s ease-in-out infinite;
    }
    
    .metric-card .value {
        font-size: 2.2rem;
        font-weight: 700;
        color: #1a1a2e;
    }
    
    .metric-card .label {
        font-size: 0.9rem;
        color: #666;
        font-weight: 500;
    }
    
    /* ===== STATUS BADGES ===== */
    .status-badge {
        padding: 4px 16px;
        border-radius: 50px;
        font-size: 0.8rem;
        font-weight: 600;
        display: inline-block;
    }
    .status-high { background: #ff6b6b; color: white; animation: pulse 1.5s infinite; }
    .status-medium { background: #feca57; color: #333; }
    .status-low { background: #48dbfb; color: #333; }
    
    /* ===== ENTITY CARDS ===== */
    .entity-card {
        background: #f8f9fa;
        padding: 1rem 1.2rem;
        border-radius: 12px;
        margin: 0.5rem 0;
        border-left: 4px solid #667eea;
        transition: all 0.3s ease;
        animation: slideInLeft 0.5s ease-out;
    }
    .entity-card:hover {
        background: #f0f2f6;
        transform: translateX(8px) scale(1.01);
        box-shadow: 0 4px 15px rgba(0,0,0,0.08);
    }
    
    /* ===== ALERT CARDS ===== */
    .alert-card-critical {
        background: linear-gradient(135deg, #ff4757, #ff6b6b);
        color: white;
        padding: 1.2rem;
        border-radius: 12px;
        margin: 0.5rem 0;
        animation: pulse 2s infinite;
        border: 2px solid rgba(255,255,255,0.2);
    }
    .alert-card-warning {
        background: linear-gradient(135deg, #ffa502, #feca57);
        color: white;
        padding: 1.2rem;
        border-radius: 12px;
        margin: 0.5rem 0;
        border: 2px solid rgba(255,255,255,0.2);
    }
    .alert-card-info {
        background: linear-gradient(135deg, #2ed573, #48dbfb);
        color: white;
        padding: 1.2rem;
        border-radius: 12px;
        margin: 0.5rem 0;
        border: 2px solid rgba(255,255,255,0.2);
    }
    
    /* ===== SECTION DIVIDER ===== */
    .section-divider {
        height: 2px;
        background: linear-gradient(90deg, transparent, #667eea, #764ba2, #f093fb, transparent);
        margin: 2rem 0;
        border-radius: 10px;
    }
    
    /* ===== GLOW CARD ===== */
    .glow-card {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        border: 1px solid rgba(102,126,234,0.1);
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        animation: glow 4s infinite;
        height: 100%;
        text-align: center;
    }
    .glow-card:hover {
        transform: translateY(-5px) scale(1.01);
        box-shadow: 0 12px 40px rgba(102,126,234,0.2);
        border-color: #667eea;
    }
    .glow-card .icon { font-size: 3rem; margin-bottom: 0.5rem; }
    .glow-card h3 { color: #1a1a2e; font-size: 1.2rem; margin: 0.5rem 0; }
    .glow-card p { color: #666; font-size: 0.9rem; }
    
    /* ===== QUICK STATS - FIXED DARK TEXT ===== */
    .quick-stats {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
    }
    .quick-stats .stat-item {
        display: flex;
        justify-content: space-between;
        padding: 0.5rem 0;
        border-bottom: 1px solid #eee;
        color: #1a1a2e;
    }
    .quick-stats .stat-item:last-child { border-bottom: none; }
    .quick-stats .stat-label { color: #666; }
    .quick-stats .stat-value { font-weight: 700; color: #1a1a2e; }
    
    /* ===== RAG RESPONSE ===== */
    .rag-response {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 4px solid #667eea;
        margin: 0.5rem 0;
    }
    
    /* ===== FOOTER ===== */
    .footer {
        text-align: center;
        padding: 1.5rem 0;
        color: #888;
        font-size: 0.85rem;
        border-top: 1px solid #eee;
        margin-top: 2rem;
    }
    
    /* ===== BUTTONS ===== */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-weight: 600;
        border: none;
        border-radius: 50px;
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
    }
    
    /* ===== RESPONSIVE ===== */
    @media (max-width: 768px) {
        .hero-title { font-size: 2.2rem; }
        .hero-section { padding: 2rem; }
        .metric-card .value { font-size: 1.5rem; }
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# SIDEBAR
# ============================================================================

with st.sidebar:
    st.markdown("""
    <div style="text-align: center; padding: 0.5rem 0;">
        <div style="font-size: 3rem; animation: float 3s ease-in-out infinite;">🕵️</div>
        <div style="font-size: 1.5rem; font-weight: 700; background: linear-gradient(135deg, #667eea, #764ba2); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
            SUTRA-X
        </div>
        <div style="font-size: 0.65rem; color: #888; margin-top: -3px;">
            Smart Unified Threat & Relationship Analytics
        </div>
        <div style="margin-top: 6px;">
            <span style="display: inline-block; background: linear-gradient(135deg, #ff6b6b, #ee5a24); color: white; padding: 3px 12px; border-radius: 50px; font-size: 0.65rem; font-weight: 600;">🏆 SIH 2026</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Language Selector - 7 Languages
    st.markdown("### 🌐 Language")
    lang_options = {code: f"{data['flag']} {data['name']}" for code, data in LANGUAGES.items()}
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
    
    # Authentication
    st.markdown("### 🔐 Security")
    
    if not st.session_state.authenticated:
        username = st.text_input("Username", key="login_username")
        password = st.text_input("Password", type="password", key="login_password")
        if st.button("Login", use_container_width=True):
            user = authenticate_user(username, password)
            if user:
                st.session_state.authenticated = True
                st.session_state.current_user = username
                st.session_state.user_role = user['role']
                add_audit_log("login", "Authentication", f"User: {username}")
                st.success(f"✅ Welcome {user['name']}!")
                st.rerun()
            else:
                st.error("❌ Invalid credentials")
    else:
        st.success(f"✅ {st.session_state.current_user}")
        st.caption(f"Role: {st.session_state.user_role.upper()}")
        if st.button("Logout", use_container_width=True):
            add_audit_log("logout", "Authentication", f"User: {st.session_state.current_user}")
            st.session_state.authenticated = False
            st.session_state.current_user = None
            st.session_state.user_role = 'viewer'
            st.rerun()
    
    st.markdown("---")
    
    # Offline Mode
    st.markdown("### 📶 Mode")
    offline_toggle = st.toggle("Offline Mode", value=st.session_state.offline_mode)
    if offline_toggle != st.session_state.offline_mode:
        st.session_state.offline_mode = offline_toggle
        add_audit_log("mode_change", "Offline Mode", f"Set to {offline_toggle}")
        st.rerun()
    
    st.markdown("---")
    
    # Navigation
    st.markdown("### 📌 Navigation")
    nav_items = [
        ("Dashboard", "📊"),
        ("Network Graph", "🌐"),
        ("Entity Profile", "👤"),
        ("Timeline", "⏱️"),
        ("Cross-Case Discovery", "🔗"),
        ("AI Copilot", "🤖"),
        ("Alerts & Emergency", "🔔"),
        ("What-If Simulation", "🎯"),
        ("Heatmap", "🗺️"),
        ("Export", "📄"),
        ("Security", "🔐")
    ]
    for page, icon in nav_items:
        if st.button(f"{icon} {page}", key=f"nav_{page}", use_container_width=True):
            st.session_state.current_page = page
            st.rerun()
    
    st.markdown("---")
    
    # Data Controls
    st.markdown("### 📊 Data")
    if st.button("🔄 Generate Sample Data", use_container_width=True):
        with st.spinner("Generating sample data..."):
            G = generate_sample_network()
            st.session_state.graph = G
            st.session_state.data_loaded = True
            st.session_state.entity_list = get_node_list(G)
            st.session_state.alerts = generate_alerts(G)
            add_audit_log("data_generate", "Network Data", "Sample data generated")
            st.success("✅ Data generated!")
            st.rerun()
    
    st.markdown("---")
    
    # Status
    if st.session_state.data_loaded:
        st.success(f"✅ Data Loaded")
        st.caption(f"Entities: {len(st.session_state.entity_list)}")
        if st.session_state.offline_mode:
            st.markdown('<span style="display: inline-block; padding: 3px 12px; border-radius: 50px; font-size: 0.65rem; font-weight: 600; background: #ffa50220; color: #ffa502; border: 1px solid #ffa50240;">📴 OFFLINE</span>', unsafe_allow_html=True)
        else:
            st.markdown('<span style="display: inline-block; padding: 3px 12px; border-radius: 50px; font-size: 0.65rem; font-weight: 600; background: #2ed57320; color: #2ed573; border: 1px solid #2ed57340;">📶 ONLINE</span>', unsafe_allow_html=True)
    else:
        st.info("⏳ No data loaded")
    
    st.markdown("---")
    st.caption("v3.0.0 | Made with ❤️")

# ============================================================================
# HERO SECTION
# ============================================================================

st.markdown("""
<div class="hero-section">
    <div class="hero-content">
        <div class="hero-badges">
            <span class="sih-badge-hero">🏆 SIH 2026</span>
            <span class="ps-badge-hero">AI-Powered Criminal Network Analysis</span>
        </div>
        <div class="hero-title">🕵️ SUTRA-X</div>
        <div class="hero-subtitle">Smart Unified Threat & Relationship Analytics</div>
        <div class="hero-description">
            AI-powered platform that connects the dots across criminal cases, discovers hidden relationships,
            and provides evidence-backed investigative leads in seconds.
        </div>
        <div style="display: flex; gap: 8px; flex-wrap: wrap; margin-top: 1rem;">
            <span class="feature-tag">🤖 AI Copilot</span>
            <span class="feature-tag">🔗 Cross-Case Discovery</span>
            <span class="feature-tag">🗺️ Heatmap</span>
            <span class="feature-tag">🔐 RBAC</span>
            <span class="feature-tag">📊 Network Analysis</span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ============================================================================
# FALLBACK NETWORK DISPLAY
# ============================================================================

def display_fallback_network(G, node_list):
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
    for u in node_list:
        for v in get_neighbors(G, u):
            if (u, v) not in [(e['Source'], e['Target']) for e in edge_data]:
                edge_data.append({
                    'Source': u,
                    'Target': v,
                    'Type': get_edge_data(G, u, v).get('type', 'CONNECTED')
                })
    if edge_data:
        st.dataframe(pd.DataFrame(edge_data), use_container_width=True)

# ============================================================================
# MAIN PAGES
# ============================================================================

# ===== DASHBOARD =====
def render_dashboard():
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
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="icon">👥</div>
            <div class="value">{metrics['total_nodes'] if metrics else 0}</div>
            <div class="label">{get_text('total_entities')}</div>
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
            <div class="label">{get_text('active_alerts')}</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    
    st.markdown(f"## 🚨 {get_text('priority_leads_title')}")
    
    if metrics and metrics['priority_entities']:
        for entity in metrics['priority_entities'][:5]:
            score = min(100, entity['degree'] * 15)
            priority_label = get_text('priority_high') if score >= 70 else get_text('priority_medium') if score >= 50 else get_text('priority_low')
            color = "🔴" if priority_label == get_text('priority_high') else "🟡" if priority_label == get_text('priority_medium') else "🟢"
            
            col1, col2, col3, col4 = st.columns([2.5, 2, 1.5, 1])
            with col1:
                st.markdown(f"""
                <div class="entity-card">
                    <strong>🔍 {entity['id']}</strong>
                    <br><span style="color: #888; font-size: 0.85rem;">{entity['type']} | {entity['name']}</span>
                </div>
                """, unsafe_allow_html=True)
            with col2:
                st.caption(f"{get_text('connections')}: {entity['degree']}")
            with col3:
                st.markdown(f'<span class="status-badge status-{priority_label.lower()}">{color} {priority_label}</span>', unsafe_allow_html=True)
            with col4:
                if st.button(get_text('view'), key=f"view_dash_{entity['id']}"):
                    st.session_state.selected_entity = entity['id']
                    st.session_state.current_page = "Entity Profile"
                    st.rerun()
            
            st.markdown("---")
    else:
        st.info(get_text('no_priority'))

# ===== NETWORK GRAPH (3D) =====
def render_network_graph():
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
        st.warning("Not enough data for graph visualization.")
        return
    
    if PLOTLY_AVAILABLE and NETWORKX_AVAILABLE:
        try:
            st.info("💡 Hover over nodes for details. Drag to rotate the 3D view.")
            
            pos = nx.spring_layout(G, dim=3, k=0.5, iterations=50)
            
            node_x, node_y, node_z = [], [], []
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
            
            edge_x, edge_y, edge_z = [], [], []
            for edge in G.edges():
                try:
                    x0, y0, z0 = pos[edge[0]]
                    x1, y1, z1 = pos[edge[1]]
                    edge_x.extend([x0, x1, None])
                    edge_y.extend([y0, y1, None])
                    edge_z.extend([z0, z1, None])
                except:
                    continue
            
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
                        camera=dict(eye=dict(x=1.5, y=1.5, z=1.5))
                    ),
                    height=700,
                    margin=dict(l=0, r=0, t=40, b=0),
                    paper_bgcolor='#f8f9fa'
                )
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
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
                <div style="margin-top: 0.5rem; font-size: 0.85rem; color: #888;">💡 Larger circles indicate higher degree</div>
            </div>
            """, unsafe_allow_html=True)
            
        except Exception as e:
            st.error(f"Error: {str(e)}")
            display_fallback_network(G, node_list)
    else:
        st.warning("Install plotly and networkx for interactive 3D visualization.")
        display_fallback_network(G, node_list)
    
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

# ===== ENTITY PROFILE =====
def render_entity_profile():
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
            st.markdown(f'<span class="status-badge status-high">🔴 {get_text("priority_high")}</span>', unsafe_allow_html=True)
        elif details.get('priority') == 'MEDIUM':
            st.markdown(f'<span class="status-badge status-medium">🟡 {get_text("priority_medium")}</span>', unsafe_allow_html=True)
        else:
            st.markdown(f'<span class="status-badge status-low">🟢 {get_text("priority_low")}</span>', unsafe_allow_html=True)
        
        st.markdown(f"**{get_text('priority_score')}:** {details['priority_score']:.1%}")
        
        st.markdown("---")
        
        st.markdown(f"**📊 {get_text('properties')}:**")
        for key, value in attrs.items():
            st.markdown(f"- **{key}:** {value}")
        
        st.markdown("---")
        
        st.markdown(f"**🔗 {get_text('connections')} ({len(details['connections'])})**")
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
        <div class="quick-stats">
            <h3 style="font-size: 1.2rem; font-weight: 600; color: #1a1a2e; margin-top: 0;">📊 {get_text('quick_stats')}</h3>
            <div class="stat-item">
                <span class="stat-label">{get_text('direct_connections')}</span>
                <span class="stat-value">{len(details['connections'])}</span>
            </div>
            <div class="stat-item">
                <span class="stat-label">{get_text('network_degree')}</span>
                <span class="stat-value">{get_degree(G, entity_id)}</span>
            </div>
            <div class="stat-item">
                <span class="stat-label">{get_text('priority_score')}</span>
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
        
        st.markdown("""
        <div style="background: white; padding: 1.5rem; border-radius: 15px; box-shadow: 0 4px 20px rgba(0,0,0,0.08);">
            <h3 style="font-size: 1.2rem; font-weight: 600; color: #1a1a2e; margin-top: 0;">🎯 Recommendations</h3>
        """, unsafe_allow_html=True)
        
        degree = len(details['connections'])
        if degree >= 5:
            st.warning("🔴 " + get_text('immediate_action'))
            st.markdown("- Assign to senior investigator")
            st.markdown("- Conduct surveillance")
            st.markdown("- Coordinate with other cases")
        elif degree >= 3:
            st.info("🟡 " + get_text('review_required'))
            st.markdown("- Gather additional evidence")
            st.markdown("- Interview connected persons")
        else:
            st.success("🟢 " + get_text('information_only'))
            st.markdown("- Monitor for new connections")
            st.markdown("- Document findings")
        
        st.markdown("</div>", unsafe_allow_html=True)

# ===== TIMELINE =====
def render_timeline():
    st.markdown("""
    <div style="animation: fadeInUp 0.6s ease-out;">
        <h1 style="font-size: 2.5rem; font-weight: 700; color: #1a1a2e;">⏱️ Investigation Timeline</h1>
        <p style="color: #666; margin-top: -0.5rem;">Track network evolution over time</p>
    </div>
    """, unsafe_allow_html=True)
    
    if not st.session_state.data_loaded:
        st.info("👈 Click 'Generate Sample Data' in the sidebar to get started")
        return
    
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
        {"date": dates[8], "event": "🔹 Network expansion detected"},
        {"date": dates[12], "event": "🔹 Priority lead identified"},
        {"date": dates[16], "event": "🔹 Evidence breakthrough found"}
    ]
    
    for event in events:
        col1, col2 = st.columns([1, 4])
        with col1:
            st.caption(event["date"].strftime("%Y-%m-%d"))
        with col2:
            st.markdown(event['event'])

# ===== CROSS-CASE =====
def render_cross_case():
    G = st.session_state.graph
    node_list = get_node_list(G)
    
    st.markdown("""
    <div style="animation: fadeInUp 0.6s ease-out;">
        <h1 style="font-size: 2.5rem; font-weight: 700; color: #1a1a2e;">🔗 Cross-Case Discovery</h1>
        <p style="color: #666; margin-top: -0.5rem;">Uncover hidden connections between cases</p>
    </div>
    """, unsafe_allow_html=True)
    
    if not st.session_state.data_loaded or G is None:
        st.info("👈 Click 'Generate Sample Data' in the sidebar to get started")
        return
    
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
                        st.metric("Total Connections", conn['shared_entities'] * 2)
                    
                    if conn['shared_persons']:
                        st.write("**Shared Persons:**")
                        for person in conn['shared_persons']:
                            attrs = get_node_attributes(G, person)
                            name = attrs.get('name', person)
                            st.markdown(f"- {person} ({name})")
                    
                    st.progress(conn['confidence'], text=f"Confidence: {conn['confidence']:.0%}")
        else:
            st.info("No cross-case connections found.")
    else:
        st.warning("Need at least 2 cases and 1 person.")

# ===== AI COPILOT =====
def render_ai_copilot():
    G = st.session_state.graph
    node_list = get_node_list(G)
    
    st.markdown("""
    <div style="animation: fadeInUp 0.6s ease-out;">
        <h1 style="font-size: 2.5rem; font-weight: 700; color: #1a1a2e;">🤖 AI Copilot</h1>
        <p style="color: #666; margin-top: -0.5rem;">Intelligent investigation assistant</p>
    </div>
    """, unsafe_allow_html=True)
    
    if not st.session_state.data_loaded or G is None:
        st.info("👈 Click 'Generate Sample Data' in the sidebar to get started")
        return
    
    if not has_permission("use_ai"):
        st.warning("🔒 You need 'Analyst' or higher role to use AI Copilot.")
        return
    
    st.info("🧠 Ask questions about your investigation or get AI-generated insights")
    
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
            if user_query:
                st.session_state.ai_query = user_query
                add_audit_log("ai_query", "AI Copilot", f"Query: {user_query[:100]}")
                st.rerun()
            else:
                st.warning("Please enter a question.")
    
    if hasattr(st.session_state, 'ai_query') and st.session_state.ai_query:
        query = st.session_state.ai_query
        
        st.markdown("---")
        st.markdown("### 🤖 AI Response")
        
        with st.spinner("Analyzing network..."):
            response_parts = []
            
            if "person" in query.lower() or "who" in query.lower() or "entity" in query.lower():
                high_degree = []
                for node in node_list:
                    degree = get_degree(G, node)
                    attrs = get_node_attributes(G, node)
                    if attrs.get('type') == 'PERSON' and degree >= 3:
                        high_degree.append((node, degree, attrs.get('name', node)))
                
                if high_degree:
                    high_degree.sort(key=lambda x: x[1], reverse=True)
                    top = high_degree[:5]
                    names = [f"{n} (degree: {d})" for n, d, _ in top]
                    response_parts.append(f"🔍 **Key entities:** {', '.join(names)}")
                else:
                    response_parts.append("🔍 No high-degree entities found.")
            
            if "connection" in query.lower() or "link" in query.lower() or "relationship" in query.lower():
                response_parts.append("🔗 **Cross-case connections detected:** Multiple relationships between cases and persons.")
            
            if "pattern" in query.lower() or "trend" in query.lower() or "activity" in query.lower():
                response_parts.append("📊 **Pattern detection:** Financial transaction patterns suggest potential money laundering.")
            
            if "priority" in query.lower() or "important" in query.lower() or "critical" in query.lower():
                critical = []
                for node in node_list:
                    degree = get_degree(G, node)
                    attrs = get_node_attributes(G, node)
                    if degree >= 5 and attrs.get('type') == 'PERSON':
                        critical.append(node)
                
                if critical:
                    response_parts.append(f"🚨 **Critical entities:** {', '.join(critical[:5])}")
                else:
                    response_parts.append("🚨 No critical entities detected.")
            
            if not response_parts:
                response_parts.append(f"💡 **Network overview:** The network contains {len(node_list)} entities.")
                response_parts.append("📊 Try asking about specific entities, connections, or patterns.")
            
            st.markdown(f"""
            <div class="rag-response">
                <strong>Response:</strong>
                <p style="margin-top: 0.5rem;">{chr(10).join(response_parts)}</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("### 📋 Relevant Entities")
            entities_with_degree = []
            for node in node_list:
                attrs = get_node_attributes(G, node)
                if attrs.get('type') == 'PERSON':
                    degree = get_degree(G, node)
                    entities_with_degree.append((node, degree, attrs.get('name', node)))
            
            entities_with_degree.sort(key=lambda x: x[1], reverse=True)
            for node, degree, name in entities_with_degree[:5]:
                st.markdown(f"- **{node}** ({name}) - Degree: {degree}")
            
            st.warning("⚠️ " + get_text('disclaimer'))
            
            st.session_state.ai_query = ""

# ===== ALERTS =====
def render_alerts():
    st.markdown("""
    <div style="animation: fadeInUp 0.6s ease-out;">
        <h1 style="font-size: 2.5rem; font-weight: 700; color: #1a1a2e;">🔔 Alerts & Emergency</h1>
        <p style="color: #666; margin-top: -0.5rem;">Real-time critical alerts and emergency notifications</p>
    </div>
    """, unsafe_allow_html=True)
    
    if not st.session_state.data_loaded:
        st.info("👈 Click 'Generate Sample Data' in the sidebar to get started")
        return
    
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        if st.button("🚨 Emergency Call", use_container_width=True):
            st.session_state.emergency_triggered = True
            st.session_state.alert_sent = True
            add_audit_log("emergency", "Alert System", "Emergency triggered")
            st.rerun()
    
    with col2:
        if st.button("📞 Call Now", use_container_width=True):
            st.success("📞 Emergency call initiated...")
            add_audit_log("call", "Emergency Services", "Call initiated")
    
    with col3:
        if st.button("📨 Send Alert to Team", use_container_width=True):
            st.session_state.alert_sent = True
            add_audit_log("alert_sent", "Alert System", "Alert sent to team")
            st.success("✅ Alert sent to all investigators!")
    
    if st.session_state.emergency_triggered:
        st.markdown("""
        <div class="alert-card-critical" style="text-align: center; padding: 2rem;">
            <div style="font-size: 3rem;">🚨</div>
            <h2 style="color: white;">EMERGENCY ALERT ACTIVATED</h2>
            <p style="color: rgba(255,255,255,0.9);">All investigators have been notified. Emergency services are being contacted.</p>
            <div style="margin-top: 1rem; display: flex; gap: 10px; justify-content: center; flex-wrap: wrap;">
                <span style="background: rgba(255,255,255,0.2); padding: 8px 20px; border-radius: 50px;">🚔 Police Dispatched</span>
                <span style="background: rgba(255,255,255,0.2); padding: 8px 20px; border-radius: 50px;">📞 Emergency Services Notified</span>
                <span style="background: rgba(255,255,255,0.2); padding: 8px 20px; border-radius: 50px;">📨 Team Alerted</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.session_state.emergency_triggered = False
    
    if st.session_state.alert_sent:
        st.success("✅ Alert sent to all investigators!")
        st.session_state.alert_sent = False
    
    st.markdown("---")
    
    col1, col2 = st.columns([3, 1])
    with col2:
        if st.button("🔄 Refresh Alerts", use_container_width=True):
            st.session_state.alerts = generate_alerts(st.session_state.graph)
            add_audit_log("refresh", "Alerts", "Alerts refreshed")
            st.rerun()
    
    st.markdown("---")
    
    alerts = st.session_state.alerts
    
    if alerts:
        critical_count = len([a for a in alerts if a['type'] == 'CRITICAL'])
        warning_count = len([a for a in alerts if a['type'] == 'WARNING'])
        info_count = len([a for a in alerts if a['type'] == 'INFO'])
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("🔴 Critical Alerts", critical_count, delta="Immediate Action")
        with col2:
            st.metric("🟡 Warnings", warning_count, delta="Review Required")
        with col3:
            st.metric("🔵 Information", info_count, delta="Info")
        
        st.markdown("---")
        
        for alert in alerts:
            if alert['type'] == 'CRITICAL':
                card_class = "alert-card-critical"
                icon = "🚨"
            elif alert['type'] == 'WARNING':
                card_class = "alert-card-warning"
                icon = "⚠️"
            else:
                card_class = "alert-card-info"
                icon = "ℹ️"
            
            st.markdown(f"""
            <div class="{card_class}">
                <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap;">
                    <div>
                        <span style="font-size: 1.2rem; font-weight: 700;">{icon} {alert['title']}</span>
                        <br>
                        <span style="opacity: 0.9;">{alert['description']}</span>
                    </div>
                    <div style="text-align: right;">
                        <span style="font-size: 0.7rem; opacity: 0.8;">{alert['timestamp'][:19]}</span>
                    </div>
                </div>
                <div style="margin-top: 0.5rem; border-top: 1px solid rgba(255,255,255,0.1); padding-top: 0.5rem;">
                    <span style="font-weight: 600;">Action:</span> {alert['action']}
                    {f"<br>Entity: {alert['entity']}" if alert.get('entity') else ""}
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No active alerts.")

# ===== SIMULATION =====
def render_simulation():
    G = st.session_state.graph
    node_list = get_node_list(G)
    
    st.markdown("""
    <div style="animation: fadeInUp 0.6s ease-out;">
        <h1 style="font-size: 2.5rem; font-weight: 700; color: #1a1a2e;">🎯 What-If Simulation</h1>
        <p style="color: #666; margin-top: -0.5rem;">Simulate network disruption scenarios</p>
    </div>
    """, unsafe_allow_html=True)
    
    if not st.session_state.data_loaded or G is None:
        st.info("👈 Click 'Generate Sample Data' in the sidebar to get started")
        return
    
    if not st.session_state.authenticated:
        st.warning("🔒 Please login to access this feature.")
        return
    
    if not node_list:
        st.warning(get_text('no_data'))
        return
    
    col1, col2 = st.columns([2, 1])
    with col1:
        target_entity = st.selectbox("🎯 Select Entity to Remove", node_list)
    with col2:
        if st.button("🚀 Run Simulation", use_container_width=True):
            with st.spinner("Running simulation..."):
                results = generate_simulation(G, target_entity)
                st.session_state.simulation_results = results
                add_audit_log("simulation", target_entity, "Simulation run")
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
        
        impact = results['network_disruption']
        color = '#ff4757' if impact > 0.5 else '#ffa502' if impact > 0.3 else '#2ed573'
        label = 'HIGH' if impact > 0.5 else 'MEDIUM' if impact > 0.3 else 'LOW'
        
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #f8f9fa, #e9ecef); padding: 1.5rem; border-radius: 15px; border: 2px dashed #667eea;">
            <h3>💥 Network Disruption Impact</h3>
            <div style="display: flex; justify-content: space-between; margin: 0.5rem 0;">
                <span>Disruption Level</span>
                <span style="font-weight: 700; color: {color};">{impact:.1%} ({label})</span>
            </div>
            <div style="height: 12px; border-radius: 10px; overflow: hidden; background: #f0f0f0; margin: 0.5rem 0;">
                <div style="height: 100%; width: {impact*100}%; background: linear-gradient(90deg, {color}, {color}cc); border-radius: 10px;"></div>
            </div>
            <div style="margin-top: 0.5rem; color: #888; font-size: 0.85rem;">
                <strong>Recommendation:</strong> {results['recommendation']}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
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

# ===== HEATMAP =====
def render_heatmap():
    G = st.session_state.graph
    node_list = get_node_list(G)
    
    st.markdown("""
    <div style="animation: fadeInUp 0.6s ease-out;">
        <h1 style="font-size: 2.5rem; font-weight: 700; color: #1a1a2e;">🗺️ Geographic Heatmap</h1>
        <p style="color: #666; margin-top: -0.5rem;">Visualize crime hotspots and entity locations</p>
    </div>
    """, unsafe_allow_html=True)
    
    if not st.session_state.data_loaded or G is None:
        st.info("👈 Click 'Generate Sample Data' in the sidebar to get started")
        return
    
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
        heatmap_data = [
            {'ID': 'L-001', 'Name': 'Mumbai', 'Type': 'LOCATION', 'Latitude': 19.0760, 'Longitude': 72.8777, 'Intensity': 85, 'Degree': 12},
            {'ID': 'L-002', 'Name': 'Delhi', 'Type': 'LOCATION', 'Latitude': 28.6139, 'Longitude': 77.2090, 'Intensity': 78, 'Degree': 9},
            {'ID': 'L-003', 'Name': 'Bangalore', 'Type': 'LOCATION', 'Latitude': 12.9716, 'Longitude': 77.5946, 'Intensity': 65, 'Degree': 7},
            {'ID': 'L-004', 'Name': 'Chennai', 'Type': 'LOCATION', 'Latitude': 13.0827, 'Longitude': 80.2707, 'Intensity': 55, 'Degree': 5},
            {'ID': 'L-005', 'Name': 'Hyderabad', 'Type': 'LOCATION', 'Latitude': 17.3850, 'Longitude': 78.4867, 'Intensity': 60, 'Degree': 6},
            {'ID': 'L-006', 'Name': 'Kolkata', 'Type': 'LOCATION', 'Latitude': 22.5726, 'Longitude': 88.3639, 'Intensity': 45, 'Degree': 4},
            {'ID': 'L-007', 'Name': 'Pune', 'Type': 'LOCATION', 'Latitude': 18.5204, 'Longitude': 73.8567, 'Intensity': 40, 'Degree': 3},
        ]
        st.info("💡 Showing sample location data.")
    
    df = pd.DataFrame(heatmap_data)
    st.dataframe(df[['ID', 'Name', 'Type', 'Latitude', 'Longitude', 'Intensity']], use_container_width=True)
    
    st.markdown("---")
    st.markdown("### 🗺️ Interactive Location Map")
    
    if PLOTLY_AVAILABLE:
        try:
            fig = go.Figure()
            
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
                title='Entity Locations Map - India',
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
            
            st.markdown("""
            <div style="background: white; padding: 1rem; border-radius: 12px; margin-top: 1rem; box-shadow: 0 2px 10px rgba(0,0,0,0.05);">
                <h4 style="margin: 0 0 0.5rem 0;">📊 Legend</h4>
                <div style="display: flex; gap: 20px; flex-wrap: wrap;">
                    <div><span style="display: inline-block; width: 20px; height: 20px; background: #ff4757; border-radius: 50%;"></span> High Intensity (70-100)</div>
                    <div><span style="display: inline-block; width: 20px; height: 20px; background: #ffa502; border-radius: 50%;"></span> Medium Intensity (40-70)</div>
                    <div><span style="display: inline-block; width: 20px; height: 20px; background: #2ed573; border-radius: 50%;"></span> Low Intensity (0-40)</div>
                    <div><span style="display: inline-block; width: 20px; height: 20px; border: 2px solid #667eea; border-radius: 50%;"></span> Entity Location</div>
                </div>
                <div style="margin-top: 0.5rem; font-size: 0.85rem; color: #888;">💡 Larger circles indicate higher investigation priority</div>
            </div>
            """, unsafe_allow_html=True)
            
        except Exception as e:
            st.error(f"Error: {str(e)}")
            st.info("Showing data table instead.")
    else:
        st.info("Install plotly for interactive map visualization.")

# ===== EXPORT =====
def render_export():
    st.markdown("""
    <div style="animation: fadeInUp 0.6s ease-out;">
        <h1 style="font-size: 2.5rem; font-weight: 700; color: #1a1a2e;">📄 Export Reports</h1>
        <p style="color: #666; margin-top: -0.5rem;">Generate and download investigation reports</p>
    </div>
    """, unsafe_allow_html=True)
    
    if not st.session_state.data_loaded:
        st.info("👈 Click 'Generate Sample Data' in the sidebar to get started")
        return
    
    if not st.session_state.authenticated:
        st.warning("🔒 Please login to access this feature.")
        return
    
    if not has_permission("export_data"):
        st.warning("🔒 You need 'Analyst' or higher role to export reports.")
        return
    
    st.info("📋 Export investigation data")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📄 Export as JSON", use_container_width=True):
            with st.spinner("Generating report..."):
                G = st.session_state.graph
                node_list = get_node_list(G)
                report = {
                    'generated_at': datetime.now().isoformat(),
                    'total_entities': len(node_list),
                    'entities': []
                }
                for node in node_list:
                    attrs = get_node_attributes(G, node)
                    report['entities'].append({
                        'id': node,
                        'type': attrs.get('type', 'UNKNOWN'),
                        'properties': attrs,
                        'degree': get_degree(G, node)
                    })
                json_str = json.dumps(report, indent=2)
                st.download_button(
                    label="📥 Download JSON",
                    data=json_str,
                    file_name=f"SUTRA-X_Report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json",
                    use_container_width=True
                )
                add_audit_log("export", "JSON Report", "Report exported")
                st.success("✅ JSON Report generated!")
    
    with col2:
        if st.button("📊 Export as CSV", use_container_width=True):
            with st.spinner("Generating report..."):
                G = st.session_state.graph
                node_list = get_node_list(G)
                data = []
                for node in node_list:
                    attrs = get_node_attributes(G, node)
                    data.append({
                        'ID': node,
                        'Type': attrs.get('type', 'UNKNOWN'),
                        'Degree': get_degree(G, node),
                        'Name': attrs.get('name', attrs.get('number', '')),
                        **attrs
                    })
                df = pd.DataFrame(data)
                csv = df.to_csv(index=False)
                st.download_button(
                    label="📥 Download CSV",
                    data=csv,
                    file_name=f"SUTRA-X_Data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv",
                    use_container_width=True
                )
                add_audit_log("export", "CSV Report", "Report exported")
                st.success("✅ CSV Report generated!")
    
    st.markdown("---")
    
    st.markdown("### 📋 Export History")
    if st.session_state.export_history:
        history_df = pd.DataFrame(st.session_state.export_history[-10:])
        st.dataframe(history_df, use_container_width=True)
    else:
        st.info("No export history available.")

# ===== SECURITY =====
def render_security():
    st.markdown("""
    <div style="animation: fadeInUp 0.6s ease-out;">
        <h1 style="font-size: 2.5rem; font-weight: 700; color: #1a1a2e;">🔐 Security & Access Control</h1>
        <p style="color: #666; margin-top: -0.5rem;">Role-Based Access Control and Audit Logs</p>
    </div>
    """, unsafe_allow_html=True)
    
    if not st.session_state.authenticated:
        st.warning("🔒 Please login to access this feature.")
        return
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
        <div style="background: white; padding: 1.5rem; border-radius: 15px; box-shadow: 0 4px 20px rgba(0,0,0,0.08);">
            <h3 style="font-size: 1.2rem; font-weight: 600; color: #1a1a2e;">🔐 Role-Based Access Control</h3>
            <div style="margin-top: 1rem;">
                <div style="display: flex; justify-content: space-between; padding: 0.5rem 0; border-bottom: 1px solid #eee;">
                    <span>Current User</span>
                    <strong>{st.session_state.current_user}</strong>
                </div>
                <div style="display: flex; justify-content: space-between; padding: 0.5rem 0; border-bottom: 1px solid #eee;">
                    <span>Current Role</span>
                    <strong>{st.session_state.user_role.upper()}</strong>
                </div>
                <div style="display: flex; justify-content: space-between; padding: 0.5rem 0;">
                    <span>Permissions</span>
                    <span style="font-size: 0.85rem;">{', '.join(ROLE_PERMISSIONS.get(st.session_state.user_role, []))}</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div style="background: white; padding: 1.5rem; border-radius: 15px; box-shadow: 0 4px 20px rgba(0,0,0,0.08);">
            <h3 style="font-size: 1.2rem; font-weight: 600; color: #1a1a2e;">📶 Offline Mode</h3>
            <div style="margin-top: 1rem;">
                <div style="display: flex; justify-content: space-between; padding: 0.5rem 0; border-bottom: 1px solid #eee;">
                    <span>Status</span>
                    <span>{'📴 Offline' if st.session_state.offline_mode else '📶 Online'}</span>
                </div>
                <div style="display: flex; justify-content: space-between; padding: 0.5rem 0;">
                    <span>Description</span>
                    <span style="font-size: 0.8rem; color: #888;">Work without internet, sync when online</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown("### 📋 Audit Logs")
    
    col1, col2 = st.columns([3, 1])
    with col2:
        if st.button("🔄 Refresh Logs", use_container_width=True):
            st.rerun()
        if st.button("🗑️ Clear Logs", use_container_width=True):
            st.session_state.audit_logs = []
            st.rerun()
    
    st.markdown("---")
    
    if st.session_state.audit_logs:
        audit_df = pd.DataFrame(st.session_state.audit_logs[:20])
        if not audit_df.empty:
            display_df = audit_df[['timestamp', 'user', 'role', 'action', 'resource']].copy()
            display_df['timestamp'] = pd.to_datetime(display_df['timestamp']).dt.strftime('%Y-%m-%d %H:%M:%S')
            st.dataframe(display_df, use_container_width=True)
            
            st.markdown("---")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Logs", len(st.session_state.audit_logs))
            with col2:
                unique_actions = len(audit_df['action'].unique())
                st.metric("Unique Actions", unique_actions)
            with col3:
                unique_users = len(audit_df['user'].unique())
                st.metric("Active Users", unique_users)
    else:
        st.info("No audit logs available.")

# ============================================================================
# MAIN ROUTER
# ============================================================================

def main():
    page = st.session_state.current_page
    
    if page == "Dashboard":
        render_dashboard()
    elif page == "Network Graph":
        render_network_graph()
    elif page == "Entity Profile":
        render_entity_profile()
    elif page == "Timeline":
        render_timeline()
    elif page == "Cross-Case Discovery":
        render_cross_case()
    elif page == "AI Copilot":
        render_ai_copilot()
    elif page == "Alerts & Emergency":
        render_alerts()
    elif page == "What-If Simulation":
        render_simulation()
    elif page == "Heatmap":
        render_heatmap()
    elif page == "Export":
        render_export()
    elif page == "Security":
        render_security()
    else:
        render_dashboard()

# ============================================================================
# FOOTER
# ============================================================================

st.markdown(f"""
<div class="footer">
    <div style="display: flex; justify-content: center; gap: 20px; flex-wrap: wrap; margin-bottom: 10px;">
        <span>🏆 SIH 2026</span>
        <span>|</span>
        <span>🕵️ SUTRA-X {get_text('version')}</span>
        <span>|</span>
        <span>🌐 {LANGUAGES[st.session_state.language]['name']}</span>
        <span>|</span>
        <span>👤 {st.session_state.user_role.upper() if st.session_state.authenticated else 'Guest'}</span>
    </div>
    <div style="font-size: 0.8rem; color: #aaa;">
        {get_text('made_with')}
    </div>
</div>
""", unsafe_allow_html=True)

# ============================================================================
# RUN APP
# ============================================================================

if __name__ == "__main__":
    main()
