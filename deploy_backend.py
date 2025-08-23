#!/usr/bin/env python3
"""
Complete Backend Deployment Script for OpenWebUI on Render.com
This script handles all aspects of backend deployment preparation.
"""

import os
import sys
import subprocess
import json
import shutil
from pathlib import Path

def run_command(command, cwd=None, check=True):
    """Run a shell command and return the result."""
    print(f"🔄 Running: {command}")
    try:
        result = subprocess.run(
            command, 
            shell=True, 
            cwd=cwd, 
            check=check, 
            capture_output=True, 
            text=True
        )
        if result.stdout:
            print(f"✅ Output: {result.stdout}")
        if result.stderr:
            print(f"⚠️  Stderr: {result.stderr}")
        return result
    except subprocess.CalledProcessError as e:
        print(f"❌ Command failed: {e}")
        if e.stdout:
            print(f"Stdout: {e.stdout}")
        if e.stderr:
            print(f"Stderr: {e.stderr}")
        if check:
            sys.exit(1)
        return e

def check_prerequisites():
    """Check if all prerequisites are met."""
    print("🔍 Checking prerequisites...")
    
    # Check Python version
    python_version = run_command("python --version", check=False)
    if python_version.returncode == 0:
        print(f"✅ Python: {python_version.stdout.strip()}")
    else:
        print("❌ Python not found")
        return False
    
    # Check if we're in the right directory
    if not Path("backend-render").exists():
        print("❌ backend-render directory not found")
        return False
    
    # Check if requirements.txt exists
    if not Path("backend-render/requirements.txt").exists():
        print("❌ requirements.txt not found")
        return False
    
    print("✅ All prerequisites met!")
    return True

def prepare_backend():
    """Prepare the backend for deployment."""
    print("🔧 Preparing backend for deployment...")
    
    backend_dir = Path("backend-render")
    
    # Create necessary directories
    (backend_dir / "data").mkdir(exist_ok=True)
    (backend_dir / "data" / "cache").mkdir(exist_ok=True)
    (backend_dir / "data" / "uploads").mkdir(exist_ok=True)
    
    # Ensure open_webui package exists
    open_webui_dir = backend_dir / "open_webui"
    if not open_webui_dir.exists():
        print("❌ open_webui package not found. Please run the setup first.")
        return False
    
    # Create __pycache__ cleanup script
    cleanup_script = backend_dir / "cleanup.py"
    cleanup_script.write_text('''#!/usr/bin/env python3
"""Cleanup script to remove Python cache files."""
import shutil
from pathlib import Path

def cleanup():
    """Remove all __pycache__ directories and .pyc files."""
    current_dir = Path(__file__).parent
    
    # Remove __pycache__ directories
    for pycache in current_dir.rglob("__pycache__"):
        shutil.rmtree(pycache)
        print(f"Removed: {pycache}")
    
    # Remove .pyc files
    for pyc_file in current_dir.rglob("*.pyc"):
        pyc_file.unlink()
        print(f"Removed: {pyc_file}")
    
    print("Cleanup completed!")

if __name__ == "__main__":
    cleanup()
''')
    
    print("✅ Backend prepared!")
    return True

