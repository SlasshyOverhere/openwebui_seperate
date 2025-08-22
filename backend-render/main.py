import asyncio
import inspect
import json
import logging
import mimetypes
import os
import shutil
import sys
import time
import random
from uuid import uuid4

from contextlib import asynccontextmanager
from urllib.parse import urlencode, parse_qs, urlparse
from pydantic import BaseModel
from sqlalchemy import text

from typing import Optional
from aiocache import cached
import aiohttp
import anyio.to_thread
import requests
from redis import Redis

from fastapi import (
    Depends,
    FastAPI,
    File,
    Form,
    HTTPException,
    Request,
    UploadFile,
    status,
    applications,
    BackgroundTasks,
)
from fastapi.openapi.docs import get_swagger_ui_html

from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles

from starlette_compress import CompressMiddleware

from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.sessions import SessionMiddleware
from starlette.responses import Response, StreamingResponse
from starlette.datastructures import Headers

# Import OpenWebUI modules
from utils import logger
from utils.audit import AuditLevel, AuditLoggingMiddleware
from utils.logger import start_logger
# Simple socket functionality for chat events
from simple_socket import socket_app, emit_chat_event, get_connected_clients
from routers import (
    audio,
    images,
    ollama,
    openai,
    retrieval,
    pipelines,
    tasks,
    auths,
    channels,
    chats,
    notes,
    folders,
    configs,
    groups,
    files,
    functions,
    memories,
    # models,  # Commented out due to database conflicts
    knowledge,
    prompts,
    evaluations,
    tools,
    users,
    utils,
    scim,
)

from routers.retrieval import (
    get_embedding_function,
    get_reranking_function,
    get_ef,
    get_rf,
)

from internal.db import Session, engine

# Import configuration
import os

