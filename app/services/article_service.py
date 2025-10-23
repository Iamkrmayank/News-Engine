"""
Core service classes for Suvichaar FastAPI Service
"""
import json
import time
import os
import uuid
import requests
import boto3
import nltk
import datetime
import random
import string
import base64
import re
import textwrap
from typing import Dict, List, Any, Optional, Tuple
from urllib.parse import urlparse
from io import BytesIO
from datetime import datetime, timezone
from collections import OrderedDict
from openai import AzureOpenAI
from textblob import TextBlob
from bs4 import BeautifulSoup

from app.core.config import settings


class ArticleService:
    """Service for article extraction and analysis"""
    
    def __init__(self):
        self.client = AzureOpenAI(
            azure_endpoint=settings.AZURE_OPENAI_ENDPOINT,
            api_key=settings.AZURE_OPENAI_API_KEY,
            api_version=settings.AZURE_OPENAI_API_VERSION
        )
        self.deployment_name = settings.AZURE_OPENAI_DEPLOYMENT_NAME
        
        # Setup NLTK
        try:
            nltk.data.find('tokenizers/punkt')
        except LookupError:
            nltk.download('punkt')
    
    def extract_article(self, url: str) -> Tuple[str, str, str]:
        """Extract article content from URL"""
        try:
            import requests
            from bs4 import BeautifulSoup
            
            # Use requests and BeautifulSoup instead of newspaper
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract title
            title_tag = soup.find('title')
            title = title_tag.get_text().strip() if title_tag else "Untitled Article"
            
            # Extract main content
            # Try to find article content in common tags
            content_selectors = [
                'article',
                '.article-content',
                '.post-content',
                '.entry-content',
                '.content',
                'main',
                '.main-content'
            ]
            
            content_text = ""
            for selector in content_selectors:
                content_elem = soup.select_one(selector)
                if content_elem:
                    content_text = content_elem.get_text().strip()
                    break
            
            # If no specific content found, get all paragraph text
            if not content_text:
                paragraphs = soup.find_all('p')
                content_text = ' '.join([p.get_text().strip() for p in paragraphs])
            
            # Fallback for missing content
            if not content_text:
                content_text = "No article content available."
            
            # Generate summary (first 300 characters)
            summary = content_text[:300] + "..." if len(content_text) > 300 else content_text
            
            return title, summary, content_text
            
        except Exception as e:
            raise Exception(f"Failed to extract article from URL: {str(e)}")
    
    def get_sentiment(self, text: str) -> str:
        """Analyze sentiment of text"""
        if not text or not text.strip():
            return "neutral"
        
        clean_text = text.strip().replace("\n", " ")
        polarity = TextBlob(clean_text).sentiment.polarity
        
        if polarity > 0.2:
            return "positive"
        elif polarity < -0.2:
            return "negative"
        else:
            return "neutral"
    
    def detect_category_and_subcategory(self, text: str, content_language: str = "English") -> Dict[str, str]:
        """Detect category, subcategory, and emotion"""
        if not text or len(text.strip()) < 50:
            return {
                "category": "Unknown",
                "subcategory": "General",
                "emotion": "Neutral"
            }
        
        # Prompt construction based on language
        if content_language == "Hindi":
            prompt = f"""
आप एक समाचार विश्लेषण विशेषज्ञ हैं।

इस समाचार लेख का विश्लेषण करें और नीचे तीन बातें बताएं:

1. category (श्रेणी)
2. subcategory (उपश्रेणी)
3. emotion (भावना)

लेख:
\"\"\"{text[:3000]}\"\"\"

जवाब केवल JSON में दें:
{{
  "category": "...",
  "subcategory": "...",
  "emotion": "..."
}}
"""
        else:
            prompt = f"""
You are an expert news analyst.

Analyze the following news article and return:

1. category
2. subcategory
3. emotion

Article:
\"\"\"{text[:3000]}\"\"\"

Return ONLY as JSON:
{{
  "category": "...",
  "subcategory": "...",
  "emotion": "..."
}}
"""
        
        try:
            response = self.client.chat.completions.create(
                model=self.deployment_name,
                messages=[
                    {"role": "system", "content": "Classify the news into category, subcategory, and emotion."},
                    {"role": "user", "content": prompt.strip()}
                ],
                max_tokens=150
            )
            
            content = response.choices[0].message.content.strip()
            content = content.strip("```json").strip("```").strip()
            
            result = json.loads(content)
            
            if all(k in result for k in ["category", "subcategory", "emotion"]):
                return result
                
        except Exception as e:
            print(f"Category detection failed: {e}")
        
        return {
            "category": "Unknown",
            "subcategory": "General",
            "emotion": "Neutral"
        }
    
    def generate_hookline(self, title: str, summary: str, content_language: str = "English") -> str:
        """Generate hookline for the story"""
        if content_language == "Hindi":
            prompt = f"""
आप 'पोलारिस' नामक एक सोशल मीडिया रणनीतिकार हैं और चैनल 'सुविचार' के लिए कार्य करते हैं। आपका कार्य है एक संक्षिप्त, ध्यान खींचने वाली *हुकलाइन* बनाना जो इस समाचार की ओर दर्शकों का ध्यान आकर्षित करे।

शीर्षक: {title}
सारांश: {summary}

भाषा: हिंदी

अनुरोध:
- केवल एक वाक्य हो
- हैशटैग, इमोजी या अधिक विराम चिह्न न हो
- भाषा सरल और भावनात्मक रूप से आकर्षक हो
- 120 वर्णों से कम होनी चाहिए
- उद्धरण ("") शामिल न करें

अब कृपया पोलारिस की आवाज़ में हुकलाइन दीजिए:
"""
        else:
            prompt = f"""
You are Polaris, a social media strategist for the news channel 'Suvichaar'. Your job is to create a short, attention-grabbing *hookline* for a news story.

Title: {title}
Summary: {summary}

Language: {content_language}

Requirements:
- One sentence only
- Avoid hashtags, emojis, and excessive punctuation
- Use simple and emotionally engaging language
- Must be under 120 characters
- Do not include quotes in output

Now generate the hookline in Polaris' tone:
"""
        
        try:
            response = self.client.chat.completions.create(
                model=self.deployment_name,
                messages=[
                    {"role": "system", "content": "You create viral hooklines for news stories."},
                    {"role": "user", "content": prompt.strip()}
                ]
            )
            return response.choices[0].message.content.strip().strip('"')
            
        except Exception as e:
            print(f"Hookline generation failed: {e}")
            return "यह खबर आपको चौंका सकती है!" if content_language == "Hindi" else "This story might surprise you!"
    
    def generate_storytitle(self, title: str, summary: str, content_language: str = "English") -> str:
        """Generate story title"""
        if content_language == "Hindi":
            prompt = f"""
आप एक समाचार शीर्षक विशेषज्ञ हैं। नीचे दी गई अंग्रेज़ी समाचार शीर्षक और सारांश को पढ़कर, उसी का अर्थ बनाए रखते हुए एक नया आकर्षक **हिंदी शीर्षक** बनाइए।

अंग्रेज़ी शीर्षक: {title}
सारांश: {summary}

अनुरोध:
- केवल एक पंक्ति
- भाषा सरल और स्पष्ट हो
- भावनात्मक रूप से आकर्षक हो
- उद्धरण ("") शामिल न करें

अब कृपया हिंदी शीर्षक दीजिए:
"""
        else:
            return title.strip()
        
        try:
            response = self.client.chat.completions.create(
                model=self.deployment_name,
                messages=[
                    {"role": "system", "content": "You generate clear and catchy news headlines."},
                    {"role": "user", "content": prompt.strip()}
                ]
            )
            return response.choices[0].message.content.strip().strip('"')
            
        except Exception as e:
            print(f"Storytitle generation failed: {e}")
            return title.strip()
    
    def title_script_generator(self, category: str, subcategory: str, emotion: str, 
                              article_text: str, content_language: str = "English", 
                              character_sketch: Optional[str] = None) -> Dict[str, Any]:
        """Generate title and script for slides"""
        if not character_sketch:
            character_sketch = (
                f"Polaris is a sincere and articulate {content_language} news anchor. "
                "They present facts clearly, concisely, and warmly, connecting deeply with their audience."
            )
        
        # Generate slides
        system_prompt = f"""
You are a digital content editor.

Create a structured 5-slide web story from the article below.

Language: {content_language}

Each slide must contain:
- A short title in {content_language}
{"- The title must be written in Hindi (Devanagari script)." if content_language == "Hindi" else ""}
- A narration prompt (instruction only, don't write narration)
{"- The narration prompt must also be in Hindi (Devanagari script)." if content_language == "Hindi" else ""}

Format:
{{
  "slides": [
    {{ "title": "...", "prompt": "..." }},
    ...
  ]
}}
"""
        
        user_prompt = f"""
Category: {category}
Subcategory: {subcategory}
Emotion: {emotion}

Article:
\"\"\"{article_text[:3000]}\"\"\"
"""
        
        response = self.client.chat.completions.create(
            model=self.deployment_name,
            messages=[
                {"role": "system", "content": system_prompt.strip()},
                {"role": "user", "content": user_prompt.strip()}
            ]
        )
        
        content = response.choices[0].message.content.strip()
        content = content.strip("```json").strip("```").strip()
        
        try:
            slides_raw = json.loads(content)["slides"]
        except:
            return {"category": category, "subcategory": subcategory, "emotion": emotion, "slides": []}
        
        # Generate Slide 1 Intro Narration
        headline = article_text.split("\n")[0].strip().replace('"', '')
        
        if content_language == "Hindi":
            slide1_prompt = f"Generate a greeting and news headline narration in Hindi for the story: {headline}"
        else:
            slide1_prompt = f"Generate a greeting and headline intro narration in English for: {headline}"
        
        slide1_response = self.client.chat.completions.create(
            model=self.deployment_name,
            messages=[
                {"role": "system", "content": "You are a news presenter generating opening lines."},
                {"role": "user", "content": slide1_prompt}
            ]
        )
        slide1_script = slide1_response.choices[0].message.content.strip()
        
        slides = [{
            "title": headline[:80],
            "prompt": "Intro slide with greeting and headline.",
            "image_prompt": f"Vector-style illustration of Polaris presenting news: {headline}",
            "script": slide1_script
        }]
        
        # Generate narration for each slide
        for slide in slides_raw:
            script_language = f"{content_language} (use Devanagari script)" if content_language == "Hindi" else content_language
            narration_prompt = f"""
Write a narration in **{script_language}** (max 200 characters),
in the voice of Polaris.

Instruction: {slide['prompt']}
Tone: Warm, clear, informative. No self-intro.

Character sketch:
{character_sketch}
"""
            
            try:
                narration_response = self.client.chat.completions.create(
                    model=self.deployment_name,
                    messages=[
                        {"role": "system", "content": "You write concise narrations for web story slides."},
                        {"role": "user", "content": narration_prompt.strip()}
                    ]
                )
                narration = narration_response.choices[0].message.content.strip()
            except:
                narration = "Unable to generate narration for this slide."
            
            slides.append({
                "title": slide['title'],
                "prompt": slide['prompt'],
                "image_prompt": f"Modern vector-style visual for: {slide['title']}",
                "script": narration
            })
        
        return {
            "category": category,
            "subcategory": subcategory,
            "emotion": emotion,
            "slides": slides
        }
