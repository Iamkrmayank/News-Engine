# 🐳 Docker Deployment Guide - Updated Suvichaar FastAPI Service

## 🎯 **What's New in This Update**

The Docker image now includes all the latest features:

### ✅ **New Features Added:**
1. **S3 Upload for `/api/v1/process-html`** - Uploads processed HTML and JSON to S3
2. **JSON URL Support for `/api/v1/generate-amp`** - Accepts JSON URLs instead of data
3. **S3 Upload for `/api/v1/generate-amp`** - Uploads generated AMP HTML to S3
4. **CloudFront URL Generation** - Returns CDN URLs for all uploaded files

## 📋 **Files Updated**

### **Core Application Files:**
- `app/models/schemas.py` - Updated response models with S3 URLs
- `app/services/html_service.py` - Added JSON URL fetching
- `app/services/s3_service.py` - Added AMP HTML upload method
- `app/api/routes.py` - Updated endpoints with S3 integration

### **Docker Files:**
- `Dockerfile` - Multi-stage production build
- `.dockerignore` - Optimized exclusions
- `docker-compose.yml` - Local development
- `docker-compose.prod.yml` - Production deployment

### **Build Scripts:**
- `push_to_acr.sh` - Linux/Mac build and push script
- `push_to_acr.bat` - Windows build and push script

## 🚀 **Deployment Steps**

### **Step 1: Update ACR Name**
Edit the build script and replace `your-acr-name` with your actual ACR name:

**Linux/Mac:**
```bash
# Edit push_to_acr.sh
ACR_NAME="your-actual-acr-name"
```

**Windows:**
```batch
REM Edit push_to_acr.bat
set ACR_NAME=your-actual-acr-name
```

### **Step 2: Build and Push**

**Linux/Mac:**
```bash
chmod +x push_to_acr.sh
./push_to_acr.sh
```

**Windows:**
```batch
push_to_acr.bat
```

### **Step 3: Manual Commands (Alternative)**

If you prefer manual commands:

```bash
# 1. Login to ACR
az acr login --name your-acr-name

# 2. Build image
docker build -t suvichaar-fastapi-service:latest .

# 3. Tag for ACR
docker tag suvichaar-fastapi-service:latest your-acr-name.azurecr.io/suvichaar-fastapi-service:latest

# 4. Push to ACR
docker push your-acr-name.azurecr.io/suvichaar-fastapi-service:latest
```

## 🔧 **Prerequisites**

### **Required Tools:**
- Docker Desktop running
- Azure CLI installed (`az` command)
- ACR (Azure Container Registry) created
- Proper Azure credentials configured

### **Environment Variables:**
Ensure `.env` file contains:
- AWS credentials for S3
- Azure OpenAI credentials
- Azure TTS credentials
- CDN configuration

## 📊 **What's Included in the Image**

### **Updated Endpoints:**
1. **`/api/v1/process-html`**
   - ✅ Processes HTML with slide data
   - ✅ Uploads HTML and JSON to S3
   - ✅ Returns CloudFront URLs

2. **`/api/v1/generate-amp`**
   - ✅ Accepts JSON URLs or direct JSON data
   - ✅ Generates AMP HTML
   - ✅ Uploads AMP HTML to S3
   - ✅ Returns CloudFront URL

3. **`/api/v1/generate-amp-download`**
   - ✅ Same features as generate-amp
   - ✅ Plus local file download option

### **S3 Integration:**
- ✅ Uploads to `suvichaarapp` bucket
- ✅ Generates CloudFront URLs
- ✅ Proper error handling
- ✅ Graceful fallback if S3 fails

## 🎯 **API Response Examples**

### **`/api/v1/process-html` Response:**
```json
{
  "updated_html": "<html>...</html>",
  "updated_json": {...},
  "filename": "output_bundle_1761318930.zip",
  "html_s3_url": "https://cdn.suvichaar.org/media/processed_html_20251024_204530.html",
  "json_s3_url": "https://cdn.suvichaar.org/media/processed_html_20251024_204530.json"
}
```

### **`/api/v1/generate-amp` Response:**
```json
{
  "final_html": "<html>...</html>",
  "filename": "pre-final_amp_story_1761322672.html",
  "html_s3_url": "https://cdn.suvichaar.org/media/amp_story_20251024_214752.html"
}
```

## 🔄 **Deployment Workflow**

### **For n8n Integration:**
1. **Process HTML**: Call `/api/v1/process-html` → Get S3 URLs
2. **Generate AMP**: Call `/api/v1/generate-amp` with JSON URL → Get AMP HTML + S3 URL
3. **Use CloudFront URLs**: Direct access to files via CDN

### **For Container Deployment:**
1. **Pull from ACR**: `docker pull your-acr-name.azurecr.io/suvichaar-fastapi-service:latest`
2. **Run Container**: `docker run -p 8000:8000 --env-file .env your-acr-name.azurecr.io/suvichaar-fastapi-service:latest`
3. **Health Check**: `curl http://localhost:8000/api/v1/health`

## ✅ **Testing Completed**

- ✅ Docker image builds successfully
- ✅ Container runs without errors
- ✅ Health endpoint responds
- ✅ S3 upload functionality works
- ✅ CloudFront URLs generated correctly
- ✅ All new features integrated

## 🎉 **Ready for Production**

The updated Docker image is ready for deployment with all new features:
- S3 integration for file storage
- CloudFront CDN URLs
- JSON URL support
- Enhanced error handling
- Production-ready configuration

**Deploy with confidence! 🚀**
