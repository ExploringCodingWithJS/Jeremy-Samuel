## 2. `ARCHITECTURE.md`

```markdown
# Architecture Overview

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    Medical Diagnosis AI System                  │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Streamlit     │    │   FastAPI       │    │   Coordinator   │
│   Frontend      │◄──►│   Backend       │◄──►│   (Orchestrator)│
│                 │    │                 │    │                 │
│ • Patient Input │    │ • REST API      │    │ • Agent Mgmt    │
│ • Results Display│   │ • Request/Resp  │    │ • Session Mgmt  │
│ • Session History│   │ • CORS Support  │    │ • Diagnosis     │
│ • System Info   │    │ • Documentation │    │   Synthesis     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │                       │
                                ▼                       ▼
                       ┌─────────────────┐    ┌─────────────────┐
                       │   Google ADK    │    │   Medical       │
                       │   (Gemini)      │    │   Agents        │
                       │                 │    │                 │
                       │ • AI Model      │    │ • Base Agent    │
                       │ • API Calls     │    │ • Specialists   │
                       │ • Response      │    │ • Analysis      │
                       │   Processing    │    │ • Enhancement   │
                       └─────────────────┘    └─────────────────┘
                                                        │
                                                        ▼
                                              ┌─────────────────┐
                                              │   Specialists   │
                                              │   (7 Agents)    │
                                              │                 │
                                              │ • General       │
                                              │   Physician     │
                                              │ • Cardiology    │
                                              │ • Radiology     │
                                              │ • Neurology     │
                                              │ • Oncology      │
                                              │ • Pediatrics    │
                                              │ • Psychiatry    │
                                              └─────────────────┘
```

## Component Details

### 1. Frontend (Streamlit)
- **Purpose**: User interface for patient interaction
- **Features**:
  - Patient information input
  - Symptom description and management
  - Real-time diagnosis results
  - Session history viewing
  - System information display

### 2. Backend (FastAPI)
- **Purpose**: RESTful API server
- **Features**:
  - Request/response handling
  - Data validation
  - CORS support
  - API documentation (Swagger/ReDoc)
  - Health monitoring

### 3. Coordinator (Orchestrator)
- **Purpose**: Manages multi-agent diagnosis workflow
- **Features**:
  - Agent initialization and management
  - Symptom-to-specialist routing
  - Concurrent agent analysis
  - Result synthesis and prioritization
  - Session tracking

### 4. Medical Agents
- **Base Agent**: Common functionality for all specialists
- **Specialist Agents**: Domain-specific medical expertise
- **Features**:
  - Specialized medical knowledge
  - Emergency condition detection
  - Evidence-based recommendations
  - Empathetic communication

### 5. Google ADK Integration
- **Purpose**: AI model access and processing
- **Features**:
  - Gemini 1.5 Flash model integration (free tier)
  - Multimodal analysis (text + images + documents)
  - Structured prompt engineering
  - Response parsing and validation
  - Error handling and fallbacks
  - Retry logic with exponential backoff
  - Mock mode for testing without API calls

## Data Flow

```
1. Patient Input → Streamlit Frontend (text + files)
2. Frontend → FastAPI Backend (multipart/form-data)
3. Backend → File Processing (image/document extraction)
4. Backend → Coordinator (Internal Call)
5. Coordinator → Symptom Analysis (Routing Logic)
6. Coordinator → Relevant Agents (Concurrent Calls)
7. Agents → Google ADK (Multimodal AI Analysis)
8. Google ADK → Agents (Structured Response)
9. Agents → Coordinator (Enhanced Analysis)
10. Coordinator → Backend (Synthesized Results)
11. Backend → Frontend (HTTP Response)
12. Frontend → Patient (Display Results)
```

## Key Design Principles

### 1. Modularity
- Each component has a single responsibility
- Clear interfaces between components
- Easy to extend with new specialists

### 2. Scalability
- Concurrent agent processing
- Stateless API design
- Configurable agent pool

### 3. Reliability
- Error handling at each layer
- Graceful degradation
- Comprehensive logging

### 4. Security
- Input validation
- No persistent patient data
- Appropriate disclaimers

### 5. User Experience
- Intuitive interface
- Real-time feedback
- Comprehensive results

## Technology Stack

| Component | Technology | Purpose |
|-----------|------------|---------|
| Frontend | Streamlit | Web interface with file upload |
| Backend | FastAPI | API server with multipart support |
| AI | Google Gemini 1.5 Flash | Multimodal medical analysis |
| Language | Python 3.8+ | Core development |
| Data | Pydantic | Validation |
| Logging | Python logging | Monitoring |
| File Processing | PyPDF2, python-docx | Document text extraction |
| Retry Logic | Custom utils | Exponential backoff |

## Configuration Management

- Environment-based configuration
- Centralized settings in `src/config.py`
- Agent-specific configurations
- Runtime parameter tuning

## Monitoring & Observability

- Comprehensive logging with structured format
- Health check endpoints (`/health`, `/agents`, `/specialties`)
- Session tracking with full consultation history
- Performance metrics and response times
- Error reporting with retry mechanisms
- Multimodal processing indicators
- API quota monitoring and fallback handling

