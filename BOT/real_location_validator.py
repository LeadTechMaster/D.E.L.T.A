#!/usr/bin/env python3
"""
Real Location Validator using Mapbox Geocoding API
Validates locations using real API data - NO HARDCODED DATA
"""

import logging
import httpx
import asyncio
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
import json

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class LocationValidationResult:
    """Result of location validation"""
    is_valid: bool
    location_name: str
    coordinates: Dict[str, float]
    suggestions: List[str]
    confidence: float
    api_response: Dict[str, Any]

class RealLocationValidator:
    """Real-time location validator using Mapbox Geocoding API"""
    
    def __init__(self):
        """Initialize the validator with real API credentials"""
        self.mapbox_token = "pk.eyJ1Ijoic3VwcG9ydG1vdmVkaW4iLCJhIjoiY21kZmdxdHh6MGQ2aDJqcHE2YTIwbTFrMiJ9.I1xkq82JXLMlgB02xT8LMw"
        self.base_url = "https://api.mapbox.com/geocoding/v5/mapbox.places"
        logger.info("📍 Real Location Validator initialized with Mapbox API")
    
    async def validate_location(self, location_query: str) -> LocationValidationResult:
        """
        Validate location using real Mapbox Geocoding API
        
        Args:
            location_query: Location string to validate
            
        Returns:
            LocationValidationResult with validation details
        """
        if not location_query or not location_query.strip():
            return LocationValidationResult(
                is_valid=False,
                location_name="",
                coordinates={},
                suggestions=[],
                confidence=0.0,
                api_response={}
            )
        
        logger.info(f"📍 Validating location: '{location_query}' using Mapbox API")
        
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                # Call Mapbox Geocoding API
                url = f"{self.base_url}/{location_query}.json"
                params = {
                    "access_token": self.mapbox_token,
                    "limit": 5,  # Get top 5 results
                    "types": "place,locality,neighborhood,address"  # Focus on actual places
                }
                
                response = await client.get(url, params=params)
                response.raise_for_status()
                
                api_data = response.json()
                logger.info(f"📍 Mapbox API response: {len(api_data.get('features', []))} results")
                
                # Process API response
                return self._process_mapbox_response(location_query, api_data)
                
        except httpx.TimeoutException:
            logger.error(f"❌ Mapbox API timeout for: {location_query}")
            return LocationValidationResult(
                is_valid=False,
                location_name=location_query,
                coordinates={},
                suggestions=[],
                confidence=0.0,
                api_response={"error": "API timeout"}
            )
        except httpx.HTTPStatusError as e:
            logger.error(f"❌ Mapbox API error: {e.response.status_code}")
            return LocationValidationResult(
                is_valid=False,
                location_name=location_query,
                coordinates={},
                suggestions=[],
                confidence=0.0,
                api_response={"error": f"HTTP {e.response.status_code}"}
            )
        except Exception as e:
            logger.error(f"❌ Location validation error: {e}")
            return LocationValidationResult(
                is_valid=False,
                location_name=location_query,
                coordinates={},
                suggestions=[],
                confidence=0.0,
                api_response={"error": str(e)}
            )
    
    def _process_mapbox_response(self, original_query: str, api_data: Dict[str, Any]) -> LocationValidationResult:
        """Process Mapbox API response and determine best match"""
        features = api_data.get("features", [])
        
        if not features:
            logger.warning(f"⚠️ No results found for: {original_query}")
            return LocationValidationResult(
                is_valid=False,
                location_name=original_query,
                coordinates={},
                suggestions=[],
                confidence=0.0,
                api_response=api_data
            )
        
        # Get the best match (first result)
        best_match = features[0]
        best_confidence = best_match.get("relevance", 0.0)
        
        # Extract location details
        location_name = best_match.get("place_name", "")
        coordinates = {
            "longitude": best_match.get("center", [0, 0])[0],
            "latitude": best_match.get("center", [0, 0])[1]
        }
        
        # Generate suggestions from other results
        suggestions = []
        for feature in features[1:4]:  # Get next 3 results as suggestions
            place_name = feature.get("place_name", "")
            if place_name and place_name != location_name:
                suggestions.append(place_name)
        
        # Determine if location is valid based on confidence and relevance
        is_valid = best_confidence > 0.7  # High confidence threshold
        
        logger.info(f"📍 Validation result: {location_name} (confidence: {best_confidence:.2f}, valid: {is_valid})")
        
        return LocationValidationResult(
            is_valid=is_valid,
            location_name=location_name,
            coordinates=coordinates,
            suggestions=suggestions,
            confidence=best_confidence,
            api_response=api_data
        )
    
    async def get_location_suggestions(self, partial_query: str) -> List[str]:
        """
        Get location suggestions using Mapbox Autocomplete API
        
        Args:
            partial_query: Partial location query
            
        Returns:
            List of location suggestions
        """
        if not partial_query or len(partial_query) < 2:
            return []
        
        logger.info(f"📍 Getting suggestions for: '{partial_query}'")
        
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                url = f"{self.base_url}/{partial_query}.json"
                params = {
                    "access_token": self.mapbox_token,
                    "limit": 5,
                    "autocomplete": "true",
                    "types": "place,locality,neighborhood"
                }
                
                response = await client.get(url, params=params)
                response.raise_for_status()
                
                api_data = response.json()
                features = api_data.get("features", [])
                
                suggestions = []
                for feature in features:
                    place_name = feature.get("place_name", "")
                    if place_name:
                        suggestions.append(place_name)
                
                logger.info(f"📍 Found {len(suggestions)} suggestions")
                return suggestions
                
        except Exception as e:
            logger.error(f"❌ Error getting suggestions: {e}")
            return []

# Global instance
real_location_validator = RealLocationValidator()

# Convenience functions
async def validate_location(location_query: str) -> LocationValidationResult:
    """Convenience function for location validation"""
    return await real_location_validator.validate_location(location_query)

async def get_location_suggestions(partial_query: str) -> List[str]:
    """Convenience function for getting location suggestions"""
    return await real_location_validator.get_location_suggestions(partial_query)

if __name__ == "__main__":
    # Test the validator
    async def test_validator():
        test_locations = [
            "New York",
            "Clifton, NJ",
            "Miami, FL",
            "Seattle, WA",
            "invalid_location_xyz"
        ]
        
        print("🧪 Testing Real Location Validator:")
        print("=" * 50)
        
        for location in test_locations:
            result = await validate_location(location)
            print(f"Input: '{location}'")
            print(f"Valid: {result.is_valid}")
            print(f"Name: {result.location_name}")
            print(f"Confidence: {result.confidence:.2f}")
            if result.suggestions:
                print(f"Suggestions: {result.suggestions}")
            print("-" * 30)
    
    asyncio.run(test_validator())



