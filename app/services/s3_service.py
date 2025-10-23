"""
S3 Service for Suvichaar FastAPI Service
"""
import os
import uuid
import json
import base64
import requests
import boto3
import random
import string
from typing import Dict, Any, Optional
from urllib.parse import urlparse
from datetime import datetime, timezone
from app.core.config import settings


class S3Service:
    """Service for S3 operations"""
    
    def __init__(self):
        self.s3_client = boto3.client(
            "s3",
            aws_access_key_id=settings.AWS_ACCESS_KEY,
            aws_secret_access_key=settings.AWS_SECRET_KEY,
            region_name=settings.AWS_REGION,
        )
        self.bucket = settings.AWS_BUCKET
        self.s3_prefix = settings.S3_PREFIX
        self.cdn_base = settings.CDN_BASE
        self.cdn_prefix_media = settings.CDN_PREFIX_MEDIA
    
    def upload_file(self, file_content: bytes, filename: str, content_type: str = "application/octet-stream") -> str:
        """Upload file to S3 and return CDN URL"""
        try:
            s3_key = f"{self.s3_prefix}{filename}"
            self.s3_client.put_object(
                Bucket=self.bucket,
                Key=s3_key,
                Body=file_content,
                ContentType=content_type,
            )
            return f"{self.cdn_base}{s3_key}"
        except Exception as e:
            raise Exception(f"S3 upload failed: {str(e)}")
    
    def upload_html_story(self, html_content: str, slug: str) -> str:
        """Upload HTML story to S3"""
        try:
            s3_key = f"{slug}.html"
            self.s3_client.put_object(
                Bucket="suvichaarstories",
                Key=s3_key,
                Body=html_content.encode("utf-8"),
                ContentType="text/html",
            )
            return f"https://suvichaarstories.s3.amazonaws.com/{s3_key}"
        except Exception as e:
            raise Exception(f"HTML upload failed: {str(e)}")
    
    def upload_metadata(self, metadata: Dict[str, Any], slug: str) -> str:
        """Upload metadata JSON to S3"""
        try:
            s3_key = f"{slug}_metadata.json"
            json_content = json.dumps(metadata, indent=2, ensure_ascii=False)
            self.s3_client.put_object(
                Bucket="suvichaarstories",
                Key=s3_key,
                Body=json_content.encode("utf-8"),
                ContentType="application/json",
            )
            return f"https://suvichaarstories.s3.amazonaws.com/{s3_key}"
        except Exception as e:
            raise Exception(f"Metadata upload failed: {str(e)}")
    
    def upload_image_from_url(self, image_url: str) -> str:
        """Download image from URL and upload to S3"""
        try:
            response = requests.get(image_url, timeout=10)
            response.raise_for_status()
            
            filename = os.path.basename(urlparse(image_url).path)
            ext = os.path.splitext(filename)[1].lower()
            if ext not in [".jpg", ".jpeg", ".png", ".gif"]:
                ext = ".jpg"
            
            unique_filename = f"{uuid.uuid4().hex}{ext}"
            s3_key = f"{self.s3_prefix}{unique_filename}"
            
            self.s3_client.put_object(
                Bucket=self.bucket,
                Key=s3_key,
                Body=response.content,
                ContentType=response.headers.get("Content-Type", "image/jpeg"),
            )
            
            return f"{self.cdn_base}{s3_key}"
            
        except Exception as e:
            raise Exception(f"Image upload failed: {str(e)}")
    
    def generate_slug_and_urls(self, title: str) -> tuple:
        """Generate slug and URLs from title"""
        if not title or not isinstance(title, str):
            raise ValueError("Invalid title")
        
        slug = ''.join(c for c in title.lower().replace(" ", "-").replace("_", "-") 
                      if c in string.ascii_lowercase + string.digits + '-')
        slug = slug.strip('-')
        nano = ''.join(random.choices(string.ascii_letters + string.digits + '_-', k=10)) + '_G'
        slug_nano = f"{slug}_{nano}"
        
        return nano, slug_nano, f"https://suvichaar.org/stories/{slug_nano}", f"https://stories.suvichaar.org/{slug_nano}.html"
    
    def generate_resized_image_urls(self, image_url: str) -> Dict[str, str]:
        """Generate resized image URLs using CDN"""
        if not image_url.startswith("http://media.suvichaar.org") and not image_url.startswith("https://media.suvichaar.org"):
            return {}
        
        parsed_cdn_url = urlparse(image_url)
        cdn_key_path = parsed_cdn_url.path.lstrip("/")
        
        resize_presets = {
            "potraitcoverurl": (640, 853),
            "msthumbnailcoverurl": (300, 300),
        }
        
        resized_urls = {}
        for label, (width, height) in resize_presets.items():
            template = {
                "bucket": self.bucket,
                "key": cdn_key_path,
                "edits": {
                    "resize": {
                        "width": width,
                        "height": height,
                        "fit": "cover"
                    }
                }
            }
            encoded = base64.urlsafe_b64encode(json.dumps(template).encode()).decode()
            final_url = f"{self.cdn_prefix_media}{encoded}"
            resized_urls[label] = final_url
        
        return resized_urls
    
    def generate_thumbnail(self, json_data: Dict[str, Any]) -> bytes:
        """Generate thumbnail using external API"""
        try:
            resp = requests.post(
                "https://remotion.suvichaar.org/api/generate-news-thumbnail",
                json=json_data,
                timeout=30
            )
            resp.raise_for_status()
            return resp.content
        except Exception as e:
            raise Exception(f"Thumbnail generation failed: {str(e)}")
    
    def upload_thumbnail(self, thumbnail_bytes: bytes) -> str:
        """Upload thumbnail to S3"""
        try:
            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            key = f"{self.s3_prefix}cover_{ts}.png"
            
            self.s3_client.put_object(
                Bucket=self.bucket,
                Key=key,
                Body=thumbnail_bytes,
                ContentType="image/png",
            )
            
            return f"{self.cdn_prefix_media}{key}"
        except Exception as e:
            raise Exception(f"Thumbnail upload failed: {str(e)}")
