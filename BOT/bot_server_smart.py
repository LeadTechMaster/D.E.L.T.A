#!/usr/bin/env python3
"""
🤖 D.E.L.T.A Smart Optimized Franchise Intelligence Bot
Full AI features with memory optimization for production deployment
"""

import json
import logging
import os
from datetime import datetime
from typing import Dict, Any, Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

# Smart AI imports with error handling for memory optimization
try:
    from api_client import DeltaAPIClient, get_state_code
    from business_classifier import classify_business_type, search_business_types
    from location_detector import location_detector
    from smart_context_analyzer import smart_context_analyzer, ContextAnalysis
    from intelligent_response_generator import intelligent_response_generator, ResponseContext
    from conversation_memory import conversation_memory
    from predictive_analytics import predictive_analytics, MarketTrend, OpportunityScore
    from advanced_nlp import advanced_nlp, ContextAnalysis as NLPContextAnalysis
    from smart_conversation_flow import smart_conversation_flow, ConversationContext
    from intelligent_comparison_engine import intelligent_comparison_engine, SmartRecommendation
    SMART_FEATURES_AVAILABLE = True
    logger = logging.getLogger(__name__)
    logger.info("🧠 All smart AI features loaded successfully")
except ImportError as e:
    logger = logging.getLogger(__name__)
    logger.warning(f"⚠️ Some smart features not available: {e}")
    SMART_FEATURES_AVAILABLE = False
    # Fallback imports
    from api_client import DeltaAPIClient, get_state_code
    from business_classifier_light import classify_business_type, search_business_types
    from location_detector import location_detector

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bot.log'),
        logging.StreamHandler()
    ]
)

# Bot Configuration
BOT_PORT = int(os.getenv("PORT", 8002))
STORAGE_DIR = "storage"
CONVERSATIONS_FILE = f"{STORAGE_DIR}/conversations.json"
RESULTS_FILE = f"{STORAGE_DIR}/analysis_results.json"

# Create storage directory
os.makedirs(STORAGE_DIR, exist_ok=True)

