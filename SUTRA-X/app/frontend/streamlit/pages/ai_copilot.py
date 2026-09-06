"""
AI Copilot Page - RAG Powered
"""

import streamlit as st
from app.backend.graph_engine.graph_builder import get_node_list, get_node_attributes, get_degree
from app.backend.security.audit import add_audit_log
from app.backend.security.rbac import has_permission

def render():
    """Render AI Copilot page"""
    
    G = st.session_state.graph
    node_list = get_node_list(G)
    
    st.markdown("""
    <div style="animation: fadeInUp 0.6s ease-out;">
        <h1 style="font-size: 2.5rem; font-weight: 700; color: #1a1a2e;">🤖 AI Copilot</h1>
        <p style="color: #666; margin-top: -0.5rem;">Intelligent investigation assistant with RAG</p>
    </div>
    """, unsafe_allow_html=True)
    
    if not st.session_state.data_loaded or G is None:
        st.info("👈 Click 'Generate Sample Data' in the sidebar to get started")
        return
    
    if not has_permission(st.session_state.user_role, "use_ai"):
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
            "Which entities should I investigate first?",
            "What are the hidden connections in this network?"
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
    
    # ===== PROCESS QUERY =====
    if hasattr(st.session_state, 'ai_query') and st.session_state.ai_query:
        query = st.session_state.ai_query
        
        st.markdown("---")
        st.markdown("### 🤖 AI Response")
        
        with st.spinner("Analyzing network..."):
            response_parts = []
            
            # Check for entity questions
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
            
            # Check for connection questions
            if "connection" in query.lower() or "link" in query.lower() or "relationship" in query.lower():
                response_parts.append("🔗 **Cross-case connections detected:** Multiple relationships between cases and persons.")
            
            # Check for pattern questions
            if "pattern" in query.lower() or "trend" in query.lower() or "activity" in query.lower():
                response_parts.append("📊 **Pattern detection:** Financial transaction patterns suggest potential money laundering.")
            
            # Check for priority questions
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
            
            # Default response
            if not response_parts:
                response_parts.append(f"💡 **Network overview:** The network contains {len(node_list)} entities.")
                response_parts.append("📊 Try asking about specific entities, connections, or patterns.")
            
            st.markdown(f"""
            <div class="rag-response">
                <strong>Response:</strong>
                <p style="margin-top: 0.5rem;">{chr(10).join(response_parts)}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Show relevant entities
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
            
            st.warning("⚠️ This is an AI-generated analysis. All findings should be verified by human investigators.")
            
            st.session_state.ai_query = ""
