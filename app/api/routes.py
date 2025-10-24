"""
API Routes for Suvichaar FastAPI Service
"""
from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from fastapi.responses import JSONResponse, FileResponse, Response
from fastapi.staticfiles import StaticFiles
from typing import Dict, Any, Optional
import json
import zipfile
import io
import time
from datetime import datetime

from app.models.schemas import (
    ArticleGenerationRequest, TTSGenerationRequest, HTMLProcessingRequest,
    AMPGenerationRequest, ContentSubmissionRequest, CoverImageRequest,
    ArticleAnalysisResponse, StructuredOutputResponse, TTSOutputResponse,
    HTMLProcessingResponse, AMPGenerationResponse, ContentSubmissionResponse,
    CoverImageResponse, MetadataResponse, ErrorResponse
)
from app.services.article_service import ArticleService
from app.services.tts_service import TTSService
from app.services.s3_service import S3Service
from app.services.html_service import HTMLProcessingService
from app.utils.helpers import (
    generate_filename, create_structured_output, restructure_slide_output,
    transform_suvichaar_json, get_random_user, create_success_response,
    create_error_response, extract_metadata_from_response
)

# Initialize routers
router = APIRouter()

# Initialize services
article_service = ArticleService()
tts_service = TTSService()
s3_service = S3Service()
html_service = HTMLProcessingService()


