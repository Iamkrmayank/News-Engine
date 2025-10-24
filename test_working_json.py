#!/usr/bin/env python3
import requests
import json

def test_with_working_json():
    url = "http://localhost:8000/api/v1/generate-amp"
    
    payload = {
        "amp_template_url": "https://cdn.suvichaar.org/media/processed_html_20251024_184052.html",  # This works
        "output_json_url": "https://httpbin.org/json"  # Working JSON URL
    }
    
    print("🧪 Testing with working JSON URL...")
    try:
        response = requests.post(url, json=payload, timeout=30)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print("✅ SUCCESS!")
            print(f"Response keys: {list(result.keys())}")
        else:
            print(f"❌ Error: {response.text}")
    except Exception as e:
        print(f"❌ Exception: {e}")

if __name__ == "__main__":
    test_with_working_json()
