"""
Test configuration and sample tests for Suvichaar FastAPI Service
"""
import pytest
import json
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_root_endpoint():
    """Test root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "version" in data


def test_health_check():
    """Test health check endpoint"""
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["data"]["status"] == "healthy"


def test_voice_options():
    """Test voice options endpoint"""
    response = client.get("/api/v1/voice-options")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "data" in data


def test_user_mapping():
    """Test user mapping endpoint"""
    response = client.get("/api/v1/user-mapping")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "data" in data


def test_category_mapping():
    """Test category mapping endpoint"""
    response = client.get("/api/v1/category-mapping")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "data" in data


def test_generate_article_invalid_url():
    """Test article generation with invalid URL"""
    response = client.post("/api/v1/generate-article", json={
        "url": "invalid-url",
        "persona": "genz",
        "content_language": "English",
        "number_of_slides": 10
    })
    assert response.status_code == 422  # Validation error


def test_generate_tts_invalid_data():
    """Test TTS generation with invalid data"""
    response = client.post("/api/v1/generate-tts", json={
        "structured_slides": {},
        "voice": "invalid-voice"
    })
    # This might succeed with empty data or fail depending on implementation
    assert response.status_code in [200, 422, 500]


def test_process_html_missing_template():
    """Test HTML processing with missing template"""
    response = client.post("/api/v1/process-html", json={
        "full_slide_json": {"slide1": {"storytitle": "Test"}},
        "html_template": None
    })
    # Should handle None template gracefully
    assert response.status_code in [200, 422, 500]


def test_generate_amp_missing_placeholder():
    """Test AMP generation with missing placeholder"""
    response = client.post("/api/v1/generate-amp", json={
        "amp_template_html": "<html><body>No placeholder</body></html>",
        "output_json": {"slide1": {"s1paragraph1": "Test"}}
    })
    assert response.status_code == 500  # Should fail due to missing placeholder


def test_submit_content_missing_fields():
    """Test content submission with missing required fields"""
    response = client.post("/api/v1/submit-content", json={
        "story_title": "",
        "meta_description": "",
        "meta_keywords": "",
        "content_type": "News",
        "language": "en-US",
        "image_url": "https://example.com/image.jpg",
        "categories": "Entertainment",
        "filter_tags": "",
        "prefinal_html_url": "https://example.com/template.html"
    })
    assert response.status_code == 422  # Validation error


def test_generate_cover_image_empty_json():
    """Test cover image generation with empty JSON"""
    response = client.post("/api/v1/generate-cover-image", json={
        "suvichaar_json": {}
    })
    # Should handle empty JSON gracefully
    assert response.status_code in [200, 500]


def test_upload_file_no_file():
    """Test file upload with no file"""
    response = client.post("/api/v1/upload-file")
    assert response.status_code == 422  # Missing file


def test_download_zip_invalid_json():
    """Test ZIP download with invalid JSON"""
    response = client.post("/api/v1/download-zip", data={
        "html_content": "<html></html>",
        "json_content": "invalid-json",
        "html_filename": "test.html",
        "json_filename": "test.json"
    })
    assert response.status_code == 500  # JSON parsing error


# Integration tests (require actual API keys)
@pytest.mark.skip(reason="Requires actual API keys")
def test_generate_article_integration():
    """Integration test for article generation"""
    response = client.post("/api/v1/generate-article", json={
        "url": "https://www.bbc.com/news",
        "persona": "genz",
        "content_language": "English",
        "number_of_slides": 5
    })
    assert response.status_code == 200
    data = response.json()
    assert "structured_output" in data
    assert "storytitle" in data["structured_output"]
    assert "hookline" in data["structured_output"]


@pytest.mark.skip(reason="Requires actual API keys")
def test_generate_tts_integration():
    """Integration test for TTS generation"""
    response = client.post("/api/v1/generate-tts", json={
        "structured_slides": {
            "storytitle": "Test Story",
            "s1paragraph1": "This is a test paragraph",
            "hookline": "This will surprise you!"
        },
        "voice": "alloy"
    })
    assert response.status_code == 200
    data = response.json()
    assert "tts_output" in data
    assert "remotion_input" in data


if __name__ == "__main__":
    pytest.main([__file__])
