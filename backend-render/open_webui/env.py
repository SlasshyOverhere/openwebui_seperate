"""
Environment configuration for OpenWebUI backend.
This file provides all the environment variables and configuration needed for the backend.
"""

import os
from pathlib import Path
from typing import Optional

# Base directories
OPEN_WEBUI_DIR = Path(__file__).parent.parent
DATA_DIR = Path(os.getenv("DATA_DIR", "./data"))
CACHE_DIR = DATA_DIR / "cache"
UPLOAD_DIR = DATA_DIR / "uploads"
STATIC_DIR = OPEN_WEBUI_DIR / "static"

# Ensure directories exist
DATA_DIR.mkdir(parents=True, exist_ok=True)
CACHE_DIR.mkdir(parents=True, exist_ok=True)
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

# Database configuration
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./data/webui.db")
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
REDIS_KEY_PREFIX = os.getenv("REDIS_KEY_PREFIX", "openwebui")

# WebUI configuration
WEBUI_SECRET_KEY = os.getenv("WEBUI_SECRET_KEY", "your-secret-key-here")
WEBUI_NAME = os.getenv("WEBUI_NAME", "OpenWebUI")
WEBUI_URL = os.getenv("WEBUI_URL", "http://localhost:8000")
WEBUI_AUTH = os.getenv("WEBUI_AUTH", "true").lower() == "true"

# CORS configuration
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "http://localhost:6969,http://127.0.0.1:6969")

# Feature flags
ENABLE_SIGNUP = os.getenv("ENABLE_SIGNUP", "true").lower() == "true"
ENABLE_LOGIN_FORM = os.getenv("ENABLE_LOGIN_FORM", "true").lower() == "true"
ENABLE_API_KEY = os.getenv("ENABLE_API_KEY", "true").lower() == "true"
ENABLE_COMMUNITY_SHARING = os.getenv("ENABLE_COMMUNITY_SHARING", "true").lower() == "true"
ENABLE_MESSAGE_RATING = os.getenv("ENABLE_MESSAGE_RATING", "true").lower() == "true"
ENABLE_CHANNELS = os.getenv("ENABLE_CHANNELS", "true").lower() == "true"
ENABLE_NOTES = os.getenv("ENABLE_NOTES", "true").lower() == "true"
ENABLE_OLLAMA_API = os.getenv("ENABLE_OLLAMA_API", "true").lower() == "true"
ENABLE_OPENAI_API = os.getenv("ENABLE_OPENAI_API", "true").lower() == "true"
ENABLE_DIRECT_CONNECTIONS = os.getenv("ENABLE_DIRECT_CONNECTIONS", "false").lower() == "true"
ENABLE_IMAGE_GENERATION = os.getenv("ENABLE_IMAGE_GENERATION", "false").lower() == "true"
ENABLE_CODE_EXECUTION = os.getenv("ENABLE_CODE_EXECUTION", "false").lower() == "true"
ENABLE_CODE_INTERPRETER = os.getenv("ENABLE_CODE_INTERPRETER", "false").lower() == "true"
ENABLE_ATLAS_CLOUD_API = os.getenv("ENABLE_ATLAS_CLOUD_API", "false").lower() == "true"

# API configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_API_BASE_URL = os.getenv("OPENAI_API_BASE_URL", "https://api.openai.com/v1")
ATLAS_CLOUD_API_KEY = os.getenv("ATLAS_CLOUD_API_KEY", "")
ATLAS_CLOUD_API_URL = os.getenv("ATLAS_CLOUD_API_URL", "https://api.atlas.nomic.ai")

# Ollama configuration
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")

# User configuration
DEFAULT_USER_ROLE = os.getenv("DEFAULT_USER_ROLE", "user")
BYPASS_MODEL_ACCESS_CONTROL = os.getenv("BYPASS_MODEL_ACCESS_CONTROL", "false").lower() == "true"

# Logging configuration
SRC_LOG_LEVELS = os.getenv("SRC_LOG_LEVELS", "INFO")
GLOBAL_LOG_LEVEL = os.getenv("GLOBAL_LOG_LEVEL", "INFO")

# Forward user info headers
ENABLE_FORWARD_USER_INFO_HEADERS = os.getenv("ENABLE_FORWARD_USER_INFO_HEADERS", "false").lower() == "true"

# Vector database configuration
VECTOR_DB = os.getenv("VECTOR_DB", "chroma")

# Environment
ENV = os.getenv("ENV", "development")
