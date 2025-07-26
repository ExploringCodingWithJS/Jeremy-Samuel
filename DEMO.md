# Demo Guide

## 🏥 Medical Diagnosis AI System Demo

This guide provides comprehensive information about demonstrating the Medical Diagnosis AI System.

## 🎯 Demo Overview

The Medical Diagnosis AI System is a multi-agent AI platform that provides comprehensive medical symptom analysis using specialized AI agents for different medical fields. The system demonstrates advanced AI coordination, empathetic patient communication, and intelligent medical routing.

## 🚀 Quick Demo Setup

### Prerequisites
- Python 3.8+
- Google API Key (Gemini)
- Internet connection

### Setup Steps
1. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure environment**
   ```bash
   cp env.example .env
   # Edit .env and add your Google API key
   ```

3. **Test the system**
   ```bash
   python test_system.py
   ```

4. **Start the system**
   ```bash
   # Terminal 1: Start API server
   python main.py
   
   # Terminal 2: Start web interface
   streamlit run streamlit_app.py
   ```

## 🎬 Demo Scenarios

### Scenario 1: Cardiac Symptoms (Emergency Detection)
**Patient**: 55-year-old male with chest pain
**Symptoms**: 
- Sharp chest pain (moderate severity, 2 hours duration)
- Shortness of breath (mild severity, 1 hour duration)
- Pain triggered by exercise

**Expected Behavior**:
- Cardiology agent flags as potential emergency
- System recommends immediate medical attention
- General physician provides comprehensive assessment
- Radiology agent suggests imaging studies

### Scenario 2: Pediatric Case (Age-Appropriate Care)
**Patient**: 8-year-old child with behavioral issues
**Symptoms**:
- Difficulty concentrating in school
- Behavioral problems at home
- Sleep disturbances

**Expected Behavior**:
- Pediatrics agent automatically included
- Psychiatry agent provides mental health assessment
- Age-appropriate recommendations
- Developmental milestone considerations

### Scenario 3: Complex Multi-System Symptoms
**Patient**: 40-year-old female with multiple symptoms
**Symptoms**:
- Headache (neurological)
- Anxiety (psychiatric)
- Fatigue (general)
- Weight loss (general/oncology)

**Expected Behavior**:
- Multiple specialists consulted
- Coordinated analysis from all relevant agents
- Prioritized recommendations
- Comprehensive follow-up plan

## 🎭 Demo Flow

### 1. System Introduction (2 minutes)
- **Show the web interface**: http://localhost:8501
- **Highlight key features**:
  - Multi-specialist AI agents
  - Real-time diagnosis
  - Emergency detection
  - Session management

### 2. Live Diagnosis Demo (3 minutes)
- **Enter patient information**:
  - Age, gender, medical history
  - Current medications, allergies
- **Add symptoms**:
  - Describe symptoms in detail
  - Specify severity and duration
- **Run diagnosis**:
  - Show real-time processing
  - Display results from multiple specialists
  - Highlight emergency detection

### 3. Technical Deep Dive (2 minutes)
- **Show API documentation**: http://localhost:8000/docs
- **Demonstrate agent coordination**:
  - Explain routing logic
  - Show concurrent processing
  - Highlight result synthesis
- **Review session history**:
  - Show consultation tracking
  - Display agent responses

### 4. System Architecture (1 minute)
- **Explain the architecture**:
  - Frontend (Streamlit)
  - Backend (FastAPI)
  - Coordinator (Orchestrator)
  - Medical Agents (7 specialists)
  - Google ADK integration

## 🎪 Key Demo Features to Highlight

### 1. Multi-Agent Coordination
- **Concurrent Processing**: Multiple specialists analyze simultaneously
- **Intelligent Routing**: Symptoms automatically routed to relevant specialists
- **Result Synthesis**: Coordinated analysis from all agents

### 2. Emergency Detection
- **Real-time Flagging**: Urgent conditions identified immediately
- **Priority Handling**: Emergency recommendations prioritized
- **Safety Protocols**: Clear emergency guidance

