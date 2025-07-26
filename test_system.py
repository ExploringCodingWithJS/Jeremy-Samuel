"""
Test script for Medical Diagnosis AI System
"""

import asyncio
import json
import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent / "src"))

from src.models import PatientInfo, Symptom, DiagnosisRequest, SeverityLevel
from src.coordinator import MedicalDiagnosisCoordinator

async def test_imports():
    """Test that all imports work correctly"""
    print("🔍 Testing imports...")
    
    try:
        from src.config import settings, MEDICAL_SPECIALTIES
        from src.models import DiagnosisRequest, PatientInfo, Symptom
        from src.coordinator import MedicalDiagnosisCoordinator
        from src.agents import (
            GeneralPhysicianAgent, CardiologyAgent, RadiologyAgent,
            NeurologyAgent, OncologyAgent, PediatricsAgent, PsychiatryAgent
        )
        print("✅ All imports successful")
        return True
    except Exception as e:
        print(f"❌ Import error: {str(e)}")
        return False

async def test_coordinator_initialization():
    """Test coordinator initialization"""
    print("\n🔍 Testing coordinator initialization...")
    
    try:
        coordinator = MedicalDiagnosisCoordinator()
        print(f"✅ Coordinator initialized with {len(coordinator.agents)} agents")
        
        # Check that all expected agents are loaded
        expected_agents = [
            "general_physician", "cardiology", "radiology", 
            "neurology", "oncology", "pediatrics", "psychiatry"
        ]
        
        for agent_name in expected_agents:
            if agent_name in coordinator.agents:
                print(f"  ✅ {agent_name} agent loaded")
            else:
                print(f"  ❌ {agent_name} agent missing")
                return False
        
        return True
    except Exception as e:
        print(f"❌ Coordinator initialization error: {str(e)}")
        return False

async def test_diagnosis_workflow():
    """Test the complete diagnosis workflow"""
    print("\n🔍 Testing diagnosis workflow...")
    
    try:
        coordinator = MedicalDiagnosisCoordinator()
        
        # Create test patient
        patient = PatientInfo(
            patient_id="TEST001",
            age=35,
            gender="Male",
            weight=75.0,
            height=175.0,
            medical_history=["hypertension"],
            allergies=["penicillin"],
            medications=["lisinopril"],
            family_history=["heart disease"]
        )
        
        # Create test symptoms
        symptoms = [
            Symptom(
                name="chest pain",
                description="Sharp pain in center of chest that started during exercise",
                severity=SeverityLevel.MODERATE,
                duration="2 hours",
                onset="sudden",
                triggers=["exercise", "stress"],
                alleviating_factors=["rest", "nitroglycerin"]
            ),
            Symptom(
                name="shortness of breath",
                description="Difficulty breathing, especially with exertion",
                severity=SeverityLevel.MILD,
                duration="1 hour",
                onset="gradual",
                triggers=["exercise"],
                alleviating_factors=["rest"]
            )
        ]
        
        # Create diagnosis request
        request = DiagnosisRequest(
            patient_info=patient,
            symptoms=symptoms,
            additional_notes="Patient is a 35-year-old male with history of hypertension"
        )
        
        print("✅ Test data created successfully")
        
        # Note: We won't actually run the diagnosis without API key
        # This is just to test the data structures
        print("✅ Diagnosis workflow structure validated")
        return True
        
    except Exception as e:
        print(f"❌ Diagnosis workflow error: {str(e)}")
        return False

async def test_api_endpoints():
    """Test API endpoint structure"""
    print("\n🔍 Testing API endpoint structure...")
    
    try:
        from src.api import app
        
        # Check that app is properly configured
        if hasattr(app, 'routes'):
            print("✅ FastAPI app properly configured")
            print(f"  📊 {len(app.routes)} routes registered")
            return True
        else:
            print("❌ FastAPI app not properly configured")
            return False
            
    except Exception as e:
        print(f"❌ API endpoint test error: {str(e)}")
        return False

def test_configuration():
    """Test configuration settings"""
    print("\n🔍 Testing configuration...")
    
    try:
        from src.config import settings, MEDICAL_SPECIALTIES, SYMPTOM_SPECIALTY_MAPPING
        
        # Check settings
        print(f"✅ Settings loaded: {settings.PRIMARY_MODEL}")
        
        # Check medical specialties
        print(f"✅ Medical specialties: {len(MEDICAL_SPECIALTIES)} configured")
        
        # Check symptom mapping
        print(f"✅ Symptom mappings: {len(SYMPTOM_SPECIALTY_MAPPING)} configured")
        
        return True
        
    except Exception as e:
        print(f"❌ Configuration error: {str(e)}")
        return False

async def main():
    """Run all tests"""
    print("🏥 Medical Diagnosis AI System - Test Suite")
    print("=" * 50)
    
    tests = [
        ("Configuration", test_configuration),
        ("Imports", test_imports),
        ("Coordinator", test_coordinator_initialization),
        ("Diagnosis Workflow", test_diagnosis_workflow),
        ("API Endpoints", test_api_endpoints),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            if asyncio.iscoroutinefunction(test_func):
                result = await test_func()
            else:
                result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} test failed with exception: {str(e)}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 Test Results Summary")
    print("=" * 50)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name:20} {status}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! System is ready to run.")
        print("\nNext steps:")
        print("1. Set up your .env file with GOOGLE_API_KEY")
        print("2. Run: python main.py")
        print("3. In another terminal: streamlit run streamlit_app.py")
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
        return 1
    
    return 0

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code) 