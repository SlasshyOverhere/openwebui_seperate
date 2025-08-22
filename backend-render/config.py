"""
Simple configuration module for the separated backend version.
This provides default values for configuration variables that are missing from open_webui.env.
"""

import os
from pathlib import Path

# Get the data directory from open_webui.env
try:
    from open_webui.env import DATA_DIR
except ImportError:
    DATA_DIR = Path("./data")

# Cache directory
CACHE_DIR = DATA_DIR / "cache"
CACHE_DIR.mkdir(parents=True, exist_ok=True)

# Upload directory
UPLOAD_DIR = DATA_DIR / "uploads"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

# Default configuration values
DEFAULT_RAG_TEMPLATE = os.getenv("DEFAULT_RAG_TEMPLATE", "default")
ENABLE_ADMIN_EXPORT = os.getenv("ENABLE_ADMIN_EXPORT", "true").lower() == "true"
ENABLE_ADMIN_CHAT_ACCESS = os.getenv("ENABLE_ADMIN_CHAT_ACCESS", "true").lower() == "true"
BYPASS_ADMIN_ACCESS_CONTROL = os.getenv("BYPASS_ADMIN_ACCESS_CONTROL", "false").lower() == "true"
DEFAULT_USER_PERMISSIONS = {
    "workspace": {"enabled": True},
    "sharing": {"enabled": True},
    "chat": {"enabled": True},
    "features": {"enabled": True}
}

# S3 Vector configuration
S3_VECTOR_BUCKET_NAME = os.getenv("S3_VECTOR_BUCKET_NAME", "")
S3_VECTOR_REGION = os.getenv("S3_VECTOR_REGION", "us-east-1")

# Vector database configuration
VECTOR_DB = os.getenv("VECTOR_DB", "chroma")
ENABLE_QDRANT_MULTITENANCY_MODE = os.getenv("ENABLE_QDRANT_MULTITENANCY_MODE", "false").lower() == "true"

# OAuth configuration
OPENID_PROVIDER_URL = os.getenv("OPENID_PROVIDER_URL", "")
ENABLE_OAUTH_SIGNUP = os.getenv("ENABLE_OAUTH_SIGNUP", "false").lower() == "true"
ENABLE_LDAP = os.getenv("ENABLE_LDAP", "false").lower() == "true"

# WebUI configuration
WEBUI_FAVICON_URL = os.getenv("WEBUI_FAVICON_URL", "")

# Configuration functions for compatibility
def get_config():
    """Get the current configuration as a dictionary."""
    return {
        "ENABLE_OLLAMA_API": os.getenv("ENABLE_OLLAMA_API", "true").lower() == "true",
        "ENABLE_OPENAI_API": os.getenv("ENABLE_OPENAI_API", "true").lower() == "true",
        "ENABLE_DIRECT_CONNECTIONS": os.getenv("ENABLE_DIRECT_CONNECTIONS", "true").lower() == "true",
        "ENABLE_IMAGE_GENERATION": os.getenv("ENABLE_IMAGE_GENERATION", "true").lower() == "true",
        "ENABLE_CODE_EXECUTION": os.getenv("ENABLE_CODE_EXECUTION", "false").lower() == "true",
        "ENABLE_CODE_INTERPRETER": os.getenv("ENABLE_CODE_INTERPRETER", "false").lower() == "true",
        "WEBUI_NAME": os.getenv("WEBUI_NAME", "OpenWebUI"),
        "WEBUI_URL": os.getenv("WEBUI_URL", ""),
        "CACHE_DIR": str(CACHE_DIR),
        "UPLOAD_DIR": str(UPLOAD_DIR),
    }

def save_config(config_dict):
    """Save configuration (placeholder for compatibility)."""
    # This is a placeholder - in a real implementation, this would save to a file or database
    pass

# Banner model for compatibility
from pydantic import BaseModel
from typing import Optional

class BannerModel(BaseModel):
    """Banner model for compatibility."""
    id: Optional[str] = None
    title: Optional[str] = None
    content: Optional[str] = None
    type: Optional[str] = None
    enabled: Optional[bool] = None
