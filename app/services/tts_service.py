"""
TTS Service for Suvichaar FastAPI Service
"""
import os
import uuid
import requests
import boto3
from typing import Dict, Any, OrderedDict
from collections import OrderedDict
from app.core.config import settings


class TTSService:
    """Service for Text-to-Speech generation and S3 upload"""
    
    def __init__(self):
        self.s3_client = boto3.client(
            "s3",
            aws_access_key_id=settings.AWS_ACCESS_KEY,
            aws_secret_access_key=settings.AWS_SECRET_KEY,
            region_name=settings.AWS_REGION,
        )
        self.azure_tts_url = settings.AZURE_TTS_URL
        self.azure_api_key = settings.AZURE_API_KEY
        self.s3_prefix = settings.S3_PREFIX
        self.cdn_base = settings.CDN_BASE
    
    def synthesize_and_upload(self, paragraphs: Dict[str, str], voice: str) -> Dict[str, Any]:
        """Synthesize text to speech and upload to S3"""
        result = OrderedDict()
        os.makedirs("temp", exist_ok=True)
        
        slide_index = 1
        
        # Slide 1: storytitle
        if "storytitle" in paragraphs:
            storytitle = paragraphs["storytitle"]
            audio_url = self._generate_audio(storytitle, voice)
            result[f"slide{slide_index}"] = {
                "storytitle": storytitle,
                "audio_url": audio_url,
                "voice": voice
            }
            slide_index += 1
        
        # Slide 2: hookline
        if "hookline" in paragraphs:
            hookline = paragraphs["hookline"]
            audio_url = self._generate_audio(hookline, voice)
            result[f"slide{slide_index}"] = {
                "hookline": hookline,
                "audio_url": audio_url,
                "voice": voice
            }
            slide_index += 1
        
        # Slide 3 onwards: s1paragraph1 to s9paragraph1
        for i in range(1, 10):  # s1 to s9
            key = f"s{i}paragraph1"
            if key not in paragraphs:
                continue
            
            text = paragraphs[key]
            audio_url = self._generate_audio(text, voice)
            
            result[f"slide{slide_index}"] = {
                key: text,
                "audio_url": audio_url,
                "voice": voice
            }
            slide_index += 1
        
        return result
    
    def _generate_audio(self, text: str, voice: str) -> str:
        """Generate audio from text using Azure TTS"""
        try:
            response = requests.post(
                self.azure_tts_url,
                headers={
                    "Content-Type": "application/json",
                    "api-key": self.azure_api_key
                },
                json={
                    "model": "tts-1-hd",
                    "input": text,
                    "voice": voice
                }
            )
            response.raise_for_status()
            
            filename = f"tts_{uuid.uuid4().hex}.mp3"
            local_path = os.path.join("temp", filename)
            
            with open(local_path, "wb") as f:
                f.write(response.content)
            
            s3_key = f"{self.s3_prefix}{filename}"
            self.s3_client.upload_file(local_path, settings.AWS_BUCKET, s3_key)
            cdn_url = f"{self.cdn_base}{s3_key}"
            
            os.remove(local_path)
            return cdn_url
            
        except Exception as e:
            raise Exception(f"TTS generation failed: {str(e)}")
    
    def generate_remotion_input(self, tts_output: Dict[str, Any], 
                               fixed_image_url: str, author_name: str = "Suvichaar") -> Dict[str, Any]:
        """Generate Remotion input from TTS output"""
        remotion_data = OrderedDict()
        slide_index = 1
        
        # Slide 1: storytitle
        if "storytitle" in tts_output:
            remotion_data[f"slide{slide_index}"] = {
                f"s{slide_index}paragraph1": tts_output["storytitle"],
                f"s{slide_index}audio1": tts_output.get(f"slide{slide_index}", {}).get("audio_url", ""),
                f"s{slide_index}image1": fixed_image_url,
                f"s{slide_index}paragraph2": f"- {author_name}"
            }
            slide_index += 1
        
        # Slides for s1paragraph1 to s9paragraph1
        for i in range(1, 10):
            key = f"s{i}paragraph1"
            if key in tts_output:
                slide_key = f"slide{slide_index}"
                remotion_data[slide_key] = {
                    f"s{slide_index}paragraph1": tts_output[key],
                    f"s{slide_index}audio1": tts_output.get(slide_key, {}).get("audio_url", ""),
                    f"s{slide_index}image1": fixed_image_url,
                    f"s{slide_index}paragraph2": f"- {author_name}"
                }
                slide_index += 1
        
        # Hookline as last content slide
        if "hookline" in tts_output:
            slide_key = f"slide{slide_index}"
            remotion_data[slide_key] = {
                f"s{slide_index}paragraph1": tts_output["hookline"],
                f"s{slide_index}audio1": tts_output.get(slide_key, {}).get("audio_url", ""),
                f"s{slide_index}image1": fixed_image_url,
                f"s{slide_index}paragraph2": f"- {author_name}"
            }
            slide_index += 1
        
        # Final CTA slide
        remotion_data[f"slide{slide_index}"] = {
            f"s{slide_index}paragraph1": "Get Such\nInspirational\nContent",
            f"s{slide_index}audio1": "https://cdn.suvichaar.org/media/tts_407078a4ff494fb5bed8c35050ffd1a7.mp3",
            f"s{slide_index}video1": "",
            f"s{slide_index}paragraph2": "Like | Subscribe | Share\nwww.suvichaar.org"
        }
        
        return remotion_data
    
    def transliterate_to_devanagari(self, json_data: Dict[str, str]) -> Dict[str, str]:
        """Transliterate Hindi text to Devanagari script"""
        from app.services.article_service import ArticleService
        
        article_service = ArticleService()
        updated = {}
        
        for k, v in json_data.items():
            # Only transliterate slide paragraphs
            if k.startswith("s") and "paragraph1" in k and v.strip():
                prompt = f"""Transliterate this Hindi sentence (written in Latin script) into Hindi Devanagari script. Return only the transliterated text:\n\n{v}"""
                
                try:
                    response = article_service.client.chat.completions.create(
                        model=article_service.deployment_name,
                        messages=[
                            {"role": "system", "content": "You are a Hindi transliteration expert."},
                            {"role": "user", "content": prompt.strip()}
                        ]
                    )
                    devanagari = response.choices[0].message.content.strip()
                    updated[k] = devanagari
                except Exception as e:
                    # Fallback: use original if error occurs
                    updated[k] = v
            else:
                updated[k] = v
        
        return updated