# Load environment variables from .env file
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    # If python-dotenv is not available, try to load .env manually
    env_file = Path(__file__).parent / '.env'
    if env_file.exists():
        with open(env_file, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ[key] = value

# Configuration with defaults
ENABLE_OLLAMA_API = os.getenv("ENABLE_OLLAMA_API", "true").lower() == "true"
OLLAMA_BASE_URLS = os.getenv("OLLAMA_BASE_URLS", "http://localhost:11434").split(",")
OLLAMA_API_CONFIGS = {}

ENABLE_OPENAI_API = os.getenv("ENABLE_OPENAI_API", "true").lower() == "true"
ONEDRIVE_CLIENT_ID = os.getenv("ONEDRIVE_CLIENT_ID", "")
ONEDRIVE_SHAREPORT_URL = os.getenv("ONEDRIVE_SHAREPORT_URL", "")
ONEDRIVE_SHAREPORT_TENANT_ID = os.getenv("ONEDRIVE_SHAREPORT_TENANT_ID", "")
OPENAI_API_BASE_URLS = os.getenv("OPENAI_API_BASE_URLS", "").split(",") if os.getenv("OPENAI_API_BASE_URLS") else []
OPENAI_API_KEYS = os.getenv("OPENAI_API_KEYS", "").split(",") if os.getenv("OPENAI_API_KEYS") else []
OPENAI_API_CONFIGS = {}

ENABLE_DIRECT_CONNECTIONS = os.getenv("ENABLE_DIRECT_CONNECTIONS", "true").lower() == "true"
ENABLE_BASE_MODELS_CACHE = os.getenv("ENABLE_BASE_MODELS_CACHE", "true").lower() == "true"
THREAD_POOL_SIZE = int(os.getenv("THREAD_POOL_SIZE", "10"))
TOOL_SERVER_CONNECTIONS = []

ENABLE_CODE_EXECUTION = os.getenv("ENABLE_CODE_EXECUTION", "false").lower() == "true"
CODE_EXECUTION_ENGINE = os.getenv("CODE_EXECUTION_ENGINE", "jupyter")
CODE_EXECUTION_JUPYTER_URL = os.getenv("CODE_EXECUTION_JUPYTER_URL", "")
CODE_EXECUTION_JUPYTER_AUTH = os.getenv("CODE_EXECUTION_JUPYTER_AUTH", "")
CODE_EXECUTION_JUPYTER_AUTH_TOKEN = os.getenv("CODE_EXECUTION_JUPYTER_AUTH_TOKEN", "")
CODE_EXECUTION_JUPYTER_AUTH_PASSWORD = os.getenv("CODE_EXECUTION_JUPYTER_AUTH_PASSWORD", "")
CODE_EXECUTION_JUPYTER_TIMEOUT = int(os.getenv("CODE_EXECUTION_JUPYTER_TIMEOUT", "30"))
ENABLE_CODE_INTERPRETER = os.getenv("ENABLE_CODE_INTERPRETER", "false").lower() == "true"
CODE_INTERPRETER_ENGINE = os.getenv("CODE_INTERPRETER_ENGINE", "jupyter")
CODE_INTERPRETER_PROMPT_TEMPLATE = os.getenv("CODE_INTERPRETER_PROMPT_TEMPLATE", "")
CODE_INTERPRETER_JUPYTER_URL = os.getenv("CODE_INTERPRETER_JUPYTER_URL", "")
CODE_INTERPRETER_JUPYTER_AUTH = os.getenv("CODE_INTERPRETER_JUPYTER_AUTH", "")
CODE_INTERPRETER_JUPYTER_AUTH_TOKEN = os.getenv("CODE_INTERPRETER_JUPYTER_AUTH_TOKEN", "")
CODE_INTERPRETER_JUPYTER_AUTH_PASSWORD = os.getenv("CODE_INTERPRETER_JUPYTER_AUTH_PASSWORD", "")
CODE_INTERPRETER_JUPYTER_TIMEOUT = int(os.getenv("CODE_INTERPRETER_JUPYTER_TIMEOUT", "30"))

AUTOMATIC1111_API_AUTH = os.getenv("AUTOMATIC1111_API_AUTH", "")
AUTOMATIC1111_BASE_URL = os.getenv("AUTOMATIC1111_BASE_URL", "")
AUTOMATIC1111_CFG_SCALE = float(os.getenv("AUTOMATIC1111_CFG_SCALE", "7.0")) if os.getenv("AUTOMATIC1111_CFG_SCALE") else None
AUTOMATIC1111_SAMPLER = os.getenv("AUTOMATIC1111_SAMPLER", "")
AUTOMATIC1111_SCHEDULER = os.getenv("AUTOMATIC1111_SCHEDULER", "")
COMFYUI_BASE_URL = os.getenv("COMFYUI_BASE_URL", "")
COMFYUI_API_KEY = os.getenv("COMFYUI_API_KEY", "")
COMFYUI_WORKFLOW = os.getenv("COMFYUI_WORKFLOW", "")
COMFYUI_WORKFLOW_NODES = os.getenv("COMFYUI_WORKFLOW_NODES", "")
ENABLE_IMAGE_GENERATION = os.getenv("ENABLE_IMAGE_GENERATION", "true").lower() == "true"
ENABLE_IMAGE_PROMPT_GENERATION = os.getenv("ENABLE_IMAGE_PROMPT_GENERATION", "false").lower() == "true"
IMAGE_GENERATION_ENGINE = os.getenv("IMAGE_GENERATION_ENGINE", "openai")
IMAGE_GENERATION_MODEL = os.getenv("IMAGE_GENERATION_MODEL", "dall-e-3")
IMAGE_SIZE = os.getenv("IMAGE_SIZE", "1024x1024")
IMAGE_STEPS = int(os.getenv("IMAGE_STEPS", "20"))
IMAGES_OPENAI_API_BASE_URL = os.getenv("IMAGES_OPENAI_API_BASE_URL", "")
IMAGES_OPENAI_API_KEY = os.getenv("IMAGES_OPENAI_API_KEY", "")
IMAGES_GEMINI_API_BASE_URL = os.getenv("IMAGES_GEMINI_API_BASE_URL", "")
IMAGES_GEMINI_API_KEY = os.getenv("IMAGES_GEMINI_API_KEY", "")

AUDIO_STT_ENGINE = os.getenv("AUDIO_STT_ENGINE", "openai")
AUDIO_STT_MODEL = os.getenv("AUDIO_STT_MODEL", "whisper-1")
AUDIO_STT_SUPPORTED_CONTENT_TYPES = os.getenv("AUDIO_STT_SUPPORTED_CONTENT_TYPES", "audio/wav,audio/mp3,audio/mp4,audio/mpeg,audio/webm").split(",")
AUDIO_STT_OPENAI_API_BASE_URL = os.getenv("AUDIO_STT_OPENAI_API_BASE_URL", "")
AUDIO_STT_OPENAI_API_KEY = os.getenv("AUDIO_STT_OPENAI_API_KEY", "")
AUDIO_STT_AZURE_API_KEY = os.getenv("AUDIO_STT_AZURE_API_KEY", "")
AUDIO_STT_AZURE_REGION = os.getenv("AUDIO_STT_AZURE_REGION", "")
AUDIO_STT_AZURE_LOCALES = os.getenv("AUDIO_STT_AZURE_LOCALES", "").split(",") if os.getenv("AUDIO_STT_AZURE_LOCALES") else []
AUDIO_STT_AZURE_BASE_URL = os.getenv("AUDIO_STT_AZURE_BASE_URL", "")
AUDIO_STT_AZURE_MAX_SPEAKERS = int(os.getenv("AUDIO_STT_AZURE_MAX_SPEAKERS", "2"))
AUDIO_TTS_API_KEY = os.getenv("AUDIO_TTS_API_KEY", "")
AUDIO_TTS_ENGINE = os.getenv("AUDIO_TTS_ENGINE", "openai")
AUDIO_TTS_MODEL = os.getenv("AUDIO_TTS_MODEL", "tts-1")
AUDIO_TTS_OPENAI_API_BASE_URL = os.getenv("AUDIO_TTS_OPENAI_API_BASE_URL", "")
AUDIO_TTS_OPENAI_API_KEY = os.getenv("AUDIO_TTS_OPENAI_API_KEY", "")
AUDIO_TTS_SPLIT_ON = os.getenv("AUDIO_TTS_SPLIT_ON", "").split(",") if os.getenv("AUDIO_TTS_SPLIT_ON") else []
AUDIO_TTS_VOICE = os.getenv("AUDIO_TTS_VOICE", "")
AUDIO_TTS_AZURE_SPEECH_REGION = os.getenv("AUDIO_TTS_AZURE_SPEECH_REGION", "")
AUDIO_TTS_AZURE_SPEECH_BASE_URL = os.getenv("AUDIO_TTS_AZURE_SPEECH_BASE_URL", "")
AUDIO_TTS_AZURE_SPEECH_OUTPUT_FORMAT = os.getenv("AUDIO_TTS_AZURE_SPEECH_OUTPUT_FORMAT", "audio-16khz-32kbitrate-mono-mp3")

PLAYWRIGHT_WS_URL = os.getenv("PLAYWRIGHT_WS_URL", "")
PLAYWRIGHT_TIMEOUT = int(os.getenv("PLAYWRIGHT_TIMEOUT", "30"))
FIRECRAWL_API_BASE_URL = os.getenv("FIRECRAWL_API_BASE_URL", "")
FIRECRAWL_API_KEY = os.getenv("FIRECRAWL_API_KEY", "")
WEB_LOADER_ENGINE = os.getenv("WEB_LOADER_ENGINE", "playwright")
WEB_LOADER_CONCURRENT_REQUESTS = int(os.getenv("WEB_LOADER_CONCURRENT_REQUESTS", "10"))
WHISPER_MODEL = os.getenv("WHISPER_MODEL", "whisper-1")
WHISPER_VAD_FILTER = os.getenv("WHISPER_VAD_FILTER", "0.2")
WHISPER_LANGUAGE = os.getenv("WHISPER_LANGUAGE", "en")
DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY", "")
WHISPER_MODEL_AUTO_UPDATE = os.getenv("WHISPER_MODEL_AUTO_UPDATE", "false").lower() == "true"
WHISPER_MODEL_DIR = os.getenv("WHISPER_MODEL_DIR", "")

RAG_TEMPLATE = os.getenv("RAG_TEMPLATE", "default")
DEFAULT_RAG_TEMPLATE = os.getenv("DEFAULT_RAG_TEMPLATE", "default")
RAG_FULL_CONTEXT = os.getenv("RAG_FULL_CONTEXT", "false").lower() == "true"
BYPASS_EMBEDDING_AND_RETRIEVAL = os.getenv("BYPASS_EMBEDDING_AND_RETRIEVAL", "false").lower() == "true"

WEBUI_URL = os.getenv("WEBUI_URL", "")
WEBUI_NAME = os.getenv("WEBUI_NAME", "OpenWebUI")
WEBUI_FAVICON_URL = os.getenv("WEBUI_FAVICON_URL", "")
WEBUI_SECRET_KEY = os.getenv("WEBUI_SECRET_KEY", "")
WEBUI_SESSION_COOKIE_SECURE = os.getenv("WEBUI_SESSION_COOKIE_SECURE", "false").lower() == "true"
WEBUI_SESSION_COOKIE_SAME_SITE = os.getenv("WEBUI_SESSION_COOKIE_SAME_SITE", "Lax")

OAUTH_PROVIDERS = os.getenv("OAUTH_PROVIDERS", "").split(",") if os.getenv("OAUTH_PROVIDERS") else []

VERSION = os.getenv("VERSION", "0.6.24")
CHANGELOG = os.getenv("CHANGELOG", "Local development version")
ENV = os.getenv("ENV", "development")

AIOHTTP_CLIENT_SESSION_SSL = os.getenv("AIOHTTP_CLIENT_SESSION_SSL", "false").lower() == "true"

# OAuth manager not available in this version
# from utils.auth import oauth_manager

# Import custom middleware
# AccessControlMiddleware not available in this version
# from utils.access_control import AccessControlMiddleware
from utils.audit import AuditLoggingMiddleware

# Import SPA static files handler
# SPAStaticFiles not available in this version
# from utils.spa_static_files import SPAStaticFiles

# Import data directories from open_webui.env
from open_webui.env import (
    DATA_DIR,
    STATIC_DIR,
)

# Add missing cache directory
CACHE_DIR = DATA_DIR / "cache"
CACHE_DIR.mkdir(parents=True, exist_ok=True)

# Import logger
from utils.logger import logger as log

# Create FastAPI app
app = FastAPI(
    title="OpenWebUI API",
    description="OpenWebUI Backend API - Separated from frontend for security",
    version="0.6.24",  # Hardcoded for now
    docs_url="/docs",
    redoc_url="/redoc",
)

# Initialize app state configuration
class AppConfig:
    """Application configuration state"""
    def __init__(self):
        # Core configuration
        self.ENABLE_OLLAMA_API = ENABLE_OLLAMA_API
        self.OLLAMA_BASE_URLS = OLLAMA_BASE_URLS
        self.OLLAMA_API_CONFIGS = OLLAMA_API_CONFIGS
        
        self.ENABLE_OPENAI_API = ENABLE_OPENAI_API
        self.OPENAI_API_BASE_URLS = OPENAI_API_BASE_URLS
        self.OPENAI_API_KEYS = OPENAI_API_KEYS
        self.OPENAI_API_CONFIGS = OPENAI_API_CONFIGS
        
        self.ENABLE_DIRECT_CONNECTIONS = ENABLE_DIRECT_CONNECTIONS
        self.ENABLE_BASE_MODELS_CACHE = ENABLE_BASE_MODELS_CACHE
        self.THREAD_POOL_SIZE = THREAD_POOL_SIZE
        self.TOOL_SERVER_CONNECTIONS = TOOL_SERVER_CONNECTIONS
        
        # Code execution
        self.ENABLE_CODE_EXECUTION = ENABLE_CODE_EXECUTION
        self.CODE_EXECUTION_ENGINE = CODE_EXECUTION_ENGINE
        self.CODE_EXECUTION_JUPYTER_URL = CODE_EXECUTION_JUPYTER_URL
        self.CODE_EXECUTION_JUPYTER_AUTH = CODE_EXECUTION_JUPYTER_AUTH
        self.CODE_EXECUTION_JUPYTER_AUTH_TOKEN = CODE_EXECUTION_JUPYTER_AUTH_TOKEN
        self.CODE_EXECUTION_JUPYTER_AUTH_PASSWORD = CODE_EXECUTION_JUPYTER_AUTH_PASSWORD
        self.CODE_EXECUTION_JUPYTER_TIMEOUT = CODE_EXECUTION_JUPYTER_TIMEOUT
        self.ENABLE_CODE_INTERPRETER = ENABLE_CODE_INTERPRETER
        self.CODE_INTERPRETER_ENGINE = CODE_INTERPRETER_ENGINE
        self.CODE_INTERPRETER_PROMPT_TEMPLATE = CODE_INTERPRETER_PROMPT_TEMPLATE
        self.CODE_INTERPRETER_JUPYTER_URL = CODE_INTERPRETER_JUPYTER_URL
        self.CODE_INTERPRETER_JUPYTER_AUTH = CODE_INTERPRETER_JUPYTER_AUTH
        self.CODE_INTERPRETER_JUPYTER_AUTH_TOKEN = CODE_INTERPRETER_JUPYTER_AUTH_TOKEN
        self.CODE_INTERPRETER_JUPYTER_AUTH_PASSWORD = CODE_INTERPRETER_JUPYTER_AUTH_PASSWORD
        self.CODE_INTERPRETER_JUPYTER_TIMEOUT = CODE_INTERPRETER_JUPYTER_TIMEOUT
        
        # Image generation
        self.ENABLE_IMAGE_GENERATION = ENABLE_IMAGE_GENERATION
        self.ENABLE_IMAGE_PROMPT_GENERATION = ENABLE_IMAGE_PROMPT_GENERATION
        self.IMAGE_GENERATION_ENGINE = IMAGE_GENERATION_ENGINE
        self.IMAGE_GENERATION_MODEL = IMAGE_GENERATION_MODEL
        self.IMAGE_SIZE = IMAGE_SIZE
        self.IMAGE_STEPS = IMAGE_STEPS
        self.IMAGES_OPENAI_API_BASE_URL = IMAGES_OPENAI_API_BASE_URL
        self.IMAGES_OPENAI_API_KEY = IMAGES_OPENAI_API_KEY
        self.IMAGES_GEMINI_API_BASE_URL = IMAGES_GEMINI_API_BASE_URL
        self.IMAGES_GEMINI_API_KEY = IMAGES_GEMINI_API_KEY
        self.AUTOMATIC1111_API_AUTH = AUTOMATIC1111_API_AUTH
        self.AUTOMATIC1111_BASE_URL = AUTOMATIC1111_BASE_URL
        self.AUTOMATIC1111_CFG_SCALE = AUTOMATIC1111_CFG_SCALE
        self.AUTOMATIC1111_SAMPLER = AUTOMATIC1111_SAMPLER
        self.AUTOMATIC1111_SCHEDULER = AUTOMATIC1111_SCHEDULER
        self.COMFYUI_BASE_URL = COMFYUI_BASE_URL
        self.COMFYUI_API_KEY = COMFYUI_API_KEY
        self.COMFYUI_WORKFLOW = COMFYUI_WORKFLOW
        self.COMFYUI_WORKFLOW_NODES = COMFYUI_WORKFLOW_NODES
        
        # Audio configuration
        self.AUDIO_STT_ENGINE = AUDIO_STT_ENGINE
        self.AUDIO_STT_MODEL = AUDIO_STT_MODEL
        self.AUDIO_STT_SUPPORTED_CONTENT_TYPES = AUDIO_STT_SUPPORTED_CONTENT_TYPES
        self.AUDIO_STT_OPENAI_API_BASE_URL = AUDIO_STT_OPENAI_API_BASE_URL
        self.AUDIO_STT_OPENAI_API_KEY = AUDIO_STT_OPENAI_API_KEY
        self.AUDIO_STT_AZURE_API_KEY = AUDIO_STT_AZURE_API_KEY
        self.AUDIO_STT_AZURE_REGION = AUDIO_STT_AZURE_REGION
        self.AUDIO_STT_AZURE_LOCALES = AUDIO_STT_AZURE_LOCALES
        self.AUDIO_STT_AZURE_BASE_URL = AUDIO_STT_AZURE_BASE_URL
        self.AUDIO_STT_AZURE_MAX_SPEAKERS = AUDIO_STT_AZURE_MAX_SPEAKERS
        self.AUDIO_TTS_API_KEY = AUDIO_TTS_API_KEY
        self.AUDIO_TTS_ENGINE = AUDIO_TTS_ENGINE
        self.AUDIO_TTS_MODEL = AUDIO_TTS_MODEL
        self.AUDIO_TTS_OPENAI_API_BASE_URL = AUDIO_TTS_OPENAI_API_BASE_URL
        self.AUDIO_TTS_OPENAI_API_KEY = AUDIO_TTS_OPENAI_API_KEY
        
        # Audio configuration with proper names for routers
        self.TTS_OPENAI_API_BASE_URL = AUDIO_TTS_OPENAI_API_BASE_URL
        self.TTS_OPENAI_API_KEY = AUDIO_TTS_OPENAI_API_KEY
        self.TTS_API_KEY = AUDIO_TTS_API_KEY
        self.TTS_ENGINE = AUDIO_TTS_ENGINE
        self.TTS_MODEL = AUDIO_TTS_MODEL
        self.TTS_VOICE = AUDIO_TTS_VOICE
        self.TTS_SPLIT_ON = AUDIO_TTS_SPLIT_ON
        self.TTS_AZURE_SPEECH_REGION = AUDIO_TTS_AZURE_SPEECH_REGION
        self.TTS_AZURE_SPEECH_BASE_URL = AUDIO_TTS_AZURE_SPEECH_BASE_URL
        self.TTS_AZURE_SPEECH_OUTPUT_FORMAT = AUDIO_TTS_AZURE_SPEECH_OUTPUT_FORMAT
        
        self.STT_OPENAI_API_BASE_URL = AUDIO_STT_OPENAI_API_BASE_URL
        self.STT_OPENAI_API_KEY = AUDIO_STT_OPENAI_API_KEY
        self.STT_ENGINE = AUDIO_STT_ENGINE
        self.STT_MODEL = AUDIO_STT_MODEL
        self.STT_SUPPORTED_CONTENT_TYPES = AUDIO_STT_SUPPORTED_CONTENT_TYPES
        self.WHISPER_MODEL = WHISPER_MODEL
        self.DEEPGRAM_API_KEY = DEEPGRAM_API_KEY
        
        # WebUI configuration
        self.WEBUI_URL = WEBUI_URL
        self.WEBUI_NAME = WEBUI_NAME
        self.WEBUI_FAVICON_URL = WEBUI_FAVICON_URL
        self.WEBUI_SECRET_KEY = WEBUI_SECRET_KEY
        
        # Admin configuration with defaults
        self.SHOW_ADMIN_DETAILS = os.getenv("SHOW_ADMIN_DETAILS", "true").lower() == "true"
        self.ENABLE_SIGNUP = os.getenv("ENABLE_SIGNUP", "true").lower() == "true"
        self.ENABLE_LOGIN_FORM = os.getenv("ENABLE_LOGIN_FORM", "true").lower() == "true"
        self.ENABLE_API_KEY = os.getenv("ENABLE_API_KEY", "false").lower() == "true"
        self.ENABLE_API_KEY_ENDPOINT_RESTRICTIONS = os.getenv("ENABLE_API_KEY_ENDPOINT_RESTRICTIONS", "false").lower() == "true"
        self.API_KEY_ALLOWED_ENDPOINTS = os.getenv("API_KEY_ALLOWED_ENDPOINTS", "").split(",") if os.getenv("API_KEY_ALLOWED_ENDPOINTS") else []
        self.DEFAULT_USER_ROLE = os.getenv("DEFAULT_USER_ROLE", "user")
        self.JWT_EXPIRES_IN = os.getenv("JWT_EXPIRES_IN", "7d")
        self.ENABLE_COMMUNITY_SHARING = os.getenv("ENABLE_COMMUNITY_SHARING", "false").lower() == "true"
        self.ENABLE_MESSAGE_RATING = os.getenv("ENABLE_MESSAGE_RATING", "true").lower() == "true"
        self.ENABLE_CHANNELS = os.getenv("ENABLE_CHANNELS", "false").lower() == "true"
        self.ENABLE_NOTES = os.getenv("ENABLE_NOTES", "false").lower() == "true"
        self.ENABLE_USER_WEBHOOKS = os.getenv("ENABLE_USER_WEBHOOKS", "false").lower() == "true"
        self.PENDING_USER_OVERLAY_TITLE = os.getenv("PENDING_USER_OVERLAY_TITLE", "")
        self.PENDING_USER_OVERLAY_CONTENT = os.getenv("PENDING_USER_OVERLAY_CONTENT", "")
        self.RESPONSE_WATERMARK = os.getenv("RESPONSE_WATERMARK", "")
        
        # Additional configuration
        self.BANNERS = []  # Empty banners list by default
        self.WEBHOOK_URL = os.getenv("WEBHOOK_URL", "")
        self.USER_PERMISSIONS = {
            "workspace": {"enabled": True},
            "sharing": {"enabled": True},
            "chat": {"enabled": True},
            "features": {"enabled": True}
        }
        
        # OpenAI Configuration - Backend Only
        self.OPENAI_API_BASE_URLS = [
            os.getenv("OPENAI_API_BASE_URL", "https://api.openai.com/v1")
        ]
        # API Keys from environment - NEVER exposed to frontend
        self.OPENAI_API_KEYS = [
            os.getenv("OPENAI_API_KEY", "your-openai-api-key-here")
        ]
        self.OPENAI_API_CONFIGS = {
            "0": {
                "name": "OpenAI",
                "azure": False,
                "api_version": None
            }
        }
        
        # Additional model configurations
        self.ENABLE_OPENAI_API = False  # OFFLINE - will be enabled via .env
        self.OPENAI_MODELS = os.getenv("OPENAI_MODELS", "gpt-4,gpt-4-turbo,gpt-3.5-turbo").split(",")
        
        # OpenRouter Configuration
        self.OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")
        self.OPENROUTER_API_BASE_URL = os.getenv("OPENROUTER_API_BASE_URL", "https://openrouter.ai/api/v1")
        self.ENABLE_OPENROUTER_API = False  # OFFLINE - will be enabled via .env
        self.OPENROUTER_MODELS = os.getenv("OPENROUTER_MODELS", "").split(",") if os.getenv("OPENROUTER_MODELS") else []
        
        # Atlas Cloud Configuration
        self.ATLAS_CLOUD_API_KEY = os.getenv("ATLAS_CLOUD_API_KEY", "your-atlas-cloud-api-key-here")
        self.ATLAS_CLOUD_API_BASE_URL = os.getenv("ATLAS_CLOUD_API_BASE_URL", "https://api.atlascloud.ai/v1")
        self.ENABLE_ATLAS_CLOUD_API = True  # ONLINE - accessible now
        self.ATLAS_CLOUD_MODELS = [
            "openai/gpt-oss-20b",    # Added GPT-OSS 20B to Atlas Cloud
            "openai/gpt-oss-120b",   # Added GPT-OSS 120B to Atlas Cloud
            "atlas-7b",              # Original Atlas models
            "atlas-13b",
            "atlas-70b"
        ]
        
        # Anthropic Configuration
        self.ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
        self.ANTHROPIC_API_BASE_URL = os.getenv("ANTHROPIC_API_BASE_URL", "https://api.anthropic.com")
        self.ENABLE_ANTHROPIC_API = False  # OFFLINE - will be enabled via .env
        self.ANTHROPIC_MODELS = os.getenv("ANTHROPIC_MODELS", "").split(",") if os.getenv("ANTHROPIC_MODELS") else []
        
        # Google AI Configuration
        self.GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")
        self.GOOGLE_API_BASE_URL = os.getenv("GOOGLE_API_BASE_URL", "https://generativelanguage.googleapis.com")
        self.ENABLE_GOOGLE_API = False  # OFFLINE - will be enabled via .env
        self.GOOGLE_MODELS = os.getenv("GOOGLE_MODELS", "").split(",") if os.getenv("GOOGLE_MODELS") else []
        
        # Mistral AI Configuration
        self.MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY", "")
        self.MISTRAL_API_BASE_URL = os.getenv("MISTRAL_API_BASE_URL", "https://api.mistral.ai")
        self.ENABLE_MISTRAL_API = False  # OFFLINE - will be enabled via .env
        self.MISTRAL_MODELS = os.getenv("MISTRAL_MODELS", "").split(",") if os.getenv("MISTRAL_MODELS") else []
        
        # Perplexity Configuration
        self.PERPLEXITY_API_KEY = os.getenv("PERPLEXITY_API_KEY", "")
        self.PERPLEXITY_API_BASE_URL = os.getenv("PERPLEXITY_API_BASE_URL", "https://api.perplexity.ai")
        self.ENABLE_PERPLEXITY_API = False  # OFFLINE - will be enabled via .env
        self.PERPLEXITY_MODELS = os.getenv("PERPLEXITY_MODELS", "").split(",") if os.getenv("PERPLEXITY_MODELS") else []
        
        # Advanced Configuration
        self.ENABLE_STREAMING = os.getenv("ENABLE_STREAMING", "true").lower() == "true"
        self.ENABLE_FUNCTION_CALLING = os.getenv("ENABLE_FUNCTION_CALLING", "true").lower() == "true"
        self.ENABLE_VISION_MODELS = os.getenv("ENABLE_VISION_MODELS", "true").lower() == "true"
        self.ENABLE_EMBEDDING_MODELS = os.getenv("ENABLE_EMBEDDING_MODELS", "true").lower() == "true"
        self.RATE_LIMIT_PER_MINUTE = int(os.getenv("RATE_LIMIT_PER_MINUTE", "60"))
        self.MAX_TOKENS_PER_REQUEST = int(os.getenv("MAX_TOKENS_PER_REQUEST", "4000"))
        self.DEFAULT_TEMPERATURE = float(os.getenv("DEFAULT_TEMPERATURE", "0.7"))
        self.DEFAULT_MAX_TOKENS = int(os.getenv("DEFAULT_MAX_TOKENS", "1000"))

# Initialize app state
app.state.config = AppConfig()

# Add CORS middleware for frontend communication - Configured for localhost
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:6969",      # Frontend dev server
        "http://127.0.0.1:6969",     # Frontend localhost
        "http://localhost:6970",      # Frontend dev server (backup port)
        "http://127.0.0.1:6970",     # Frontend localhost (backup port)
        "http://localhost:6971",      # Frontend dev server (backup port 2)
        "http://127.0.0.1:6971",     # Frontend localhost (backup port 2)
        "http://localhost:6972",      # Frontend dev server (backup port 3)
        "http://127.0.0.1:6972",     # Frontend localhost (backup port 3)
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
    allow_headers=["*"],
    allow_origin_regex=None,
    expose_headers=["*"],
    max_age=86400,
)

