"""
Simple startup script for Suvichaar FastAPI Service
"""
import uvicorn
import sys
from pathlib import Path

# Add the app directory to Python path
app_dir = Path(__file__).parent / "app"
sys.path.insert(0, str(app_dir))

def main():
    """Main startup function"""
    print("Starting Suvichaar FastAPI Service...")
    print("API Documentation: http://127.0.0.1:8000/docs")
    print("Health Check: http://127.0.0.1:8000/api/v1/health")
    print("-" * 50)
    
    # Start the server
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
        log_level="info"
    )

if __name__ == "__main__":
    main()
