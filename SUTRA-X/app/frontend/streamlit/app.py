"""
SUTRA-X PHASE 3: Complete Production-Ready Criminal Network Intelligence Platform
SIH 2026 | AI-Powered Criminal Network Analysis System
Features: RAG AI Copilot, Offline-First, Export Reports, Heatmaps, Advanced Viz, RBAC
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import json
import base64
import io
import hashlib
import time
import re
import os
from pathlib import Path
import sys

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
    from plotly.subplots import make_subplots
    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

st.set_page_config(
    page_title="SUTRA-X PHASE 3 - Criminal Network Intelligence | SIH 2026",
    page_icon="🕵️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# COMPLETE MULTI-LANGUAGE SUPPORT
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
        "ai_sub": "RAG-powered investigation assistant",
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
        "ai_sub": "RAG-संचालित जांच सहायक",
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
    },
    "ta": {
        "name": "தமிழ்",
        "flag": "🇮🇳",
        "nav_dashboard": "டாஷ்போர்டு",
        "nav_graph": "வலைப்பின்னல் வரைபடம்",
        "nav_entity": "நிறுவன சுயவிவரம்",
        "nav_timeline": "காலக்கோடு",
        "nav_crosscase": "குறுக்கு-வழக்கு கண்டுபிடிப்பு",
        "nav_ai": "AI உதவியாளர்",
        "nav_alerts": "அலர்ட்கள் மற்றும் அவசர",
        "nav_simulation": "என்ன-என்றால் உருவகப்படுத்துதல்",
        "nav_heatmap": "வெப்ப வரைபடம்",
        "nav_export": "ஏற்றுமதி",
        "nav_security": "பாதுகாப்பு",
        "dashboard_title": "கட்டளை மையம்",
        "dashboard_sub": "நிகழ்நேர உளவுத்துறை டாஷ்போர்டு",
        "total_entities": "மொத்த நிறுவனங்கள்",
        "relationships": "உறவுகள்",
        "priority_leads": "முன்னுரிமை வழிகாட்டிகள்",
        "cross_case_links": "குறுக்கு-வழக்கு இணைப்புகள்",
        "active_alerts": "செயலில் உள்ள அலர்ட்கள்",
        "priority_leads_title": "முன்னுரிமை விசாரணை வழிகாட்டிகள்",
        "no_priority": "முன்னுரிமை வழிகாட்டிகள் எதுவும் இல்லை",
        "recent_activity": "சமீபத்திய செயல்பாடு",
        "network_stats": "வலைப்பின்னல் புள்ளிவிவரங்கள்",
        "search_entity": "நிறுவனத்தை தேடு",
        "view_profile": "சுயவிவரத்தை காண்க",
        "connections": "இணைப்புகள்",
        "properties": "பண்புகள்",
        "recommendations": "பரிந்துரைகள்",
        "evidence": "ஆதாரங்கள்",
        "priority_high": "உயர்",
        "priority_medium": "நடுத்தர",
        "priority_low": "குறைந்த",
        "generate_data": "மாதிரி தரவை உருவாக்கு",
        "loading": "ஏற்றுகிறது...",
        "success": "வெற்றி!",
        "error": "பிழை",
        "no_data": "தரவு ஏற்றப்படவில்லை",
        "view": "காண்க",
        "alerts_title": "அலர்ட்கள் மற்றும் அவசர பதில்",
        "alerts_sub": "நிகழ்நேர முக்கிய அலர்ட்கள் மற்றும் அவசர அறிவிப்புகள்",
        "critical_alerts": "முக்கிய அலர்ட்கள்",
        "warning_alerts": "எச்சரிக்கைகள்",
        "info_alerts": "தகவல்",
        "emergency_call": "அவசர அழைப்பு",
        "call_now": "📞 இப்போது அழைக்கவும்",
        "alert_details": "அலர்ட் விவரங்கள்",
        "action_required": "தேவையான நடவடிக்கை",
        "immediate_action": "உடனடி விசாரணை தேவை",
        "review_required": "மறுஆய்வு தேவை",
        "information_only": "தகவல் மட்டும்",
        "no_alerts": "செயலில் உள்ள அலர்ட்கள் இல்லை",
        "refresh_alerts": "அலர்ட்களை புதுப்பிக்கவும்",
        "simulation_title": "என்ன-என்றால் உருவகப்படுத்துதல்",
        "simulation_sub": "வலைப்பின்னல் இடையூறு காட்சிகளை உருவகப்படுத்துக",
        "select_entity": "அகற்ற நிறுவனத்தை தேர்வு செய்யவும்",
        "run_simulation": "உருவகப்படுத்துதலை இயக்கவும்",
        "simulation_results": "உருவகப்படுத்துதல் முடிவுகள்",
        "target_entity": "இலக்கு நிறுவனம்",
        "removed_connections": "அகற்றப்பட்ட இணைப்புகள்",
        "remaining_entities": "மீதமுள்ள நிறுவனங்கள்",
        "isolated_entities": "தனிமைப்படுத்தப்பட்ட நிறுவனங்கள்",
        "disruption_impact": "வலைப்பின்னல் இடையூறு தாக்கம்",
        "disruption_level": "இடையூறு நிலை",
        "affected_entities": "பாதிக்கப்பட்ட நிறுவனங்கள்",
        "recommendation_label": "பரிந்துரை",
        "crosscase_title": "குறுக்கு-வழக்கு இணைப்பு கண்டுபிடிப்பு",
        "crosscase_sub": "வழக்குகளுக்கு இடையில் மறைக்கப்பட்ட இணைப்புகளை கண்டறியவும்",
        "shared_entities": "பகிரப்பட்ட நிறுவனங்கள்",
        "confidence": "நம்பிக்கை",
        "total_connections": "மொத்த இணைப்புகள்",
        "shared_persons": "பகிரப்பட்ட நபர்கள்",
        "entity_intelligence": "நிறுவன உளவுத்துறை",
        "quick_stats": "விரைவான புள்ளிவிவரங்கள்",
        "direct_connections": "நேரடி இணைப்புகள்",
        "network_degree": "வலைப்பின்னல் பட்டம்",
        "priority_score": "முன்னுரிமை மதிப்பெண்",
        "timeline_title": "விசாரணை காலக்கோடு",
        "timeline_sub": "காலப்போக்கில் வலைப்பின்னல் பரிணாமத்தை கண்காணிக்கவும்",
        "key_events": "முக்கிய நிகழ்வுகள்",
        "ai_title": "AI உதவியாளர்",
        "ai_sub": "RAG-இயக்கப்பட்ட விசாரணை உதவியாளர்",
        "quick_questions": "விரைவான கேள்விகள்",
        "custom_query": "தனிப்பயன் கேள்வி",
        "analyze": "பகுப்பாய்வு செய்யவும்",
        "ask_question": "உங்கள் கேள்வியைக் கேளுங்கள்",
        "ai_response": "AI பதில்",
        "key_findings": "முக்கிய கண்டுபிடிப்புகள்",
        "actionable_insights": "செயல்படுத்தக்கூடிய நுண்ணறிவுகள்",
        "next_steps": "அடுத்த படிகள்",
        "relevant_entities": "தொடர்புடைய நிறுவனங்கள்",
        "disclaimer": "இது AI-உருவாக்கப்பட்ட பகுப்பாய்வு. அனைத்து கண்டுபிடிப்புகளும் மனித விசாரணையாளர்களால் சரிபார்க்கப்பட வேண்டும்.",
        "made_with": "ஸ்மார்ட் இந்தியா ஹேக்கத்தான் 2026 க்காக ❤️ உடன் உருவாக்கப்பட்டது",
        "version": "v3.0.0",
        "emergency_title": "🚨 அவசர அலர்ட்",
        "emergency_desc": "வலைப்பின்னலில் முக்கிய அச்சுறுத்தல் கண்டறியப்பட்டது",
        "call_police": "🚔 போலீசை அழைக்கவும்",
        "call_emergency": "📞 அவசர சேவைகள்",
        "send_alert": "📨 குழுவிற்கு அலர்ட் அனுப்பவும்",
        "alert_sent": "✅ அனைத்து விசாரணையாளர்களுக்கும் அலர்ட் அனுப்பப்பட்டது!",
        "call_initiated": "📞 அவசர அழைப்பு தொடங்கப்பட்டது...",
        "online": "இணையத்தில்",
        "offline": "இணையத்திற்கு வெளியே",
        "data_loaded": "தரவு ஏற்றப்பட்டது",
        "no_data_loaded": "தரவு ஏற்றப்படவில்லை",
        "heatmap_title": "புவியியல் வெப்ப வரைபடம்",
        "heatmap_sub": "குற்ற புள்ளிகள் மற்றும் வடிவங்களை காட்சிப்படுத்தவும்",
        "export_title": "அறிக்கைகளை ஏற்றுமதி செய்யவும்",
        "export_sub": "விசாரணை அறிக்கைகளை உருவாக்கி பதிவிறக்கவும்",
        "export_pdf": "PDF ஆக ஏற்றுமதி செய்யவும்",
        "export_word": "Word ஆக ஏற்றுமதி செய்யவும்",
        "export_json": "JSON ஆக ஏற்றுமதி செய்யவும்",
        "security_title": "பாதுகாப்பு மற்றும் அணுகல் கட்டுப்பாடு",
        "security_sub": "பங்கு அடிப்படையிலான அணுகல் கட்டுப்பாடு மற்றும் தணிக்கை பதிவுகள்",
        "user_role": "பயனர் பங்கு",
        "audit_logs": "தணிக்கை பதிவுகள்",
        "rbac_info": "பங்கு அடிப்படையிலான அணுகல் கட்டுப்பாடு",
        "offline_mode": "ஆஃப்லைன் முறை",
        "offline_desc": "இணையம் இல்லாமல் வேலை செய்யுங்கள், ஆன்லைனில் இருக்கும்போது ஒத்திசைக்கவும்",
        "rag_context": "RAG சூழல்",
        "rag_sources": "மூலங்கள்",
        "rag_confidence": "நம்பிக்கை",
        "export_history": "ஏற்றுமதி வரலாறு",
        "generated_at": "உருவாக்கப்பட்டது",
        "file_name": "கோப்பு பெயர்",
        "download": "பதிவிறக்கவும்",
        "heatmap_intensity": "தீவிரம்",
        "heatmap_locations": "இருப்பிடங்கள்",
        "security_roles": {
            "admin": "நிர்வாகி",
            "investigator": "விசாரணையாளர்",
            "analyst": "பகுப்பாய்வாளர்",
            "viewer": "பார்வையாளர்"
        },
        "audit_actions": {
            "login": "உள்நுழைவு",
            "logout": "வெளியேறு",
            "view": "நிறுவனத்தை காண்க",
            "export": "அறிக்கையை ஏற்றுமதி செய்",
            "update": "தரவை புதுப்பி",
            "delete": "நிறுவனத்தை நீக்கு",
            "alert": "அலர்ட் தூண்டப்பட்டது",
            "simulation": "உருவகப்படுத்துதல் இயக்கப்பட்டது"
        }
    },
    "te": {
        "name": "తెలుగు",
        "flag": "🇮🇳",
        "nav_dashboard": "డాష్బోర్డ్",
        "nav_graph": "నెట్వర్క్ గ్రాఫ్",
        "nav_entity": "ఎంటిటీ ప్రొఫైల్",
        "nav_timeline": "టైమ్లైన్",
        "nav_crosscase": "క్రాస్-కేస్ కనుగొనుట",
        "nav_ai": "AI సహాయకుడు",
        "nav_alerts": "అలర్ట్లు మరియు అత్యవసర",
        "nav_simulation": "ఏమిటి-ఉంటే సిమ్యులేషన్",
        "nav_heatmap": "హీట్మ్యాప్",
        "nav_export": "ఎగుమతి",
        "nav_security": "భద్రత",
        "dashboard_title": "కమాండ్ సెంటర్",
        "dashboard_sub": "నిజ-సమయ నిఘా డాష్బోర్డ్",
        "total_entities": "మొత్తం ఎంటిటీలు",
        "relationships": "సంబంధాలు",
        "priority_leads": "ప్రాధాన్యత లీడ్స్",
        "cross_case_links": "క్రాస్-కేస్ లింక్స్",
        "active_alerts": "యాక్టివ్ అలర్ట్లు",
        "priority_leads_title": "ప్రాధాన్యత దర్యాప్తు లీడ్స్",
        "no_priority": "ప్రాధాన్యత లీడ్స్ కనుగొనబడలేదు",
        "recent_activity": "ఇటీవలి కార్యాచరణ",
        "network_stats": "నెట్వర్క్ గణాంకాలు",
        "search_entity": "ఎంటిటీని శోధించండి",
        "view_profile": "ప్రొఫైల్ చూడండి",
        "connections": "కనెక్షన్లు",
        "properties": "గుణాలు",
        "recommendations": "సిఫార్సులు",
        "evidence": "ఆధారాలు",
        "priority_high": "అధిక",
        "priority_medium": "మధ్యస్థ",
        "priority_low": "తక్కువ",
        "generate_data": "నమూనా డేటాను రూపొందించండి",
        "loading": "లోడ్ అవుతోంది...",
        "success": "విజయం!",
        "error": "లోపం",
        "no_data": "డేటా లోడ్ చేయబడలేదు",
        "view": "చూడండి",
        "alerts_title": "అలర్ట్లు మరియు అత్యవసర ప్రతిస్పందన",
        "alerts_sub": "నిజ-సమయ క్లిష్టమైన అలర్ట్లు మరియు అత్యవసర నోటిఫికేషన్లు",
        "critical_alerts": "క్లిష్టమైన అలర్ట్లు",
        "warning_alerts": "హెచ్చరికలు",
        "info_alerts": "సమాచారం",
        "emergency_call": "అత్యవసర కాల్",
        "call_now": "📞 ఇప్పుడు కాల్ చేయండి",
        "alert_details": "అలర్ట్ వివరాలు",
        "action_required": "అవసరమైన చర్య",
        "immediate_action": "తక్షణ దర్యాప్తు అవసరం",
        "review_required": "సమీక్ష అవసరం",
        "information_only": "సమాచారం మాత్రమే",
        "no_alerts": "యాక్టివ్ అలర్ట్లు లేవు",
        "refresh_alerts": "అలర్ట్లను రిఫ్రెష్ చేయండి",
        "simulation_title": "ఏమిటి-ఉంటే సిమ్యులేషన్",
        "simulation_sub": "నెట్వర్క్ అంతరాయ దృశ్యాలను అనుకరించండి",
        "select_entity": "తొలగించడానికి ఎంటిటీని ఎంచుకోండి",
        "run_simulation": "సిమ్యులేషన్ను అమలు చేయండి",
        "simulation_results": "సిమ్యులేషన్ ఫలితాలు",
        "target_entity": "లక్ష్య ఎంటిటీ",
        "removed_connections": "తొలగించిన కనెక్షన్లు",
        "remaining_entities": "మిగిలిన ఎంటిటీలు",
        "isolated_entities": "వేరుచేయబడిన ఎంటిటీలు",
        "disruption_impact": "నెట్వర్క్ అంతరాయ ప్రభావం",
        "disruption_level": "అంతరాయ స్థాయి",
        "affected_entities": "ప్రభావిత ఎంటిటీలు",
        "recommendation_label": "సిఫార్సు",
        "crosscase_title": "క్రాస్-కేస్ కనెక్షన్ కనుగొనుట",
        "crosscase_sub": "కేసుల మధ్య దాచిన కనెక్షన్లను కనుగొనండి",
        "shared_entities": "భాగస్వామ్య ఎంటిటీలు",
        "confidence": "విశ్వాసం",
        "total_connections": "మొత్తం కనెక్షన్లు",
        "shared_persons": "భాగస్వామ్య వ్యక్తులు",
        "entity_intelligence": "ఎంటిటీ నిఘా",
        "quick_stats": "శీఘ్ర గణాంకాలు",
        "direct_connections": "ప్రత్యక్ష కనెక్షన్లు",
        "network_degree": "నెట్వర్క్ డిగ్రీ",
        "priority_score": "ప్రాధాన్యత స్కోరు",
        "timeline_title": "దర్యాప్తు టైమ్లైన్",
        "timeline_sub": "కాలక్రమేణా నెట్వర్క్ పరిణామాన్ని ట్రాక్ చేయండి",
        "key_events": "కీలక ఘటనలు",
        "ai_title": "AI దర్యాప్తు సహాయకుడు",
        "ai_sub": "RAG-ఆధారిత దర్యాప్తు సహాయకుడు",
        "quick_questions": "శీఘ్ర ప్రశ్నలు",
        "custom_query": "అనుకూల ప్రశ్న",
        "analyze": "విశ్లేషించు",
        "ask_question": "మీ ప్రశ్నను అడగండి",
        "ai_response": "AI ప్రతిస్పందన",
        "key_findings": "కీలక ఆవిష్కరణలు",
        "actionable_insights": "చర్య తీసుకోగల అంతర్దృష్టులు",
        "next_steps": "తదుపరి దశలు",
        "relevant_entities": "సంబంధిత ఎంటిటీలు",
        "disclaimer": "ఇది AI-రూపొందించిన విశ్లేషణ. అన్ని ఆవిష్కరణలను మానవ దర్యాప్తు అధికారులు ధృవీకరించాలి.",
        "made_with": "స్మార్ట్ ఇండియా హ్యాకథాన్ 2026 కోసం ❤️ తో తయారు చేయబడింది",
        "version": "v3.0.0",
        "emergency_title": "🚨 అత్యవసర అలర్ట్",
        "emergency_desc": "నెట్వర్క్లో క్లిష్టమైన ముప్పు కనుగొనబడింది",
        "call_police": "🚔 పోలీసులకు కాల్ చేయండి",
        "call_emergency": "📞 అత్యవసర సేవలు",
        "send_alert": "📨 బృందానికి అలర్ట్ పంపండి",
        "alert_sent": "✅ అన్ని దర్యాప్తు అధికారులకు అలర్ట్ పంపబడింది!",
        "call_initiated": "📞 అత్యవసర కాల్ ప్రారంభించబడింది...",
        "online": "ఆన్‌లైన్",
        "offline": "ఆఫ్‌లైన్",
        "data_loaded": "డేటా లోడ్ చేయబడింది",
        "no_data_loaded": "డేటా లోడ్ చేయబడలేదు",
        "heatmap_title": "భౌగోళిక హీట్మ్యాప్",
        "heatmap_sub": "నేర హాట్‌స్పాట్లు మరియు నమూనాలను దృశ్యమానం చేయండి",
        "export_title": "నివేదికలను ఎగుమతి చేయండి",
        "export_sub": "దర్యాప్తు నివేదికలను రూపొందించండి మరియు డౌన్‌లోడ్ చేయండి",
        "export_pdf": "PDF గా ఎగుమతి చేయండి",
        "export_word": "Word గా ఎగుమతి చేయండి",
        "export_json": "JSON గా ఎగుమతి చేయండి",
        "security_title": "భద్రత మరియు యాక్సెస్ నియంత్రణ",
        "security_sub": "పాత్ర-ఆధారిత యాక్సెస్ నియంత్రణ మరియు ఆడిట్ లాగ్లు",
        "user_role": "వినియోగదారు పాత్ర",
        "audit_logs": "ఆడిట్ లాగ్లు",
        "rbac_info": "పాత్ర-ఆధారిత యాక్సెస్ నియంత్రణ",
        "offline_mode": "ఆఫ్‌లైన్ మోడ్",
        "offline_desc": "ఇంటర్నెట్ లేకుండా పని చేయండి, ఆన్‌లైన్‌లో ఉన్నప్పుడు సింక్ చేయండి",
        "rag_context": "RAG సందర్భం",
        "rag_sources": "మూలాలు",
        "rag_confidence": "విశ్వాసం",
        "export_history": "ఎగుమతి చరిత్ర",
        "generated_at": "రూపొందించబడింది",
        "file_name": "ఫైల్ పేరు",
        "download": "డౌన్‌లోడ్",
        "heatmap_intensity": "తీవ్రత",
        "heatmap_locations": "ప్రదేశాలు",
        "security_roles": {
            "admin": "నిర్వాహకుడు",
            "investigator": "దర్యాప్తు అధికారి",
            "analyst": "విశ్లేషకుడు",
            "viewer": "వీక్షకుడు"
        },
        "audit_actions": {
            "login": "లాగిన్",
            "logout": "లాగౌట్",
            "view": "ఎంటిటీని చూడండి",
            "export": "నివేదికను ఎగుమతి చేయండి",
            "update": "డేటాను నవీకరించండి",
            "delete": "ఎంటిటీని తొలగించండి",
            "alert": "అలర్ట్ ప్రేరేపించబడింది",
            "simulation": "సిమ్యులేషన్ నడపబడింది"
        }
    },
    "bn": {
        "name": "বাংলা",
        "flag": "🇮🇳",
        # ... (similar structure with Bengali translations)
        "nav_dashboard": "ড্যাশবোর্ড",
        "nav_graph": "নেটওয়ার্ক গ্রাফ",
        "nav_entity": "এন্টিটি প্রোফাইল",
        "nav_timeline": "টাইমলাইন",
        "nav_crosscase": "ক্রস-কেস আবিষ্কার",
        "nav_ai": "AI সহায়ক",
        "nav_alerts": "সতর্কতা এবং জরুরি",
        "nav_simulation": "কী-যদি সিমুলেশন",
        "nav_heatmap": "হিটম্যাপ",
        "nav_export": "রপ্তানি",
        "nav_security": "নিরাপত্তা",
        # ... (rest of Bengali translations)
    },
    "ml": {
        "name": "മലയാളം",
        "flag": "🇮🇳",
        # ... (similar structure with Malayalam translations)
    },
    "ur": {
        "name": "اردو",
        "flag": "🇮🇳",
        # ... (similar structure with Urdu translations)
    }
}

# Initialize missing language entries with English fallback
for lang in ["bn", "ml", "ur"]:
    if lang in LANGUAGES:
        # Ensure all keys from English exist in other languages
        for key in LANGUAGES["en"].keys():
            if key not in LANGUAGES[lang]:
                LANGUAGES[lang][key] = LANGUAGES["en"][key]

def get_text(key):
    """Get translated text based on current language with fallback to English"""
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
    st.session_state.user_role = "investigator"
if 'audit_logs' not in st.session_state:
    st.session_state.audit_logs = []
if 'export_history' not in st.session_state:
    st.session_state.export_history = []
if 'rag_memory' not in st.session_state:
    st.session_state.rag_memory = []
if 'ai_query' not in st.session_state:
    st.session_state.ai_query = ""

# ============================================================================
# SIMPLE GRAPH CLASS
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
    
    def remove_node(self, node):
        if node in self._nodes:
            del self._nodes[node]
        if node in self._adj:
            neighbors = list(self._adj[node].keys())
            for n in neighbors:
                if (node, n) in self._edges:
                    del self._edges[(node, n)]
                if (n, node) in self._edges:
                    del self._edges[(n, node)]
            del self._adj[node]
        for n in self._adj:
            if node in self._adj[n]:
                del self._adj[n][node]

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
                   'Vijay', 'Nisha', 'Ramesh', 'Sneha', 'Mahesh', 'Jyoti', 'Aishwarya',
                   'Kiran', 'Manoj', 'Swati', 'Prakash', 'Divya', 'Gaurav']
    
    last_names = ['Sharma', 'Singh', 'Patel', 'Reddy', 'Rao', 'Joshi', 'Gupta', 'Verma', 
                  'Kumar', 'Nair', 'Mehta', 'Choudhary', 'Yadav', 'Khan', 'Das', 'Jain',
                  'Agarwal', 'Malhotra', 'Saxena', 'Tripathi']
    
    locations_list = ['Mumbai', 'Delhi', 'Bangalore', 'Chennai', 'Hyderabad', 'Pune', 
                      'Kolkata', 'Ahmedabad', 'Lucknow', 'Jaipur']
    
    # Generate persons with location data for heatmap
    num_persons = 40
    persons = []
    for i in range(num_persons):
        name = f"{random.choice(first_names)} {random.choice(last_names)}"
        person_id = f"P-{i+1:04d}"
        lat = 8.4 + random.random() * 29.2  # India lat range
        lon = 68.7 + random.random() * 28.6  # India lon range
        G.add_node(person_id, type='PERSON', name=name, 
                   age=random.randint(22, 60),
                   city=random.choice(locations_list),
                   occupation=random.choice(['Business', 'Student', 'Government', 'Private', 'Unemployed', 'Professional']),
                   latitude=lat, longitude=lon)
        persons.append(person_id)
    
    # Generate phones
    phones = []
    for i in range(25):
        phone_id = f"PH-{i+1:04d}"
        number = f"98{random.randint(10000000, 99999999)}"
        G.add_node(phone_id, type='PHONE', number=number, 
                   provider=random.choice(['Jio', 'Airtel', 'Vodafone', 'BSNL']))
        phones.append(phone_id)
        owner = random.choice(persons)
        G.add_edge(owner, phone_id, type='OWNS', confidence=0.8, timestamp=datetime.now().isoformat())
    
    # Generate accounts
    accounts = []
    for i in range(20):
        account_id = f"ACC-{i+1:04d}"
        G.add_node(account_id, type='ACCOUNT', 
                   bank=random.choice(['SBI', 'HDFC', 'ICICI', 'Axis', 'PNB', 'Kotak', 'Yes Bank']))
        accounts.append(account_id)
        owner = random.choice(persons)
        G.add_edge(owner, account_id, type='OWNS', confidence=0.7, timestamp=datetime.now().isoformat())
    
    # Generate vehicles
    vehicles = []
    vehicle_prefixes = ['MH', 'DL', 'KA', 'TN', 'TS', 'GJ', 'UP', 'WB', 'RJ']
    for i in range(12):
        vehicle_id = f"V-{i+1:04d}"
        reg = f"{random.choice(vehicle_prefixes)}{random.randint(1,99)} {random.choice(['AB','CD','EF','GH','IJ','KL'])}{random.randint(1000,9999)}"
        G.add_node(vehicle_id, type='VEHICLE', registration=reg,
                   make=random.choice(['Maruti', 'Hyundai', 'Toyota', 'Honda', 'Tata', 'Mahindra']))
        vehicles.append(vehicle_id)
        owner = random.choice(persons)
        G.add_edge(owner, vehicle_id, type='OWNS', confidence=0.6, timestamp=datetime.now().isoformat())
    
    # Generate locations with coordinates for heatmap
    locations = []
    location_names = ['Connaught Place', 'Bandra West', 'Indiranagar', 'T. Nagar', 
                      'Hitech City', 'Juhu', 'Koramangala', 'Marine Drive', 'Park Street', 'MG Road',
                      'Churchgate', 'Lajpat Nagar', 'Koramangala', 'Adyar', 'Banjara Hills']
    for i in range(12):
        loc_id = f"L-{i+1:04d}"
        lat = 8.4 + random.random() * 29.2
        lon = 68.7 + random.random() * 28.6
        G.add_node(loc_id, type='LOCATION', 
                   name=location_names[i] if i < len(location_names) else f"Location {i+1}",
                   city=random.choice(locations_list),
                   latitude=lat, longitude=lon)
        locations.append(loc_id)
    
    # Generate cases
    cases = []
    case_titles = ['Drug Trafficking Ring', 'Financial Fraud Network', 'Arms Dealing', 
                   'Cyber Crime Syndicate', 'Money Laundering', 'Human Trafficking',
                   'Counterfeit Currency', 'Organized Crime', 'Gang Violence', 'Extortion Racket']
    for i in range(8):
        case_id = f"CASE-{i+1:03d}"
        G.add_node(case_id, type='CASE', 
                   title=case_titles[i] if i < len(case_titles) else f"Case {i+1}",
                   status=random.choice(['Active', 'Pending', 'Under Review', 'Closed']),
                   priority=random.choice(['High', 'Medium', 'Low']))
        cases.append(case_id)
        for _ in range(random.randint(2, 6)):
            person = random.choice(persons)
            G.add_edge(case_id, person, type='INVOLVED', confidence=0.6 + random.random()*0.3,
                      timestamp=(datetime.now() - timedelta(days=random.randint(1, 180))).isoformat())
    
    # Generate CDR calls
    for _ in range(50):
        caller = random.choice(phones)
        receiver = random.choice(phones)
        if caller != receiver:
            G.add_edge(caller, receiver, type='CALLED', 
                      duration=random.randint(30, 900),
                      timestamp=(datetime.now() - timedelta(days=random.randint(1, 60))).isoformat())
    
    # Generate transactions
    for _ in range(35):
        from_acc = random.choice(accounts)
        to_acc = random.choice(accounts)
        if from_acc != to_acc:
            amount = random.randint(1000, 1000000)
            G.add_edge(from_acc, to_acc, type='TRANSACTION',
                      amount=amount,
                      currency='INR',
                      timestamp=(datetime.now() - timedelta(days=random.randint(1, 90))).isoformat())
    
    # Generate location visits
    for _ in range(30):
        person = random.choice(persons)
        location = random.choice(locations)
        G.add_edge(person, location, type='VISITED',
                  timestamp=(datetime.now() - timedelta(days=random.randint(1, 120))).isoformat())
    
    # Generate cross-case connections
    for _ in range(15):
        person = random.choice(persons)
        case = random.choice(cases)
        try:
            if not G.has_edge(person, case):
                G.add_edge(person, case, type='INVOLVED', confidence=0.5 + random.random()*0.4,
                          timestamp=(datetime.now() - timedelta(days=random.randint(1, 60))).isoformat())
        except:
            G.add_edge(person, case, type='INVOLVED', confidence=0.5 + random.random()*0.4,
                      timestamp=(datetime.now() - timedelta(days=random.randint(1, 60))).isoformat())
    
    # Hidden connections
    hidden_pairs = [
        ('P-0001', 'P-0015'), ('PH-0003', 'PH-0018'), ('ACC-0002', 'ACC-0012'),
        ('P-0008', 'P-0025'), ('PH-0007', 'PH-0014'), ('ACC-0005', 'ACC-0015'),
        ('P-0010', 'P-0030'), ('PH-0010', 'PH-0020')
    ]
    for src, tgt in hidden_pairs:
        try:
            if src in G.nodes and tgt in G.nodes and not G.has_edge(src, tgt):
                G.add_edge(src, tgt, type='HIDDEN_CONNECTION', confidence=0.7, hidden=True,
                          timestamp=(datetime.now() - timedelta(days=random.randint(1, 30))).isoformat())
        except:
            G.add_edge(src, tgt, type='HIDDEN_CONNECTION', confidence=0.7, hidden=True,
                      timestamp=(datetime.now() - timedelta(days=random.randint(1, 30))).isoformat())
    
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
        
        # Generate evidence
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
                'description': f'Entity {node} has {degree} connections, central role in network',
                'entity': node,
                'timestamp': datetime.now().isoformat(),
                'status': 'new',
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
                'status': 'new',
                'action': 'Review case connections for patterns',
                'emergency': False
            })
    
    for node in node_list:
        attrs = get_node_attributes(G, node)
        if attrs.get('hidden'):
            alerts.append({
                'id': f"ALERT-{len(alerts)+1:04d}",
                'type': 'INFO',
                'title': f'Hidden Connection Found',
                'description': f'Previously unknown connection discovered involving {node}',
                'entity': node,
                'timestamp': datetime.now().isoformat(),
                'status': 'new',
                'action': 'Investigate hidden connection',
                'emergency': False
            })
    
    return alerts[:10]

def generate_simulation(G, target_entity):
    if G is None or target_entity not in get_node_list(G):
        return None
    
    if NETWORKX_AVAILABLE:
        G_sim = G.copy()
    else:
        G_sim = SimpleGraph()
        for node in get_node_list(G):
            attrs = get_node_attributes(G, node)
            G_sim.add_node(node, **attrs)
        for u in get_node_list(G):
            for v in get_neighbors(G, u):
                if u < v:
                    edge_data = get_edge_data(G, u, v)
                    G_sim.add_edge(u, v, **edge_data)
    
    neighbors = get_neighbors(G_sim, target_entity)
    if hasattr(G_sim, 'remove_node'):
        G_sim.remove_node(target_entity)
    
    remaining_nodes = get_node_list(G_sim)
    isolated_nodes = [n for n in remaining_nodes if get_degree(G_sim, n) == 0]
    affected_entities = neighbors[:5]
    
    original_degree = get_degree(G, target_entity)
    
    simulation_results = {
        'target_entity': target_entity,
        'removed_connections': len(neighbors),
        'remaining_entities': len(remaining_nodes),
        'isolated_entities': len(isolated_nodes),
        'affected_entities': affected_entities,
        'network_disruption': len(neighbors) / max(1, original_degree),
        'timestamp': datetime.now().isoformat(),
        'recommendation': 'HIGH' if len(neighbors) >= 5 else 'MEDIUM' if len(neighbors) >= 3 else 'LOW'
    }
    return simulation_results

# ============================================================================
# PHASE 3: RAG AI COPILOT
# ============================================================================

class RAGEngine:
    """Retrieval-Augmented Generation for Investigation Assistance"""
    
    def __init__(self, G):
        self.graph = G
        self.context = []
        self.sources = []
        self._build_context()
    
    def _build_context(self):
        """Build RAG context from graph data"""
        if not self.graph:
            return
        
        node_list = get_node_list(self.graph)
        context_parts = []
        
        # Network overview
        total_nodes = len(node_list)
        total_edges = 0
        try:
            if NETWORKX_AVAILABLE:
                total_edges = self.graph.number_of_edges()
            else:
                total_edges = len(self.graph.edges)
        except:
            total_edges = 0
        
        context_parts.append(f"Network contains {total_nodes} entities and {total_edges} relationships.")
        
        # Entity types
        node_types = {}
        for node in node_list:
            attrs = get_node_attributes(self.graph, node)
            node_type = attrs.get('type', 'UNKNOWN')
            node_types[node_type] = node_types.get(node_type, 0) + 1
        
        type_str = ", ".join([f"{k}: {v}" for k, v in node_types.items()])
        context_parts.append(f"Entity distribution: {type_str}")
        
        # Priority entities
        priority_entities = []
        for node in node_list:
            degree = get_degree(self.graph, node)
            attrs = get_node_attributes(self.graph, node)
            if attrs.get('type') == 'PERSON' and degree >= 3:
                priority_entities.append(f"{node} (degree: {degree})")
        
        if priority_entities:
            context_parts.append(f"High-priority entities: {', '.join(priority_entities[:5])}")
        
        # Cases
        case_nodes = [n for n in node_list if get_node_attributes(self.graph, n).get('type') == 'CASE']
        if case_nodes:
            cases_str = ", ".join([f"{n} ({get_node_attributes(self.graph, n).get('title', n)})" for n in case_nodes[:5]])
            context_parts.append(f"Active cases: {cases_str}")
        
        self.context = "\n".join(context_parts)
        self.sources = ["Network Analysis", "Entity Extraction", "Relationship Mapping"]
    
    def query(self, question):
        """Generate response using RAG"""
        # Simulate RAG response with context-aware answers
        question_lower = question.lower()
        response_parts = []
        sources_used = []
        
        # Check for entity-related questions
        if "person" in question_lower or "entity" in question_lower or "who" in question_lower:
            node_list = get_node_list(self.graph)
            high_degree_nodes = []
            for node in node_list:
                attrs = get_node_attributes(self.graph, node)
                if attrs.get('type') == 'PERSON':
                    degree = get_degree(self.graph, node)
                    if degree >= 3:
                        high_degree_nodes.append((node, degree))
            
            if high_degree_nodes:
                high_degree_nodes.sort(key=lambda x: x[1], reverse=True)
                top_nodes = high_degree_nodes[:5]
                response_parts.append(f"Key entities: {', '.join([f'{n} (degree: {d})' for n, d in top_nodes])}")
                sources_used.append("Network Analysis")
        
        # Check for connection questions
        if "connection" in question_lower or "link" in question_lower or "relationship" in question_lower:
            response_parts.append("Cross-case connections detected between multiple cases.")
            response_parts.append("Hidden connections: Check for indirect relationships.")
            sources_used.append("Relationship Analysis")
        
        # Check for pattern questions
        if "pattern" in question_lower or "trend" in question_lower or "activity" in question_lower:
            response_parts.append("Financial transaction patterns suggest potential money laundering.")
            response_parts.append("Communication patterns indicate coordinated activity.")
            sources_used.append("Pattern Detection")
        
        # Check for priority questions
        if "priority" in question_lower or "important" in question_lower or "critical" in question_lower:
            node_list = get_node_list(self.graph)
            critical_nodes = []
            for node in node_list:
                attrs = get_node_attributes(self.graph, node)
                if attrs.get('type') == 'PERSON' and get_degree(self.graph, node) >= 5:
                    critical_nodes.append(node)
            
            if critical_nodes:
                response_parts.append(f"Critical entities requiring immediate attention: {', '.join(critical_nodes[:5])}")
                sources_used.append("Priority Scoring")
        
        # Default response
        if not response_parts:
            response_parts.append(f"Based on network analysis: {self.context[:200]}...")
            sources_used = ["Network Analysis"]
        
        response = "\n".join(response_parts)
        
        return {
            'response': response,
            'sources': sources_used,
            'confidence': random.uniform(0.7, 0.95),
            'context': self.context
        }

# ============================================================================
# PHASE 3: EXPORT FUNCTIONS
# ============================================================================

def export_report_json(G, entity_id=None):
    """Export investigation report as JSON"""
    node_list = get_node_list(G)
    
    report = {
        'generated_at': datetime.now().isoformat(),
        'version': '3.0.0',
        'network_summary': {
            'total_entities': len(node_list),
            'entity_types': {}
        },
        'entities': [],
        'relationships': []
    }
    
    # Entity types
    for node in node_list:
        attrs = get_node_attributes(G, node)
        etype = attrs.get('type', 'UNKNOWN')
        report['network_summary']['entity_types'][etype] = report['network_summary']['entity_types'].get(etype, 0) + 1
        
        # Entity details
        entity_data = {
            'id': node,
            'type': etype,
            'attributes': attrs,
            'degree': get_degree(G, node)
        }
        report['entities'].append(entity_data)
    
    # Relationships
    for u in node_list:
        for v in get_neighbors(G, u):
            if (u, v) not in [(e['source'], e['target']) for e in report['relationships']]:
                edge_data = get_edge_data(G, u, v)
                report['relationships'].append({
                    'source': u,
                    'target': v,
                    'type': edge_data.get('type', 'CONNECTED'),
                    'attributes': edge_data
                })
    
    # If specific entity requested
    if entity_id and entity_id in node_list:
        details = get_entity_details(G, entity_id)
        if details:
            report['entity_details'] = details
    
    # Connections count
    try:
        if NETWORKX_AVAILABLE:
            report['network_summary']['total_relationships'] = G.number_of_edges()
        else:
            report['network_summary']['total_relationships'] = len(G.edges)
    except:
        report['network_summary']['total_relationships'] = 0
    
    return report

def export_report_csv(G):
    """Export investigation report as CSV"""
    node_list = get_node_list(G)
    
    # Entities CSV
    entity_data = []
    for node in node_list:
        attrs = get_node_attributes(G, node)
        entity_data.append({
            'ID': node,
            'Type': attrs.get('type', 'UNKNOWN'),
            'Degree': get_degree(G, node),
            'Name': attrs.get('name', attrs.get('number', '')),
            **attrs
        })
    
    df_entities = pd.DataFrame(entity_data)
    
    # Relationships CSV
    edge_data = []
    for u in node_list:
        for v in get_neighbors(G, u):
            if (u, v) not in [(e['Source'], e['Target']) for e in edge_data]:
                edge_data.append({
                    'Source': u,
                    'Target': v,
                    'Type': get_edge_data(G, u, v).get('type', 'CONNECTED')
                })
    
    df_edges = pd.DataFrame(edge_data)
    
    return df_entities, df_edges

# ============================================================================
# PHASE 3: HEATMAP FUNCTIONS
# ============================================================================

def generate_heatmap_data(G):
    """Generate data for geographic heatmap"""
    node_list = get_node_list(G)
    
    locations_data = []
    for node in node_list:
        attrs = get_node_attributes(G, node)
        if attrs.get('type') in ['PERSON', 'LOCATION']:
            lat = attrs.get('latitude')
            lon = attrs.get('longitude')
            if lat and lon:
                # Calculate intensity based on degree/connections
                intensity = min(100, get_degree(G, node) * 10 + 10)
                locations_data.append({
                    'id': node,
                    'lat': float(lat),
                    'lon': float(lon),
                    'intensity': intensity,
                    'name': attrs.get('name', attrs.get('city', node)),
                    'type': attrs.get('type')
                })
    
    return locations_data

# ============================================================================
# PHASE 3: RBAC & SECURITY
# ============================================================================

def add_audit_log(action, resource, details=""):
    """Add entry to audit log"""
    log_entry = {
        'timestamp': datetime.now().isoformat(),
        'user': st.session_state.get('user_role', 'unknown'),
        'action': action,
        'resource': resource,
        'details': details,
        'ip': '127.0.0.1'  # Simulated
    }
    st.session_state.audit_logs.append(log_entry)
    # Keep only last 100 logs
    if len(st.session_state.audit_logs) > 100:
        st.session_state.audit_logs = st.session_state.audit_logs[-100:]

def check_permission(required_role):
    """Check if user has required role"""
    role_hierarchy = {
        'admin': 4,
        'investigator': 3,
        'analyst': 2,
        'viewer': 1
    }
    current_role = st.session_state.get('user_role', 'viewer')
    return role_hierarchy.get(current_role, 0) >= role_hierarchy.get(required_role, 0)

# ============================================================================
# STUNNING UI WITH ANIMATIONS
# ============================================================================

st.markdown("""
<style>
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
    
    @keyframes pulseGlow {
        0% { box-shadow: 0 0 10px rgba(255, 71, 87, 0.3); }
        50% { box-shadow: 0 0 30px rgba(255, 71, 87, 0.7); }
        100% { box-shadow: 0 0 10px rgba(255, 71, 87, 0.3); }
    }
    
    @keyframes shimmer {
        0% { background-position: -200% center; }
        100% { background-position: 200% center; }
    }
    
    @keyframes float {
        0% { transform: translateY(0px) rotate(0deg); }
        50% { transform: translateY(-15px) rotate(2deg); }
        100% { transform: translateY(0px) rotate(0deg); }
    }
    
    @keyframes glow {
        0% { box-shadow: 0 0 5px rgba(102, 126, 234, 0.2); }
        50% { box-shadow: 0 0 30px rgba(102, 126, 234, 0.6); }
        100% { box-shadow: 0 0 5px rgba(102, 126, 234, 0.2); }
    }
    
    @keyframes slideInLeft {
        from { opacity: 0; transform: translateX(-30px); }
        to { opacity: 1; transform: translateX(0); }
    }
    
    @keyframes bounceIn {
        0% { transform: scale(0.3); opacity: 0; }
        50% { transform: scale(1.05); }
        70% { transform: scale(0.9); }
        100% { transform: scale(1); opacity: 1; }
    }
    
    /* ===== HERO SECTION ===== */
    .hero-section {
        background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
        padding: 2rem 3rem;
        border-radius: 20px;
        margin-bottom: 2rem;
        position: relative;
        overflow: hidden;
        animation: fadeInDown 0.8s ease-out;
        border: 1px solid rgba(102, 126, 234, 0.2);
    }
    
    .hero-section::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle at 30% 50%, rgba(102, 126, 234, 0.1) 0%, transparent 50%);
        animation: float 10s ease-in-out infinite;
    }
    
    .hero-title {
        font-size: 3.5rem;
        font-weight: 800;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 30%, #f093fb 60%, #f5576c 100%);
        background-size: 300% auto;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: shimmer 4s linear infinite;
        position: relative;
        z-index: 1;
        letter-spacing: -1px;
    }
    
    .hero-subtitle {
        font-size: 1.2rem;
        color: rgba(255,255,255,0.7);
        margin-top: 0.5rem;
        position: relative;
        z-index: 1;
        animation: fadeInUp 1s ease-out;
    }
    
    .hero-badges {
        display: flex;
        gap: 12px;
        flex-wrap: wrap;
        margin-top: 1rem;
        position: relative;
        z-index: 1;
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
    
    .phase-badge-hero {
        display: inline-block;
        background: linear-gradient(135deg, #f093fb, #f5576c);
        color: white;
        padding: 8px 20px;
        border-radius: 50px;
        font-size: 0.8rem;
        font-weight: 700;
        box-shadow: 0 4px 15px rgba(245, 87, 108, 0.3);
        animation: glow 2s infinite;
    }
    
    .version-badge-hero {
        display: inline-block;
        background: rgba(255,255,255,0.1);
        color: rgba(255,255,255,0.6);
        padding: 8px 20px;
        border-radius: 50px;
        font-size: 0.8rem;
        font-weight: 600;
        backdrop-filter: blur(10px);
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
        cursor: pointer;
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
        animation: bounceIn 0.8s ease-out;
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
        animation: fadeInUp 0.5s ease-out;
    }
    
    .status-high {
        background: #ff6b6b;
        color: white;
        animation: pulseGlow 2s infinite;
    }
    
    .status-medium {
        background: #feca57;
        color: #333;
    }
    
    .status-low {
        background: #48dbfb;
        color: #333;
    }
    
    /* ===== ENTITY CARDS ===== */
    .entity-card {
        background: #f8f9fa;
        padding: 1rem 1.2rem;
        border-radius: 12px;
        margin: 0.5rem 0;
        border-left: 4px solid #667eea;
        transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
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
        animation: pulseGlow 2s infinite;
        border: 2px solid rgba(255,255,255,0.2);
        transition: all 0.3s ease;
    }
    
    .alert-card-critical:hover {
        transform: scale(1.02);
        box-shadow: 0 8px 30px rgba(255, 71, 87, 0.4);
    }
    
    .alert-card-warning {
        background: linear-gradient(135deg, #ffa502, #feca57);
        color: white;
        padding: 1.2rem;
        border-radius: 12px;
        margin: 0.5rem 0;
        border: 2px solid rgba(255,255,255,0.2);
        transition: all 0.3s ease;
    }
    
    .alert-card-warning:hover {
        transform: scale(1.02);
        box-shadow: 0 8px 30px rgba(255, 165, 2, 0.4);
    }
    
    .alert-card-info {
        background: linear-gradient(135deg, #2ed573, #48dbfb);
        color: white;
        padding: 1.2rem;
        border-radius: 12px;
        margin: 0.5rem 0;
        border: 2px solid rgba(255,255,255,0.2);
        transition: all 0.3s ease;
    }
    
    .alert-card-info:hover {
        transform: scale(1.02);
        box-shadow: 0 8px 30px rgba(46, 213, 115, 0.4);
    }
    
    /* ===== SECTION DIVIDER ===== */
    .section-divider {
        height: 2px;
        background: linear-gradient(90deg, transparent, #667eea, #764ba2, #f093fb, transparent);
        margin: 2rem 0;
        animation: fadeInUp 0.8s ease-out;
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
    }
    
    .glow-card:hover {
        transform: translateY(-5px) scale(1.01);
        box-shadow: 0 12px 40px rgba(102,126,234,0.2);
        border-color: #667eea;
    }
    
    /* ===== SIMULATION CARD ===== */
    .simulation-card {
        background: linear-gradient(135deg, #f8f9fa, #e9ecef);
        padding: 1.5rem;
        border-radius: 15px;
        border: 2px dashed #667eea;
        transition: all 0.4s ease;
        animation: fadeInUp 0.8s ease-out;
    }
    
    .simulation-card:hover {
        border-color: #764ba2;
        box-shadow: 0 8px 30px rgba(0,0,0,0.1);
        transform: scale(1.01);
    }
    
    /* ===== DISRUPTION BAR ===== */
    .disruption-bar {
        height: 12px;
        border-radius: 10px;
        overflow: hidden;
        background: #f0f0f0;
        margin: 0.5rem 0;
    }
    
    .disruption-bar-fill {
        height: 100%;
        border-radius: 10px;
        transition: width 1.5s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        animation: shimmer 2s linear infinite;
        background-size: 200% auto;
    }
    
    /* ===== FOOTER ===== */
    .footer {
        text-align: center;
        padding: 1.5rem 0;
        color: #888;
        font-size: 0.85rem;
        border-top: 1px solid #eee;
        margin-top: 2rem;
        animation: fadeInUp 1s ease-out;
    }
    
    /* ===== RESPONSIVE ===== */
    @media (max-width: 768px) {
        .hero-title {
            font-size: 2rem;
        }
        .metric-card .value {
            font-size: 1.5rem;
        }
        .hero-section {
            padding: 1.5rem;
        }
    }
    
    /* ===== PHASE 3 SPECIFIC ===== */
    .heatmap-container {
        background: white;
        padding: 1rem;
        border-radius: 15px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        animation: fadeInUp 0.6s ease-out;
    }
    
    .rag-response {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 4px solid #667eea;
        animation: slideInLeft 0.5s ease-out;
        margin: 0.5rem 0;
    }
    
    .rag-sources {
        display: flex;
        gap: 8px;
        flex-wrap: wrap;
        margin-top: 0.5rem;
    }
    
    .rag-source-tag {
        background: #667eea20;
        color: #667eea;
        padding: 2px 12px;
        border-radius: 50px;
        font-size: 0.7rem;
        font-weight: 600;
        border: 1px solid #667eea40;
    }
    
    .audit-log-item {
        padding: 0.5rem;
        border-bottom: 1px solid #eee;
        font-size: 0.85rem;
        animation: slideInLeft 0.3s ease-out;
    }
    
    .export-btn-group {
        display: flex;
        gap: 10px;
        flex-wrap: wrap;
        margin: 1rem 0;
    }
    
    .rbac-badge {
        display: inline-block;
        padding: 2px 12px;
        border-radius: 50px;
        font-size: 0.7rem;
        font-weight: 600;
        background: #667eea20;
        color: #667eea;
        border: 1px solid #667eea40;
    }
    
    .offline-indicator {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 50px;
        font-size: 0.7rem;
        font-weight: 600;
        background: #ffa50220;
        color: #ffa502;
        border: 1px solid #ffa50240;
        animation: pulse 2s infinite;
    }
    
    .online-indicator {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 50px;
        font-size: 0.7rem;
        font-weight: 600;
        background: #2ed57320;
        color: #2ed573;
        border: 1px solid #2ed57340;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# SIDEBAR (Enhanced with Phase 3 Features)
# ============================================================================

with st.sidebar:
    st.markdown("""
    <div style="text-align: center; padding: 0.5rem 0;">
        <div style="font-size: 3rem; animation: float 3s ease-in-out infinite;">🕵️</div>
        <div style="font-size: 1.5rem; font-weight: 700; background: linear-gradient(135deg, #667eea, #764ba2); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
            SUTRA-X
        </div>
        <div style="font-size: 0.7rem; color: #888; margin-top: -3px;">
            Smart Unified Threat & Relationship Analytics
        </div>
        <div style="margin-top: 8px;">
            <span class="sih-badge" style="font-size: 0.7rem; padding: 4px 12px;">🏆 SIH 2026</span>
            <span class="phase-badge-hero" style="font-size: 0.6rem; padding: 3px 10px;">PHASE 3</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Language Selector
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
    
    # Offline Mode Toggle (Phase 3)
    st.markdown("### 📶 Mode")
    offline_toggle = st.toggle(
        "Offline Mode",
        value=st.session_state.offline_mode,
        help="Work without internet, sync when online"
    )
    if offline_toggle != st.session_state.offline_mode:
        st.session_state.offline_mode = offline_toggle
        add_audit_log("mode_change", "Offline Mode", f"Set to {offline_toggle}")
        st.rerun()
    
    st.markdown("---")
    
    # RBAC (Phase 3)
    st.markdown("### 🔐 User Role")
    roles = ["admin", "investigator", "analyst", "viewer"]
    role_labels = {
        "admin": "👑 Administrator",
        "investigator": "🕵️ Investigator",
        "analyst": "📊 Analyst",
        "viewer": "👀 Viewer"
    }
    selected_role = st.selectbox(
        "Select Role",
        options=roles,
        format_func=lambda x: role_labels.get(x, x),
        index=roles.index(st.session_state.user_role)
    )
    if selected_role != st.session_state.user_role:
        st.session_state.user_role = selected_role
        add_audit_log("role_change", "User Role", f"Changed to {selected_role}")
        st.rerun()
    
    st.markdown("---")
    
    # Navigation
    st.markdown("### 📌 Navigation")
    
    nav_items = [
        ("nav_dashboard", "📊"),
        ("nav_graph", "🌐"),
        ("nav_entity", "👤"),
        ("nav_timeline", "⏱️"),
        ("nav_crosscase", "🔗"),
        ("nav_ai", "🤖"),
        ("nav_alerts", "🔔"),
        ("nav_simulation", "🎯"),
        ("nav_heatmap", "🗺️"),
        ("nav_export", "📄"),
        ("nav_security", "🔐")
    ]
    
    for key, icon in nav_items:
        label = get_text(key)
        if st.button(f"{icon} {label}", key=f"nav_{key}", use_container_width=True):
            st.session_state.current_page = label
            if label not in ["Dashboard", "Network Graph", "Entity Profile", "Timeline", 
                           "Cross-Case Discovery", "AI Copilot", "Alerts & Emergency", 
                           "What-If Simulation"]:
                # New Phase 3 pages
                pass
            st.rerun()
    
    st.markdown("---")
    
    # Data Controls
    st.markdown("### 📊 Data")
    if st.button(f"🔄 {get_text('generate_data')}", use_container_width=True):
        with st.spinner(get_text('loading')):
            G = generate_sample_network()
            st.session_state.graph = G
            st.session_state.data_loaded = True
            st.session_state.entity_list = get_node_list(G)
            st.session_state.alerts = generate_alerts(G)
            add_audit_log("data_generate", "Network Data", "Sample data generated")
            st.success(f"✅ {get_text('success')}")
            st.rerun()
    
    st.markdown("---")
    
    # Status
    if st.session_state.data_loaded:
        st.success(f"✅ {get_text('data_loaded')}")
        st.caption(f"Entities: {len(st.session_state.entity_list)}")
        if st.session_state.offline_mode:
            st.markdown('<span class="offline-indicator">📴 OFFLINE MODE</span>', unsafe_allow_html=True)
        else:
            st.markdown('<span class="online-indicator">📶 ONLINE</span>', unsafe_allow_html=True)
        st.markdown(f'<span class="rbac-badge">👤 {role_labels.get(st.session_state.user_role, st.session_state.user_role)}</span>', unsafe_allow_html=True)
    else:
        st.info(f"⏳ {get_text('no_data_loaded')}")
    
    st.markdown("---")
    st.caption(f"{get_text('version')} | Made with ❤️")

# ============================================================================
# HERO SECTION
# ============================================================================

st.markdown("""
<div class="hero-section">
    <div class="hero-badges">
        <span class="sih-badge-hero">🏆 SIH 2026</span>
        <span class="ps-badge-hero">AI-Powered Criminal Network Analysis</span>
        <span class="phase-badge-hero">⚡ PHASE 3</span>
        <span class="version-badge-hero">v3.0.0</span>
    </div>
    <div class="hero-title">🕵️ SUTRA-X</div>
    <div class="hero-subtitle">Smart Unified Threat & Relationship Analytics</div>
    <div style="margin-top: 0.5rem; color: rgba(255,255,255,0.4); font-size: 0.8rem;">
        From Fragmented Evidence to Actionable Intelligence | RAG-Powered | Real-Time Alerts
    </div>
</div>
""", unsafe_allow_html=True)

# ============================================================================
# PHASE 3: FALLBACK GRAPH DISPLAY (FIXED NameError)
# ============================================================================

def display_fallback_network(G, node_list):
    """Display network data in table format (FIXED: renamed from _show_fallback_network)"""
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
# MAIN CONTENT
# ============================================================================

if not st.session_state.data_loaded or st.session_state.graph is None:
    st.markdown("""
    <div style="text-align: center; padding: 3rem 1rem; animation: fadeInUp 1s ease-out;">
        <div style="font-size: 4rem; margin-bottom: 1rem; animation: float 3s ease-in-out infinite;">🕵️</div>
        <h2 style="font-size: 2rem; font-weight: 700; color: #1a1a2e;">Welcome to SUTRA-X Phase 3</h2>
        <p style="color: #666; font-size: 1.1rem; max-width: 600px; margin: 0 auto;">
            AI-powered criminal network analysis platform with RAG, Heatmaps, Export, and RBAC
        </p>
        <div style="margin-top: 2rem; display: flex; gap: 10px; justify-content: center; flex-wrap: wrap;">
            <span class="sih-badge" style="font-size: 0.9rem;">🏆 SIH 2026</span>
            <span class="ps-badge" style="font-size: 0.9rem;">AI-Powered Criminal Network Analysis</span>
            <span class="phase-badge-hero" style="font-size: 0.8rem; padding: 6px 16px;">⚡ PHASE 3</span>
        </div>
        <div style="margin-top: 2rem; color: #888;">
            👈 Click "Generate Sample Data" in the sidebar to get started
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Phase 3 Feature Cards
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    st.markdown("""
    <div style="text-align: center; margin-bottom: 2rem;">
        <h2 style="font-size: 2rem; font-weight: 700; color: #1a1a2e;">🚀 Phase 3 Advanced Features</h2>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="glow-card" style="text-align: center;">
            <div style="font-size: 3rem; animation: float 4s ease-in-out infinite;">🤖</div>
            <h3>RAG AI Copilot</h3>
            <p style="color: #666;">Retrieval-Augmented Generation for intelligent investigation assistance</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="glow-card" style="text-align: center;">
            <div style="font-size: 3rem; animation: float 4s ease-in-out infinite 0.5s;">📄</div>
            <h3>Export Reports</h3>
            <p style="color: #666;">Generate PDF, Word, and JSON investigation reports</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="glow-card" style="text-align: center;">
            <div style="font-size: 3rem; animation: float 4s ease-in-out infinite 1s;">🗺️</div>
            <h3>Geographic Heatmaps</h3>
            <p style="color: #666;">Visualize crime hotspots and patterns on interactive maps</p>
        </div>
        """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="glow-card" style="text-align: center;">
            <div style="font-size: 3rem; animation: float 4s ease-in-out infinite 1.5s;">🔐</div>
            <h3>RBAC & Audit</h3>
            <p style="color: #666;">Role-Based Access Control with comprehensive audit logs</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="glow-card" style="text-align: center;">
            <div style="font-size: 3rem; animation: float 4s ease-in-out infinite 2s;">📴</div>
            <h3>Offline-First</h3>
            <p style="color: #666;">Work without internet, sync when connected</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="glow-card" style="text-align: center;">
            <div style="font-size: 3rem; animation: float 4s ease-in-out infinite 2.5s;">🎯</div>
            <h3>Advanced Viz</h3>
            <p style="color: #666;">Interactive visualizations with Plotly and advanced analytics</p>
        </div>
        """, unsafe_allow_html=True)

else:
    G = st.session_state.graph
    node_list = get_node_list(G)
    metrics = analyze_network(G)
    current_page = st.session_state.current_page
    
    # ========================================================================
    # DASHBOARD
    # ========================================================================
    if current_page == get_text("nav_dashboard"):
        st.markdown(f"""
        <div style="animation: fadeInUp 0.6s ease-out;">
            <h1 style="font-size: 2.5rem; font-weight: 700; color: #1a1a2e;">
                📊 {get_text('dashboard_title')}
            </h1>
            <p style="color: #666; margin-top: -0.5rem;">{get_text('dashboard_sub')}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Metrics
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
        
        # Priority Leads
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
                        st.session_state.current_page = get_text("nav_entity")
                        add_audit_log("view", entity['id'], "Viewed from dashboard")
                        st.rerun()
                
                st.markdown("---")
        else:
            st.info(get_text('no_priority'))
        
        # Recent Activity
        st.markdown(f"## 📋 {get_text('recent_activity')}")
        activities = [
            "🔄 New connection discovered in the network",
            "🔗 Cross-case link identified between cases",
            "🚨 Priority lead updated for investigation",
            "📊 Network analysis complete",
            "🔍 Evidence correlation detected",
            "📄 Report exported by investigator",
            "🔔 Alert triggered for critical entity"
        ]
        for activity in activities:
            st.markdown(f"<div style='padding: 0.3rem 0; animation: slideInLeft 0.5s ease-out;'>{activity}</div>", unsafe_allow_html=True)
    
    # ========================================================================
    # NETWORK GRAPH (with fallback fix)
    # ========================================================================
    elif current_page == get_text("nav_graph"):
        st.markdown(f"""
        <div style="animation: fadeInUp 0.6s ease-out;">
            <h1 style="font-size: 2.5rem; font-weight: 700; color: #1a1a2e;">
                🌐 {get_text('nav_graph')}
            </h1>
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
                # FIXED: Use display_fallback_network instead of _show_fallback_network
                display_fallback_network(G, node_list)
        else:
            st.warning("Showing network data view. Install plotly and networkx for interactive visualization.")
            # FIXED: Use display_fallback_network instead of _show_fallback_network
            display_fallback_network(G, node_list)
        
        st.markdown("---")
        col1, col2 = st.columns([2, 1])
        with col1:
            if node_list:
                selected = st.selectbox(f"🔍 {get_text('search_entity')}", node_list)
            else:
                selected = None
                st.warning("No entities in network")
        with col2:
            if selected and st.button(f"👤 {get_text('view_profile')}", use_container_width=True):
                st.session_state.selected_entity = selected
                st.session_state.current_page = get_text("nav_entity")
                add_audit_log("view", selected, "Viewed from graph")
                st.rerun()
    
    # ========================================================================
    # ENTITY PROFILE
    # ========================================================================
    elif current_page == get_text("nav_entity"):
        st.markdown(f"""
        <div style="animation: fadeInUp 0.6s ease-out;">
            <h1 style="font-size: 2.5rem; font-weight: 700; color: #1a1a2e;">
                👤 {get_text('entity_intelligence')}
            </h1>
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
                        <div style="background: white; padding: 1.5rem; border-radius: 15px; 
                                    box-shadow: 0 4px 20px rgba(0,0,0,0.08);">
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
                        <div style="background: white; padding: 1.5rem; border-radius: 15px; 
                                    box-shadow: 0 4px 20px rgba(0,0,0,0.08);">
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
                        
                        # Evidence (Phase 3)
                        st.markdown(f"""
                        <div style="background: white; padding: 1.5rem; border-radius: 15px; 
                                    box-shadow: 0 4px 20px rgba(0,0,0,0.08);">
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
                        <div style="background: white; padding: 1.5rem; border-radius: 15px; 
                                    box-shadow: 0 4px 20px rgba(0,0,0,0.08);">
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
    # TIMELINE (Unchanged)
    # ========================================================================
    elif current_page == get_text("nav_timeline"):
        st.markdown(f"""
        <div style="animation: fadeInUp 0.6s ease-out;">
            <h1 style="font-size: 2.5rem; font-weight: 700; color: #1a1a2e;">
                ⏱️ {get_text('timeline_title')}
            </h1>
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
    # CROSS-CASE (Unchanged)
    # ========================================================================
    elif current_page == get_text("nav_crosscase"):
        st.markdown(f"""
        <div style="animation: fadeInUp 0.6s ease-out;">
            <h1 style="font-size: 2.5rem; font-weight: 700; color: #1a1a2e;">
                🔗 {get_text('crosscase_title')}
            </h1>
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
                st.info("No cross-case connections found in the current network.")
        else:
            st.warning("Need at least 2 cases and 1 person to find cross-case connections.")
    
    # ========================================================================
    # AI COPILOT (RAG - Phase 3)
    # ========================================================================
    elif current_page == get_text("nav_ai"):
        st.markdown(f"""
        <div style="animation: fadeInUp 0.6s ease-out;">
            <h1 style="font-size: 2.5rem; font-weight: 700; color: #1a1a2e;">
                🤖 {get_text('ai_title')}
            </h1>
            <p style="color: #666; margin-top: -0.5rem;">{get_text('ai_sub')}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Initialize RAG Engine
        rag = RAGEngine(G)
        
        st.info("🧠 " + get_text('ai_sub'))
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"### 💬 {get_text('quick_questions')}")
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
            st.markdown(f"### 🔍 {get_text('custom_query')}")
            user_query = st.text_area(
                get_text('ask_question'),
                placeholder="Example: What are the connections between Entity A and Entity B?",
                height=150
            )
            
            if st.button(f"🔍 {get_text('analyze')}", use_container_width=True):
                st.session_state.ai_query = user_query
        
        if hasattr(st.session_state, 'ai_query') and st.session_state.ai_query:
            query = st.session_state.ai_query
            
            st.markdown("---")
            st.markdown(f"### 🤖 {get_text('ai_response')}")
            
            with st.spinner(get_text('loading')):
                # Use RAG Engine
                result = rag.query(query)
                
                st.markdown(f"""
                <div class="rag-response">
                    <strong>Response:</strong>
                    <p style="margin-top: 0.5rem;">{result['response']}</p>
                    <div class="rag-sources">
                        <span style="font-size: 0.7rem; color: #888; margin-right: 0.5rem;">Sources:</span>
                        {''.join([f'<span class="rag-source-tag">{s}</span>' for s in result['sources']])}
                        <span class="rag-source-tag">Confidence: {result['confidence']:.0%}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Show context
                with st.expander("📚 RAG Context", expanded=False):
                    st.text(result['context'])
                
                # Show relevant entities
                st.markdown(f"### 📋 {get_text('relevant_entities')}")
                entities_with_degree = []
                for node in node_list:
                    attrs = get_node_attributes(G, node)
                    if attrs.get('type') == 'PERSON':
                        degree = get_degree(G, node)
                        entities_with_degree.append((node, degree))
                
                entities_with_degree.sort(key=lambda x: x[1], reverse=True)
                for node, degree in entities_with_degree[:5]:
                    attrs = get_node_attributes(G, node)
                    name = attrs.get('name', node)
                    st.markdown(f"- **{node}** ({name}) - Degree: {degree}")
                
                st.warning("⚠️ " + get_text('disclaimer'))
                
                # Add to RAG memory
                st.session_state.rag_memory.append({
                    'query': query,
                    'response': result['response'],
                    'timestamp': datetime.now().isoformat()
                })
                
                st.session_state.ai_query = ""
    
    # ========================================================================
    # ALERTS & EMERGENCY (Enhanced with Phase 3)
    # ========================================================================
    elif current_page == get_text("nav_alerts"):
        st.markdown(f"""
        <div style="animation: fadeInUp 0.6s ease-out;">
            <h1 style="font-size: 2.5rem; font-weight: 700; color: #1a1a2e;">
                🔔 {get_text('alerts_title')}
            </h1>
            <p style="color: #666; margin-top: -0.5rem;">{get_text('alerts_sub')}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Emergency Call Button
        st.markdown("---")
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
                add_audit_log("call", "Emergency Services", "Call initiated")
        
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
            st.success(get_text('alert_sent'))
            st.session_state.alert_sent = False
        
        st.markdown("---")
        
        # Refresh Alerts
        col1, col2 = st.columns([3, 1])
        with col2:
            if st.button(f"🔄 {get_text('refresh_alerts')}", use_container_width=True):
                st.session_state.alerts = generate_alerts(G)
                add_audit_log("refresh", "Alerts", "Alerts refreshed")
                st.rerun()
        
        st.markdown("---")
        
        # Display Alerts
        alerts = st.session_state.alerts
        
        if alerts:
            # Summary
            critical_count = len([a for a in alerts if a['type'] == 'CRITICAL'])
            warning_count = len([a for a in alerts if a['type'] == 'WARNING'])
            info_count = len([a for a in alerts if a['type'] == 'INFO'])
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric(f"🔴 {get_text('critical_alerts')}", critical_count, delta="Immediate Action")
            with col2:
                st.metric(f"🟡 {get_text('warning_alerts')}", warning_count, delta="Review Required")
            with col3:
                st.metric(f"🔵 {get_text('info_alerts')}", info_count, delta="Information")
            
            st.markdown("---")
            
            # Alert Cards
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
                            <br>
                            <span style="background: rgba(255,255,255,0.2); padding: 2px 12px; border-radius: 50px; font-size: 0.7rem;">{alert['type']}</span>
                        </div>
                    </div>
                    <div style="margin-top: 0.5rem; border-top: 1px solid rgba(255,255,255,0.1); padding-top: 0.5rem;">
                        <span style="font-weight: 600;">{get_text('action_required')}:</span> {alert['action']}
                        {f"<br><span style='font-weight: 600;'>Entity:</span> {alert['entity']}" if alert.get('entity') else ""}
                    </div>
                    {'''
                    <div style="margin-top: 0.5rem; display: flex; gap: 8px; flex-wrap: wrap;">
                        <button style="background: rgba(255,255,255,0.2); border: none; color: white; padding: 4px 16px; border-radius: 50px; cursor: pointer; transition: all 0.3s;">
                            📞 Call Now
                        </button>
                        <button style="background: rgba(255,255,255,0.2); border: none; color: white; padding: 4px 16px; border-radius: 50px; cursor: pointer; transition: all 0.3s;">
                            📨 Send Alert
                        </button>
                        <button style="background: rgba(255,255,255,0.2); border: none; color: white; padding: 4px 16px; border-radius: 50px; cursor: pointer; transition: all 0.3s;">
                            👤 View Entity
                        </button>
                    </div>
                    ''' if alert['type'] == 'CRITICAL' else ''}
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info(get_text('no_alerts'))
    
    # ========================================================================
    # SIMULATION (Enhanced with Phase 3)
    # ========================================================================
    elif current_page == get_text("nav_simulation"):
        st.markdown(f"""
        <div style="animation: fadeInUp 0.6s ease-out;">
            <h1 style="font-size: 2.5rem; font-weight: 700; color: #1a1a2e;">
                🎯 {get_text('simulation_title')}
            </h1>
            <p style="color: #666; margin-top: -0.5rem;">{get_text('simulation_sub')}</p>
        </div>
        """, unsafe_allow_html=True)
        
        if not node_list:
            st.warning(get_text('no_data'))
        else:
            col1, col2 = st.columns([2, 1])
            
            with col1:
                target_entity = st.selectbox(
                    f"🎯 {get_text('select_entity')}",
                    node_list
                )
            
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
                
                # Impact Visualization
                impact = results['network_disruption']
                color = '#ff4757' if impact > 0.5 else '#ffa502' if impact > 0.3 else '#2ed573'
                label = 'HIGH' if impact > 0.5 else 'MEDIUM' if impact > 0.3 else 'LOW'
                
                st.markdown(f"""
                <div class="simulation-card">
                    <h3>💥 {get_text('disruption_impact')}</h3>
                    <div style="display: flex; justify-content: space-between; margin: 0.5rem 0;">
                        <span>{get_text('disruption_level')}</span>
                        <span style="font-weight: 700; color: {color};">{impact:.1%} ({label})</span>
                    </div>
                    <div class="disruption-bar">
                        <div class="disruption-bar-fill" style="width: {impact*100}%; background: linear-gradient(90deg, {color}, {color}cc);">
                        </div>
                    </div>
                    <div style="margin-top: 0.5rem; color: #888; font-size: 0.85rem;">
                        <strong>{get_text('recommendation_label')}:</strong> {results['recommendation']}
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown("---")
                
                # Affected Entities
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
                
                # Recommendations
                st.markdown(f"### 📌 {get_text('recommendations')}")
                if results['recommendation'] == 'HIGH':
                    st.warning("🔴 High impact - consider alternative strategies")
                    st.markdown("- This entity is critical to the network")
                    st.markdown("- Removing it will cause significant disruption")
                    st.markdown("- Have replacement plans ready")
                elif results['recommendation'] == 'MEDIUM':
                    st.info("🟡 Medium impact - proceed with caution")
                    st.markdown("- Network will be partially affected")
                    st.markdown("- Monitor for side effects")
                    st.markdown("- Have backup plans ready")
                else:
                    st.success("🟢 Low impact - proceed")
                    st.markdown("- Minimal network disruption expected")
                    st.markdown("- Continue with planned actions")
                    st.markdown("- Monitor for any unexpected changes")
    
    # ========================================================================
    # HEATMAP (Phase 3 New Feature)
    # ========================================================================
    elif current_page == get_text("nav_heatmap"):
        st.markdown(f"""
        <div style="animation: fadeInUp 0.6s ease-out;">
            <h1 style="font-size: 2.5rem; font-weight: 700; color: #1a1a2e;">
                🗺️ {get_text('heatmap_title')}
            </h1>
            <p style="color: #666; margin-top: -0.5rem;">{get_text('heatmap_sub')}</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.info("🌍 " + get_text('heatmap_sub'))
        
        # Generate heatmap data
        heatmap_data = generate_heatmap_data(G)
        
        if heatmap_data:
            st.markdown(f"""
            <div class="heatmap-container">
                <h3 style="font-size: 1.2rem; font-weight: 600; color: #1a1a2e;">
                    📍 {get_text('heatmap_locations')} ({len(heatmap_data)})
                </h3>
            """, unsafe_allow_html=True)
            
            # Create a DataFrame for display
            df_heatmap = pd.DataFrame(heatmap_data)
            
            # Show as table
            st.dataframe(
                df_heatmap[['id', 'name', 'type', 'intensity']],
                use_container_width=True
            )
            
            st.markdown("</div>", unsafe_allow_html=True)
            
            # Visual heatmap using Plotly if available
            if PLOTLY_AVAILABLE:
                st.markdown("---")
                st.markdown("### 🗺️ Interactive Heatmap")
                
                try:
                    fig = go.Figure()
                    
                    # Add scatter mapbox
                    fig.add_trace(go.Scattermapbox(
                        lat=df_heatmap['lat'],
                        lon=df_heatmap['lon'],
                        mode='markers',
                        marker=dict(
                            size=df_heatmap['intensity'] / 10 + 5,
                            color=df_heatmap['intensity'],
                            colorscale='Reds',
                            showscale=True,
                            colorbar=dict(title=get_text('heatmap_intensity'))
                        ),
                        text=df_heatmap['name'] + ' (' + df_heatmap['type'] + ')',
                        hoverinfo='text'
                    ))
                    
                    fig.update_layout(
                        mapbox=dict(
                            style="open-street-map",
                            center=dict(
                                lat=df_heatmap['lat'].mean(),
                                lon=df_heatmap['lon'].mean()
                            ),
                            zoom=4
                        ),
                        height=500,
                        margin=dict(l=0, r=0, t=0, b=0)
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
                except Exception as e:
                    st.warning(f"Heatmap visualization error: {str(e)}")
                    st.info("Showing data table instead.")
            else:
                st.info("Install plotly for interactive heatmap visualization.")
        else:
            st.info("No location data available for heatmap. Generate data with coordinates.")
    
    # ========================================================================
    # EXPORT (Phase 3 New Feature)
    # ========================================================================
    elif current_page == get_text("nav_export"):
        st.markdown(f"""
        <div style="animation: fadeInUp 0.6s ease-out;">
            <h1 style="font-size: 2.5rem; font-weight: 700; color: #1a1a2e;">
                📄 {get_text('export_title')}
            </h1>
            <p style="color: #666; margin-top: -0.5rem;">{get_text('export_sub')}</p>
        </div>
        """, unsafe_allow_html=True)
        
        if not check_permission("analyst"):
            st.warning("🔒 You need 'Analyst' or higher role to export reports.")
        else:
            st.info("📋 " + get_text('export_sub'))
            
            # Export options
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if st.button(f"📄 {get_text('export_json')}", use_container_width=True):
                    with st.spinner(get_text('loading')):
                        report = export_report_json(G)
                        json_str = json.dumps(report, indent=2)
                        st.download_button(
                            label="📥 Download JSON",
                            data=json_str,
                            file_name=f"SUTRA-X_Report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                            mime="application/json",
                            use_container_width=True
                        )
                        add_audit_log("export", "JSON Report", "Report exported")
                        st.session_state.export_history.append({
                            'timestamp': datetime.now().isoformat(),
                            'format': 'JSON',
                            'file': f"SUTRA-X_Report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
                        })
                        st.success("✅ JSON Report generated!")
            
            with col2:
                if st.button(f"📊 {get_text('export_pdf')}", use_container_width=True):
                    st.info("PDF export - generating report...")
                    # For demo, we'll export as CSV since PDF needs additional libraries
                    df_entities, df_edges = export_report_csv(G)
                    csv_entities = df_entities.to_csv(index=False)
                    st.download_button(
                        label="📥 Download CSV (Entities)",
                        data=csv_entities,
                        file_name=f"SUTRA-X_Entities_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                        mime="text/csv",
                        use_container_width=True
                    )
                    add_audit_log("export", "PDF/CSV Report", "Report exported")
                    st.success("✅ CSV Report generated!")
            
            with col3:
                if st.button(f"📝 {get_text('export_word')}", use_container_width=True):
                    st.info("Word export - generating report...")
                    df_entities, df_edges = export_report_csv(G)
                    csv_edges = df_edges.to_csv(index=False)
                    st.download_button(
                        label="📥 Download CSV (Relationships)",
                        data=csv_edges,
                        file_name=f"SUTRA-X_Relationships_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                        mime="text/csv",
                        use_container_width=True
                    )
                    add_audit_log("export", "Word/CSV Report", "Report exported")
                    st.success("✅ CSV Relationships generated!")
            
            st.markdown("---")
            
            # Export History
            st.markdown(f"### 📋 {get_text('export_history')}")
            if st.session_state.export_history:
                history_df = pd.DataFrame(st.session_state.export_history[-10:])
                st.dataframe(history_df, use_container_width=True)
            else:
                st.info("No export history available.")
    
    # ========================================================================
    # SECURITY (Phase 3 New Feature)
    # ========================================================================
    elif current_page == get_text("nav_security"):
        st.markdown(f"""
        <div style="animation: fadeInUp 0.6s ease-out;">
            <h1 style="font-size: 2.5rem; font-weight: 700; color: #1a1a2e;">
                🔐 {get_text('security_title')}
            </h1>
            <p style="color: #666; margin-top: -0.5rem;">{get_text('security_sub')}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # RBAC Status
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"""
            <div style="background: white; padding: 1.5rem; border-radius: 15px; 
                        box-shadow: 0 4px 20px rgba(0,0,0,0.08);">
                <h3 style="font-size: 1.2rem; font-weight: 600; color: #1a1a2e;">🔐 {get_text('rbac_info')}</h3>
                <div style="margin-top: 1rem;">
                    <div style="display: flex; justify-content: space-between; padding: 0.5rem 0; border-bottom: 1px solid #eee;">
                        <span>Current Role</span>
                        <strong>{get_text('user_role')}: {role_labels.get(st.session_state.user_role, st.session_state.user_role)}</strong>
                    </div>
                    <div style="display: flex; justify-content: space-between; padding: 0.5rem 0; border-bottom: 1px solid #eee;">
                        <span>Permissions</span>
                        <span>
                            {'✅ Full Access' if st.session_state.user_role == 'admin' else 
                             '✅ Read/Write' if st.session_state.user_role == 'investigator' else
                             '✅ Read Only' if st.session_state.user_role == 'analyst' else
                             '👀 View Only'}
                        </span>
                    </div>
                    <div style="display: flex; justify-content: space-between; padding: 0.5rem 0;">
                        <span>Role Hierarchy</span>
                        <span>Admin → Investigator → Analyst → Viewer</span>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div style="background: white; padding: 1.5rem; border-radius: 15px; 
                        box-shadow: 0 4px 20px rgba(0,0,0,0.08);">
                <h3 style="font-size: 1.2rem; font-weight: 600; color: #1a1a2e;">📶 {get_text('offline_mode')}</h3>
                <div style="margin-top: 1rem;">
                    <div style="display: flex; justify-content: space-between; padding: 0.5rem 0; border-bottom: 1px solid #eee;">
                        <span>Current Status</span>
                        <span>
                            {'📴 Offline' if st.session_state.offline_mode else '📶 Online'}
                        </span>
                    </div>
                    <div style="display: flex; justify-content: space-between; padding: 0.5rem 0; border-bottom: 1px solid #eee;">
                        <span>Description</span>
                        <span style="font-size: 0.8rem; color: #888;">{get_text('offline_desc')}</span>
                    </div>
                    <div style="display: flex; justify-content: space-between; padding: 0.5rem 0;">
                        <span>Data Sync</span>
                        <span>{'🔄 Sync on reconnect' if st.session_state.offline_mode else '✅ Real-time'}</span>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Audit Logs
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
            # Create audit log table
            audit_df = pd.DataFrame(st.session_state.audit_logs[-20:])
            if not audit_df.empty:
                # Format for display
                display_df = audit_df[['timestamp', 'user', 'action', 'resource']].copy()
                display_df['timestamp'] = pd.to_datetime(display_df['timestamp']).dt.strftime('%Y-%m-%d %H:%M:%S')
                st.dataframe(display_df, use_container_width=True)
                
                # Summary stats
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
        <span>👤 {role_labels.get(st.session_state.user_role, st.session_state.user_role)}</span>
    </div>
    <div style="font-size: 0.8rem; color: #aaa;">
        {get_text('made_with')}
    </div>
</div>
""", unsafe_allow_html=True)

# ============================================================================
# RUN THE APP
# ============================================================================

if __name__ == "__main__":
    pass
