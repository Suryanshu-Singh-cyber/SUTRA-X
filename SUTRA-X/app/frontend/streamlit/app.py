"""
SUTRA-X: Smart Unified Threat & Relationship Analytics
AI-Powered Criminal Network Analysis System
SIH 2026
"""

import streamlit as st
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))

# Import pages
from app.frontend.streamlit.pages import (
    dashboard, network_graph, entity_profile, timeline, cross_case,
    ai_copilot, alerts, simulation, heatmap, export, security
)
from app.frontend.streamlit.components.sidebar import render_sidebar
from app.backend.data.sample_data import generate_sample_network
from app.backend.graph_engine.graph_builder import get_node_list
from app.backend.intelligence_engine.analyzer import analyze_network, generate_alerts

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

# ============================================================================
# CUSTOM CSS - FIXED UI
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
        0% { transform: translateY(0px) rotate(0deg); }
        50% { transform: translateY(-15px) rotate(2deg); }
        100% { transform: translateY(0px) rotate(0deg); }
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
    
    /* ===== HERO SECTION WITH BACKGROUND ===== */
    .hero-section {
        background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
        padding: 3rem 4rem;
        border-radius: 25px;
        margin-bottom: 2rem;
        position: relative;
        overflow: hidden;
        border: 1px solid rgba(102, 126, 234, 0.2);
        min-height: 300px;
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
    
    /* ===== METRIC CARDS - FIXED TEXT COLOR ===== */
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
    
    /* ===== FOOTER ===== */
    .footer {
        text-align: center;
        padding: 1.5rem 0;
        color: #888;
        font-size: 0.85rem;
        border-top: 1px solid #eee;
        margin-top: 2rem;
    }
    
    /* ===== RAG RESPONSE ===== */
    .rag-response {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 4px solid #667eea;
        margin: 0.5rem 0;
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
# RENDER SIDEBAR
# ============================================================================

render_sidebar()

# ============================================================================
# HERO SECTION - FIXED UI
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
