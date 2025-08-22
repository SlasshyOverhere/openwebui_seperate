#!/usr/bin/env python3
"""
Simple startup script for OpenWebUI backend in local development
"""

import uvicorn
import os
from pathlib import Path

if __name__ == "__main__":
    # Create data directory if it doesn't exist
    data_dir = Path("./data")
    data_dir.mkdir(exist_ok=True)
    
    # Set default environment variables for local development
    os.environ.setdefault("DATABASE_URL", "sqlite:///./data/webui.db")
    os.environ.setdefault("WEBUI_SECRET_KEY", "local-dev-secret-key")
    os.environ.setdefault("ENV", "development")
    
    print("🚀 Starting OpenWebUI Backend (Local Development)")
    print("📍 Backend will be available at: http://localhost:8000")
    print("📚 API Documentation: http://localhost:8000/docs")
    print("🔒 CORS configured for: http://localhost:6969")
    print("💾 Database: SQLite (./data/webui.db)")
    print("")
    print("Press Ctrl+C to stop the server")
    print("")
    
    # Start the server
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
