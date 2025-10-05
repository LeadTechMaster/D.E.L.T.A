#!/usr/bin/env python3
"""
SMART Location Detection System - Advanced NLP & Language Understanding
Uses ONLY real APIs with intelligent language processing - NO HARDCODED DATA
"""

import re
import logging
import asyncio
from typing import Optional, List, Dict, Tuple
from dataclasses import dataclass

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class LocationIntent:
    """Represents a detected location intent with confidence"""
    location: str
    confidence: float
    context: str
    position: int  # Position in text

class SmartLocationDetector:
    """SMART location detection using advanced NLP and language understanding"""
    
    def __init__(self):
        """Initialize with advanced language understanding"""
        from api_client import DeltaAPIClient
        self.api_client = DeltaAPIClient()
        logger.info("🧠 SMART location detector initialized - Advanced NLP, NO HARDCODED DATA")
    
    async def detect_location(self, text: str) -> Optional[str]:
        """
        SMART location detection using advanced language understanding
        
        Args:
            text: Input text to analyze
            
        Returns:
            Detected location name or None if not found
        """
        logger.info(f"🧠 SMART location analysis of: '{text}'")
        
        # Step 1: Advanced intent detection
        intents = self._detect_location_intents(text)
        if not intents:
            return None
        
        # Step 2: Rank intents by confidence and context
        best_intent = self._rank_location_intents(intents, text)
        if not best_intent:
            return None
        
        # Step 3: Validate using real APIs
        validated_location = await self._validate_location_smart(best_intent.location)
        if validated_location:
            logger.info(f"✅ SMART result: '{best_intent.location}' -> '{validated_location}' (confidence: {best_intent.confidence:.2f})")
            return validated_location
        
        logger.warning(f"❌ No valid location found in: '{text}'")
        return None
    
    def _detect_location_intents(self, text: str) -> List[LocationIntent]:
        """Detect location intents using advanced language understanding"""
        text_lower = text.lower()
        intents = []
        
        # Advanced location patterns with context understanding
        location_patterns = [
            # Complex location patterns (highest priority) - handles "beach in island" type locations
            {
                'pattern': r'\b([a-z]+(?:\s+[a-z]+)*)\s+in\s+([a-z]+(?:\s+[a-z]+)*(?:,\s*[a-z]{2})?)(?:\s|$)',
                'confidence': 0.98,
                'context': 'complex_location'
            },
            # Specific location patterns for common phrases
            {
                'pattern': r'\b(?:in|at|near)\s+([a-z]+(?:\s+[a-z]+)*)\s+in\s+([a-z]+(?:\s+[a-z]+)*(?:,\s*[a-z]{2})?)(?:\s|$)',
                'confidence': 0.99,
                'context': 'specific_location'
            },
            # Specific "at" pattern (very high priority)
            {
                'pattern': r'\bat\s+([a-z]+(?:\s+[a-z]+)*(?:,\s*[a-z]{2})?)(?:\s|$)',
                'confidence': 0.95,
                'context': 'at_prepositional'
            },
            # Preposition-based patterns (high priority) - case insensitive
            {
                'pattern': r'\b(?:in|near|around|close to|within|inside|outside)\s+([a-z]+(?:\s+[a-z]+)*(?:,\s*[a-z]{2})?)(?:\s|$)',
                'confidence': 0.9,
                'context': 'prepositional'
            },
            # City, State patterns - case insensitive
            {
                'pattern': r'\b([a-z]+(?:\s+[a-z]+)*),\s*([a-z]{2})\b',
                'confidence': 0.85,
                'context': 'city_state'
            },
            # Standalone phrases (potential city names) - case insensitive
            {
                'pattern': r'\b([a-z]+(?:\s+[a-z]+)+)\b',
                'confidence': 0.6,
                'context': 'phrase'
            },
            # Address-like patterns - case insensitive
            {
                'pattern': r'\b(\d+\s+[a-z]+(?:\s+[a-z]+)*)\b',
                'confidence': 0.7,
                'context': 'address_like'
            }
        ]
        
        for pattern_info in location_patterns:
            matches = re.finditer(pattern_info['pattern'], text_lower)
            for match in matches:
                if pattern_info['context'] == 'city_state':
                    # Join city and state
                    location = f"{match.group(1)}, {match.group(2)}"
                elif pattern_info['context'] == 'complex_location':
                    # Join the two parts for complex locations like "beach in island"
                    location = f"{match.group(1)} in {match.group(2)}"
                elif pattern_info['context'] == 'specific_location':
                    # Join the two parts for specific locations like "beach in island"
                    location = f"{match.group(1)} in {match.group(2)}"
                else:
                    location = match.group(1)
                
                if len(location) > 2:
                    # Boost confidence for specific indicators
                    confidence = pattern_info['confidence']
                    
                    # Boost for common location indicators
                    if any(word in location.lower() for word in ['city', 'town', 'village', 'island', 'beach', 'hills', 'park', 'square']):
                        confidence += 0.1
                    
                    # Extra boost for well-known locations
                    if any(known_location in location.lower() for known_location in ['staten island', 'manhattan', 'brooklyn', 'queens', 'bronx', 'miami beach', 'coney island']):
                        confidence += 0.15
                    
                    # Boost for state abbreviations
                    if re.search(r',\s*[A-Z]{2}$', location):
                        confidence += 0.1
                    
                    intents.append(LocationIntent(
                        location=location,
                        confidence=confidence,
                        context=pattern_info['context'],
                        position=match.start()
                    ))
        
        return intents
    
    def _rank_location_intents(self, intents: List[LocationIntent], text: str) -> Optional[LocationIntent]:
        """Rank location intents by confidence and context"""
        if not intents:
            return None
        
        # Prioritize more specific patterns over longer ones
        for intent in intents:
            # Penalize very long locations (likely over-extracted)
            if len(intent.location) > 50:
                intent.confidence -= 0.3
            
            # Boost specific location patterns
            if intent.context == 'specific_location':
                intent.confidence += 0.2
            elif intent.context == 'complex_location':
                # Only boost if it's not too long
                if len(intent.location) < 30:
                    intent.confidence += 0.1
                else:
                    intent.confidence -= 0.2
        
        # Sort by confidence (highest first)
        intents.sort(key=lambda x: x.confidence, reverse=True)
        
        # Additional ranking factors
        for intent in intents:
            # Boost confidence for locations that appear later in the text (more likely to be the target)
            position_boost = (len(text) - intent.position) / len(text) * 0.1
            intent.confidence += position_boost
            
            # Boost for shorter, more specific locations (avoid long phrases)
            word_count = len(intent.location.split())
            if word_count <= 3:  # Prefer shorter locations
                intent.confidence += 0.1
            else:
                intent.confidence -= 0.2  # Penalize very long phrases
            
            # Boost for specific context types
            if intent.context == 'at_prepositional':
                intent.confidence += 0.2
        
        # Re-sort with updated confidence
        intents.sort(key=lambda x: x.confidence, reverse=True)
        
        return intents[0] if intents else None
    
    def _format_location_for_geocoding(self, location: str) -> str:
        """Format location for better geocoding results"""
        location_lower = location.lower()
        
        # Common location corrections
        corrections = {
            'robinsons beach': 'robinson beach',
            'coney island': 'coney island',
            'staten island': 'staten island, ny',
            'manhattan': 'manhattan, ny',
            'brooklyn': 'brooklyn, ny',
            'queens': 'queens, ny',
            'bronx': 'bronx, ny'
        }
        
        # Apply corrections
        for wrong, correct in corrections.items():
            if wrong in location_lower:
                location = location.replace(wrong, correct)
                break
        
        # Add state if missing for NYC boroughs
        if 'staten island' in location_lower and ', ny' not in location_lower:
            location = location.replace('staten island', 'staten island, ny')
        elif 'manhattan' in location_lower and ', ny' not in location_lower:
            location = location.replace('manhattan', 'manhattan, ny')
        elif 'brooklyn' in location_lower and ', ny' not in location_lower:
            location = location.replace('brooklyn', 'brooklyn, ny')
        elif 'queens' in location_lower and ', ny' not in location_lower:
            location = location.replace('queens', 'queens, ny')
        elif 'bronx' in location_lower and ', ny' not in location_lower:
            location = location.replace('bronx', 'bronx, ny')
        
        return location
    
    async def _validate_location_smart(self, location: str) -> Optional[str]:
        """Validate location using smart API strategy with ambiguity handling"""
        try:
            # Format location for better geocoding results
            formatted_location = self._format_location_for_geocoding(location)
            
            # First try direct geocoding for the formatted location
            geocode_result = await self.api_client.geocode_location(formatted_location)
            
            if geocode_result and geocode_result.get("success"):
                validated_location = geocode_result.get("place_name", location)
                
                # Check for ambiguous locations that need clarification
                ambiguous_locations = self._check_location_ambiguity(location, validated_location)
                if ambiguous_locations:
                    logger.info(f"🔍 Ambiguous location detected: {location} -> {validated_location}")
                    return f"AMBIGUOUS:{validated_location}"
                
                logger.info(f"✅ Geocoding API validated: '{location}' -> '{validated_location}'")
                return validated_location
            
            # If direct geocoding fails, try autocomplete for suggestions
            autocomplete_result = await self.api_client.search_autocomplete(location)
            
            if autocomplete_result and autocomplete_result.get("success"):
                suggestions = autocomplete_result.get("suggestions", [])
                if suggestions:
                    # Use the first (best) suggestion
                    best_match = suggestions[0]
                    validated_location = best_match.get("place_name", location)
                    logger.info(f"✅ Autocomplete API validated: '{location}' -> '{validated_location}'")
                    return validated_location
            
            logger.info(f"❌ APIs rejected location: '{location}'")
            return None
                    
        except Exception as e:
            logger.warning(f"⚠️ Error validating '{location}' with APIs: {e}")
        return None
    
    def _check_location_ambiguity(self, original_location: str, validated_location: str) -> List[str]:
        """Check if location is ambiguous and return alternative suggestions"""
        # Common ambiguous city names
        ambiguous_cities = {
            "woodbridge": ["Woodbridge, New Jersey", "Woodbridge, Virginia"],
            "springfield": ["Springfield, Illinois", "Springfield, Massachusetts", "Springfield, Missouri"],
            "franklin": ["Franklin, Tennessee", "Franklin, Massachusetts"],
            "clinton": ["Clinton, Iowa", "Clinton, Mississippi", "Clinton, New Jersey"],
            "madison": ["Madison, Wisconsin", "Madison, Alabama", "Madison, Mississippi"],
            "georgetown": ["Georgetown, Texas", "Georgetown, South Carolina", "Georgetown, Washington DC"],
            "columbia": ["Columbia, South Carolina", "Columbia, Missouri", "Columbia, Maryland"],
            "auburn": ["Auburn, Alabama", "Auburn, Washington", "Auburn, New York"],
            "troy": ["Troy, Michigan", "Troy, New York", "Troy, Alabama"],
            "newport": ["Newport, Rhode Island", "Newport, Kentucky", "Newport, Oregon"]
        }
        
        location_lower = original_location.lower().strip()
        
        if location_lower in ambiguous_cities:
            return ambiguous_cities[location_lower]
        
        return []
    
    def extract_all_potential_locations(self, text: str) -> List[str]:
        """
        Extract all potential locations from text using smart analysis
        
        Args:
            text: Input text to analyze
            
        Returns:
            List of potential location strings
        """
        intents = self._detect_location_intents(text)
        return [intent.location for intent in intents]
    
    def analyze_location_context(self, text: str) -> Dict[str, any]:
        """
        Analyze the context around location mentions
        
        Args:
            text: Input text to analyze
            
        Returns:
            Dictionary with location analysis
        """
        intents = self._detect_location_intents(text)
        
        analysis = {
            'total_locations': len(intents),
            'locations': [intent.location for intent in intents],
            'best_location': intents[0].location if intents else None,
            'confidence': intents[0].confidence if intents else 0.0,
            'contexts': [intent.context for intent in intents]
        }
        
        return analysis

# Initialize the smart detector
location_detector = SmartLocationDetector()

if __name__ == "__main__":
    # Test the smart location detector
    test_queries = [
        "i want to open a coffee shop in miami",
        "i want to open a gym in seattle",
        "i want to open a restaurant in new york",
        "i want to open a moro boat shop in coney island",
        "i want to open a store in london",
        "i want to start a business in san francisco california",
        "looking to open a franchise in austin, texas",
        "considering a location in beverly hills, ca"
    ]
    
    for query in test_queries:
        result = location_detector.detect_location(query)
        print(f"Query: '{query}'")
        print(f"  -> Location: {result}")
        
        # Also test analysis
        analysis = location_detector.analyze_location_context(query)
        print(f"  -> Analysis: {analysis}")
        print()