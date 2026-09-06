"""
SUTRA-X: Smart Unified Threat & Relationship Analytics
Main Application Entry Point
SIH 2026 | AI-Powered Criminal Network Analysis System
"""

import streamlit as st
import sys
import os
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / "app" / "frontend" / "streamlit"))

# Import pages
from pages import (
    dashboard, network_graph, entity_profile, timeline, cross_case,
    ai_copilot, alerts, simulation, heatmap, export, security
)
from components.sidebar import render_sidebar
from backend.data.sample_data import generate_sample_network
from backend.graph_engine.graph_builder import get_node_list
from backend.intelligence_engine.analyzer import generate_alerts
from backend.security.audit import add_audit_log

# Page config
st.set_page_config(
    page_title="SUTRA-X - Criminal Network Intelligence | SIH 2026",
    page_icon="🕵️",
    layout="wide",
    initial_sidebar_state="expanded"
)

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
# CUSTOM CSS - ULTIMATE UI
# ============================================================================

st.markdown("""
<style>
    /* ===== IMPORTS ===== */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    /* ===== ROOT VARIABLES ===== */
    :root {
        --primary: #667eea;
        --primary-dark: #5a67d8;
        --secondary: #764ba2;
        --accent: #f093fb;
        --success: #2ed573;
        --warning: #ffa502;
        --danger: #ff4757;
        --dark: #0f0c29;
        --dark2: #302b63;
        --dark3: #24243e;
        --light: #f8f9fa;
        --white: #ffffff;
        --text-dark: #1a1a2e;
        --text-medium: #4a4a6a;
        --text-light: #8888aa;
    }
    
    /* ===== GLOBAL ===== */
    .main {
        background: #f0f2f6;
    }
    
    /* ===== ANIMATIONS ===== */
    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(30px); }
        to { opacity: 1; transform: translateY(0); }
    }
    @keyframes fadeInDown {
        from { opacity: 0; transform: translateY(-30px); }
        to { opacity: 1; transform: translateY(0); }
    }
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
    @keyframes float {
        0% { transform: translateY(0px); }
        50% { transform: translateY(-12px); }
        100% { transform: translateY(0px); }
    }
    @keyframes shimmer {
        0% { background-position: -200% center; }
        100% { background-position: 200% center; }
    }
    @keyframes glow {
        0% { box-shadow: 0 0 5px rgba(102, 126, 234, 0.2); }
        50% { box-shadow: 0 0 30px rgba(102, 126, 234, 0.5); }
        100% { box-shadow: 0 0 5px rgba(102, 126, 234, 0.2); }
    }
    @keyframes slideInLeft {
        from { opacity: 0; transform: translateX(-30px); }
        to { opacity: 1; transform: translateX(0); }
    }
    @keyframes slideInRight {
        from { opacity: 0; transform: translateX(30px); }
        to { opacity: 1; transform: translateX(0); }
    }
    @keyframes bounceIn {
        0% { transform: scale(0.3); opacity: 0; }
        50% { transform: scale(1.05); }
        70% { transform: scale(0.9); }
        100% { transform: scale(1); opacity: 1; }
    }
    @keyframes rotateIn {
        from { transform: rotate(-180deg) scale(0); opacity: 0; }
        to { transform: rotate(0deg) scale(1); opacity: 1; }
    }
    
    /* ===== HERO SECTION ===== */
    .hero-section {
        background: linear-gradient(135deg, var(--dark) 0%, var(--dark2) 50%, var(--dark3) 100%);
        padding: 3rem 4rem;
        border-radius: 25px;
        margin-bottom: 2rem;
        position: relative;
        overflow: hidden;
        border: 1px solid rgba(102, 126, 234, 0.2);
        min-height: 300px;
        display: flex;
        align-items: center;
        animation: fadeInDown 0.8s ease-out;
    }
    
    .hero-section::before {
        content: '';
        position: absolute;
        top: -50%;
        right: -20%;
        width: 60%;
        height: 200%;
        background: radial-gradient(circle, rgba(102, 126, 234, 0.08) 0%, transparent 70%);
        animation: float 10s ease-in-out infinite;
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
        font-family: 'Inter', sans-serif;
    }
    
    .hero-subtitle {
        font-size: 1.3rem;
        color: rgba(255,255,255,0.8);
        margin-top: 0.5rem;
        font-weight: 300;
        font-family: 'Inter', sans-serif;
    }
    
    .hero-description {
        color: rgba(255,255,255,0.6);
        margin-top: 1rem;
        font-size: 1rem;
        max-width: 600px;
        line-height: 1.6;
        font-family: 'Inter', sans-serif;
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
        font-family: 'Inter', sans-serif;
    }
    
    /* ===== METRIC CARDS ===== */
    .metric-card {
        background: var(--white);
        padding: 1.5rem;
        border-radius: 16px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.06);
        border-left: 5px solid var(--primary);
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        animation: fadeInUp 0.6s ease-out;
        position: relative;
        overflow: hidden;
    }
    
    .metric-card:hover {
        transform: translateY(-6px) scale(1.01);
        box-shadow: 0 12px 40px rgba(0,0,0,0.1);
    }
    
    .metric-card::before {
        content: '';
        position: absolute;
        top: -50%;
        right: -50%;
        width: 100%;
        height: 100%;
        background: radial-gradient(circle, rgba(102,126,234,0.04) 0%, transparent 70%);
        border-radius: 50%;
        transition: all 0.5s ease;
    }
    
    .metric-card:hover::before {
        transform: scale(1.5);
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
        color: var(--text-dark);
        font-family: 'Inter', sans-serif;
    }
    
    .metric-card .label {
        font-size: 0.9rem;
        color: var(--text-medium);
        font-weight: 500;
        font-family: 'Inter', sans-serif;
    }
    
    /* ===== STATUS BADGES ===== */
    .status-badge {
        padding: 4px 16px;
        border-radius: 50px;
        font-size: 0.8rem;
        font-weight: 600;
        display: inline-block;
        font-family: 'Inter', sans-serif;
    }
    .status-high { background: var(--danger); color: white; animation: pulse 1.5s infinite; }
    .status-medium { background: var(--warning); color: var(--text-dark); }
    .status-low { background: #48dbfb; color: var(--text-dark); }
    
    /* ===== ENTITY CARDS ===== */
    .entity-card {
        background: var(--light);
        padding: 1rem 1.2rem;
        border-radius: 12px;
        margin: 0.5rem 0;
        border-left: 4px solid var(--primary);
        transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        animation: slideInLeft 0.5s ease-out;
    }
    .entity-card:hover {
        background: #e8ecf1;
        transform: translateX(8px) scale(1.01);
        box-shadow: 0 4px 15px rgba(0,0,0,0.08);
    }
    .entity-card strong { color: var(--text-dark); }
    .entity-card span { color: var(--text-medium); }
    
    /* ===== ALERT CARDS ===== */
    .alert-card-critical {
        background: linear-gradient(135deg, #ff4757, #ff6b6b);
        color: white;
        padding: 1.2rem;
        border-radius: 12px;
        margin: 0.5rem 0;
        animation: pulse 2s infinite;
        border: 2px solid rgba(255,255,255,0.2);
        transition: all 0.3s ease;
    }
    .alert-card-critical:hover { transform: scale(1.02); box-shadow: 0 8px 30px rgba(255, 71, 87, 0.4); }
    .alert-card-warning {
        background: linear-gradient(135deg, #ffa502, #feca57);
        color: white;
        padding: 1.2rem;
        border-radius: 12px;
        margin: 0.5rem 0;
        border: 2px solid rgba(255,255,255,0.2);
        transition: all 0.3s ease;
    }
    .alert-card-warning:hover { transform: scale(1.02); box-shadow: 0 8px 30px rgba(255, 165, 2, 0.4); }
    .alert-card-info {
        background: linear-gradient(135deg, #2ed573, #48dbfb);
        color: white;
        padding: 1.2rem;
        border-radius: 12px;
        margin: 0.5rem 0;
        border: 2px solid rgba(255,255,255,0.2);
        transition: all 0.3s ease;
    }
    .alert-card-info:hover { transform: scale(1.02); box-shadow: 0 8px 30px rgba(46, 213, 115, 0.4); }
    
    /* ===== SECTION DIVIDER ===== */
    .section-divider {
        height: 2px;
        background: linear-gradient(90deg, transparent, var(--primary), var(--secondary), var(--accent), transparent);
        margin: 2rem 0;
        border-radius: 10px;
    }
    
    /* ===== GLOW CARD ===== */
    .glow-card {
        background: var(--white);
        padding: 1.5rem;
        border-radius: 16px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.06);
        border: 1px solid rgba(102,126,234,0.1);
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        animation: glow 4s infinite;
        height: 100%;
        text-align: center;
    }
    .glow-card:hover {
        transform: translateY(-5px) scale(1.01);
        box-shadow: 0 12px 40px rgba(102,126,234,0.15);
        border-color: var(--primary);
    }
    .glow-card .icon { font-size: 3rem; margin-bottom: 0.5rem; }
    .glow-card h3 { color: var(--text-dark); font-size: 1.2rem; margin: 0.5rem 0; font-family: 'Inter', sans-serif; }
    .glow-card p { color: var(--text-medium); font-size: 0.9rem; font-family: 'Inter', sans-serif; }
    
    /* ===== QUICK STATS - FIXED ===== */
    .quick-stats {
        background: var(--white);
        padding: 1.5rem;
        border-radius: 16px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.06);
    }
    .quick-stats .stat-item {
        display: flex;
        justify-content: space-between;
        padding: 0.6rem 0;
        border-bottom: 1px solid #eee;
        color: var(--text-dark);
        font-family: 'Inter', sans-serif;
    }
    .quick-stats .stat-item:last-child { border-bottom: none; }
    .quick-stats .stat-label { color: var(--text-medium); font-weight: 400; }
    .quick-stats .stat-value { font-weight: 700; color: var(--text-dark); }
    
    /* ===== RAG RESPONSE ===== */
    .rag-response {
        background: var(--light);
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 4px solid var(--primary);
        margin: 0.5rem 0;
    }
    .rag-response p { color: var(--text-dark); font-family: 'Inter', sans-serif; }
    .rag-response strong { color: var(--text-dark); }
    
    /* ===== FOOTER ===== */
    .footer {
        text-align: center;
        padding: 1.5rem 0;
        color: var(--text-light);
        font-size: 0.85rem;
        border-top: 1px solid #eee;
        margin-top: 2rem;
        font-family: 'Inter', sans-serif;
    }
    
    /* ===== BUTTONS ===== */
    .stButton > button {
        background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
        color: white;
        font-weight: 600;
        border: none;
        border-radius: 50px;
        transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        font-family: 'Inter', sans-serif;
        padding: 0.6rem 2rem;
    }
    .stButton > button:hover {
        transform: translateY(-2px) scale(1.02);
        box-shadow: 0 8px 30px rgba(102, 126, 234, 0.4);
    }
    
    /* ===== RESPONSIVE ===== */
    @media (max-width: 768px) {
        .hero-title { font-size: 2.2rem; }
        .hero-section { padding: 2rem; }
        .metric-card .value { font-size: 1.5rem; }
    }
    
    /* ===== SIDEBAR ===== */
    .css-1d391kg { background: var(--dark); }
    .css-1d391kg .stButton > button { background: linear-gradient(135deg, var(--primary), var(--secondary)); }
    
    /* ===== SCROLLBAR ===== */
    ::-webkit-scrollbar { width: 6px; }
    ::-webkit-scrollbar-track { background: var(--light); border-radius: 10px; }
    ::-webkit-scrollbar-thumb { background: var(--primary); border-radius: 10px; }
    ::-webkit-scrollbar-thumb:hover { background: var(--secondary); }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# RENDER SIDEBAR
# ============================================================================

render_sidebar()

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
# MAIN ROUTER
# ============================================================================

def main():
    page = st.session_state.current_page
    
    if page == "Dashboard":
        dashboard.render()
    elif page == "Network Graph":
        network_graph.render()
    elif page == "Entity Profile":
        entity_profile.render()
    elif page == "Timeline":
        timeline.render()
    elif page == "Cross-Case Discovery":
        cross_case.render()
    elif page == "AI Copilot":
        ai_copilot.render()
    elif page == "Alerts & Emergency":
        alerts.render()
    elif page == "What-If Simulation":
        simulation.render()
    elif page == "Heatmap":
        heatmap.render()
    elif page == "Export":
        export.render()
    elif page == "Security":
        security.render()
    else:
        dashboard.render()

if __name__ == "__main__":
    main()
