"""
Streamlit frontend for Medical Diagnosis AI System
"""

import streamlit as st
import requests
import json
from datetime import datetime
from typing import List, Dict, Any
import pandas as pd

# Configuration
API_BASE_URL = "http://localhost:8000"

def main():
    st.set_page_config(
        page_title="Medical Diagnosis AI System",
        page_icon="🏥",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    
    st.title("🏥 Medical Diagnosis AI System")
    st.markdown("### Multi-Agent AI-Powered Medical Diagnosis")
    
    # Sidebar
    with st.sidebar:
        st.header("Navigation")
        page = st.selectbox(
            "Choose a page",
            ["Diagnosis", "Session History", "System Info"]
        )
        
        st.markdown("---")
        st.markdown("### About")
        st.markdown("""
        This system uses multiple AI agents specialized in different medical fields:
        
        - **General Physician**: Primary care and general diagnosis
        - **Cardiology**: Heart and cardiovascular conditions
        - **Radiology**: Medical imaging and diagnostic radiology
        - **Neurology**: Nervous system and brain disorders
        - **Oncology**: Cancer diagnosis and treatment
        - **Pediatrics**: Children's health and development
        - **Psychiatry**: Mental health and behavioral disorders
        """)
        
        st.markdown("---")
        st.markdown("**Disclaimer**: This is an AI-assisted tool and should not replace professional medical evaluation.")
    
    # Page routing
    if page == "Diagnosis":
        diagnosis_page()
    elif page == "Session History":
        session_history_page()
    elif page == "System Info":
        system_info_page()

def diagnosis_page():
    """Main diagnosis page"""
    st.header("🔍 Symptom Diagnosis")
    
    # Check API health
    if not check_api_health():
        st.error("❌ API server is not running. Please start the server first.")
        st.info("Run: `python main.py` to start the server")
        return
    
    # Patient Information
    st.subheader("Patient Information")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        patient_id = st.text_input("Patient ID", value=f"P{datetime.now().strftime('%Y%m%d%H%M%S')}")
        age = st.number_input("Age", min_value=0, max_value=120, value=30)
    
    with col2:
        gender = st.selectbox("Gender", ["Male", "Female", "Other"])
        weight = st.number_input("Weight (kg)", min_value=0.0, max_value=300.0, value=70.0)
    
    with col3:
        height = st.number_input("Height (cm)", min_value=0.0, max_value=250.0, value=170.0)
    
    # Medical History
    st.subheader("Medical History")
    col1, col2 = st.columns(2)
    
    with col1:
        medical_history = st.text_area("Medical History (comma-separated)", 
                                     placeholder="e.g., diabetes, hypertension, asthma")
        allergies = st.text_area("Allergies (comma-separated)", 
                               placeholder="e.g., penicillin, peanuts")
    
    with col2:
        medications = st.text_area("Current Medications (comma-separated)", 
                                 placeholder="e.g., metformin, lisinopril")
        family_history = st.text_area("Family History (comma-separated)", 
                                    placeholder="e.g., heart disease, cancer")
    
    # Intuitive Symptom Input
    st.subheader("Describe What You're Feeling")
    user_symptom_text = st.text_area(
        "Describe your symptoms or what you are feeling in your own words:",
        placeholder="e.g., I have a headache and feel dizzy with chest pain."
    )

    # File Upload
    st.subheader("Upload Files (optional)")
    uploaded_files = st.file_uploader(
        "Upload images and documents (e.g., scans, photos, reports, PDFs)",
        type=["png", "jpg", "jpeg", "pdf", "docx", "txt"],
        accept_multiple_files=True,
        help="Supported formats: Images (PNG, JPG, JPEG), Documents (PDF, DOCX, TXT)"
    )

    # Advanced/Structured Input (optional, hidden by default)
    with st.expander("Advanced: Add Structured Symptoms (optional)"):
        symptoms = []
        num_symptoms = st.number_input("Number of symptoms", min_value=0, max_value=10, value=0, key="adv_num_symptoms")
        for i in range(num_symptoms):
            with st.expander(f"Symptom {i+1}", expanded=True):
                col1, col2 = st.columns(2)
                with col1:
                    name = st.text_input(f"Symptom name {i+1}", 
                                       placeholder="e.g., chest pain, headache", key=f"adv_name_{i}")
                    description = st.text_area(f"Description {i+1}", 
                                             placeholder="Describe the symptom in detail", key=f"adv_desc_{i}")
                    severity = st.selectbox(f"Severity {i+1}", 
                                          ["mild", "moderate", "severe", "critical"], key=f"adv_sev_{i}")
                with col2:
                    duration = st.text_input(f"Duration {i+1}", 
                                           placeholder="e.g., 2 days, 1 week", key=f"adv_dur_{i}")
                    onset = st.text_input(f"Onset {i+1}", 
                                        placeholder="e.g., sudden, gradual", key=f"adv_onset_{i}")
                    triggers = st.text_input(f"Triggers {i+1}", 
                                           placeholder="e.g., exercise, stress", key=f"adv_trig_{i}")
                    alleviating_factors = st.text_input(f"Alleviating factors {i+1}", 
                                                      placeholder="e.g., rest, medication", key=f"adv_allev_{i}")
                if name and description:
                    symptoms.append({
                        "name": name,
                        "description": description,
                        "severity": severity,
                        "duration": duration,
                        "onset": onset,
                        "triggers": [t.strip() for t in triggers.split(",") if t.strip()],
                        "alleviating_factors": [a.strip() for a in alleviating_factors.split(",") if a.strip()]
                    })
    
    # Additional Notes
    additional_notes = st.text_area("Additional Notes", 
                                   placeholder="Any additional information that might be relevant")
    
    # Diagnosis Button
    if st.button("🔍 Get Diagnosis", type="primary", use_container_width=True):
        if user_symptom_text.strip() or symptoms or uploaded_files:
            with st.spinner("Analyzing symptoms and files with multiple specialists..."):
                # If user provided free-text, use it as a single symptom
                if user_symptom_text.strip():
                    symptoms_to_send = [{
                        "name": "User Description",
                        "description": user_symptom_text.strip(),
                        "severity": "moderate",
                        "duration": "unspecified",
                        "onset": "unspecified",
                        "triggers": [],
                        "alleviating_factors": []
                    }]
                else:
                    symptoms_to_send = symptoms
                
                # Separate images and documents from uploaded files
                uploaded_images = []
                uploaded_docs = []
                if uploaded_files:
                    for file in uploaded_files:
                        if file.type.startswith("image/"):
                            uploaded_images.append(file)
                        elif file.type in ["application/pdf", "application/vnd.openxmlformats-officedocument.wordprocessingml.document", "text/plain"]:
                            uploaded_docs.append(file)
                
                result = get_diagnosis(
                    patient_id, age, gender, weight, height,
                    medical_history, allergies, medications, family_history,
                    symptoms_to_send, additional_notes,
                    uploaded_images, uploaded_docs
                )
                if result:
                    display_diagnosis_result(result)
        else:
            st.warning("Please describe what you are feeling, add at least one symptom, or upload a file.")

def display_diagnosis_result(result: Dict[str, Any]):
    """Display diagnosis results"""
    st.success("✅ Diagnosis completed!")
    
    # Urgency level
    urgency = result['diagnosis']['urgency_level']
    if urgency == "emergency":
        st.error("🚨 EMERGENCY: Seek immediate medical attention!")
    elif urgency == "urgent":
        st.warning("⚠️ URGENT: Seek medical attention within 24 hours")
    else:
        st.info("ℹ️ Routine: Schedule appointment with your healthcare provider")
    
    # Message
    st.markdown(f"**Message**: {result['message']}")
    
    # Results in tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "👨‍⚕️ Specialists", "🔬 Tests", "⚡ Actions", "📝 Follow-up"
    ])
    
    with tab1:
        st.subheader("Recommended Specialists")
        specialists = result['diagnosis']['recommended_specialists']
        if specialists:
            for specialist in specialists:
                st.markdown(f"- {specialist.replace('_', ' ').title()}")
        else:
            st.info("No specific specialists recommended")
    
    with tab2:
        st.subheader("Suggested Tests")
        tests = result['diagnosis']['suggested_tests']
        if tests:
            for test in tests:
                st.markdown(f"- {test}")
        else:
            st.info("No specific tests recommended")
    
    with tab3:
        st.subheader("Immediate Actions")
        actions = result['diagnosis']['immediate_actions']
        if actions:
            for action in actions:
                st.markdown(f"- {action}")
        else:
            st.info("No immediate actions required")
    
    with tab4:
        st.subheader("Follow-up Plan")
        st.markdown(result['diagnosis']['follow_up_plan'])
        
        st.markdown("---")
        st.markdown("**Disclaimers**:")
        for disclaimer in result['diagnosis']['disclaimers']:
            st.markdown(f"- {disclaimer}")

