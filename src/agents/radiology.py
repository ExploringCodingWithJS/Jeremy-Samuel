"""
Radiology Agent
Medical imaging and diagnostic radiology specialist
"""

from typing import Dict, List, Any
from src.agents.base_agent import BaseMedicalAgent
from src.models import AgentResponse, DiagnosisRequest

class RadiologyAgent(BaseMedicalAgent):
    """Radiology Agent for medical imaging and diagnostic radiology"""
    
    def __init__(self, agent_id: str = "radio_001"):
        super().__init__("radiology", agent_id)
        
    async def specialized_analysis(self, diagnosis_request: DiagnosisRequest) -> AgentResponse:
        """Specialized analysis for radiological imaging and diagnosis"""
        
        # Add radiology specific prompt
        additional_prompt = """
As a Radiologist, I specialize in:
- Medical imaging interpretation (X-rays, CT, MRI, ultrasound)
- Diagnostic radiology and imaging-guided procedures
- Radiation safety and appropriate imaging protocols
- Interventional radiology procedures
- Screening and diagnostic imaging recommendations

I will evaluate symptoms and recommend appropriate imaging studies for diagnosis.
"""
        
        # Get base analysis
        base_response = await self.analyze_symptoms(diagnosis_request)
        
        # Enhance with radiology specific insights
        enhanced_analysis = self._enhance_radiology_analysis(
            base_response, diagnosis_request
        )
        
        return enhanced_analysis
    
    def _enhance_radiology_analysis(
        self, 
        base_response: AgentResponse, 
        diagnosis_request: DiagnosisRequest
    ) -> AgentResponse:
        """Enhance analysis with radiology specific insights"""
        
        enhanced_recommendations = base_response.recommendations.copy()
        enhanced_tests = base_response.suggested_tests.copy()
        
        # Add appropriate imaging studies based on symptoms
        imaging_studies = self._recommend_imaging_studies(diagnosis_request)
        enhanced_tests.extend(imaging_studies)
        
        # Add radiology specific recommendations
        enhanced_recommendations.extend([
            "Consult with a radiologist for imaging interpretation",
            "Ensure appropriate radiation safety measures",
            "Consider contrast studies if clinically indicated",
            "Follow up with referring physician for imaging results"
        ])
        
        # Add imaging protocol recommendations
        protocol_recommendations = self._get_imaging_protocols(diagnosis_request)
        enhanced_recommendations.extend(protocol_recommendations)
        
        # Create enhanced response
        return AgentResponse(
            agent_id=base_response.agent_id,
            specialty=base_response.specialty,
            analysis=base_response.analysis + "\n\nAs a radiologist, I've evaluated your symptoms and recommended appropriate imaging studies for accurate diagnosis.",
            recommendations=enhanced_recommendations,
            confidence=base_response.confidence,
            additional_questions=base_response.additional_questions,
            suggested_tests=enhanced_tests
        )
    
    def _recommend_imaging_studies(self, diagnosis_request: DiagnosisRequest) -> List[str]:
        """Recommend appropriate imaging studies based on symptoms"""
        imaging_studies = []
        
        for symptom in diagnosis_request.symptoms:
            symptom_text = f"{symptom.name} {symptom.description}".lower()
            
            # Chest symptoms
            if any(keyword in symptom_text for keyword in ["chest pain", "shortness of breath", "cough"]):
                imaging_studies.extend([
                    "Chest X-ray",
                    "Chest CT scan (if indicated)"
                ])
            
            # Head symptoms
            if any(keyword in symptom_text for keyword in ["headache", "head injury", "dizziness"]):
                imaging_studies.extend([
                    "Head CT scan",
                    "Brain MRI (if indicated)"
                ])
            
            # Abdominal symptoms
            if any(keyword in symptom_text for keyword in ["abdominal pain", "nausea", "vomiting"]):
                imaging_studies.extend([
                    "Abdominal ultrasound",
                    "Abdominal CT scan (if indicated)"
                ])
            
            # Back/spine symptoms
            if any(keyword in symptom_text for keyword in ["back pain", "spine", "numbness"]):
                imaging_studies.extend([
                    "Spine X-ray",
                    "Spine MRI (if indicated)"
                ])
            
            # Joint symptoms
            if any(keyword in symptom_text for keyword in ["joint pain", "swelling", "fracture"]):
                imaging_studies.extend([
                    "Joint X-ray",
                    "Joint MRI (if indicated)"
                ])
        
        # Remove duplicates
        return list(set(imaging_studies))
    
    def _get_imaging_protocols(self, diagnosis_request: DiagnosisRequest) -> List[str]:
        """Get imaging protocol recommendations"""
        protocols = []
        
        # Add general imaging protocols
        protocols.extend([
            "Ensure proper patient preparation for imaging studies",
            "Consider contrast administration if clinically indicated",
            "Follow ALARA principle (As Low As Reasonably Achievable) for radiation exposure"
        ])
        
        # Add specific protocols based on patient factors
        patient = diagnosis_request.patient_info
        
        if patient.age < 18:
            protocols.append("Use pediatric imaging protocols to minimize radiation exposure")
        
        if "pregnancy" in patient.medical_history or patient.gender.lower() == "female":
            protocols.append("Assess pregnancy status before any radiation exposure")
        
        return protocols 