# Initialize FastAPI
app = FastAPI(
    title="🤖 D.E.L.T.A Smart Optimized Franchise Intelligence Bot",
    description="Advanced AI-powered franchise intelligence with memory optimization",
    version="2.0.0-smart"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models
class BotMessage(BaseModel):
    message: str
    session_id: Optional[str] = None

class BotResponse(BaseModel):
    response: str
    session_id: str
    timestamp: str
    intent: Optional[str] = None
    next_questions: Optional[list] = None
    analysis_data: Optional[dict] = None

class BotState:
    """Smart bot state management"""
    def __init__(self):
        self.sessions = {}
        self.conversations = self.load_conversations()
        self.analysis_results = self.load_analysis_results()
    
    def load_conversations(self):
        """Load conversations from file"""
        try:
            if os.path.exists(CONVERSATIONS_FILE):
                with open(CONVERSATIONS_FILE, 'r') as f:
                    return json.load(f)
        except Exception as e:
            logger.warning(f"⚠️ Could not load conversations: {e}")
        return {}
    
    def save_conversations(self):
        """Save conversations to file"""
        try:
            with open(CONVERSATIONS_FILE, 'w') as f:
                json.dump(self.conversations, f, indent=2)
        except Exception as e:
            logger.warning(f"⚠️ Could not save conversations: {e}")
    
    def load_analysis_results(self):
        """Load analysis results from file"""
        try:
            if os.path.exists(RESULTS_FILE):
                with open(RESULTS_FILE, 'r') as f:
                    return json.load(f)
        except Exception as e:
            logger.warning(f"⚠️ Could not load analysis results: {e}")
        return {}
    
    def save_analysis_results(self, results):
        """Save analysis results to file"""
        try:
            with open(RESULTS_FILE, 'w') as f:
                json.dump(results, f, indent=2)
        except Exception as e:
            logger.warning(f"⚠️ Could not save analysis results: {e}")
    
    def get_session(self, session_id: str) -> Dict[str, Any]:
        """Get or create session"""
        if session_id not in self.sessions:
            self.sessions[session_id] = {
                "session_id": session_id,
                "created_at": datetime.now().isoformat(),
                "current_step": "greeting",
                "analysis_data": {},
                "messages": []
            }
        return self.sessions[session_id]
    
    def add_message(self, session_id: str, user_message: str, bot_response: str):
        """Add message to session"""
        session = self.get_session(session_id)
        session["messages"].append({
            "user": user_message,
            "bot": bot_response,
            "timestamp": datetime.now().isoformat()
        })

# Initialize bot state
bot_state = BotState()

class SmartFranchiseBot:
    """Smart optimized franchise intelligence bot"""
    
    def __init__(self):
        self.smart_features_available = SMART_FEATURES_AVAILABLE
        logger.info(f"🤖 Smart bot initialized with features: {self.smart_features_available}")
    
    async def process_message(self, message: str, session_id: str) -> BotResponse:
        """Process user message with smart AI features"""
        try:
            # Get or create session
            session = bot_state.get_session(session_id)
            
            # Parse message with smart features
            if self.smart_features_available:
                parsed = await self.parse_message_smart(message, session)
            else:
                parsed = self.parse_message_basic(message)
            
            logger.info(f"🧠 Parsed message: {parsed}")
            
            # Generate response with smart features
            if self.smart_features_available:
                response_data = await self.generate_smart_response(parsed, session, session_id)
            else:
                response_data = await self.generate_basic_response(parsed, session)
            
            # Add to conversation history
            bot_state.add_message(session_id, message, response_data["response"])
            
            # Create bot response
            bot_response = BotResponse(
                response=response_data["response"],
                session_id=session_id,
                timestamp=datetime.now().isoformat(),
                intent=response_data.get("intent"),
                next_questions=response_data.get("next_questions"),
                analysis_data=response_data.get("analysis_data")
            )
            
            logger.info("✅ Message processed successfully with smart features")
            return bot_response
            
        except Exception as e:
            logger.error(f"❌ Error processing message: {e}")
            return BotResponse(
                response=f"Sorry, I encountered an error: {str(e)}",
                session_id=session_id,
                timestamp=datetime.now().isoformat()
            )
    
    async def parse_message_smart(self, message: str, session: Dict[str, Any]) -> Dict[str, Any]:
        """Parse message with smart AI features"""
        message_lower = message.lower()
        
        # Check for enhanced search commands first
        if message_lower.startswith("/search"):
            return await self.parse_enhanced_search(message)
        
        # Use smart context analyzer
        context_analysis = smart_context_analyzer.analyze_context(message)
        logger.info(f"🧠 Smart context analysis: {context_analysis.intent}")
        
        # Use intelligent business classifier
        detected_business, confidence = classify_business_type(message)
        logger.info(f"🧠 Smart classifier result: '{detected_business}' (confidence: {confidence:.2f})")
        
        # Use intelligent location detector
        detected_location = location_detector.detect_location(message)
        logger.info(f"🔍 Smart location detected: {detected_location}")
        
        return {
            "original_message": message,
            "detected_business": detected_business,
            "detected_location": detected_location,
            "has_question": "?" in message,
            "intent": context_analysis.intent.value,
            "confidence": confidence,
            "context_analysis": context_analysis,
            "entities": context_analysis.entities
        }
    
    def parse_message_basic(self, message: str) -> Dict[str, Any]:
        """Basic message parsing fallback"""
        message_lower = message.lower()
        
        # Check for enhanced search commands
        if message_lower.startswith("/search"):
            return {"original_message": message, "intent": "enhanced_search"}
        
        # Basic classification
        detected_business, confidence = classify_business_type(message)
        detected_location = location_detector.detect_location(message)
        
        # Basic intent detection
        intent = "business_inquiry"
        if any(word in message_lower for word in ["hello", "hi", "hey"]):
            intent = "greeting"
        elif any(word in message_lower for word in ["help", "what", "how"]):
            intent = "help"
        
        return {
            "original_message": message,
            "detected_business": detected_business,
            "detected_location": detected_location,
            "has_question": "?" in message,
            "intent": intent,
            "confidence": confidence
        }
    
    async def parse_enhanced_search(self, message: str) -> Dict[str, Any]:
        """Parse enhanced search commands"""
        search_parts = message.replace("/search", "").strip().split()
        
        if len(search_parts) < 2:
            return {
                "original_message": message,
                "intent": "search_help",
                "search_type": None,
                "search_query": None
            }
        
        search_type = search_parts[0].lower()
        search_query = " ".join(search_parts[1:])
        
        return {
            "original_message": message,
            "intent": "enhanced_search",
            "search_type": search_type,
            "search_query": search_query
        }
    
    async def generate_smart_response(self, parsed: Dict[str, Any], session: Dict[str, Any], session_id: str) -> Dict[str, Any]:
        """Generate response with smart AI features"""
        intent = parsed.get("intent")
        
        # Handle enhanced search
        if intent == "enhanced_search":
            return await self.handle_enhanced_search(parsed, session)
        
        # Handle greeting with smart response generator
        if intent == "greeting":
            if self.smart_features_available:
                response_context = ResponseContext(
                    user_message=parsed["original_message"],
                    detected_business=None,
                    detected_location=None,
                    intent="greeting",
                    entities={}
                )
                intelligent_response = intelligent_response_generator.generate_intelligent_response(response_context)
                follow_up_questions = intelligent_response_generator.generate_follow_up_questions(response_context)
                
                return {
                    "response": intelligent_response,
                    "intent": "greeting",
                    "next_questions": follow_up_questions
                }
            else:
                return {
                    "response": "🤖 Hello! I'm the D.E.L.T.A Smart Franchise Intelligence Bot. How can I help you today?",
                    "intent": "greeting",
                    "next_questions": ["What type of business are you interested in?", "Where are you looking to open?"]
                }
        
        # Handle business inquiry with smart features
        if intent == "business_inquiry":
            detected_business = parsed.get("detected_business")
            detected_location = parsed.get("detected_location")
            context_analysis = parsed.get("context_analysis")
            
            if detected_business and detected_location:
                logger.info("🎯 Both business and location detected, performing smart analysis...")
                session["analysis_data"] = {
                    "business_type": detected_business,
                    "location": detected_location
                }
                
                # Update conversation flow context
                if self.smart_features_available:
                    try:
                        smart_conversation_flow.update_context(
                            session_id, 
                            business_type=detected_business,
                            location=detected_location
                        )
                    except Exception as e:
                        logger.warning(f"⚠️ Could not update conversation flow: {e}")
                
                # Perform analysis
                result = await self.perform_market_analysis(parsed, session)
                
                # Generate smart follow-ups
                if self.smart_features_available:
                    try:
                        smart_follow_ups = smart_conversation_flow.generate_smart_follow_ups(
                            session_id, result.get("analysis_data", {})
                        )
                        if smart_follow_ups:
                            result["next_questions"] = [fup.question for fup in smart_follow_ups]
                    except Exception as e:
                        logger.warning(f"⚠️ Could not generate smart follow-ups: {e}")
                
                # Enhance with smart suggestions
                if context_analysis and hasattr(context_analysis, 'smart_response') and context_analysis.smart_response:
                    result["response"] = context_analysis.smart_response + "\n\n" + result["response"]
                
                return result
            
            elif detected_business:
                session["analysis_data"] = {"business_type": detected_business}
                if self.smart_features_available:
                    response_context = ResponseContext(
                        user_message=parsed["original_message"],
                        detected_business=detected_business,
                        detected_location=detected_location,
                        intent=intent,
                        entities=parsed.get("entities", {})
                    )
                    intelligent_response = intelligent_response_generator.generate_intelligent_response(response_context)
                    follow_up_questions = intelligent_response_generator.generate_follow_up_questions(response_context)
                else:
                    intelligent_response = f"Great! I can help you with {detected_business} opportunities. Where are you looking to open your business?"
                    follow_up_questions = ["What city or state are you interested in?", "Do you have a specific area in mind?"]
                
                return {
                    "response": intelligent_response,
                    "intent": "business_inquiry",
                    "next_questions": follow_up_questions,
                    "analysis_data": {"business_type": detected_business}
                }
            
            elif detected_location:
                session["analysis_data"] = {"location": detected_location}
                if self.smart_features_available:
                    response_context = ResponseContext(
                        user_message=parsed["original_message"],
                        detected_business=None,
                        detected_location=detected_location,
                        intent=intent,
                        entities=parsed.get("entities", {})
                    )
                    intelligent_response = intelligent_response_generator.generate_intelligent_response(response_context)
                    follow_up_questions = intelligent_response_generator.generate_follow_up_questions(response_context)
                else:
                    intelligent_response = f"I can help you find business opportunities in {detected_location}. What type of business are you interested in?"
                    follow_up_questions = ["What type of business do you want to start?", "Are you looking for franchises or independent businesses?"]
                
                return {
                    "response": intelligent_response,
                    "intent": "business_inquiry",
                    "next_questions": follow_up_questions,
                    "analysis_data": {"location": detected_location}
                }
        
        # Default response
        return {
            "response": "I can help you with franchise intelligence and market analysis. What would you like to know?",
            "intent": "unknown",
            "next_questions": ["Try asking about a specific business type or location"]
        }
    
    async def generate_basic_response(self, parsed: Dict[str, Any], session: Dict[str, Any]) -> Dict[str, Any]:
        """Basic response generation fallback"""
        intent = parsed.get("intent")
        
        if intent == "enhanced_search":
            return await self.handle_enhanced_search(parsed, session)
        elif intent == "greeting":
            return {
                "response": "🤖 Hello! I'm the D.E.L.T.A Franchise Intelligence Bot. How can I help you?",
                "intent": "greeting"
            }
        elif intent == "business_inquiry":
            detected_business = parsed.get("detected_business")
            detected_location = parsed.get("detected_location")
            
            if detected_business and detected_location:
                result = await self.perform_market_analysis(parsed, session)
                return result
            elif detected_business:
                return {
                    "response": f"Great! I can help you with {detected_business} opportunities. Where are you looking to open?",
                    "intent": "business_inquiry"
                }
            elif detected_location:
                return {
                    "response": f"I can help you find opportunities in {detected_location}. What type of business are you interested in?",
                    "intent": "business_inquiry"
                }
        
        return {
            "response": "I can help you with franchise intelligence. What would you like to know?",
            "intent": "unknown"
        }
    
    async def handle_enhanced_search(self, parsed: Dict[str, Any], session: Dict[str, Any]) -> Dict[str, Any]:
        """Handle enhanced search commands with smart features"""
        search_type = parsed.get("search_type")
        search_query = parsed.get("search_query")
        
        if not search_type or not search_query:
            return {
                "response": """🔍 **Enhanced Search Commands**\n\n**Usage:** `/search [type] [query]`\n\n**Available search types:**\n• `/search business [business_type]` - Search business types\n• `/search address [location]` - Search addresses\n• `/search places [business_type] in [location]` - Search places\n• `/search franchises [business_type] in [location]` - Search franchises\n\n**Examples:**\n• `/search business coffee shop`\n• `/search address Miami, FL`\n• `/search places restaurants in Seattle`\n• `/search franchises fast food in Miami`""",
                "intent": "search_help",
                "next_questions": ["Try `/search business coffee` or `/search address Miami`"]
            }
        
        try:
            if search_type == "business":
                matching_types = search_business_types(search_query)
                if matching_types:
                    response = f"🏢 **Business Type Search Results for '{search_query}':**\n\n"
                    for i, business_type in enumerate(matching_types[:5], 1):
                        # Handle both string and tuple formats
                        if isinstance(business_type, tuple):
                            business_type = business_type[0]
                        response += f"{i}. **{business_type.title()}**\n"
                    response += f"\n💡 Found {len(matching_types)} matching business types!"
                else:
                    response = f"❌ No business types found matching '{search_query}'"
                
                return {
                    "response": response,
                    "intent": "business_search_complete",
                    "next_questions": ["Try `/search places [business_type] in [location]` to find actual businesses"]
                }
            
            elif search_type == "address":
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
                        "intent": "address_search_complete",
                        "next_questions": ["Try `/search places [business_type] in [location]` to find businesses in this area"]
                    }
            
            elif search_type == "places":
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
                        "intent": "places_search_complete",
                        "next_questions": ["Try `/search franchises [business_type] in [location]` for franchise opportunities"]
                    }
            
            elif search_type == "franchises":
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
                        "intent": "franchise_search_complete",
                        "next_questions": ["Try `/search business [business_type]` to explore more business types"]
                    }
            
            else:
                return {
                    "response": f"❌ Unknown search type '{search_type}'. Available types: business, address, places, franchises",
                    "intent": "search_error",
                    "next_questions": ["Try `/search business coffee` or `/search address Miami`"]
                }
        
        except Exception as e:
            logger.error(f"❌ Enhanced search error: {e}")
            return {
                "response": f"❌ Error performing search: {str(e)}",
                "intent": "search_error",
                "next_questions": ["Try again with a simpler search query"]
            }
    
    async def perform_market_analysis(self, parsed: Dict[str, Any], session: Dict[str, Any]) -> Dict[str, Any]:
        """Perform comprehensive market analysis with smart features"""
        business_type = parsed.get("detected_business")
        location = parsed.get("detected_location")
        
        if not business_type or not location:
            return {
                "response": "I need both a business type and location to perform analysis.",
                "intent": "analysis_incomplete"
            }
        
        logger.info(f"🎯 Starting market analysis for {business_type} in {location}")
        
        try:
            async with DeltaAPIClient() as api_client:
                analysis_results = {}
                
                # Get location data
                location_result = await api_client.get_location_data(location)
                analysis_results["location"] = location_result
                
                # Get places data
                places_result = await api_client.search_places(business_type, location)
                analysis_results["places"] = places_result
                
                # Get franchise opportunities
                franchise_result = await api_client.search_franchise_opportunities(f"{business_type} franchise", location)
                analysis_results["franchises"] = franchise_result
                
                # Get demographics
                state_code = get_state_code(location)
                if state_code:
                    demographics_result = await api_client.get_demographics(state_code)
                    analysis_results["demographics"] = demographics_result
                
                # Generate smart analysis summary
                summary = await self.generate_smart_analysis_summary(analysis_results, business_type, location)
                
                # Save analysis results
                bot_state.save_analysis_results(analysis_results)
                
                return {
                    "response": summary,
                    "intent": "analysis_complete",
                    "analysis_data": analysis_results,
                    "next_questions": [
                        "Would you like to see detailed competitor analysis?",
                        "Should I find franchise opportunities in this area?",
                        "Do you want demographic data for this location?"
                    ]
                }
        
        except Exception as e:
            logger.error(f"❌ Market analysis error: {e}")
            return {
                "response": f"Sorry, I encountered an error during analysis: {str(e)}",
                "intent": "analysis_error"
            }
    
    async def generate_smart_analysis_summary(self, analysis_results: Dict[str, Any], business_type: str, location: str) -> str:
        """Generate smart analysis summary with AI features"""
        summary = f"🎯 **Smart Market Analysis for {business_type.title()} in {location}**\n\n"
        
        # Location information
        if "location" in analysis_results and analysis_results["location"].get("status") == "success":
            location_data = analysis_results["location"]
            summary += f"📍 **Location:** {location_data.get('place_name', location)}\n"
            coords = location_data.get('coordinates', {})
            summary += f"🌍 **Coordinates:** {coords.get('latitude', 'N/A')}, {coords.get('longitude', 'N/A')}\n\n"
        
        # Places analysis
        if "places" in analysis_results and analysis_results["places"].get("status") == "success":
            places_data = analysis_results["places"]
            businesses = places_data.get("businesses", [])
            summary += f"🏪 **Found {len(businesses)} businesses** in the area\n"
            
            if businesses:
                # Calculate average rating
                ratings = [b.get("rating", 0) for b in businesses if b.get("rating")]
                avg_rating = sum(ratings) / len(ratings) if ratings else 0
                summary += f"⭐ **Average Rating:** {avg_rating:.1f}/5\n"
                
                # Show top competitors
                summary += f"\n🏆 **Top Competitors:**\n"
                for i, business in enumerate(businesses[:5], 1):
                    summary += f"{i}. **{business.get('name', 'N/A')}** - {business.get('rating', 'N/A')}/5\n"
                summary += "\n"
        
        # Franchise opportunities
        if "franchises" in analysis_results and analysis_results["franchises"].get("status") == "success":
            franchise_data = analysis_results["franchises"]
            franchises = franchise_data.get("search_results", [])
            summary += f"🏆 **Found {len(franchises)} franchise opportunities**\n\n"
        
        # Demographics
        if "demographics" in analysis_results and analysis_results["demographics"].get("status") == "success":
            demo_data = analysis_results["demographics"]
            demographics = demo_data.get("demographics", {})
            summary += f"👥 **Demographics:**\n"
            summary += f"• Population: {demographics.get('total_population', 'N/A'):,}\n"
            summary += f"• Median Income: ${demographics.get('median_household_income', 'N/A'):,}\n\n"
        
        # Smart recommendations with AI features
        if self.smart_features_available:
            try:
                # Use predictive analytics for smart recommendations
                market_trend = predictive_analytics.analyze_market_trends(business_type, location, analysis_results)
                opportunity_score = predictive_analytics.calculate_opportunity_score(analysis_results)
                
                summary += f"🧠 **Smart AI Analysis:**\n"
                summary += f"• Market Trend: {market_trend.trend_direction}\n"
                summary += f"• Opportunity Score: {opportunity_score.overall_score:.1f}/10\n"
                summary += f"• Risk Level: {opportunity_score.risk_level}\n\n"
                
                if opportunity_score.recommendations:
                    summary += f"💡 **AI Recommendations:**\n"
                    for rec in opportunity_score.recommendations[:3]:
                        summary += f"• {rec}\n"
                    summary += "\n"
                
            except Exception as e:
                logger.warning(f"⚠️ Could not generate smart AI analysis: {e}")
        
        summary += "✅ **Analysis completed with smart AI features**"
        return summary

