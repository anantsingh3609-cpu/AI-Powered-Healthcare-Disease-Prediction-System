import os
import streamlit as st
import datetime
from data import DISEASES_DB, ALL_SYMPTOMS
import model

# Page configuration
st.set_page_config(
    page_title="AI Healthcare Diagnosis Assistant",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load CSS custom styling
css_path = os.path.join(os.path.dirname(__file__), "styles.css")
if os.path.exists(css_path):
    with open(css_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Initialize Session State
if "history" not in st.session_state:
    st.session_state.history = []
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        {
            "role": "assistant", 
            "content": "Hello! I am your AI Health Advisor. You can ask me general questions about health, wellness, symptoms, or how to manage simple conditions.\n\n*Please remember, I cannot diagnose medical conditions in chat—use the **Symptom Checker** tab to run a structured diagnostic check!*"
        }
    ]
if "diagnosis_result" not in st.session_state:
    st.session_state.diagnosis_result = None
if "ai_summary" not in st.session_state:
    st.session_state.ai_summary = None
if "reported_symptoms_cache" not in st.session_state:
    st.session_state.reported_symptoms_cache = []

# Main Header
st.markdown("""
<div class="header-container">
    <h1 style='margin:0; font-weight: 700; font-size: 2.2rem;'>🏥 CareAI</h1>
    <p style='margin:5px 0 0 0; font-weight: 300; font-size: 1.1rem; opacity: 0.9;'>AI-Powered Healthcare Diagnostic & Wellness Assistant</p>
</div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("### 👤 Patient Profile")
    age = st.number_input("Age", min_value=0, max_value=120, value=30, step=1)
    gender = st.selectbox("Biological Sex", ["Female", "Male", "Other"])
    conditions = st.text_input("Existing Medical Conditions (e.g. Asthma, Diabetes)", placeholder="None")
    
    st.markdown("---")
    
    st.markdown("### ⚙️ Settings")
    api_key = st.text_input(
        "Gemini API Key (Optional)", 
        type="password", 
        help="Enter your Google Gemini API key to unlock advanced patient-tailored AI reports and conversational chat."
    )
    
    st.markdown("---")
    
    # Emergency Warning Block
    st.markdown("""
    <div class="emergency-banner">
        <div class="emergency-title">⚠️ EMERGENCY NOTICE</div>
        <div class="emergency-text">
            If you are experiencing a medical emergency, such as severe chest pain, shortness of breath, sudden numbness, or severe bleeding, please call <b>911</b> or go to the nearest emergency room immediately.
            <br><br>
            <i>This AI tool is for educational purposes and is not a substitute for professional medical advice.</i>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Main Application Tabs
tab1, tab2, tab3, tab4 = st.tabs([
    "📋 Symptom Checker", 
    "💬 AI Health Advisor (Chat)", 
    "📜 Assessment History", 
    "ℹ️ How It Works"
])

# Tab 1: Symptom Checker
with tab1:
    col1, col2 = st.columns([1, 1.2], gap="large")
    
    with col1:
        st.markdown("### 🔍 Report Symptoms")
        st.write("Select symptoms from the clinical checklist or describe how you feel in your own words.")
        
        # 1. Multi-select list of symptoms
        selected_symptoms = st.multiselect(
            "Select specific symptoms from the list:",
            options=ALL_SYMPTOMS,
            help="Select one or more symptoms that match what you are feeling."
        )
        
        # 2. Free text description
        user_text = st.text_area(
            "Or describe how you feel in your own words:",
            placeholder="e.g. 'I woke up with a dry cough, mild fever, and a sore throat. I also feel quite tired.'",
            height=120,
            help="Our matching engine will extract symptoms from your text description."
        )
        
        run_btn = st.button("🚀 Analyze Symptoms", use_container_width=True)
        
        if run_btn:
            if not selected_symptoms and not user_text.strip():
                st.warning("⚠️ Please select at least one symptom or describe your condition in the text area.")
            else:
                with st.spinner("Analyzing symptoms and matching with clinical database..."):
                    # Run matching engine
                    results = model.diagnose_symptoms(selected_symptoms, user_text)
                    st.session_state.diagnosis_result = results
                    
                    # Combine selected symptoms with extracted symptoms for record keeping
                    extracted = model.extract_symptoms_from_text(user_text)
                    all_reported = list(set(selected_symptoms + extracted))
                    st.session_state.reported_symptoms_cache = all_reported
                    
                    # Generate diagnosis summary (Gemini or Fallback)
                    patient_profile = {
                        "age": age,
                        "gender": gender,
                        "conditions": conditions
                    }
                    
                    st.session_state.ai_summary = model.generate_ai_summary(
                        patient_profile,
                        all_reported,
                        results,
                        api_key=api_key
                    )
                    
                    # Save to History Log
                    if results:
                        st.session_state.history.append({
                            "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
                            "reported_symptoms": all_reported,
                            "top_match": results[0]["name"],
                            "severity": results[0]["severity"],
                            "summary": st.session_state.ai_summary
                        })
    
    with col2:
        st.markdown("### 📊 Diagnostic Analysis")
        
        if st.session_state.diagnosis_result is None:
            st.info("← Enter symptoms on the left and click **Analyze Symptoms** to generate your report.")
        elif not st.session_state.diagnosis_result:
            st.error("No clinical matches found for the reported symptoms. Please try clarifying your symptoms or seek a general practitioner's advice.")
        else:
            results = st.session_state.diagnosis_result
            primary = results[0]
            
            # Severity color class mapping
            sev_class = "severity-low"
            if primary["severity"].lower() == "medium":
                sev_class = "severity-medium"
            elif primary["severity"].lower() == "high":
                sev_class = "severity-high"
                
            st.markdown(f"""
            <div class="diagnostic-card">
                <span class="match-score-pill">Match Score: {primary['score']}%</span>
                <span class="severity-badge {sev_class}">{primary['severity']} Urgency</span>
                <h3 style="margin-top: 10px; margin-bottom: 5px; font-weight: 600; color: white;">Primary Match: {primary['name']}</h3>
                <p style="color: #aaaaaa; font-size: 0.9rem; margin-bottom: 15px;">Category: {primary['category']}</p>
                <p style="line-height: 1.6; font-size: 0.95rem; color: #e0e0e0;">{primary['description']}</p>
                <hr style="opacity: 0.15; margin: 15px 0;">
                <p style="font-size: 0.9rem; color: #f0f0f0;">🩺 <b>Recommended Specialist</b>: {primary['specialty']}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Show matching symptoms tags
            st.markdown("**Symptom Matches:**")
            symptom_tags_html = ""
            for sym in primary["matched_symptoms"]:
                symptom_tags_html += f'<span class="symptom-tag symptom-tag-match">✓ {sym}</span>'
            for sym in primary["missing_symptoms"]:
                symptom_tags_html += f'<span class="symptom-tag symptom-tag-missing">? {sym}</span>'
            st.markdown(f'<div>{symptom_tags_html}</div>', unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Show other potential matches if any
            if len(results) > 1:
                with st.expander(f"➕ Other Potential Matches ({len(results)-1})"):
                    for alt in results[1:4]:
                        alt_sev_class = "severity-low"
                        if alt["severity"].lower() == "medium":
                            alt_sev_class = "severity-medium"
                        elif alt["severity"].lower() == "high":
                            alt_sev_class = "severity-high"
                            
                        st.markdown(f"""
                        <div style="padding: 12px; border-bottom: 1px solid rgba(255,255,255,0.05); margin-bottom: 10px;">
                            <span style="float: right; font-weight: 500; font-size: 0.85rem; color: #888888;">{alt['score']}% match</span>
                            <span class="severity-badge {alt_sev_class}" style="padding: 2px 8px; font-size: 0.75rem; margin-bottom: 5px;">{alt['severity']}</span>
                            <h4 style="margin: 0 0 5px 0; font-size: 1rem; font-weight: 600; color: white;">{alt['name']}</h4>
                            <p style="margin: 0; font-size: 0.85rem; line-height: 1.4; color: #cccccc;">{alt['description']}</p>
                        </div>
                        """, unsafe_allow_html=True)
            
            st.markdown("---")
            st.markdown("### 🤖 Clinical AI Summary & Care Plan")
            st.markdown(st.session_state.ai_summary)

# Tab 2: Chat Advisor
with tab2:
    st.markdown("### 💬 Chat with AI Health Advisor")
    st.write("Ask follow-up questions, get wellness tips, or request clarifications on symptoms or terminology.")
    
    # Display chat history
    for msg in st.session_state.chat_history:
        if msg["role"] == "user":
            with st.chat_message("user", avatar="👤"):
                st.write(msg["content"])
        else:
            with st.chat_message("assistant", avatar="🤖"):
                st.write(msg["content"])
                
    # Chat Input
    if chat_input := st.chat_input("Ask a medical or wellness question..."):
        # Display user message
        with st.chat_message("user", avatar="👤"):
            st.write(chat_input)
            
        # Append user message
        st.session_state.chat_history.append({"role": "user", "content": chat_input})
        
        # Display response
        with st.chat_message("assistant", avatar="🤖"):
            with st.spinner("AI is thinking..."):
                response = model.generate_chat_response(
                    chat_input,
                    st.session_state.chat_history[:-1],
                    api_key=api_key
                )
                st.write(response)
                
        # Append response
        st.session_state.chat_history.append({"role": "assistant", "content": response})

# Tab 3: Assessment History
with tab3:
    st.markdown("### 📜 Assessment History Log")
    st.write("Review all diagnostic assessments logged during this browser session.")
    
    if not st.session_state.history:
        st.info("No assessments have been recorded yet. Complete an analysis in the **Symptom Checker** tab to log a report.")
    else:
        col1, col2 = st.columns([1, 4])
        with col1:
            if st.button("🧹 Clear History Log", use_container_width=True):
                st.session_state.history = []
                st.rerun()
                
        st.markdown("<br>", unsafe_allow_html=True)
        for idx, record in enumerate(reversed(st.session_state.history)):
            reported_syms = ", ".join(record["reported_symptoms"])
            with st.expander(f"📋 {record['timestamp']} - Primary Match: {record['top_match']} ({record['severity']} Urgency)"):
                st.markdown(f"**Reported Symptoms**: `{reported_syms}`")
                st.markdown("---")
                st.markdown(record["summary"])

# Tab 4: How It Works
with tab4:
    st.markdown("### ℹ️ Under the Hood: Clinical Reasoning Engine")
    st.write("This application combines deterministic expert system classification with generative AI synthesis:")
    
    st.markdown("""
    1. **Structured Matching**: When you select symptoms from the list, the engine calculates a weighted similarity score (prioritizing recall/sensitivity) against a curated database of 15+ common clinical conditions.
    2. **Fuzzy Text Extraction**: If you describe your feelings in the text box, our system parses your description and automatically extracts matching clinical symptoms, adding them to the analysis.
    3. **LLM Synthesis (Google Gemini)**: If a Gemini API key is provided, the local diagnosis results are sent to `gemini-2.5-flash` to construct a natural, empathetic, and comprehensive wellness and triage report customized to the patient's profile (age, biological sex, chronic conditions).
    """)
    
    st.info("🔒 **Privacy Note**: Your medical inputs, profiles, and API keys are processed in real-time and are not saved permanently or shared with third parties, except for processing via Google Gemini if the API key is used.")
