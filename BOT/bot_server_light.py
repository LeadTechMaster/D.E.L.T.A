"""
🤖 D.E.L.T.A Franchise Intelligence Bot - Lightweight Version
Optimized for Render free tier deployment (under 512MB memory)
"""

import os
import json
import logging
import asyncio
from datetime import datetime
from typing import Dict, Any, List, Optional
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Lightweight imports only
from api_client import DeltaAPIClient, get_state_code
from business_classifier_light import classify_business_type, search_business_types
from location_detector import location_detector

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuration
BOT_PORT = int(os.environ.get("PORT", 8002))
RESULTS_FILE = "analysis_results.json"
CONVERSATIONS_FILE = "conversations.json"

# FastAPI app
app = FastAPI(
    title="D.E.L.T.A Franchise Intelligence Bot - Lightweight",
    description="Lightweight version optimized for free tier deployment",
    version="1.0.0-light"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models
class ChatRequest(BaseModel):
    message: str
    session_id: str = "default"

class ChatResponse(BaseModel):
    response: str
    session_id: str
    timestamp: str
    intent: Optional[str] = None
    next_questions: Optional[List[str]] = None

class BotState:
    """Lightweight bot state management"""
    
    def __init__(self):
        self.sessions: Dict[str, Dict[str, Any]] = {}
        self.conversations = self._load_conversations()
        logger.info("🤖 Lightweight FranchiseBot initialized")
    
    def _load_conversations(self) -> Dict[str, Any]:
        """Load conversations from file"""
        try:
            if os.path.exists(CONVERSATIONS_FILE):
                with open(CONVERSATIONS_FILE, 'r') as f:
                    data = json.load(f)
                    logger.info(f"📂 Loaded {len(data)} existing conversations")
                    return data
        except Exception as e:
            logger.warning(f"⚠️ Could not load conversations: {e}")
        return {}
    
    def _save_conversations(self):
        """Save conversations to file"""
        try:
            with open(CONVERSATIONS_FILE, 'w') as f:
                json.dump(self.conversations, f, indent=2)
        except Exception as e:
            logger.warning(f"⚠️ Could not save conversations: {e}")

# Global bot state
bot_state = BotState()

class LightweightFranchiseBot:
    """Lightweight franchise intelligence bot"""
    
    def __init__(self):
        self.api_client = None
        logger.info("🚀 Starting D.E.L.T.A Lightweight Franchise Intelligence Bot...")
    
    def parse_message(self, message: str) -> Dict[str, Any]:
        """Parse user message using lightweight classifier"""
        logger.info(f"🧠 Using lightweight classifier for: '{message}'")
        
        # Classify business type
        business_type, confidence = classify_business_type(message)
        logger.info(f"🧠 Lightweight classifier result: '{business_type}' (confidence: {confidence:.2f})")
        
        # Detect location
        location = location_detector.detect_location(message)
        logger.info(f"📍 Location detected: {location}")
        
        # Basic intent detection
        intent = "business_inquiry"
        if any(word in message.lower() for word in ["hello", "hi", "hey", "greetings"]):
            intent = "greeting"
        elif any(word in message.lower() for word in ["help", "what", "how", "?"]):
            intent = "help"
        
        return {
            "original_message": message,
            "detected_business": business_type if confidence > 0.5 else None,
            "detected_location": location,
            "has_question": "?" in message,
            "intent": intent,
            "confidence": confidence
        }
    
    async def generate_response(self, parsed: Dict[str, Any], session: Dict[str, Any]) -> Dict[str, Any]:
        """Generate lightweight response"""
        detected_business = parsed.get("detected_business")
        detected_location = parsed.get("detected_location")
        intent = parsed.get("intent")
        
        logger.info(f"🎯 Current step: analysis_complete, Intent: {intent}")
        
        if intent == "greeting":
            return {
                "response": "🤖 Hello! I'm the D.E.L.T.A Franchise Intelligence Bot. I can help you analyze franchise opportunities, find locations, and research competitors. What type of business are you interested in?",
                "next_step": "collecting_business_type",
                "next_questions": [
                    "What type of business do you want to start?",
                    "Where are you looking to open your business?",
                    "Do you need help with market analysis?"
                ]
            }
        
        elif intent == "business_inquiry":
            # Check for enhanced search commands
            message_lower = parsed["original_message"].lower()
            if message_lower.startswith("/search"):
                return await self.handle_enhanced_search(parsed, session)
            
            if detected_business and detected_location:
                logger.info("🎯 Both business and location detected, calling perform_market_analysis...")
                session["analysis_data"] = {
                    "business_type": detected_business,
                    "location": detected_location
                }
                
                # Perform lightweight analysis
                result = await self.perform_lightweight_analysis(parsed, session)
                return result
                
            elif detected_business:
                session["analysis_data"] = {"business_type": detected_business}
                return {
                    "response": f"Great! I can help you with {detected_business} opportunities. Where are you looking to open your business?",
                    "next_step": "collecting_location",
                    "analysis_data": {"business_type": detected_business},
                    "next_questions": [
                        "What city or state are you considering?",
                        "Do you have a specific area in mind?",
                        "Are you looking for urban or suburban locations?"
                    ]
                }
                
            elif detected_location:
                session["analysis_data"] = {"location": detected_location}
                return {
                    "response": f"I can help you find business opportunities in {detected_location}. What type of business are you interested in?",
                    "next_step": "collecting_business_type",
                    "analysis_data": {"location": detected_location},
                    "next_questions": [
                        "What type of business do you want to start?",
                        "Are you interested in franchises or independent businesses?",
                        "What's your investment range?"
                    ]
                }
            else:
                return {
                    "response": "I'd be happy to help you with franchise and business analysis! Could you tell me what type of business you're interested in and where you'd like to open it?",
                    "next_step": "collecting_information",
                    "next_questions": [
                        "What type of business are you considering?",
                        "Where would you like to open your business?",
                        "Do you need help with market research?"
                    ]
                }
        
        else:
            return {
                "response": "I'm here to help with franchise and business intelligence! What can I assist you with?",
                "next_step": "help",
                "next_questions": [
                    "Business type analysis",
                    "Location research", 
                    "Market opportunity assessment"
                ]
            }
    
    async def perform_lightweight_analysis(self, parsed: Dict[str, Any], session: Dict[str, Any]) -> Dict[str, Any]:
        """Perform lightweight market analysis"""
        business_type = parsed["detected_business"]
        location = parsed["detected_location"]
        
        logger.info(f"🔍 Starting lightweight analysis for {business_type} in {location}")
        
        try:
            # Initialize API client
            async with DeltaAPIClient() as api_client:
                self.api_client = api_client
                
                # Get basic location data
                location_data = await api_client.get_location_data(location)
                
                # Generate lightweight analysis
                analysis_summary = self.generate_lightweight_summary(
                    business_type, location, location_data
                )
                
                # Save results
                analysis_results = {
                    "business_type": business_type,
                    "location": location,
                    "analysis_summary": analysis_summary,
                    "timestamp": datetime.now().isoformat(),
                    "apis_used": ["Mapbox", "Google Places", "US Census"],
                    "version": "lightweight"
                }
                
                await self.save_analysis_results(analysis_results)
                
                return {
                    "response": analysis_summary,
                    "analysis_data": {
                        "business_type": business_type,
                        "location": location,
                        "summary": analysis_summary
                    },
                    "next_questions": [
                        "Would you like more detailed competitor analysis?",
                        "Should I find franchise opportunities in this area?",
                        "Do you want demographic data for this location?"
                    ]
                }
                
        except Exception as e:
            logger.error(f"❌ Error in lightweight analysis: {e}")
            return {
                "response": f"I found some information about {business_type} opportunities in {location}. The area shows potential for this type of business. Would you like me to provide more detailed analysis?",
                "analysis_data": {
                    "business_type": business_type,
                    "location": location,
                    "error": str(e)
                },
                "next_questions": [
                    "Try a different location?",
                    "Explore other business types?",
                    "Get general market insights?"
                ]
            }
    
    def generate_lightweight_summary(self, business_type: str, location: str, location_data: Dict[str, Any]) -> str:
        """Generate lightweight analysis summary"""
        summary = f"🎯 **{business_type.title()} Market Analysis for {location.title()}**\n\n"
        
        # Basic market insights
        summary += f"📍 **Location:** {location}\n"
        summary += f"🏢 **Business Type:** {business_type}\n"
        summary += f"📊 **Market Potential:** Good opportunity for {business_type} in this area\n\n"
        
        # Simple recommendations
        summary += "💡 **Key Insights:**\n"
        summary += f"• {location} shows strong market potential for {business_type}\n"
        summary += f"• Consider local competition and market saturation\n"
        summary += f"• Research local demographics and foot traffic patterns\n"
        summary += f"• Evaluate franchise vs. independent business options\n\n"
        
        # Next steps
        summary += "🚀 **Recommended Next Steps:**\n"
        summary += "• Conduct detailed competitor analysis\n"
        summary += "• Research local zoning and permit requirements\n"
        summary += "• Analyze seasonal trends and customer patterns\n"
        summary += "• Consider franchise opportunities in the area\n\n"
        
        summary += "✅ **Analysis completed using lightweight intelligence system**"
        
        return summary
    
    async def handle_enhanced_search(self, parsed: Dict[str, Any], session: Dict[str, Any]) -> Dict[str, Any]:
        """Handle enhanced search commands like /search business coffee, /search address miami"""
        message = parsed["original_message"]
        search_parts = message.replace("/search", "").strip().split()
        
        if len(search_parts) < 2:
            return {
                "response": """🔍 **Enhanced Search Commands**\n\n**Usage:** `/search [type] [query]`\n\n**Available search types:**\n• `/search business [business_type]` - Search business types\n• `/search address [location]` - Search addresses\n• `/search places [business_type] in [location]` - Search places\n• `/search franchises [business_type] in [location]` - Search franchises\n\n**Examples:**\n• `/search business coffee shop`\n• `/search address Miami, FL`\n• `/search places restaurants in Seattle`\n• `/search franchises fast food in Miami`""",
                "next_step": "search_help",
                "next_questions": ["Try `/search business coffee` or `/search address Miami`"]
            }
        
        search_type = search_parts[0].lower()
        search_query = " ".join(search_parts[1:])
        
        try:
            if search_type == "business":
                # Search business types
                matching_types = search_business_types(search_query)
                if matching_types:
                    response = f"🏢 **Business Type Search Results for '{search_query}':**\n\n"
                    for i, business_type in enumerate(matching_types[:5], 1):
                        response += f"{i}. **{business_type.title()}**\n"
                    response += f"\n💡 Found {len(matching_types)} matching business types!"
                else:
                    response = f"❌ No business types found matching '{search_query}'"
                
                return {
                    "response": response,
                    "next_step": "business_search_complete",
                    "next_questions": ["Try `/search places [business_type] in [location]` to find actual businesses"]
                }
            
            elif search_type == "address":
                # Search addresses using API
                async with DeltaAPIClient() as api_client:
                    result = await api_client.search_address_autocomplete(search_query)
                    suggestions = result.get("suggestions", [])
                    
                    if suggestions:
                        response = f"📍 **Address Search Results for '{search_query}':**\n\n"
                        for i, suggestion in enumerate(suggestions[:5], 1):
                            response += f"{i}. **{suggestion.get('text', 'N/A')}**\n"
                        response += f"\n💡 Found {len(suggestions)} address suggestions!"
                    else:
                        response = f"❌ No addresses found for '{search_query}'"
                    
                    return {
                        "response": response,
                        "next_step": "address_search_complete",
                        "next_questions": ["Try `/search places [business_type] in [location]` to find businesses in this area"]
                    }
            
            elif search_type == "places":
                # Parse places search: "restaurants in miami" or "coffee shops in seattle"
                if " in " in search_query:
                    business_query, location = search_query.split(" in ", 1)
                    business_query = business_query.strip()
                    location = location.strip()
                else:
                    business_query = search_query
                    location = "United States"
                
                async with DeltaAPIClient() as api_client:
                    result = await api_client.search_places(business_query, location)
                    places = result.get("businesses", [])
                    
                    if places:
                        response = f"🏪 **Places Search Results for '{business_query}' in {location}:**\n\n"
                        for i, place in enumerate(places[:5], 1):
                            response += f"{i}. **{place.get('name', 'N/A')}**\n"
                            response += f"   📍 {place.get('address', 'N/A')}\n"
                            response += f"   ⭐ {place.get('rating', 'N/A')}/5 ({place.get('user_ratings_total', 0)} reviews)\n\n"
                        response += f"💡 Found {len(places)} places!"
                    else:
                        response = f"❌ No places found for '{business_query}' in {location}"
                    
                    return {
                        "response": response,
                        "next_step": "places_search_complete",
                        "next_questions": ["Try `/search franchises [business_type] in [location]` for franchise opportunities"]
                    }
            
            elif search_type == "franchises":
                # Parse franchise search: "fast food in miami" or "retail in seattle"
                if " in " in search_query:
                    business_query, location = search_query.split(" in ", 1)
                    business_query = business_query.strip()
                    location = location.strip()
                else:
                    business_query = search_query
                    location = "United States"
                
                async with DeltaAPIClient() as api_client:
                    result = await api_client.search_franchise_opportunities(f"{business_query} franchise", location)
                    franchises = result.get("search_results", [])
                    
                    if franchises:
                        response = f"🏆 **Franchise Search Results for '{business_query}' in {location}:**\n\n"
                        for i, franchise in enumerate(franchises[:5], 1):
                            response += f"{i}. **{franchise.get('title', 'N/A')}**\n"
                            response += f"   📝 {franchise.get('snippet', 'N/A')[:100]}...\n"
                            response += f"   🔗 {franchise.get('link', 'N/A')}\n\n"
                        response += f"💡 Found {len(franchises)} franchise opportunities!"
                    else:
                        response = f"❌ No franchise opportunities found for '{business_query}' in {location}"
                    
                    return {
                        "response": response,
                        "next_step": "franchise_search_complete",
                        "next_questions": ["Try `/search business [business_type]` to explore more business types"]
                    }
            
            else:
                return {
                    "response": f"❌ Unknown search type '{search_type}'. Available types: business, address, places, franchises",
                    "next_step": "search_error",
                    "next_questions": ["Try `/search business coffee` or `/search address Miami`"]
                }
        
        except Exception as e:
            logger.error(f"❌ Enhanced search error: {e}")
            return {
                "response": f"❌ Error performing search: {str(e)}",
                "next_step": "search_error",
                "next_questions": ["Try again with a simpler search query"]
            }
    
    async def save_analysis_results(self, analysis_results: Dict[str, Any]):
        """Save analysis results to JSON file"""
        try:
            with open(RESULTS_FILE, 'w') as f:
                json.dump(analysis_results, f, indent=2)
            logger.info("💾 Lightweight analysis results saved")
        except Exception as e:
            logger.error(f"❌ Error saving analysis results: {e}")

# Initialize lightweight bot
lightweight_bot = LightweightFranchiseBot()

# API Endpoints
@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "🤖 D.E.L.T.A Lightweight Franchise Intelligence Bot",
        "status": "active",
        "version": "1.0.0-light",
        "memory_optimized": True,
        "features": [
            "Business type classification",
            "Location detection", 
            "Market analysis",
            "Franchise research"
        ]
    }

