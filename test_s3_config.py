#!/usr/bin/env python3
"""
Test S3 configuration and upload
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from app.services.s3_service import S3Service
from app.core.config import settings

def test_s3_config():
    """Test S3 configuration"""
    
    print("🧪 Testing S3 Configuration...")
    print("-" * 50)
    
    try:
        # Check environment variables
        print(f"🔍 AWS_ACCESS_KEY: {'Set' if settings.AWS_ACCESS_KEY else 'Not Set'}")
        print(f"🔍 AWS_SECRET_KEY: {'Set' if settings.AWS_SECRET_KEY else 'Not Set'}")
        print(f"🔍 AWS_REGION: {settings.AWS_REGION}")
        print(f"🔍 AWS_BUCKET: {settings.AWS_BUCKET}")
        print(f"🔍 CDN_BASE: {settings.CDN_BASE}")
        print(f"🔍 S3_PREFIX: {settings.S3_PREFIX}")
        
        # Test S3 service initialization
        s3_service = S3Service()
        print("✅ S3 service initialized successfully")
        
        # Test upload
        test_html = "<html><body><h1>Test</h1></body></html>"
        test_json = {"test": "data", "number": 123}
        
        html_url, json_url = s3_service.upload_processed_files(test_html, test_json, "test")
        
        print(f"✅ Upload successful!")
        print(f"🔗 HTML URL: {html_url}")
        print(f"🔗 JSON URL: {json_url}")
        
    except Exception as e:
        print(f"❌ S3 test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_s3_config()