# Add compression middleware
app.add_middleware(CompressMiddleware)

# Add access control middleware
# app.add_middleware(AccessControlMiddleware)  # Not available in this version

# Add audit logging middleware
app.add_middleware(AuditLoggingMiddleware, audit_level=AuditLevel.REQUEST_RESPONSE)

# Add socket app
app.mount("/socket.io", socket_app)  # Simple socket functionality enabled

# Include all API routers
app.include_router(audio.router, prefix="/api/v1/audio", tags=["audio"])
app.include_router(images.router, prefix="/api/v1/images", tags=["images"])
app.include_router(ollama.router, prefix="/ollama", tags=["ollama"])
# app.include_router(openai.router, prefix="/openai", tags=["openai"])  # Temporarily disabled due to import issues
app.include_router(retrieval.router, prefix="/api/v1/retrieval", tags=["retrieval"])
app.include_router(pipelines.router, prefix="/api/v1/pipelines", tags=["pipelines"])
app.include_router(tasks.router, prefix="/api/v1/tasks", tags=["tasks"])
app.include_router(auths.router, prefix="/api/v1/auths", tags=["auths"])
app.include_router(channels.router, prefix="/api/v1/channels", tags=["channels"])
app.include_router(chats.router, prefix="/api/v1/chats", tags=["chats"])
app.include_router(notes.router, prefix="/api/v1/notes", tags=["notes"])
app.include_router(folders.router, prefix="/api/v1/folders", tags=["folders"])
app.include_router(configs.router, prefix="/api/v1/configs", tags=["configs"])
app.include_router(groups.router, prefix="/api/v1/groups", tags=["groups"])
app.include_router(files.router, prefix="/api/v1/files", tags=["files"])
app.include_router(functions.router, prefix="/api/v1/functions", tags=["functions"])
app.include_router(memories.router, prefix="/api/v1/memories", tags=["memories"])
# app.include_router(models.router, prefix="/api/v1/models", tags=["models"])  # Commented out due to database conflicts
app.include_router(knowledge.router, prefix="/api/v1/knowledge", tags=["knowledge"])
app.include_router(prompts.router, prefix="/api/v1/prompts", tags=["prompts"])
app.include_router(evaluations.router, prefix="/api/v1/evaluations", tags=["evaluations"])
app.include_router(tools.router, prefix="/api/v1/tools", tags=["tools"])
app.include_router(users.router, prefix="/api/v1/users", tags=["users"])
app.include_router(utils.router, prefix="/api/v1/utils", tags=["utils"])
app.include_router(scim.router, prefix="/api/v1/scim", tags=["scim"])

