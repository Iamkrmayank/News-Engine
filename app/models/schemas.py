"""
Pydantic models for Suvichaar FastAPI Service
"""
from typing import List, Optional, Dict, Any, Union
from pydantic import BaseModel, Field, HttpUrl, model_validator
from enum import Enum


class PersonaEnum(str, Enum):
    """Persona options"""
    GENZ = "genz"
    MILLENNIAL = "millenial"
    WORKING_PROFESSIONALS = "working professionals"
    CREATIVE_THINKERS = "creative thinkers"
    SPIRITUAL_EXPLORERS = "spiritual explorers"


class LanguageEnum(str, Enum):
    """Language options"""
    ENGLISH = "English"
    HINDI = "Hindi"


class ContentTypeEnum(str, Enum):
    """Content type options"""
    NEWS = "News"
    ARTICLE = "Article"


class LanguageCodeEnum(str, Enum):
    """Language code options"""
    EN_US = "en-US"
    HI = "hi"


class CategoryEnum(str, Enum):
    """Category options"""
    ART = "Art"
    TRAVEL = "Travel"
    ENTERTAINMENT = "Entertainment"
    LITERATURE = "Literature"
    BOOKS = "Books"
    SPORTS = "Sports"
    HISTORY = "History"
    CULTURE = "Culture"
    WILDLIFE = "Wildlife"
    SPIRITUAL = "Spiritual"
    FOOD = "Food"


# === Request Models ===

class ArticleGenerationRequest(BaseModel):
    """Request model for article generation (Tab 1)"""
    url: HttpUrl = Field(..., description="News article URL")
    persona: PersonaEnum = Field(..., description="Target audience persona")
    content_language: LanguageEnum = Field(..., description="Content language")
    number_of_slides: int = Field(default=10, ge=0, le=1000, description="Number of slides to generate")


class TTSGenerationRequest(BaseModel):
    """Request model for TTS generation (Tab 2)"""
    structured_slides: Dict[str, Any] = Field(..., description="Structured slide JSON data")
    voice: str = Field(default="alloy", description="Voice to use for TTS")


class HTMLProcessingRequest(BaseModel):
    """Request model for HTML processing (Tab 3)"""
    full_slide_json: Dict[str, Any] = Field(..., description="Full slide JSON with slide1 to slide8")
    html_template: Optional[str] = Field(None, description="Custom HTML template")
    template_url: Optional[HttpUrl] = Field(None, description="URL to fetch HTML template from")


class AMPGenerationRequest(BaseModel):
    """Request model for AMP generation (Tab 4)"""
    amp_template_html: Optional[str] = Field(None, description="AMP template HTML")
    amp_template_url: Optional[HttpUrl] = Field(None, description="URL to fetch AMP template from")
    output_json: Dict[str, Any] = Field(..., description="Output JSON data")
    
    @model_validator(mode='after')
    def validate_template_source(self):
        """Ensure at least one template source is provided"""
        if not self.amp_template_html and not self.amp_template_url:
            raise ValueError("Either amp_template_html or amp_template_url must be provided")
        return self


class ContentSubmissionRequest(BaseModel):
    """Request model for content submission (Tab 5)"""
    story_title: str = Field(..., description="Story title")
    meta_description: str = Field(..., description="Meta description")
    meta_keywords: str = Field(..., description="Meta keywords")
    content_type: ContentTypeEnum = Field(..., description="Content type")
    language: LanguageCodeEnum = Field(..., description="Language code")
    image_url: HttpUrl = Field(..., description="Image URL")
    categories: CategoryEnum = Field(..., description="Content category")
    filter_tags: str = Field(..., description="Comma-separated filter tags")
    use_custom_cover: bool = Field(default=False, description="Use custom cover image")
    cover_image_url: Optional[HttpUrl] = Field(None, description="Custom cover image URL")
    prefinal_html: str = Field(..., description="Pre-final AMP HTML content")


class CoverImageRequest(BaseModel):
    """Request model for cover image generation (Tab 6)"""
    suvichaar_json: Dict[str, Any] = Field(..., description="Suvichaar-style JSON data")


# === Response Models ===

class SlideData(BaseModel):
    """Individual slide data"""
    title: str
    prompt: str
    image_prompt: Optional[str] = None
    script: Optional[str] = None


class ArticleAnalysisResponse(BaseModel):
    """Response model for article analysis"""
    title: str
    summary: str
    sentiment: str
    emotion: str
    category: str
    subcategory: str
    persona: str
    slides: List[SlideData]
    storytitle: str
    hookline: str


class StructuredOutputResponse(BaseModel):
    """Response model for structured output"""
    structured_output: Dict[str, str]
    filename: str
    download_url: Optional[str] = None


class TTSOutputResponse(BaseModel):
    """Response model for TTS output"""
    tts_output: Dict[str, Any]
    remotion_input: Dict[str, Any]
    filename: str
    download_url: Optional[str] = None


class HTMLProcessingResponse(BaseModel):
    """Response model for HTML processing"""
    updated_html: str
    updated_json: Dict[str, Any]
    filename: str
    download_url: Optional[str] = None


class AMPGenerationResponse(BaseModel):
    """Response model for AMP generation"""
    final_html: str
    filename: str
    download_url: Optional[str] = None


class MetadataResponse(BaseModel):
    """Response model for metadata generation"""
    meta_description: str
    meta_keywords: str
    filter_tags: str


class ContentSubmissionResponse(BaseModel):
    """Response model for content submission"""
    success: bool
    story_url: str
    html_url: str
    metadata_url: str
    slug: str
    filename: str
    download_url: Optional[str] = None


class CoverImageResponse(BaseModel):
    """Response model for cover image generation"""
    success: bool
    thumbnail_url: str
    transformed_json: Dict[str, Any]
    filename: str
    download_url: Optional[str] = None


class ErrorResponse(BaseModel):
    """Error response model"""
    error: str
    detail: Optional[str] = None
    status_code: int


# === Utility Models ===

class VoiceOption(BaseModel):
    """Voice option model"""
    id: str
    name: str


class UserMapping(BaseModel):
    """User mapping model"""
    name: str
    profile_url: str


class CategoryMapping(BaseModel):
    """Category mapping model"""
    name: str
    id: int


# === File Upload Models ===

class FileUploadResponse(BaseModel):
    """File upload response"""
    filename: str
    file_url: str
    file_size: int
    content_type: str


class BatchProcessingResponse(BaseModel):
    """Batch processing response"""
    total_items: int
    processed_items: int
    failed_items: int
    results: List[Dict[str, Any]]
