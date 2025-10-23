# Suvichaar FastAPI Service

A comprehensive FastAPI service that replicates all functionality from the Suvichaar Streamlit application, providing RESTful APIs for web story content generation.

## 🚀 Features

### Complete Tab Functionality Coverage

- **Tab 1**: Article Generation & Analysis
- **Tab 2**: Text-to-Speech Generation & S3 Upload
- **Tab 3**: HTML Processing & Template Modification
- **Tab 4**: AMP HTML Generation
- **Tab 5**: Content Submission & Publishing
- **Tab 6**: Cover Image Generation

### Core Services

- **Article Service**: URL extraction, sentiment analysis, category detection
- **TTS Service**: Azure Speech API integration, S3 audio upload
- **S3 Service**: File uploads, image processing, metadata management
- **HTML Service**: Template processing, AMP generation, ZIP creation

## 📁 Project Structure

```
suvichaar-fastapi-service/
├── app/
│   ├── api/
│   │   └── routes.py          # API endpoints
│   ├── core/
│   │   ├── config.py          # Configuration settings
│   │   └── database.py        # Database connection
│   ├── models/
│   │   ├── schemas.py         # Pydantic models
│   │   └── database.py        # SQLAlchemy models
│   ├── services/
│   │   ├── article_service.py # Article processing
│   │   ├── tts_service.py     # Text-to-speech
│   │   ├── s3_service.py      # AWS S3 operations
│   │   └── html_service.py    # HTML processing
│   ├── utils/
│   │   └── helpers.py         # Utility functions
│   └── main.py               # FastAPI application
├── requirements.txt          # Python dependencies
├── setup.py                  # Package setup
├── env.example              # Environment template
└── README.md                # This file
```

## 🛠️ Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd suvichaar-fastapi-service
```

### 2. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Environment Configuration

Copy the environment template and configure your credentials:

```bash
cp env.example .env
```

Edit `.env` with your actual values:

```env
# Azure OpenAI Configuration
AZURE_OPENAI_ENDPOINT=https://your-azure-openai.openai.azure.com/
AZURE_OPENAI_API_KEY=your-azure-openai-key-here
AZURE_OPENAI_API_VERSION=2024-02-01

# Azure Speech/TTS Configuration  
AZURE_TTS_URL=https://your-region.tts.speech.microsoft.com/cognitiveservices/v1
AZURE_API_KEY=your-azure-speech-key-here

# AWS Configuration
AWS_ACCESS_KEY=your-aws-access-key-here
AWS_SECRET_KEY=your-aws-secret-key-here
AWS_REGION=us-east-1
AWS_BUCKET=suvichaarapp
S3_PREFIX=media/
CDN_BASE=https://media.suvichaar.org/
```

## 🚀 Running the Service

### Development Mode

```bash
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Production Mode

```bash
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

The API will be available at:
- **API**: http://localhost:8000
- **Documentation**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 📚 API Endpoints

### Core Functionality

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/generate-article` | POST | Generate article content (Tab 1) |
| `/api/v1/generate-tts` | POST | Generate TTS and upload (Tab 2) |
| `/api/v1/process-html` | POST | Process HTML templates (Tab 3) |
| `/api/v1/generate-amp` | POST | Generate AMP HTML (Tab 4) |
| `/api/v1/submit-content` | POST | Submit content for publishing (Tab 5) |
| `/api/v1/generate-cover-image` | POST | Generate cover image (Tab 6) |

### Utility Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/generate-metadata` | POST | Generate SEO metadata |
| `/api/v1/upload-file` | POST | Upload files to S3 |
| `/api/v1/download-zip` | POST | Create and download ZIP files |
| `/api/v1/voice-options` | GET | Get available voice options |
| `/api/v1/user-mapping` | GET | Get user mapping |
| `/api/v1/category-mapping` | GET | Get category mapping |
| `/api/v1/health` | GET | Health check |

## 🔧 Usage Examples

### 1. Generate Article Content

```python
import requests

response = requests.post("http://localhost:8000/api/v1/generate-article", json={
    "url": "https://example.com/news-article",
    "persona": "genz",
    "content_language": "English",
    "number_of_slides": 10
})

data = response.json()
print(data["structured_output"])
```

### 2. Generate TTS

```python
response = requests.post("http://localhost:8000/api/v1/generate-tts", json={
    "structured_slides": {
        "storytitle": "Breaking News",
        "s1paragraph1": "First slide content",
        "hookline": "This will surprise you!"
    },
    "voice": "alloy"
})

data = response.json()
print(data["tts_output"])
```

### 3. Submit Content for Publishing

```python
response = requests.post("http://localhost:8000/api/v1/submit-content", json={
    "story_title": "Amazing Story",
    "meta_description": "SEO description",
    "meta_keywords": "news, story, amazing",
    "content_type": "News",
    "language": "en-US",
    "image_url": "https://example.com/image.jpg",
    "categories": "Entertainment",
    "filter_tags": "news, entertainment",
    "prefinal_html": "<html>...</html>"
})

data = response.json()
print(f"Story URL: {data['story_url']}")
```

## 🧪 Testing

Run the test suite:

```bash
pytest
```

Run with coverage:

```bash
pytest --cov=app
```

## 📝 API Documentation

Once the service is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🔒 Security Considerations

- All API keys and secrets are managed through environment variables
- CORS is configured for specific origins
- File uploads have size and type restrictions
- Input validation using Pydantic models

## 🚀 Deployment

### Docker Deployment

Create a `Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Build and run:

```bash
docker build -t suvichaar-api .
docker run -p 8000:8000 --env-file .env suvichaar-api
```

### Cloud Deployment

The service is ready for deployment on:
- **AWS**: EC2, ECS, Lambda
- **Google Cloud**: Cloud Run, App Engine
- **Azure**: Container Instances, App Service
- **Heroku**: Direct deployment

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🆘 Support

For support and questions:
- Create an issue in the repository

## 🔄 Migration from Streamlit

This FastAPI service provides 100% feature parity with the original Streamlit application:

- All 6 tabs functionality is available as API endpoints
- Same Azure OpenAI and Azure Speech integrations
- Same AWS S3 operations
- Same HTML processing and AMP generation
- Same metadata and publishing workflows

The main difference is that instead of a web UI, you now have RESTful APIs that can be integrated into any application or frontend framework.