# Mount static files (only backend assets, no frontend)
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# API endpoints
@app.get("/api/config")
async def get_backend_config(request: Request):
    """Get backend configuration for frontend initialization"""
    return {
        "name": request.app.state.config.WEBUI_NAME,
        "version": "0.6.24",
        "default_locale": "en-US",
        "features": {
            "enable_signup": request.app.state.config.ENABLE_SIGNUP,
            "enable_login_form": True,  # Enable login form to show input boxes
            "enable_api_key": request.app.state.config.ENABLE_API_KEY,
            "enable_community_sharing": request.app.state.config.ENABLE_COMMUNITY_SHARING,
            "enable_message_rating": request.app.state.config.ENABLE_MESSAGE_RATING,
            "enable_channels": request.app.state.config.ENABLE_CHANNELS,
            "enable_notes": request.app.state.config.ENABLE_NOTES,
            "enable_websocket": True,
            "enable_direct_connections": False,  # Disabled - backend-only configuration
            "enable_ollama_api": request.app.state.config.ENABLE_OLLAMA_API,
            "enable_openai_api": request.app.state.config.ENABLE_OPENAI_API,
            "backend_managed": True,  # Indicates this is a backend-managed instance
            "enable_image_generation": request.app.state.config.ENABLE_IMAGE_GENERATION,
            "enable_code_execution": request.app.state.config.ENABLE_CODE_EXECUTION,
            "enable_code_interpreter": request.app.state.config.ENABLE_CODE_INTERPRETER,
        },
        "default_user_role": request.app.state.config.DEFAULT_USER_ROLE,
        "oauth": {
            "providers": {}  # Empty for now - OAuth not configured
        },
        "auth": {
            "trusted_header_auth": False
        },
        "status": True
    }

