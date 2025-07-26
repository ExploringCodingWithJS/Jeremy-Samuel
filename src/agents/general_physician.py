"""
General Physician Agent
Primary care and general medical diagnosis specialist
"""

from typing import Dict, List, Any
from src.agents.base_agent import BaseMedicalAgent
from src.models import AgentResponse, DiagnosisRequest

class GeneralPhysicianAgent(BaseMedicalAgent):
    """General Physician Agent for primary care and general medical diagnosis"""
    
    def __init__(self, agent_id: str = "gp_001"):
        super().__init__("general_physician", agent_id)
        
    async def specialized_analysis(self, diagnosis_request: DiagnosisRequest) -> AgentResponse:
        """Specialized analysis for general medical conditions"""
        
        # Add general physician specific prompt
        additional_prompt = """
As a General Physician, I focus on:
- Comprehensive health assessment
- Preventive care recommendations
- Coordination with specialists when needed
- Management of common medical conditions
- Patient education and lifestyle counseling

I will evaluate the overall health picture and determine if specialist referral is needed.
"""
        
        # Get base analysis
        base_response = await self.analyze_symptoms(diagnosis_request)
        
        # Enhance with general physician specific insights
        enhanced_analysis = self._enhance_general_physician_analysis(
            base_response, diagnosis_request
        )
        
        return enhanced_analysis
    
    def _enhance_general_physician_analysis(
        self, 
        base_response: AgentResponse, 
        diagnosis_request: DiagnosisRequest
    ) -> AgentResponse:
        """Enhance analysis with general physician specific insights"""
        
        # Add general health recommendations
        enhanced_recommendations = base_response.recommendations.copy()
        
        # Add preventive care recommendations
        patient_age = diagnosis_request.patient_info.age
        
        if patient_age >= 18:
            enhanced_recommendations.extend([
                "Schedule annual physical examination",
                "Consider routine blood work and health screenings",
                "Review vaccination status and update as needed"
            ])
        
        # Add lifestyle recommendations
        enhanced_recommendations.extend([
            "Maintain a balanced diet and regular exercise routine",
            "Ensure adequate sleep and stress management",
            "Avoid smoking and limit alcohol consumption"
        ])
        
        # Create enhanced response
        return AgentResponse(
            agent_id=base_response.agent_id,
            specialty=base_response.specialty,
            analysis=base_response.analysis + "\n\nAs your general physician, I recommend a comprehensive approach to your health concerns.",
            recommendations=enhanced_recommendations,
            confidence=base_response.confidence,
            additional_questions=base_response.additional_questions,
            suggested_tests=base_response.suggested_tests
        ) 