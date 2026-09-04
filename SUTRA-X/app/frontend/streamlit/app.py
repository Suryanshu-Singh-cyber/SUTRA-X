"""
SUTRA-X: Smart Unified Threat & Relationship Analytics
AI-Powered Criminal Network Analysis System
SIH 2026 | Complete Phase 2 with Full Multi-Language, Emergency Alerts, Simulations
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import json
import base64
import io
from pathlib import Path
import sys
import os
import hashlib
import time
import re

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
# COMPLETE MULTI-LANGUAGE SUPPORT (10 Languages)
# ============================================================================

LANGUAGES = {
    "en": {
        "name": "English",
        "flag": "🇬🇧",
        # Navigation
        "nav_dashboard": "Dashboard",
        "nav_graph": "Network Graph",
        "nav_entity": "Entity Profile",
        "nav_timeline": "Timeline",
        "nav_crosscase": "Cross-Case Discovery",
        "nav_ai": "AI Assistant",
        "nav_alerts": "Alerts & Emergency",
        "nav_simulation": "What-If Simulation",
        # Dashboard
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
        # Common
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
        # Alerts
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
        # Simulation
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
        # Cross-Case
        "crosscase_title": "Cross-Case Connection Discovery",
        "crosscase_sub": "Uncover hidden connections between cases",
        "shared_entities": "Shared Entities",
        "confidence": "Confidence",
        "total_connections": "Total Connections",
        "shared_persons": "Shared Persons",
        # Entity Profile
        "entity_intelligence": "Entity Intelligence",
        "quick_stats": "Quick Stats",
        "direct_connections": "Direct Connections",
        "network_degree": "Network Degree",
        "priority_score": "Priority Score",
        # Timeline
        "timeline_title": "Investigation Timeline",
        "timeline_sub": "Track network evolution over time",
        "key_events": "Key Events",
        # AI Assistant
        "ai_title": "AI Investigation Copilot",
        "ai_sub": "Get AI-powered insights",
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
        # Footer
        "made_with": "Made with ❤️ for Smart India Hackathon 2026",
        "version": "v2.0.0",
        # Emergency
        "emergency_title": "🚨 EMERGENCY ALERT",
        "emergency_desc": "Critical threat detected in the network",
        "call_police": "🚔 Call Police",
        "call_emergency": "📞 Emergency Services",
        "send_alert": "📨 Send Alert to Team",
        "alert_sent": "✅ Alert sent to all investigators!",
        "call_initiated": "📞 Emergency call initiated...",
        # Status
        "online": "Online",
        "offline": "Offline",
        "data_loaded": "Data Loaded",
        "no_data_loaded": "No data loaded",
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
        "ai_title": "एआई जांच सहायक",
        "ai_sub": "एआई-संचालित अंतर्दृष्टि प्राप्त करें",
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
        "version": "v2.0.0",
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
        "ai_title": "AI விசாரணை உதவியாளர்",
        "ai_sub": "AI-இயக்கப்பட்ட நுண்ணறிவுகளைப் பெறுங்கள்",
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
        "version": "v2.0.0",
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
        "ai_sub": "AI-ఆధారిత అంతర్దృష్టులను పొందండి",
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
        "version": "v2.0.0",
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
    },
    "bn": {
        "name": "বাংলা",
        "flag": "🇮🇳",
        "nav_dashboard": "ড্যাশবোর্ড",
        "nav_graph": "নেটওয়ার্ক গ্রাফ",
        "nav_entity": "এন্টিটি প্রোফাইল",
        "nav_timeline": "টাইমলাইন",
        "nav_crosscase": "ক্রস-কেস আবিষ্কার",
        "nav_ai": "AI সহায়ক",
        "nav_alerts": "সতর্কতা এবং জরুরি",
        "nav_simulation": "কী-যদি সিমুলেশন",
        "dashboard_title": "কমান্ড সেন্টার",
        "dashboard_sub": "রিয়েল-টাইম ইন্টেলিজেন্স ড্যাশবোর্ড",
        "total_entities": "মোট এন্টিটি",
        "relationships": "সম্পর্ক",
        "priority_leads": "অগ্রাধিকার লিড",
        "cross_case_links": "ক্রস-কেস লিঙ্ক",
        "active_alerts": "সক্রিয় সতর্কতা",
        "priority_leads_title": "অগ্রাধিকার তদন্ত লিড",
        "no_priority": "কোন অগ্রাধিকার লিড পাওয়া যায়নি",
        "recent_activity": "সাম্প্রতিক কার্যকলাপ",
        "network_stats": "নেটওয়ার্ক পরিসংখ্যান",
        "search_entity": "এন্টিটি অনুসন্ধান করুন",
        "view_profile": "প্রোফাইল দেখুন",
        "connections": "সংযোগ",
        "properties": "বৈশিষ্ট্য",
        "recommendations": "সুপারিশ",
        "evidence": "প্রমাণ",
        "priority_high": "উচ্চ",
        "priority_medium": "মধ্যম",
        "priority_low": "নিম্ন",
        "generate_data": "নমুনা ডেটা তৈরি করুন",
        "loading": "লোড হচ্ছে...",
        "success": "সফল!",
        "error": "ত্রুটি",
        "no_data": "কোন ডেটা লোড হয়নি",
        "view": "দেখুন",
        "alerts_title": "সতর্কতা এবং জরুরি প্রতিক্রিয়া",
        "alerts_sub": "রিয়েল-টাইম ক্রিটিক্যাল সতর্কতা এবং জরুরি বিজ্ঞপ্তি",
        "critical_alerts": "গুরুতর সতর্কতা",
        "warning_alerts": "সতর্কতা",
        "info_alerts": "তথ্য",
        "emergency_call": "জরুরি কল",
        "call_now": "📞 এখন কল করুন",
        "alert_details": "সতর্কতা বিবরণ",
        "action_required": "প্রয়োজনীয় পদক্ষেপ",
        "immediate_action": "তাৎক্ষণিক তদন্ত প্রয়োজন",
        "review_required": "পর্যালোচনা প্রয়োজন",
        "information_only": "শুধুমাত্র তথ্য",
        "no_alerts": "কোন সক্রিয় সতর্কতা নেই",
        "refresh_alerts": "সতর্কতা রিফ্রেশ করুন",
        "simulation_title": "কী-যদি সিমুলেশন",
        "simulation_sub": "নেটওয়ার্ক বিঘ্ন দৃশ্যকল্প অনুকরণ করুন",
        "select_entity": "অপসারণের জন্য এন্টিটি নির্বাচন করুন",
        "run_simulation": "সিমুলেশন চালান",
        "simulation_results": "সিমুলেশন ফলাফল",
        "target_entity": "লক্ষ্য এন্টিটি",
        "removed_connections": "অপসারিত সংযোগ",
        "remaining_entities": "অবশিষ্ট এন্টিটি",
        "isolated_entities": "বিচ্ছিন্ন এন্টিটি",
        "disruption_impact": "নেটওয়ার্ক বিঘ্ন প্রভাব",
        "disruption_level": "বিঘ্ন স্তর",
        "affected_entities": "প্রভাবিত এন্টিটি",
        "recommendation_label": "সুপারিশ",
        "crosscase_title": "ক্রস-কেস সংযোগ আবিষ্কার",
        "crosscase_sub": "মামলার মধ্যে লুকানো সংযোগ আবিষ্কার করুন",
        "shared_entities": "ভাগ করা এন্টিটি",
        "confidence": "আত্মবিশ্বাস",
        "total_connections": "মোট সংযোগ",
        "shared_persons": "ভাগ করা ব্যক্তি",
        "entity_intelligence": "এন্টিটি ইন্টেলিজেন্স",
        "quick_stats": "দ্রুত পরিসংখ্যান",
        "direct_connections": "সরাসরি সংযোগ",
        "network_degree": "নেটওয়ার্ক ডিগ্রি",
        "priority_score": "অগ্রাধিকার স্কোর",
        "timeline_title": "তদন্ত টাইমলাইন",
        "timeline_sub": "সময়ের সাথে নেটওয়ার্ক বিবর্তন ট্র্যাক করুন",
        "key_events": "মূল ঘটনা",
        "ai_title": "AI তদন্ত সহায়ক",
        "ai_sub": "AI-চালিত অন্তর্দৃষ্টি পান",
        "quick_questions": "দ্রুত প্রশ্ন",
        "custom_query": "কাস্টম প্রশ্ন",
        "analyze": "বিশ্লেষণ করুন",
        "ask_question": "আপনার প্রশ্ন জিজ্ঞাসা করুন",
        "ai_response": "AI প্রতিক্রিয়া",
        "key_findings": "মূল অনুসন্ধান",
        "actionable_insights": "কার্যকর অন্তর্দৃষ্টি",
        "next_steps": "পরবর্তী পদক্ষেপ",
        "relevant_entities": "প্রাসঙ্গিক এন্টিটি",
        "disclaimer": "এটি একটি AI-উত্পন্ন বিশ্লেষণ। সমস্ত অনুসন্ধান মানব তদন্তকারীদের দ্বারা যাচাই করা উচিত।",
        "made_with": "স্মার্ট ইন্ডিয়া হ্যাকাথন 2026 এর জন্য ❤️ দিয়ে তৈরি",
        "version": "v2.0.0",
        "emergency_title": "🚨 জরুরি সতর্কতা",
        "emergency_desc": "নেটওয়ার্কে গুরুতর হুমকি পাওয়া গেছে",
        "call_police": "🚔 পুলিশকে কল করুন",
        "call_emergency": "📞 জরুরি সেবা",
        "send_alert": "📨 দলকে সতর্কতা পাঠান",
        "alert_sent": "✅ সমস্ত তদন্তকারীদের কাছে সতর্কতা পাঠানো হয়েছে!",
        "call_initiated": "📞 জরুরি কল শুরু হয়েছে...",
        "online": "অনলাইন",
        "offline": "অফলাইন",
        "data_loaded": "ডেটা লোড হয়েছে",
        "no_data_loaded": "কোন ডেটা লোড হয়নি",
    },
    "ml": {
        "name": "മലയാളം",
        "flag": "🇮🇳",
        "nav_dashboard": "ഡാഷ്ബോർഡ്",
        "nav_graph": "നെറ്റ്വർക്ക് ഗ്രാഫ്",
        "nav_entity": "എന്റിറ്റി പ്രൊഫൈൽ",
        "nav_timeline": "ടൈംലൈൻ",
        "nav_crosscase": "ക്രോസ്-കേസ് കണ്ടെത്തൽ",
        "nav_ai": "AI അസിസ്റ്റന്റ്",
        "nav_alerts": "അലേർട്ടുകളും അടിയന്തരവും",
        "nav_simulation": "എന്ത്-എങ്കിൽ സിമുലേഷൻ",
        "dashboard_title": "കമാൻഡ് സെന്റർ",
        "dashboard_sub": "തത്സമയ ഇന്റലിജൻസ് ഡാഷ്ബോർഡ്",
        "total_entities": "ആകെ എന്റിറ്റികൾ",
        "relationships": "ബന്ധങ്ങൾ",
        "priority_leads": "മുൻഗണന ലീഡുകൾ",
        "cross_case_links": "ക്രോസ്-കേസ് ലിങ്കുകൾ",
        "active_alerts": "സജീവ അലേർട്ടുകൾ",
        "priority_leads_title": "മുൻഗണന അന്വേഷണ ലീഡുകൾ",
        "no_priority": "മുൻഗണന ലീഡുകളൊന്നും കണ്ടെത്തിയില്ല",
        "recent_activity": "സമീപകാല പ്രവർത്തനം",
        "network_stats": "നെറ്റ്വർക്ക് സ്ഥിതിവിവരക്കണക്കുകൾ",
        "search_entity": "എന്റിറ്റി തിരയുക",
        "view_profile": "പ്രൊഫൈൽ കാണുക",
        "connections": "കണക്ഷനുകൾ",
        "properties": "സവിശേഷതകൾ",
        "recommendations": "ശുപാർശകൾ",
        "evidence": "തെളിവുകൾ",
        "priority_high": "ഉയർന്ന",
        "priority_medium": "ഇടത്തരം",
        "priority_low": "താഴ്ന്ന",
        "generate_data": "സാമ്പിൾ ഡാറ്റ സൃഷ്ടിക്കുക",
        "loading": "ലോഡ് ചെയ്യുന്നു...",
        "success": "വിജയം!",
        "error": "പിശക്",
        "no_data": "ഡാറ്റ ലോഡ് ചെയ്തിട്ടില്ല",
        "view": "കാണുക",
        "alerts_title": "അലേർട്ടുകളും അടിയന്തര പ്രതികരണവും",
        "alerts_sub": "തത്സമയ നിർണായക അലേർട്ടുകളും അടിയന്തര അറിയിപ്പുകളും",
        "critical_alerts": "നിർണായക അലേർട്ടുകൾ",
        "warning_alerts": "മുന്നറിയിപ്പുകൾ",
        "info_alerts": "വിവരങ്ങൾ",
        "emergency_call": "അടിയന്തര കോൾ",
        "call_now": "📞 ഇപ്പോൾ വിളിക്കുക",
        "alert_details": "അലേർട്ട് വിശദാംശങ്ങൾ",
        "action_required": "ആവശ്യമായ നടപടി",
        "immediate_action": "ഉടനടി അന്വേഷണം ആവശ്യമാണ്",
        "review_required": "അവലോകനം ആവശ്യമാണ്",
        "information_only": "വിവരങ്ങൾ മാത്രം",
        "no_alerts": "സജീവ അലേർട്ടുകളൊന്നുമില്ല",
        "refresh_alerts": "അലേർട്ടുകൾ പുതുക്കുക",
        "simulation_title": "എന്ത്-എങ്കിൽ സിമുലേഷൻ",
        "simulation_sub": "നെറ്റ്വർക്ക് തടസ്സ സാഹചര്യങ്ങൾ അനുകരിക്കുക",
        "select_entity": "നീക്കം ചെയ്യാനുള്ള എന്റിറ്റി തിരഞ്ഞെടുക്കുക",
        "run_simulation": "സിമുലേഷൻ പ്രവർത്തിപ്പിക്കുക",
        "simulation_results": "സിമുലേഷൻ ഫലങ്ങൾ",
        "target_entity": "ലക്ഷ്യ എന്റിറ്റി",
        "removed_connections": "നീക്കം ചെയ്ത കണക്ഷനുകൾ",
        "remaining_entities": "ശേഷിക്കുന്ന എന്റിറ്റികൾ",
        "isolated_entities": "ഒറ്റപ്പെട്ട എന്റിറ്റികൾ",
        "disruption_impact": "നെറ്റ്വർക്ക് തടസ്സ ആഘാതം",
        "disruption_level": "തടസ്സ നില",
        "affected_entities": "ബാധിക്കപ്പെട്ട എന്റിറ്റികൾ",
        "recommendation_label": "ശുപാർശ",
        "crosscase_title": "ക്രോസ്-കേസ് കണക്ഷൻ കണ്ടെത്തൽ",
        "crosscase_sub": "കേസുകൾക്കിടയിൽ മറഞ്ഞിരിക്കുന്ന കണക്ഷനുകൾ കണ്ടെത്തുക",
        "shared_entities": "പങ്കിട്ട എന്റിറ്റികൾ",
        "confidence": "ആത്മവിശ്വാസം",
        "total_connections": "ആകെ കണക്ഷനുകൾ",
        "shared_persons": "പങ്കിട്ട വ്യക്തികൾ",
        "entity_intelligence": "എന്റിറ്റി ഇന്റലിജൻസ്",
        "quick_stats": "ദ്രുത സ്ഥിതിവിവരക്കണക്കുകൾ",
        "direct_connections": "നേരിട്ടുള്ള കണക്ഷനുകൾ",
        "network_degree": "നെറ്റ്വർക്ക് ഡിഗ്രി",
        "priority_score": "മുൻഗണന സ്കോർ",
        "timeline_title": "അന്വേഷണ ടൈംലൈൻ",
        "timeline_sub": "കാലക്രമേണ നെറ്റ്വർക്ക് പരിണാമം ട്രാക്ക് ചെയ്യുക",
        "key_events": "പ്രധാന സംഭവങ്ങൾ",
        "ai_title": "AI അന്വേഷണ സഹായി",
        "ai_sub": "AI-അധിഷ്ഠിത ഉൾക്കാഴ്ചകൾ നേടുക",
        "quick_questions": "ദ്രുത ചോദ്യങ്ങൾ",
        "custom_query": "ഇഷ്ടാനുസൃത ചോദ്യം",
        "analyze": "വിശകലനം ചെയ്യുക",
        "ask_question": "നിങ്ങളുടെ ചോദ്യം ചോദിക്കുക",
        "ai_response": "AI പ്രതികരണം",
        "key_findings": "പ്രധാന കണ്ടെത്തലുകൾ",
        "actionable_insights": "പ്രവർത്തനക്ഷമമായ ഉൾക്കാഴ്ചകൾ",
        "next_steps": "അടുത്ത ഘട്ടങ്ങൾ",
        "relevant_entities": "ബന്ധപ്പെട്ട എന്റിറ്റികൾ",
        "disclaimer": "ഇത് AI-സൃഷ്ടിച്ച വിശകലനമാണ്. എല്ലാ കണ്ടെത്തലുകളും മനുഷ്യ അന്വേഷണ ഉദ്യോഗസ്ഥർ പരിശോധിക്കണം.",
        "made_with": "സ്മാർട്ട് ഇന്ത്യ ഹാക്കത്തോൺ 2026 നായി ❤️ ഉപയോഗിച്ച് നിർമ്മിച്ചത്",
        "version": "v2.0.0",
        "emergency_title": "🚨 അടിയന്തര അലേർട്ട്",
        "emergency_desc": "നെറ്റ്വർക്കിൽ നിർണായക ഭീഷണി കണ്ടെത്തി",
        "call_police": "🚔 പോലീസിനെ വിളിക്കുക",
        "call_emergency": "📞 അടിയന്തര സേവനങ്ങൾ",
        "send_alert": "📨 ടീമിന് അലേർട്ട് അയയ്ക്കുക",
        "alert_sent": "✅ എല്ലാ അന്വേഷണ ഉദ്യോഗസ്ഥർക്കും അലേർട്ട് അയച്ചു!",
        "call_initiated": "📞 അടിയന്തര കോൾ ആരംഭിച്ചു...",
        "online": "ഓൺലൈൻ",
        "offline": "ഓഫ്‌ലൈൻ",
        "data_loaded": "ഡാറ്റ ലോഡ് ചെയ്തു",
        "no_data_loaded": "ഡാറ്റ ലോഡ് ചെയ്തിട്ടില്ല",
    },
    "ur": {
        "name": "اردو",
        "flag": "🇮🇳",
        "nav_dashboard": "ڈیش بورڈ",
        "nav_graph": "نیٹ ورک گراف",
        "nav_entity": "انٹیٹی پروفائل",
        "nav_timeline": "ٹائم لائن",
        "nav_crosscase": "کراس کیس دریافت",
        "nav_ai": "AI اسسٹنٹ",
        "nav_alerts": "الرٹس اور ہنگامی",
        "nav_simulation": "کیا-اگر سمولیشن",
        "dashboard_title": "کمانڈ سینٹر",
        "dashboard_sub": "ریئل ٹائم انٹیلی جنس ڈیش بورڈ",
        "total_entities": "کل انٹیٹیز",
        "relationships": "تعلقات",
        "priority_leads": "ترجیحی لیڈز",
        "cross_case_links": "کراس کیس لنکس",
        "active_alerts": "فعال الرٹس",
        "priority_leads_title": "ترجیحی تفتیش لیڈز",
        "no_priority": "کوئی ترجیحی لیڈ نہیں ملی",
        "recent_activity": "حالیہ سرگرمی",
        "network_stats": "نیٹ ورک کے اعدادوشمار",
        "search_entity": "انٹیٹی تلاش کریں",
        "view_profile": "پروفائل دیکھیں",
        "connections": "کنکشنز",
        "properties": "خصائص",
        "recommendations": "سفارشات",
        "evidence": "شواہد",
        "priority_high": "اعلیٰ",
        "priority_medium": "درمیانی",
        "priority_low": "کم",
        "generate_data": "نمونہ ڈیٹا بنائیں",
        "loading": "لوڈ ہو رہا ہے...",
        "success": "کامیابی!",
        "error": "خرابی",
        "no_data": "کوئی ڈیٹا لوڈ نہیں",
        "view": "دیکھیں",
        "alerts_title": "الرٹس اور ہنگامی ردعمل",
        "alerts_sub": "ریئل ٹائم اہم الرٹس اور ہنگامی اطلاعات",
        "critical_alerts": "اہم الرٹس",
        "warning_alerts": "انتباہات",
        "info_alerts": "معلومات",
        "emergency_call": "ہنگامی کال",
        "call_now": "📞 ابھی کال کریں",
        "alert_details": "الرٹ کی تفصیلات",
        "action_required": "مطلوبہ کارروائی",
        "immediate_action": "فوری تفتیش ضروری",
        "review_required": "جائزہ ضروری",
        "information_only": "صرف معلومات",
        "no_alerts": "کوئی فعال الرٹس نہیں",
        "refresh_alerts": "الرٹس ریفریش کریں",
        "simulation_title": "کیا-اگر سمولیشن",
        "simulation_sub": "نیٹ ورک میں خلل کے مناظر کی نقل کریں",
        "select_entity": "ہٹانے کے لیے انٹیٹی منتخب کریں",
        "run_simulation": "سمولیشن چلائیں",
        "simulation_results": "سمولیشن کے نتائج",
        "target_entity": "ہدف انٹیٹی",
        "removed_connections": "ہٹائے گئے کنکشنز",
        "remaining_entities": "باقی انٹیٹیز",
        "isolated_entities": "الگ تھلگ انٹیٹیز",
        "disruption_impact": "نیٹ ورک میں خلل کا اثر",
        "disruption_level": "خلل کی سطح",
        "affected_entities": "متاثرہ انٹیٹیز",
        "recommendation_label": "سفارش",
        "crosscase_title": "کراس کیس کنکشن دریافت",
        "crosscase_sub": "کیسز کے درمیان پوشیدہ کنکشنز دریافت کریں",
        "shared_entities": "مشترکہ انٹیٹیز",
        "confidence": "اعتماد",
        "total_connections": "کل کنکشنز",
        "shared_persons": "مشترکہ افراد",
        "entity_intelligence": "انٹیٹی انٹیلی جنس",
        "quick_stats": "فوری اعدادوشمار",
        "direct_connections": "براہ راست کنکشنز",
        "network_degree": "نیٹ ورک ڈگری",
        "priority_score": "ترجیحی اسکور",
        "timeline_title": "تفتیش ٹائم لائن",
        "timeline_sub": "وقت کے ساتھ نیٹ ورک کے ارتقاء کو ٹریک کریں",
        "key_events": "اہم واقعات",
        "ai_title": "AI تفتیش اسسٹنٹ",
        "ai_sub": "AI سے چلنے والی بصیرت حاصل کریں",
        "quick_questions": "فوری سوالات",
        "custom_query": "اپنی مرضی کا سوال",
        "analyze": "تجزیہ کریں",
        "ask_question": "اپنا سوال پوچھیں",
        "ai_response": "AI جواب",
        "key_findings": "اہم نتائج",
        "actionable_insights": "قابل عمل بصیرت",
        "next_steps": "اگلے اقدامات",
        "relevant_entities": "متعلقہ انٹیٹیز",
        "disclaimer": "یہ AI سے تیار کردہ تجزیہ ہے۔ تمام نتائج کو انسانی تفتیش کاروں سے تصدیق کرنی چاہیے۔",
        "made_with": "سمارٹ انڈیا ہیکاتھون 2026 کے لیے ❤️ کے ساتھ بنایا گیا",
        "version": "v2.0.0",
        "emergency_title": "🚨 ہنگامی الرٹ",
        "emergency_desc": "نیٹ ورک میں اہم خطرہ پایا گیا",
        "call_police": "🚔 پولیس کو کال کریں",
        "call_emergency": "📞 ہنگامی خدمات",
        "send_alert": "📨 ٹیم کو الرٹ بھیجیں",
        "alert_sent": "✅ تمام تفتیش کاروں کو الرٹ بھیجا گیا!",
        "call_initiated": "📞 ہنگامی کال شروع کی گئی...",
        "online": "آن لائن",
        "offline": "آف لائن",
        "data_loaded": "ڈیٹا لوڈ ہوگیا",
        "no_data_loaded": "کوئی ڈیٹا لوڈ نہیں",
    }
}

def get_text(key):
    """Get translated text based on current language with fallback to English"""
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
    
    num_persons = 35
    persons = []
    for i in range(num_persons):
        name = f"{random.choice(first_names)} {random.choice(last_names)}"
        person_id = f"P-{i+1:04d}"
        G.add_node(person_id, type='PERSON', name=name, 
                   age=random.randint(22, 60),
                   city=random.choice(locations_list),
                   occupation=random.choice(['Business', 'Student', 'Government', 'Private', 'Unemployed', 'Professional']))
        persons.append(person_id)
    
    phones = []
    for i in range(25):
        phone_id = f"PH-{i+1:04d}"
        number = f"98{random.randint(10000000, 99999999)}"
        G.add_node(phone_id, type='PHONE', number=number, 
                   provider=random.choice(['Jio', 'Airtel', 'Vodafone', 'BSNL']))
        phones.append(phone_id)
        owner = random.choice(persons)
        G.add_edge(owner, phone_id, type='OWNS', confidence=0.8, timestamp=datetime.now().isoformat())
    
    accounts = []
    for i in range(18):
        account_id = f"ACC-{i+1:04d}"
        G.add_node(account_id, type='ACCOUNT', 
                   bank=random.choice(['SBI', 'HDFC', 'ICICI', 'Axis', 'PNB', 'Kotak', 'Yes Bank']))
        accounts.append(account_id)
        owner = random.choice(persons)
        G.add_edge(owner, account_id, type='OWNS', confidence=0.7, timestamp=datetime.now().isoformat())
    
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
    
    locations = []
    location_names = ['Connaught Place', 'Bandra West', 'Indiranagar', 'T. Nagar', 
                      'Hitech City', 'Juhu', 'Koramangala', 'Marine Drive', 'Park Street', 'MG Road']
    for i in range(10):
        loc_id = f"L-{i+1:04d}"
        G.add_node(loc_id, type='LOCATION', 
                   name=location_names[i] if i < len(location_names) else f"Location {i+1}",
                   city=random.choice(locations_list))
        locations.append(loc_id)
    
    cases = []
    case_titles = ['Drug Trafficking Ring', 'Financial Fraud Network', 'Arms Dealing', 
                   'Cyber Crime Syndicate', 'Money Laundering', 'Human Trafficking',
                   'Counterfeit Currency', 'Organized Crime']
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
    
    for _ in range(40):
        caller = random.choice(phones)
        receiver = random.choice(phones)
        if caller != receiver:
            G.add_edge(caller, receiver, type='CALLED', 
                      duration=random.randint(30, 900),
                      timestamp=(datetime.now() - timedelta(days=random.randint(1, 60))).isoformat())
    
    for _ in range(30):
        from_acc = random.choice(accounts)
        to_acc = random.choice(accounts)
        if from_acc != to_acc:
            amount = random.randint(1000, 1000000)
            G.add_edge(from_acc, to_acc, type='TRANSACTION',
                      amount=amount,
                      currency='INR',
                      timestamp=(datetime.now() - timedelta(days=random.randint(1, 90))).isoformat())
    
    for _ in range(25):
        person = random.choice(persons)
        location = random.choice(locations)
        G.add_edge(person, location, type='VISITED',
                  timestamp=(datetime.now() - timedelta(days=random.randint(1, 120))).isoformat())
    
    for _ in range(12):
        person = random.choice(persons)
        case = random.choice(cases)
        try:
            if not G.has_edge(person, case):
                G.add_edge(person, case, type='INVOLVED', confidence=0.5 + random.random()*0.4,
                          timestamp=(datetime.now() - timedelta(days=random.randint(1, 60))).isoformat())
        except:
            G.add_edge(person, case, type='INVOLVED', confidence=0.5 + random.random()*0.4,
                      timestamp=(datetime.now() - timedelta(days=random.randint(1, 60))).isoformat())
    
    hidden_pairs = [
        ('P-0001', 'P-0015'), ('PH-0003', 'PH-0018'), ('ACC-0002', 'ACC-0012'),
        ('P-0008', 'P-0025'), ('PH-0007', 'PH-0014'), ('ACC-0005', 'ACC-0015')
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
        'priority_score': random.uniform(0.3, 0.9)
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
    
    @keyframes typing {
        from { width: 0; }
        to { width: 100%; }
    }
    
    @keyframes blink {
        0%, 100% { border-color: transparent; }
        50% { border-color: #667eea; }
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
    
    .hero-section::after {
        content: '🕵️';
        position: absolute;
        right: 2rem;
        bottom: 1rem;
        font-size: 6rem;
        opacity: 0.1;
        animation: float 6s ease-in-out infinite;
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
    
    .metric-card::before {
        content: '';
        position: absolute;
        top: -50%;
        right: -50%;
        width: 100%;
        height: 100%;
        background: radial-gradient(circle, rgba(102,126,234,0.05) 0%, transparent 70%);
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
        color: #1a1a2e;
        animation: bounceIn 0.8s ease-out;
    }
    
    .metric-card .label {
        font-size: 0.9rem;
        color: #666;
        font-weight: 500;
    }
    
    .metric-card .trend {
        font-size: 0.8rem;
        color: #2ed573;
        margin-top: 0.3rem;
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
    
    /* ===== EMERGENCY BUTTON ===== */
    .emergency-btn {
        background: linear-gradient(135deg, #ff4757, #ff6b6b);
        color: white;
        border: none;
        padding: 12px 30px;
        border-radius: 50px;
        font-size: 1.1rem;
        font-weight: 700;
        animation: pulseGlow 1.5s infinite;
        cursor: pointer;
        transition: all 0.3s ease;
        width: 100%;
        box-shadow: 0 4px 20px rgba(255, 71, 87, 0.4);
    }
    
    .emergency-btn:hover {
        transform: scale(1.05);
        box-shadow: 0 8px 40px rgba(255, 71, 87, 0.6);
    }
    
    /* ===== BUTTONS ===== */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-weight: 600;
        border: none;
        padding: 0.6rem 2rem;
        border-radius: 50px;
        transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        animation: glow 3s infinite;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px) scale(1.02);
        box-shadow: 0 8px 30px rgba(102, 126, 234, 0.5);
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
    
    /* ===== LANGUAGE SELECTOR ===== */
    .lang-selector {
        background: white;
        padding: 0.5rem;
        border-radius: 12px;
        border: 1px solid #e0e0e0;
        transition: all 0.3s ease;
    }
    
    .lang-selector:hover {
        border-color: #667eea;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
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
    
    /* ===== TYPING EFFECT ===== */
    .typing-text {
        overflow: hidden;
        white-space: nowrap;
        border-right: 3px solid #667eea;
        animation: typing 2s steps(30) 1s forwards, blink 0.8s step-end infinite;
        width: 0;
        display: inline-block;
    }
    
    /* ===== SCROLL ANIMATION ===== */
    .scroll-reveal {
        opacity: 0;
        animation: fadeInUp 0.8s ease-out forwards;
    }
    
    .scroll-reveal:nth-child(1) { animation-delay: 0.1s; }
    .scroll-reveal:nth-child(2) { animation-delay: 0.3s; }
    .scroll-reveal:nth-child(3) { animation-delay: 0.5s; }
    .scroll-reveal:nth-child(4) { animation-delay: 0.7s; }
    
    /* ===== HOVER GLOW ===== */
    .hover-glow {
        transition: all 0.3s ease;
    }
    
    .hover-glow:hover {
        filter: drop-shadow(0 0 20px rgba(102, 126, 234, 0.3));
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
        <div style="font-size: 0.7rem; color: #888; margin-top: -3px;">
            Smart Unified Threat & Relationship Analytics
        </div>
        <div style="margin-top: 8px;">
            <span class="sih-badge" style="font-size: 0.7rem; padding: 4px 12px;">🏆 SIH 2026</span>
        </div>
        <div style="font-size: 0.6rem; color: #999; margin-top: 4px;">
            AI-Powered Criminal Network Analysis
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
    
    # Navigation
    st.markdown("### 📌 Navigation")
    
    nav_items = {
        "nav_dashboard": "📊",
        "nav_graph": "🌐",
        "nav_entity": "👤",
        "nav_timeline": "⏱️",
        "nav_crosscase": "🔗",
        "nav_ai": "🤖",
        "nav_alerts": "🔔",
        "nav_simulation": "🎯"
    }
    
    for key, icon in nav_items.items():
        label = get_text(key)
        if st.button(f"{icon} {label}", key=f"nav_{key}", use_container_width=True):
            st.session_state.current_page = label
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
            st.success(f"✅ {get_text('success')}")
            st.rerun()
    
    st.markdown("---")
    
    # Status
    if st.session_state.data_loaded:
        st.success(f"✅ {get_text('data_loaded')}")
        st.caption(f"Entities: {len(st.session_state.entity_list)}")
    else:
        st.info(f"⏳ {get_text('no_data_loaded')}")
    
    st.markdown("---")
    st.caption(f"{get_text('version')} | Made with ❤️")

# ============================================================================
# HERO SECTION (Top Center)
# ============================================================================

st.markdown("""
<div class="hero-section">
    <div class="hero-badges">
        <span class="sih-badge-hero">🏆 SIH 2026</span>
        <span class="ps-badge-hero">AI-Powered Criminal Network Analysis</span>
        <span class="version-badge-hero">v2.0.0</span>
    </div>
    <div class="hero-title">🕵️ SUTRA-X</div>
    <div class="hero-subtitle">Smart Unified Threat & Relationship Analytics</div>
    <div style="margin-top: 0.5rem; color: rgba(255,255,255,0.4); font-size: 0.8rem;">
        From Fragmented Evidence to Actionable Intelligence
    </div>