def session_history_page():
    """Session history page"""
    st.header("📚 Session History")
    
    if not check_api_health():
        st.error("❌ API server is not running.")
        return
    
    # Get sessions
    try:
        response = requests.get(f"{API_BASE_URL}/sessions")
        if response.status_code == 200:
            sessions_data = response.json()
            sessions = sessions_data['sessions']
            
            if sessions:
                # Convert to DataFrame for better display
                df = pd.DataFrame(sessions)
                df['start_time'] = pd.to_datetime(df['start_time'])
                df['end_time'] = pd.to_datetime(df['end_time'])
                
                st.dataframe(df, use_container_width=True)
                
                # Session details
                selected_session = st.selectbox(
                    "Select session for details",
                    sessions,
                    format_func=lambda x: f"{x['session_id'][:8]} - {x['patient_id']} - {x['start_time']}"
                )
                
                if selected_session:
                    display_session_details(selected_session['session_id'])
            else:
                st.info("No sessions found")
        else:
            st.error("Failed to fetch sessions")
    except Exception as e:
        st.error(f"Error fetching sessions: {str(e)}")

def display_session_details(session_id: str):
    """Display detailed session information"""
    try:
        response = requests.get(f"{API_BASE_URL}/sessions/{session_id}")
        if response.status_code == 200:
            session = response.json()
            
            st.subheader(f"Session Details: {session_id[:8]}")
            
            # Basic info
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Patient ID", session['patient_id'])
            with col2:
                st.metric("Status", session['status'])
            with col3:
                st.metric("Duration", 
                         f"{(session['end_time'] - session['start_time']).total_seconds():.1f}s" 
                         if session['end_time'] else "N/A")
            
            # Agent responses
            if session['agent_responses']:
                st.subheader("Specialist Analyses")
                for resp in session['agent_responses']:
                    with st.expander(f"{resp['specialty'].replace('_', ' ').title()} Analysis"):
                        st.markdown(f"**Agent ID**: {resp['agent_id']}")
                        st.markdown(f"**Confidence**: {resp['confidence']:.2%}")
                        st.markdown("**Analysis**:")
                        st.markdown(resp['analysis'])
                        st.markdown("**Recommendations**:")
                        for rec in resp['recommendations']:
                            st.markdown(f"- {rec}")
            
            # Final diagnosis
            if session['final_diagnosis']:
                st.subheader("Final Diagnosis")
                diagnosis = session['final_diagnosis']
                st.json(diagnosis)
        else:
            st.error("Failed to fetch session details")
    except Exception as e:
        st.error(f"Error fetching session details: {str(e)}")

