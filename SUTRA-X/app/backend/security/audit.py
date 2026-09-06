"""
Audit Logging
"""

import streamlit as st
from datetime import datetime

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
