"""
Sidebar Component - FIXED with 7 Languages
"""

import streamlit as st
from app.backend.data.sample_data import generate_sample_network
from app.backend.graph_engine.graph_builder import get_node_list
from app.backend.intelligence_engine.analyzer import generate_alerts
from app.backend.security.audit import add_audit_log
from app.backend.security.rbac import authenticate_user

# ============================================================================
# 7 LANGUAGES SUPPORT - FIXED
# ============================================================================

LANGUAGES = {
    "en": {"name": "English", "flag": "🇬🇧"},
    "hi": {"name": "हिंदी", "flag": "🇮🇳"},
    "ta": {"name": "தமிழ்", "flag": "🇮🇳"},
    "te": {"name": "తెలుగు", "flag": "🇮🇳"},
    "bn": {"name": "বাংলা", "flag": "🇮🇳"},
    "ml": {"name": "മലയാളം", "flag": "🇮🇳"},
    "ur": {"name": "اردو", "flag": "🇮🇳"},
}

def render_sidebar():
    """Render sidebar with navigation and controls"""
    
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
        
        # ===== LANGUAGE SELECTOR - 7 LANGUAGES =====
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
        
        # ===== AUTHENTICATION =====
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
        
        # ===== OFFLINE MODE =====
        st.markdown("### 📶 Mode")
        offline_toggle = st.toggle("Offline Mode", value=st.session_state.offline_mode)
        if offline_toggle != st.session_state.offline_mode:
            st.session_state.offline_mode = offline_toggle
            add_audit_log("mode_change", "Offline Mode", f"Set to {offline_toggle}")
            st.rerun()
        
        st.markdown("---")
        
        # ===== NAVIGATION =====
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
        
        # ===== DATA CONTROLS =====
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
        
        # ===== STATUS =====
        st.markdown("### 📶 Status")
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