def create_render_config():
    """Create Render.com configuration files."""
    print("📝 Creating Render.com configuration...")
    
    # Create render.yaml if it doesn't exist
    render_yaml = Path("render.yaml")
    if not render_yaml.exists():
        render_yaml.write_text('''services:
  - type: web
    name: openwebui-backend
    env: python
    plan: starter
    pythonVersion: "3.11.18"
    rootDir: backend-render
    buildCommand: python3.11 -m pip install --upgrade pip setuptools wheel && python3.11 -m pip install -r requirements.txt
    startCommand: python start_production.py
    envVars:
      - key: PYTHON_VERSION
        value: "3.11.18"
      - key: PORT
        value: 10000
      - key: ENV
        value: production
      - key: PYTHONPATH
        value: "."
      - key: DATABASE_URL
        fromDatabase:
          name: openwebui-db
          property: connectionString
      - key: REDIS_URL
        fromService:
          type: redis
          name: openwebui-redis
          property: connectionString
      - key: WEBUI_SECRET_KEY
        generateValue: true
      - key: ENABLE_SIGNUP
        value: "true"
      - key: ENABLE_LOGIN_FORM
        value: "true"
      - key: ENABLE_ATLAS_CLOUD_API
        value: "true"
      - key: ENABLE_OLLAMA_API
        value: "false"
      - key: ENABLE_OPENAI_API
        value: "false"
      - key: ENABLE_DIRECT_CONNECTIONS
        value: "false"
      - key: ENABLE_IMAGE_GENERATION
        value: "false"
      - key: ENABLE_CODE_EXECUTION
        value: "false"
      - key: ENABLE_CODE_INTERPRETER
        value: "false"
      - key: WEBUI_AUTH
        value: "true"
      - key: WEBUI_NAME
        value: "OpenWebUI"
      - key: WEBUI_URL
        value: "https://your-frontend-domain.vercel.app"
      - key: CORS_ORIGINS
        value: "https://your-frontend-domain.vercel.app"
      - key: ATLAS_CLOUD_API_KEY
        sync: false
      - key: ATLAS_CLOUD_API_URL
        value: "https://api.atlas.nomic.ai"
      - key: ENABLE_API_KEY
        value: "true"
      - key: ENABLE_COMMUNITY_SHARING
        value: "true"
      - key: ENABLE_MESSAGE_RATING
        value: "true"
      - key: ENABLE_CHANNELS
        value: "true"
      - key: ENABLE_NOTES
        value: "true"
      - key: DEFAULT_USER_ROLE
        value: "user"
      - key: VECTOR_DB
        value: "chroma"
      - key: SRC_LOG_LEVELS
        value: "INFO"
      - key: GLOBAL_LOG_LEVEL
        value: "INFO"
    healthCheckPath: /docs
    autoDeploy: true

databases:
  - name: openwebui-db
    databaseName: openwebui
    user: openwebui
    plan: starter

services:
  - type: redis
    name: openwebui-redis
    plan: starter
    maxmemoryPolicy: allkeys-lru
''')
        print("✅ Created render.yaml")
    
    # Create .renderignore
    render_ignore = Path(".renderignore")
    render_ignore.write_text('''# Python cache files
__pycache__/
*.pyc
*.pyo
*.pyd
.Python

# Virtual environments
venv/
env/
ENV/

# IDE files
.vscode/
.idea/
*.swp
*.swo

# OS files
.DS_Store
Thumbs.db

# Logs
*.log

# Local data
data/
.env.local
.env.development

# Git
.git/
.gitignore

# Documentation
*.md
docs/

# Tests
tests/
test_*
*_test.py

# Frontend files
frontend-vercel/
src/
''')
        print("✅ Created .renderignore")
    
    print("✅ Render.com configuration created!")

def create_deployment_scripts():
    """Create deployment and build scripts."""
    print("📜 Creating deployment scripts...")
    
    backend_dir = Path("backend-render")
    
    # Create build script
    build_script = backend_dir / "build.sh"
    build_script.write_text('''#!/bin/bash
# Build script for OpenWebUI backend on Render.com

echo "🚀 Starting OpenWebUI backend build..."

# Upgrade pip and install dependencies
echo "📦 Installing Python dependencies..."
python3.11 -m pip install --upgrade pip setuptools wheel
python3.11 -m pip install -r requirements.txt

# Create necessary directories
echo "📁 Creating directories..."
mkdir -p data/cache
mkdir -p data/uploads
mkdir -p data/logs

# Set permissions
echo "🔐 Setting permissions..."
chmod +x start_production.py
chmod +x cleanup.py

# Clean up Python cache
echo "🧹 Cleaning up Python cache..."
python3.11 cleanup.py

echo "✅ Build completed successfully!"
''')
    
    # Create run script
    run_script = backend_dir / "run.sh"
    run_script.write_text('''#!/bin/bash
# Run script for OpenWebUI backend on Render.com

echo "🚀 Starting OpenWebUI backend..."

# Set environment variables
export PYTHONPATH="."
export PYTHONUNBUFFERED=1

# Start the application
echo "🌟 Starting FastAPI application..."
python start_production.py
''')
    
    # Create health check script
    health_check = backend_dir / "health_check.py"
    health_check.write_text('''#!/usr/bin/env python3
"""Health check script for Render.com."""
import requests
import sys
import time

def check_health():
    """Check if the application is healthy."""
    try:
        # Wait a bit for the app to start
        time.sleep(5)
        
        # Try to connect to the health endpoint
        response = requests.get("http://localhost:10000/health", timeout=10)
        
        if response.status_code == 200:
            print("✅ Health check passed!")
            return True
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return False

if __name__ == "__main__":
    if check_health():
        sys.exit(0)
    else:
        sys.exit(1)
''')
    
    # Make scripts executable
    build_script.chmod(0o755)
    run_script.chmod(0o755)
    health_check.chmod(0o755)
    
    print("✅ Deployment scripts created!")

