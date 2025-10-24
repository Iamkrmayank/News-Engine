#!/usr/bin/env python3
"""
Docker Configuration Validator
Validates Docker files and configuration for Suvichaar FastAPI Service
"""

import os
import sys
from pathlib import Path

def check_file_exists(file_path, description):
    """Check if a file exists and print status"""
    if os.path.exists(file_path):
        print(f"✅ {description}: {file_path}")
        return True
    else:
        print(f"❌ {description}: {file_path} - NOT FOUND")
        return False

def check_dockerfile_syntax():
    """Check Dockerfile syntax"""
    dockerfile_path = "Dockerfile"
    if not os.path.exists(dockerfile_path):
        print("❌ Dockerfile not found")
        return False
    
    try:
        with open(dockerfile_path, 'r') as f:
            content = f.read()
        
        # Basic syntax checks
        if "FROM" not in content:
            print("❌ Dockerfile missing FROM instruction")
            return False
        
        if "CMD" not in content and "ENTRYPOINT" not in content:
            print("❌ Dockerfile missing CMD or ENTRYPOINT")
            return False
        
        if "EXPOSE" not in content:
            print("❌ Dockerfile missing EXPOSE instruction")
            return False
        
        print("✅ Dockerfile syntax looks good")
        return True
        
    except Exception as e:
        print(f"❌ Error reading Dockerfile: {e}")
        return False

def check_dockerignore():
    """Check .dockerignore file"""
    dockerignore_path = ".dockerignore"
    if not os.path.exists(dockerignore_path):
        print("❌ .dockerignore not found")
        return False
    
    try:
        with open(dockerignore_path, 'r') as f:
            content = f.read()
        
        # Check for important exclusions
        important_exclusions = [
            "__pycache__",
            "venv",
            ".env",
            "*.pyc",
            "*.log",
            "temp",
            "tests"
        ]
        
        missing_exclusions = []
        for exclusion in important_exclusions:
            if exclusion not in content:
                missing_exclusions.append(exclusion)
        
        if missing_exclusions:
            print(f"⚠️  .dockerignore missing some exclusions: {missing_exclusions}")
        else:
            print("✅ .dockerignore looks comprehensive")
        
        return True
        
    except Exception as e:
        print(f"❌ Error reading .dockerignore: {e}")
        return False

def check_requirements():
    """Check requirements.txt"""
    req_path = "requirements.txt"
    if not os.path.exists(req_path):
        print("❌ requirements.txt not found")
        return False
    
    try:
        with open(req_path, 'r') as f:
            content = f.read()
        
        # Check for essential packages
        essential_packages = [
            "fastapi",
            "uvicorn",
            "pydantic"
        ]
        
        missing_packages = []
        for package in essential_packages:
            if package not in content.lower():
                missing_packages.append(package)
        
        if missing_packages:
            print(f"❌ requirements.txt missing essential packages: {missing_packages}")
            return False
        else:
            print("✅ requirements.txt contains essential packages")
            return True
        
    except Exception as e:
        print(f"❌ Error reading requirements.txt: {e}")
        return False

def check_app_structure():
    """Check app directory structure"""
    app_dir = Path("app")
    if not app_dir.exists():
        print("❌ app directory not found")
        return False
    
    required_files = [
        "app/main.py",
        "app/api/routes.py",
        "app/core/config.py",
        "app/models/schemas.py"
    ]
    
    missing_files = []
    for file_path in required_files:
        if not os.path.exists(file_path):
            missing_files.append(file_path)
    
    if missing_files:
        print(f"❌ Missing required app files: {missing_files}")
        return False
    else:
        print("✅ App directory structure looks good")
        return True

def main():
    """Main validation function"""
    print("🐳 Suvichaar FastAPI Service - Docker Configuration Validator")
    print("=" * 60)
    
    all_good = True
    
    # Check essential files
    files_to_check = [
        ("Dockerfile", "Docker build file"),
        (".dockerignore", "Docker ignore file"),
        ("docker-compose.yml", "Docker Compose file"),
        ("docker-compose.prod.yml", "Production Docker Compose file"),
        ("requirements.txt", "Python dependencies"),
        ("start.py", "Startup script"),
        (".env", "Environment file (optional)")
    ]
    
    for file_path, description in files_to_check:
        if not check_file_exists(file_path, description):
            if file_path != ".env":  # .env is optional
                all_good = False
    
    print("\n" + "=" * 60)
    
    # Check file contents
    if not check_dockerfile_syntax():
        all_good = False
    
    if not check_dockerignore():
        all_good = False
    
    if not check_requirements():
        all_good = False
    
    if not check_app_structure():
        all_good = False
    
    print("\n" + "=" * 60)
    
    if all_good:
        print("🎉 All Docker configuration checks passed!")
        print("\nNext steps:")
        print("1. Start Docker Desktop")
        print("2. Run: docker build -t suvichaar-fastapi-service:latest .")
        print("3. Test: docker run -p 8000:8000 --env-file .env suvichaar-fastapi-service:latest")
        print("4. Update ACR name in build scripts")
        print("5. Push to ACR when ready")
    else:
        print("❌ Some issues found. Please fix them before building Docker image.")
    
    return all_good

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