@app.get("/api/version")
async def get_app_version():
    return {
        "version": "0.6.24",
    }

@app.get("/api/version/updates")
async def get_app_latest_release_version():
    # Simplified version for testing
    return {"current": "0.6.24", "latest": "0.6.24"}

@app.get("/api/changelog")
async def get_app_changelog():
    # Simplified version for testing
    return {"changelog": "Local development version"}

# Simple models endpoints to fix the 404 issue
@app.get("/api/models")
async def get_models_simple(request: Request):
    """Simple models endpoint for compatibility - Frontend expects res.data"""
    models = []
    
    # Add OpenAI models if enabled
    if request.app.state.config.ENABLE_OPENAI_API:
        for model_id in request.app.state.config.OPENAI_MODELS:
            models.append({
                "id": model_id,
                "name": model_id.split("/")[-1].replace("-", " ").title(),
                "object": "model",
                "created": 1677610602,
                "owned_by": "openai",
                "provider": "openai",
                "info": {
                    "meta": {
                        "description": f"OpenAI {model_id} Model",
                        "capabilities": {
                            "vision": "gpt-4o" in model_id or "vision" in model_id.lower(),
                            "usage": "text-generation"
                        }
                    }
                }
            })
    
    # Add OpenRouter models if enabled
    if request.app.state.config.ENABLE_OPENROUTER_API:
        for model_id in request.app.state.config.OPENROUTER_MODELS:
            models.append({
                "id": model_id,
                "name": model_id.split("/")[-1].replace("-", " ").title(),
                "object": "model",
                "created": 1677610602,
                "owned_by": "openrouter",
                "provider": "openrouter",
                "info": {
                    "meta": {
                        "description": f"OpenRouter {model_id} Model",
                        "capabilities": {
                            "vision": False,
                            "usage": "text-generation"
                        }
                    }
                }
            })
    
    # Add Atlas Cloud models if enabled
    if request.app.state.config.ENABLE_ATLAS_CLOUD_API:
        for model_id in request.app.state.config.ATLAS_CLOUD_MODELS:
            models.append({
                "id": model_id,
                "name": model_id.replace("-", " ").title(),
                "object": "model",
                "created": 1677610602,
                "owned_by": "openai",
                "provider": "atlascloud",
                "info": {
                    "meta": {
                        "description": f"Atlas Cloud {model_id} Model",
                        "capabilities": {
                            "vision": False,
                            "usage": "text-generation"
                        }
                    }
                }
            })
    
    # Add Anthropic models if enabled
    if request.app.state.config.ENABLE_ANTHROPIC_API:
        for model_id in request.app.state.config.ANTHROPIC_MODELS:
            models.append({
                "id": model_id,
                "name": model_id.replace("-", " ").title(),
                "object": "model",
                "created": 1677610602,
                "owned_by": "anthropic",
                "provider": "anthropic",
                "info": {
                    "meta": {
                        "description": f"Anthropic {model_id} Model",
                        "capabilities": {
                            "vision": "opus" in model_id or "sonnet" in model_id,
                            "usage": "text-generation"
                        }
                    }
                }
            })
    
    # Add Google models if enabled
    if request.app.state.config.ENABLE_GOOGLE_API:
        for model_id in request.app.state.config.GOOGLE_MODELS:
            models.append({
                "id": model_id,
                "name": model_id.replace("-", " ").title(),
                "object": "model",
                "created": 1677610602,
                "owned_by": "google",
                "provider": "google",
                "info": {
                    "meta": {
                        "description": f"Google {model_id} Model",
                        "capabilities": {
                            "vision": "vision" in model_id.lower(),
                            "usage": "text-generation"
                        }
                    }
                }
            })
    
    # Add Mistral models if enabled
    if request.app.state.config.ENABLE_MISTRAL_API:
        for model_id in request.app.state.config.MISTRAL_MODELS:
            models.append({
                "id": model_id,
                "name": model_id.replace("-", " ").title(),
                "object": "model",
                "created": 1677610602,
                "owned_by": "mistral",
                "provider": "mistral",
                "info": {
                    "meta": {
                        "description": f"Mistral {model_id} Model",
                        "capabilities": {
                            "vision": False,
                            "usage": "text-generation"
                        }
                    }
                }
            })
    
    # Add Perplexity models if enabled
    if request.app.state.config.ENABLE_PERPLEXITY_API:
        for model_id in request.app.state.config.PERPLEXITY_MODELS:
            models.append({
                "id": model_id,
                "name": model_id.replace("-", " ").title(),
                "object": "model",
                "created": 1677610602,
                "owned_by": "perplexity",
                "provider": "perplexity",
                "info": {
                    "meta": {
                        "description": f"Perplexity {model_id} Model",
                        "capabilities": {
                            "vision": False,
                            "usage": "text-generation"
                        }
                    }
                }
            })
    
    return {"data": models}

