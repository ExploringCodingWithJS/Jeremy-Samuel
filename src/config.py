"""
Configuration settings for the Medical Diagnosis AI System
"""

import os
from typing import Dict, Any
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """Application settings"""
    
    # Google ADK Configuration
    GOOGLE_API_KEY: str = ""
    # Removed GOOGLE_PROJECT_ID and GOOGLE_LOCATION
    
    # Model Configuration
    PRIMARY_MODEL: str = "gemini-1.5-flash"  # Free, fast model
    TEMPERATURE: float = 0.3
    MAX_TOKENS: int = 4000
    
    # Development/Testing
    MOCK_MODE: bool = False  # Set to True to use mock responses when API quota is exceeded
    
    # Removed DATABASE_URL
    
    # API Configuration
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    DEBUG: bool = False
    
    # Removed MEDICAL_KB_PATH
    
    # Agent Configuration
    MAX_AGENTS: int = 10
    AGENT_TIMEOUT: int = 30
    
    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "./logs/medical_ai.log"
    
    class Config:
        env_file = ".env"

# Global settings instance
settings = Settings()

# Medical specialties configuration
MEDICAL_SPECIALTIES = {
    "general_physician": {
        "name": "General Physician",
        "description": "Primary care and general medical diagnosis",
        "expertise": ["general medicine", "primary care", "preventive medicine"],
        "model": "gemini-1.5-flash",
        "temperature": 0.2
    },
    "cardiology": {
        "name": "Cardiologist",
        "description": "Heart and cardiovascular system specialist",
        "expertise": ["cardiology", "heart disease", "cardiovascular health"],
        "model": "gemini-1.5-flash",
        "temperature": 0.2
    },
    "radiology": {
        "name": "Radiologist",
        "description": "Medical imaging and diagnostic radiology",
        "expertise": ["radiology", "medical imaging", "diagnostic imaging"],
        "model": "gemini-1.5-flash",
        "temperature": 0.2
    },
    "neurology": {
        "name": "Neurologist",
        "description": "Nervous system and brain specialist",
        "expertise": ["neurology", "brain disorders", "nervous system"],
        "model": "gemini-1.5-flash",
        "temperature": 0.2
    },
    "oncology": {
        "name": "Oncologist",
        "description": "Cancer diagnosis and treatment specialist",
        "expertise": ["oncology", "cancer", "tumor diagnosis"],
        "model": "gemini-1.5-flash",
        "temperature": 0.2
    },
    "pediatrics": {
        "name": "Pediatrician",
        "description": "Children's health and development specialist",
        "expertise": ["pediatrics", "child health", "developmental medicine"],
        "model": "gemini-1.5-flash",
        "temperature": 0.2
    },
    "psychiatry": {
        "name": "Psychiatrist",
        "description": "Mental health and behavioral disorders specialist",
        "expertise": ["psychiatry", "mental health", "behavioral disorders"],
        "model": "gemini-1.5-flash",
        "temperature": 0.2
    }
}

# Symptom to specialty mapping
SYMPTOM_SPECIALTY_MAPPING = {
    "chest pain": ["cardiology", "general_physician"],
    "heart palpitations": ["cardiology"],
    "shortness of breath": ["cardiology", "general_physician"],
    "headache": ["neurology", "general_physician"],
    "dizziness": ["neurology", "cardiology", "general_physician"],
    "numbness": ["neurology", "general_physician"],
    "cough": ["general_physician"],
    "fever": ["general_physician"],
    "fatigue": ["general_physician"],
    "abdominal pain": ["general_physician"],
    "nausea": ["general_physician"],
    "vomiting": ["general_physician"],
    "diarrhea": ["general_physician"],
    "constipation": ["general_physician"],
    "back pain": ["general_physician"],
    "joint pain": ["general_physician"],
    "skin rash": ["general_physician"],
    "vision problems": ["neurology", "general_physician"],
    "hearing problems": ["general_physician"],
    "memory problems": ["neurology", "psychiatry", "general_physician"],
    "mood changes": ["psychiatry", "general_physician"],
    "anxiety": ["psychiatry", "general_physician"],
    "depression": ["psychiatry", "general_physician"],
    "weight loss": ["general_physician", "oncology"],
    "weight gain": ["general_physician"],
    "swelling": ["general_physician"],
    "bleeding": ["general_physician"],
    "lump": ["general_physician", "oncology"],
    "cancer": ["oncology"],
    "tumor": ["oncology"],
    "child symptoms": ["pediatrics"],
    "developmental issues": ["pediatrics"],
    "behavioral problems": ["pediatrics", "psychiatry"]
} 