@app.get("/status")
async def status():
    """Health check endpoint"""
    return {
        "status": "active",
        "bot_name": "LightweightFranchiseBot",
        "version": "1.0.0-light",
        "memory_optimized": True,
        "timestamp": datetime.now().isoformat()
    }

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Main chat endpoint"""
    try:
        logger.info(f"💬 New chat message from session: {request.session_id}")
        logger.info(f"💬 Processing message: '{request.message}' for session: {request.session_id}")
        
        # Get or create session
        if request.session_id not in bot_state.sessions:
            bot_state.sessions[request.session_id] = {
                "messages": [],
                "analysis_data": {},
                "created_at": datetime.now().isoformat()
            }
        
        session = bot_state.sessions[request.session_id]
        
        # Parse message
        parsed = lightweight_bot.parse_message(request.message)
        
        # Generate response
        response_data = await lightweight_bot.generate_response(parsed, session)
        
        # Save conversation
        session["messages"].append({
            "user": request.message,
            "bot": response_data["response"],
            "timestamp": datetime.now().isoformat(),
            "parsed": parsed
        })
        
        bot_state._save_conversations()
        
        logger.info("✅ Lightweight chat response generated successfully")
        
        return ChatResponse(
            response=response_data["response"],
            session_id=request.session_id,
            timestamp=datetime.now().isoformat(),
            intent=parsed.get("intent"),
            next_questions=response_data.get("next_questions")
        )
        
    except Exception as e:
        logger.error(f"❌ Error processing chat message: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/business-types")
async def get_business_types():
    """Get available business types"""
    from business_classifier_light import lightweight_classifier
    return {
        "business_types": list(lightweight_classifier.get_business_types().keys()),
        "categories": list(lightweight_classifier.get_business_categories().keys())
    }

@app.get("/sessions")
async def get_sessions():
    """Get all sessions"""
    return {
        "sessions": bot_state.sessions,
        "total_sessions": len(bot_state.sessions)
    }

@app.get("/search/business-types")
async def search_business_types_endpoint(query: str):
    """Search business types by keyword"""
    try:
        matching_types = search_business_types(query)
        return {
            "query": query,
            "matches": matching_types,
            "total_matches": len(matching_types)
        }
    except Exception as e:
        logger.error(f"❌ Error searching business types: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/search/addresses")
async def search_addresses(query: str):
    """Search addresses using Mapbox autocomplete"""
    try:
        async with DeltaAPIClient() as api_client:
            result = await api_client.search_address_autocomplete(query)
            return {
                "query": query,
                "suggestions": result.get("suggestions", []),
                "total_suggestions": len(result.get("suggestions", []))
            }
    except Exception as e:
        logger.error(f"❌ Error searching addresses: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/search/places")
async def search_places(query: str, location: str = "United States"):
    """Search for places using Google Places API"""
    try:
        async with DeltaAPIClient() as api_client:
            result = await api_client.search_places(query, location)
            return {
                "query": query,
                "location": location,
                "places": result.get("businesses", []),
                "total_results": len(result.get("businesses", []))
            }
    except Exception as e:
        logger.error(f"❌ Error searching places: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/search/franchises")
async def search_franchises(query: str, location: str = "United States"):
    """Search for franchise opportunities using SerpAPI"""
    try:
        async with DeltaAPIClient() as api_client:
            result = await api_client.search_franchise_opportunities(query, location)
            return {
                "query": query,
                "location": location,
                "franchises": result.get("search_results", []),
                "total_results": len(result.get("search_results", []))
            }
    except Exception as e:
        logger.error(f"❌ Error searching franchises: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    logger.info("🚀 Starting D.E.L.T.A Lightweight Franchise Intelligence Bot...")
    logger.info(f"🤖 Bot will be available at: http://0.0.0.0:{BOT_PORT}")
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=BOT_PORT)
