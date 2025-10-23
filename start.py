#!/usr/bin/env python3
"""
Startup script for Suvichaar FastAPI Service
"""
import os
import sys
import uvicorn
from pathlib import Path

# Add the app directory to Python path
app_dir = Path(__file__).parent / "app"
sys.path.insert(0, str(app_dir))

def main():
    """Main startup function"""
    print("Starting Suvichaar FastAPI Service...")
    print("API Documentation: http://localhost:8000/docs")
    print("ReDoc Documentation: http://localhost:8000/redoc")
    print("Health Check: http://localhost:8000/api/v1/health")
    print("-" * 50)
    
    # Check if .env file exists
    env_file = Path(__file__).parent / ".env"
    if not env_file.exists():
        print("Warning: .env file not found!")
        print("   Please copy env.example to .env and configure your credentials.")
        print("   The service will start but API calls may fail without proper configuration.")
        print("-" * 50)
    
    # Start the server
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )

if __name__ == "__main__":
    main()
