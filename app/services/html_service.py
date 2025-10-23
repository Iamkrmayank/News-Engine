"""
HTML Processing Service for Suvichaar FastAPI Service
"""
import re
import textwrap
import zipfile
import io
import json
import httpx
from typing import Dict, Any, Optional
from collections import OrderedDict
from datetime import datetime, timezone
from app.core.config import settings


class HTMLProcessingService:
    """Service for HTML processing and template manipulation"""
    
    def __init__(self):
        self.user_mapping = settings.USER_MAPPING
        self.category_mapping = settings.CATEGORY_MAPPING
        self.default_bg_image = settings.DEFAULT_BG_IMAGE
        self.default_cover_image = settings.DEFAULT_COVER_IMAGE
    
    async def fetch_template_from_url(self, template_url: str) -> str:
        """Fetch HTML template from URL"""
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.get(template_url)
                response.raise_for_status()
                
                # Check if content type is HTML
                content_type = response.headers.get('content-type', '').lower()
                if 'text/html' not in content_type and 'application/xhtml' not in content_type:
                    raise ValueError(f"URL does not return HTML content. Content-Type: {content_type}")
                
                return response.text
                
        except httpx.TimeoutException:
            raise ValueError("Timeout while fetching template from URL")
        except httpx.HTTPStatusError as e:
            raise ValueError(f"HTTP error {e.response.status_code} while fetching template from URL")
        except httpx.RequestError as e:
            raise ValueError(f"Network error while fetching template from URL: {str(e)}")
        except Exception as e:
            raise ValueError(f"Unexpected error while fetching template from URL: {str(e)}")
    
    def replace_placeholders_in_html(self, html_text: str, json_data: Dict[str, Any]) -> str:
        """Replace placeholders in HTML template"""
        storytitle = json_data.get("slide1", {}).get("storytitle", "")
        storytitle_url = json_data.get("slide1", {}).get("audio_url", "")
        hookline = json_data.get("slide2", {}).get("hookline", "")
        hookline_url = json_data.get("slide2", {}).get("audio_url", "")
        
        html_text = html_text.replace("{{storytitle}}", storytitle)
        html_text = html_text.replace("{{storytitle_audiourl}}", storytitle_url)
        html_text = html_text.replace("{{hookline}}", hookline)
        html_text = html_text.replace("{{hookline_audiourl}}", hookline_url)
        
        return html_text
    
    def modify_tab4_json(self, original_json: Dict[str, Any]) -> Dict[str, Any]:
        """Modify JSON structure for tab 4 processing"""
        updated_json = OrderedDict()
        slide_number = 2  # Start from slide2 since slide1 & slide2 are removed
        
        for i in range(3, 100):  # Covers slide3 to slide99
            old_key = f"slide{i}"
            if old_key not in original_json:
                break
            content = original_json[old_key]
            new_key = f"slide{slide_number}"
            
            for k, v in content.items():
                if k.endswith("paragraph1"):
                    para_key = f"s{slide_number}paragraph1"
                    audio_key = f"audio_url{slide_number}"
                    updated_json[new_key] = {
                        para_key: v,
                        audio_key: content.get("audio_url", ""),
                        "voice": content.get("voice", "")
                    }
                    break
            slide_number += 1
        
        return updated_json
    
    def generate_slide(self, paragraph: str, audio_url: str) -> str:
        """Generate AMP slide HTML"""
        return f"""
        <amp-story-page id="c29cbf94-847a-4bb7-a4eb-47d17d8c2d5a" auto-advance-after="page-c29cbf94-847a-4bb7-a4eb-47d17d8c2d5a-background-audio" class="i-amphtml-layout-container" i-amphtml-layout="container">
            <amp-story-animation layout="nodisplay" trigger="visibility" class="i-amphtml-layout-nodisplay" hidden="hidden" i-amphtml-layout="nodisplay">
                <script type="application/json">[{{"selector":"#anim-1a95e072-cada-435a-afea-082ddd65ff10","keyframes":{{"opacity":[0,1]}},"delay":0,"duration":600,"easing":"cubic-bezier(0.2, 0.6, 0.0, 1)","fill":"both"}}]</script>
            </amp-story-animation>
            <amp-story-animation layout="nodisplay" trigger="visibility" class="i-amphtml-layout-nodisplay" hidden="hidden" i-amphtml-layout="nodisplay">
                <script type="application/json">[{{"selector":"#anim-a938fe3f-03cf-47c5-9a84-da919c4f870b","keyframes":{{"transform":["translate3d(-115.2381%, 0px, 0)","translate3d(0px, 0px, 0)"]}},"delay":0,"duration":600,"easing":"cubic-bezier(0.2, 0.6, 0.0, 1)","fill":"both"}}]</script>
            </amp-story-animation>
            <amp-story-animation layout="nodisplay" trigger="visibility" class="i-amphtml-layout-nodisplay" hidden="hidden" i-amphtml-layout="nodisplay">
                <script type="application/json">[{{"selector":"#anim-f7c5981e-ac77-48d5-9b40-7a987a3e2ab0","keyframes":{{"opacity":[0,1]}},"delay":0,"duration":600,"easing":"cubic-bezier(0.2, 0.6, 0.0, 1)","fill":"both"}}]</script>
            </amp-story-animation>
            <amp-story-animation layout="nodisplay" trigger="visibility" class="i-amphtml-layout-nodisplay" hidden="hidden" i-amphtml-layout="nodisplay">
                <script type="application/json">[{{"selector":"#anim-0c1e94dd-ab91-415c-9372-0aa2e7e61630","keyframes":{{"transform":["translate3d(-115.55555%, 0px, 0)","translate3d(0px, 0px, 0)"]}},"delay":0,"duration":600,"easing":"cubic-bezier(0.2, 0.6, 0.0, 1)","fill":"both"}}]</script>
            </amp-story-animation>
            <amp-story-grid-layer template="vertical" aspect-ratio="412:618" class="grid-layer i-amphtml-layout-container" i-amphtml-layout="container" style="--aspect-ratio:412/618;">
                <div class="page-fullbleed-area"><div class="page-safe-area">
                    <div class="_6120891"><div class="_89d52dd mask" id="el-f00095ab-c147-4f19-9857-72ac678f953f">
                        <div class="_dc67a5c fill"></div></div></div></div></div>
            </amp-story-grid-layer>
            <amp-story-grid-layer template="fill" class="i-amphtml-layout-container" i-amphtml-layout="container">
                <amp-video autoplay="autoplay" layout="fixed" width="1" height="1" poster="" id="page-c29cbf94-847a-4bb7-a4eb-47d17d8c2d5a-background-audio" cache="google" class="i-amphtml-layout-fixed i-amphtml-layout-size-defined" style="width:1px;height:1px" i-amphtml-layout="fixed">
                    <source type="audio/mpeg" src="{audio_url}">
                </amp-video>
            </amp-story-grid-layer>
            <amp-story-grid-layer template="vertical" aspect-ratio="412:618" class="grid-layer i-amphtml-layout-container" i-amphtml-layout="container" style="--aspect-ratio:412/618;">
                <div class="page-fullbleed-area"><div class="page-safe-area">
                    <div class="_c19e533"><div class="_89d52dd mask" id="el-344ed989-789b-4a01-a124-9ae1d15d67f4">
                        <div data-leaf-element="true" class="_8aed44c">
                            <amp-img layout="fill" src="https://media.suvichaar.org/upload/polaris/polarisslide.png" alt="polarisslide.png" disable-inline-width="true" class="i-amphtml-layout-fill i-amphtml-layout-size-defined" i-amphtml-layout="fill"></amp-img>
                        </div></div></div>
                    <div class="_3d0c7a9"><div id="anim-1a95e072-cada-435a-afea-082ddd65ff10" class="_75da10d animation-wrapper">
                        <div id="anim-a938fe3f-03cf-47c5-9a84-da919c4f870b" class="_e559378 animation-wrapper">
                            <div id="el-2f080472-6c81-40a1-ac00-339cc8981388" class="_5342a26">
                                <h3 class="_d1a8d0d fill text-wrapper"><span><span class="_14af73e">{paragraph}</span></span></h3>
                            </div></div></div></div>
                    <div class="_a336742"><div id="anim-f7c5981e-ac77-48d5-9b40-7a987a3e2ab0" class="_75da10d animation-wrapper">
                        <div id="anim-0c1e94dd-ab91-415c-9372-0aa2e7e61630" class="_09239f8 animation-wrapper">
                            <div id="el-1a0d583c-c99b-4156-825b-3188408c0551" class="_ee8f788">
                                <h2 class="_59f9bb8 fill text-wrapper"><span><span class="_14af73e"></span></span></h2>
                            </div></div></div></div></div></div>
            </amp-story-grid-layer>
        </amp-story-page>
        """
    
    def process_amp_template(self, template_html: str, output_data: Dict[str, Any]) -> str:
        """Process AMP template with output data"""
        if "<!--INSERT_SLIDES_HERE-->" not in template_html:
            raise ValueError("Placeholder <!--INSERT_SLIDES_HERE--> not found in uploaded HTML.")
        
        all_slides = ""
        for key in sorted(output_data.keys(), key=lambda x: int(x.replace("slide", ""))):
            slide_num = key.replace("slide", "")
            data = output_data[key]
            para_key = f"s{slide_num}paragraph1"
            audio_key = f"audio_url{slide_num}"
            
            if para_key in data and audio_key in data:
                raw = data[para_key].replace("'", "'").replace('"', '&quot;')
                paragraph = textwrap.shorten(raw, width=180, placeholder="...")
                audio_url = data[audio_key]
                all_slides += self.generate_slide(paragraph, audio_url)
        
        final_html = template_html.replace("<!--INSERT_SLIDES_HERE-->", all_slides)
        return final_html
    
    def process_content_submission(self, html_template: str, submission_data: Dict[str, Any]) -> str:
        """Process content submission HTML template"""
        # Replace user and profile URL
        selected_user = submission_data.get("selected_user", "Suvichaar")
        user_profile_url = self.user_mapping.get(selected_user, "")
        
        html_template = html_template.replace("{{user}}", selected_user)
        html_template = html_template.replace("{{userprofileurl}}", user_profile_url)
        
        # Replace timestamps
        now = datetime.now(timezone.utc).isoformat(timespec='seconds')
        html_template = html_template.replace("{{publishedtime}}", now)
        html_template = html_template.replace("{{modifiedtime}}", now)
        
        # Replace content fields
        html_template = html_template.replace("{{storytitle}}", submission_data.get("story_title", ""))
        html_template = html_template.replace("{{metadescription}}", submission_data.get("meta_description", ""))
        html_template = html_template.replace("{{metakeywords}}", submission_data.get("meta_keywords", ""))
        html_template = html_template.replace("{{contenttype}}", submission_data.get("content_type", ""))
        html_template = html_template.replace("{{lang}}", submission_data.get("language", ""))
        html_template = html_template.replace("{{pagetitle}}", submission_data.get("page_title", ""))
        html_template = html_template.replace("{{canurl}}", submission_data.get("canonical_url", ""))
        html_template = html_template.replace("{{canurl1}}", submission_data.get("canonical_url1", ""))
        
        # Replace image URLs
        image_url = submission_data.get("image_url", "")
        if image_url:
            html_template = html_template.replace("{{image0}}", image_url)
        
        # Cleanup incorrect URL wrapping
        html_template = re.sub(r'href="\{(https://[^}]+)\}"', r'href="\1"', html_template)
        html_template = re.sub(r'src="\{(https://[^}]+)\}"', r'src="\1"', html_template)
        
        return html_template
    
    def create_zip_file(self, html_content: str, json_content: Dict[str, Any], 
                        html_filename: str, json_filename: str) -> bytes:
        """Create ZIP file with HTML and JSON content"""
        buffer = io.BytesIO()
        with zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED) as zipf:
            zipf.writestr(html_filename, html_content)
            zipf.writestr(json_filename, json.dumps(json_content, indent=2, ensure_ascii=False))
        buffer.seek(0)
        return buffer.getvalue()
    
    def generate_metadata(self, story_title: str, categories: int, filter_tags: list, 
                         nano: str, slug_nano: str, canonical_url: str, canonical_url1: str,
                         cover_image_url: str, meta_keywords: str, meta_description: str, 
                         language: str) -> Dict[str, Any]:
        """Generate metadata JSON"""
        return {
            "story_title": story_title,
            "categories": categories,
            "filterTags": filter_tags,
            "story_uid": nano,
            "story_link": canonical_url,
            "storyhtmlurl": canonical_url1,
            "urlslug": slug_nano,
            "cover_image_link": cover_image_url,
            "publisher_id": 1,
            "story_logo_link": "https://media.suvichaar.org/filters:resize/96x96/media/brandasset/suvichaariconblack.png",
            "keywords": meta_keywords,
            "metadescription": meta_description,
            "lang": language
        }
