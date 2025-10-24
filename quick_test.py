#!/usr/bin/env python3
import requests
import json

# Test with working URLs
def test_with_working_urls():
    url = "http://localhost:8000/api/v1/generate-amp"
    
    payload = {
        "amp_template_url": "https://httpbin.org/html",  # Working URL
        "output_json_url": "https://httpbin.org/json"    # Working URL
    }
    
    print("🧪 Testing with working URLs...")
    try:
        response = requests.post(url, json=payload, timeout=30)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            print("✅ SUCCESS!")
        else:
            print(f"❌ Error: {response.text}")
    except Exception as e:
        print(f"❌ Exception: {e}")

if __name__ == "__main__":
    test_with_working_urls()
