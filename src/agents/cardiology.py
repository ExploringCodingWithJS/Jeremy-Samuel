"""
Cardiology Agent
Heart and cardiovascular system specialist
"""

from typing import Dict, List, Any
from src.agents.base_agent import BaseMedicalAgent
from src.models import AgentResponse, DiagnosisRequest, UrgencyLevel

class CardiologyAgent(BaseMedicalAgent):
    """Cardiology Agent for heart and cardiovascular system diagnosis"""
    
    def __init__(self, agent_id: str = "cardio_001"):
        super().__init__("cardiology", agent_id)
        
    async def specialized_analysis(self, diagnosis_request: DiagnosisRequest) -> AgentResponse:
        """Specialized analysis for cardiovascular conditions"""
        
        # Add cardiology specific prompt
        additional_prompt = """
As a Cardiologist, I specialize in:
- Heart disease and cardiovascular conditions
- Cardiac imaging and diagnostic tests
- Risk factor assessment and management
- Emergency cardiac conditions
- Preventive cardiology

I will evaluate cardiac symptoms and determine appropriate diagnostic and treatment approaches.
"""
        
        # Get base analysis
        base_response = await self.analyze_symptoms(diagnosis_request)
        
        # Enhance with cardiology specific insights
        enhanced_analysis = self._enhance_cardiology_analysis(
            base_response, diagnosis_request
        )
        
        return enhanced_analysis
    
    def _enhance_cardiology_analysis(
        self, 
        base_response: AgentResponse, 
        diagnosis_request: DiagnosisRequest
    ) -> AgentResponse:
        """Enhance analysis with cardiology specific insights"""
        
        # Check for emergency cardiac symptoms
        emergency_symptoms = self._check_emergency_cardiac_symptoms(diagnosis_request)
        
        enhanced_recommendations = base_response.recommendations.copy()
        enhanced_tests = base_response.suggested_tests.copy()
        
        # Add cardiology specific tests
        enhanced_tests.extend([
            "Electrocardiogram (ECG/EKG)",
            "Echocardiogram",
            "Cardiac stress test",
            "Holter monitor (24-hour ECG)",
            "Cardiac CT or MRI if indicated"
        ])
        
        # Add cardiac risk factor assessment
        enhanced_recommendations.extend([
            "Assess cardiac risk factors (hypertension, diabetes, smoking, family history)",
            "Monitor blood pressure regularly",
            "Consider lipid profile testing",
            "Evaluate for signs of heart failure"
        ])
        
        # Add emergency recommendations if needed
        if emergency_symptoms:
            enhanced_recommendations.insert(0, "URGENT: Seek immediate medical attention - possible cardiac emergency")
            enhanced_recommendations.insert(1, "Call emergency services if chest pain is severe or accompanied by shortness of breath")
        
        # Create enhanced response
        return AgentResponse(
            agent_id=base_response.agent_id,
            specialty=base_response.specialty,
            analysis=base_response.analysis + "\n\nAs a cardiologist, I've evaluated your symptoms for potential cardiovascular concerns.",
            recommendations=enhanced_recommendations,
            confidence=base_response.confidence,
            additional_questions=base_response.additional_questions,
            suggested_tests=enhanced_tests
        )
    
    def _check_emergency_cardiac_symptoms(self, diagnosis_request: DiagnosisRequest) -> bool:
        """Check for emergency cardiac symptoms"""
        emergency_keywords = [
            "chest pain", "chest pressure", "heart attack", "angina",
            "severe chest pain", "crushing chest pain", "chest tightness",
            "sudden chest pain", "chest pain with shortness of breath"
        ]
        
        for symptom in diagnosis_request.symptoms:
            symptom_text = f"{symptom.name} {symptom.description}".lower()
            for keyword in emergency_keywords:
                if keyword in symptom_text and symptom.severity.value in ["severe", "critical"]:
                    return True
        
        return False 