#!/usr/bin/env python3
"""
🔌 D.E.L.T.A Bot API Client
Connects to the existing D.E.L.T.A backend APIs for real data analysis
"""

import httpx
import logging
from typing import Dict, Any, Optional
import json
from datetime import datetime

logger = logging.getLogger(__name__)

class DeltaAPIClient:
    def __init__(self, base_url: str = "http://localhost:8001"):
        self.base_url = base_url
        self.client = httpx.AsyncClient(timeout=30.0)
        logger.info(f"🔌 API Client initialized for {base_url}")
    
    async def __aenter__(self):
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.client.aclose()
    
    async def geocode_location(self, location: str) -> Dict[str, Any]:
        """Geocode a location using Mapbox API"""
        try:
            logger.info(f"🗺️ Geocoding location: {location}")
            response = await self.client.get(
                f"{self.base_url}/api/v1/mapbox/geocode",
                params={"location": location}
            )
            
            if response.status_code == 200:
                data = response.json()
                logger.info(f"✅ Geocoding successful for {location}")
                return {
                    "success": True,
                    "data": data,
                    "coordinates": data.get("coordinates", {}),
                    "place_name": data.get("place_name", location)
                }
            else:
                logger.error(f"❌ Geocoding failed for {location}: {response.status_code}")
                return {"success": False, "error": f"HTTP {response.status_code}"}
                
        except Exception as e:
            logger.error(f"❌ Geocoding error for {location}: {e}")
            return {"success": False, "error": str(e)}
    
    async def search_places(self, query: str, location: str) -> Dict[str, Any]:
        """Search for places using Google Places API"""
        try:
            logger.info(f"🏢 Searching places: {query} in {location}")
            response = await self.client.get(
                f"{self.base_url}/api/v1/google-places/search",
                params={"query": query, "location": location}
            )
            
            if response.status_code == 200:
                data = response.json()
                logger.info(f"✅ Places search successful: {len(data.get('businesses', []))} results")
                return {
                    "success": True,
                    "data": data,
                    "businesses": data.get("businesses", []),
                    "total_results": data.get("total_results", 0)
                }
            else:
                logger.error(f"❌ Places search failed: {response.status_code}")
                return {"success": False, "error": f"HTTP {response.status_code}"}
                
        except Exception as e:
            logger.error(f"❌ Places search error: {e}")
            return {"success": False, "error": str(e)}
    
    async def analyze_territory(self, lat: float, lng: float, business_type: str, radius_miles: float = 10) -> Dict[str, Any]:
        """Analyze territory using our territory analysis API"""
        try:
            logger.info(f"🎯 Analyzing territory: {business_type} at ({lat}, {lng})")
            response = await self.client.get(
                f"{self.base_url}/api/v1/territory/analyze",
                params={
                    "center_lat": lat,
                    "center_lng": lng,
                    "business_type": business_type,
                    "radius_miles": radius_miles
                }
            )
            
            if response.status_code == 200:
                data = response.json()
                logger.info(f"✅ Territory analysis successful")
                return {
                    "success": True,
                    "data": data,
                    "territory_analysis": data.get("territory_analysis", {}),
                    "competitor_count": data.get("territory_analysis", {}).get("competitor_count", 0),
                    "opportunity_score": data.get("territory_analysis", {}).get("opportunity_score", 0)
                }
            else:
                logger.error(f"❌ Territory analysis failed: {response.status_code}")
                return {"success": False, "error": f"HTTP {response.status_code}"}
                
        except Exception as e:
            logger.error(f"❌ Territory analysis error: {e}")
            return {"success": False, "error": str(e)}
    
    async def get_demographics(self, state_code: str) -> Dict[str, Any]:
        """Get demographics using Census API"""
        try:
            logger.info(f"👥 Getting demographics for state: {state_code}")
            response = await self.client.get(
                f"{self.base_url}/api/v1/census/demographics",
                params={"state": state_code}
            )
            
            if response.status_code == 200:
                data = response.json()
                logger.info(f"✅ Demographics successful")
                return {
                    "success": True,
                    "data": data,
                    "demographics": data.get("demographics", {}),
                    "population": data.get("demographics", {}).get("total_population", 0),
                    "median_income": data.get("demographics", {}).get("median_household_income", 0)
                }
            else:
                logger.error(f"❌ Demographics failed: {response.status_code}")
                return {"success": False, "error": f"HTTP {response.status_code}"}
                
        except Exception as e:
            logger.error(f"❌ Demographics error: {e}")
            return {"success": False, "error": str(e)}
    
    async def search_franchise_opportunities(self, query: str, location: str) -> Dict[str, Any]:
        """Search for franchise opportunities using SerpAPI"""
        try:
            logger.info(f"🔍 Searching franchise opportunities: {query} in {location}")
            response = await self.client.get(
                f"{self.base_url}/api/v1/serpapi/search",
                params={"query": query, "location": location}
            )
            
            if response.status_code == 200:
                data = response.json()
                logger.info(f"✅ Franchise search successful: {len(data.get('search_results', []))} results")
                return {
                    "success": True,
                    "data": data,
                    "search_results": data.get("search_results", []),
                    "total_results": data.get("total_results", 0)
                }
            else:
                logger.error(f"❌ Franchise search failed: {response.status_code}")
                return {"success": False, "error": f"HTTP {response.status_code}"}
                
        except Exception as e:
            logger.error(f"❌ Franchise search error: {e}")
            return {"success": False, "error": str(e)}
    
    async def search_autocomplete(self, query: str) -> Dict[str, Any]:
        """Search for address autocomplete using Mapbox API"""
        try:
            logger.info(f"🔍 Autocomplete search: {query}")
            response = await self.client.get(
                f"{self.base_url}/api/v1/mapbox/autocomplete",
                params={"query": query}
            )
            
            if response.status_code == 200:
                data = response.json()
                suggestions = data.get("suggestions", [])
                logger.info(f"✅ Autocomplete successful: {len(suggestions)} suggestions")
                
                # Format suggestions for bot display
                formatted_suggestions = []
                for suggestion in suggestions:
                    formatted_suggestions.append({
                        "text": suggestion.get("text", ""),
                        "city": suggestion.get("city", ""),
                        "state": suggestion.get("state", ""),
                        "zip": suggestion.get("zip", ""),
                        "coordinates": suggestion.get("coordinates", [])
                    })
                
                return {
                    "success": True,
                    "data": data,
                    "suggestions": formatted_suggestions,
                    "total_results": len(formatted_suggestions)
                }
            else:
                logger.error(f"❌ Autocomplete search failed: {response.status_code}")
                return {"success": False, "error": f"HTTP {response.status_code}"}
                
        except Exception as e:
            logger.error(f"❌ Autocomplete search error: {e}")
            return {"success": False, "error": str(e)}

# State code mapping for Census API
STATE_CODES = {
    "miami": "12",  # Florida
    "florida": "12",
    "seattle": "53",  # Washington
    "washington": "53",
    "new york": "36",  # New York
    "nyc": "36",
    "manhattan": "36",
    "brooklyn": "36",
    "chicago": "17",  # Illinois
    "illinois": "17",
    "atlanta": "13",  # Georgia
    "georgia": "13",
    "dallas": "48",  # Texas
    "texas": "48"
}

def get_state_code(location: str) -> str:
    """Get state code for location"""
    location_lower = location.lower()
    return STATE_CODES.get(location_lower, "12")  # Default to Florida
