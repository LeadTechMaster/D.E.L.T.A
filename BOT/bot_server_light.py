#!/usr/bin/env python3
"""
🚀 D.E.L.T.A Bot Server - Lightweight Version
Optimized for Render free tier deployment (512MB memory limit)
Uses lightweight classifiers and no heavy AI models
"""

import os
import logging
import asyncio
from typing import Dict, Any, Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

# Force lightweight imports to avoid memory issues
from api_client import DeltaAPIClient, get_state_code
from business_classifier_light import classify_business_type, search_business_types
from location_detector import location_detector

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('bot_server.log')
    ]
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="🚀 D.E.L.T.A Bot API - Lightweight",
    description="Franchise Intelligence Platform - Memory Optimized Version",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request/Response models
class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None
    user_context: Optional[Dict[str, Any]] = None

class ChatResponse(BaseModel):
    response: str
    session_id: str
    business_type: Optional[str] = None
    location: Optional[str] = None
    confidence: Optional[float] = None
    suggestions: Optional[list] = None
    api_data: Optional[Dict[str, Any]] = None

class StatusResponse(BaseModel):
    status: str
    message: str
    version: str
    features: Dict[str, bool]

# Global API client
api_client = None

@app.on_event("startup")
async def startup_event():
    """Initialize the API client on startup"""
    global api_client
    try:
        api_client = DeltaAPIClient()
        logger.info("🚀 D.E.L.T.A Bot Server (Lightweight) started successfully")
        logger.info("💾 Memory optimized for Render free tier (512MB limit)")
    except Exception as e:
        logger.error(f"❌ Failed to initialize API client: {e}")

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    global api_client
    if api_client:
        await api_client.__aexit__(None, None, None)
    logger.info("🛑 D.E.L.T.A Bot Server shutdown")

@app.get("/", response_model=StatusResponse)
async def root():
    """Root endpoint with status"""
    return StatusResponse(
        status="running",
        message="🚀 D.E.L.T.A Franchise Intelligence Platform - Lightweight Version",
        version="1.0.0-light",
        features={
            "business_classification": True,
            "location_detection": True,
            "api_integration": True,
            "memory_optimized": True,
            "smart_ai_features": False,  # Disabled for memory optimization
            "heavy_models": False
        }
    )

@app.get("/status", response_model=StatusResponse)
async def status():
    """Health check endpoint"""
    return StatusResponse(
        status="healthy",
        message="D.E.L.T.A Bot is running in lightweight mode",
        version="1.0.0-light",
        features={
            "business_classification": True,
            "location_detection": True,
            "api_integration": True,
            "memory_optimized": True,
            "smart_ai_features": False,
            "heavy_models": False
        }
    )

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Main chat endpoint with lightweight processing"""
    try:
        logger.info(f"💬 Chat request: {request.message[:100]}...")
        
        # Lightweight business type classification
        business_result = classify_business_type(request.message)
        business_type = business_result.get("business_type") if business_result else None
        
        # Lightweight location detection
        location_result = location_detector(request.message)
        location = location_result.get("location") if location_result else None
        
        # Generate response using lightweight logic
        response_text = await generate_lightweight_response(
            request.message, 
            business_type, 
            location
        )
        
        # Generate suggestions
        suggestions = generate_suggestions(business_type, location)
        
        return ChatResponse(
            response=response_text,
            session_id=request.session_id or "lightweight_session",
            business_type=business_type,
            location=location,
            confidence=business_result.get("confidence", 0.0) if business_result else None,
            suggestions=suggestions,
            api_data=None  # No heavy API calls in lightweight mode
        )
        
    except Exception as e:
        logger.error(f"❌ Chat error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

async def generate_lightweight_response(message: str, business_type: str = None, location: str = None) -> str:
    """Generate response using lightweight logic (no heavy AI models)"""
    
    response_parts = []
    
    # Business type response
    if business_type:
        response_parts.append(f"I can help you with {business_type} opportunities!")
    
    # Location response
    if location:
        response_parts.append(f"I see you're interested in {location}.")
    
    # Default response
    if not response_parts:
        response_parts.append("I'm here to help with franchise and business opportunities!")
    
    # Add helpful suggestions
    if business_type and location:
        response_parts.append(f"For {business_type} in {location}, I can help you analyze the market, find competitors, and identify opportunities.")
    elif business_type:
        response_parts.append(f"For {business_type}, I can help you find locations, analyze markets, and research opportunities.")
    else:
        response_parts.append("Tell me what type of business you're interested in and where you'd like to operate!")
    
    return " ".join(response_parts)

def generate_suggestions(business_type: str = None, location: str = None) -> list:
    """Generate helpful suggestions"""
    suggestions = []
    
    if business_type and location:
        suggestions.extend([
            f"Analyze {business_type} market in {location}",
            f"Find {business_type} competitors in {location}",
            f"Research {business_type} opportunities in {location}"
        ])
    elif business_type:
        suggestions.extend([
            f"Find best locations for {business_type}",
            f"Research {business_type} market trends",
            f"Analyze {business_type} competition"
        ])
    else:
        suggestions.extend([
            "What type of business interests you?",
            "Where would you like to operate?",
            "Tell me about your franchise goals"
        ])
    
    return suggestions[:5]  # Limit to 5 suggestions

@app.get("/business-types")
async def get_business_types():
    """Get available business types"""
    return {
        "business_types": [
            "coffee shop", "restaurant", "retail", "fitness", "beauty",
            "healthcare", "education", "automotive", "home services", "technology"
        ],
        "total": 10
    }

@app.get("/health")
async def health_check():
    """Simple health check"""
    return {"status": "healthy", "mode": "lightweight"}

if __name__ == "__main__":
    # Run the server
    uvicorn.run(
        "bot_server_light:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", 8002)),
        reload=False,  # Disable reload for production
        log_level="info"
    )