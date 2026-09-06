
"""
Alerts & Emergency Page
"""

import streamlit as st
from app.backend.intelligence_engine.analyzer import generate_alerts
from app.backend.security.audit import add_audit_log

def render():
    """Render Alerts & Emergency page"""
    
    st.markdown("""
    <div style="animation: fadeInUp 0.6s ease-out;">
        <h1 style="font-size: 2.5rem; font-weight: 700; color: #1a1a2e;">🔔 Alerts & Emergency</h1>
        <p style="color: #666; margin-top: -0.5rem;">Real-time critical alerts and emergency notifications</p>
    </div>
    """, unsafe_allow_html=True)
    
    if not st.session_state.data_loaded:
        st.info("👈 Click 'Generate Sample Data' in the sidebar to get started")
        return
    
    # ===== EMERGENCY BUTTONS =====
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
    
    # ===== REFRESH ALERTS =====
    col1, col2 = st.columns([3, 1])
    with col2:
        if st.button("🔄 Refresh Alerts", use_container_width=True):
            st.session_state.alerts = generate_alerts(st.session_state.graph)
            add_audit_log("refresh", "Alerts", "Alerts refreshed")
            st.rerun()
    
    st.markdown("---")
    
    # ===== DISPLAY ALERTS =====
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
        st.info("No active alerts. Generate sample data to see alerts.")
