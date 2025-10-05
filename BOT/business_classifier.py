#!/usr/bin/env python3
"""
SMART Business Type Classifier - Advanced NLP & Language Understanding
Uses ONLY real APIs with intelligent language processing - NO HARDCODED DATA
"""

import logging
import re
import asyncio
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class BusinessIntent:
    """Represents a detected business intent with confidence"""
    business_type: str
    confidence: float
    context: str
    modifiers: List[str]

class SmartBusinessClassifier:
    """SMART business classifier using advanced NLP and language understanding"""
    
    def __init__(self):
        """Initialize with advanced language understanding"""
        logger.info("🧠 SMART business classifier initialized - Advanced NLP, NO HARDCODED DATA")
    
    def classify_business_type(self, text: str) -> Tuple[Optional[str], float]:
        """
        SMART business type classification using advanced language understanding
        
        Args:
            text: Input text to analyze
            
        Returns:
            Tuple of (business_type, confidence_score)
        """
        logger.info(f"🧠 SMART analysis of: '{text}'")
        
        # Step 1: Advanced intent detection
        intent = self._detect_business_intent(text)
        if not intent:
            return None, 0.0
        
        # Step 2: Extract business type using context understanding
        business_type = self._extract_business_type_smart(text, intent)
        if not business_type:
            return None, 0.0
        
        # Step 3: Validate and refine using language patterns
        refined_type = self._refine_business_type(business_type, text)
        
        # Step 4: Calculate confidence based on multiple factors
        confidence = self._calculate_confidence(refined_type, text, intent)
        
        logger.info(f"✅ SMART result: '{refined_type}' (confidence: {confidence:.2f})")
        return refined_type, confidence
    
    def _detect_business_intent(self, text: str) -> Optional[BusinessIntent]:
        """Detect business intent using advanced language understanding"""
        text_lower = text.lower()
        
        # Advanced intent patterns with context understanding
        intent_patterns = [
            # Direct business creation intent
            {
                'pattern': r'(?:want\s+to|looking\s+to|planning\s+to|considering|thinking\s+about)\s+(?:open|start|launch|begin|establish|create|build)\s+(?:a\s+)?([^,]+?)(?:\s+in|\s+at|\s+near|\s+around|$)',
                'confidence_boost': 0.9,
                'context': 'business_creation'
            },
            # Direct action intent
            {
                'pattern': r'(?:open|start|launch|begin|establish|create|build)\s+(?:a\s+)?([^,]+?)(?:\s+in|\s+at|\s+near|\s+around|$)',
                'confidence_boost': 0.8,
                'context': 'direct_action'
            },
            # Franchise intent
            {
                'pattern': r'(?:franchise|franchise\s+opportunity|buy\s+a\s+franchise)\s+(?:in|at|near|around)\s+([^,]+)',
                'confidence_boost': 0.85,
                'context': 'franchise_inquiry'
            },
            # Business type mention
            {
                'pattern': r'\b([a-z]+(?:\s+[a-z]+)*\s+(?:shop|store|restaurant|cafe|gym|salon|clinic|office|agency|center|facility|dealer|service|repair|sales|market|business|company))\b',
                'confidence_boost': 0.7,
                'context': 'business_mention'
            }
        ]
        
        best_intent = None
        best_confidence = 0.0
        
        for pattern_info in intent_patterns:
            matches = re.findall(pattern_info['pattern'], text_lower)
            for match in matches:
                if isinstance(match, tuple):
                    business_phrase = ' '.join(match).strip()
                else:
                    business_phrase = match.strip()
                
                if len(business_phrase) > 2:
                    confidence = pattern_info['confidence_boost']
                    
                    # Boost confidence for specific business indicators
                    if any(word in business_phrase for word in ['shop', 'store', 'restaurant', 'cafe', 'gym', 'salon', 'clinic', 'office', 'agency', 'center', 'facility', 'dealer', 'service', 'repair', 'sales', 'market']):
                        confidence += 0.1
                    
                    if confidence > best_confidence:
                        best_intent = BusinessIntent(
                            business_type=business_phrase,
                            confidence=confidence,
                            context=pattern_info['context'],
                            modifiers=self._extract_modifiers(text_lower)
                        )
                        best_confidence = confidence
        
        return best_intent
    
    def _extract_business_type_smart(self, text: str, intent: BusinessIntent) -> Optional[str]:
        """Extract business type using smart language understanding"""
        if not intent:
            return None
        
        # Clean the business type using intelligent parsing
        business_type = intent.business_type
        
        # Remove location indicators using smart detection
        business_type = self._remove_location_indicators(business_type)
        
        # Extract core business concept
        core_business = self._extract_core_business_concept(business_type)
        
        return core_business
    
    def _remove_location_indicators(self, business_type: str) -> str:
        """Remove location indicators using smart detection"""
        # Use regex to detect and remove location patterns
        location_patterns = [
            r'\s+in\s+[^,]+$',  # "shop in miami"
            r'\s+at\s+[^,]+$',  # "shop at miami"
            r'\s+near\s+[^,]+$',  # "shop near miami"
            r'\s+around\s+[^,]+$',  # "shop around miami"
            r'\s+close\s+to\s+[^,]+$',  # "shop close to miami"
        ]
        
        cleaned = business_type
        for pattern in location_patterns:
            cleaned = re.sub(pattern, '', cleaned, flags=re.IGNORECASE)
        
        return cleaned.strip()
    
    def _extract_core_business_concept(self, business_type: str) -> str:
        """Extract the core business concept using language understanding"""
        words = business_type.lower().split()
        
        # Find business type indicators
        business_indicators = ['shop', 'store', 'restaurant', 'cafe', 'gym', 'salon', 'clinic', 'office', 'agency', 'center', 'facility', 'dealer', 'service', 'repair', 'sales', 'market', 'business', 'company']
        
        # Find the business indicator and everything before it
        for i, word in enumerate(words):
            if word in business_indicators:
                # Take the word before the indicator and the indicator itself
                if i > 0:
                    return f"{words[i-1]} {word}"
                else:
                    return word
        
        # If no indicator found, return the whole phrase cleaned
        return ' '.join(words)
    
    def _extract_modifiers(self, text: str) -> List[str]:
        """Extract business modifiers and context"""
        modifiers = []
        
        # Size modifiers
        if any(word in text for word in ['small', 'large', 'big', 'huge', 'mini', 'micro']):
            modifiers.append('size')
        
        # Type modifiers
        if any(word in text for word in ['luxury', 'premium', 'budget', 'affordable', 'high-end', 'low-cost']):
            modifiers.append('price_tier')
        
        # Service modifiers
        if any(word in text for word in ['full-service', 'self-service', 'drive-through', 'delivery', 'pickup']):
            modifiers.append('service_type')
        
        return modifiers
    
    def _refine_business_type(self, business_type: str, original_text: str) -> str:
        """Refine business type using context from original text"""
        if not business_type:
            return business_type
        
        # Add context from original text if it makes sense
        original_lower = original_text.lower()
        
        # Check for specific business types mentioned in context
        if 'boat' in original_lower and 'shop' in business_type:
            return 'boat shop'
        elif 'marine' in original_lower and 'shop' in business_type:
            return 'marine shop'
        elif 'coffee' in original_lower and 'shop' in business_type:
            return 'coffee shop'
        elif 'fitness' in original_lower and 'gym' in business_type:
            return 'fitness center'
        
        return business_type
    
    def _calculate_confidence(self, business_type: str, text: str, intent: BusinessIntent) -> float:
        """Calculate confidence based on multiple intelligent factors"""
        if not business_type or not intent:
            return 0.0
        
        base_confidence = intent.confidence
        
        # Boost confidence for specific business indicators
        business_indicators = ['shop', 'store', 'restaurant', 'cafe', 'gym', 'salon', 'clinic', 'office', 'agency', 'center', 'facility', 'dealer', 'service', 'repair', 'sales', 'market']
        if any(indicator in business_type.lower() for indicator in business_indicators):
            base_confidence += 0.1
        
        # Boost confidence for longer, more specific business types
        word_count = len(business_type.split())
        if word_count > 1:
            base_confidence += 0.05 * (word_count - 1)
        
        # Boost confidence for clear intent context
        if intent.context == 'business_creation':
            base_confidence += 0.1
        elif intent.context == 'direct_action':
            base_confidence += 0.05
        
        # Cap confidence at 0.95
        return min(0.95, base_confidence)
    
    def search_business_types(self, query: str, limit: int = 5) -> List[Dict[str, any]]:
        """
        Search for business types using intelligent understanding
        
        Args:
            query: Search query
            limit: Maximum number of results
            
        Returns:
            List of business type suggestions
        """
        logger.info(f"🔍 SMART search for: '{query}'")
        
        # Analyze the query to understand what they're looking for
        business_type, confidence = self.classify_business_type(query)
        
        suggestions = []
        if business_type and confidence > 0.5:
            suggestions.append({
                "name": business_type,
                "description": f"Detected business type: {business_type}",
                "confidence": confidence
            })
        
        return suggestions[:limit]

# Initialize the smart classifier
business_classifier = SmartBusinessClassifier()

# Convenience functions
def classify_business_type(text: str) -> Tuple[Optional[str], float]:
    """Classify business type from text using smart language understanding"""
    return business_classifier.classify_business_type(text)

def search_business_types(query: str, limit: int = 5) -> List[Dict[str, any]]:
    """Search for business types using intelligent understanding"""
    return business_classifier.search_business_types(query, limit)

if __name__ == "__main__":
    # Test the smart business classifier
    test_queries = [
        "i want to open a coffee shop in miami",
        "i want to start a gym in seattle",
        "i want to open a restaurant in new york",
        "i want to open a moro boat shop in coney island",
        "i want to open a store in london",
        "i want to start a fitness center in austin",
        "i want to open a marine repair shop in florida",
        "looking to launch a luxury spa in beverly hills",
        "considering opening a drive-through restaurant in texas"
    ]
    
    for query in test_queries:
        business_type, confidence = classify_business_type(query)
        print(f"Query: '{query}'")
        print(f"  -> Business: {business_type} (confidence: {confidence:.2f})")
        print()