@app.get("/api/v1/models")
async def get_models_redirect():
    """Redirect to models endpoint with trailing slash"""
    from fastapi.responses import RedirectResponse
    return RedirectResponse(url="/api/v1/models/", status_code=307)

@app.get("/api/v1/models/")
async def get_models_v1(request: Request, user = Depends(lambda: None)):
    """Models endpoint - returns configured models"""
    models = []
    
    # Add OpenAI models if enabled
    if request.app.state.config.ENABLE_OPENAI_API:
        for model_id in request.app.state.config.OPENAI_MODELS:
            models.append({
                "id": model_id,
                "name": model_id.split("/")[-1].replace("-", " ").title(),
                "object": "model",
                "created": 1677610602,
                "owned_by": "openai",
                "provider": "openai",
                "info": {
                    "meta": {
                        "description": f"OpenAI {model_id} Model",
                        "capabilities": {
                            "vision": "gpt-4o" in model_id or "vision" in model_id.lower(),
                            "usage": "text-generation"
                        }
                    }
                }
            })
    
    # Add OpenRouter models if enabled
    if request.app.state.config.ENABLE_OPENROUTER_API:
        for model_id in request.app.state.config.OPENROUTER_MODELS:
            models.append({
                "id": model_id,
                "name": model_id.split("/")[-1].replace("-", " ").title(),
                "object": "model",
                "created": 1677610602,
                "owned_by": "openrouter",
                "provider": "openrouter",
                "info": {
                    "meta": {
                        "description": f"OpenRouter {model_id} Model",
                        "capabilities": {
                            "vision": False,
                            "usage": "text-generation"
                        }
                    }
                }
            })
    
    # Add Atlas Cloud models if enabled
    if request.app.state.config.ENABLE_ATLAS_CLOUD_API:
        for model_id in request.app.state.config.ATLAS_CLOUD_MODELS:
            models.append({
                "id": model_id,
                "name": model_id.replace("-", " ").title(),
                "object": "model",
                "created": 1677610602,
                "owned_by": "openai",  # Changed from "atlascloud" to "openai" for frontend compatibility
                "provider": "atlascloud",
                "info": {
                    "meta": {
                        "description": f"Atlas Cloud {model_id} Model",
                        "capabilities": {
                            "vision": False,
                            "usage": "text-generation"
                        }
                    }
                }
            })
    
    # Add Anthropic models if enabled
    if request.app.state.config.ENABLE_ANTHROPIC_API:
        for model_id in request.app.state.config.ANTHROPIC_MODELS:
            models.append({
                "id": model_id,
                "name": model_id.replace("-", " ").title(),
                "object": "model",
                "created": 1677610602,
                "owned_by": "anthropic",
                "provider": "anthropic",
                "info": {
                    "meta": {
                        "description": f"Anthropic {model_id} Model",
                        "capabilities": {
                            "vision": "opus" in model_id or "sonnet" in model_id,
                            "usage": "text-generation"
                        }
                    }
                }
            })
    
    # Add Google models if enabled
    if request.app.state.config.ENABLE_GOOGLE_API:
        for model_id in request.app.state.config.GOOGLE_MODELS:
            models.append({
                "id": model_id,
                "name": model_id.replace("-", " ").title(),
                "object": "model",
                "created": 1677610602,
                "owned_by": "google",
                "provider": "google",
                "info": {
                    "meta": {
                        "description": f"Google {model_id} Model",
                        "capabilities": {
                            "vision": "vision" in model_id.lower(),
                            "usage": "text-generation"
                        }
                    }
                }
            })
    
    # Add Mistral models if enabled
    if request.app.state.config.ENABLE_MISTRAL_API:
        for model_id in request.app.state.config.MISTRAL_MODELS:
            models.append({
                "id": model_id,
                "name": model_id.replace("-", " ").title(),
                "object": "model",
                "created": 1677610602,
                "owned_by": "mistral",
                "provider": "mistral",
                "info": {
                    "meta": {
                        "description": f"Mistral {model_id} Model",
                        "capabilities": {
                            "vision": False,
                            "usage": "text-generation"
                        }
                    }
                }
            })
    
    # Add Perplexity models if enabled
    if request.app.state.config.ENABLE_PERPLEXITY_API:
        for model_id in request.app.state.config.PERPLEXITY_MODELS:
            models.append({
                "id": model_id,
                "name": model_id.replace("-", " ").title(),
                "object": "model",
                "created": 1677610602,
                "owned_by": "perplexity",
                "provider": "perplexity",
                "info": {
                    "meta": {
                        "description": f"Perplexity {model_id} Model",
                        "capabilities": {
                            "vision": False,
                            "usage": "text-generation"
                        }
                    }
                }
            })
    
    return models

