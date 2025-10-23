"""
Utility functions for Suvichaar FastAPI Service
"""
import json
import time
import random
import string
from typing import Dict, Any, List
from collections import OrderedDict


def generate_slug_and_urls(title: str) -> tuple:
    """Generate slug and URLs from title"""
    if not title or not isinstance(title, str):
        raise ValueError("Invalid title")
    
    slug = ''.join(c for c in title.lower().replace(" ", "-").replace("_", "-") 
                  if c in string.ascii_lowercase + string.digits + '-')
    slug = slug.strip('-')
    nano = ''.join(random.choices(string.ascii_letters + string.digits + '_-', k=10)) + '_G'
    slug_nano = f"{slug}_{nano}"
    
    return nano, slug_nano, f"https://suvichaar.org/stories/{slug_nano}", f"https://stories.suvichaar.org/{slug_nano}.html"


def restructure_slide_output(final_output: Dict[str, Any]) -> Dict[str, str]:
    """Restructure slide output into paragraph format"""
    slides = final_output.get("slides", [])
    structured = {}
    
    for idx, slide in enumerate(slides):
        key = f"s{idx + 1}paragraph1"
        script = slide.get("script", "").strip()
        
        # Safety net: If empty script, fall back to title or prompt
        if not script:
            fallback = slide.get("title") or slide.get("prompt") or "Content unavailable"
            script = fallback.strip()
        
        structured[key] = script
    
    return structured


def create_structured_output(storytitle: str, hookline: str, slides: List[Dict[str, Any]], 
                           number_of_slides: int) -> Dict[str, str]:
    """Create structured output from story components"""
    structured_output = OrderedDict()
    structured_output["storytitle"] = storytitle
    
    for i in range(1, number_of_slides + 1):
        key = f"s{i}paragraph1"
        if i <= len(slides):
            structured_output[key] = slides[i-1].get("script", slides[i-1].get("title", ""))
        else:
            structured_output[key] = ""
    
    structured_output["hookline"] = hookline
    return structured_output


def generate_filename(prefix: str, extension: str = "json") -> str:
    """Generate filename with timestamp"""
    timestamp = int(time.time())
    return f"{prefix}_{timestamp}.{extension}"


def validate_json_structure(data: Dict[str, Any], required_keys: List[str]) -> bool:
    """Validate JSON structure has required keys"""
    return all(key in data for key in required_keys)


def clean_text_for_html(text: str) -> str:
    """Clean text for HTML output"""
    if not text:
        return ""
    
    # Replace common problematic characters
    text = text.replace("'", "'")
    text = text.replace('"', '&quot;')
    text = text.replace('\n', ' ')
    text = text.replace('\r', '')
    
    return text.strip()


def extract_metadata_from_response(response_text: str) -> Dict[str, str]:
    """Extract metadata from AI response"""
    import re
    
    # Try multiple patterns to extract metadata
    patterns = {
        "meta_description": [
            r"[Dd]escription\s*[:\-]\s*(.+?)(?=\n|$)",
            r"[Mm]eta\s*[Dd]escription\s*[:\-]\s*(.+?)(?=\n|$)",
            r"Description\s*[:\-]\s*(.+?)(?=\n|$)"
        ],
        "meta_keywords": [
            r"[Kk]eywords\s*[:\-]\s*(.+?)(?=\n|$)",
            r"[Mm]eta\s*[Kk]eywords\s*[:\-]\s*(.+?)(?=\n|$)",
            r"Keywords\s*[:\-]\s*(.+?)(?=\n|$)"
        ],
        "filter_tags": [
            r"[Ff]ilter\s*[Tt]ags\s*[:\-]\s*(.+?)(?=\n|$)",
            r"[Tt]ags\s*[:\-]\s*(.+?)(?=\n|$)",
            r"Filter Tags\s*[:\-]\s*(.+?)(?=\n|$)"
        ]
    }
    
    result = {
        "meta_description": "",
        "meta_keywords": "",
        "filter_tags": ""
    }
    
    for field, field_patterns in patterns.items():
        for pattern in field_patterns:
            match = re.search(pattern, response_text, re.MULTILINE | re.DOTALL)
            if match:
                result[field] = match.group(1).strip()
                break
    
    # If still empty, try to extract from numbered lists or bullet points
    if not result["meta_description"]:
        desc_match = re.search(r"1\.?\s*(.+?)(?=\n|$)", response_text)
        if desc_match:
            result["meta_description"] = desc_match.group(1).strip()
    
    if not result["meta_keywords"]:
        keys_match = re.search(r"2\.?\s*(.+?)(?=\n|$)", response_text)
        if keys_match:
            result["meta_keywords"] = keys_match.group(1).strip()
    
    if not result["filter_tags"]:
        tags_match = re.search(r"3\.?\s*(.+?)(?=\n|$)", response_text)
        if tags_match:
            result["filter_tags"] = tags_match.group(1).strip()
    
    return result


def transform_suvichaar_json(data: Dict[str, Any]) -> Dict[str, Any]:
    """Transform Suvichaar JSON for cover image generation"""
    transformed = {}
    
    for slide_key, info in data.items():
        idx = int(slide_key.replace("slide", ""))
        
        if "storytitle" in info:
            text = info["storytitle"]
        elif "hookline" in info:
            text = info["hookline"]
        else:
            text = next((v for k, v in info.items() if "paragraph" in k), "")
        
        audio = info.get("audio_url", "")
        
        transformed[slide_key] = {
            f"s{idx}paragraph1": text,
            f"s{idx}audio1": audio,
            f"s{idx}image1": "https://media.suvichaar.org/upload/polaris/polariscover.png",
            f"s{idx}paragraph2": "Suvichaar"
        }
    
    return transformed


def get_random_user() -> str:
    """Get random user from user mapping"""
    from app.core.config import settings
    return random.choice(list(settings.USER_MAPPING.keys()))


def format_error_message(error: Exception) -> str:
    """Format error message for API response"""
    return f"{type(error).__name__}: {str(error)}"


def create_success_response(data: Any, message: str = "Success") -> Dict[str, Any]:
    """Create standardized success response"""
    return {
        "success": True,
        "message": message,
        "data": data
    }


def create_error_response(error: str, detail: str = None, status_code: int = 400) -> Dict[str, Any]:
    """Create standardized error response"""
    return {
        "success": False,
        "error": error,
        "detail": detail,
        "status_code": status_code
    }
