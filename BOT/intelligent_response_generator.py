"""
Intelligent Response Generator - Smart, Contextual Responses
Generates intelligent, helpful responses based on context analysis
"""

import logging
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
import random

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class ResponseContext:
    """Context for generating intelligent responses"""
    user_message: str
    detected_business: Optional[str]
    detected_location: Optional[str]
    intent: str
    entities: Dict[str, Any]
    analysis_data: Optional[Dict[str, Any]] = None

class IntelligentResponseGenerator:
    """Generates intelligent, contextual responses"""
    
    def __init__(self):
        """Initialize the response generator"""
        self.response_templates = self._build_response_templates()
        self.smart_suggestions = self._build_smart_suggestions()
        self.contextual_enhancements = self._build_contextual_enhancements()
        logger.info("🤖 Intelligent response generator initialized")
    
    def _build_response_templates(self) -> Dict[str, List[str]]:
        """Build intelligent response templates"""
        return {
            "greeting": [
                "Welcome to D.E.L.T.A Franchise Intelligence! 🚀 I'm here to help you make data-driven business decisions. What would you like to explore?",
                "Hello! I'm your AI-powered franchise intelligence assistant. Ready to analyze markets and find opportunities? Let's get started!",
                "Hi there! Welcome to the most advanced franchise intelligence platform. I can help you find the perfect business opportunity. What's your vision?"
            ],
            "business_analysis_complete": [
                "📊 **Analysis Complete!** Here's your comprehensive market intelligence for {business_type} in {location}.",
                "🎯 **Market Intelligence Ready!** I've analyzed the {business_type} market in {location} with real-time data.",
                "✅ **Analysis Complete!** Here's your data-driven insights for {business_type} opportunities in {location}."
            ],
            "needs_business_type": [
                "Great! I'd love to help you find the perfect business opportunity. What type of business are you considering?",
                "Excellent! To provide you with the most relevant analysis, what kind of business interests you?",
                "Perfect! Let me help you explore business opportunities. What type of business are you thinking about?"
            ],
            "needs_location": [
                "Good choice! Now, where are you thinking of opening your {business_type}?",
                "Excellent business idea! Which location or area are you considering for your {business_type}?",
                "Great business type! To analyze the market properly, where would you like to open your {business_type}?"
            ],
            "needs_both": [
                "I'd love to help you find the perfect business opportunity! What type of business are you considering, and where?",
                "Excellent! Let me provide you with comprehensive market analysis. What business type interests you, and which location?",
                "Perfect! I can help you find the ideal business opportunity. What kind of business are you planning, and where?"
            ],
            "location_question": [
                "Great question about location! Let me analyze the best areas for {business_type} businesses.",
                "Location is crucial for success! I'll help you find the optimal spots for your {business_type}.",
                "Smart thinking! Location can make or break a business. Let me find the best areas for {business_type}."
            ],
            "business_type_question": [
                "I'd be happy to help you choose the right business type! Based on {location}, let me suggest some promising opportunities.",
                "Great question! Let me suggest the best business types for {location} based on market data.",
                "Perfect! I'll help you find the most profitable business types in {location}."
            ],
            "franchise_inquiry": [
                "Excellent! Franchising can be a great path to entrepreneurship. Let me find the best franchise opportunities for you.",
                "Smart choice! Franchises offer proven business models. Let me show you the best options.",
                "Great thinking! Franchises provide excellent support systems. Let me find the perfect franchise for you."
            ],
            "competition_analysis": [
                "Competitive analysis is crucial for success! Let me analyze the competitive landscape for you.",
                "Smart to research competition! I'll provide detailed competitive intelligence.",
                "Excellent approach! Understanding your competition is key. Let me give you the full picture."
            ],
            "market_research": [
                "Market research is the foundation of any successful business. Let me provide comprehensive market data.",
                "Great approach! Data-driven decisions lead to success. Let me gather the market intelligence you need.",
                "Perfect! Market research is essential. Let me provide you with detailed market insights."
            ],
            "investment_analysis": [
                "Smart to analyze the financial aspects! Let me provide investment requirements and projections.",
                "Excellent thinking! Understanding costs is crucial. Let me break down the financial requirements.",
                "Great approach! Let me provide detailed financial analysis and investment requirements."
            ],
            "help_request": [
                "I'm here to help! Let me guide you through the business analysis process step by step.",
                "Absolutely! I'm your business intelligence assistant. How can I help you succeed?",
                "Of course! I'm here to make your business planning easier. What would you like to know?"
            ]
        }
    
    def _build_smart_suggestions(self) -> Dict[str, List[str]]:
        """Build intelligent suggestions based on context"""
        return {
            "high_competition": [
                "Consider a niche market or unique positioning",
                "Look for underserved areas within your target location",
                "Analyze competitor weaknesses you can capitalize on",
                "Consider franchise opportunities with strong differentiators"
            ],
            "low_competition": [
                "Verify market demand exists for your business type",
                "Research why competitors haven't entered this market",
                "Consider being a market pioneer with proper marketing",
                "Analyze demographic trends to ensure future demand"
            ],
            "high_investment": [
                "Explore financing options and SBA loans",
                "Consider franchise opportunities with financing programs",
                "Look for business partners or investors",
                "Start with a smaller location and expand gradually"
            ],
            "emerging_market": [
                "This could be a great opportunity to establish market leadership",
                "Consider early entry with strong branding",
                "Research market growth projections and timing",
                "Look for franchise opportunities in growing sectors"
            ],
            "saturated_market": [
                "Focus on differentiation and unique value propositions",
                "Consider adjacent markets or related services",
                "Look for franchise opportunities with proven success in competitive markets",
                "Analyze customer pain points competitors aren't addressing"
            ]
        }
    
    def _build_contextual_enhancements(self) -> Dict[str, str]:
        """Build contextual response enhancements"""
        return {
            "uncertainty": "I understand you're exploring options - let me provide comprehensive data to help you make an informed decision.",
            "confidence": "I can see you're serious about this opportunity - let me give you detailed, actionable insights.",
            "urgency": "I'll prioritize getting you the most current data quickly so you can move forward.",
            "research_mode": "Perfect! I'll provide thorough analysis so you can make the best decision.",
            "comparison": "Great approach! I'll help you compare multiple options side by side.",
            "beginner": "No worries! I'll explain everything clearly and guide you through the process step by step.",
            "experienced": "Excellent! I'll provide you with detailed data and advanced insights.",
            "budget_conscious": "Smart thinking! I'll focus on cost-effective opportunities and investment requirements.",
            "growth_focused": "Perfect! I'll highlight high-growth opportunities and expansion potential.",
            "lifestyle_business": "Great! I'll focus on opportunities that match your lifestyle goals."
        }
    
    def generate_intelligent_response(self, context: ResponseContext) -> str:
        """Generate intelligent, contextual response"""
        
        # Determine response type based on context
        response_type = self._determine_response_type(context)
        
        # Get base response template
        base_response = self._get_base_response(response_type, context)
        
        # Add contextual enhancements
        enhanced_response = self._add_contextual_enhancements(base_response, context)
        
        # Add smart suggestions
        final_response = self._add_smart_suggestions(enhanced_response, context)
        
        logger.info(f"🤖 Generated intelligent response type: {response_type}")
        return final_response
    
    def _determine_response_type(self, context: ResponseContext) -> str:
        """Determine the appropriate response type"""
        
        # Check if we have both business type and location
        if context.detected_business and context.detected_location:
            return "business_analysis_complete"
        
        # Check if we need business type
        if not context.detected_business and context.detected_location:
            return "needs_business_type"
        
        # Check if we need location
        if context.detected_business and not context.detected_location:
            return "needs_location"
        
        # Check if we need both
        if not context.detected_business and not context.detected_location:
            # Check if it's a greeting
            if context.intent == "greeting":
                return "greeting"
            # Check if it's asking for help
            if context.intent == "help_request":
                return "help_request"
            return "needs_both"
        
        # Intent-based responses
        intent_mapping = {
            "location_question": "location_question",
            "business_type_question": "business_type_question",
            "franchise_inquiry": "franchise_inquiry",
            "competition_analysis": "competition_analysis",
            "market_research": "market_research",
            "investment_analysis": "investment_analysis"
        }
        
        return intent_mapping.get(context.intent, "needs_both")
    
    def _get_base_response(self, response_type: str, context: ResponseContext) -> str:
        """Get base response template"""
        templates = self.response_templates.get(response_type, ["I'm here to help! What would you like to know?"])
        
        # Choose random template for variety
        template = random.choice(templates)
        
        # Replace placeholders
        business_type = context.detected_business or "your business"
        location = context.detected_location or "your target area"
        
        return template.format(business_type=business_type, location=location)
    
    def _add_contextual_enhancements(self, response: str, context: ResponseContext) -> str:
        """Add contextual enhancements to response"""
        entities = context.entities
        
        # Add uncertainty enhancement
        if entities.get("uncertainty_level", 0) > 0.3:
            enhancement = self.contextual_enhancements["uncertainty"]
            response += f"\n\n{enhancement}"
        
        # Add confidence enhancement
        elif entities.get("emphasis_level", 0) > 0.3:
            enhancement = self.contextual_enhancements["confidence"]
            response += f"\n\n{enhancement}"
        
        # Add research mode enhancement
        elif entities.get("specificity_level", 0) > 0.6:
            enhancement = self.contextual_enhancements["research_mode"]
            response += f"\n\n{enhancement}"
        
        return response
    
    def _add_smart_suggestions(self, response: str, context: ResponseContext) -> str:
        """Add smart suggestions based on analysis data"""
        if not context.analysis_data:
            return response
        
        analysis = context.analysis_data
        
        # Add suggestions based on market conditions
        suggestions = []
        
        # Competition-based suggestions
        if analysis.get("territory_analysis", {}).get("market_saturation") == "high":
            suggestions.extend(self.smart_suggestions["high_competition"][:2])
        elif analysis.get("territory_analysis", {}).get("market_saturation") == "low":
            suggestions.extend(self.smart_suggestions["low_competition"][:2])
        
        # Investment-based suggestions
        franchise_opps = analysis.get("franchise_opportunities", [])
        if franchise_opps:
            # Check if high investment franchises are present
            high_investment_keywords = ["$500,000", "$1,000,000", "high investment", "major investment"]
            if any(keyword in str(franchise_opps).lower() for keyword in high_investment_keywords):
                suggestions.extend(self.smart_suggestions["high_investment"][:2])
        
        # Add suggestions to response
        if suggestions:
            response += "\n\n💡 **Smart Suggestions:**\n"
            for i, suggestion in enumerate(suggestions, 1):
                response += f"• {suggestion}\n"
        
        return response
    
    def generate_follow_up_questions(self, context: ResponseContext) -> List[str]:
        """Generate intelligent follow-up questions"""
        questions = []
        
        if context.detected_business and context.detected_location:
            # Analysis complete - suggest next steps
            questions.extend([
                "Would you like to see detailed competitor analysis?",
                "Should I find franchise opportunities in this area?",
                "Do you want demographic data for this location?",
                "Would you like to analyze other locations for comparison?"
            ])
        elif context.detected_business and not context.detected_location:
            # Have business type, need location
            questions.extend([
                f"Which location are you considering for your {context.detected_business}?",
                f"Do you have a preferred area for your {context.detected_business}?",
                f"What radius are you willing to travel for your {context.detected_business}?"
            ])
        elif not context.detected_business and context.detected_location:
            # Have location, need business type
            questions.extend([
                f"What type of business interests you in {context.detected_location}?",
                f"Do you have any business preferences for {context.detected_location}?",
                f"Are you looking for franchise or independent business opportunities in {context.detected_location}?"
            ])
        else:
            # Need both
            questions.extend([
                "What type of business are you considering?",
                "Which location or area interests you?",
                "Do you have any specific business goals or preferences?"
            ])
        
        return questions[:3]  # Return top 3 questions

# Global instance
intelligent_response_generator = IntelligentResponseGenerator()
