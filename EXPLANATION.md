# Technical Explanation

## 1. Agent Workflow

The Medical Diagnosis AI System processes patient symptoms through a sophisticated multi-agent workflow:

### Step-by-Step Process:

1. **Receive Patient Input**
   - Patient information (age, gender, medical history)
   - Symptom descriptions with severity, duration, onset
   - Additional context and notes

2. **Intelligent Specialist Routing**
   - Analyze symptoms against specialty mapping
   - Determine relevant medical specialists
   - Route to appropriate agents (General Physician always included)

3. **Concurrent Agent Analysis**
   - Multiple specialists analyze symptoms simultaneously
   - Each agent provides domain-specific insights
   - Emergency conditions flagged immediately

4. **Result Synthesis & Prioritization**
   - Combine analyses from all specialists
   - Prioritize recommendations by urgency
   - Calculate overall confidence scores

5. **Comprehensive Output Generation**
   - Structured diagnosis results
   - Immediate action recommendations
   - Follow-up plans and specialist referrals

## 2. Key Modules

### **Coordinator** (`src/coordinator.py`)
- **Purpose**: Orchestrates multi-agent diagnosis workflow
- **Key Functions**:
  - `diagnose_symptoms()`: Main entry point for diagnosis
  - `_determine_relevant_specialists()`: Routes symptoms to appropriate specialists
  - `_get_specialist_analyses()`: Manages concurrent agent processing
  - `_synthesize_diagnosis()`: Combines and prioritizes results

### **Base Medical Agent** (`src/agents/base_agent.py`)
- **Purpose**: Common functionality for all medical specialists
- **Key Functions**:
  - `analyze_symptoms()`: Core analysis workflow
  - `_create_analysis_prompt()`: Generates specialized prompts
  - `_parse_ai_response()`: Processes AI model responses
  - `specialized_analysis()`: Abstract method for specialist-specific logic

### **Specialist Agents** (`src/agents/*.py`)
- **Purpose**: Domain-specific medical expertise
- **Agents**: General Physician, Cardiology, Radiology, Neurology, Oncology, Pediatrics, Psychiatry
- **Key Functions**:
  - Emergency condition detection
  - Specialized test recommendations
  - Domain-specific insights and enhancements

### **API Layer** (`src/api.py`)
- **Purpose**: RESTful API interface
- **Key Functions**:
  - Request validation and processing
  - Response formatting and error handling
  - Session management and tracking

## 3. Tool Integration

### **Google ADK (Gemini) Integration**
- **Primary Tool**: Google Generative AI (Gemini 1.5 Flash - Free Tier)
- **Integration Method**: Direct API calls via `google.generativeai`
- **Multimodal Support**: Text, images, and document analysis
- **Usage Pattern**:
  ```python
  genai.configure(api_key=settings.GOOGLE_API_KEY)
  model = genai.GenerativeModel(model_name="gemini-1.5-flash")
  response = await asyncio.to_thread(model.generate_content, prompt)
  ```
- **Retry Logic**: Exponential backoff with jitter for reliability
- **Mock Mode**: Fallback responses when API quota is exceeded

### **Prompt Engineering**
- **Structured Prompts**: Each agent has specialized system prompts
- **Context Injection**: Patient info, symptoms, medical history
- **Response Formatting**: JSON-structured responses for parsing
- **Safety Guidelines**: Medical disclaimers and safety warnings

### **Concurrent Processing**
- **Async/Await**: Non-blocking agent analysis
- **asyncio.gather()**: Parallel specialist consultations
- **Error Handling**: Graceful degradation if agents fail
- **Multimodal Processing**: Concurrent image and document analysis
- **File Upload Support**: Multipart form data handling

## 4. Observability & Testing

### **Comprehensive Logging**
- **Location**: `./logs/medical_ai.log`
- **Levels**: INFO, ERROR, DEBUG, WARNING
- **Content**: Agent responses, API calls, error traces, retry attempts
- **Format**: Structured format with timestamps and module names
- **Multimodal Indicators**: File processing, image analysis, document extraction
- **Quota Monitoring**: API limit tracking and fallback handling

### **Health Monitoring**
- **Endpoint**: `/health` - System status and agent count
- **Metrics**: Active sessions, loaded agents, response times
- **Real-time**: Live system status updates

### **Session Tracking**
- **Storage**: In-memory session management
- **Data**: Complete consultation history
- **Access**: `/sessions` and `/sessions/{id}` endpoints

### **Testing Strategy**
```bash
# Import validation
python -c "import src; print('All imports successful')"

# API health check
curl http://localhost:8000/health

# End-to-end diagnosis test
curl -X POST http://localhost:8000/diagnose \
  -H "Content-Type: application/json" \
  -d @test_request.json
```

## 5. Known Limitations

### **AI Model Limitations**
- **Accuracy**: AI responses should be validated by medical professionals
- **Context**: Limited to training data cutoff date
- **Complexity**: May miss rare or complex medical conditions
- **Bias**: Potential for training data biases

### **System Limitations**
- **No Persistent Storage**: Patient data not permanently stored
- **Single Session**: No cross-session learning or memory
- **Limited Integration**: No direct EHR or medical database connections
- **Emergency Handling**: Cannot replace emergency medical services

### **Performance Considerations**
- **API Rate Limits**: Google Gemini API usage limits (15 requests/minute free tier)
- **Response Times**: Concurrent processing but still dependent on AI model speed
- **Scalability**: In-memory session storage limits concurrent users
- **Error Recovery**: Robust retry mechanisms with exponential backoff
- **Multimodal Processing**: Additional time for image/document analysis
- **Mock Mode**: Instant responses when API quota is exceeded

### **Medical Limitations**
- **Not Medical Advice**: Educational and informational purposes only
- **Professional Consultation**: Always requires healthcare provider validation
- **Emergency Situations**: Cannot handle true medical emergencies
- **Regulatory Compliance**: Not FDA-approved or HIPAA-compliant

## 6. Safety & Ethics

### **Medical Safety**
- **Emergency Detection**: Automatic flagging of urgent conditions
- **Disclaimers**: Clear warnings about AI limitations
- **Professional Guidance**: Always recommend healthcare provider consultation
- **No Treatment**: Only provides analysis, not treatment recommendations

### **Data Privacy**
- **No Persistence**: Patient data not stored permanently
- **Session-based**: Data only exists during active consultation
- **Local Processing**: All analysis happens on local infrastructure
- **Transparency**: Clear data handling policies

### **Ethical Considerations**
- **Bias Awareness**: Acknowledgment of potential AI biases
- **Accessibility**: Designed for broad accessibility
- **Transparency**: Clear explanation of AI decision-making
- **Accountability**: Clear disclaimers and limitations