@router.post("/generate-article", response_model=StructuredOutputResponse)
async def generate_article(request: ArticleGenerationRequest):
    """
    Generate article content and structured output (Tab 1 functionality)
    """
    try:
        # Extract and analyze article
        title, summary, full_text = article_service.extract_article(str(request.url))
        sentiment = article_service.get_sentiment(summary or full_text)
        result = article_service.detect_category_and_subcategory(full_text, request.content_language.value)
        
        category = result["category"]
        subcategory = result["subcategory"]
        emotion = result["emotion"]
        
        # Generate hookline and storytitle
        hookline = article_service.generate_hookline(title, summary, request.content_language.value)
        storytitle = article_service.generate_storytitle(title, summary, request.content_language.value)
        
        # Generate slide content
        output = article_service.title_script_generator(
            category, subcategory, emotion, full_text, request.content_language.value
        )
        
        # Create structured output
        structured_output = create_structured_output(
            storytitle, hookline, output.get("slides", []), request.number_of_slides
        )
        
        # Hindi transliteration if needed
        if request.content_language.value == "Hindi":
            structured_output = tts_service.transliterate_to_devanagari(structured_output)
        
        filename = generate_filename("structured_slides", "json")
        
        return StructuredOutputResponse(
            structured_output=structured_output,
            filename=filename
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Article generation failed: {str(e)}")


@router.post("/generate-tts", response_model=TTSOutputResponse)
async def generate_tts(request: TTSGenerationRequest):
    """
    Generate TTS and upload to S3 (Tab 2 functionality)
    """
    try:
        # Generate TTS and upload to S3
        tts_output = tts_service.synthesize_and_upload(request.structured_slides, request.voice)
        
        # Generate Remotion input
        fixed_image_url = "https://media.suvichaar.org/upload/polaris/polariscover.png"
        remotion_input = tts_service.generate_remotion_input(tts_output, fixed_image_url)
        
        filename = generate_filename("tts_output", "json")
        
        return TTSOutputResponse(
            tts_output=tts_output,
            remotion_input=remotion_input,
            filename=filename
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"TTS generation failed: {str(e)}")


@router.post("/process-html", response_model=HTMLProcessingResponse)
async def process_html(request: HTMLProcessingRequest):
    """
    Process HTML template with slide data (Tab 3 functionality)
    """
    try:
        # Determine HTML template source
        html_template = ""
        
        if request.template_url:
            # Fetch template from URL
            html_template = await html_service.fetch_template_from_url(str(request.template_url))
        elif request.html_template:
            # Use provided template
            html_template = request.html_template
        else:
            # Use empty template if neither provided
            html_template = ""
        
        # Replace placeholders in HTML
        updated_html = html_service.replace_placeholders_in_html(
            html_template, request.full_slide_json
        )
        
        # Modify JSON structure
        updated_json = html_service.modify_tab4_json(request.full_slide_json)
        
        filename = generate_filename("output_bundle", "zip")
        
        # Upload files to S3 and get CloudFront URLs
        try:
            from app.services.s3_service import S3Service
            s3_service = S3Service()
            html_s3_url, json_s3_url = s3_service.upload_processed_files(
                updated_html, updated_json, "processed_html"
            )
        except Exception as s3_error:
            # If S3 upload fails, still return the response without S3 URLs
            html_s3_url = None
            json_s3_url = None
            print(f"S3 upload failed: {s3_error}")
        
        return HTMLProcessingResponse(
            updated_html=updated_html,
            updated_json=updated_json,
            filename=filename,
            html_s3_url=html_s3_url,
            json_s3_url=json_s3_url
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"HTML processing failed: {str(e)}")


@router.post("/process-html-download", response_class=Response)
async def process_html_download(request: HTMLProcessingRequest):
    """
    Process HTML template with slide data and return ZIP file for download
    """
    try:
        # Determine HTML template source
        html_template = ""
        
        if request.template_url:
            # Fetch template from URL
            html_template = await html_service.fetch_template_from_url(str(request.template_url))
        elif request.html_template:
            # Use provided template
            html_template = request.html_template
        else:
            # Use empty template if neither provided
            html_template = ""
        
        # Replace placeholders in HTML
        updated_html = html_service.replace_placeholders_in_html(
            html_template, request.full_slide_json
        )
        
        # Modify JSON structure
        updated_json = html_service.modify_tab4_json(request.full_slide_json)
        
        # Generate filenames
        timestamp = int(time.time())
        html_filename = f"processed_template_{timestamp}.html"
        json_filename = f"processed_data_{timestamp}.json"
        zip_filename = f"html_processing_bundle_{timestamp}.zip"
        
        # Create ZIP file
        zip_content = html_service.create_zip_file(
            updated_html, updated_json, html_filename, json_filename
        )
        
        # Return ZIP file as download
        return Response(
            content=zip_content,
            media_type="application/zip",
            headers={
                "Content-Disposition": f"attachment; filename={zip_filename}",
                "Content-Length": str(len(zip_content))
            }
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"HTML processing download failed: {str(e)}")


@router.get("/download-html/{filename}")
async def download_html_file(filename: str):
    """
    Download individual HTML file (placeholder - would need file storage)
    """
    raise HTTPException(status_code=501, detail="Individual file download not implemented yet. Use /process-html-download for ZIP bundle.")


@router.get("/download-json/{filename}")
async def download_json_file(filename: str):
    """
    Download individual JSON file (placeholder - would need file storage)
    """
    raise HTTPException(status_code=501, detail="Individual file download not implemented yet. Use /process-html-download for ZIP bundle.")


@router.post("/generate-amp", response_model=AMPGenerationResponse)
async def generate_amp(request: AMPGenerationRequest):
    """
    Generate AMP HTML from template and JSON (Tab 4 functionality)
    """
    try:
        # Determine AMP template source
        amp_template_html = ""
        
        if request.amp_template_url:
            # Fetch template from URL
            amp_template_html = await html_service.fetch_template_from_url(str(request.amp_template_url))
        elif request.amp_template_html:
            # Use provided template
            amp_template_html = request.amp_template_html
        else:
            # Use empty template if neither provided
            amp_template_html = ""
        
        # Determine output JSON data source
        output_json_data = {}
        
        if request.output_json_url:
            # Fetch JSON data from URL
            output_json_data = await html_service.fetch_json_from_url(str(request.output_json_url))
        elif request.output_json:
            # Use provided JSON data
            output_json_data = request.output_json
        else:
            # Use empty JSON if neither provided
            output_json_data = {}
        
        # Process AMP template
        final_html = html_service.process_amp_template(amp_template_html, output_json_data)
        
        filename = generate_filename("pre-final_amp_story", "html")
        
        # Upload HTML to S3 and get CloudFront URL
        try:
            from app.services.s3_service import S3Service
            s3_service = S3Service()
            html_s3_url = s3_service.upload_amp_html(final_html, "amp_story")
        except Exception as s3_error:
            # If S3 upload fails, still return the response without S3 URL
            html_s3_url = None
            print(f"S3 upload failed: {s3_error}")
        
        return AMPGenerationResponse(
            final_html=final_html,
            filename=filename,
            html_s3_url=html_s3_url
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AMP generation failed: {str(e)}")


@router.get("/download-amp/{filename}")
async def download_amp_file(filename: str):
    """
    Download AMP HTML file by filename
    """
    try:
        # For now, we'll store files in a temporary directory
        # In production, you might want to use S3 or a proper file storage
        import os
        temp_dir = "temp"
        file_path = os.path.join(temp_dir, filename)
        
        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail="File not found")
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        return Response(
            content=content,
            media_type="text/html",
            headers={
                "Content-Disposition": f"attachment; filename={filename}",
                "Content-Length": str(len(content.encode('utf-8')))
            }
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"File download failed: {str(e)}")


@router.post("/generate-amp-download", response_model=AMPGenerationResponse)
async def generate_amp_download(request: AMPGenerationRequest):
    """
    Generate AMP HTML from template and JSON and return both HTML content and download URL
    """
    try:
        # Determine AMP template source
        amp_template_html = ""
        
        if request.amp_template_url:
            # Fetch template from URL
            amp_template_html = await html_service.fetch_template_from_url(str(request.amp_template_url))
        elif request.amp_template_html:
            # Use provided template
            amp_template_html = request.amp_template_html
        else:
            # Use empty template if neither provided
            amp_template_html = ""
        
        # Determine output JSON data source
        output_json_data = {}
        
        if request.output_json_url:
            # Fetch JSON data from URL
            output_json_data = await html_service.fetch_json_from_url(str(request.output_json_url))
        elif request.output_json:
            # Use provided JSON data
            output_json_data = request.output_json
        else:
            # Use empty JSON if neither provided
            output_json_data = {}
        
        # Process AMP template
        final_html = html_service.process_amp_template(amp_template_html, output_json_data)
        
        # Generate filename
        timestamp = int(time.time())
        html_filename = f"generated_amp_story_{timestamp}.html"
        
        # Save file to temp directory for download
        import os
        temp_dir = "temp"
        os.makedirs(temp_dir, exist_ok=True)
        file_path = os.path.join(temp_dir, html_filename)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(final_html)
        
        # Generate download URL
        download_url = f"/api/v1/download-amp/{html_filename}"
        
        # Upload HTML to S3 and get CloudFront URL
        try:
            from app.services.s3_service import S3Service
            s3_service = S3Service()
            html_s3_url = s3_service.upload_amp_html(final_html, "generated_amp_story")
        except Exception as s3_error:
            # If S3 upload fails, still return the response without S3 URL
            html_s3_url = None
            print(f"S3 upload failed: {s3_error}")
        
        return AMPGenerationResponse(
            final_html=final_html,
            filename=html_filename,
            download_url=download_url,
            html_s3_url=html_s3_url
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AMP generation download failed: {str(e)}")


@router.post("/generate-metadata", response_model=MetadataResponse)
async def generate_metadata(story_title: str = Form(...)):
    """
    Generate metadata for story title (Tab 5 helper)
    """
    try:
        from app.services.article_service import ArticleService
        article_service = ArticleService()
        
        messages = [
            {
                "role": "user",
                "content": f"""Generate metadata for a web story titled '{story_title}'. Please provide the response in this exact format:

Description: [Write a short SEO-friendly meta description here]
Keywords: [Write comma-separated meta keywords here]
Filter Tags: [Write comma-separated filter tags here]

Make sure to use the exact labels "Description:", "Keywords:", and "Filter Tags:" in your response."""
            }
        ]
        
        response = article_service.client.chat.completions.create(
            model=article_service.deployment_name,
            messages=messages,
            max_tokens=300,
            temperature=0.5,
        )
        
        output = response.choices[0].message.content
        metadata = extract_metadata_from_response(output)
        
        # Fallback: If extraction failed, generate basic metadata
        if not metadata.get("meta_description") or metadata.get("meta_description") == "**":
            metadata["meta_description"] = f"Latest news and updates about {story_title}. Stay informed with comprehensive coverage and analysis."
        
        if not metadata.get("meta_keywords") or metadata.get("meta_keywords") == "**":
            metadata["meta_keywords"] = f"{story_title.lower()}, news, updates, latest, information"
        
        if not metadata.get("filter_tags") or metadata.get("filter_tags") == "**":
            metadata["filter_tags"] = f"{story_title}, News, Updates"
        
        return MetadataResponse(**metadata)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Metadata generation failed: {str(e)}")


@router.post("/submit-content", response_model=ContentSubmissionResponse)
async def submit_content(request: ContentSubmissionRequest):
    """
    Submit content for publishing (Tab 5 functionality)
    """
    try:
        # Generate slug and URLs
        nano, slug_nano, canonical_url, canonical_url1 = s3_service.generate_slug_and_urls(request.story_title)
        page_title = f"{request.story_title} | Suvichaar"
        
        # Process image URL
        cover_image_url = request.cover_image_url if request.use_custom_cover else request.image_url
        
        # Fetch HTML content from URL
        prefinal_html = await html_service.fetch_template_from_url(str(request.prefinal_html_url))
        
        # Process HTML template
        submission_data = {
            "story_title": request.story_title,
            "meta_description": request.meta_description,
            "meta_keywords": request.meta_keywords,
            "content_type": request.content_type.value,
            "language": request.language.value,
            "image_url": str(request.image_url),
            "page_title": page_title,
            "canonical_url": canonical_url,
            "canonical_url1": canonical_url1,
            "selected_user": get_random_user()
        }
        
        processed_html = html_service.process_content_submission(prefinal_html, submission_data)
        
        # Generate resized image URLs
        resized_urls = s3_service.generate_resized_image_urls(str(request.image_url))
        for label, url in resized_urls.items():
            processed_html = processed_html.replace(f"{{{{{label}}}}}", url)
        
        # Upload HTML to S3
        html_url = s3_service.upload_html_story(processed_html, slug_nano)
        
        # Generate and upload metadata
        filter_tags = [tag.strip() for tag in request.filter_tags.split(",") if tag.strip()]
        metadata = html_service.generate_metadata(
            request.story_title, 
            html_service.category_mapping[request.categories.value],
            filter_tags,
            nano, slug_nano, canonical_url, canonical_url1,
            str(cover_image_url), request.meta_keywords, request.meta_description,
            request.language.value
        )
        
        metadata_url = s3_service.upload_metadata(metadata, slug_nano)
        
        filename = f"{request.story_title}.zip"
        
        return ContentSubmissionResponse(
            success=True,
            story_url=canonical_url,
            html_url=html_url,
            metadata_url=metadata_url,
            slug=slug_nano,
            filename=filename
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Content submission failed: {str(e)}")


@router.post("/generate-cover-image", response_model=CoverImageResponse)
async def generate_cover_image(request: CoverImageRequest):
    """
    Generate cover image thumbnail (Tab 6 functionality)
    """
    try:
        # Transform JSON data
        transformed_json = transform_suvichaar_json(request.suvichaar_json)
        
        # Generate thumbnail
        thumbnail_bytes = s3_service.generate_thumbnail(transformed_json)
        
        # Upload thumbnail
        thumbnail_url = s3_service.upload_thumbnail(thumbnail_bytes)
        
        filename = generate_filename("CoverJSON", "json")
        
        return CoverImageResponse(
            success=True,
            thumbnail_url=thumbnail_url,
            transformed_json=transformed_json,
            filename=filename
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Cover image generation failed: {str(e)}")


# === File Upload Routes ===

@router.post("/upload-file")
async def upload_file(file: UploadFile = File(...)):
    """
    Upload file to S3
    """
    try:
        content = await file.read()
        filename = f"{int(datetime.now().timestamp())}_{file.filename}"
        
        file_url = s3_service.upload_file(content, filename, file.content_type)
        
        return create_success_response({
            "filename": filename,
            "file_url": file_url,
            "file_size": len(content),
            "content_type": file.content_type
        })
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"File upload failed: {str(e)}")


@router.post("/download-zip")
async def download_zip(html_content: str = Form(...), json_content: str = Form(...), 
                      html_filename: str = Form(...), json_filename: str = Form(...)):
    """
    Create and download ZIP file
    """
    try:
        json_data = json.loads(json_content)
        zip_content = html_service.create_zip_file(
            html_content, json_data, html_filename, json_filename
        )
        
        return FileResponse(
            io.BytesIO(zip_content),
            media_type="application/zip",
            filename=f"output_{int(datetime.now().timestamp())}.zip"
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"ZIP creation failed: {str(e)}")


# === Utility Routes ===

@router.get("/voice-options")
async def get_voice_options():
    """
    Get available voice options
    """
    from app.core.config import settings
    return create_success_response(settings.VOICE_OPTIONS)


@router.get("/user-mapping")
async def get_user_mapping():
    """
    Get user mapping
    """
    from app.core.config import settings
    return create_success_response(settings.USER_MAPPING)


@router.get("/category-mapping")
async def get_category_mapping():
    """
    Get category mapping
    """
    from app.core.config import settings
    return create_success_response(settings.CATEGORY_MAPPING)


@router.get("/health")
async def health_check():
    """
    Health check endpoint
    """
    return create_success_response({"status": "healthy", "timestamp": datetime.now().isoformat()})
