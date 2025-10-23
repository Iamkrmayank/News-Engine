"""
Configuration settings for Suvichaar FastAPI Service
"""
import os
from typing import Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings"""
    
    # API Settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Suvichaar Content Generator API"
    VERSION: str = "1.0.0"
    DESCRIPTION: str = "FastAPI service for Suvichaar web story content generation"
    
    # Azure OpenAI Settings
    AZURE_OPENAI_ENDPOINT: str
    AZURE_OPENAI_API_KEY: str
    AZURE_OPENAI_API_VERSION: str = "2024-02-01"
    AZURE_OPENAI_DEPLOYMENT_NAME: str = "gpt-4"
    
    # Azure Speech/TTS Settings
    AZURE_TTS_URL: str
    AZURE_API_KEY: str
    
    # AWS Settings
    AWS_ACCESS_KEY: str
    AWS_SECRET_KEY: str
    AWS_REGION: str = "us-east-1"
    AWS_BUCKET: str
    S3_PREFIX: str = "media/"
    CDN_BASE: str
    CDN_PREFIX_MEDIA: str = "https://media.suvichaar.org/"
    
    # Default Values
    DEFAULT_BG_IMAGE: str = "https://media.suvichaar.org/upload/polaris/polariscover.png"
    DEFAULT_COVER_IMAGE: str = "https://media.suvichaar.org/upload/polaris/polariscover.png"
    PIXEL_GIF_URL: str = "https://media.suvichaar.org/pixel.gif"
    
    # Voice Options
    VOICE_OPTIONS: dict = {
        "1": "alloy",
        "2": "echo", 
        "3": "fable",
        "4": "onyx",
        "5": "nova",
        "6": "shimmer"
    }
    
    # User Mapping
    USER_MAPPING: dict = {
        "Mayank": "https://www.instagram.com/iamkrmayank?igsh=eW82NW1qbjh4OXY2&utm_source=qr",
        "Onip": "https://www.instagram.com/onip.mathur/profilecard/?igsh=MW5zMm5qMXhybGNmdA==",
        "Naman": "https://njnaman.in/"
    }
    
    # Category Mapping
    CATEGORY_MAPPING: dict = {
        "Art": 1,
        "Travel": 2,
        "Entertainment": 3,
        "Literature": 4,
        "Books": 5,
        "Sports": 6,
        "History": 7,
        "Culture": 8,
        "Wildlife": 9,
        "Spiritual": 10,
        "Food": 11
    }
    
    # Default Filter Tags
    DEFAULT_FILTER_TAGS: list = [
        "Lata Mangeshkar",
        "Indian Music Legends",
        "Playback Singing",
        "Bollywood Golden Era",
        "Indian Cinema",
        "Musical Icons",
        "Voice of India",
        "Bharat Ratna",
        "Indian Classical Music",
        "Hindi Film Songs",
        "Legendary Singers",
        "Cultural Heritage",
        "Suvichaar Stories"
    ]
    
    # File Upload Settings
    MAX_FILE_SIZE: int = 10 * 1024 * 1024  # 10MB
    ALLOWED_FILE_TYPES: list = ["json", "html", "htm", "mp3", "png", "jpg", "jpeg"]
    
    # CORS Settings
    BACKEND_CORS_ORIGINS: list = [
        "http://localhost:3000",
        "http://localhost:8000",
        "http://localhost:8080",
        "https://localhost:3000",
        "https://localhost:8000",
        "https://localhost:8080",
    ]
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Global settings instance
settings = Settings()
