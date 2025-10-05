#!/usr/bin/env python3
"""
Smart Keyword Enhancement System
Uses intelligent language understanding to suggest related keywords for comprehensive search
"""

import logging
from typing import List, Dict, Tuple
from dataclasses import dataclass

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class KeywordSuggestion:
    """Represents a keyword suggestion with context"""
    keyword: str
    category: str
    reason: str
    confidence: float

class SmartKeywordEnhancer:
    """Smart keyword enhancement using language understanding"""
    
    def __init__(self):
        """Initialize the keyword enhancer"""
        logger.info("🧠 Smart keyword enhancer initialized")
    
    def enhance_business_keywords(self, business_type: str, location: str = None) -> List[KeywordSuggestion]:
        """
        Enhance business keywords with intelligent suggestions
        
        Args:
            business_type: The detected business type
            location: The location (optional, for location-specific suggestions)
            
        Returns:
            List of keyword suggestions
        """
        logger.info(f"🔍 Enhancing keywords for: '{business_type}' in '{location}'")
        
        suggestions = []
        business_lower = business_type.lower()
        
        # Core business type suggestions
        suggestions.extend(self._get_core_business_suggestions(business_lower))
        
        # Related service suggestions
        suggestions.extend(self._get_service_suggestions(business_lower))
        
        # Industry-specific suggestions
        suggestions.extend(self._get_industry_suggestions(business_lower))
        
        # Location-specific suggestions
        if location:
            suggestions.extend(self._get_location_suggestions(business_lower, location))
        
        # Remove duplicates and sort by confidence
        unique_suggestions = self._deduplicate_suggestions(suggestions)
        unique_suggestions.sort(key=lambda x: x.confidence, reverse=True)
        
        logger.info(f"✅ Generated {len(unique_suggestions)} keyword suggestions")
        return unique_suggestions[:8]  # Return top 8 suggestions
    
    def _get_core_business_suggestions(self, business_type: str) -> List[KeywordSuggestion]:
        """Get core business type variations"""
        suggestions = []
        
        # Boat/Marine related
        if any(word in business_type for word in ['boat', 'marine', 'yacht', 'watercraft']):
            suggestions.extend([
                KeywordSuggestion("boat sales", "core", "Direct sales focus", 0.9),
                KeywordSuggestion("boat repair", "core", "Service component", 0.9),
                KeywordSuggestion("marine equipment", "core", "Equipment sales", 0.8),
                KeywordSuggestion("boat parts", "core", "Parts and accessories", 0.8),
                KeywordSuggestion("boat rental", "core", "Rental services", 0.7),
                KeywordSuggestion("boat storage", "core", "Storage services", 0.7),
                KeywordSuggestion("boat insurance", "core", "Insurance services", 0.6),
                KeywordSuggestion("boat financing", "core", "Financial services", 0.6),
            ])
        
        # Coffee/Cafe related
        elif any(word in business_type for word in ['coffee', 'cafe', 'espresso']):
            suggestions.extend([
                KeywordSuggestion("coffee beans", "core", "Product sales", 0.9),
                KeywordSuggestion("pastries", "core", "Food offerings", 0.8),
                KeywordSuggestion("sandwiches", "core", "Food menu", 0.8),
                KeywordSuggestion("coffee equipment", "core", "Equipment sales", 0.7),
                KeywordSuggestion("coffee roasting", "core", "Production service", 0.7),
                KeywordSuggestion("catering", "core", "Event services", 0.6),
                KeywordSuggestion("coffee delivery", "core", "Delivery service", 0.6),
            ])
        
        # Restaurant related
        elif any(word in business_type for word in ['restaurant', 'dining', 'eatery']):
            suggestions.extend([
                KeywordSuggestion("takeout", "core", "Service option", 0.9),
                KeywordSuggestion("delivery", "core", "Service option", 0.9),
                KeywordSuggestion("catering", "core", "Event services", 0.8),
                KeywordSuggestion("private events", "core", "Event hosting", 0.7),
                KeywordSuggestion("bar", "core", "Beverage service", 0.7),
                KeywordSuggestion("wine", "core", "Beverage selection", 0.6),
            ])
        
        # Fitness/Gym related
        elif any(word in business_type for word in ['gym', 'fitness', 'workout']):
            suggestions.extend([
                KeywordSuggestion("personal training", "core", "Service offering", 0.9),
                KeywordSuggestion("group classes", "core", "Class offerings", 0.9),
                KeywordSuggestion("nutrition counseling", "core", "Health services", 0.8),
                KeywordSuggestion("massage therapy", "core", "Wellness services", 0.7),
                KeywordSuggestion("supplements", "core", "Product sales", 0.7),
                KeywordSuggestion("fitness equipment", "core", "Equipment sales", 0.6),
            ])
        
        return suggestions
    
    def _get_service_suggestions(self, business_type: str) -> List[KeywordSuggestion]:
        """Get related service suggestions"""
        suggestions = []
        
        # Common service additions
        service_keywords = [
            ("consultation", "service", "Expert advice", 0.7),
            ("installation", "service", "Setup services", 0.7),
            ("maintenance", "service", "Ongoing support", 0.8),
            ("warranty", "service", "Customer protection", 0.6),
            ("financing", "service", "Payment options", 0.6),
            ("delivery", "service", "Convenience service", 0.7),
            ("pickup", "service", "Convenience service", 0.6),
            ("emergency service", "service", "Urgent support", 0.5),
        ]
        
        for keyword, category, reason, confidence in service_keywords:
            suggestions.append(KeywordSuggestion(keyword, category, reason, confidence))
        
        return suggestions
    
    def _get_industry_suggestions(self, business_type: str) -> List[KeywordSuggestion]:
        """Get industry-specific suggestions"""
        suggestions = []
        
        # Boat/Marine industry
        if any(word in business_type for word in ['boat', 'marine', 'yacht']):
            suggestions.extend([
                KeywordSuggestion("fishing equipment", "industry", "Related outdoor activity", 0.6),
                KeywordSuggestion("water sports", "industry", "Recreational services", 0.6),
                KeywordSuggestion("dock services", "industry", "Marine infrastructure", 0.5),
                KeywordSuggestion("boat cleaning", "industry", "Maintenance service", 0.7),
                KeywordSuggestion("boat detailing", "industry", "Premium service", 0.6),
            ])
        
        # Food service industry
        elif any(word in business_type for word in ['coffee', 'restaurant', 'cafe', 'food']):
            suggestions.extend([
                KeywordSuggestion("organic", "industry", "Health trend", 0.6),
                KeywordSuggestion("local sourcing", "industry", "Sustainability trend", 0.5),
                KeywordSuggestion("gluten-free", "industry", "Dietary options", 0.5),
                KeywordSuggestion("vegan options", "industry", "Dietary options", 0.5),
                KeywordSuggestion("artisanal", "industry", "Quality positioning", 0.6),
            ])
        
        return suggestions
    
    def _get_location_suggestions(self, business_type: str, location: str) -> List[KeywordSuggestion]:
        """Get location-specific suggestions"""
        suggestions = []
        location_lower = location.lower()
        
        # Coastal/waterfront locations
        if any(word in location_lower for word in ['island', 'beach', 'coast', 'waterfront', 'harbor', 'marina']):
            if any(word in business_type for word in ['boat', 'marine']):
                suggestions.extend([
                    KeywordSuggestion("beach access", "location", "Coastal advantage", 0.7),
                    KeywordSuggestion("harbor services", "location", "Marine infrastructure", 0.6),
                    KeywordSuggestion("dock access", "location", "Water access", 0.6),
                ])
        
        # Urban locations
        elif any(word in location_lower for word in ['city', 'downtown', 'center', 'district']):
            suggestions.extend([
                KeywordSuggestion("walk-in traffic", "location", "Urban advantage", 0.6),
                KeywordSuggestion("office delivery", "location", "Business district", 0.5),
                KeywordSuggestion("lunch rush", "location", "Peak time service", 0.5),
            ])
        
        return suggestions
    
    def _deduplicate_suggestions(self, suggestions: List[KeywordSuggestion]) -> List[KeywordSuggestion]:
        """Remove duplicate suggestions, keeping the highest confidence"""
        seen = {}
        for suggestion in suggestions:
            key = suggestion.keyword.lower()
            if key not in seen or seen[key].confidence < suggestion.confidence:
                seen[key] = suggestion
        return list(seen.values())
    
    def generate_enhancement_message(self, business_type: str, location: str, suggestions: List[KeywordSuggestion]) -> str:
        """Generate a user-friendly message with keyword suggestions"""
        if not suggestions:
            return ""
        
        # Group suggestions by category
        categories = {}
        for suggestion in suggestions:
            if suggestion.category not in categories:
                categories[suggestion.category] = []
            categories[suggestion.category].append(suggestion)
        
        message = f"🧠 **Smart Keyword Enhancement for {business_type.title()}**\n\n"
        message += "I can expand your search with these related keywords to find more comprehensive data:\n\n"
        
        for category, category_suggestions in categories.items():
            if category == "core":
                message += "🎯 **Core Business Keywords:**\n"
            elif category == "service":
                message += "⚙️ **Service Keywords:**\n"
            elif category == "industry":
                message += "🏭 **Industry Keywords:**\n"
            elif category == "location":
                message += "📍 **Location Keywords:**\n"
            
            for suggestion in category_suggestions[:3]:  # Show top 3 per category
                message += f"• **{suggestion.keyword}** - {suggestion.reason}\n"
            message += "\n"
        
        message += "💡 **Would you like me to include these keywords in the search?**\n"
        message += "This will help find more competitors, services, and market opportunities!\n\n"
        message += "**Options:**\n"
        message += "• ✅ **Yes, use all keywords** - Comprehensive analysis\n"
        message += "• 🎯 **Yes, use core keywords only** - Focused analysis\n"
        message += "• ❌ **No, use original search** - Basic analysis"
        
        return message

# Initialize the enhancer
keyword_enhancer = SmartKeywordEnhancer()

if __name__ == "__main__":
    # Test the keyword enhancer
    test_cases = [
        ("boat shop", "coney island"),
        ("coffee shop", "miami"),
        ("restaurant", "seattle"),
        ("gym", "austin")
    ]
    
    for business_type, location in test_cases:
        print(f"\n{'='*50}")
        print(f"Testing: {business_type} in {location}")
        print('='*50)
        
        suggestions = keyword_enhancer.enhance_business_keywords(business_type, location)
        message = keyword_enhancer.generate_enhancement_message(business_type, location, suggestions)
        print(message)



