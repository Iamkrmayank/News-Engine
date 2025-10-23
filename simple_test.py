"""
Simple test script for Suvichaar FastAPI Service
"""
import requests
import time
import sys

def test_service():
    """Test if the service is running"""
    base_url = "http://127.0.0.1:8000"
    
    print("Testing Suvichaar FastAPI Service...")
    print("=" * 50)
    
    # Test root endpoint
    try:
        response = requests.get(f"{base_url}/", timeout=5)
        print(f"SUCCESS Root endpoint: {response.status_code}")
        data = response.json()
        print(f"   Message: {data.get('message', 'N/A')}")
    except requests.exceptions.RequestException as e:
        print(f"ERROR Root endpoint failed: {e}")
        return False
    
    # Test health check
    try:
        response = requests.get(f"{base_url}/api/v1/health", timeout=5)
        print(f"SUCCESS Health check: {response.status_code}")
        data = response.json()
        print(f"   Status: {data.get('data', {}).get('status', 'N/A')}")
    except requests.exceptions.RequestException as e:
        print(f"ERROR Health check failed: {e}")
        return False
    
    # Test voice options
    try:
        response = requests.get(f"{base_url}/api/v1/voice-options", timeout=5)
        print(f"SUCCESS Voice options: {response.status_code}")
        data = response.json()
        print(f"   Available voices: {len(data.get('data', {}))}")
    except requests.exceptions.RequestException as e:
        print(f"ERROR Voice options failed: {e}")
        return False
    
    print("=" * 50)
    print("SUCCESS: All basic tests passed!")
    return True

if __name__ == "__main__":
    print("Starting service test...")
    print("Make sure the service is running on http://127.0.0.1:8000")
    print()
    
    # Wait a moment
    time.sleep(2)
    
    success = test_service()
    
    if success:
        print("\nSUCCESS: Service is working correctly!")
        print("Visit http://127.0.0.1:8000/docs for API documentation")
    else:
        print("\nERROR: Service is not responding")
        print("Please check if the service is running")
        sys.exit(1)
