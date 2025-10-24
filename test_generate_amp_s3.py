#!/usr/bin/env python3
"""
Test script for the updated /api/v1/generate-amp endpoint with S3 upload
"""

import requests
import json

def test_generate_amp_with_s3():
    """Test the generate-amp endpoint with S3 upload"""
    
    # Test data with JSON data
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
                "s3paragraph1": "Test slide content for AMP story",
                "audio_url3": "https://example.com/audio3.mp3"
            },
            "slide4": {
                "s4paragraph1": "Another test slide for AMP story",
                "audio_url4": "https://example.com/audio4.mp3"
            }
        }
    }
    
    # API endpoint
    url = "http://localhost:8000/api/v1/generate-amp"
    
    print("🧪 Testing generate-amp endpoint with S3 upload...")
    print(f"📡 URL: {url}")
    print(f"📊 Template: {'Provided' if test_data.get('amp_template_html') else 'Not provided'}")
    print(f"📊 JSON Data: {'Provided' if test_data.get('output_json') else 'Not provided'}")
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
            print(f"🔗 HTML S3 URL: {result.get('html_s3_url', 'N/A')}")
            
            # Check if S3 URL is provided
            if result.get('html_s3_url'):
                print("✅ S3 upload successful - CloudFront URL provided")
            else:
                print("⚠️  S3 upload failed or URL not provided")
            
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

def test_generate_amp_download_with_s3():
    """Test the generate-amp-download endpoint with S3 upload"""
    
    # Test data with JSON data
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
                "s3paragraph1": "Test slide content for AMP download",
                "audio_url3": "https://example.com/audio3.mp3"
            },
            "slide4": {
                "s4paragraph1": "Another test slide for AMP download",
                "audio_url4": "https://example.com/audio4.mp3"
            }
        }
    }
    
    # API endpoint
    url = "http://localhost:8000/api/v1/generate-amp-download"
    
    print("\n🧪 Testing generate-amp-download endpoint with S3 upload...")
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
            print(f"🔗 Download URL: {result.get('download_url', 'N/A')}")
            print(f"🔗 HTML S3 URL: {result.get('html_s3_url', 'N/A')}")
            
            # Check if S3 URL is provided
            if result.get('html_s3_url'):
                print("✅ S3 upload successful - CloudFront URL provided")
            else:
                print("⚠️  S3 upload failed or URL not provided")
            
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
    test_generate_amp_with_s3()
    test_generate_amp_download_with_s3()