### 3. Empathetic Communication
- **Patient-Friendly Language**: Clear, understandable explanations
- **Comprehensive Results**: Detailed analysis and recommendations
- **Follow-up Planning**: Structured next steps

### 4. Technical Excellence
- **Modern Architecture**: FastAPI + Streamlit + Google ADK
- **Scalable Design**: Easy to add new specialists
- **Robust Error Handling**: Graceful degradation
- **Comprehensive Logging**: Full observability

## 🛠️ Demo Preparation Checklist

- [ ] **Environment Setup**
  - [ ] Dependencies installed
  - [ ] Google API key configured
  - [ ] System tested with `python test_system.py`

- [ ] **System Startup**
  - [ ] API server running on port 8000
  - [ ] Web interface running on port 8501
  - [ ] Health check passing

- [ ] **Demo Data Prepared**
  - [ ] Sample patient scenarios ready
  - [ ] Expected outcomes documented
  - [ ] Backup scenarios available

- [ ] **Technical Verification**
  - [ ] All agents loading correctly
  - [ ] API endpoints responding
  - [ ] Error handling working

## 🎯 Demo Script

### Opening (30 seconds)
"Welcome to the Medical Diagnosis AI System. This is a multi-agent AI platform that provides comprehensive medical symptom analysis using specialized AI agents for different medical fields. The system demonstrates how AI can coordinate multiple specialists to provide empathetic, evidence-based medical guidance."

### Live Demo (3 minutes)
"Let me show you how the system works. I'll enter a patient with chest pain symptoms and demonstrate the multi-agent analysis process..."

### Technical Highlights (2 minutes)
"Behind the scenes, the system uses a sophisticated architecture. The coordinator routes symptoms to relevant specialists, who analyze the case concurrently using Google's Gemini AI. Results are synthesized and prioritized based on urgency and confidence levels."

### Closing (30 seconds)
"This system demonstrates the potential of AI to enhance healthcare by providing comprehensive, coordinated analysis while maintaining appropriate medical disclaimers and safety protocols."

## 🚨 Demo Troubleshooting

### Common Issues
1. **API Key Error**: Ensure Google API key is properly set in `.env`
2. **Port Conflicts**: Check that ports 8000 and 8501 are available
3. **Import Errors**: Run `python test_system.py` to verify setup
4. **Slow Responses**: Normal for AI model calls, explain this is expected

### Backup Plans
- **Offline Demo**: Use pre-recorded session data
- **API Documentation**: Show the comprehensive API docs
- **Architecture Walkthrough**: Explain the system design
- **Code Review**: Walk through key components

## 📊 Demo Metrics

### Success Indicators
- **System Response**: All agents load and respond correctly
- **User Experience**: Intuitive interface and clear results
- **Technical Quality**: Robust error handling and logging
- **Medical Safety**: Appropriate disclaimers and emergency detection

### Key Messages
- **Innovation**: Multi-agent AI coordination for healthcare
- **Safety**: Comprehensive medical disclaimers and emergency protocols
- **Empathy**: Patient-friendly communication and guidance
- **Scalability**: Easy to extend with new medical specialists

## 🎬 Video Demo Structure

### Recommended Timeline
1. **Introduction** (0:00-0:30): System overview and purpose
2. **Live Demo** (0:30-3:30): Complete diagnosis workflow
3. **Technical Deep Dive** (3:30-5:30): Architecture and implementation
4. **Results & Impact** (5:30-6:00): Key benefits and future potential

### Key Moments to Capture
- **Multi-agent coordination**: Show multiple specialists analyzing
- **Emergency detection**: Demonstrate urgent condition flagging
- **User interface**: Highlight intuitive design and comprehensive results
- **Technical architecture**: Explain the sophisticated backend coordination

---

**🎯 Ready to demonstrate the future of AI-powered medical diagnosis!** 
