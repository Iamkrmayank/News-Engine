# 🐳 Suvichaar FastAPI Service - Docker Deployment Guide

This guide covers building, testing, and deploying the Suvichaar FastAPI service using Docker.

## 📁 Files Created

- `Dockerfile` - Multi-stage Docker build configuration
- `.dockerignore` - Excludes unnecessary files from Docker context
- `docker-compose.yml` - Local development setup
- `docker-compose.prod.yml` - Production deployment configuration
- `build_and_push.sh` - Linux/Mac build script
- `build_and_push.bat` - Windows build script

## 🚀 Quick Start

### 1. Local Development

```bash
# Build and run locally
docker-compose up -d

# Check logs
docker-compose logs -f

# Stop services
docker-compose down
```

### 2. Production Deployment

```bash
# Build and run production
docker-compose -f docker-compose.prod.yml up -d

# Check logs
docker-compose -f docker-compose.prod.yml logs -f
```

## 🔧 Manual Docker Commands

### Build Image
```bash
docker build -t suvichaar-fastapi-service:latest .
```

### Run Container
```bash
docker run -p 8000:8000 --env-file .env suvichaar-fastapi-service:latest
```

### Test Health
```bash
curl http://localhost:8000/api/v1/health
```

## 📋 Prerequisites

1. **Docker Desktop** installed and running
2. **Azure CLI** installed (for ACR push)
3. **Environment file** (.env) configured
4. **Azure Container Registry** created

## 🔐 Environment Configuration

Create a `.env` file with the following variables:

```env
# Azure OpenAI
AZURE_OPENAI_ENDPOINT=your_endpoint
AZURE_OPENAI_API_KEY=your_key
AZURE_OPENAI_API_VERSION=2024-02-01
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4

# Azure Speech/TTS
AZURE_TTS_URL=your_tts_url
AZURE_API_KEY=your_api_key

# AWS S3
AWS_ACCESS_KEY=your_access_key
AWS_SECRET_KEY=your_secret_key
AWS_REGION=us-east-1
AWS_BUCKET=your_bucket
CDN_BASE=your_cdn_base
```

## 🏗️ Docker Image Details

### Multi-Stage Build
- **Builder Stage**: Installs dependencies and creates virtual environment
- **Production Stage**: Minimal runtime with only necessary files

### Security Features
- Non-root user execution
- Minimal attack surface
- Health checks included
- Resource limits in production

### Image Size Optimization
- Multi-stage build reduces final image size
- Only production dependencies included
- Virtual environment copied from builder stage

## 🌐 Azure Container Registry (ACR) Deployment

### 1. Create ACR
```bash
az acr create --resource-group your-rg --name your-acr-name --sku Basic
```

### 2. Login to ACR
```bash
az acr login --name your-acr-name
```

### 3. Build and Push
```bash
# Update ACR name in build script
./build_and_push.sh

# Or manually:
docker tag suvichaar-fastapi-service:latest your-acr-name.azurecr.io/suvichaar-fastapi-service:latest
docker push your-acr-name.azurecr.io/suvichaar-fastapi-service:latest
```

### 4. Deploy from ACR
```bash
docker pull your-acr-name.azurecr.io/suvichaar-fastapi-service:latest
docker run -p 8000:8000 --env-file .env your-acr-name.azurecr.io/suvichaar-fastapi-service:latest
```

## 🔄 Route Changes and Updates

When you need to make changes to routes:

### 1. Update Code
```bash
# Make your changes to app/api/routes.py
# Test locally
python start.py
```

### 2. Rebuild Docker Image
```bash
# Build new image
docker build -t suvichaar-fastapi-service:latest .

# Test locally
docker run -p 8000:8000 --env-file .env suvichaar-fastapi-service:latest
```

### 3. Push to ACR
```bash
# Push updated image
docker push your-acr-name.azurecr.io/suvichaar-fastapi-service:latest
```

### 4. Deploy Updated Image
```bash
# Pull and run updated image
docker pull your-acr-name.azurecr.io/suvichaar-fastapi-service:latest
docker run -p 8000:8000 --env-file .env your-acr-name.azurecr.io/suvichaar-fastapi-service:latest
```

## 📊 Monitoring and Health Checks

### Health Check Endpoint
```bash
curl http://localhost:8000/api/v1/health
```

### Container Health Status
```bash
docker ps
docker inspect <container_id> | grep Health
```

### Logs
```bash
# Container logs
docker logs <container_id>

# Follow logs
docker logs -f <container_id>

# Docker Compose logs
docker-compose logs -f
```

## 🚨 Troubleshooting

### Common Issues

1. **Port Already in Use**
   ```bash
   # Find process using port 8000
   netstat -ano | findstr :8000
   
   # Kill process (Windows)
   taskkill /PID <PID> /F
   ```

2. **Environment Variables Not Loading**
   ```bash
   # Check .env file exists
   ls -la .env
   
   # Verify environment variables
   docker run --env-file .env suvichaar-fastapi-service:latest env
   ```

3. **Build Failures**
   ```bash
   # Clean Docker cache
   docker system prune -a
   
   # Rebuild without cache
   docker build --no-cache -t suvichaar-fastapi-service:latest .
   ```

4. **ACR Push Failures**
   ```bash
   # Re-login to ACR
   az acr login --name your-acr-name
   
   # Check ACR permissions
   az acr show --name your-acr-name
   ```

## 📈 Performance Optimization

### Production Settings
- Resource limits configured in `docker-compose.prod.yml`
- Health checks for automatic restart
- Non-root user for security
- Minimal image size

### Scaling
```bash
# Scale to multiple instances
docker-compose -f docker-compose.prod.yml up -d --scale suvichaar-api=3
```

## 🔒 Security Best Practices

1. **Non-root User**: Container runs as non-root user
2. **Minimal Image**: Only necessary files included
3. **Environment Variables**: Sensitive data via environment variables
4. **Health Checks**: Automatic container health monitoring
5. **Resource Limits**: Prevents resource exhaustion

## 📝 Next Steps

1. **Update ACR Name**: Replace `your-acr-name` in build scripts
2. **Configure Environment**: Set up `.env` file with actual credentials
3. **Test Locally**: Run `docker-compose up -d` to test
4. **Push to ACR**: Use build scripts to push to Azure
5. **Deploy**: Pull and run from ACR in your target environment

## 🆘 Support

For issues or questions:
1. Check Docker logs: `docker logs <container_id>`
2. Verify environment variables
3. Test health endpoint
4. Check ACR connectivity
5. Review this documentation