# Initialize smart bot
smart_bot = SmartFranchiseBot()

# API Endpoints
@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "🤖 D.E.L.T.A Smart Optimized Franchise Intelligence Bot",
        "status": "active",
        "version": "2.0.0-smart",
        "smart_features": SMART_FEATURES_AVAILABLE,
        "features": [
            "Smart AI business classification",
            "Intelligent location detection", 
            "Enhanced search functionality",
            "Smart market analysis",
            "Predictive analytics",
            "Conversation memory",
            "Smart follow-up generation"
        ]
    }

@app.get("/status")
async def get_status():
    """Get bot status"""
    return {
        "status": "active",
        "bot_name": "SmartFranchiseBot",
        "version": "2.0.0-smart",
        "smart_features": SMART_FEATURES_AVAILABLE,
        "timestamp": datetime.now().isoformat()
    }

@app.post("/chat", response_model=BotResponse)
async def chat(message: BotMessage):
    """Main chat endpoint with smart features"""
    session_id = message.session_id or f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    try:
        response = await smart_bot.process_message(message.message, session_id)
        
        # Add to conversation memory if available
        if SMART_FEATURES_AVAILABLE:
            try:
                conversation_memory.add_turn(
                    session_id,
                    user_message=message.message,
                    bot_response=response.response
                )
            except Exception as e:
                logger.warning(f"⚠️ Could not add to conversation memory: {e}")
        
        return response
        
    except Exception as e:
        logger.error(f"❌ Chat error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Enhanced Search Endpoints
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
            result = await api_client.search_franchise_opportunities(f"{query} franchise", location)
            return {
                "query": query,
                "location": location,
                "franchises": result.get("search_results", []),
                "total_results": len(result.get("search_results", []))
            }
    except Exception as e:
        logger.error(f"❌ Error searching franchises: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Smart AI Endpoints (if features available)
if SMART_FEATURES_AVAILABLE:
    @app.post("/compare")
    async def compare_options(comparison_request: dict):
        """Smart comparison endpoint"""
        try:
            comparison_type = comparison_request.get("type", "business_types")
            items = comparison_request.get("items", [])
            business_type = comparison_request.get("business_type")
            location = comparison_request.get("location")
            user_profile = comparison_request.get("user_profile", {})
            
            if comparison_type == "business_types" and business_type and location:
                # Compare business types for a location
                market_data = {}
                for item in items:
                    market_data[item] = {
                        "territory_analysis": {"competitor_count": 5, "opportunity_score": 0.6},
                        "demographics": {"total_population": 1000000, "median_household_income": 60000},
                        "franchise_opportunities": []
                    }
                
                results = intelligent_comparison_engine.compare_business_types(
                    items, market_data, user_profile
                )
                
                # Convert to serializable format
                serializable_results = []
                for result in results:
                    serializable_results.append({
                        "item_name": result.item_name,
                        "overall_score": result.overall_score,
                        "strengths": result.strengths,
                        "weaknesses": result.weaknesses,
                        "recommendation_reason": result.recommendation_reason,
                        "best_for": result.best_for,
                        "criteria_scores": {
                            "profitability": result.criteria_scores.profitability,
                            "competition_level": result.criteria_scores.competition_level,
                            "investment_required": result.criteria_scores.investment_required,
                            "growth_potential": result.criteria_scores.growth_potential,
                            "market_demand": result.criteria_scores.market_demand,
                            "location_suitability": result.criteria_scores.location_suitability,
                            "franchise_support": result.criteria_scores.franchise_support,
                            "risk_level": result.criteria_scores.risk_level
                        }
                    })
                
                return {"comparison_results": serializable_results}
            
            else:
                raise HTTPException(status_code=400, detail="Invalid comparison request")
                
        except Exception as e:
            logger.error(f"❌ Comparison error: {e}")
            raise HTTPException(status_code=500, detail=str(e))
    
    @app.get("/conversation-flow/{session_id}")
    async def get_conversation_flow(session_id: str):
        """Get conversation flow status"""
        try:
            next_step = smart_conversation_flow.get_next_conversation_step(session_id)
            return {"conversation_flow": next_step}
        except Exception as e:
            logger.error(f"❌ Conversation flow error: {e}")
            raise HTTPException(status_code=500, detail=str(e))

@app.get("/sessions")
async def get_sessions():
    """Get all sessions"""
    return {
        "sessions": bot_state.sessions,
        "total_sessions": len(bot_state.sessions),
        "smart_features": SMART_FEATURES_AVAILABLE
    }

if __name__ == "__main__":
    logger.info("🚀 Starting D.E.L.T.A Smart Optimized Franchise Intelligence Bot...")
    logger.info(f"🤖 Bot will be available at: http://0.0.0.0:{BOT_PORT}")
    logger.info(f"🧠 Smart features available: {SMART_FEATURES_AVAILABLE}")
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=BOT_PORT)
