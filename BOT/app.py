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

# For gunicorn deployment, we just need to expose the app object
# The render.yaml startCommand handles the gunicorn execution
