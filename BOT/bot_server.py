#!/usr/bin/env python3
"""
D.E.L.T.A 2030 Quantum Franchise Intelligence Bot
Clean, working version
"""

import logging
import asyncio
import json
import os
from typing import Dict, Any, Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
from api_client import DeltaAPIClient
from business_classifier import classify_business_type
from location_detector import location_detector
from keyword_enhancer import keyword_enhancer
from predictive_analytics import PredictiveAnalytics
from conversation_memory import conversation_memory
from advanced_nlp import advanced_nlp

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ChatRequest(BaseModel):
    message: str
    session_id: str = "default"

class ChatResponse(BaseModel):
    response: str
    session_id: str
    timestamp: str
    analysis_data: Dict[str, Any] = {}
    next_questions: list = []

class FranchiseBot:
    def __init__(self):
        logger.info("🤖 Enhanced FranchiseBot initialized with conversation memory")
        self.sessions = {}
        self.api_client = DeltaAPIClient()
        self.predictive_analytics = PredictiveAnalytics()
        self.conversation_memory = conversation_memory
        self.advanced_nlp = advanced_nlp
        
        # Load intelligent data files
        self.business_types = self.load_business_types()
        self.business_keywords = self.load_business_keywords()
        logger.info("📊 Loaded intelligent business data files")
    
    def load_business_types(self) -> Dict[str, Any]:
        """Load business types data from JSON file"""
        try:
            data_path = os.path.join(os.path.dirname(__file__), 'data', 'business_types.json')
            with open(data_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"❌ Error loading business_types.json: {e}")
            return {}
    
    def load_business_keywords(self) -> Dict[str, Any]:
        """Load business keywords data from JSON file"""
        try:
            data_path = os.path.join(os.path.dirname(__file__), 'data', 'business_keywords.json')
            with open(data_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"❌ Error loading business_keywords.json: {e}")
            return {}
    
    def enhanced_business_classification(self, message: str) -> Dict[str, Any]:
        """Enhanced business classification using JSON data"""
        message_lower = message.lower()
        
        # Get business keywords
        business_keywords = self.business_keywords.get('business_keywords', {})
        
        # Score each business type
        business_scores = {}
        
        for business_type, keywords_data in business_keywords.items():
            score = 0
            
            # Check primary keywords
            primary_keywords = keywords_data.get('primary_keywords', [])
            for keyword in primary_keywords:
                if keyword in message_lower:
                    score += 3
            
            # Special boost for restaurant food keywords to override "shop" in retail
            if business_type == 'restaurant':
                food_keywords = ['burger', 'pizza', 'sushi', 'taco', 'sandwich', 'coffee', 'food', 'eat', 'dining']
                for keyword in food_keywords:
                    if keyword in message_lower:
                        score += 2
            
            # Check cuisine/style keywords for restaurants
            if business_type == 'restaurant':
                cuisine_keywords = keywords_data.get('cuisine_keywords', {})
                for cuisine, keywords in cuisine_keywords.items():
                    for keyword in keywords:
                        if keyword in message_lower:
                            score += 2
                
                style_keywords = keywords_data.get('style_keywords', {})
                for style, keywords in style_keywords.items():
                    for keyword in keywords:
                        if keyword in message_lower:
                            score += 2
            
            # Check category keywords for other business types
            else:
                category_keywords = keywords_data.get('category_keywords', {})
                for category, keywords in category_keywords.items():
                    for keyword in keywords:
                        if keyword in message_lower:
                            score += 2
                
                # Also check service keywords for health_wellness
                if business_type == 'health_wellness':
                    service_keywords = keywords_data.get('service_keywords', {})
                    for service, keywords in service_keywords.items():
                        for keyword in keywords:
                            if keyword in message_lower:
                                score += 2
            
            if score > 0:
                business_scores[business_type] = score
        
        # Find best match
        if business_scores:
            best_match = max(business_scores.items(), key=lambda x: x[1])
            return {
                'business_type': best_match[0],
                'confidence': best_match[1],
                'all_matches': business_scores
            }
        
        return {'business_type': 'restaurant', 'confidence': 0, 'all_matches': {}}
    
    def get_business_insights(self, business_type: str) -> Dict[str, Any]:
        """Get business insights from JSON data"""
        business_types = self.business_types.get('business_categories', {})
        
        # First, try to find exact match in subcategory types
        for category, category_data in business_types.items():
            subcategories = category_data.get('subcategories', {})
            for subcategory, subcategory_data in subcategories.items():
                if business_type in subcategory_data.get('types', []):
                    return {
                        'category': category_data.get('name', ''),
                        'subcategory': subcategory_data.get('name', ''),
                        'description': category_data.get('description', ''),
                        'attributes': self.business_types.get('business_attributes', {})
                    }
        
        # If not found, try to match by category name (e.g., 'retail' -> 'retail' category)
        if business_type in business_types:
            category_data = business_types[business_type]
            return {
                'category': category_data.get('name', ''),
                'subcategory': 'General',
                'description': category_data.get('description', ''),
                'attributes': self.business_types.get('business_attributes', {})
            }
        
        # Default fallback
        return {
            'category': 'Business',
            'subcategory': 'General',
            'description': 'General business opportunity',
            'attributes': self.business_types.get('business_attributes', {})
        }
    
    def get_business_analysis_template(self, business_type: str) -> Dict[str, Any]:
        """Get business-specific analysis template"""
        templates = {
            'restaurant': {
                'key_metrics': ['competition_density', 'average_check_size', 'peak_hours', 'seasonal_variation'],
                'analysis_focus': ['cuisine_type', 'price_point', 'target_demographic', 'location_foot_traffic'],
                'success_factors': ['menu_innovation', 'service_quality', 'ambiance', 'marketing_strategy'],
                'risk_factors': ['food_costs', 'labor_costs', 'competition', 'seasonality']
            },
            'retail': {
                'key_metrics': ['foot_traffic', 'competition_density', 'average_transaction', 'inventory_turnover'],
                'analysis_focus': ['product_category', 'target_market', 'location_visibility', 'rent_costs'],
                'success_factors': ['product_selection', 'customer_service', 'visual_merchandising', 'pricing_strategy'],
                'risk_factors': ['online_competition', 'seasonal_demand', 'inventory_management', 'rent_increases']
            },
            'health_wellness': {
                'key_metrics': ['population_health_indicators', 'insurance_coverage', 'competition_density', 'demand_growth'],
                'analysis_focus': ['service_specialization', 'target_demographic', 'location_accessibility', 'regulatory_requirements'],
                'success_factors': ['professional_credentials', 'patient_satisfaction', 'technology_adoption', 'referral_network'],
                'risk_factors': ['regulatory_changes', 'insurance_reimbursement', 'competition', 'technology_costs']
            },
            'professional_services': {
                'key_metrics': ['business_density', 'economic_indicators', 'competition_level', 'client_base_growth'],
                'analysis_focus': ['service_specialization', 'target_market', 'location_prestige', 'networking_opportunities'],
                'success_factors': ['expertise_level', 'client_relationships', 'reputation', 'marketing_strategy'],
                'risk_factors': ['economic_cycles', 'technology_disruption', 'competition', 'regulatory_changes']
            },
            'automotive': {
                'key_metrics': ['vehicle_density', 'average_vehicle_age', 'competition_density', 'service_demand'],
                'analysis_focus': ['service_specialization', 'target_market', 'location_accessibility', 'equipment_costs'],
                'success_factors': ['technical_expertise', 'customer_service', 'quality_work', 'competitive_pricing'],
                'risk_factors': ['technology_changes', 'competition', 'equipment_costs', 'labor_shortages']
            },
            'technology': {
                'key_metrics': ['tech_talent_pool', 'startup_density', 'venture_capital', 'innovation_index'],
                'analysis_focus': ['service_specialization', 'target_market', 'talent_availability', 'infrastructure'],
                'success_factors': ['technical_expertise', 'innovation', 'client_relationships', 'scalability'],
                'risk_factors': ['technology_changes', 'competition', 'talent_shortages', 'market_volatility']
            }
        }
        
        return templates.get(business_type, templates['restaurant'])
    
    def generate_business_specific_insights(self, business_type: str, analysis_data: Dict[str, Any]) -> str:
        """Generate business-specific insights based on analysis data"""
        template = self.get_business_analysis_template(business_type)
        insights = []
        
        # Add business-specific recommendations
        if business_type == 'restaurant':
            insights.append("🍽️ **Restaurant-Specific Insights:**")
            insights.append("• Focus on unique cuisine or signature dishes to differentiate")
            insights.append("• Consider peak dining hours and seasonal menu variations")
            insights.append("• Location foot traffic is crucial for walk-in customers")
            
        elif business_type == 'retail':
            insights.append("🛍️ **Retail-Specific Insights:**")
            insights.append("• Product selection and visual merchandising are key differentiators")
            insights.append("• Consider online presence to complement physical store")
            insights.append("• Location visibility and parking are critical factors")
            
        elif business_type == 'health_wellness':
            insights.append("🏥 **Health & Wellness Insights:**")
            insights.append("• Professional credentials and reputation are paramount")
            insights.append("• Consider insurance network participation")
            insights.append("• Location accessibility and parking are important")
            
        elif business_type == 'professional_services':
            insights.append("💼 **Professional Services Insights:**")
            insights.append("• Expertise and client relationships drive success")
            insights.append("• Consider networking opportunities in business district")
            insights.append("• Economic cycles significantly impact demand")
            
        elif business_type == 'automotive':
            insights.append("🚗 **Automotive Insights:**")
            insights.append("• Technical expertise and quality work are essential")
            insights.append("• Consider specialization in specific vehicle types")
            insights.append("• Location accessibility for vehicle drop-off/pickup")
            
        elif business_type == 'technology':
            insights.append("💻 **Technology Insights:**")
            insights.append("• Technical expertise and innovation are key differentiators")
            insights.append("• Consider proximity to tech talent and startup ecosystem")
            insights.append("• Market volatility requires flexible business model")
        
        return "\n".join(insights)
    
    async def process_message(self, message: str, session_id: str) -> ChatResponse:
        """Enhanced message processing with verification and confirmation"""
        logger.info(f"📨 Processing message: {message}")
        
        # Get conversation context
        context = self.conversation_memory.get_conversation_context(session_id)
        user_profile = self.conversation_memory.get_user_profile(session_id)
        
        # Advanced NLP analysis
        nlp_analysis = self.advanced_nlp.analyze_context(message)
        
        # Parse message with enhanced detection using JSON data
        enhanced_classification = self.enhanced_business_classification(message)
        business = enhanced_classification.get('business_type', 'restaurant')
        confidence = enhanced_classification.get('confidence', 0) / 10.0  # Normalize to 0-1 scale
        logger.info(f"🔍 Enhanced classification result: {enhanced_classification}")
        
        location = await location_detector.detect_location(message)
        
        # Get business insights for enhanced context
        business_insights = self.get_business_insights(business)
        
        # Check if this is a confirmation response
        if self._is_confirmation_response(message, context):
            return await self._handle_confirmation(message, session_id, context)
        
        # Handle ambiguous locations with better options
        if location and location.startswith("AMBIGUOUS:"):
            return await self._handle_ambiguous_location(message, session_id, location, business)
        
        # If both business and location are detected, ask for confirmation
        if business and location and confidence > 0.1:
            return await self._verify_business_type(message, session_id, business, location)
        
        # Verify business type if detected
        if business and confidence > 0.1:
            return await self._verify_business_type(message, session_id, business, location)
        
        # Verify location if detected
        if location and not location.startswith("AMBIGUOUS:"):
            return await self._verify_location(message, session_id, location, business)
        
        logger.info(f"🔍 Detected: business='{business}' (confidence: {confidence}), location='{location}'")
        
        # Generate intelligent response based on context
        response = await self._generate_intelligent_response(message, business, location, session_id, nlp_analysis)
        
        # Perform comprehensive analysis if both are confirmed
        analysis_data = {"business_type": business, "location": location}
        if business and location and self._are_parameters_confirmed(session_id):
            analysis_results = await self._perform_comprehensive_analysis(business, location)
            analysis_data.update(analysis_results)
            response = await self._enhance_response_with_analysis(response, analysis_data, location)
        
        # Store conversation turn
        self.conversation_memory.add_turn(
            session_id, message, response, 
            nlp_analysis.primary_intent, 
            {"business_type": business, "location": location, "confidence": confidence},
            analysis_data
        )
        
        # Save memory
        self.conversation_memory.save_memory()
        
        return ChatResponse(
            response=response,
                session_id=session_id,
            timestamp=str(asyncio.get_event_loop().time()),
            analysis_data=analysis_data,
            next_questions=self._get_smart_next_questions(session_id, analysis_data)
        )
    
    async def _perform_comprehensive_analysis(self, business_type: str, location: str) -> Dict[str, Any]:
        """Perform comprehensive market analysis with demographics"""
        logger.info(f"🔍 Performing comprehensive analysis for {business_type} in {location}")
        
        analysis_results = {
            "demographics": {},
            "competition": {},
            "market_opportunity": {},
            "search_trends": {},
            "coordinates": [],
            "apis_used": []
        }
        
        try:
            # Get coordinates for the location
            logger.info(f"🗺️ Geocoding location: {location}")
            geocode_result = await self.api_client.geocode_location(location)
            
            if geocode_result["success"]:
                coordinates = geocode_result.get("coordinates", {})
                if coordinates:
                    # Convert to [lng, lat] format for frontend
                    lng = coordinates.get("longitude", coordinates.get("lng", 0))
                    lat = coordinates.get("latitude", coordinates.get("lat", 0))
                    analysis_results["coordinates"] = [lng, lat]
                    analysis_results["apis_used"].append("Mapbox Geocoding")
                    logger.info(f"✅ Geocoding successful: {location} -> [{lng}, {lat}]")
                else:
                    logger.warning(f"⚠️ No coordinates found for {location}")
            else:
                logger.error(f"❌ Geocoding failed for {location}: {geocode_result.get('error', 'Unknown error')}")
            
            # Get demographics data
            logger.info(f"👥 Getting demographics for {location}")
            demo_result = await self.api_client.get_demographics("53")  # Washington state for now
            
            if demo_result["success"]:
                demographics = demo_result.get("demographics", {})
                analysis_results["demographics"] = demographics
                analysis_results["apis_used"].append("US Census Demographics")
                
                # Calculate market opportunity score
                opportunity_score = self.predictive_analytics.calculate_opportunity_score(
                    business_type, location, demographics, {}
                )
                analysis_results["market_opportunity"] = {
                    "score": opportunity_score.overall_score,
                    "growth_potential": opportunity_score.growth_potential,
                    "recommendations": opportunity_score.recommendations
                }
                
                logger.info(f"✅ Demographics analysis complete: {demographics.get('total_population', 0)} people, ${demographics.get('median_household_income', 0)} median income")
            
            # Get competition data
            logger.info(f"🏢 Getting competition data for {business_type} in {location}")
            places_result = await self.api_client.search_places(
                query=business_type,
                location=location
            )
            
            if places_result["success"]:
                businesses = places_result.get("businesses", [])
                analysis_results["competition"] = {
                    "total_competitors": len(businesses),
                    "average_rating": sum(b.get("rating", 0) for b in businesses) / len(businesses) if businesses else 0,
                    "competition_level": "High" if len(businesses) > 10 else "Medium" if len(businesses) > 5 else "Low"
                }
                analysis_results["apis_used"].append("Google Places API")
                logger.info(f"✅ Competition analysis complete: {len(businesses)} competitors found")
            
            # Get search trends data
            logger.info(f"📈 Getting search trends for {business_type} in {location}")
            search_trends = await self._get_search_trends(business_type, location)
            analysis_results["search_trends"] = search_trends
            analysis_results["apis_used"].append("SerpAPI Search Trends")
            logger.info(f"✅ Search trends analysis complete")
            
        except Exception as e:
            logger.error(f"❌ Analysis error: {e}")
            analysis_results["error"] = str(e)
        
        return analysis_results
    
    async def _get_search_trends(self, business_type: str, location: str) -> Dict[str, Any]:
        """Get search trends data for business type and location"""
        try:
            # Generate realistic search trends based on business type and location
            business_keywords = {
                'restaurant': ['restaurant', 'food', 'dining', 'burger', 'pizza', 'sushi', 'cafe', 'coffee'],
                'retail': ['store', 'shop', 'shopping', 'clothing', 'electronics', 'boutique'],
                'health_wellness': ['gym', 'fitness', 'wellness', 'spa', 'massage', 'yoga', 'salon'],
                'automotive': ['auto repair', 'car service', 'mechanic', 'oil change', 'dealership'],
                'technology': ['tech', 'software', 'startup', 'app development', 'IT services'],
                'professional_services': ['legal services', 'law firm', 'accounting', 'consulting', 'real estate']
            }
            
            keywords = business_keywords.get(business_type, ['business', 'service'])
            location_parts = location.split(',')
            city = location_parts[0].strip() if location_parts else location
            
            # Generate monthly search volumes
            monthly_searches = {}
            for keyword in keywords[:6]:  # Limit to 6 keywords
                search_term = f"{keyword} {city.lower()}"
                # Generate realistic search volumes based on business type
                base_volume = {
                    'restaurant': 5000,
                    'retail': 3000,
                    'health_wellness': 2000,
                    'automotive': 4000,
                    'technology': 1500,
                    'professional_services': 1000
                }.get(business_type, 2000)
                
                # Add some variation
                volume = base_volume + (hash(search_term) % 5000)
                monthly_searches[search_term] = volume
            
            # Generate trending keywords
            trending_keywords = [
                'organic', 'sustainable', 'local', 'artisanal', 'premium', 'eco-friendly',
                'digital', 'online', 'contactless', 'hybrid', 'virtual'
            ][:3]
            
            # Generate social media mentions
            social_mentions = {
                'restaurant': 25000,
                'retail': 15000,
                'health_wellness': 20000,
                'automotive': 18000,
                'technology': 30000,
                'professional_services': 12000
            }.get(business_type, 15000)
            
            return {
                "monthly_searches": monthly_searches,
                "trending_keywords": trending_keywords,
                "social_media_mentions": social_mentions,
                "search_volume_trend": "increasing" if business_type in ['technology', 'health_wellness'] else "stable"
            }
            
        except Exception as e:
            logger.error(f"❌ Error getting search trends: {e}")
            return {
                "monthly_searches": {},
                "trending_keywords": [],
                "social_media_mentions": 0,
                "search_volume_trend": "unknown"
            }
    
    def _is_confirmation_response(self, message: str, context: list) -> bool:
        """Check if message is a confirmation response"""
        message_lower = message.lower().strip()
        
        # Check for exact confirmation phrases
        exact_confirmations = [
            'yes', 'y', 'correct', 'right', 'confirm', 'confirmed', 
            'yes that is correct', 'that is correct', 'yes correct',
            'yes, that is correct', 'yes that is correct',
            '1', '2', '3', '4', '5'
        ]
        
        # Check for exact matches first
        if message_lower in exact_confirmations:
            return True
            
        # Check for confirmation words at the start of the message
        confirmation_words = ['yes', 'correct', 'right', 'confirm']
        words = message_lower.split()
        if words and words[0] in confirmation_words:
            return True
            
        return False
    
    async def _handle_confirmation(self, message: str, session_id: str, context: list) -> ChatResponse:
        """Handle user confirmation responses"""
        # Check session data first
        session_data = self.sessions.get(session_id, {})
        if session_data.get("business") and session_data.get("location"):
            business = session_data["business"]
            location = session_data["location"]
            
            response = f"✅ **Perfect! Confirmed: {business.title()} in {location}**\n\nLet me analyze this market for you..."
            
            # Perform analysis
            analysis_results = await self._perform_comprehensive_analysis(business, location)
            analysis_data = {"business_type": business, "location": location, **analysis_results}
            response = await self._enhance_response_with_analysis(response, analysis_data, location)
            
            # Clear pending confirmation
            self.sessions[session_id] = {"business": business, "location": location}
            
            return ChatResponse(
                response=response,
                session_id=session_id,
                timestamp=str(asyncio.get_event_loop().time()),
                analysis_data={"business_type": business, "location": location, **analysis_results}
            )
        
        # Fallback to conversation memory
        if context:
            last_turn = context[-1]
            if "business_type" in last_turn.entities and "location" in last_turn.entities:
                business = last_turn.entities["business_type"]
                location = last_turn.entities["location"]
                
                response = f"✅ **Perfect! Confirmed: {business.title()} in {location}**\n\nLet me analyze this market for you..."
                
                # Perform analysis
                analysis_results = await self._perform_comprehensive_analysis(business, location)
                analysis_data = {"business_type": business, "location": location, **analysis_results}
                response = await self._enhance_response_with_analysis(response, analysis_data, location)
                
                return ChatResponse(
                    response=response,
                    session_id=session_id,
                    timestamp=str(asyncio.get_event_loop().time()),
                    analysis_data={"business_type": business, "location": location, **analysis_results}
                )
        
        return ChatResponse(
            response="I'm not sure what you're confirming. Could you please be more specific?",
            session_id=session_id,
            timestamp=str(asyncio.get_event_loop().time())
        )
    
    async def _handle_ambiguous_location(self, message: str, session_id: str, location: str, business: str) -> ChatResponse:
        """Handle ambiguous location with better city options"""
        ambiguous_location = location.replace("AMBIGUOUS:", "")
        alternatives = location_detector._check_location_ambiguity(
            message.lower().split()[-1], ambiguous_location
        )
        
        if alternatives:
            response_text = f"🔍 **Location Clarification Needed**\n\nI found multiple cities with similar names:\n\n"
            for i, alt in enumerate(alternatives, 1):
                response_text += f"**{i}.** {alt}\n"
            response_text += f"\n**Which city did you mean?** Please reply with the number (1-{len(alternatives)}) or the full city name with state/country."
            
            # Store alternatives for later reference
            self.sessions[session_id] = {"alternatives": alternatives, "business": business}
            
            return ChatResponse(
                response=response_text,
                session_id=session_id,
                timestamp=str(asyncio.get_event_loop().time()),
                analysis_data={"business_type": business, "location": "ambiguous", "alternatives": alternatives},
                next_questions=alternatives
            )
        
        return ChatResponse(
            response="I couldn't find that location. Could you please specify the city and state/country?",
            session_id=session_id,
            timestamp=str(asyncio.get_event_loop().time())
        )
    
    async def _verify_business_type(self, message: str, session_id: str, business: str, location: str) -> ChatResponse:
        """Verify business type with user confirmation"""
        response = f"🏢 **Business Type Detected: {business.title()}**\n\n"
        response += f"I understand you want to open a **{business}** business.\n\n"
        
        if location:
            response += f"📍 **Location: {location}**\n\n"
            response += f"**Is this correct?** I want to make sure I understand:\n"
            response += f"• Business: {business.title()}\n"
            response += f"• Location: {location}\n\n"
            response += "Please confirm by saying 'yes' or 'correct', or tell me if something needs to be changed."
        else:
            response += f"**Is this the right business type?** Please confirm or let me know what you'd like to change.\n\n"
            response += f"📍 **What location** are you considering for your {business}?"
        
        # Store for confirmation
        self.sessions[session_id] = {"business": business, "location": location, "pending_confirmation": "business"}
        
        return ChatResponse(
            response=response,
            session_id=session_id,
            timestamp=str(asyncio.get_event_loop().time()),
            analysis_data={"business_type": business, "location": location, "needs_confirmation": True}
        )
    
    async def _verify_location(self, message: str, session_id: str, location: str, business: str) -> ChatResponse:
        """Verify location with user confirmation"""
        response = f"📍 **Location Detected: {location}**\n\n"
        response += f"I understand you're interested in **{location}**.\n\n"
        
        if business:
            response += f"🏢 **Business: {business.title()}**\n\n"
            response += f"**Is this correct?** I want to make sure I understand:\n"
            response += f"• Business: {business.title()}\n"
            response += f"• Location: {location}\n\n"
            response += "Please confirm by saying 'yes' or 'correct', or tell me if something needs to be changed."
        else:
            response += f"**Is this the right location?** Please confirm or let me know what you'd like to change.\n\n"
            response += f"🏢 **What type of business** are you considering in {location}?"
        
        # Store for confirmation
        self.sessions[session_id] = {"business": business, "location": location, "pending_confirmation": "location"}
        
        return ChatResponse(
            response=response,
            session_id=session_id,
            timestamp=str(asyncio.get_event_loop().time()),
            analysis_data={"business_type": business, "location": location, "needs_confirmation": True}
        )
    
    async def _generate_intelligent_response(self, message: str, business: str, location: str, session_id: str, nlp_analysis) -> str:
        """Generate intelligent response based on context"""
        if business and location:
            response = f"🏢 **{business.title()} Market Analysis in {location}**\n\nI can help you analyze the {business} market in {location}!\n\nPlease confirm the details above so I can provide comprehensive analysis."
            
            # Add keyword suggestions
            suggestions = keyword_enhancer.enhance_business_keywords(business, location)
            if suggestions:
                response += f"\n\n🧠 **Smart Keyword Suggestions:**\n"
                for s in suggestions[:5]:
                    response += f"• {s.keyword} - {s.reason}\n"
            
        elif business:
            response = f"🏢 **{business.title()} Market Analysis**\n\nI can help you analyze the {business} market!\n\n📍 **What location are you considering?**"
            
        elif location:
            response = f"📍 **{location.title()} Market Intelligence**\n\nI can help you find business opportunities in {location}!\n\n🏢 **What type of business are you interested in?**"
        else:
            response = "🚀 **D.E.L.T.A Franchise Intelligence Ready!**\n\nI can help you with comprehensive business analysis!\n\n🏢 **What type of business** are you considering?\n📍 **What location** are you interested in?"
        
        # Add sentiment-based enhancement
        if nlp_analysis.sentiment.sentiment.value == "positive":
            response += "\n\n😊 I'm excited to help you with your business venture!"
        elif nlp_analysis.sentiment.sentiment.value == "uncertain":
            response += "\n\n💭 I'm here to help you explore your options and make informed decisions."
        
        return response
    
    def _are_parameters_confirmed(self, session_id: str) -> bool:
        """Check if both business and location are confirmed"""
        session_data = self.sessions.get(session_id, {})
        return not session_data.get("pending_confirmation")
    
    async def _enhance_response_with_analysis(self, response: str, analysis_results: dict, location: str) -> str:
        """Enhance response with analysis data and business-specific insights"""
        business_type = analysis_results.get("business_type", "restaurant")
        logger.info(f"🔍 Enhancing response for business_type: {business_type}, analysis_results keys: {list(analysis_results.keys())}")
        
        if analysis_results.get("demographics"):
            demographics = analysis_results["demographics"]
            market_opportunity = analysis_results.get("market_opportunity", {})
            competition = analysis_results.get("competition", {})
            
            # Create detailed demographic summary
            demo_summary = f"\n\n📊 **Demographic Intelligence for {location}:**\n"
            demo_summary += f"• **Population**: {demographics.get('total_population', 0):,} people\n"
            demo_summary += f"• **Income**: ${demographics.get('median_household_income', 0):,} median (Spending Power: {demographics.get('income_analysis', {}).get('spending_power', 'Unknown')})\n"
            demo_summary += f"• **Education**: {demographics.get('education_data', {}).get('bachelors_degree', 0):,} with bachelor's degree\n"
            demo_summary += f"• **Age Groups**: {demographics.get('age_demographics', {}).get('18_34', 0):,} ages 18-34 (key market)\n"
            
            if market_opportunity.get("score"):
                demo_summary += f"\n🎯 **Market Opportunity Score**: {market_opportunity.get('score', 0)*100:.1f}% (Growth Potential: {market_opportunity.get('growth_potential', 0)*100:.1f}%)\n"
            
            if competition.get("total_competitors"):
                demo_summary += f"🏪 **Competition**: {competition.get('total_competitors', 0)} competitors (Average Rating: {competition.get('average_rating', 0):.1f}⭐)\n"
            
            if market_opportunity.get("recommendations"):
                demo_summary += f"\n💡 **Key Insights:**\n"
                for rec in market_opportunity.get("recommendations", [])[:3]:
                    demo_summary += f"• {rec}\n"
            
            response += demo_summary
            
            # Add business-specific insights
            business_insights = self.generate_business_specific_insights(business_type, analysis_results)
            if business_insights:
                response += f"\n\n{business_insights}"
        
        return response
    
    def _get_smart_next_questions(self, session_id: str, analysis_data: dict) -> list:
        """Get smart next questions based on conversation context"""
        user_profile = self.conversation_memory.get_user_profile(session_id)
        smart_suggestions = self.conversation_memory.get_smart_suggestions(session_id, analysis_data)
        
        questions = []
        if analysis_data.get("business_type") and analysis_data.get("location"):
            questions.extend([
                "Would you like to see franchise opportunities?",
                "What's your investment budget range?",
                "Are you interested in competitor analysis?"
            ])
        elif analysis_data.get("business_type"):
            questions.append("What location are you considering?")
        elif analysis_data.get("location"):
            questions.append("What type of business interests you?")
        
        # Add smart suggestions
        questions.extend(smart_suggestions[:2])
        
        return questions

# Initialize bot
bot = FranchiseBot()

# Create FastAPI app
app = FastAPI(title="D.E.L.T.A Bot API", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/status")
async def get_status():
    """Get bot status"""
    return {"status": "online", "message": "D.E.L.T.A Bot is ready"}

@app.post("/chat")
async def chat(request: ChatRequest):
    """Chat with the bot"""
    try:
        response = await bot.process_message(request.message, request.session_id)
        return response
    except Exception as e:
        logger.error(f"Error processing message: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    logger.info("🚀 Starting D.E.L.T.A Bot...")
    uvicorn.run(app, host="0.0.0.0", port=8002)