# Admin promotion endpoint removed - admin account created successfully

# Chat completions endpoint - Frontend expects this
@app.post("/api/chat/completions")
async def chat_completions(request: Request):
    """Chat completions endpoint - Frontend compatibility"""
    try:
        body = await request.json()
        model = body.get("model", "")
        messages = body.get("messages", [])
        
        # Check if model is supported and get provider info
        model_provider = None
        if model in request.app.state.config.OPENAI_MODELS:
            model_provider = "openai"
            api_key = request.app.state.config.OPENAI_API_KEYS[0]
            if not api_key or api_key == "your-openai-api-key-here":
                return {
                    "error": {
                        "message": "OpenAI API key not configured. Set OPENAI_API_KEY environment variable.",
                        "type": "configuration_error",
                        "code": "api_key_required"
                    }
                }
        elif model in request.app.state.config.ATLAS_CLOUD_MODELS:
            model_provider = "atlascloud"
            api_key = request.app.state.config.ATLAS_CLOUD_API_KEY
            if not api_key or api_key == "your-atlas-cloud-api-key-here":
                return {
                    "error": {
                        "message": "Atlas Cloud API key not configured. Set ATLAS_CLOUD_API_KEY environment variable.",
                        "type": "configuration_error",
                        "code": "api_key_required"
                    }
                }
        else:
            return {
                "error": {
                    "message": f"Model {model} not found. Available models: {', '.join(request.app.state.config.OPENAI_MODELS + request.app.state.config.ATLAS_CLOUD_MODELS)}",
                    "type": "model_not_found",
                    "code": "model_not_found"
                }
            }
        
        # Real API call to Atlas Cloud
        if model_provider == "atlascloud":
            try:
                import aiohttp
                async with aiohttp.ClientSession() as session:
                    headers = {
                        "Authorization": f"Bearer {api_key}",
                        "Content-Type": "application/json"
                    }
                    
                    payload = {
                        "model": model,
                        "messages": messages,
                        "max_tokens": 1000,
                        "temperature": 0.7
                    }
                    
                    async with session.post(
                        "https://api.atlascloud.ai/v1/chat/completions",
                        headers=headers,
                        json=payload
                    ) as response:
                        if response.status == 200:
                            result = await response.json()
                            
                            # Extract the response content
                            if result.get("choices") and len(result["choices"]) > 0:
                                content = result["choices"][0].get("message", {}).get("content", "")
                                
                                # Emit WebSocket event for real-time updates
                                try:
                                    from simple_socket import emit_chat_event
                                    await emit_chat_event("chat-events", {
                                        "chat_id": body.get("chat_id", "default"),
                                        "message_id": body.get("id", "default"),
                                        "data": {
                                            "type": "chat:completion",
                                            "data": {
                                                "done": True,
                                                "content": content,
                                                "title": f"Chat with {model}"
                                            }
                                        }
                                    })
                                except Exception as ws_error:
                                    print(f"WebSocket emit error: {ws_error}")
                            
                            # Return response with task_id for frontend compatibility
                            result["task_id"] = f"task_{int(time.time())}"
                            return result
                        else:
                            error_text = await response.text()
                            return {
                                "error": {
                                    "message": f"Atlas Cloud API error: {response.status} - {error_text}",
                                    "type": "api_error",
                                    "code": "atlas_cloud_error"
                                }
                            }
            except Exception as e:
                return {
                    "error": {
                        "message": f"Error calling Atlas Cloud API: {str(e)}",
                        "type": "api_error",
                        "code": "atlas_cloud_error"
                    }
                }
        
        # Real API call to OpenAI
        elif model_provider == "openai":
            try:
                import aiohttp
                async with aiohttp.ClientSession() as session:
                    headers = {
                        "Authorization": f"Bearer {api_key}",
                        "Content-Type": "application/json"
                    }
                    
                    payload = {
                        "model": model,
                        "messages": messages,
                        "max_tokens": 1000,
                        "temperature": 0.7
                    }
                    
                    async with session.post(
                        "https://api.openai.com/v1/chat/completions",
                        headers=headers,
                        json=payload
                    ) as response:
                        if response.status == 200:
                            result = await response.json()
                            
                            # Extract the response content
                            if result.get("choices") and len(result["choices"]) > 0:
                                content = result["choices"][0].get("message", {}).get("content", "")
                                
                                # Emit WebSocket event for real-time updates
                                try:
                                    from simple_socket import emit_chat_event
                                    await emit_chat_event("chat-events", {
                                        "chat_id": body.get("chat_id", "default"),
                                        "message_id": body.get("id", "default"),
                                        "data": {
                                            "type": "chat:completion",
                                            "data": {
                                                "done": True,
                                                "content": content,
                                                "title": f"Chat with {model}"
                                            }
                                        }
                                    })
                                except Exception as ws_error:
                                    print(f"WebSocket emit error: {ws_error}")
                            
                            # Return response with task_id for frontend compatibility
                            result["task_id"] = f"task_{int(time.time())}"
                            return result
                        else:
                            error_text = await response.text()
                            return {
                                "error": {
                                    "message": f"OpenAI API error: {response.status} - {error_text}",
                                    "type": "api_error",
                                    "code": "openai_error"
                                }
                            }
            except Exception as e:
                return {
                    "error": {
                        "message": f"Error calling OpenAI API: {str(e)}",
                        "type": "api_error",
                        "code": "openai_error"
                    }
                }
        
        # Fallback for unknown providers
        return {
            "error": {
                "message": f"Unknown provider: {model_provider}",
                "type": "configuration_error",
                "code": "unknown_provider"
            }
        }
        
    except Exception as e:
        return {"error": {"message": str(e), "type": "server_error"}}

# Additional essential endpoints for frontend compatibility
@app.post("/api/chat/completed")
async def chat_completed(request: Request):
    """Chat completed endpoint - Frontend compatibility"""
    try:
        body = await request.json()
        return {
            "status": "success",
            "message": "Chat completed endpoint working",
            "received_data": body
        }
    except Exception as e:
        return {"error": {"message": str(e), "type": "server_error"}}

@app.get("/api/usage")
async def get_usage():
    """Usage endpoint - Frontend compatibility"""
    return {
        "status": "success",
        "message": "Usage tracking disabled in backend-only mode",
        "usage": {
            "total_tokens": 0,
            "total_requests": 0
        }
    }

@app.get("/api/changelog")
async def get_changelog():
    """Changelog endpoint - Frontend compatibility"""
    return {
        "status": "success",
        "message": "Backend-only OpenWebUI instance",
        "version": "1.0.0"
    }

@app.get("/api/config/model/filter")
async def get_model_filter():
    """Model filter endpoint - Frontend compatibility"""
    return {
        "status": "success",
        "message": "Model filtering disabled in backend-only mode",
        "filters": []
    }

@app.post("/api/config/model/filter")
async def update_model_filter(request: Request):
    """Update model filter endpoint - Frontend compatibility"""
    try:
        body = await request.json()
        return {
            "status": "success",
            "message": "Model filtering disabled in backend-only mode",
            "received_data": body
        }
    except Exception as e:
        return {"error": {"message": str(e), "type": "server_error"}}