def system_info_page():
    """System information page"""
    st.header("ℹ️ System Information")
    
    if not check_api_health():
        st.error("❌ API server is not running.")
        return
    
    # Health check
    try:
        response = requests.get(f"{API_BASE_URL}/health")
        if response.status_code == 200:
            health = response.json()
            st.success("✅ System is healthy")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Agents Loaded", health['agents_loaded'])
            with col2:
                st.metric("Active Sessions", health['active_sessions'])
            with col3:
                st.metric("Status", health['status'])
        else:
            st.error("❌ System health check failed")
    except Exception as e:
        st.error(f"Error checking system health: {str(e)}")
    
    # Available agents
    try:
        response = requests.get(f"{API_BASE_URL}/agents")
        if response.status_code == 200:
            agents_data = response.json()
            agents = agents_data['agents']
            
            st.subheader("Available Medical Specialists")
            
            for agent in agents:
                with st.expander(f"{agent['name']} ({agent['specialty'].replace('_', ' ').title()})"):
                    st.markdown(f"**Agent ID**: {agent['agent_id']}")
                    st.markdown(f"**Description**: {agent['description']}")
                    st.markdown("**Expertise Areas**:")
                    for expertise in agent['expertise']:
                        st.markdown(f"- {expertise}")
        else:
            st.error("Failed to fetch agents")
    except Exception as e:
        st.error(f"Error fetching agents: {str(e)}")
    
    # API documentation
    st.subheader("API Documentation")
    st.markdown(f"API documentation is available at: [{API_BASE_URL}/docs]({API_BASE_URL}/docs)")

def check_api_health() -> bool:
    """Check if the API server is running"""
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=5)
        return response.status_code == 200
    except:
        return False

def get_diagnosis(patient_id: str, age: int, gender: str, weight: float, height: float,
                 medical_history: str, allergies: str, medications: str, family_history: str,
                 symptoms: List[Dict], additional_notes: str,
                 uploaded_images=None, uploaded_docs=None) -> Dict[str, Any]:
    """Send diagnosis request to API, including files if present"""
    try:
        # Prepare request data
        request_data = {
            "patient_info": {
                "patient_id": patient_id,
                "age": age,
                "gender": gender,
                "weight": weight,
                "height": height,
                "medical_history": [h.strip() for h in medical_history.split(",") if h.strip()],
                "allergies": [a.strip() for a in allergies.split(",") if a.strip()],
                "medications": [m.strip() for m in medications.split(",") if m.strip()],
                "family_history": [f.strip() for f in family_history.split(",") if f.strip()]
            },
            "symptoms": symptoms,
            "additional_notes": additional_notes
        }
        files = {}
        # Attach images
        if uploaded_images:
            for idx, img in enumerate(uploaded_images):
                files[f"image_{idx}"] = (img.name, img, img.type)
        # Attach documents
        if uploaded_docs:
            for idx, doc in enumerate(uploaded_docs):
                files[f"document_{idx}"] = (doc.name, doc, doc.type)
        if files:
            # Send as multipart/form-data
            response = requests.post(
                f"{API_BASE_URL}/diagnose",
                data={"json": json.dumps(request_data)},
                files=files,
                timeout=120
            )
        else:
            # Send as JSON
            response = requests.post(
                f"{API_BASE_URL}/diagnose",
                json=request_data,
                timeout=120
            )
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"API Error: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        st.error(f"Error sending diagnosis request: {str(e)}")
        return None

if __name__ == "__main__":
    main() 