"""
Data models for the Medical Diagnosis AI System
"""

from datetime import datetime
from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field
from enum import Enum

class SeverityLevel(str, Enum):
    """Severity levels for symptoms and conditions"""
    MILD = "mild"
    MODERATE = "moderate"
    SEVERE = "severe"
    CRITICAL = "critical"

class UrgencyLevel(str, Enum):
    """Urgency levels for medical attention"""
    ROUTINE = "routine"
    URGENT = "urgent"
    EMERGENCY = "emergency"

class PatientInfo(BaseModel):
    """Patient information model"""
    patient_id: str
    age: int
    gender: str
    weight: Optional[float] = None
    height: Optional[float] = None
    medical_history: List[str] = []
    allergies: List[str] = []
    medications: List[str] = []
    family_history: List[str] = []

class Symptom(BaseModel):
    """Symptom model"""
    name: str
    description: str
    severity: SeverityLevel
    duration: str
    onset: str
    triggers: List[str] = []
    alleviating_factors: List[str] = []

class DiagnosisRequest(BaseModel):
    """Diagnosis request model"""
    patient_info: PatientInfo
    symptoms: List[Symptom]
    additional_notes: Optional[str] = None
    urgency_level: UrgencyLevel = UrgencyLevel.ROUTINE

class DiagnosisResult(BaseModel):
    """Diagnosis result model"""
    possible_conditions: List[Dict[str, Any]]
    recommended_specialists: List[str]
    suggested_tests: List[str]
    immediate_actions: List[str]
    follow_up_plan: str
    confidence_score: float
    urgency_level: UrgencyLevel
    disclaimers: List[str]

class AgentResponse(BaseModel):
    """Agent response model"""
    agent_id: str
    specialty: str
    analysis: str
    recommendations: List[str]
    confidence: float
    additional_questions: List[str] = []
    suggested_tests: List[str] = []

class ConsultationSession(BaseModel):
    """Consultation session model"""
    session_id: str
    patient_id: str
    start_time: datetime
    end_time: Optional[datetime] = None
    diagnosis_request: DiagnosisRequest
    agent_responses: List[AgentResponse] = []
    final_diagnosis: Optional[DiagnosisResult] = None
    status: str = "active"

class MedicalKnowledge(BaseModel):
    """Medical knowledge base entry"""
    condition: str
    symptoms: List[str]
    risk_factors: List[str]
    diagnostic_tests: List[str]
    treatments: List[str]
    specialists: List[str]
    urgency_level: UrgencyLevel
    description: str

class AgentConfig(BaseModel):
    """Agent configuration model"""
    agent_id: str
    specialty: str
    name: str
    description: str
    expertise: List[str]
    model: str
    temperature: float
    system_prompt: str
    is_active: bool = True 