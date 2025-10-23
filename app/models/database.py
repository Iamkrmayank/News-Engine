"""
Database models for Suvichaar FastAPI Service
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from datetime import datetime

Base = declarative_base()


class ContentGeneration(Base):
    """Model for tracking content generation requests"""
    __tablename__ = "content_generations"
    
    id = Column(Integer, primary_key=True, index=True)
    url = Column(String(500), nullable=False)
    persona = Column(String(50), nullable=False)
    content_language = Column(String(20), nullable=False)
    number_of_slides = Column(Integer, default=10)
    status = Column(String(20), default="pending")  # pending, processing, completed, failed
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    result_data = Column(JSON, nullable=True)
    error_message = Column(Text, nullable=True)


class TTSGeneration(Base):
    """Model for tracking TTS generation requests"""
    __tablename__ = "tts_generations"
    
    id = Column(Integer, primary_key=True, index=True)
    content_generation_id = Column(Integer, nullable=True)
    voice = Column(String(20), nullable=False)
    status = Column(String(20), default="pending")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    result_data = Column(JSON, nullable=True)
    error_message = Column(Text, nullable=True)


class PublishedStory(Base):
    """Model for tracking published stories"""
    __tablename__ = "published_stories"
    
    id = Column(Integer, primary_key=True, index=True)
    story_title = Column(String(200), nullable=False)
    slug = Column(String(100), unique=True, nullable=False)
    story_url = Column(String(500), nullable=False)
    html_url = Column(String(500), nullable=False)
    metadata_url = Column(String(500), nullable=True)
    cover_image_url = Column(String(500), nullable=True)
    category = Column(String(50), nullable=False)
    language = Column(String(10), nullable=False)
    status = Column(String(20), default="published")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    metadata = Column(JSON, nullable=True)


class FileUpload(Base):
    """Model for tracking file uploads"""
    __tablename__ = "file_uploads"
    
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String(200), nullable=False)
    file_url = Column(String(500), nullable=False)
    file_size = Column(Integer, nullable=False)
    content_type = Column(String(100), nullable=False)
    s3_key = Column(String(300), nullable=False)
    uploaded_at = Column(DateTime(timezone=True), server_default=func.now())
    is_active = Column(Boolean, default=True)


class APIUsage(Base):
    """Model for tracking API usage"""
    __tablename__ = "api_usage"
    
    id = Column(Integer, primary_key=True, index=True)
    endpoint = Column(String(100), nullable=False)
    method = Column(String(10), nullable=False)
    status_code = Column(Integer, nullable=False)
    response_time_ms = Column(Integer, nullable=False)
    user_agent = Column(String(500), nullable=True)
    ip_address = Column(String(45), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    request_data = Column(JSON, nullable=True)
    response_data = Column(JSON, nullable=True)