@app.get("/api/config/models")
async def get_config_models():
    """Config models endpoint - Frontend compatibility"""
    return {
        "status": "success",
        "message": "Models configured server-side",
        "models": [
            "openai/gpt-oss-20b",
            "openai/gpt-oss-120b"
        ]
    }

@app.post("/api/config/models")
async def update_config_models(request: Request):
    """Update config models endpoint - Frontend compatibility"""
    try:
        body = await request.json()
        return {
            "status": "disabled",
            "message": "Model configuration is backend-only. Set models in environment variables.",
            "received_data": body
        }
    except Exception as e:
        return {"error": {"message": str(e), "type": "server_error"}}

# OpenAI endpoints - working versions
@app.post("/openai/verify")
async def verify_openai_connection(request: Request):
    """Verify OpenAI API connection"""
    try:
        from utils.auth import get_admin_user
        from fastapi import Depends
        from pydantic import BaseModel
        
        class ConnectionForm(BaseModel):
            url: str
            key: str
            config: dict = {}
        
        # For now, return a simple success response
        # This can be expanded later with actual OpenAI API verification
        return {
            "status": "success",
            "message": "OpenAI verify endpoint is working",
            "note": "Add authentication dependency when needed"
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/openai/config")
async def get_openai_config(request: Request):
    """Get OpenAI configuration - FRONTEND SAFE (no API keys exposed)"""
    return {
        "enabled": request.app.state.config.ENABLE_OPENAI_API,
        "models_available": len(request.app.state.config.OPENAI_MODELS),
        "api_configured": bool(request.app.state.config.OPENAI_API_KEYS[0] and 
                             request.app.state.config.OPENAI_API_KEYS[0] != "your-openai-api-key-here"),
        "status": "success",
        "message": "OpenAI is configured server-side. API keys are not exposed to frontend."
    }

@app.get("/openai/models")
async def get_openai_models(request: Request):
    """Get OpenAI models with configured models"""
    models = [
        {
            "id": "openai/gpt-oss-20b",
            "object": "model",
            "created": 1677610602,
            "owned_by": "openai",
            "permission": [
                {
                    "id": "modelperm-1",
                    "object": "model_permission",
                    "created": 1677610602,
                    "allow_create_engine": False,
                    "allow_sampling": True,
                    "allow_logprobs": True,
                    "allow_search_indices": False,
                    "allow_view": True,
                    "allow_fine_tuning": False,
                    "organization": "*",
                    "group": None,
                    "is_blocking": False
                }
            ],
            "root": "openai/gpt-oss-20b",
            "parent": None
        },
        {
            "id": "openai/gpt-oss-120b",
            "object": "model",
            "created": 1677610602,
            "owned_by": "openai",
            "permission": [
                {
                    "id": "modelperm-2",
                    "object": "model_permission",
                    "created": 1677610602,
                    "allow_create_engine": False,
                    "allow_sampling": True,
                    "allow_logprobs": True,
                    "allow_search_indices": False,
                    "allow_view": True,
                    "allow_fine_tuning": False,
                    "organization": "*",
                    "group": None,
                    "is_blocking": False
                }
            ],
            "root": "openai/gpt-oss-120b",
            "parent": None
        }
    ]
    
    return {
        "data": models,
        "object": "list",
        "status": "success"
    }

@app.get("/openai/models/{url_idx}")
async def get_openai_models_by_index(url_idx: int, request: Request):
    """Get OpenAI models by URL index"""
    models = [
        {
            "id": "openai/gpt-oss-20b",
            "object": "model",
            "created": 1677610602,
            "owned_by": "openai",
            "root": "openai/gpt-oss-20b",
            "parent": None
        },
        {
            "id": "openai/gpt-oss-120b", 
            "object": "model",
            "created": 1677610602,
            "owned_by": "openai",
            "root": "openai/gpt-oss-120b",
            "parent": None
        }
    ]
    
    return {
        "data": models,
        "object": "list",
        "url_idx": url_idx,
        "status": "success"
    }

@app.post("/openai/config/update")
async def update_openai_config(request: Request):
    """DISABLED: Configuration is backend-only"""
    return {
        "status": "disabled",
        "message": "Configuration updates are disabled. All settings are managed server-side via environment variables.",
        "note": "Set OPENAI_API_KEY environment variable to configure API access."
    }

@app.post("/openai/chat/completions")
async def openai_chat_completions(request: Request):
    """OpenAI chat completions endpoint - Backend managed"""
    try:
        body = await request.json()
        model = body.get("model", "")
        
        # Check if API is configured
        api_key = request.app.state.config.OPENAI_API_KEYS[0]
        if not api_key or api_key == "your-openai-api-key-here":
            return {
                "error": {
                    "message": "OpenAI API key not configured. Set OPENAI_API_KEY environment variable.",
                    "type": "configuration_error",
                    "code": "api_key_required"
                }
            }
        
        # Check if model is supported
        if model not in request.app.state.config.OPENAI_MODELS:
            return {
                "error": {
                    "message": f"Model {model} not found. Available models: {', '.join(request.app.state.config.OPENAI_MODELS)}",
                    "type": "model_not_found",
                    "code": "model_not_found"
                }
            }
        
        # Placeholder response - would call actual OpenAI API here
        return {
            "id": "chatcmpl-test123",
            "object": "chat.completion",
            "created": 1677610602,
            "model": model,
            "choices": [
                {
                    "index": 0,
                    "message": {
                        "role": "assistant",
                        "content": f"This is a test response from {model}. In production, this would call the actual OpenAI API with your configured API key."
                    },
                    "finish_reason": "stop"
                }
            ],
            "usage": {
                "prompt_tokens": 10,
                "completion_tokens": 25,
                "total_tokens": 35
            }
        }
        
    except Exception as e:
        return {"error": {"message": str(e), "type": "server_error"}}

@app.post("/openai/audio/speech")
async def openai_audio_speech(request: Request):
    """OpenAI audio speech endpoint"""
    try:
        body = await request.json()
        return {
            "status": "success",
            "message": "OpenAI audio speech endpoint working",
            "note": "Add actual audio speech logic when needed"
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/api/usage")
async def get_current_usage():
    """
    Get current usage statistics for Open WebUI.
    This is an experimental endpoint and subject to change.
    """
    try:
        return {"model_ids": [], "user_ids": []}
    except Exception as e:
        log.error(f"Error getting usage statistics: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

# Health check endpoints
@app.get("/health")
async def healthcheck():
    return {"status": True}

@app.get("/health/db")
async def healthcheck_with_db():
    try:
        # Simple health check without database dependency for now
        return {"status": True, "database": "not_configured"}
    except Exception as e:
        return {"status": False, "error": str(e)}

# Cache file serving
@app.get("/cache/{path:path}")
async def serve_cache_file(path: str):
    # Simplified for testing
    return {"message": "Cache endpoint", "path": path}

# Custom Swagger UI
def swagger_ui_html(*args, **kwargs):
    return get_swagger_ui_html(
        *args,
        **kwargs,
        swagger_js_url="/static/swagger-ui/swagger-ui-bundle.js",
        swagger_css_url="/static/swagger-ui/swagger-ui.css",
        swagger_favicon_url="/static/swagger-ui/favicon.png",
    )

applications.get_swagger_ui_html = swagger_ui_html

# Note: This backend-only version does NOT serve frontend files
# The frontend should be deployed separately and communicate via API calls
