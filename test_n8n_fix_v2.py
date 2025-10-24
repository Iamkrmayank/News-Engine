#!/usr/bin/env python3
"""
Test script to verify the n8n fix for generate-amp endpoint
This simulates the exact request that was failing in n8n
"""

import requests
import json

# Test the problematic n8n request
def test_n8n_problematic_request():
    """Test the exact request that was failing in n8n"""
    
    url = "http://localhost:8000/api/v1/generate-amp"
    
    # This is the exact request that was failing in n8n
    payload = {
        "amp_template_html": "string",  # This is what n8n sends
        "amp_template_url": "https://cdn.suvichaar.org/media/processed_html_20251024_184052.html",
        "output_json": {},  # Empty object
        "output_json_url": "https://cdn.suvichaar.org/media/processed_data_20251024_184052.json"
    }
    
    print("🧪 Testing problematic n8n request...")
    print(f"URL: {url}")
    print(f"Payload: {json.dumps(payload, indent=2)}")
    
    try:
        response = requests.post(url, json=payload, timeout=30)
        print(f"\n📊 Response Status: {response.status_code}")
        print(f"📊 Response Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ SUCCESS!")
            print(f"📄 Response: {json.dumps(result, indent=2)}")
            return True
        else:
            print(f"❌ FAILED!")
            print(f"📄 Error Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ EXCEPTION: {str(e)}")
        return False

def test_correct_request():
    """Test the correct way to make the request"""
    
    url = "http://localhost:8000/api/v1/generate-amp"
    
    # Correct request - only use URL, not both
    payload = {
        "amp_template_url": "https://cdn.suvichaar.org/media/processed_html_20251024_184052.html",
        "output_json_url": "https://cdn.suvichaar.org/media/processed_data_20251024_184052.json"
    }
    
    print("\n🧪 Testing correct request (URL only)...")
    print(f"URL: {url}")
    print(f"Payload: {json.dumps(payload, indent=2)}")
    
    try:
        response = requests.post(url, json=payload, timeout=30)
        print(f"\n📊 Response Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ SUCCESS!")
            print(f"📄 Response: {json.dumps(result, indent=2)}")
            return True
        else:
            print(f"❌ FAILED!")
            print(f"📄 Error Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ EXCEPTION: {str(e)}")
        return False

def test_health():
    """Test health endpoint first"""
    try:
        response = requests.get("http://localhost:8000/api/v1/health", timeout=10)
        if response.status_code == 200:
            print("✅ Health check passed")
            return True
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health check exception: {str(e)}")
        return False

if __name__ == "__main__":
    print("🚀 Testing n8n Fix for generate-amp endpoint")
    print("=" * 50)
    
    # Test health first
    if not test_health():
        print("❌ Server not ready, exiting")
        exit(1)
    
    print("\n" + "=" * 50)
    
    # Test problematic request (should now fail with clear error)
    problematic_result = test_n8n_problematic_request()
    
    print("\n" + "=" * 50)
    
    # Test correct request (should work)
    correct_result = test_correct_request()
    
    print("\n" + "=" * 50)
    print("📋 SUMMARY:")
    print(f"Problematic Request: {'✅ PASS (Clear Error)' if not problematic_result else '❌ FAIL (Should have failed)'}")
    print(f"Correct Request: {'✅ PASS' if correct_result else '❌ FAIL'}")
    
    if not problematic_result and correct_result:
        print("\n🎉 All tests passed! The fix is working correctly.")
    else:
        print("\n⚠️ Some tests failed. Check the output above.")
