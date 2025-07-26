"""
Medical Diagnosis Coordinator
Manages multiple specialist agents for comprehensive medical diagnosis
"""

import asyncio
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime
import uuid

from src.config import settings, SYMPTOM_SPECIALTY_MAPPING, MEDICAL_SPECIALTIES
from src.models import (
    DiagnosisRequest, DiagnosisResult, AgentResponse, 
    ConsultationSession, UrgencyLevel, PatientInfo, Symptom
)
from src.agents import (
    GeneralPhysicianAgent, CardiologyAgent, RadiologyAgent,
    NeurologyAgent, OncologyAgent, PediatricsAgent, PsychiatryAgent
)

logger = logging.getLogger(__name__)

class MedicalDiagnosisCoordinator:
    """Coordinates multiple medical specialist agents for comprehensive diagnosis"""
    
    def __init__(self):
        self.agents = {}
        self.sessions = {}
        self._initialize_agents()
        
    def _initialize_agents(self):
        """Initialize all medical specialist agents"""
        self.agents = {
            "general_physician": GeneralPhysicianAgent("gp_001"),
            "cardiology": CardiologyAgent("cardio_001"),
            "radiology": RadiologyAgent("radio_001"),
            "neurology": NeurologyAgent("neuro_001"),
            "oncology": OncologyAgent("onco_001"),
            "pediatrics": PediatricsAgent("ped_001"),
            "psychiatry": PsychiatryAgent("psych_001")
        }
        logger.info(f"Initialized {len(self.agents)} medical specialist agents")
    
    async def diagnose_symptoms(self, diagnosis_request: DiagnosisRequest) -> DiagnosisResult:
        """Main method to coordinate diagnosis across multiple specialists"""
        try:
            # Create consultation session
            session_id = str(uuid.uuid4())
            session = ConsultationSession(
                session_id=session_id,
                patient_id=diagnosis_request.patient_info.patient_id,
                start_time=datetime.now(),
                diagnosis_request=diagnosis_request
            )
            self.sessions[session_id] = session
            
            logger.info(f"Starting diagnosis session {session_id} for patient {diagnosis_request.patient_info.patient_id}")
            
            # Determine which specialists to consult
            relevant_specialists = self._determine_relevant_specialists(diagnosis_request)
            
            # Get analyses from relevant specialists
            agent_responses = await self._get_specialist_analyses(
                diagnosis_request, relevant_specialists
            )
            
            # Update session with agent responses
            session.agent_responses = agent_responses
            
            # Synthesize final diagnosis
            final_diagnosis = await self._synthesize_diagnosis(
                diagnosis_request, agent_responses
            )
            
            # Update session with final diagnosis
            session.final_diagnosis = final_diagnosis
            session.end_time = datetime.now()
            session.status = "completed"
            
            logger.info(f"Completed diagnosis session {session_id}")
            
            return final_diagnosis
            
        except Exception as e:
            logger.error(f"Error in diagnosis coordination: {str(e)}")
            return self._create_error_diagnosis(diagnosis_request)
    
    def _determine_relevant_specialists(self, diagnosis_request: DiagnosisRequest) -> List[str]:
        """Determine which specialists should be consulted based on symptoms"""
        relevant_specialists = set()
        
        # Always include general physician
        relevant_specialists.add("general_physician")
        
        # Check symptoms against specialty mapping
        for symptom in diagnosis_request.symptoms:
            symptom_text = f"{symptom.name} {symptom.description}".lower()
            
            for symptom_keyword, specialties in SYMPTOM_SPECIALTY_MAPPING.items():
                if symptom_keyword in symptom_text:
                    relevant_specialists.update(specialties)
        
        # Add age-based specialists
        patient_age = diagnosis_request.patient_info.age
        if patient_age < 18:
            relevant_specialists.add("pediatrics")
        
        # Add mental health specialist if mental health symptoms are present
        mental_health_keywords = ["anxiety", "depression", "mood", "behavior", "mental"]
        for symptom in diagnosis_request.symptoms:
            symptom_text = f"{symptom.name} {symptom.description}".lower()
            if any(keyword in symptom_text for keyword in mental_health_keywords):
                relevant_specialists.add("psychiatry")
        
        return list(relevant_specialists)
    
    async def _get_specialist_analyses(
        self, 
        diagnosis_request: DiagnosisRequest, 
        specialists: List[str]
    ) -> List[AgentResponse]:
        """Get analyses from all relevant specialists"""
        tasks = []
        
        for specialty in specialists:
            if specialty in self.agents:
                agent = self.agents[specialty]
                task = agent.specialized_analysis(diagnosis_request)
                tasks.append(task)
        
        # Execute all analyses concurrently
        responses = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Filter out exceptions and return valid responses
        valid_responses = []
        for response in responses:
            if isinstance(response, Exception):
                logger.error(f"Agent analysis failed: {str(response)}")
            else:
                valid_responses.append(response)
        
        return valid_responses
    
    async def _synthesize_diagnosis(
        self, 
        diagnosis_request: DiagnosisRequest, 
        agent_responses: List[AgentResponse]
    ) -> DiagnosisResult:
        """Synthesize final diagnosis from all specialist responses"""
        
        # Collect all possible conditions
        all_conditions = []
        all_recommendations = []
        all_tests = []
        all_questions = []
        
        # Calculate overall confidence
        total_confidence = 0
        valid_responses = 0
        
        # Determine overall urgency level
        urgency_level = UrgencyLevel.ROUTINE
        
        for response in agent_responses:
            if response.confidence > 0:
                total_confidence += response.confidence
                valid_responses += 1
            
            # Check for urgent recommendations
            for rec in response.recommendations:
                if "URGENT" in rec.upper() or "EMERGENCY" in rec.upper():
                    urgency_level = UrgencyLevel.EMERGENCY
                elif "urgent" in rec.lower() and urgency_level != UrgencyLevel.EMERGENCY:
                    urgency_level = UrgencyLevel.URGENT
            
            all_recommendations.extend(response.recommendations)
            all_tests.extend(response.suggested_tests)
            all_questions.extend(response.additional_questions)
        
        # Calculate average confidence
        overall_confidence = total_confidence / valid_responses if valid_responses > 0 else 0.5
        
        # Remove duplicates and organize
        unique_recommendations = list(set(all_recommendations))
        unique_tests = list(set(all_tests))
        unique_questions = list(set(all_questions))
        
        # Create immediate actions based on urgency
        immediate_actions = self._create_immediate_actions(urgency_level, unique_recommendations)
        
        # Create follow-up plan
        follow_up_plan = self._create_follow_up_plan(agent_responses, diagnosis_request)
        
        # Create disclaimers
        disclaimers = [
            "This is an AI-assisted analysis and should not replace professional medical evaluation",
            "Always consult with qualified healthcare providers for proper diagnosis and treatment",
            "Emergency symptoms require immediate medical attention",
            "Individual medical decisions should be made in consultation with healthcare professionals"
        ]
        
        return DiagnosisResult(
            possible_conditions=all_conditions,
            recommended_specialists=[resp.specialty for resp in agent_responses],
            suggested_tests=unique_tests,
            immediate_actions=immediate_actions,
            follow_up_plan=follow_up_plan,
            confidence_score=overall_confidence,
            urgency_level=urgency_level,
            disclaimers=disclaimers
        )
    
    def _create_immediate_actions(self, urgency_level: UrgencyLevel, recommendations: List[str]) -> List[str]:
        """Create immediate actions based on urgency level"""
        immediate_actions = []
        
        if urgency_level == UrgencyLevel.EMERGENCY:
            immediate_actions.extend([
                "Call emergency services immediately (911 or local emergency number)",
                "Do not delay seeking medical attention",
                "Follow emergency medical personnel instructions"
            ])
        elif urgency_level == UrgencyLevel.URGENT:
            immediate_actions.extend([
                "Seek medical attention within 24 hours",
                "Contact your primary care physician or visit urgent care",
                "Monitor symptoms closely and seek care if they worsen"
            ])
        else:
            immediate_actions.extend([
                "Schedule an appointment with your primary care physician",
                "Monitor symptoms and seek care if they persist or worsen",
                "Follow up with recommended specialists as needed"
            ])
        
        # Add specific recommendations
        for rec in recommendations:
            if "URGENT" in rec.upper() or "IMMEDIATE" in rec.upper():
                immediate_actions.append(rec)
        
        return immediate_actions
    
    def _create_follow_up_plan(self, agent_responses: List[AgentResponse], diagnosis_request: DiagnosisRequest) -> str:
        """Create a comprehensive follow-up plan"""
        plan_parts = []
        
        # Add general follow-up
        plan_parts.append("1. Schedule follow-up with your primary care physician")
        
        # Add specialist-specific follow-up
        for response in agent_responses:
            if response.specialty != "general_physician":
                plan_parts.append(f"2. Consider consultation with {response.specialty} specialist")
        
        # Add testing follow-up
        all_tests = []
        for response in agent_responses:
            all_tests.extend(response.suggested_tests)
        
        if all_tests:
            unique_tests = list(set(all_tests))
            plan_parts.append(f"3. Schedule recommended diagnostic tests: {', '.join(unique_tests[:5])}")
        
        # Add monitoring instructions
        plan_parts.append("4. Monitor symptoms and report any changes to your healthcare provider")
        plan_parts.append("5. Follow up on test results and specialist recommendations")
        
        return "\n".join(plan_parts)
    
    def _create_error_diagnosis(self, diagnosis_request: DiagnosisRequest) -> DiagnosisResult:
        """Create an error diagnosis when coordination fails"""
        return DiagnosisResult(
            possible_conditions=[],
            recommended_specialists=["general_physician"],
            suggested_tests=[],
            immediate_actions=[
                "Contact your healthcare provider for proper evaluation",
                "Seek medical attention if symptoms are severe or concerning"
            ],
            follow_up_plan="Please consult with a healthcare provider for proper diagnosis and treatment.",
            confidence_score=0.0,
            urgency_level=UrgencyLevel.ROUTINE,
            disclaimers=[
                "System error occurred during analysis",
                "Please consult with qualified healthcare providers",
                "This analysis should not replace professional medical evaluation"
            ]
        )
    
    def get_session(self, session_id: str) -> Optional[ConsultationSession]:
        """Get a consultation session by ID"""
        return self.sessions.get(session_id)
    
    def get_all_sessions(self) -> List[ConsultationSession]:
        """Get all consultation sessions"""
        return list(self.sessions.values()) 