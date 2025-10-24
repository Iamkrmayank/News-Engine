#!/usr/bin/env python3
"""
Test script for the modified generate-amp-download endpoint
"""
import requests
import json
import os
import time

# Configuration
BASE_URL = "http://localhost:8000"
API_ENDPOINT = f"{BASE_URL}/api/v1/generate-amp-download"

def test_generate_amp_download():
    """Test the generate-amp-download endpoint with both HTML content and download URL"""
    
    # Create a simple AMP template for testing
    amp_template = """
    <!DOCTYPE html>
    <html ⚡>
    <head>
        <meta charset="utf-8">
        <title>{{storytitle}}</title>
        <link rel="canonical" href="{{canonicalurl}}">
        <meta name="viewport" content="width=device-width,minimum-scale=1,initial-scale=1">
        <script type="application/ld+json">
        {
            "@context": "http://schema.org",
            "@type": "NewsArticle",
            "headline": "{{storytitle}}",
            "author": {
                "@type": "Person",
                "name": "{{author}}"
            },
            "datePublished": "{{publishedtime}}",
            "image": "{{image0}}"
        }
        </script>
        <style amp-boilerplate>body{-webkit-animation:-amp-start 8s steps(1,end) 0s 1 normal both;-moz-animation:-amp-start 8s steps(1,end) 0s 1 normal both;-ms-animation:-amp-start 8s steps(1,end) 0s 1 normal both;animation:-amp-start 8s steps(1,end) 0s 1 normal both}@-webkit-keyframes -amp-start{from{visibility:hidden}to{visibility:visible}}@-moz-keyframes -amp-start{from{visibility:hidden}to{visibility:visible}}@-ms-keyframes -amp-start{from{visibility:hidden}to{visibility:visible}}@-o-keyframes -amp-start{from{visibility:hidden}to{visibility:visible}}@keyframes -amp-start{from{visibility:hidden}to{visibility:visible}}</style><noscript><style amp-boilerplate>body{-webkit-animation:none;-moz-animation:none;-ms-animation:none;animation:none}</style></noscript>
        <script async src="https://cdn.ampproject.org/v0.js"></script>
    </head>
    <body>
        <h1>{{storytitle}}</h1>
        <p>{{storydescription}}</p>
        <amp-img src="{{image0}}" width="600" height="400" layout="responsive" alt="Story Image"></amp-img>
        <!--INSERT_SLIDES_HERE-->
    </body>
    </html>
    """
    
    # Test data
    test_data = {
        "amp_template_html": amp_template,
        "output_json": {
            "slide1": {
                "s1paragraph1": "First slide content about Bengal politics and current developments",
                "audio_url1": "https://example.com/audio1.mp3"
            },
            "slide2": {
                "s2paragraph1": "Second slide about Bengal culture and traditional festivals",
                "audio_url2": "https://example.com/audio2.mp3"
            }
        }
    }
    
    try:
        print("Testing generate-amp-download endpoint...")
        print(f"Request data: {json.dumps(test_data, indent=2)}")
        
        # Make the request
        response = requests.post(API_ENDPOINT, json=test_data, timeout=30)
        
        print(f"\nResponse Status Code: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Success! Endpoint is working correctly.")
            response_data = response.json()
            print(f"Response: {json.dumps(response_data, indent=2)}")
            
            # Check if we have both HTML content and download URL
            if 'final_html' in response_data and 'download_url' in response_data:
                print("\n✅ Both HTML content and download URL are provided!")
                
                # Test the download URL
                download_url = f"{BASE_URL}{response_data['download_url']}"
                print(f"\nTesting download URL: {download_url}")
                
                download_response = requests.get(download_url)
                if download_response.status_code == 200:
                    print("✅ Download URL is working correctly!")
                    print(f"Downloaded file size: {len(download_response.content)} bytes")
                else:
                    print(f"❌ Download URL failed with status: {download_response.status_code}")
            else:
                print("❌ Missing HTML content or download URL in response")
        else:
            print("❌ Error occurred.")
            print(f"Response: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection error. Make sure the FastAPI server is running on localhost:8000")
    except requests.exceptions.Timeout:
        print("❌ Request timeout")
    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")

if __name__ == "__main__":
    test_generate_amp_download()
