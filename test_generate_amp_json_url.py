#!/usr/bin/env python3
"""
Test script for the updated /api/v1/generate-amp endpoint with JSON URL support
"""

import requests
import json

def test_generate_amp_with_json_url():
    """Test the generate-amp endpoint with JSON URL"""
    
    # Test data with JSON URL instead of JSON data
    test_data = {
        "amp_template_html": """<!DOCTYPE html>
<html amp lang="en">
<head>
    <meta charset="utf-8">
    <title>Suvichaar Story</title>
    <script async src="https://cdn.ampproject.org/v0.js"></script>
    <script async custom-element="amp-story" src="https://cdn.ampproject.org/v0/amp-story-1.0.js"></script>
    <script async custom-element="amp-audio" src="https://cdn.ampproject.org/v0/amp-audio-0.1.js"></script>
</head>
<body>
    <amp-story standalone>
        <!--INSERT_SLIDES_HERE-->
    </amp-story>
</body>
</html>""",
        "output_json_url": "https://cdn.suvichaar.org/media/processed_html_20251024_204530.json"
    }
    
    # API endpoint
    url = "http://localhost:8000/api/v1/generate-amp"
    
    print("🧪 Testing generate-amp endpoint with JSON URL...")
    print(f"📡 URL: {url}")
    print(f"📊 Template: {'Provided' if test_data.get('amp_template_html') else 'Not provided'}")
    print(f"🔗 JSON URL: {test_data.get('output_json_url', 'Not provided')}")
    print("-" * 50)
    
    try:
        # Make the request
        response = requests.post(url, json=test_data, timeout=30)
        
        print(f"📈 Status Code: {response.status_code}")
        print(f"📋 Response Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ SUCCESS!")
            print(f"📄 Final HTML Length: {len(result.get('final_html', ''))}")
            print(f"📁 Filename: {result.get('filename', 'N/A')}")
            
            # Check if HTML contains slides
            html_content = result.get('final_html', '')
            if 'amp-story-page' in html_content:
                print("✅ AMP story pages found in HTML")
            else:
                print("⚠️  No AMP story pages found in HTML")
                
        else:
            print("❌ FAILED!")
            print(f"📄 Error Response: {response.text}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

def test_generate_amp_with_json_data():
    """Test the generate-amp endpoint with JSON data (backward compatibility)"""
    
    # Test data with JSON data instead of JSON URL
    test_data = {
        "amp_template_html": """<!DOCTYPE html>
<html amp lang="en">
<head>
    <meta charset="utf-8">
    <title>Suvichaar Story</title>
    <script async src="https://cdn.ampproject.org/v0.js"></script>
    <script async custom-element="amp-story" src="https://cdn.ampproject.org/v0/amp-story-1.0.js"></script>
    <script async custom-element="amp-audio" src="https://cdn.ampproject.org/v0/amp-audio-0.1.js"></script>
</head>
<body>
    <amp-story standalone>
        <!--INSERT_SLIDES_HERE-->
    </amp-story>
</body>
</html>""",
        "output_json": {
            "slide3": {
                "s3paragraph1": "Test slide content",
                "audio_url3": "https://example.com/audio3.mp3"
            },
            "slide4": {
                "s4paragraph1": "Another test slide",
                "audio_url4": "https://example.com/audio4.mp3"
            }
        }
    }
    
    # API endpoint
    url = "http://localhost:8000/api/v1/generate-amp"
    
    print("\n🧪 Testing generate-amp endpoint with JSON data (backward compatibility)...")
    print(f"📡 URL: {url}")
    print(f"📊 Template: {'Provided' if test_data.get('amp_template_html') else 'Not provided'}")
    print(f"📊 JSON Data: {'Provided' if test_data.get('output_json') else 'Not provided'}")
    print("-" * 50)
    
    try:
        # Make the request
        response = requests.post(url, json=test_data, timeout=30)
        
        print(f"📈 Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ SUCCESS!")
            print(f"📄 Final HTML Length: {len(result.get('final_html', ''))}")
            print(f"📁 Filename: {result.get('filename', 'N/A')}")
            
            # Check if HTML contains slides
            html_content = result.get('final_html', '')
            if 'amp-story-page' in html_content:
                print("✅ AMP story pages found in HTML")
            else:
                print("⚠️  No AMP story pages found in HTML")
                
        else:
            print("❌ FAILED!")
            print(f"📄 Error Response: {response.text}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

if __name__ == "__main__":
    test_generate_amp_with_json_url()
    test_generate_amp_with_json_data()
