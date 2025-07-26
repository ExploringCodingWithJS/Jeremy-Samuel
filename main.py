"""
Main entry point for Medical Diagnosis AI System
"""

import asyncio
import logging
import os
import sys
from pathlib import Path

# Ensure logs directory exists before logging is configured
os.makedirs("logs", exist_ok=True)

# Add src to path
sys.path.append(str(Path(__file__).parent / "src"))

from src.api import app
from src.config import settings

def setup_logging():
    """Setup logging configuration"""
    # Create logs directory if it doesn't exist
    log_dir = Path(settings.LOG_FILE).parent
    log_dir.mkdir(parents=True, exist_ok=True)
    
    logging.basicConfig(
        level=getattr(logging, settings.LOG_LEVEL),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(settings.LOG_FILE),
            logging.StreamHandler()
        ]
    )

def check_environment():
    """Check if required environment variables are set"""
    if not settings.GOOGLE_API_KEY:
        print("WARNING: GOOGLE_API_KEY not set. Please set it in your .env file.")
        print("You can get an API key from: https://makersuite.google.com/app/apikey")
        return False
    return True

def main():
    """Main application entry point"""
    print("🏥 Medical Diagnosis AI System")
    print("=" * 50)
    
    # Setup logging
    setup_logging()
    logger = logging.getLogger(__name__)
    
    # Check environment
    if not check_environment():
        logger.warning("Environment not properly configured")
    
    logger.info("Starting Medical Diagnosis AI System")
    
    # Import and run the FastAPI app
    import uvicorn
    
    try:
        uvicorn.run(
            "src.api:app",
            host=settings.API_HOST,
            port=settings.API_PORT,
            reload=settings.DEBUG,
            log_level=settings.LOG_LEVEL.lower()
        )
    except KeyboardInterrupt:
        logger.info("Application stopped by user")
    except Exception as e:
        logger.error(f"Application error: {str(e)}")
        raise

if __name__ == "__main__":
    main() 