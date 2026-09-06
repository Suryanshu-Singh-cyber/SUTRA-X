"""
SUTRA-X PHASE 3: Complete Criminal Network Intelligence Platform
SIH 2026 | AI-Powered Criminal Network Analysis System
Single File - No Import Errors
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
# MULTI-LANGUAGE SUPPORT
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
        "network_stats": "Network Statistics",
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
        "call_now": "📞 Call Now",
        "alert_details": "Alert Details",
        "action_required": "Action Required",
        "immediate_action": "Immediate investigation required",
        "review_required": "Review Required",
        "information_only": "Information Only",
        "no_alerts": "No active alerts",
        "refresh_alerts": "Refresh Alerts",
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
        "key_events": "Key Events",
        "ai_title": "AI Copilot",
        "ai_sub": "Intelligent investigation assistant",
        "quick_questions": "Quick Questions",
        "custom_query": "Custom Query",
        "analyze": "Analyze",
        "ask_question": "Ask your question",
        "ai_response": "AI Response",
        "key_findings": "Key Findings",
        "actionable_insights": "Actionable Insights",
        "next_steps": "Next Steps",
        "relevant_entities": "Relevant Entities",
        "disclaimer": "This is an AI-generated analysis. All findings should be verified by human investigators.",
        "made_with": "Made with ❤️ for Smart India Hackathon 2026",
        "version": "v3.0.0",
        "emergency_title": "🚨 EMERGENCY ALERT",
        "emergency_desc": "Critical threat detected in the network",
        "call_police": "🚔 Call Police",
        "call_emergency": "📞 Emergency Services",
        "send_alert": "📨 Send Alert to Team",
        "alert_sent": "✅ Alert sent to all investigators!",
        "call_initiated": "📞 Emergency call initiated...",
        "online": "Online",
        "offline": "Offline",
        "data_loaded": "Data Loaded",
        "no_data_loaded": "No data loaded",
        "heatmap_title": "Geographic Heatmap",
        "heatmap_sub": "Visualize crime hotspots and patterns",
        "export_title": "Export Reports",
        "export_sub": "Generate and download investigation reports",
        "export_pdf": "Export as PDF",
        "export_word": "Export as Word",
        "export_json": "Export as JSON",
        "security_title": "Security & Access Control",
        "security_sub": "Role-Based Access Control and Audit Logs",
        "user_role": "User Role",
        "audit_logs": "Audit Logs",
        "rbac_info": "Role-Based Access Control",
        "offline_mode": "Offline Mode",
        "offline_desc": "Work without internet, sync when online",
        "rag_context": "RAG Context",
        "rag_sources": "Sources",
        "rag_confidence": "Confidence",
        "export_history": "Export History",
        "generated_at": "Generated At",
        "file_name": "File Name",
        "download": "Download",
        "heatmap_intensity": "Intensity",
        "heatmap_locations": "Locations",
        "login": "Login",
        "username": "Username",
        "password": "Password",
        "logout": "Logout",
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
            "simulation": "Simulation Run"
        }
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
        "network_stats": "नेटवर्क आंकड़े",
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
        "call_now": "📞 अभी कॉल करें",
        "alert_details": "अलर्ट विवरण",
        "action_required": "आवश्यक कार्रवाई",
        "immediate_action": "तत्काल जांच आवश्यक",
        "review_required": "समीक्षा आवश्यक",
        "information_only": "केवल सूचना",
        "no_alerts": "कोई सक्रिय अलर्ट नहीं",
        "refresh_alerts": "अलर्ट रिफ्रेश करें",
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
        "key_events": "मुख्य घटनाएं",
        "ai_title": "एआई सहायक",
        "ai_sub": "बुद्धिमान जांच सहायक",
        "quick_questions": "त्वरित प्रश्न",
        "custom_query": "कस्टम प्रश्न",
        "analyze": "विश्लेषण करें",
        "ask_question": "अपना प्रश्न पूछें",
        "ai_response": "एआई प्रतिक्रिया",
        "key_findings": "मुख्य निष्कर्ष",
        "actionable_insights": "कार्रवाई योग्य अंतर्दृष्टि",
        "next_steps": "अगले कदम",
        "relevant_entities": "प्रासंगिक इकाइयां",
        "disclaimer": "यह एक एआई-जनित विश्लेषण है। सभी निष्कर्षों को मानव जांचकर्ताओं द्वारा सत्यापित किया जाना चाहिए।",
        "made_with": "स्मार्ट इंडिया हैकथॉन 2026 के लिए ❤️ के साथ बनाया गया",
        "version": "v3.0.0",
        "emergency_title": "🚨 आपातकालीन अलर्ट",
        "emergency_desc": "नेटवर्क में गंभीर खतरा पाया गया",
        "call_police": "🚔 पुलिस को कॉल करें",
        "call_emergency": "📞 आपातकालीन सेवाएं",
        "send_alert": "📨 टीम को अलर्ट भेजें",
        "alert_sent": "✅ सभी जांचकर्ताओं को अलर्ट भेजा गया!",
        "call_initiated": "📞 आपातकालीन कॉल शुरू की गई...",
        "online": "ऑनलाइन",
        "offline": "ऑफलाइन",
        "data_loaded": "डेटा लोड हुआ",
        "no_data_loaded": "कोई डेटा लोड नहीं",
        "heatmap_title": "भौगोलिक हीटमैप",
        "heatmap_sub": "अपराध हॉटस्पॉट और पैटर्न देखें",
        "export_title": "रिपोर्ट निर्यात",
        "export_sub": "जांच रिपोर्ट जनरेट और डाउनलोड करें",
        "export_pdf": "PDF के रूप में निर्यात करें",
        "export_word": "Word के रूप में निर्यात करें",
        "export_json": "JSON के रूप में निर्यात करें",
        "security_title": "सुरक्षा और पहुंच नियंत्रण",
        "security_sub": "रोल-आधारित पहुंच नियंत्रण और ऑडिट लॉग",
        "user_role": "उपयोगकर्ता भूमिका",
        "audit_logs": "ऑडिट लॉग",
        "rbac_info": "रोल-आधारित पहुंच नियंत्रण",
        "offline_mode": "ऑफलाइन मोड",
        "offline_desc": "इंटरनेट के बिना काम करें, ऑनलाइन होने पर सिंक करें",
        "rag_context": "RAG संदर्भ",
        "rag_sources": "स्रोत",
        "rag_confidence": "विश्वास",
        "export_history": "निर्यात इतिहास",
        "generated_at": "जनरेट किया गया",
        "file_name": "फ़ाइल नाम",
        "download": "डाउनलोड",
        "heatmap_intensity": "तीव्रता",
        "heatmap_locations": "स्थान",
        "login": "लॉगिन",
        "username": "उपयोगकर्ता नाम",
        "password": "पासवर्ड",
        "logout": "लॉगआउट",
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
            "simulation": "सिमुलेशन चलाएं"
        }
    }
}

def get_text(key):
    lang = st.session_state.get('language', 'en')
    if lang in LANGUAGES and key in LANGUAGES[lang]:
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
# GRAPH CLASS
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
    
    locations_list = ['Mumbai', 'Delhi', 'Bangalore', 'Chennai', 'Hyderabad', 'Pune', 
                      'Kolkata', 'Ahmedabad', 'Lucknow', 'Jaipur']
    
    num_persons = 30
    persons = []
    for i in range(num_persons):
        name = f"{random.choice(first_names)} {random.choice(last_names)}"
        person_id = f"P-{i+1:04d}"
        G.add_node(person_id, type='PERSON', name=name, 
                   age=random.randint(22, 60),
                   city=random.choice(locations_list),
                   occupation=random.choice(['Business', 'Student', 'Government', 'Private', 'Professional']))
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
        G.add_node(account_id, type='ACCOUNT', 
                   bank=random.choice(['SBI', 'HDFC', 'ICICI', 'Axis', 'PNB']))
        accounts.append(account_id)
        owner = random.choice(persons)
        G.add_edge(owner, account_id, type='OWNS', confidence=0.7)
    
    vehicles = []
    vehicle_prefixes = ['MH', 'DL', 'KA', 'TN', 'TS', 'GJ']
    for i in range(10):
        vehicle_id = f"V-{i+1:04d}"
        reg = f"{random.choice(vehicle_prefixes)}{random.randint(1,99)} {random.choice(['AB','CD','EF','GH'])}{random.randint(1000,9999)}"
        G.add_node(vehicle_id, type='VEHICLE', registration=reg,
                   make=random.choice(['Maruti', 'Hyundai', 'Toyota', 'Honda']))
        vehicles.append(vehicle_id)
        owner = random.choice(persons)
        G.add_edge(owner, vehicle_id, type='OWNS', confidence=0.6)
    
    locations = []
    location_names = ['Connaught Place', 'Bandra West', 'Indiranagar', 'T. Nagar', 
                      'Hitech City', 'Juhu', 'Koramangala', 'Marine Drive']
    for i in range(8):
        loc_id = f"L-{i+1:04d}"
        G.add_node(loc_id, type='LOCATION', 
                   name=location_names[i] if i < len(location_names) else f"Location {i+1}",
                   city=random.choice(locations_list))
        locations.append(loc_id)
    
    cases = []
    case_titles = ['Drug Trafficking Ring', 'Financial Fraud Network', 'Arms Dealing', 
                   'Cyber Crime Syndicate', 'Money Laundering', 'Human Trafficking']
    for i in range(6):
        case_id = f"CASE-{i+1:03d}"
        G.add_node(case_id, type='CASE', 
                   title=case_titles[i] if i < len(case_titles) else f"Case {i+1}",
                   status=random.choice(['Active', 'Pending', 'Under Review']))
        cases.append(case_id)
        for _ in range(random.randint(2, 5)):
            person = random.choice(persons)
            G.add_edge(case_id, person, type='INVOLVED', confidence=0.6 + random.random()*0.3)
    
    for _ in range(30):
        caller = random.choice(phones)
        receiver = random.choice(phones)
        if caller != receiver:
            G.add_edge(caller, receiver, type='CALLED', 
                      duration=random.randint(30, 600))
    
    for _ in range(25):
        from_acc = random.choice(accounts)
        to_acc = random.choice(accounts)
        if from_acc != to_acc:
            amount = random.randint(5000, 500000)
            G.add_edge(from_acc, to_acc, type='TRANSACTION', amount=amount)
    
    for _ in range(20):
        person = random.choice(persons)
        location = random.choice(locations)
        G.add_edge(person, location, type='VISITED')
    
    for _ in range(8):
        person = random.choice(persons)
        case = random.choice(cases)
        try:
            if not G.has_edge(person, case):
                G.add_edge(person, case, type='INVOLVED', confidence=0.5 + random.random()*0.4)
        except:
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
                'title': f'Critical Entity Detected: {node}',
                'description': f'Entity {node} has {degree} connections',
                'entity': node,
                'timestamp': datetime.now().isoformat(),
                'action': 'Immediate investigation required',
                'emergency': True
            })
    
    case_nodes = [n for n in node_list if get_node_attributes(G, n).get('type') == 'CASE']
    for case in case_nodes:
        neighbors = get_neighbors(G, case)
        person_neighbors = [n for n in neighbors if get_node_attributes(G, n).get('type') == 'PERSON']
        if len(person_neighbors) >= 4:
            alerts.append({
                'id': f"ALERT-{len(alerts)+1:04d}",
                'type': 'WARNING',
                'title': f'Cross-Case Connection: {case}',
                'description': f'Case {case} connected to {len(person_neighbors)} persons',
                'entity': case,
                'timestamp': datetime.now().isoformat(),
                'action': 'Review case connections',
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
# DISPLAY FUNCTIONS
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
# CSS
# ============================================================================

st.markdown("""
<style>
    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(30px); }
        to { opacity: 1; transform: translateY(0); }
    }
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
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
    
    .hero-section {
        background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
        padding: 2rem 3rem;
        border-radius: 20px;
        margin-bottom: 2rem;
        border: 1px solid rgba(102, 126, 234, 0.2);
    }
    .hero-title {
        font-size: 3rem;
        font-weight: 800;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 30%, #f093fb 60%, #f5576c 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: -1px;
    }
    .hero-subtitle {
        font-size: 1.2rem;
        color: rgba(255,255,255,0.7);
        margin-top: 0.5rem;
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
    }
    .ps-badge-hero {
        display: inline-block;
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        padding: 8px 24px;
        border-radius: 50px;
        font-size: 0.9rem;
        font-weight: 700;
    }
    .phase-badge-hero {
        display: inline-block;
        background: linear-gradient(135deg, #f093fb, #f5576c);
        color: white;
        padding: 8px 20px;
        border-radius: 50px;
        font-size: 0.8rem;
        font-weight: 700;
    }
    
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        border-left: 5px solid #667eea;
        transition: all 0.3s ease;
        animation: fadeInUp 0.6s ease-out;
    }
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 30px rgba(0,0,0,0.15);
    }
    .metric-card .icon { font-size: 2rem; margin-bottom: 0.5rem; }
    .metric-card .value { font-size: 2rem; font-weight: 700; color: #1a1a2e; }
    .metric-card .label { font-size: 0.9rem; color: #666; }
    
    .status-badge {
        padding: 4px 16px;
        border-radius: 50px;
        font-size: 0.8rem;
        font-weight: 600;
        display: inline-block;
    }
    .status-high { background: #ff6b6b; color: white; }
    .status-medium { background: #feca57; color: #333; }
    .status-low { background: #48dbfb; color: #333; }
    
    .entity-card {
        background: #f8f9fa;
        padding: 1rem 1.2rem;
        border-radius: 12px;
        margin: 0.5rem 0;
        border-left: 4px solid #667eea;
        transition: all 0.3s ease;
    }
    .entity-card:hover {
        background: #f0f2f6;
        transform: translateX(5px);
    }
    
    .alert-card-critical {
        background: linear-gradient(135deg, #ff4757, #ff6b6b);
        color: white;
        padding: 1.2rem;
        border-radius: 12px;
        margin: 0.5rem 0;
        animation: pulse 2s infinite;
    }
    .alert-card-warning {
        background: linear-gradient(135deg, #ffa502, #feca57);
        color: white;
        padding: 1.2rem;
        border-radius: 12px;
        margin: 0.5rem 0;
    }
    .alert-card-info {
        background: linear-gradient(135deg, #2ed573, #48dbfb);
        color: white;
        padding: 1.2rem;
        border-radius: 12px;
        margin: 0.5rem 0;
    }
    
    .section-divider {
        height: 2px;
        background: linear-gradient(90deg, transparent, #667eea, #764ba2, transparent);
        margin: 2rem 0;
    }
    
    .glow-card {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        border: 1px solid rgba(102,126,234,0.1);
        transition: all 0.3s ease;
        height: 100%;
    }
    .glow-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 30px rgba(102,126,234,0.2);
    }
    
    .rag-response {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 4px solid #667eea;
        margin: 0.5rem 0;
    }
    
    .footer {
        text-align: center;
        padding: 1.5rem 0;
        color: #888;
        font-size: 0.85rem;
        border-top: 1px solid #eee;
        margin-top: 2rem;
    }
    
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
        <div style="font-size: 0.7rem; color: #888;">Smart Unified Threat & Relationship Analytics</div>
        <div style="margin-top: 8px;">
            <span style="display: inline-block; background: linear-gradient(135deg, #ff6b6b, #ee5a24); color: white; padding: 4px 12px; border-radius: 50px; font-size: 0.7rem;">🏆 SIH 2026</span>
            <span style="display: inline-block; background: linear-gradient(135deg, #f093fb, #f5576c); color: white; padding: 3px 10px; border-radius: 50px; font-size: 0.6rem;">PHASE 3</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Language
    st.markdown("### 🌐 Language")
    lang_options = {code: f"{data['flag']} {data['name']}" for code, data in LANGUAGES.items()}
    selected_lang = st.selectbox("Select Language", options=list(lang_options.keys()), 
                                  format_func=lambda x: lang_options[x],
                                  index=list(lang_options.keys()).index(st.session_state.language))
    if selected_lang != st.session_state.language:
        st.session_state.language = selected_lang
        st.rerun()
    
    st.markdown("---")
    
    # Authentication
    st.markdown("### 🔐 Security")
    
    if not st.session_state.authenticated:
        username = st.text_input(get_text('username'))
        password = st.text_input(get_text('password'), type="password")
        if st.button(get_text('login'), use_container_width=True):
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
        if st.button(get_text('logout'), use_container_width=True):
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
            st.markdown('<span style="display: inline-block; padding: 4px 12px; border-radius: 50px; font-size: 0.7rem; font-weight: 600; background: #ffa50220; color: #ffa502;">📴 OFFLINE</span>', unsafe_allow_html=True)
        else:
            st.markdown('<span style="display: inline-block; padding: 4px 12px; border-radius: 50px; font-size: 0.7rem; font-weight: 600; background: #2ed57320; color: #2ed573;">📶 ONLINE</span>', unsafe_allow_html=True)
    else:
        st.info("⏳ No data loaded")
    
    st.markdown("---")
    st.caption("v3.0.0 | Made with ❤️")

# ============================================================================
# HERO SECTION
# ============================================================================

st.markdown("""
<div class="hero-section">
    <div style="display: flex; gap: 12px; flex-wrap: wrap; margin-bottom: 1rem;">
        <span class="sih-badge-hero">🏆 SIH 2026</span>
        <span class="ps-badge-hero">AI-Powered Criminal Network Analysis</span>
        <span class="phase-badge-hero">⚡ PHASE 3</span>
    </div>
    <div class="hero-title">🕵️ SUTRA-X</div>
    <div class="hero-subtitle">Smart Unified Threat & Relationship Analytics</div>
</div>
""", unsafe_allow_html=True)

# ============================================================================
# MAIN FUNCTION
# ============================================================================

def main():
    """Main application router"""
    
    if not st.session_state.data_loaded or st.session_state.graph is None:
        # Landing Page
        st.markdown("""
        <div style="text-align: center; padding: 3rem 1rem; animation: fadeInUp 1s ease-out;">
            <div style="font-size: 4rem; margin-bottom: 1rem; animation: float 3s ease-in-out infinite;">🕵️</div>
            <h2 style="font-size: 2rem; font-weight: 700; color: #1a1a2e;">Welcome to SUTRA-X</h2>
            <p style="color: #666; font-size: 1.1rem; max-width: 600px; margin: 0 auto;">
                AI-powered criminal network analysis platform
            </p>
            <div style="margin-top: 2rem; display: flex; gap: 10px; justify-content: center; flex-wrap: wrap;">
                <span style="background: linear-gradient(135deg, #ff6b6b, #ee5a24); color: white; padding: 8px 20px; border-radius: 50px; font-weight: 600;">🤖 AI Copilot</span>
                <span style="background: linear-gradient(135deg, #667eea, #764ba2); color: white; padding: 8px 20px; border-radius: 50px; font-weight: 600;">🗺️ Heatmap</span>
                <span style="background: linear-gradient(135deg, #f093fb, #f5576c); color: white; padding: 8px 20px; border-radius: 50px; font-weight: 600;">🔐 RBAC</span>
                <span style="background: linear-gradient(135deg, #2ed573, #26de81); color: white; padding: 8px 20px; border-radius: 50px; font-weight: 600;">📄 Export</span>
            </div>
            <div style="margin-top: 2rem; color: #888;">
                👈 Click "Generate Sample Data" in the sidebar to get started
            </div>
        </div>
        """, unsafe_allow_html=True)
        return
    
    # Main content
    G = st.session_state.graph
    node_list = get_node_list(G)
    metrics = analyze_network(G)
    current_page = st.session_state.current_page
    
    # ========================================================================
    # DASHBOARD
    # ========================================================================
    if current_page == "Dashboard":
        st.markdown(f"""
        <div style="animation: fadeInUp 0.6s ease-out;">
            <h1 style="font-size: 2.5rem; font-weight: 700; color: #1a1a2e;">📊 {get_text('dashboard_title')}</h1>
            <p style="color: #666; margin-top: -0.5rem;">{get_text('dashboard_sub')}</p>
        </div>
        """, unsafe_allow_html=True)
        
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
    
    # ========================================================================
    # NETWORK GRAPH
    # ========================================================================
    elif current_page == "Network Graph":
        st.markdown(f"""
        <div style="animation: fadeInUp 0.6s ease-out;">
            <h1 style="font-size: 2.5rem; font-weight: 700; color: #1a1a2e;">🌐 {get_text('nav_graph')}</h1>
            <p style="color: #666; margin-top: -0.5rem;">Interactive network visualization</p>
        </div>
        """, unsafe_allow_html=True)
        
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
                st.error(f"Error: {str(e)}")
                display_fallback_network(G, node_list)
        else:
            st.warning("Showing network data view. Install plotly and networkx for interactive visualization.")
            display_fallback_network(G, node_list)
        
        st.markdown("---")
        col1, col2 = st.columns([2, 1])
        with col1:
            if node_list:
                selected = st.selectbox(f"🔍 {get_text('search_entity')}", node_list)
            else:
                selected = None
        with col2:
            if selected and st.button(f"👤 {get_text('view_profile')}", use_container_width=True):
                st.session_state.selected_entity = selected
                st.session_state.current_page = "Entity Profile"
                st.rerun()
    
    # ========================================================================
    # ENTITY PROFILE
    # ========================================================================
    elif current_page == "Entity Profile":
        st.markdown(f"""
        <div style="animation: fadeInUp 0.6s ease-out;">
            <h1 style="font-size: 2.5rem; font-weight: 700; color: #1a1a2e;">👤 {get_text('entity_intelligence')}</h1>
        </div>
        """, unsafe_allow_html=True)
        
        if not node_list:
            st.warning(get_text('no_data'))
        else:
            if st.session_state.selected_entity and st.session_state.selected_entity in node_list:
                entity_id = st.session_state.selected_entity
            else:
                entity_id = st.selectbox(f"🔍 {get_text('search_entity')}", node_list)
                st.session_state.selected_entity = entity_id
            
            if entity_id and entity_id in node_list:
                details = get_entity_details(G, entity_id)
                
                if details:
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
                        <div style="background: white; padding: 1.5rem; border-radius: 15px; box-shadow: 0 4px 20px rgba(0,0,0,0.08);">
                            <h3 style="font-size: 1.2rem; font-weight: 600; color: #1a1a2e;">📊 {get_text('quick_stats')}</h3>
                            <div style="margin-top: 1rem;">
                                <div style="display: flex; justify-content: space-between; padding: 0.5rem 0; border-bottom: 1px solid #eee;">
                                    <span>{get_text('direct_connections')}</span>
                                    <strong>{len(details['connections'])}</strong>
                                </div>
                                <div style="display: flex; justify-content: space-between; padding: 0.5rem 0; border-bottom: 1px solid #eee;">
                                    <span>{get_text('network_degree')}</span>
                                    <strong>{get_degree(G, entity_id)}</strong>
                                </div>
                                <div style="display: flex; justify-content: space-between; padding: 0.5rem 0;">
                                    <span>{get_text('priority_score')}</span>
                                    <strong>{details['priority_score']:.1%}</strong>
                                </div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        st.markdown("---")
                        
                        st.markdown(f"""
                        <div style="background: white; padding: 1.5rem; border-radius: 15px; box-shadow: 0 4px 20px rgba(0,0,0,0.08);">
                            <h3 style="font-size: 1.2rem; font-weight: 600; color: #1a1a2e;">📄 {get_text('evidence')}</h3>
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
                        
                        st.markdown(f"""
                        <div style="background: white; padding: 1.5rem; border-radius: 15px; box-shadow: 0 4px 20px rgba(0,0,0,0.08);">
                            <h3 style="font-size: 1.2rem; font-weight: 600; color: #1a1a2e;">🎯 {get_text('recommendations')}</h3>
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
    
    # ========================================================================
    # TIMELINE
    # ========================================================================
    elif current_page == "Timeline":
        st.markdown(f"""
        <div style="animation: fadeInUp 0.6s ease-out;">
            <h1 style="font-size: 2.5rem; font-weight: 700; color: #1a1a2e;">⏱️ {get_text('timeline_title')}</h1>
            <p style="color: #666; margin-top: -0.5rem;">{get_text('timeline_sub')}</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.info("📈 " + get_text('timeline_sub'))
        
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
                name=get_text('total_entities'),
                line=dict(color='#667eea', width=3),
                marker=dict(size=8)
            ))
            fig.add_trace(go.Scatter(
                x=timeline_df['Date'], 
                y=timeline_df['Relationships'],
                mode='lines+markers',
                name=get_text('relationships'),
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
        st.markdown(f"### 📌 {get_text('key_events')}")
        
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
    
    # ========================================================================
    # CROSS-CASE
    # ========================================================================
    elif current_page == "Cross-Case Discovery":
        st.markdown(f"""
        <div style="animation: fadeInUp 0.6s ease-out;">
            <h1 style="font-size: 2.5rem; font-weight: 700; color: #1a1a2e;">🔗 {get_text('crosscase_title')}</h1>
            <p style="color: #666; margin-top: -0.5rem;">{get_text('crosscase_sub')}</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.info("🔍 " + get_text('crosscase_sub'))
        
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
                            st.metric(get_text('shared_entities'), conn['shared_entities'])
                        with col2:
                            st.metric(get_text('confidence'), f"{conn['confidence']:.0%}")
                        with col3:
                            st.metric(get_text('total_connections'), conn['shared_entities'] * 2)
                        
                        if conn['shared_persons']:
                            st.write(f"**👤 {get_text('shared_persons')}:**")
                            for person in conn['shared_persons']:
                                attrs = get_node_attributes(G, person)
                                name = attrs.get('name', person)
                                st.markdown(f"- {person} ({name})")
                        
                        st.progress(conn['confidence'], text=f"{get_text('confidence')}: {conn['confidence']:.0%}")
            else:
                st.info("No cross-case connections found.")
        else:
            st.warning("Need at least 2 cases and 1 person.")
    
    # ========================================================================
    # AI COPILOT
    # ========================================================================
    elif current_page == "AI Copilot":
        st.markdown(f"""
        <div style="animation: fadeInUp 0.6s ease-out;">
            <h1 style="font-size: 2.5rem; font-weight: 700; color: #1a1a2e;">🤖 {get_text('ai_title')}</h1>
            <p style="color: #666; margin-top: -0.5rem;">{get_text('ai_sub')}</p>
        </div>
        """, unsafe_allow_html=True)
        
        if not has_permission("use_ai"):
            st.warning("🔒 You need 'Analyst' or higher role to use AI Copilot.")
        else:
            st.info("🧠 " + get_text('ai_sub'))
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"### 💬 {get_text('quick_questions')}")
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
                st.markdown(f"### 🔍 {get_text('custom_query')}")
                user_query = st.text_area(
                    get_text('ask_question'),
                    placeholder="Example: What are the connections between Entity A and Entity B?",
                    height=150
                )
                if st.button(f"🔍 {get_text('analyze')}", use_container_width=True):
                    if user_query:
                        st.session_state.ai_query = user_query
                        st.rerun()
            
            if hasattr(st.session_state, 'ai_query') and st.session_state.ai_query:
                query = st.session_state.ai_query
                st.markdown("---")
                st.markdown(f"### 🤖 {get_text('ai_response')}")
                
                # Generate response based on query
                response_parts = []
                if "person" in query.lower() or "who" in query.lower():
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
                        response_parts.append(f"🔍 Key entities: {', '.join(names)}")
                
                if "connection" in query.lower() or "link" in query.lower():
                    response_parts.append("🔗 Multiple cross-case connections detected.")
                
                if "pattern" in query.lower() or "trend" in query.lower():
                    response_parts.append("📊 Financial transaction patterns suggest potential money laundering.")
                
                if "priority" in query.lower() or "important" in query.lower():
                    critical = []
                    for node in node_list:
                        degree = get_degree(G, node)
                        attrs = get_node_attributes(G, node)
                        if degree >= 5 and attrs.get('type') == 'PERSON':
                            critical.append(node)
                    if critical:
                        response_parts.append(f"🚨 Critical entities: {', '.join(critical[:5])}")
                
                if not response_parts:
                    response_parts.append(f"💡 The network contains {len(node_list)} entities.")
                    response_parts.append("📊 Try asking about specific entities, connections, or patterns.")
                
                st.markdown(f"""
                <div class="rag-response">
                    <strong>Response:</strong>
                    <p style="margin-top: 0.5rem;">{chr(10).join(response_parts)}</p>
                </div>
                """, unsafe_allow_html=True)
                
                st.warning("⚠️ " + get_text('disclaimer'))
                st.session_state.ai_query = ""
    
    # ========================================================================
    # ALERTS & EMERGENCY
    # ========================================================================
    elif current_page == "Alerts & Emergency":
        st.markdown(f"""
        <div style="animation: fadeInUp 0.6s ease-out;">
            <h1 style="font-size: 2.5rem; font-weight: 700; color: #1a1a2e;">🔔 {get_text('alerts_title')}</h1>
            <p style="color: #666; margin-top: -0.5rem;">{get_text('alerts_sub')}</p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 1, 1])
        with col1:
            if st.button("🚨 " + get_text('emergency_call'), use_container_width=True):
                st.session_state.emergency_triggered = True
                st.session_state.alert_sent = True
                add_audit_log("emergency", "Alert System", "Emergency triggered")
                st.rerun()
        
        with col2:
            if st.button("📞 " + get_text('call_now'), use_container_width=True):
                st.success(get_text('call_initiated'))
        
        with col3:
            if st.button("📨 " + get_text('send_alert'), use_container_width=True):
                st.session_state.alert_sent = True
                add_audit_log("alert_sent", "Alert System", "Alert sent to team")
                st.success(get_text('alert_sent'))
        
        if st.session_state.emergency_triggered:
            st.markdown("""
            <div class="alert-card-critical" style="text-align: center; padding: 2rem;">
                <div style="font-size: 3rem;">🚨</div>
                <h2 style="color: white;">EMERGENCY ALERT ACTIVATED</h2>
                <p style="color: rgba(255,255,255,0.9);">All investigators have been notified.</p>
            </div>
            """, unsafe_allow_html=True)
            st.session_state.emergency_triggered = False
        
        if st.session_state.alert_sent:
            st.success(get_text('alert_sent'))
            st.session_state.alert_sent = False
        
        st.markdown("---")
        
        col1, col2 = st.columns([3, 1])
        with col2:
            if st.button(f"🔄 {get_text('refresh_alerts')}", use_container_width=True):
                st.session_state.alerts = generate_alerts(G)
                st.rerun()
        
        st.markdown("---")
        
        alerts = st.session_state.alerts
        
        if alerts:
            critical_count = len([a for a in alerts if a['type'] == 'CRITICAL'])
            warning_count = len([a for a in alerts if a['type'] == 'WARNING'])
            info_count = len([a for a in alerts if a['type'] == 'INFO'])
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric(f"🔴 {get_text('critical_alerts')}", critical_count)
            with col2:
                st.metric(f"🟡 {get_text('warning_alerts')}", warning_count)
            with col3:
                st.metric(f"🔵 {get_text('info_alerts')}", info_count)
            
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
            st.info(get_text('no_alerts'))
    
    # ========================================================================
    # SIMULATION
    # ========================================================================
    elif current_page == "What-If Simulation":
        st.markdown(f"""
        <div style="animation: fadeInUp 0.6s ease-out;">
            <h1 style="font-size: 2.5rem; font-weight: 700; color: #1a1a2e;">🎯 {get_text('simulation_title')}</h1>
            <p style="color: #666; margin-top: -0.5rem;">{get_text('simulation_sub')}</p>
        </div>
        """, unsafe_allow_html=True)
        
        if not st.session_state.authenticated:
            st.warning("🔒 Please login to access this feature.")
        elif not node_list:
            st.warning(get_text('no_data'))
        else:
            col1, col2 = st.columns([2, 1])
            with col1:
                target_entity = st.selectbox(f"🎯 {get_text('select_entity')}", node_list)
            with col2:
                if st.button(f"🚀 {get_text('run_simulation')}", use_container_width=True):
                    with st.spinner(get_text('loading')):
                        results = generate_simulation(G, target_entity)
                        st.session_state.simulation_results = results
                        add_audit_log("simulation", target_entity, "Simulation run")
                        st.rerun()
            
            if st.session_state.simulation_results:
                results = st.session_state.simulation_results
                
                st.markdown("---")
                st.markdown(f"### 📊 {get_text('simulation_results')}")
                
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric(get_text('target_entity'), results['target_entity'])
                with col2:
                    st.metric(get_text('removed_connections'), results['removed_connections'])
                with col3:
                    st.metric(get_text('remaining_entities'), results['remaining_entities'])
                with col4:
                    st.metric(get_text('isolated_entities'), results['isolated_entities'])
                
                st.markdown("---")
                
                impact = results['network_disruption']
                color = '#ff4757' if impact > 0.5 else '#ffa502' if impact > 0.3 else '#2ed573'
                label = 'HIGH' if impact > 0.5 else 'MEDIUM' if impact > 0.3 else 'LOW'
                
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #f8f9fa, #e9ecef); padding: 1.5rem; border-radius: 15px; border: 2px dashed #667eea;">
                    <h3>💥 {get_text('disruption_impact')}</h3>
                    <div style="display: flex; justify-content: space-between; margin: 0.5rem 0;">
                        <span>{get_text('disruption_level')}</span>
                        <span style="font-weight: 700; color: {color};">{impact:.1%} ({label})</span>
                    </div>
                    <div style="height: 12px; border-radius: 10px; overflow: hidden; background: #f0f0f0; margin: 0.5rem 0;">
                        <div style="height: 100%; width: {impact*100}%; background: linear-gradient(90deg, {color}, {color}cc); border-radius: 10px;"></div>
                    </div>
                    <div style="margin-top: 0.5rem; color: #888; font-size: 0.85rem;">
                        <strong>{get_text('recommendation_label')}:</strong> {results['recommendation']}
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown("---")
                
                st.markdown(f"### 🔗 {get_text('affected_entities')}")
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
    
    # ========================================================================
    # HEATMAP
    # ========================================================================
    elif current_page == "Heatmap":
        st.markdown(f"""
        <div style="animation: fadeInUp 0.6s ease-out;">
            <h1 style="font-size: 2.5rem; font-weight: 700; color: #1a1a2e;">🗺️ {get_text('heatmap_title')}</h1>
            <p style="color: #666; margin-top: -0.5rem;">{get_text('heatmap_sub')}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Show location data
        heatmap_data = []
        for node in node_list:
            attrs = get_node_attributes(G, node)
            if attrs.get('type') in ['PERSON', 'LOCATION']:
                lat = attrs.get('latitude')
                lon = attrs.get('longitude')
                if lat and lon:
                    heatmap_data.append({
                        'ID': node,
                        'Name': attrs.get('name', attrs.get('number', node)),
                        'Type': attrs.get('type'),
                        'Latitude': float(lat),
                        'Longitude': float(lon),
                        'Intensity': min(100, get_degree(G, node) * 10 + 10)
                    })
        
        if heatmap_data:
            st.dataframe(pd.DataFrame(heatmap_data), use_container_width=True)
            
            if PLOTLY_AVAILABLE:
                st.markdown("---")
                st.markdown("### 🗺️ Location Map")
                
                fig = go.Figure()
                fig.add_trace(go.Scattergeo(
                    lon=[d['Longitude'] for d in heatmap_data],
                    lat=[d['Latitude'] for d in heatmap_data],
                    text=[f"{d['Name']}<br>Type: {d['Type']}<br>Intensity: {d['Intensity']}" for d in heatmap_data],
                    mode='markers',
                    marker=dict(
                        size=[d['Intensity']/10 + 5 for d in heatmap_data],
                        color=[d['Intensity'] for d in heatmap_data],
                        colorscale='Reds',
                        showscale=True,
                        colorbar=dict(title="Intensity"),
                        line=dict(width=1, color='white')
                    )
                ))
                
                fig.update_layout(
                    title='Entity Locations Map',
                    geo=dict(
                        scope='asia',
                        projection_type='mercator',
                        center=dict(lat=20.5937, lon=78.9629),
                        lonaxis_range=[68, 98],
                        lataxis_range=[8, 38]
                    ),
                    height=500,
                    margin=dict(l=0, r=0, t=40, b=0)
                )
                
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Install plotly for interactive map visualization.")
        else:
            st.info("No location data available for heatmap.")
    
    # ========================================================================
    # EXPORT
    # ========================================================================
    elif current_page == "Export":
        st.markdown(f"""
        <div style="animation: fadeInUp 0.6s ease-out;">
            <h1 style="font-size: 2.5rem; font-weight: 700; color: #1a1a2e;">📄 {get_text('export_title')}</h1>
            <p style="color: #666; margin-top: -0.5rem;">{get_text('export_sub')}</p>
        </div>
        """, unsafe_allow_html=True)
        
        if not st.session_state.authenticated:
            st.warning("🔒 Please login to access this feature.")
        elif not has_permission("export_data"):
            st.warning("🔒 You need 'Analyst' or higher role to export reports.")
        else:
            st.info("📋 " + get_text('export_sub'))
            
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button(f"📄 JSON Report", use_container_width=True):
                    with st.spinner(get_text('loading')):
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
                if st.button(f"📊 CSV Report", use_container_width=True):
                    with st.spinner(get_text('loading')):
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
            
            st.markdown(f"### 📋 {get_text('export_history')}")
            if st.session_state.export_history:
                history_df = pd.DataFrame(st.session_state.export_history[-10:])
                st.dataframe(history_df, use_container_width=True)
            else:
                st.info("No export history available.")
    
    # ========================================================================
    # SECURITY
    # ========================================================================
    elif current_page == "Security":
        st.markdown(f"""
        <div style="animation: fadeInUp 0.6s ease-out;">
            <h1 style="font-size: 2.5rem; font-weight: 700; color: #1a1a2e;">🔐 {get_text('security_title')}</h1>
            <p style="color: #666; margin-top: -0.5rem;">{get_text('security_sub')}</p>
        </div>
        """, unsafe_allow_html=True)
        
        if not st.session_state.authenticated:
            st.warning("🔒 Please login to access this feature.")
        else:
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(f"""
                <div style="background: white; padding: 1.5rem; border-radius: 15px; box-shadow: 0 4px 20px rgba(0,0,0,0.08);">
                    <h3 style="font-size: 1.2rem; font-weight: 600; color: #1a1a2e;">🔐 {get_text('rbac_info')}</h3>
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
                    <h3 style="font-size: 1.2rem; font-weight: 600; color: #1a1a2e;">📶 {get_text('offline_mode')}</h3>
                    <div style="margin-top: 1rem;">
                        <div style="display: flex; justify-content: space-between; padding: 0.5rem 0; border-bottom: 1px solid #eee;">
                            <span>Status</span>
                            <span>{'📴 Offline' if st.session_state.offline_mode else '📶 Online'}</span>
                        </div>
                        <div style="display: flex; justify-content: space-between; padding: 0.5rem 0;">
                            <span>Description</span>
                            <span style="font-size: 0.8rem; color: #888;">{get_text('offline_desc')}</span>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("---")
            
            st.markdown(f"### 📋 {get_text('audit_logs')}")
            
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
# FOOTER
# ============================================================================

st.markdown(f"""
<div class="footer">
    <div style="display: flex; justify-content: center; gap: 20px; flex-wrap: wrap; margin-bottom: 10px;">
        <span>🏆 SIH 2026</span>
        <span>|</span>
        <span>🕵️ SUTRA-X {get_text('version')}</span>
        <span>|</span>
        <span>⚡ PHASE 3</span>
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
