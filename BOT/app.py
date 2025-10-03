#!/usr/bin/env python3
"""
🚀 D.E.L.T.A Franchise Intelligence Bot - Production Deployment
Production-ready FastAPI application for Render deployment
"""

import os
import sys
from pathlib import Path

# Add the BOT directory to Python path
sys.path.append(str(Path(__file__).parent))

# Import the main bot server
from bot_server import app

# Production configuration
if __name__ == "__main__":
    import uvicorn
    
    # Get port from environment variable (Render sets this)
    port = int(os.environ.get("PORT", 8000))
    
    # Run with production settings
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=port,
        workers=1,  # Render free tier limitation
        log_level="info"
    )
