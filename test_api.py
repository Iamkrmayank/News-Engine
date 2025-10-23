"""
Quick test script to verify the FastAPI service is working
"""
import requests
import json
import time

def test_api_endpoints():
    """Test basic API endpoints"""
    base_url = "http://localhost:8000"
    
    print("🧪 Testing Suvichaar FastAPI Service...")
    print("=" * 50)
    
    # Test root endpoint
    try:
        response = requests.get(f"{base_url}/")
        print(f"✅ Root endpoint: {response.status_code}")
        print(f"   Response: {response.json()['message']}")
    except Exception as e:
        print(f"❌ Root endpoint failed: {e}")
    
    print()
    
    # Test health check
    try:
        response = requests.get(f"{base_url}/api/v1/health")
        print(f"✅ Health check: {response.status_code}")
        data = response.json()
        print(f"   Status: {data['data']['status']}")
    except Exception as e:
        print(f"❌ Health check failed: {e}")
    
    print()
    
    # Test voice options
    try:
        response = requests.get(f"{base_url}/api/v1/voice-options")
        print(f"✅ Voice options: {response.status_code}")
        data = response.json()
        print(f"   Available voices: {len(data['data'])}")
    except Exception as e:
        print(f"❌ Voice options failed: {e}")
    
    print()
    
    # Test user mapping
    try:
        response = requests.get(f"{base_url}/api/v1/user-mapping")
        print(f"✅ User mapping: {response.status_code}")
        data = response.json()
        print(f"   Available users: {len(data['data'])}")
    except Exception as e:
        print(f"❌ User mapping failed: {e}")
    
    print()
    
    # Test category mapping
    try:
        response = requests.get(f"{base_url}/api/v1/category-mapping")
        print(f"✅ Category mapping: {response.status_code}")
        data = response.json()
        print(f"   Available categories: {len(data['data'])}")
    except Exception as e:
        print(f"❌ Category mapping failed: {e}")
    
    print()
    print("=" * 50)
    print("🎉 Basic API tests completed!")
    print("📚 Visit http://localhost:8000/docs for full API documentation")

def test_article_generation():
    """Test article generation with a sample URL"""
    base_url = "http://localhost:8000"
    
    print("\n🧪 Testing Article Generation...")
    print("=" * 50)
    
    try:
        response = requests.post(f"{base_url}/api/v1/generate-article", json={
            "url": "https://www.bbc.com/news",
            "persona": "genz",
            "content_language": "English",
            "number_of_slides": 5
        })
        
        if response.status_code == 200:
            print("✅ Article generation: SUCCESS")
            data = response.json()
            print(f"   Generated slides: {len(data['structured_output'])}")
            print(f"   Story title: {data['structured_output'].get('storytitle', 'N/A')[:50]}...")
        else:
            print(f"❌ Article generation failed: {response.status_code}")
            print(f"   Error: {response.text}")
            
    except Exception as e:
        print(f"❌ Article generation failed: {e}")

if __name__ == "__main__":
    print("🚀 Suvichaar FastAPI Service Test Suite")
    print("Make sure the service is running on http://localhost:8000")
    print()
    
    # Wait a moment for user to start the service
    input("Press Enter when the service is running...")
    
    # Run basic tests
    test_api_endpoints()
    
    # Ask if user wants to test article generation (requires API keys)
    print("\n" + "=" * 50)
    test_article = input("Test article generation? (requires API keys) [y/N]: ").lower()
    
    if test_article == 'y':
        test_article_generation()
    
    print("\n🎉 All tests completed!")
