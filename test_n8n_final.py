#!/usr/bin/env python3
"""
Test script to verify the n8n fix for generate-amp endpoint
This simulates the exact request that was failing in n8n
"""

import requests
import json

def test_n8n_exact_request():
    """Test the exact request that was failing in n8n"""
    
    url = "http://localhost:8000/api/v1/generate-amp"
    
    # This is the exact request that was failing in n8n
    payload = {
        "amp_template_html": "",  # Empty string from n8n
        "amp_template_url": "https://cdn.suvichaar.org/media/processed_html_20251024_194615.html",
        "output_json": "",  # Empty string from n8n
        "output_json_url": "https://cdn.suvichaar.org/media/processed_html_20251024_194615.json"
    }
    
    print("🧪 Testing exact n8n request with empty strings...")
    print(f"URL: {url}")
    print(f"Payload: {json.dumps(payload, indent=2)}")
    
    try:
        response = requests.post(url, json=payload, timeout=30)
        print(f"\n📊 Response Status: {response.status_code}")
        print(f"📊 Response Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ SUCCESS!")
            print(f"📄 Response keys: {list(result.keys())}")
            print(f"📄 Final HTML length: {len(result.get('final_html', ''))}")
            return True
        else:
            print(f"❌ FAILED!")
            print(f"📄 Error Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ EXCEPTION: {str(e)}")
        return False

def test_urls_only():
    """Test with only URLs (recommended approach)"""
    
    url = "http://localhost:8000/api/v1/generate-amp"
    
    payload = {
        "amp_template_url": "https://cdn.suvichaar.org/media/processed_html_20251024_194615.html",
        "output_json_url": "https://cdn.suvichaar.org/media/processed_html_20251024_194615.json"
    }
    
    print("\n🧪 Testing with URLs only (recommended)...")
    print(f"URL: {url}")
    print(f"Payload: {json.dumps(payload, indent=2)}")
    
    try:
        response = requests.post(url, json=payload, timeout=30)
        print(f"\n📊 Response Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ SUCCESS!")
            print(f"📄 Response keys: {list(result.keys())}")
            print(f"📄 Final HTML length: {len(result.get('final_html', ''))}")
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
    print("=" * 60)
    
    # Test health first
    if not test_health():
        print("❌ Server not ready, exiting")
        exit(1)
    
    print("\n" + "=" * 60)
    
    # Test exact n8n request (should now work with empty strings)
    n8n_result = test_n8n_exact_request()
    
    print("\n" + "=" * 60)
    
    # Test URLs only (recommended approach)
    urls_result = test_urls_only()
    
    print("\n" + "=" * 60)
    print("📋 SUMMARY:")
    print(f"n8n Exact Request: {'✅ PASS' if n8n_result else '❌ FAIL'}")
    print(f"URLs Only Request: {'✅ PASS' if urls_result else '❌ FAIL'}")
    
    if n8n_result and urls_result:
        print("\n🎉 All tests passed! Ready for Docker push.")
    else:
        print("\n⚠️ Some tests failed. Check the output above.")
