"""
Pediatrics Agent
Children's health and development specialist
"""

from typing import Dict, List, Any
from src.agents.base_agent import BaseMedicalAgent
from src.models import AgentResponse, DiagnosisRequest

class PediatricsAgent(BaseMedicalAgent):
    """Pediatrics Agent for children's health and development"""
    
    def __init__(self, agent_id: str = "ped_001"):
        super().__init__("pediatrics", agent_id)
        
    async def specialized_analysis(self, diagnosis_request: DiagnosisRequest) -> AgentResponse:
        """Specialized analysis for pediatric conditions"""
        
        # Get base analysis
        base_response = await self.analyze_symptoms(diagnosis_request)
        
        # Enhance with pediatrics specific insights
        enhanced_analysis = self._enhance_pediatrics_analysis(
            base_response, diagnosis_request
        )
        
        return enhanced_analysis
    
    def _enhance_pediatrics_analysis(
        self, 
        base_response: AgentResponse, 
        diagnosis_request: DiagnosisRequest
    ) -> AgentResponse:
        """Enhance analysis with pediatrics specific insights"""
        
        enhanced_recommendations = base_response.recommendations.copy()
        enhanced_tests = base_response.suggested_tests.copy()
        
        # Add pediatrics specific tests
        enhanced_tests.extend([
            "Pediatric physical examination",
            "Growth and development assessment",
            "Age-appropriate laboratory tests",
            "Developmental screening tests",
            "Vaccination status review"
        ])
        
        # Add pediatrics specific recommendations
        enhanced_recommendations.extend([
            "Consult with a pediatrician for age-appropriate care",
            "Monitor growth and development milestones",
            "Ensure up-to-date vaccinations",
            "Consider developmental screening if indicated"
        ])
        
        # Add age-specific recommendations
        age_specific_recs = self._get_age_specific_recommendations(diagnosis_request)
        enhanced_recommendations.extend(age_specific_recs)
        
        return AgentResponse(
            agent_id=base_response.agent_id,
            specialty=base_response.specialty,
            analysis=base_response.analysis + "\n\nAs a pediatrician, I've evaluated your child's symptoms with age-appropriate considerations.",
            recommendations=enhanced_recommendations,
            confidence=base_response.confidence,
            additional_questions=base_response.additional_questions,
            suggested_tests=enhanced_tests
        )
    
    def _get_age_specific_recommendations(self, diagnosis_request: DiagnosisRequest) -> List[str]:
        """Get age-specific pediatric recommendations"""
        age = diagnosis_request.patient_info.age
        recommendations = []
        
        if age < 2:
            recommendations.extend([
                "Monitor feeding and growth patterns",
                "Assess developmental milestones",
                "Review vaccination schedule"
            ])
        elif age < 5:
            recommendations.extend([
                "Monitor speech and language development",
                "Assess motor skills and coordination",
                "Review safety measures and childproofing"
            ])
        elif age < 12:
            recommendations.extend([
                "Monitor school performance and behavior",
                "Assess social development",
                "Review nutrition and physical activity"
            ])
        else:
            recommendations.extend([
                "Monitor adolescent development",
                "Assess mental health and well-being",
                "Review risk behaviors and safety"
            ])
        
        return recommendations 