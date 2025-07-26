"""
Neurology Agent
Nervous system and brain specialist
"""

from typing import Dict, List, Any
from src.agents.base_agent import BaseMedicalAgent
from src.models import AgentResponse, DiagnosisRequest

class NeurologyAgent(BaseMedicalAgent):
    """Neurology Agent for nervous system and brain disorders"""
    
    def __init__(self, agent_id: str = "neuro_001"):
        super().__init__("neurology", agent_id)
        
    async def specialized_analysis(self, diagnosis_request: DiagnosisRequest) -> AgentResponse:
        """Specialized analysis for neurological conditions"""
        
        # Get base analysis
        base_response = await self.analyze_symptoms(diagnosis_request)
        
        # Enhance with neurology specific insights
        enhanced_analysis = self._enhance_neurology_analysis(
            base_response, diagnosis_request
        )
        
        return enhanced_analysis
    
    def _enhance_neurology_analysis(
        self, 
        base_response: AgentResponse, 
        diagnosis_request: DiagnosisRequest
    ) -> AgentResponse:
        """Enhance analysis with neurology specific insights"""
        
        enhanced_recommendations = base_response.recommendations.copy()
        enhanced_tests = base_response.suggested_tests.copy()
        
        # Add neurology specific tests
        enhanced_tests.extend([
            "Neurological examination",
            "Brain MRI or CT scan",
            "Electroencephalogram (EEG)",
            "Nerve conduction studies",
            "Lumbar puncture (if indicated)"
        ])
        
        # Add neurology specific recommendations
        enhanced_recommendations.extend([
            "Complete neurological examination by a neurologist",
            "Monitor for changes in symptoms",
            "Consider neuroimaging studies",
            "Evaluate for signs of stroke or other acute neurological conditions"
        ])
        
        # Check for emergency neurological symptoms
        if self._check_emergency_neurological_symptoms(diagnosis_request):
            enhanced_recommendations.insert(0, "URGENT: Seek immediate medical attention - possible neurological emergency")
        
        return AgentResponse(
            agent_id=base_response.agent_id,
            specialty=base_response.specialty,
            analysis=base_response.analysis + "\n\nAs a neurologist, I've evaluated your symptoms for potential neurological concerns.",
            recommendations=enhanced_recommendations,
            confidence=base_response.confidence,
            additional_questions=base_response.additional_questions,
            suggested_tests=enhanced_tests
        )
    
    def _check_emergency_neurological_symptoms(self, diagnosis_request: DiagnosisRequest) -> bool:
        """Check for emergency neurological symptoms"""
        emergency_keywords = [
            "sudden severe headache", "worst headache", "thunderclap headache",
            "sudden weakness", "paralysis", "numbness", "speech problems",
            "vision loss", "double vision", "seizure", "loss of consciousness"
        ]
        
        for symptom in diagnosis_request.symptoms:
            symptom_text = f"{symptom.name} {symptom.description}".lower()
            for keyword in emergency_keywords:
                if keyword in symptom_text and symptom.severity.value in ["severe", "critical"]:
                    return True
        
        return False 