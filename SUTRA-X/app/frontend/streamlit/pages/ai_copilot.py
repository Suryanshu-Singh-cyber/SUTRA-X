
"""
AI Copilot Page - Real RAG with API Integration
"""

import streamlit as st
from app.backend.rag.rag_engine import RAGEngine
from app.backend.security.audit import audit_logger
from app.backend.security.rbac import rbac_manager
import os
from dotenv import load_dotenv

load_dotenv()

def render():
    """Render AI Copilot page"""
    
    st.markdown("""
    <div style="animation: fadeInUp 0.6s ease-out;">
        <h1 style="font-size: 2.5rem; font-weight: 700; color: #1a1a2e;">
            🤖 AI Copilot
        </h1>
        <p style="color: #666; margin-top: -0.5rem;">RAG-powered investigation assistant with real OpenAI API</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Check permissions
    if not rbac_manager.has_permission(st.session_state.get('user_role', 'viewer'), 'view_data'):
        st.warning("🔒 You don't have permission to access this feature.")
        return
    
    # Initialize RAG Engine
    rag = RAGEngine(st.session_state.get('graph'))
    
    # API Key Status
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key:
        st.success("✅ OpenAI API connected. RAG is fully functional.")
        st.caption(f"Model: {os.getenv('OPENAI_MODEL', 'gpt-4-turbo-preview')}")
    else:
        st.warning("⚠️ OpenAI API key not found. RAG is in fallback mode.")
        st.info("💡 Set OPENAI_API_KEY in .env file for full functionality.")
    
    st.markdown("---")
    
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
                audit_logger.log(
                    "ai_query",
                    st.session_state.get('user_role', 'unknown'),
                    "AI Copilot",
                    f"Query: {user_query[:100]}"
                )
                st.rerun()
            else:
                st.warning("Please enter a question.")
    
    # Process query
    if hasattr(st.session_state, 'ai_query') and st.session_state.ai_query:
        query = st.session_state.ai_query
        
        st.markdown("---")
        st.markdown("### 🤖 AI Response")
        
        with st.spinner("🧠 Analyzing with RAG..."):
            # Get response from RAG
            result = rag.query(query)
            
            # Display response
            st.markdown(f"""
            <div style="background: #f8f9fa; padding: 1.5rem; border-radius: 12px; 
                        border-left: 4px solid #667eea; animation: slideInLeft 0.5s ease-out;">
                <strong>Response:</strong>
                <p style="margin-top: 0.5rem; white-space: pre-wrap;">{result['response']}</p>
                <div style="display: flex; gap: 8px; flex-wrap: wrap; margin-top: 0.5rem;">
                    <span style="font-size: 0.7rem; color: #888; margin-right: 0.5rem;">Sources:</span>
                    {''.join([f'<span style="background: #667eea20; color: #667eea; padding: 2px 12px; border-radius: 50px; font-size: 0.7rem; font-weight: 600;">{s}</span>' for s in result['sources']])}
                    <span style="background: #667eea20; color: #667eea; padding: 2px 12px; border-radius: 50px; font-size: 0.7rem; font-weight: 600;">
                        Confidence: {result['confidence']:.0%}
                    </span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Show context
            with st.expander("📚 RAG Context", expanded=False):
                context = rag.get_context()
                st.text(context if context else "No context available. Generate data first.")
            
            # Show relevant entities
            if st.session_state.get('graph'):
                G = st.session_state.graph
                st.markdown("### 📋 Relevant Entities")
                entities_with_degree = []
                for node in list(G.nodes):
                    attrs = dict(G.nodes[node])
                    if attrs.get('type') == 'PERSON':
                        degree = len(list(G.neighbors(node)))
                        entities_with_degree.append((node, degree, attrs.get('name', node)))
                
                entities_with_degree.sort(key=lambda x: x[1], reverse=True)
                for node, degree, name in entities_with_degree[:5]:
                    st.markdown(f"- **{node}** ({name}) - Degree: {degree}")
            
            st.warning("⚠️ This is an AI-generated analysis. All findings should be verified by human investigators.")
            
            # Clear query
            st.session_state.ai_query = ""

def get_api_status():
    """Get API status"""
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key:
        return "✅ Connected", "success"
    return "⚠️ Not Connected", "warning"
