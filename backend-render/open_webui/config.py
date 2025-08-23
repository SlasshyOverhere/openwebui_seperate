"""
Configuration for OpenWebUI backend.
This file provides configuration for various components.
"""

import os
from typing import Optional

# Vector database configuration
VECTOR_DB = os.getenv("VECTOR_DB", "chroma")

# S3 configuration for vector storage
S3_VECTOR_BUCKET_NAME = os.getenv("S3_VECTOR_BUCKET_NAME", "")
S3_VECTOR_REGION = os.getenv("S3_VECTOR_REGION", "us-east-1")

# Qdrant configuration
ENABLE_QDRANT_MULTITENANCY_MODE = os.getenv("ENABLE_QDRANT_MULTITENANCY_MODE", "false").lower() == "true"

# OAuth configuration
OPENID_PROVIDER_URL = os.getenv("OPENID_PROVIDER_URL", "")
ENABLE_OAUTH_SIGNUP = os.getenv("ENABLE_OAUTH_SIGNUP", "false").lower() == "true"
ENABLE_LDAP = os.getenv("ENABLE_LDAP", "false").lower() == "true"

# WebUI configuration
WEBUI_FAVICON_URL = os.getenv("WEBUI_FAVICON_URL", "")

# RAG configuration
DEFAULT_RAG_TEMPLATE = os.getenv("DEFAULT_RAG_TEMPLATE", "default")

# Admin configuration
ENABLE_ADMIN_EXPORT = os.getenv("ENABLE_ADMIN_EXPORT", "true").lower() == "true"
ENABLE_ADMIN_CHAT_ACCESS = os.getenv("ENABLE_ADMIN_CHAT_ACCESS", "true").lower() == "true"
BYPASS_ADMIN_ACCESS_CONTROL = os.getenv("BYPASS_ADMIN_ACCESS_CONTROL", "false").lower() == "true"

# Default user permissions
DEFAULT_USER_PERMISSIONS = {
    "workspace": {"enabled": True},
    "sharing": {"enabled": True},
    "chat": {"enabled": True},
    "features": {"enabled": True}
}
