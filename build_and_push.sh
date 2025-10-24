#!/bin/bash

# Suvichaar FastAPI Service - Docker Build and Push Script
# This script builds the Docker image locally and pushes it to Azure Container Registry (ACR)

set -e  # Exit on any error

# Configuration
IMAGE_NAME="suvichaar-fastapi-service"
ACR_NAME="your-acr-name"  # Replace with your ACR name
TAG="latest"
REGISTRY="${ACR_NAME}.azurecr.io"
FULL_IMAGE_NAME="${REGISTRY}/${IMAGE_NAME}:${TAG}"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🐳 Suvichaar FastAPI Service - Docker Build & Push Script${NC}"
echo -e "${BLUE}======================================================${NC}"

# Function to print colored output
print_status() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    print_error "Docker is not running. Please start Docker Desktop."
    exit 1
fi

print_status "Docker is running"

# Check if .env file exists
if [ ! -f ".env" ]; then
    print_warning ".env file not found. Creating from env.example..."
    if [ -f "env.example" ]; then
        cp env.example .env
        print_warning "Please update .env file with your actual credentials before proceeding."
        read -p "Press Enter to continue after updating .env file..."
    else
        print_error "env.example file not found. Please create .env file manually."
        exit 1
    fi
fi

# Login to ACR (uncomment when ready to push to ACR)
# print_info "Logging into Azure Container Registry..."
# az acr login --name $ACR_NAME

# Build the Docker image
print_info "Building Docker image: ${IMAGE_NAME}:${TAG}"
docker build -t ${IMAGE_NAME}:${TAG} .

if [ $? -eq 0 ]; then
    print_status "Docker image built successfully!"
else
    print_error "Docker build failed!"
    exit 1
fi

# Tag the image for ACR
print_info "Tagging image for ACR: ${FULL_IMAGE_NAME}"
docker tag ${IMAGE_NAME}:${TAG} ${FULL_IMAGE_NAME}

# Test the image locally (optional)
print_info "Testing the image locally..."
docker run --rm -d --name test-container -p 8001:8000 ${IMAGE_NAME}:${TAG}

# Wait for container to start
sleep 10

# Test health endpoint
if curl -f http://localhost:8001/api/v1/health > /dev/null 2>&1; then
    print_status "Local test successful! Service is running."
else
    print_warning "Local test failed. Service might not be ready yet."
fi

# Stop test container
docker stop test-container > /dev/null 2>&1

# Push to ACR (uncomment when ready)
# print_info "Pushing image to ACR: ${FULL_IMAGE_NAME}"
# docker push ${FULL_IMAGE_NAME}

# if [ $? -eq 0 ]; then
#     print_status "Image pushed to ACR successfully!"
# else
#     print_error "Failed to push image to ACR!"
#     exit 1
# fi

print_info "Build completed successfully!"
print_info "Image: ${IMAGE_NAME}:${TAG}"
print_info "ACR Image: ${FULL_IMAGE_NAME}"
print_info ""
print_info "To run locally:"
print_info "  docker run -p 8000:8000 --env-file .env ${IMAGE_NAME}:${TAG}"
print_info ""
print_info "To run with docker-compose:"
print_info "  docker-compose up -d"
print_info ""
print_info "To push to ACR (uncomment the push commands in this script):"
print_info "  az acr login --name ${ACR_NAME}"
print_info "  docker push ${FULL_IMAGE_NAME}"
