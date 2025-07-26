"""
Base agent class for medical specialists
"""

import asyncio
import logging
from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional
import google.generativeai as genai
from src.config import settings, MEDICAL_SPECIALTIES
from src.models import AgentResponse, DiagnosisRequest, Symptom

logger = logging.getLogger(__name__)

class BaseMedicalAgent(ABC):
    """Base class for all medical specialist agents"""
    
    def __init__(self, specialty: str, agent_id: str):
        self.specialty = specialty
        self.agent_id = agent_id
        self.config = MEDICAL_SPECIALTIES.get(specialty, {})
        self.name = self.config.get("name", specialty.title())
        self.description = self.config.get("description", "")
        self.expertise = self.config.get("expertise", [])
        self.model_name = self.config.get("model", settings.PRIMARY_MODEL)
        self.temperature = self.config.get("temperature", settings.TEMPERATURE)
        
        # Initialize Google Gemini
        genai.configure(api_key=settings.GOOGLE_API_KEY)
        self.model = genai.GenerativeModel(
            model_name=self.model_name,
            generation_config=genai.types.GenerationConfig(
                temperature=self.temperature,
                max_output_tokens=settings.MAX_TOKENS
            )
        )
        
        # System prompt for the agent
        self.system_prompt = self._create_system_prompt()
        
    def _create_system_prompt(self) -> str:
        """Create the system prompt for the agent"""
        return f"""You are {self.name}, a specialized medical AI agent with expertise in {', '.join(self.expertise)}.

Your role is to:
1. Analyze patient symptoms and medical history
2. Provide evidence-based medical insights
3. Suggest relevant diagnostic tests
4. Recommend appropriate specialists if needed
5. Communicate with empathy and clarity
6. Always prioritize patient safety

IMPORTANT GUIDELINES:
- You are an AI assistant, not a replacement for professional medical care
- Always recommend consulting with a qualified healthcare provider
- Be empathetic and supportive in your communication
- Provide clear, understandable explanations
- Include relevant disclaimers about AI limitations
- If symptoms suggest emergency conditions, clearly state the urgency

Your expertise areas: {', '.join(self.expertise)}

Respond in a structured format with:
1. Analysis of symptoms
2. Possible conditions to consider
3. Recommended diagnostic tests
4. Immediate actions if needed
5. Follow-up recommendations
6. Confidence level in your assessment
7. Additional questions to gather more information"""

    async def analyze_symptoms(self, diagnosis_request: DiagnosisRequest) -> AgentResponse:
        """Analyze symptoms and provide medical insights"""
        try:
            # Create the prompt for analysis
            prompt = self._create_analysis_prompt(diagnosis_request)
            
            # Get response from Gemini
            response = await self._get_ai_response(prompt)
            
            # Parse and structure the response
            agent_response = self._parse_ai_response(response, diagnosis_request)
            
            logger.info(f"Agent {self.agent_id} completed analysis for patient {diagnosis_request.patient_info.patient_id}")
            return agent_response
            
        except Exception as e:
            logger.error(f"Error in agent {self.agent_id} analysis: {str(e)}")
            return self._create_error_response(diagnosis_request)
    
    def _create_analysis_prompt(self, diagnosis_request: DiagnosisRequest) -> str:
        """Create the analysis prompt for the AI model"""
        patient = diagnosis_request.patient_info
        symptoms = diagnosis_request.symptoms
        
        prompt = f"""
{self.system_prompt}

PATIENT INFORMATION:
- Age: {patient.age}
- Gender: {patient.gender}
- Medical History: {', '.join(patient.medical_history) if patient.medical_history else 'None'}
- Allergies: {', '.join(patient.allergies) if patient.allergies else 'None'}
- Current Medications: {', '.join(patient.medications) if patient.medications else 'None'}

SYMPTOMS:
"""
        
        for symptom in symptoms:
            prompt += f"""
- {symptom.name}: {symptom.description}
  Severity: {symptom.severity}
  Duration: {symptom.duration}
  Onset: {symptom.onset}
  Triggers: {', '.join(symptom.triggers) if symptom.triggers else 'None'}
  Alleviating factors: {', '.join(symptom.alleviating_factors) if symptom.alleviating_factors else 'None'}
"""
        
        if diagnosis_request.additional_notes:
            prompt += f"\nADDITIONAL NOTES: {diagnosis_request.additional_notes}"
        
        prompt += f"""

Please provide your analysis as a {self.specialty} specialist. Focus on conditions within your area of expertise and provide actionable recommendations.

Respond in the following JSON format:
{{
    "analysis": "Your detailed analysis of the symptoms",
    "possible_conditions": ["condition1", "condition2"],
    "recommendations": ["recommendation1", "recommendation2"],
    "suggested_tests": ["test1", "test2"],
    "confidence": 0.85,
    "additional_questions": ["question1", "question2"],
    "urgency_level": "routine|urgent|emergency"
}}
"""
        
        return prompt
    
    async def _get_ai_response(self, prompt: str) -> str:
        """Get response from the AI model"""
        try:
            response = await asyncio.to_thread(
                self.model.generate_content,
                prompt
            )
            return response.text
        except Exception as e:
            logger.error(f"Error getting AI response: {str(e)}")
            raise
    
    def _parse_ai_response(self, response: str, diagnosis_request: DiagnosisRequest) -> AgentResponse:
        """Parse the AI response into structured format"""
        try:
            # Extract JSON from response if present
            import json
            import re
            
            # Try to find JSON in the response
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                parsed = json.loads(json_match.group())
            else:
                # Fallback to parsing the text response
                parsed = self._parse_text_response(response)
            
            return AgentResponse(
                agent_id=self.agent_id,
                specialty=self.specialty,
                analysis=parsed.get("analysis", response),
                recommendations=parsed.get("recommendations", []),
                confidence=parsed.get("confidence", 0.5),
                additional_questions=parsed.get("additional_questions", []),
                suggested_tests=parsed.get("suggested_tests", [])
            )
            
        except Exception as e:
            logger.error(f"Error parsing AI response: {str(e)}")
            return self._create_error_response(diagnosis_request)
    
    def _parse_text_response(self, response: str) -> Dict[str, Any]:
        """Parse text response when JSON is not available"""
        # Simple parsing of text response
        lines = response.split('\n')
        analysis = ""
        recommendations = []
        confidence = 0.5
        
        for line in lines:
            line = line.strip()
            if line.startswith("Recommendation:") or line.startswith("- "):
                recommendations.append(line.replace("Recommendation:", "").replace("- ", "").strip())
            elif "confidence" in line.lower():
                # Try to extract confidence score
                import re
                conf_match = re.search(r'(\d+\.?\d*)', line)
                if conf_match:
                    confidence = float(conf_match.group(1))
            else:
                analysis += line + "\n"
        
        return {
            "analysis": analysis.strip(),
            "recommendations": recommendations,
            "confidence": confidence,
            "additional_questions": [],
            "suggested_tests": []
        }
    
    def _create_error_response(self, diagnosis_request: DiagnosisRequest) -> AgentResponse:
        """Create an error response when analysis fails"""
        return AgentResponse(
            agent_id=self.agent_id,
            specialty=self.specialty,
            analysis="I apologize, but I encountered an error while analyzing your symptoms. Please try again or consult with a healthcare provider.",
            recommendations=["Consult with a healthcare provider for proper evaluation"],
            confidence=0.0,
            additional_questions=[],
            suggested_tests=[]
        )
    
    @abstractmethod
    async def specialized_analysis(self, diagnosis_request: DiagnosisRequest) -> AgentResponse:
        """Specialized analysis method to be implemented by each agent"""
        pass 