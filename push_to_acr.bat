@echo off
REM Suvichaar FastAPI Service - Docker Build and Push Script (Windows)
REM This script builds the Docker image locally and pushes it to Azure Container Registry (ACR)

setlocal enabledelayedexpansion

REM Configuration - UPDATE THESE VALUES
set IMAGE_NAME=suvichaar-fastapi-service
set ACR_NAME=your-acr-name
set TAG=v3
set REGISTRY=%ACR_NAME%.azurecr.io
set FULL_IMAGE_NAME=%REGISTRY%/%IMAGE_NAME%:%TAG%

echo.
echo 🐳 Suvichaar FastAPI Service - Docker Build ^& Push Script
echo ======================================================
echo.

REM Check if Docker is running
docker info >nul 2>&1
if errorlevel 1 (
    echo ❌ Docker is not running. Please start Docker Desktop.
    pause
    exit /b 1
)

echo ✅ Docker is running

REM Check if .env file exists
if not exist ".env" (
    echo ⚠️  .env file not found. Creating from env.example...
    if exist "env.example" (
        copy env.example .env >nul
        echo ⚠️  Please update .env file with your actual credentials before proceeding.
        pause
    ) else (
        echo ❌ env.example file not found. Please create .env file manually.
        pause
        exit /b 1
    )
)

REM Check if ACR name is set
if "%ACR_NAME%"=="your-acr-name" (
    echo ❌ Please update ACR_NAME in this script with your actual ACR name.
    echo ℹ️  Edit this script and replace 'your-acr-name' with your ACR name.
    pause
    exit /b 1
)

REM Login to ACR
echo ℹ️  Logging into Azure Container Registry...
az acr login --name %ACR_NAME%

REM Build the Docker image
echo ℹ️  Building Docker image: %IMAGE_NAME%:%TAG%
docker build -t %IMAGE_NAME%:%TAG% .

if errorlevel 1 (
    echo ❌ Docker build failed!
    pause
    exit /b 1
)

echo ✅ Docker image built successfully!

REM Tag the image for ACR
echo ℹ️  Tagging image for ACR: %FULL_IMAGE_NAME%
docker tag %IMAGE_NAME%:%TAG% %FULL_IMAGE_NAME%

REM Test the image locally (optional)
echo ℹ️  Testing the image locally...
docker run --rm -d --name test-container -p 8001:8000 %IMAGE_NAME%:%TAG%

REM Wait for container to start
timeout /t 10 /nobreak >nul

REM Test health endpoint
curl -f http://localhost:8001/api/v1/health >nul 2>&1
if errorlevel 1 (
    echo ⚠️  Local test failed. Service might not be ready yet.
) else (
    echo ✅ Local test successful! Service is running.
)

REM Stop test container
docker stop test-container >nul 2>&1

REM Push to ACR
echo ℹ️  Pushing image to ACR: %FULL_IMAGE_NAME%
docker push %FULL_IMAGE_NAME%

if errorlevel 1 (
    echo ❌ Failed to push image to ACR!
    pause
    exit /b 1
)

echo ✅ Image pushed to ACR successfully!

echo.
echo ℹ️  Build and push completed successfully!
echo ℹ️  Image: %IMAGE_NAME%:%TAG%
echo ℹ️  ACR Image: %FULL_IMAGE_NAME%
echo.
echo ℹ️  To run locally:
echo ℹ️    docker run -p 8000:8000 --env-file .env %IMAGE_NAME%:%TAG%
echo.
echo ℹ️  To run with docker-compose:
echo ℹ️    docker-compose up -d
echo.
echo ℹ️  To deploy from ACR:
echo ℹ️    docker pull %FULL_IMAGE_NAME%
echo ℹ️    docker run -p 8000:8000 --env-file .env %FULL_IMAGE_NAME%
echo.

pause
