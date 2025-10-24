#!/usr/bin/env python3
"""
Test script for the updated /api/v1/process-html endpoint with S3 upload
"""

import requests
import json

def test_process_html_with_s3():
    """Test the process-html endpoint with S3 upload"""
    
    # Sample test data
    test_data = {
        "html_template": """<!DOCTYPE html>
<html>
<head>
    <title>{{title}}</title>
</head>
<body>
    <h1>{{title}}</h1>
    <p>{{content}}</p>
</body>
</html>""",
        "full_slide_json": {
            "title": "Test Story",
            "content": "This is a test content for the story.",
            "slide1": {
                "s1paragraph1": "First slide content",
                "audio_url1": "https://example.com/audio1.mp3"
            },
            "slide2": {
                "s2paragraph1": "Second slide content", 
                "audio_url2": "https://example.com/audio2.mp3"
            }
        }
    }
    
    # API endpoint
    url = "http://localhost:8000/api/v1/process-html"
    
    print("🧪 Testing process-html endpoint with S3 upload...")
    print(f"📡 URL: {url}")
    print(f"📊 Data keys: {list(test_data.keys())}")
    print("-" * 50)
    
    try:
        # Make the request
        response = requests.post(url, json=test_data, timeout=30)
        
        print(f"📈 Status Code: {response.status_code}")
        print(f"📋 Response Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ SUCCESS!")
            print(f"📄 Updated HTML Length: {len(result.get('updated_html', ''))}")
            print(f"📊 Updated JSON Keys: {list(result.get('updated_json', {}).keys())}")
            print(f"📁 Filename: {result.get('filename', 'N/A')}")
            print(f"🔗 HTML S3 URL: {result.get('html_s3_url', 'N/A')}")
            print(f"🔗 JSON S3 URL: {result.get('json_s3_url', 'N/A')}")
            
            # Check if S3 URLs are provided
            if result.get('html_s3_url') and result.get('json_s3_url'):
                print("✅ S3 upload successful - CloudFront URLs provided")
            else:
                print("⚠️  S3 upload failed or URLs not provided")
                
        else:
            print("❌ FAILED!")
            print(f"📄 Error Response: {response.text}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

if __name__ == "__main__":
    test_process_html_with_s3()
