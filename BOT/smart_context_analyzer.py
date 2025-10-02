"""
Smart Context Analyzer - Advanced NLP for Business Intelligence
Provides intelligent context understanding, intent analysis, and smart responses
"""

import re
import logging
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass
from enum import Enum
import json

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class IntentType(Enum):
    """Types of user intents"""
    BUSINESS_ANALYSIS = "business_analysis"
    LOCATION_QUESTION = "location_question"
    BUSINESS_TYPE_QUESTION = "business_type_question"
    FRANCHISE_INQUIRY = "franchise_inquiry"
    COMPETITION_ANALYSIS = "competition_analysis"
    MARKET_RESEARCH = "market_research"
    INVESTMENT_ANALYSIS = "investment_analysis"
    GENERAL_QUESTION = "general_question"
    HELP_REQUEST = "help_request"
    GREETING = "greeting"

@dataclass
class ContextAnalysis:
    """Result of context analysis"""
    intent: IntentType
    confidence: float
    entities: Dict[str, Any]
    suggestions: List[str]
    follow_up_questions: List[str]
    requires_clarification: bool
    smart_response: Optional[str] = None

class SmartContextAnalyzer:
    """Advanced context analyzer with intelligent understanding"""
    
    def __init__(self):
        """Initialize the smart context analyzer"""
        self.intent_patterns = self._build_intent_patterns()
        self.entity_extractors = self._build_entity_extractors()
        self.response_templates = self._build_response_templates()
        logger.info("🧠 Smart context analyzer initialized")
    
    def _build_intent_patterns(self) -> Dict[IntentType, List[str]]:
        """Build intent recognition patterns"""
        return {
            IntentType.BUSINESS_ANALYSIS: [
                r"i want to open",
                r"i want to start",
                r"i'm thinking about opening",
                r"planning to open",
                r"considering opening",
                r"looking to start",
                r"want to launch",
                r"interested in opening"
            ],
            IntentType.LOCATION_QUESTION: [
                r"where should i",
                r"where can i",
                r"which location",
                r"best place to",
                r"where to open",
                r"where to start",
                r"location for",
                r"place for"
            ],
            IntentType.BUSINESS_TYPE_QUESTION: [
                r"what type of business",
                r"what kind of business",
                r"which business",
                r"business type",
                r"what should i open",
                r"what business",
                r"business ideas"
            ],
            IntentType.FRANCHISE_INQUIRY: [
                r"franchise",
                r"franchise opportunities",
                r"franchise options",
                r"franchise costs",
                r"franchise investment",
                r"buy a franchise",
                r"franchise for sale"
            ],
            IntentType.COMPETITION_ANALYSIS: [
                r"competition",
                r"competitors",
                r"market saturation",
                r"how many",
                r"existing businesses",
                r"market analysis",
                r"competitive landscape"
            ],
            IntentType.MARKET_RESEARCH: [
                r"market research",
                r"market size",
                r"demographics",
                r"target market",
                r"customer base",
                r"market demand",
                r"market trends"
            ],
            IntentType.INVESTMENT_ANALYSIS: [
                r"investment",
                r"cost",
                r"budget",
                r"funding",
                r"capital",
                r"financial",
                r"profit",
                r"revenue",
                r"roi"
            ],
            IntentType.HELP_REQUEST: [
                r"help",
                r"assist",
                r"support",
                r"guide",
                r"advice",
                r"recommendations",
                r"suggestions"
            ],
            IntentType.GREETING: [
                r"hello",
                r"hi",
                r"hey",
                r"good morning",
                r"good afternoon",
                r"good evening",
                r"greetings"
            ]
        }
    
    def _build_entity_extractors(self) -> Dict[str, List[str]]:
        """Build entity extraction patterns"""
        return {
            "business_indicators": [
                "open", "start", "launch", "begin", "establish", "create", "build", "operate",
                "run", "manage", "own", "invest in", "franchise", "buy"
            ],
            "location_indicators": [
                "in", "at", "near", "around", "close to", "within", "located", "based in",
                "situated", "positioned", "where", "place", "location", "area", "region"
            ],
            "question_words": [
                "what", "where", "when", "why", "how", "which", "who", "should", "could",
                "would", "can", "may", "might", "is", "are", "do", "does", "will"
            ],
            "uncertainty_words": [
                "maybe", "perhaps", "possibly", "potentially", "considering", "thinking",
                "interested", "curious", "wondering", "unsure", "not sure", "help me"
            ],
            "emphasis_words": [
                "really", "very", "extremely", "definitely", "certainly", "absolutely",
                "definitely", "surely", "obviously", "clearly", "particularly", "especially"
            ]
        }
    
    def _build_response_templates(self) -> Dict[IntentType, str]:
        """Build smart response templates"""
        return {
            IntentType.BUSINESS_ANALYSIS: "I'll analyze the {business_type} market in {location} for you. Let me gather real-time data on competition, demographics, and franchise opportunities.",
            IntentType.LOCATION_QUESTION: "Great question about location! Let me analyze the best areas for {business_type} businesses and provide data-driven recommendations.",
            IntentType.BUSINESS_TYPE_QUESTION: "I'd be happy to help you choose the right business type! Based on {location}, let me suggest some promising opportunities.",
            IntentType.FRANCHISE_INQUIRY: "Excellent! Franchising can be a great path to entrepreneurship. Let me find the best franchise opportunities for {business_type} in {location}.",
            IntentType.COMPETITION_ANALYSIS: "Competitive analysis is crucial for success! Let me analyze the competitive landscape for {business_type} in {location}.",
            IntentType.MARKET_RESEARCH: "Market research is the foundation of any successful business. Let me provide comprehensive market data for {business_type} in {location}.",
            IntentType.INVESTMENT_ANALYSIS: "Smart to analyze the financial aspects! Let me provide investment requirements and financial projections for {business_type} in {location}.",
            IntentType.HELP_REQUEST: "I'm here to help! Let me guide you through the business analysis process step by step.",
            IntentType.GREETING: "Welcome to D.E.L.T.A Franchise Intelligence! I'm here to help you make data-driven business decisions. What would you like to explore?"
        }
    
    def analyze_context(self, message: str, detected_business: Optional[str] = None, 
                       detected_location: Optional[str] = None) -> ContextAnalysis:
        """
        Perform comprehensive context analysis
        
        Args:
            message: User message
            detected_business: Previously detected business type
            detected_location: Previously detected location
            
        Returns:
            ContextAnalysis object with intent and suggestions
        """
        message_lower = message.lower().strip()
        
        # Detect primary intent
        intent, confidence = self._detect_intent(message_lower)
        
        # Extract entities and context
        entities = self._extract_entities(message_lower, detected_business, detected_location)
        
        # Generate smart suggestions
        suggestions = self._generate_suggestions(intent, entities, message_lower)
        
        # Generate follow-up questions
        follow_up_questions = self._generate_follow_up_questions(intent, entities)
        
        # Determine if clarification is needed
        requires_clarification = self._needs_clarification(intent, entities)
        
        # Generate smart response
        smart_response = self._generate_smart_response(intent, entities, requires_clarification)
        
        logger.info(f"🧠 Context analysis: intent={intent.value}, confidence={confidence:.2f}, entities={len(entities)}")
        
        return ContextAnalysis(
            intent=intent,
            confidence=confidence,
            entities=entities,
            suggestions=suggestions,
            follow_up_questions=follow_up_questions,
            requires_clarification=requires_clarification,
            smart_response=smart_response
        )
    
    def _detect_intent(self, message: str) -> Tuple[IntentType, float]:
        """Detect user intent with confidence scoring"""
        intent_scores = {}
        
        for intent_type, patterns in self.intent_patterns.items():
            score = 0
            for pattern in patterns:
                if re.search(pattern, message, re.IGNORECASE):
                    score += 1
            
            if score > 0:
                intent_scores[intent_type] = score / len(patterns)
        
        if intent_scores:
            best_intent = max(intent_scores.items(), key=lambda x: x[1])
            return best_intent[0], best_intent[1]
        
        return IntentType.GENERAL_QUESTION, 0.5
    
    def _extract_entities(self, message: str, detected_business: Optional[str], 
                         detected_location: Optional[str]) -> Dict[str, Any]:
        """Extract entities and context from message"""
        entities = {
            "business_type": detected_business,
            "location": detected_location,
            "has_question": "?" in message,
            "uncertainty_level": 0,
            "emphasis_level": 0,
            "specificity_level": 0,
            "keywords": [],
            "sentiment": "neutral"
        }
        
        # Extract keywords
        words = re.findall(r'\b\w+\b', message)
        entities["keywords"] = words
        
        # Calculate uncertainty level
        uncertainty_count = sum(1 for word in self.entity_extractors["uncertainty_words"] if word in message)
        entities["uncertainty_level"] = min(uncertainty_count / 3, 1.0)
        
        # Calculate emphasis level
        emphasis_count = sum(1 for word in self.entity_extractors["emphasis_words"] if word in message)
        entities["emphasis_level"] = min(emphasis_count / 3, 1.0)
        
        # Calculate specificity level
        business_indicators = sum(1 for word in self.entity_extractors["business_indicators"] if word in message)
        location_indicators = sum(1 for word in self.entity_extractors["location_indicators"] if word in message)
        question_words = sum(1 for word in self.entity_extractors["question_words"] if word in message)
        
        entities["specificity_level"] = min((business_indicators + location_indicators + question_words) / 5, 1.0)
        
        # Determine sentiment
        positive_words = ["good", "great", "excellent", "amazing", "wonderful", "fantastic", "perfect"]
        negative_words = ["bad", "terrible", "awful", "horrible", "worst", "difficult", "hard"]
        
        positive_count = sum(1 for word in positive_words if word in message)
        negative_count = sum(1 for word in negative_words if word in message)
        
        if positive_count > negative_count:
            entities["sentiment"] = "positive"
        elif negative_count > positive_count:
            entities["sentiment"] = "negative"
        
        return entities
    
    def _generate_suggestions(self, intent: IntentType, entities: Dict[str, Any], 
                            message: str) -> List[str]:
        """Generate intelligent suggestions based on context"""
        suggestions = []
        
        if intent == IntentType.BUSINESS_ANALYSIS:
            if not entities["business_type"]:
                suggestions.append("Specify the type of business you're interested in")
            if not entities["location"]:
                suggestions.append("Provide a specific location or area")
            suggestions.extend([
                "Consider analyzing multiple locations for comparison",
                "Research franchise opportunities in your area",
                "Analyze competitor density and market saturation"
            ])
        
        elif intent == IntentType.LOCATION_QUESTION:
            suggestions.extend([
                "Consider factors like demographics, competition, and accessibility",
                "Analyze foot traffic and visibility in potential locations",
                "Research local zoning laws and regulations",
                "Compare multiple locations using our territory analysis"
            ])
        
        elif intent == IntentType.BUSINESS_TYPE_QUESTION:
            suggestions.extend([
                "Consider your interests, skills, and investment capacity",
                "Research market demand and growth potential",
                "Analyze competition in your target area",
                "Explore franchise vs. independent business options"
            ])
        
        elif intent == IntentType.FRANCHISE_INQUIRY:
            suggestions.extend([
                "Compare franchise costs and requirements",
                "Research franchise success rates and support",
                "Analyze territory availability",
                "Consider your financial capacity and goals"
            ])
        
        return suggestions[:3]  # Limit to top 3 suggestions
    
    def _generate_follow_up_questions(self, intent: IntentType, entities: Dict[str, Any]) -> List[str]:
        """Generate intelligent follow-up questions"""
        questions = []
        
        if intent == IntentType.BUSINESS_ANALYSIS:
            if not entities["business_type"]:
                questions.append("What type of business are you considering?")
            if not entities["location"]:
                questions.append("Which location or area interests you?")
            questions.extend([
                "Would you like to see franchise opportunities?",
                "Should I analyze the competitive landscape?",
                "Do you want demographic data for the area?"
            ])
        
        elif intent == IntentType.LOCATION_QUESTION:
            questions.extend([
                "What type of business are you planning?",
                "What's your target customer demographic?",
                "Do you have a preferred area or radius?",
                "Are you looking for high-traffic or low-competition areas?"
            ])
        
        elif intent == IntentType.BUSINESS_TYPE_QUESTION:
            questions.extend([
                "What location are you considering?",
                "What's your investment budget range?",
                "Do you have any specific interests or skills?",
                "Are you open to franchise opportunities?"
            ])
        
        return questions[:3]  # Limit to top 3 questions
    
    def _needs_clarification(self, intent: IntentType, entities: Dict[str, Any]) -> bool:
        """Determine if clarification is needed"""
        if intent in [IntentType.BUSINESS_ANALYSIS, IntentType.LOCATION_QUESTION]:
            return not entities["business_type"] or not entities["location"]
        
        if intent == IntentType.BUSINESS_TYPE_QUESTION:
            return not entities["location"]
        
        return False
    
    def _generate_smart_response(self, intent: IntentType, entities: Dict[str, Any], 
                               requires_clarification: bool) -> Optional[str]:
        """Generate intelligent response based on context"""
        if requires_clarification:
            return None  # Let the main bot handle clarification
        
        template = self.response_templates.get(intent)
        if not template:
            return None
        
        # Replace placeholders with actual values
        business_type = entities.get("business_type", "your business")
        location = entities.get("location", "your target area")
        
        response = template.format(business_type=business_type, location=location)
        
        # Add context-specific enhancements
        if entities["uncertainty_level"] > 0.3:
            response += " I understand you're exploring options - I'll provide comprehensive data to help you decide."
        
        if entities["emphasis_level"] > 0.3:
            response += " I'll make sure to give you detailed, actionable insights."
        
        return response

# Global instance
smart_context_analyzer = SmartContextAnalyzer()
