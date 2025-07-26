# 🏥 Medical Diagnosis AI System

A comprehensive multi-agent AI system for medical diagnosis and patient care, built with Google ADK and specialized medical agents.

## 🌟 Features

- **Multi-Specialist AI Agents**: 7 specialized medical agents covering different areas
- **Intelligent Symptom Analysis**: Automatic routing to relevant specialists
- **Emergency Detection**: Real-time identification of urgent medical conditions
- **Comprehensive Diagnosis**: Coordinated analysis from multiple specialists
- **Empathetic Communication**: Patient-friendly explanations and recommendations
- **Session Management**: Complete consultation history and tracking
- **Modern Web Interface**: Beautiful Streamlit frontend with real-time updates

## 🏥 Medical Specialists

| Specialist | Focus Area | Key Capabilities |
|------------|------------|------------------|
| **General Physician** | Primary care & general diagnosis | Comprehensive health assessment, preventive care |
| **Cardiologist** | Heart & cardiovascular system | Cardiac conditions, emergency cardiac detection |
| **Radiologist** | Medical imaging & diagnostics | Imaging recommendations, radiation safety |
| **Neurologist** | Nervous system & brain | Neurological disorders, stroke detection |
| **Oncologist** | Cancer diagnosis & treatment | Cancer screening, tumor assessment |
| **Pediatrician** | Children's health & development | Age-appropriate care, developmental milestones |
| **Psychiatrist** | Mental health & behavioral disorders | Psychiatric evaluation, safety assessment |

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Google API Key (Gemini)
- Internet connection

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd medical-diagnosis-ai
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment**
   ```bash
   cp env.example .env
   # Edit .env and add your Google API key
   ```

4. **Get Google API Key**
   - Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Create a new API key
   - Add it to your `.env` file

### Running the System

1. **Start the API server**
   ```bash
   python main.py
   ```
   The API will be available at `http://localhost:8000`

2. **Start the web interface**
   ```bash
   streamlit run streamlit_app.py
   ```
   The web interface will be available at `http://localhost:8501`

3. **Access the system**
   - Web Interface: http://localhost:8501
   - API Documentation: http://localhost:8000/docs
   - Health Check: http://localhost:8000/health

## 📋 Usage

### Web Interface

1. **Navigate to the Diagnosis page**
2. **Enter patient information**:
   - Basic demographics (age, gender, weight, height)
   - Medical history, allergies, medications
   - Family history

3. **Add symptoms**:
   - Describe each symptom in detail
   - Specify severity, duration, onset
   - Add triggers and alleviating factors

4. **Get diagnosis**:
   - Click "Get Diagnosis" to analyze symptoms
   - Review results from multiple specialists
   - Follow recommended actions and follow-up plan

### API Usage

```python
import requests

# Example diagnosis request
request_data = {
    "patient_info": {
        "patient_id": "P12345",
        "age": 35,
        "gender": "Male",
        "weight": 75.0,
        "height": 175.0,
        "medical_history": ["hypertension"],
        "allergies": ["penicillin"],
        "medications": ["lisinopril"],
        "family_history": ["heart disease"]
    },
    "symptoms": [
        {
            "name": "chest pain",
            "description": "Sharp pain in center of chest",
            "severity": "moderate",
            "duration": "2 hours",
            "onset": "sudden",
            "triggers": ["exercise"],
            "alleviating_factors": ["rest"]
        }
    ],
    "additional_notes": "Pain started during morning jog"
}

response = requests.post("http://localhost:8000/diagnose", json=request_data)
diagnosis = response.json()
```

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Streamlit     │    │   FastAPI       │    │   Coordinator   │
│   Frontend      │◄──►│   Backend       │◄──►│   (Orchestrator)│
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │                       │
                                ▼                       ▼
                       ┌─────────────────┐    ┌─────────────────┐
                       │   Google ADK    │    │   Medical       │
                       │   (Gemini)      │    │   Agents        │
                       └─────────────────┘    └─────────────────┘
                                                       │
                                                       ▼
                                              ┌─────────────────┐
                                              │   Specialists   │
                                              │   (7 Agents)    │
                                              └─────────────────┘
```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `GOOGLE_API_KEY` | Google Gemini API key | Required |
| `PRIMARY_MODEL` | AI model to use | `gemini-pro` |
| `TEMPERATURE` | AI creativity level | `0.3` |
| `API_HOST` | API server host | `0.0.0.0` |
| `API_PORT` | API server port | `8000` |
| `LOG_LEVEL` | Logging level | `INFO` |

### Agent Configuration

Each medical specialist agent can be configured in `src/config.py`:

```python
MEDICAL_SPECIALTIES = {
    "cardiology": {
        "name": "Cardiologist",
        "description": "Heart and cardiovascular system specialist",
        "expertise": ["cardiology", "heart disease", "cardiovascular health"],
        "model": "gemini-pro",
        "temperature": 0.2
    }
    # ... other specialists
}
```

## 🧪 Testing

### Run Tests

```bash
# Test imports
python -c "import src; print('All imports successful')"

# Test API endpoints
curl http://localhost:8000/health

# Test diagnosis endpoint
curl -X POST http://localhost:8000/diagnose \
  -H "Content-Type: application/json" \
  -d @test_request.json
```

### Example Test Request

```json
{
  "patient_info": {
    "patient_id": "TEST001",
    "age": 45,
    "gender": "Female",
    "medical_history": [],
    "allergies": [],
    "medications": [],
    "family_history": []
  },
  "symptoms": [
    {
      "name": "headache",
      "description": "Dull pain in temples",
      "severity": "mild",
      "duration": "1 day",
      "onset": "gradual",
      "triggers": [],
      "alleviating_factors": []
    }
  ],
  "additional_notes": ""
}
```

## 📊 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Root endpoint |
| `/health` | GET | System health check |
| `/diagnose` | POST | Main diagnosis endpoint |
| `/sessions` | GET | List all sessions |
| `/sessions/{id}` | GET | Get session details |
| `/agents` | GET | List available agents |
| `/specialties` | GET | List medical specialties |
| `/docs` | GET | API documentation |

## 🔒 Security & Privacy

- **No Data Persistence**: Patient data is not stored permanently
- **Local Processing**: All analysis happens locally
- **HIPAA Considerations**: System includes appropriate disclaimers
- **API Security**: CORS enabled for web interface

## ⚠️ Important Disclaimers

- **Not Medical Advice**: This system is for educational and informational purposes only
- **Professional Consultation**: Always consult qualified healthcare providers
- **Emergency Situations**: Call emergency services for urgent medical conditions
- **AI Limitations**: Results should be validated by medical professionals

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Google ADK and Gemini for AI capabilities
- Medical community for domain expertise
- Open source community for tools and libraries

## 📞 Support

For questions or issues:
- Create an issue on GitHub
- Check the API documentation at `/docs`
- Review the system logs in `./logs/`

---

**🏥 Built with ❤️ for better healthcare through AI**


