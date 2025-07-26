"""
FastAPI application for Medical Diagnosis AI System
"""

import logging
from typing import List, Dict, Any, Optional
from fastapi import FastAPI, HTTPException, BackgroundTasks, UploadFile, File, Form, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import uvicorn
import tempfile
import os
import io

from src.coordinator import MedicalDiagnosisCoordinator
from src.models import (
    DiagnosisRequest, DiagnosisResult, PatientInfo, Symptom,
    ConsultationSession, UrgencyLevel, SeverityLevel
)
from src.config import settings

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(settings.LOG_FILE),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Medical Diagnosis AI System",
    description="A multi-agent AI system for medical diagnosis and patient care",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize coordinator
coordinator = MedicalDiagnosisCoordinator()

# Request/Response models for API
class SymptomRequest(BaseModel):
    name: str
    description: str
    severity: str
    duration: str
    onset: str
    triggers: List[str] = []
    alleviating_factors: List[str] = []

class PatientRequest(BaseModel):
    patient_id: str
    age: int
    gender: str
    weight: float = None
    height: float = None
    medical_history: List[str] = []
    allergies: List[str] = []
    medications: List[str] = []
    family_history: List[str] = []

class DiagnosisRequestAPI(BaseModel):
    patient_info: PatientRequest
    symptoms: List[SymptomRequest]
    additional_notes: str = None

class DiagnosisResponse(BaseModel):
    session_id: str
    diagnosis: DiagnosisResult
    message: str

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Medical Diagnosis AI System",
        "version": "1.0.0",
        "status": "operational"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "agents_loaded": len(coordinator.agents),
        "active_sessions": len(coordinator.sessions)
    }

@app.get("/specialties")
async def get_specialties():
    """Get available medical specialties"""
    from src.config import MEDICAL_SPECIALTIES
    return {
        "specialties": MEDICAL_SPECIALTIES,
        "count": len(MEDICAL_SPECIALTIES)
    }

@app.post("/diagnose", response_model=DiagnosisResponse)
async def diagnose_symptoms(
    request: Request,
    # For multipart/form-data
    json: Optional[str] = Form(None),
    files: Optional[list[UploadFile]] = File(None)
):
    """Main diagnosis endpoint supporting file uploads"""
    try:
        # If multipart/form-data, parse JSON and files
        if json is not None:
            import json as pyjson
            data = pyjson.loads(json)
        else:
            data = await request.json()
        # Parse patient info and symptoms as before
        patient_info = PatientInfo(**data["patient_info"])
        symptoms = [Symptom(**s) for s in data["symptoms"]]
        additional_notes = data.get("additional_notes", "")
        # Handle files (images/docs)
        uploaded_images = []
        uploaded_docs = []
        if files:
            for f in files:
                if f.content_type.startswith("image/"):
                    uploaded_images.append(f)
                elif f.content_type in ["application/pdf", "application/vnd.openxmlformats-officedocument.wordprocessingml.document", "text/plain"]:
                    uploaded_docs.append(f)
        # Extract text from documents
        doc_texts = []
        for doc in uploaded_docs:
            content = await doc.read()
            if doc.content_type == "application/pdf":
                try:
                    import PyPDF2
                    reader = PyPDF2.PdfReader(io.BytesIO(content))
                    text = " ".join(page.extract_text() or "" for page in reader.pages)
                    doc_texts.append(text)
                except Exception:
                    doc_texts.append("[Could not extract text from PDF]")
            elif doc.content_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                try:
                    import docx
                    docx_file = docx.Document(io.BytesIO(content))
                    text = " ".join([p.text for p in docx_file.paragraphs])
                    doc_texts.append(text)
                except Exception:
                    doc_texts.append("[Could not extract text from DOCX]")
            elif doc.content_type == "text/plain":
                try:
                    text = content.decode("utf-8", errors="ignore")
                    doc_texts.append(text)
                except Exception:
                    doc_texts.append("[Could not extract text from TXT]")
        # Pass everything to the coordinator
        diagnosis_request = DiagnosisRequest(
            patient_info=patient_info,
            symptoms=symptoms,
            additional_notes=additional_notes
        )
        # Read image bytes
        image_bytes_list = []
        for img in uploaded_images:
            image_bytes_list.append(await img.read())
        # Call coordinator with extra files/texts
        diagnosis_result = await coordinator.diagnose_symptoms(
            diagnosis_request,
            image_bytes_list=image_bytes_list,
            doc_texts=doc_texts
        )
        # Get session ID (assuming it's the latest session for this patient)
        session_id = None
        for session in coordinator.get_all_sessions():
            if session.patient_id == patient_info.patient_id:
                session_id = session.session_id
                break
        # Create response message based on urgency
        if diagnosis_result.urgency_level == UrgencyLevel.EMERGENCY:
            message = "URGENT: Please seek immediate medical attention. This may be a medical emergency."
        elif diagnosis_result.urgency_level == UrgencyLevel.URGENT:
            message = "URGENT: Please seek medical attention within 24 hours."
        else:
            message = "Please consult with your healthcare provider for proper evaluation and treatment."
        return DiagnosisResponse(
            session_id=session_id or "unknown",
            diagnosis=diagnosis_result,
            message=message
        )
    except Exception as e:
        import traceback
        traceback.print_exc()
        logger.error(f"Error in diagnosis endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Diagnosis failed: {str(e)}")

@app.get("/sessions/{session_id}")
async def get_session(session_id: str):
    """Get consultation session by ID"""
    session = coordinator.get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    return {
        "session_id": session.session_id,
        "patient_id": session.patient_id,
        "start_time": session.start_time,
        "end_time": session.end_time,
        "status": session.status,
        "agent_responses": [
            {
                "agent_id": resp.agent_id,
                "specialty": resp.specialty,
                "analysis": resp.analysis,
                "recommendations": resp.recommendations,
                "confidence": resp.confidence
            }
            for resp in session.agent_responses
        ],
        "final_diagnosis": session.final_diagnosis.dict() if session.final_diagnosis else None
    }

@app.get("/sessions")
async def get_all_sessions():
    """Get all consultation sessions"""
    sessions = coordinator.get_all_sessions()
    return {
        "sessions": [
            {
                "session_id": session.session_id,
                "patient_id": session.patient_id,
                "start_time": session.start_time,
                "end_time": session.end_time,
                "status": session.status
            }
            for session in sessions
        ],
        "count": len(sessions)
    }

@app.get("/agents")
async def get_agents():
    """Get information about available agents"""
    agents_info = []
    for specialty, agent in coordinator.agents.items():
        agents_info.append({
            "specialty": specialty,
            "agent_id": agent.agent_id,
            "name": agent.name,
            "description": agent.description,
            "expertise": agent.expertise
        })
    
    return {
        "agents": agents_info,
        "count": len(agents_info)
    }

if __name__ == "__main__":
    uvicorn.run(
        "src.api:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=settings.DEBUG
    ) 