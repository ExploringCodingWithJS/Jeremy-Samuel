"""
Oncology Agent
Cancer diagnosis and treatment specialist
"""

from typing import Dict, List, Any
from src.agents.base_agent import BaseMedicalAgent
from src.models import AgentResponse, DiagnosisRequest

class OncologyAgent(BaseMedicalAgent):
    """Oncology Agent for cancer diagnosis and treatment"""
    
    def __init__(self, agent_id: str = "onco_001"):
        super().__init__("oncology", agent_id)
        
    async def specialized_analysis(self, diagnosis_request: DiagnosisRequest) -> AgentResponse:
        """Specialized analysis for oncological conditions"""
        
        # Get base analysis
        base_response = await self.analyze_symptoms(diagnosis_request)
        
        # Enhance with oncology specific insights
        enhanced_analysis = self._enhance_oncology_analysis(
            base_response, diagnosis_request
        )
        
        return enhanced_analysis
    
    def _enhance_oncology_analysis(
        self, 
        base_response: AgentResponse, 
        diagnosis_request: DiagnosisRequest
    ) -> AgentResponse:
        """Enhance analysis with oncology specific insights"""
        
        enhanced_recommendations = base_response.recommendations.copy()
        enhanced_tests = base_response.suggested_tests.copy()
        
        # Add oncology specific tests
        enhanced_tests.extend([
            "Comprehensive blood work including tumor markers",
            "Biopsy of suspicious lesions",
            "Imaging studies (CT, MRI, PET scan)",
            "Genetic testing if indicated",
            "Staging workup if cancer is suspected"
        ])
        
        # Add oncology specific recommendations
        enhanced_recommendations.extend([
            "Consult with an oncologist for comprehensive evaluation",
            "Consider cancer screening based on age and risk factors",
            "Monitor for cancer warning signs",
            "Review family history for cancer predisposition"
        ])
        
        # Add cancer warning signs assessment
        warning_signs = self._assess_cancer_warning_signs(diagnosis_request)
        if warning_signs:
            enhanced_recommendations.insert(0, "URGENT: Symptoms may indicate cancer warning signs - immediate evaluation recommended")
        
        return AgentResponse(
            agent_id=base_response.agent_id,
            specialty=base_response.specialty,
            analysis=base_response.analysis + "\n\nAs an oncologist, I've evaluated your symptoms for potential oncological concerns.",
            recommendations=enhanced_recommendations,
            confidence=base_response.confidence,
            additional_questions=base_response.additional_questions,
            suggested_tests=enhanced_tests
        )
    
    def _assess_cancer_warning_signs(self, diagnosis_request: DiagnosisRequest) -> bool:
        """Assess for cancer warning signs"""
        warning_signs = [
            "unexplained weight loss", "lump", "mass", "tumor",
            "persistent cough", "blood in stool", "blood in urine",
            "unexplained bleeding", "persistent pain", "fatigue",
            "night sweats", "fever", "changes in skin", "mole changes"
        ]
        
        for symptom in diagnosis_request.symptoms:
            symptom_text = f"{symptom.name} {symptom.description}".lower()
            for sign in warning_signs:
                if sign in symptom_text:
                    return True
        
        return False 