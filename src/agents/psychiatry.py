"""
Psychiatry Agent
Mental health and behavioral disorders specialist
"""

from typing import Dict, List, Any
from src.agents.base_agent import BaseMedicalAgent
from src.models import AgentResponse, DiagnosisRequest

class PsychiatryAgent(BaseMedicalAgent):
    """Psychiatry Agent for mental health and behavioral disorders"""
    
    def __init__(self, agent_id: str = "psych_001"):
        super().__init__("psychiatry", agent_id)
        
    async def specialized_analysis(self, diagnosis_request: DiagnosisRequest) -> AgentResponse:
        """Specialized analysis for psychiatric conditions"""
        
        # Get base analysis
        base_response = await self.analyze_symptoms(diagnosis_request)
        
        # Enhance with psychiatry specific insights
        enhanced_analysis = self._enhance_psychiatry_analysis(
            base_response, diagnosis_request
        )
        
        return enhanced_analysis
    
    def _enhance_psychiatry_analysis(
        self, 
        base_response: AgentResponse, 
        diagnosis_request: DiagnosisRequest
    ) -> AgentResponse:
        """Enhance analysis with psychiatry specific insights"""
        
        enhanced_recommendations = base_response.recommendations.copy()
        enhanced_tests = base_response.suggested_tests.copy()
        
        # Add psychiatry specific tests
        enhanced_tests.extend([
            "Comprehensive psychiatric evaluation",
            "Mental status examination",
            "Psychological assessment tools",
            "Laboratory tests to rule out medical causes",
            "Substance use screening"
        ])
        
        # Add psychiatry specific recommendations
        enhanced_recommendations.extend([
            "Consult with a psychiatrist for comprehensive mental health evaluation",
            "Consider psychotherapy or counseling",
            "Monitor for safety concerns",
            "Review medication history and potential interactions"
        ])
        
        # Check for emergency psychiatric symptoms
        if self._check_emergency_psychiatric_symptoms(diagnosis_request):
            enhanced_recommendations.insert(0, "URGENT: Seek immediate mental health evaluation - possible psychiatric emergency")
        
        # Add safety recommendations
        safety_recs = self._get_safety_recommendations(diagnosis_request)
        enhanced_recommendations.extend(safety_recs)
        
        return AgentResponse(
            agent_id=base_response.agent_id,
            specialty=base_response.specialty,
            analysis=base_response.analysis + "\n\nAs a psychiatrist, I've evaluated your symptoms for potential mental health concerns.",
            recommendations=enhanced_recommendations,
            confidence=base_response.confidence,
            additional_questions=base_response.additional_questions,
            suggested_tests=enhanced_tests
        )
    
    def _check_emergency_psychiatric_symptoms(self, diagnosis_request: DiagnosisRequest) -> bool:
        """Check for emergency psychiatric symptoms"""
        emergency_keywords = [
            "suicidal thoughts", "suicide", "self-harm", "homicidal thoughts",
            "psychosis", "hallucinations", "delusions", "paranoia",
            "severe depression", "mania", "violent thoughts"
        ]
        
        for symptom in diagnosis_request.symptoms:
            symptom_text = f"{symptom.name} {symptom.description}".lower()
            for keyword in emergency_keywords:
                if keyword in symptom_text:
                    return True
        
        return False
    
    def _get_safety_recommendations(self, diagnosis_request: DiagnosisRequest) -> List[str]:
        """Get safety recommendations for psychiatric patients"""
        safety_recs = [
            "Ensure a safe environment",
            "Remove access to potentially harmful objects",
            "Have emergency contact information readily available",
            "Consider 24-hour crisis hotline numbers"
        ]
        
        # Add specific safety measures based on symptoms
        for symptom in diagnosis_request.symptoms:
            symptom_text = f"{symptom.name} {symptom.description}".lower()
            if "suicide" in symptom_text or "self-harm" in symptom_text:
                safety_recs.extend([
                    "Do not leave the person alone",
                    "Remove firearms and medications from the environment",
                    "Contact emergency services if immediate danger is present"
                ])
        
        return safety_recs 