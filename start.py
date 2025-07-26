#!/usr/bin/env python3
"""
Startup script for Medical Diagnosis AI System
"""

import os
import sys
import subprocess
import time
from pathlib import Path

def check_requirements():
    """Check if all requirements are met"""
    print("🔍 Checking requirements...")
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ required")
        return False
    
    # Check if .env exists
    if not Path(".env").exists():
        print("⚠️  .env file not found. Creating from template...")
        if Path("env.example").exists():
            subprocess.run(["cp", "env.example", ".env"])
            print("✅ .env file created. Please edit it with your Google API key.")
            return False
        else:
            print("❌ env.example not found")
            return False
    
    # Check if Google API key is set
    try:
        from dotenv import load_dotenv
        load_dotenv()
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key or api_key == "your_google_api_key_here":
            print("⚠️  Please set your Google API key in .env file")
            print("   Get one from: https://makersuite.google.com/app/apikey")
            return False
    except ImportError:
        print("⚠️  python-dotenv not installed. Install with: pip install python-dotenv")
        return False
    
    print("✅ Requirements check passed")
    return True

def install_dependencies():
    """Install required dependencies"""
    print("📦 Installing dependencies...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], check=True)
        print("✅ Dependencies installed")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install dependencies")
        return False

def test_system():
    """Test the system"""
    print("🧪 Testing system...")
    try:
        result = subprocess.run([sys.executable, "test_system.py"], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ System test passed")
            return True
        else:
            print("❌ System test failed")
            print(result.stdout)
            print(result.stderr)
            return False
    except Exception as e:
        print(f"❌ Test error: {str(e)}")
        return False

def start_system():
    """Start the medical diagnosis system"""
    print("🚀 Starting Medical Diagnosis AI System...")
    print("=" * 50)
    
    # Check requirements
    if not check_requirements():
        print("\n❌ Requirements not met. Please fix the issues above.")
        return False
    
    # Test system
    if not test_system():
        print("\n❌ System test failed. Please fix the issues above.")
        return False
    
    print("\n🎉 System ready! Starting services...")
    print("\n📋 Available commands:")
    print("  • API Server:     python main.py")
    print("  • Web Interface:  streamlit run streamlit_app.py")
    print("  • Test System:    python test_system.py")
    print("\n🌐 Access URLs:")
    print("  • Web Interface:  http://localhost:8501")
    print("  • API Docs:       http://localhost:8000/docs")
    print("  • Health Check:   http://localhost:8000/health")
    
    print("\n🚀 To start the system:")
    print("1. Terminal 1: python main.py")
    print("2. Terminal 2: streamlit run streamlit_app.py")
    
    return True

def main():
    """Main function"""
    print("🏥 Medical Diagnosis AI System")
    print("=" * 50)
    
    # Check if dependencies need to be installed
    try:
        import fastapi
        import streamlit
        import google.generativeai
    except ImportError:
        print("📦 Dependencies not found. Installing...")
        if not install_dependencies():
            print("❌ Failed to install dependencies")
            return 1
    
    # Start system
    if start_system():
        print("\n✅ System is ready to run!")
        return 0
    else:
        print("\n❌ System setup failed")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code) 