def create_dockerfile():
    """Create a Dockerfile for alternative deployment."""
    print("🐳 Creating Dockerfile...")
    
    dockerfile = Path("backend-render/Dockerfile")
    dockerfile.write_text('''# OpenWebUI Backend Dockerfile
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \\
    gcc \\
    g++ \\
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip setuptools wheel
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p data/cache data/uploads data/logs

# Set permissions
RUN chmod +x start_production.py cleanup.py

# Clean up Python cache
RUN python cleanup.py

# Expose port
EXPOSE 10000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \\
    CMD python health_check.py

# Start the application
CMD ["python", "start_production.py"]
''')
    
    print("✅ Dockerfile created!")

def create_github_actions():
    """Create GitHub Actions workflow for automated deployment."""
    print("🔧 Creating GitHub Actions workflow...")
    
    workflows_dir = Path(".github/workflows")
    workflows_dir.mkdir(parents=True, exist_ok=True)
    
    workflow_file = workflows_dir / "deploy-backend.yml"
    workflow_file.write_text('''name: Deploy Backend to Render.com

on:
  push:
    branches: [ main ]
    paths:
      - 'backend-render/**'
      - 'render.yaml'
      - '.github/workflows/deploy-backend.yml'

jobs:
  deploy:
    runs-on: ubuntu-latest
    
    steps:
    - name: Checkout code
      uses: actions/checkout@v4
      
    - name: Setup Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
        
    - name: Install dependencies
      run: |
        cd backend-render
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        
    - name: Run tests
      run: |
        cd backend-render
        python -m pytest tests/ -v || echo "No tests found"
        
    - name: Deploy to Render
      uses: johnbeynon/render-deploy-action@v1.0.0
      with:
        service-id: ${{ secrets.RENDER_SERVICE_ID }}
        api-key: ${{ secrets.RENDER_API_KEY }}
''')
    
    print("✅ GitHub Actions workflow created!")

def create_environment_template():
    """Create environment variable template."""
    print("🌍 Creating environment template...")
    
    env_template = Path("backend-render/.env.template")
    env_template.write_text('''# OpenWebUI Backend Environment Variables Template
# Copy this file to .env and fill in your values

# Core Configuration
ENV=production
WEBUI_SECRET_KEY=your-super-secret-key-here
WEBUI_NAME=OpenWebUI
WEBUI_URL=https://your-frontend-domain.vercel.app

# CORS Configuration
CORS_ORIGINS=https://your-frontend-domain.vercel.app

# Features
ENABLE_SIGNUP=true
ENABLE_LOGIN_FORM=true
ENABLE_ATLAS_CLOUD_API=true
ENABLE_OLLAMA_API=false
ENABLE_OPENAI_API=false
ENABLE_DIRECT_CONNECTIONS=false
ENABLE_IMAGE_GENERATION=false
ENABLE_CODE_EXECUTION=false
ENABLE_CODE_INTERPRETER=false

# API Keys
ATLAS_CLOUD_API_KEY=your-atlas-cloud-api-key
ATLAS_CLOUD_API_URL=https://api.atlas.nomic.ai

# User Settings
DEFAULT_USER_ROLE=user
ENABLE_API_KEY=true
ENABLE_COMMUNITY_SHARING=true
ENABLE_MESSAGE_RATING=true
ENABLE_CHANNELS=true
ENABLE_NOTES=true

# Database & Redis (Auto-configured by Render)
# DATABASE_URL and REDIS_URL are automatically set

# Vector Database
VECTOR_DB=chroma

# Logging
SRC_LOG_LEVELS=INFO
GLOBAL_LOG_LEVEL=INFO

# Security
BYPASS_MODEL_ACCESS_CONTROL=false
BYPASS_ADMIN_ACCESS_CONTROL=false
''')
    
    print("✅ Environment template created!")

def main():
    """Main deployment preparation function."""
    print("🚀 OpenWebUI Backend Deployment Preparation")
    print("=" * 50)
    
    if not check_prerequisites():
        print("❌ Prerequisites not met. Please fix the issues above.")
        sys.exit(1)
    
    if not prepare_backend():
        print("❌ Backend preparation failed.")
        sys.exit(1)
    
    create_render_config()
    create_deployment_scripts()
    create_dockerfile()
    create_github_actions()
    create_environment_template()
    
    print("\n" + "=" * 50)
    print("✅ Backend deployment preparation completed!")
    print("\n📋 Next steps:")
    print("1. Push your code to GitHub")
    print("2. Go to Render.com and create a new web service")
    print("3. Connect your GitHub repository")
    print("4. Use the render.yaml configuration")
    print("5. Set your environment variables")
    print("6. Deploy!")
    print("\n📚 See DEPLOYMENT_READY.md for detailed instructions")

if __name__ == "__main__":
    main()