</div>
""", unsafe_allow_html=True)

# ============================================================================
# MAIN CONTENT
# ============================================================================

if not st.session_state.data_loaded or st.session_state.graph is None:
    st.markdown("""
    <div style="text-align: center; padding: 3rem 1rem; animation: fadeInUp 1s ease-out;">
        <div style="font-size: 4rem; margin-bottom: 1rem; animation: float 3s ease-in-out infinite;">🕵️</div>
        <h2 style="font-size: 2rem; font-weight: 700; color: #1a1a2e;">Welcome to SUTRA-X</h2>
        <p style="color: #666; font-size: 1.1rem; max-width: 600px; margin: 0 auto;">
            AI-powered criminal network analysis platform for investigators
        </p>
        <div style="margin-top: 2rem;">
            <span class="sih-badge" style="font-size: 0.9rem;">🏆 SIH 2026</span>
            <span class="ps-badge" style="font-size: 0.9rem;">AI-Powered Criminal Network Analysis</span>
        </div>
        <div style="margin-top: 2rem; color: #888;">
            👈 Click "Generate Sample Data" in the sidebar to get started
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Feature Cards
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="glow-card" style="text-align: center;">
            <div style="font-size: 3rem; animation: float 4s ease-in-out infinite;">📊</div>
            <h3>Multi-Source Intelligence</h3>
            <p style="color: #666;">Ingest data from FIR, CDR, financial records, vehicles, and locations</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="glow-card" style="text-align: center;">
            <div style="font-size: 3rem; animation: float 4s ease-in-out infinite 0.5s;">🧠</div>
            <h3>AI-Powered Analysis</h3>
            <p style="color: #666;">Entity extraction, relationship discovery, and intelligent prioritization</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="glow-card" style="text-align: center;">
            <div style="font-size: 3rem; animation: float 4s ease-in-out infinite 1s;">🎯</div>
            <h3>Actionable Intelligence</h3>
            <p style="color: #666;">Evidence-backed leads with investigation briefs in 30 seconds</p>
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
            <h1 class="hero-title" style="font-size: 2.5rem; -webkit-text-fill-color: #1a1a2e; background: none; animation: none;">
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
            "🔍 Evidence correlation detected"
        ]
        for activity in activities:
            st.markdown(f"<div style='padding: 0.3rem 0; animation: slideInLeft 0.5s ease-out;'>{activity}</div>", unsafe_allow_html=True)
    
    # ========================================================================
    # NETWORK GRAPH
    # ========================================================================
    elif current_page == get_text("nav_graph"):
        st.markdown(f"""
        <div style="animation: fadeInUp 0.6s ease-out;">
            <h1 class="hero-title" style="font-size: 2.5rem; -webkit-text-fill-color: #1a1a2e; background: none; animation: none;">
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
                _show_fallback_network(G, node_list)
        else:
            st.warning("Showing network data view. Install plotly and networkx for interactive visualization.")
            _show_fallback_network(G, node_list)
        
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
                st.rerun()
    
    # ========================================================================
    # ENTITY PROFILE
    # ========================================================================
    elif current_page == get_text("nav_entity"):
        st.markdown(f"""
        <div style="animation: fadeInUp 0.6s ease-out;">
            <h1 class="hero-title" style="font-size: 2.5rem; -webkit-text-fill-color: #1a1a2e; background: none; animation: none;">
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
    # TIMELINE
    # ========================================================================
    elif current_page == get_text("nav_timeline"):
        st.markdown(f"""
        <div style="animation: fadeInUp 0.6s ease-out;">
            <h1 class="hero-title" style="font-size: 2.5rem; -webkit-text-fill-color: #1a1a2e; background: none; animation: none;">
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
    # CROSS-CASE
    # ========================================================================
    elif current_page == get_text("nav_crosscase"):
        st.markdown(f"""
        <div style="animation: fadeInUp 0.6s ease-out;">
            <h1 class="hero-title" style="font-size: 2.5rem; -webkit-text-fill-color: #1a1a2e; background: none; animation: none;">
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
    # AI ASSISTANT
    # ========================================================================
    elif current_page == get_text("nav_ai"):
        st.markdown(f"""
        <div style="animation: fadeInUp 0.6s ease-out;">
            <h1 class="hero-title" style="font-size: 2.5rem; -webkit-text-fill-color: #1a1a2e; background: none; animation: none;">
                🤖 {get_text('ai_title')}
            </h1>
            <p style="color: #666; margin-top: -0.5rem;">{get_text('ai_sub')}</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.info("💡 " + get_text('ai_sub'))
        
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
                st.session_state.ai_query = user_query
        
        if hasattr(st.session_state, 'ai_query') and st.session_state.ai_query:
            query = st.session_state.ai_query
            
            st.markdown("---")
            st.markdown(f"### 🤖 {get_text('ai_response')}")
            
            with st.spinner(get_text('loading')):
                response = f"""
                ## 📋 Investigation Brief
                
                ### 🔍 Query Analysis
                I've analyzed your query about **{query[:50]}...**
                
                ### 📊 Key Findings
                1. **Network Overview**: The network contains {len(node_list)} entities
                2. **🔗 Key Connections**: Multiple relationships discovered
                3. **🎯 Priority Entities**: {len([n for n in node_list if get_degree(G, n) >= 3])} entities have high connectivity
                
                ### 💡 Actionable Insights
                - 🎯 **Focus Areas**: Investigate entities with high connectivity first
                - 🔗 **Hidden Connections**: Look for indirect paths between key persons
                - 📊 **Pattern Detection**: Financial and communication patterns are most revealing
                
                ### 📌 Next Steps
                1. Review priority entities in the Dashboard
                2. Explore connections in the Network Graph
                3. Check cross-case connections for broader patterns
                """
                
                st.markdown(response)
                
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
                
                st.session_state.ai_query = None
    
    # ========================================================================
    # ALERTS & EMERGENCY
    # ========================================================================
    elif current_page == get_text("nav_alerts"):
        st.markdown(f"""
        <div style="animation: fadeInUp 0.6s ease-out;">
            <h1 class="hero-title" style="font-size: 2.5rem; -webkit-text-fill-color: #1a1a2e; background: none; animation: none;">
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
                st.rerun()
        
        with col2:
            if st.button("📞 " + get_text('call_now'), use_container_width=True):
                st.success(get_text('call_initiated'))
        
        with col3:
            if st.button("📨 " + get_text('send_alert'), use_container_width=True):
                st.session_state.alert_sent = True
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
                    <div style="margin-top: 0.5rem;">
                        <button style="background: rgba(255,255,255,0.2); border: none; color: white; padding: 4px 16px; border-radius: 50px; cursor: pointer; transition: all 0.3s;">
                            📞 Call Now
                        </button>
                        <button style="background: rgba(255,255,255,0.2); border: none; color: white; padding: 4px 16px; border-radius: 50px; cursor: pointer; margin-left: 0.5rem; transition: all 0.3s;">
                            📨 Send Alert
                        </button>
                    </div>
                    ''' if alert['type'] == 'CRITICAL' else ''}
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info(get_text('no_alerts'))
    
    # ========================================================================
    # SIMULATION
    # ========================================================================
    elif current_page == get_text("nav_simulation"):
        st.markdown(f"""
        <div style="animation: fadeInUp 0.6s ease-out;">
            <h1 class="hero-title" style="font-size: 2.5rem; -webkit-text-fill-color: #1a1a2e; background: none; animation: none;">
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

# ============================================================================
# HELPER FUNCTION FOR FALLBACK
# ============================================================================

def _show_fallback_network(G, node_list):
    st.subheader("📋 Network Data")
    
    st.write("**Entities:**")
    node_data = []
    for node in node_list:
        attrs = get_node_attributes(G, node)
        node_data.append({
            'ID': node,
            'Type': attrs.get('type', 'UNKNOWN'),
            'Degree': get_degree(G, node)
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
# FOOTER
# ============================================================================

st.markdown(f"""
<div class="footer">
    <div style="display: flex; justify-content: center; gap: 20px; flex-wrap: wrap; margin-bottom: 10px;">
        <span>🏆 SIH 2026</span>
        <span>|</span>
        <span>🕵️ SUTRA-X {get_text('version')}</span>
        <span>|</span>
        <span>{get_text('nav_dashboard')}</span>
        <span>|</span>
        <span>🌐 {LANGUAGES[st.session_state.language]['name']}</span>
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
