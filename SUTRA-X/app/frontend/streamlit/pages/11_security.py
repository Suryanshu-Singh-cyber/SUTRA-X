
"""
Security Page - Real RBAC and Audit
"""

import streamlit as st
import pandas as pd
from app.backend.security.rbac import rbac_manager, Role, Permission
from app.backend.security.audit import audit_logger
from datetime import datetime, timedelta

def render():
    """Render Security page"""
    
    st.markdown("""
    <div style="animation: fadeInUp 0.6s ease-out;">
        <h1 style="font-size: 2.5rem; font-weight: 700; color: #1a1a2e;">
            🔐 Security & Access Control
        </h1>
        <p style="color: #666; margin-top: -0.5rem;">Real Role-Based Access Control and Audit Logs</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Check permissions for security features
    current_role = st.session_state.get('user_role', 'viewer')
    
    # ===== Login/Logout =====
    st.markdown("### 🔑 Authentication")
    
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
        st.session_state.current_user = None
    
    if not st.session_state.authenticated:
        col1, col2 = st.columns([1, 1])
        with col1:
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            if st.button("Login", use_container_width=True):
                user_data = rbac_manager.authenticate(username, password)
                if user_data:
                    st.session_state.authenticated = True
                    st.session_state.current_user = username
                    st.session_state.user_role = user_data['role']
                    audit_logger.log(
                        "login",
                        username,
                        "Authentication",
                        f"Login successful with role: {user_data['role']}",
                        status="success"
                    )
                    st.success(f"✅ Welcome {username}! (Role: {user_data['role']})")
                    st.rerun()
                else:
                    st.error("❌ Invalid username or password")
        
        with col2:
            st.markdown("""
            <div style="background: #f8f9fa; padding: 1rem; border-radius: 12px;">
                <p><strong>Demo Credentials:</strong></p>
                <p>👑 Admin: admin / admin123</p>
                <p>🕵️ Investigator: investigator / invest123</p>
                <p>📊 Analyst: analyst / analyst123</p>
                <p>👀 Viewer: viewer / viewer123</p>
            </div>
            """, unsafe_allow_html=True)
        return
    else:
        col1, col2, col3 = st.columns([2, 1, 1])
        with col1:
            st.success(f"✅ Logged in as: **{st.session_state.current_user}** (Role: {st.session_state.user_role})")
        with col3:
            if st.button("🚪 Logout", use_container_width=True):
                audit_logger.log(
                    "logout",
                    st.session_state.current_user,
                    "Authentication",
                    "User logged out"
                )
                st.session_state.authenticated = False
                st.session_state.current_user = None
                st.session_state.user_role = 'viewer'
                st.rerun()
    
    st.markdown("---")
    
    # ===== RBAC Status =====
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🔐 Role-Based Access Control")
        
        # Current Role Info
        role_info = {
            'admin': {'icon': '👑', 'desc': 'Full access to all features'},
            'investigator': {'icon': '🕵️', 'desc': 'Access to investigation features'},
            'analyst': {'icon': '📊', 'desc': 'Read and export data'},
            'viewer': {'icon': '👀', 'desc': 'Read-only access'}
        }
        
        info = role_info.get(current_role, {'icon': '👀', 'desc': 'View only'})
        st.markdown(f"""
        <div style="background: white; padding: 1rem; border-radius: 12px; 
                    box-shadow: 0 2px 10px rgba(0,0,0,0.05);">
            <div style="font-size: 2rem;">{info['icon']}</div>
            <div><strong>Current Role:</strong> {current_role.upper()}</div>
            <div style="color: #666; font-size: 0.9rem;">{info['desc']}</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Available Roles
        st.markdown("#### Available Roles")
        for role in Role:
            permissions = [p.value for p in ROLE_PERMISSIONS.get(role, [])]
            st.markdown(f"- **{role.value.upper()}**: {', '.join(permissions[:3])}{'...' if len(permissions) > 3 else ''}")
    
    with col2:
        st.markdown("### 📶 Offline Mode")
        
        offline_toggle = st.toggle(
            "Enable Offline Mode",
            value=st.session_state.get('offline_mode', False),
            help="Work without internet, sync when online"
        )
        if offline_toggle != st.session_state.get('offline_mode', False):
            st.session_state.offline_mode = offline_toggle
            audit_logger.log(
                "mode_change",
                st.session_state.current_user,
                "Offline Mode",
                f"Set to {offline_toggle}"
            )
            st.rerun()
        
        st.markdown("""
        <div style="background: #f8f9fa; padding: 1rem; border-radius: 12px; margin-top: 1rem;">
            <div style="display: flex; justify-content: space-between;">
                <span>Current Status:</span>
                <span style="font-weight: 600; color: #2ed573;">📶 Online</span>
            </div>
            <div style="display: flex; justify-content: space-between;">
                <span>Data Sync:</span>
                <span style="font-weight: 600;">✅ Real-time</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # ===== Audit Logs =====
    st.markdown("### 📋 Audit Logs")
    
    if not rbac_manager.has_permission(current_role, 'view_audit'):
        st.warning("🔒 You don't have permission to view audit logs.")
    else:
        col1, col2, col3 = st.columns([2, 1, 1])
        
        with col1:
            limit = st.number_input("Logs to show", min_value=10, max_value=500, value=50, step=10)
        
        with col2:
            users = audit_logger.get_users()
            selected_user = st.selectbox("Filter by User", ["All"] + users)
        
        with col3:
            actions = audit_logger.get_actions()
            selected_action = st.selectbox("Filter by Action", ["All"] + actions)
        
        # Get logs
        user_filter = None if selected_user == "All" else selected_user
        action_filter = None if selected_action == "All" else selected_action
        
        logs = audit_logger.get_logs(limit=limit, user=user_filter, action=action_filter)
        
        if logs:
            # Display stats
            stats = audit_logger.get_stats()
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total Logs", stats['total_logs'])
            with col2:
                st.metric("Last 24h", stats['last_24h'])
            with col3:
                st.metric("Unique Users", len(stats['user_count']))
            with col4:
                st.metric("Unique Actions", len(stats['action_count']))
            
            # Display logs table
            st.markdown("---")
            
            logs_df = pd.DataFrame(logs[::-1])  # Reverse for newest first
            if not logs_df.empty:
                # Format for display
                display_cols = ['timestamp', 'user', 'action', 'resource', 'status']
                if all(c in logs_df.columns for c in display_cols):
                    display_df = logs_df[display_cols].copy()
                    display_df['timestamp'] = pd.to_datetime(display_df['timestamp']).dt.strftime('%Y-%m-%d %H:%M:%S')
                    st.dataframe(display_df, use_container_width=True)
                    
                    # Export logs
                    csv = display_df.to_csv(index=False)
                    st.download_button(
                        label="📥 Download Logs (CSV)",
                        data=csv,
                        file_name=f"audit_logs_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                        mime="text/csv"
                    )
        else:
            st.info("No audit logs found.")

def check_permission(permission):
    """Check if current user has permission"""
    return rbac_manager.has_permission(
        st.session_state.get('user_role', 'viewer'),
        permission
    )
