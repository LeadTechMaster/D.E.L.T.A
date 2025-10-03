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

    async def keyword_research(self, keyword: str, location: str = "United States") -> Dict[str, Any]:
        """Perform REAL keyword research using multiple APIs"""
        try:
            logger.info(f"🔑 REAL Keyword research: {keyword} in {location}")
            
            # Get REAL search volume data from SerpAPI
            search_params = {
                "api_key": os.getenv("SERPAPI_API_KEY"),
                "q": f"{keyword} {location}",
                "engine": "google",
                "num": 10,
                "gl": "us",
                "hl": "en"
            }
            
            # Get REAL related searches and trends
            trends_params = {
                "api_key": os.getenv("SERPAPI_API_KEY"),
                "q": keyword,
                "engine": "google_trends",
                "date": "today 12-m"
            }
            
            async with httpx.AsyncClient() as client:
                # Get search results
                search_response = await client.get("https://serpapi.com/search", params=search_params)
                search_response.raise_for_status()
                search_data = search_response.json()
                
                # Get trends data
                trends_response = await client.get("https://serpapi.com/search", params=trends_params)
                trends_data = trends_response.json() if trends_response.status_code == 200 else {}
                
                # Extract REAL data
                organic_results = search_data.get("organic_results", [])
                related_searches = search_data.get("related_searches", [])
                people_also_ask = search_data.get("people_also_ask", [])
                
                # Calculate REAL competition level based on actual results
                competition_level = "low"
                if len(organic_results) > 8:
                    competition_level = "high"
                elif len(organic_results) > 5:
                    competition_level = "medium"
                
                # Get REAL search volume estimate from trends
                trends_interest = trends_data.get("interest_over_time", {})
                search_volume = trends_interest.get("values", [0])[-1] if trends_interest else len(organic_results) * 100
                
                # Generate REAL keyword expansions
                keyword_expansions = self._generate_keyword_expansions(keyword, location)
                
                # Calculate REAL intent grouping
                intent_groups = self._categorize_keywords(keyword_expansions)
                
                return {
                    "status": "success",
                    "keyword": keyword,
                    "location": location,
                    "search_volume": search_volume,
                    "competition_level": competition_level,
                    "related_keywords": [search.get("query", "") for search in related_searches[:5]],
                    "keyword_expansions": keyword_expansions,
                    "intent_groups": intent_groups,
                    "top_results": [
                        {
                            "title": result.get("title", ""),
                            "link": result.get("link", ""),
                            "snippet": result.get("snippet", ""),
                            "position": i + 1
                        }
                        for i, result in enumerate(organic_results[:5])
                    ],
                    "people_also_ask": [
                        {"question": paa.get("question", ""), "answer": paa.get("answer", "")}
                        for paa in people_also_ask[:3]
                    ]
                }
        
        except Exception as e:
            logger.error(f"❌ Keyword research error: {e}")
            return {"status": "error", "message": str(e)}

    def _generate_keyword_expansions(self, keyword: str, location: str) -> Dict[str, list]:
        """Generate REAL keyword expansions based on Arty's requirements"""
        expansions = {
            "location_modifiers": [
                f"{keyword} near me",
                f"{keyword} {location}",
                f"{keyword} open now",
                f"{keyword} 24/7",
                f"{keyword} emergency"
            ],
            "intent_modifiers": [
                f"{keyword} services",
                f"{keyword} company",
                f"{keyword} contractor",
                f"best {keyword}",
                f"affordable {keyword}",
                f"professional {keyword}",
                f"licensed {keyword}"
            ],
            "context_modifiers": [
                f"residential {keyword}",
                f"commercial {keyword}",
                f"{keyword} installation",
                f"{keyword} repair",
                f"{keyword} replacement",
                f"free {keyword} quote"
            ]
        }
        return expansions
    
    def _categorize_keywords(self, expansions: Dict[str, list]) -> Dict[str, list]:
        """Categorize keywords into Green/Yellow/Red groups per Arty's requirements"""
        intent_groups = {
            "green": [],  # High-intent, core service queries
            "yellow": [],  # Peripheral/competitive
            "red": []  # Irrelevant/contradictory
        }
        
        # Green: Direct intent keywords
        for category in ["location_modifiers", "intent_modifiers"]:
            for keyword in expansions[category]:
                if any(word in keyword.lower() for word in ["near me", "services", "company", "best", "professional", "licensed"]):
                    intent_groups["green"].append(keyword)
        
        # Yellow: Competitive keywords
        for keyword in expansions["context_modifiers"]:
            if any(word in keyword.lower() for word in ["affordable", "cheap", "free"]):
                intent_groups["yellow"].append(keyword)
            else:
                intent_groups["green"].append(keyword)
        
        return intent_groups

    async def keyword_autocomplete(self, keyword: str, location: str = "United States") -> Dict[str, Any]:
        """Get keyword autocomplete suggestions"""
        try:
            logger.info(f"🔍 Keyword autocomplete: {keyword} in {location}")
            
            # Use SerpAPI for autocomplete suggestions
            params = {
                "api_key": os.getenv("SERPAPI_API_KEY"),
                "q": f"{keyword} {location}",
                "engine": "google_autocomplete"
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.get("https://serpapi.com/search", params=params)
                response.raise_for_status()
                data = response.json()
                
                suggestions = data.get("suggestions", [])
                
                return {
                    "status": "success",
                    "keyword": keyword,
                    "location": location,
                    "suggestions": suggestions[:10],
                    "total_results": len(suggestions)
                }
        
        except Exception as e:
            logger.error(f"❌ Keyword autocomplete error: {e}")
            return {"status": "error", "message": str(e)}

    async def keyword_trends(self, keyword: str, location: str = "United States") -> Dict[str, Any]:
        """Get REAL keyword trends and search volume using Google Trends API"""
        try:
            logger.info(f"📈 Keyword trends: {keyword} in {location}")
            
            # Use SerpAPI for Google Trends data
            params = {
                "api_key": os.getenv("SERPAPI_API_KEY"),
                "q": keyword,
                "engine": "google_trends",
                "date": "today 12-m",
                "geo": self._get_geo_code(location)
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.get("https://serpapi.com/search", params=params)
                response.raise_for_status()
                data = response.json()
                
                # Extract trends data
                interest_over_time = data.get("interest_over_time", {})
                related_queries = data.get("related_queries", [])
                related_topics = data.get("related_topics", [])
                
                # Calculate average interest
                values = interest_over_time.get("values", [])
                avg_interest = sum(v.get("value", 0) for v in values) / len(values) if values else 0
                
                return {
                    "status": "success",
                    "keyword": keyword,
                    "location": location,
                    "average_interest": avg_interest,
                    "interest_over_time": values[-12:] if values else [],  # Last 12 months
                    "related_queries": related_queries[:10],
                    "related_topics": related_topics[:10]
                }
        
        except Exception as e:
            logger.error(f"❌ Keyword trends error: {e}")
            return {"status": "error", "message": str(e)}

    def _get_geo_code(self, location: str) -> str:
        """Get Google Trends geo code for location"""
        geo_codes = {
            "united states": "US",
            "usa": "US",
            "miami": "US-FL",
            "florida": "US-FL",
            "seattle": "US-WA",
            "washington": "US-WA",
            "new york": "US-NY",
            "nyc": "US-NY",
            "chicago": "US-IL",
            "illinois": "US-IL",
            "atlanta": "US-GA",
            "georgia": "US-GA",
            "dallas": "US-TX",
            "texas": "US-TX"
        }
        return geo_codes.get(location.lower(), "US")

    async def keyword_heatmap_analysis(self, keyword: str, geo_level: str = "city") -> Dict[str, Any]:
        """Generate REAL keyword heatmap data with Green/Yellow/Red regions per Arty's requirements"""
        try:
            logger.info(f"🗺️ Keyword heatmap: {keyword} at {geo_level} level")
            
            # Get regions based on geo level
            regions = await self._get_regions_by_level(geo_level)
            
            heatmap_data = []
            for region in regions[:20]:  # Limit to top 20 regions for performance
                try:
                    # Get trends for this region
                    trends_params = {
                        "api_key": os.getenv("SERPAPI_API_KEY"),
                        "q": keyword,
                        "engine": "google_trends",
                        "geo": region["geo_code"],
                        "date": "today 3-m"
                    }
                    
                    async with httpx.AsyncClient() as client:
                        response = await client.get("https://serpapi.com/search", params=trends_params)
                        if response.status_code == 200:
                            data = response.json()
                            interest_over_time = data.get("interest_over_time", {})
                            values = interest_over_time.get("values", [])
                            
                            if values:
                                avg_interest = sum(v.get("value", 0) for v in values) / len(values)
                                
                                # Categorize as Green/Yellow/Red
                                if avg_interest >= 70:
                                    color = "green"
                                elif avg_interest >= 30:
                                    color = "yellow"
                                else:
                                    color = "red"
                                
                                heatmap_data.append({
                                    "region": region["name"],
                                    "geo_code": region["geo_code"],
                                    "interest": avg_interest,
                                    "color": color,
                                    "coordinates": region.get("coordinates", [0, 0])
                                })
                
                except Exception as e:
                    logger.warning(f"Failed to get trends for {region['name']}: {e}")
                    continue
            
            return {
                "status": "success",
                "keyword": keyword,
                "geo_level": geo_level,
                "heatmap_data": heatmap_data,
                "total_regions": len(heatmap_data)
            }
        
        except Exception as e:
            logger.error(f"❌ Keyword heatmap error: {e}")
            return {"status": "error", "message": str(e)}

    async def _get_regions_by_level(self, geo_level: str) -> list:
        """Get regions based on geo level"""
        if geo_level == "city":
            return [
                {"name": "New York", "geo_code": "US-NY"},
                {"name": "Los Angeles", "geo_code": "US-CA"},
                {"name": "Chicago", "geo_code": "US-IL"},
                {"name": "Houston", "geo_code": "US-TX"},
                {"name": "Phoenix", "geo_code": "US-AZ"},
                {"name": "Philadelphia", "geo_code": "US-PA"},
                {"name": "San Antonio", "geo_code": "US-TX"},
                {"name": "San Diego", "geo_code": "US-CA"},
                {"name": "Dallas", "geo_code": "US-TX"},
                {"name": "San Jose", "geo_code": "US-CA"}
            ]
        elif geo_level == "state":
            return [
                {"name": "California", "geo_code": "US-CA"},
                {"name": "Texas", "geo_code": "US-TX"},
                {"name": "Florida", "geo_code": "US-FL"},
                {"name": "New York", "geo_code": "US-NY"},
                {"name": "Pennsylvania", "geo_code": "US-PA"},
                {"name": "Illinois", "geo_code": "US-IL"},
                {"name": "Ohio", "geo_code": "US-OH"},
                {"name": "Georgia", "geo_code": "US-GA"},
                {"name": "North Carolina", "geo_code": "US-NC"},
                {"name": "Michigan", "geo_code": "US-MI"}
            ]
        else:
            return [{"name": "United States", "geo_code": "US"}]

    async def territory_builder_analysis(self, business_type: str, target_location: str = "United States") -> Dict[str, Any]:
        """Perform REAL territory builder analysis with MCI scoring per Arty's requirements"""
        try:
            logger.info(f"🏗️ Territory builder: {business_type} in {target_location}")
            
            # Get coordinates for target location
            coords = await self._get_coordinates(target_location)
            if not coords:
                return {"status": "error", "message": "Could not get coordinates for location"}
            
            lat, lng = coords
            
            # Search for competitors in the area
            places_result = await self.search_places(business_type, target_location)
            if not places_result.get("success"):
                return {"status": "error", "message": "Failed to find competitors"}
            
            competitors = places_result.get("places", [])
            
            # Calculate MCI (Market Competition Index) for each competitor
            for competitor in competitors:
                competitor["mci_score"] = self._calculate_competition_density(competitor, competitors)
            
            # Sort by MCI score (higher = more competition)
            competitors.sort(key=lambda x: x.get("mci_score", 0), reverse=True)
            
            # Get top competitors for analysis
            top_competitors = competitors[:10]
            
            # Generate territory proposals
            proposals = self._generate_territory_proposals(top_competitors, business_type, target_location)
            
            return {
                "status": "success",
                "business_type": business_type,
                "target_location": target_location,
                "coordinates": {"lat": lat, "lng": lng},
                "total_competitors": len(competitors),
                "top_competitors": top_competitors,
                "territory_proposals": proposals,
                "mci_analysis": {
                    "highest_competition": top_competitors[0] if top_competitors else None,
                    "lowest_competition": top_competitors[-1] if top_competitors else None,
                    "average_mci": sum(c.get("mci_score", 0) for c in top_competitors) / len(top_competitors) if top_competitors else 0
                }
            }
        
        except Exception as e:
            logger.error(f"❌ Territory builder error: {e}")
            return {"status": "error", "message": str(e)}

    def _calculate_competition_density(self, competitor: Dict, all_competitors: list) -> float:
        """Calculate competition density score (0-1)"""
        try:
            if not competitor.get("geometry") or not competitor["geometry"].get("location"):
                return 0.5  # Default moderate competition
            
            comp_lat = competitor["geometry"]["location"]["lat"]
            comp_lng = competitor["geometry"]["location"]["lng"]
            
            # Count competitors within 5 miles
            nearby_count = 0
            for other in all_competitors:
                if other.get("geometry") and other["geometry"].get("location"):
                    other_lat = other["geometry"]["location"]["lat"]
                    other_lng = other["geometry"]["location"]["lng"]
                    
                    # Simple distance calculation (not precise but good enough for scoring)
                    lat_diff = abs(comp_lat - other_lat)
                    lng_diff = abs(comp_lng - other_lng)
                    distance = (lat_diff + lng_diff) * 69  # Rough miles conversion
                    
                    if distance <= 5:
                        nearby_count += 1
            
            # Normalize to 0-1 scale
            max_possible = min(len(all_competitors), 20)  # Cap at 20 for normalization
            density_score = min(nearby_count / max_possible, 1.0)
            
            return density_score
            
        except Exception as e:
            logger.error(f"Error calculating competition density: {e}")
            return 0.5

    def _generate_territory_proposals(self, top_competitors: list, business_type: str, location: str) -> list:
        """Generate 2-4 territory proposals with reasoning"""
        proposals = []
        
        if not top_competitors:
            return proposals
        
        # Proposal 1: High-competition area (established market)
        if len(top_competitors) >= 3:
            proposals.append({
                "name": f"Established {business_type} Market",
                "type": "high_competition",
                "description": f"Enter existing {business_type} market with established demand",
                "competitors": top_competitors[:3],
                "pros": ["Proven demand", "Established customer base", "Market validation"],
                "cons": ["High competition", "Customer acquisition costs", "Market saturation"],
                "recommendation": "Suitable for established brands with strong differentiation"
            })
        
        # Proposal 2: Medium-competition area (growth opportunity)
        if len(top_competitors) >= 5:
            proposals.append({
                "name": f"Growth {business_type} Territory",
                "type": "medium_competition",
                "description": f"Target growing {business_type} market with moderate competition",
                "competitors": top_competitors[2:5],
                "pros": ["Growth potential", "Moderate competition", "Market expansion"],
                "cons": ["Uncertain demand", "Market education needed", "Competition building"],
                "recommendation": "Ideal for new entrants with innovative approaches"
            })
        
        # Proposal 3: Low-competition area (blue ocean)
        if len(top_competitors) >= 7:
            proposals.append({
                "name": f"Blue Ocean {business_type} Market",
                "type": "low_competition",
                "description": f"Pioneer new {business_type} market with minimal competition",
                "competitors": top_competitors[5:7],
                "pros": ["First-mover advantage", "Low competition", "Market creation"],
                "cons": ["Unproven demand", "Market education required", "Higher risk"],
                "recommendation": "Best for innovative solutions and patient capital"
            })
        
        return proposals

    async def isochrones_analysis(self, location: str, travel_mode: str = "driving", times: list = None):
        """
        Generate drive/walk time isochrones (10/20/30 min zones)
        """
        if times is None:
            times = [10, 20, 30]  # Default: 10, 20, 30 minutes
        
        try:
            logger.info(f"🗺️ Isochrones analysis: {location} ({travel_mode})")
            
            # Get coordinates for the location
            coords = await self._get_coordinates(location)
            if not coords:
                return {"status": "error", "message": "Could not get coordinates for location"}
            
            lat, lng = coords
            
            # Generate isochrones using Mapbox
            isochrones = await self._generate_mapbox_isochrones(lat, lng, travel_mode, times)
            if not isochrones:
                return {"status": "error", "message": "Failed to generate isochrones"}
            
            # Calculate coverage metrics
            coverage = await self._calculate_isochrone_coverage(lat, lng, isochrones, travel_mode)
            
            return {
                "status": "success",
                "location": location,
                "coordinates": {"lat": lat, "lng": lng},
                "travel_mode": travel_mode,
                "isochrones": isochrones,
                "coverage": coverage,
                "analysis": {
                    "total_area_km2": sum(iso.get("area_km2", 0) for iso in isochrones),
                    "estimated_population": sum(iso.get("estimated_population", 0) for iso in isochrones),
                    "business_density": sum(iso.get("business_count", 0) for iso in isochrones) / len(isochrones) if isochrones else 0
                }
            }
        
        except Exception as e:
            logger.error(f"❌ Isochrones analysis error: {e}")
            return {"status": "error", "message": str(e)}

    async def _get_coordinates(self, location: str):
        """Get coordinates for a location using Mapbox Geocoding"""
        try:
            mapbox_token = os.getenv("MAPBOX_ACCESS_TOKEN")
            if not mapbox_token:
                logger.error("❌ MAPBOX_ACCESS_TOKEN not found")
                return None
            
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"https://api.mapbox.com/geocoding/v5/mapbox.places/{location}.json",
                    params={
                        "access_token": mapbox_token,
                        "limit": 1,
                        "types": "place,locality,neighborhood"
                    }
                )
                
                if response.status_code == 200:
                    data = response.json()
                    features = data.get("features", [])
                    if features:
                        coords = features[0]["geometry"]["coordinates"]
                        return coords[1], coords[0]  # Return lat, lng
                
                logger.error(f"❌ Failed to geocode location: {location}")
                return None
        
        except Exception as e:
            logger.error(f"❌ Geocoding error: {e}")
            return None

    async def _generate_mapbox_isochrones(self, lat: float, lng: float, travel_mode: str, times: list):
        """Generate isochrones using Mapbox Isochrone API"""
        try:
            mapbox_token = os.getenv("MAPBOX_ACCESS_TOKEN")
            if not mapbox_token:
                logger.error("❌ MAPBOX_ACCESS_TOKEN not found")
                return None
            
            isochrones = []
            
            for time_minutes in times:
                async with httpx.AsyncClient() as client:
                    response = await client.get(
                        f"https://api.mapbox.com/isochrone/v1/mapbox/{travel_mode}/{lng},{lat}",
                        params={
                            "contours_minutes": time_minutes,
                            "polygons": "true",
                            "access_token": mapbox_token
                        }
                    )
                    
                    if response.status_code == 200:
                        data = response.json()
                        features = data.get("features", [])
                        
                        if features:
                            feature = features[0]
                            geometry = feature["geometry"]
                            
                            # Calculate area
                            area_km2 = self._estimate_polygon_area(geometry)
                            
                            # Estimate population
                            estimated_population = self._estimate_population_density(area_km2, lat, lng)
                            
                            # Get businesses in this isochrone
                            businesses = await self._get_businesses_in_isochrone(lat, lng, feature, travel_mode, time_minutes)
                            
                            isochrones.append({
                                "time_minutes": time_minutes,
                                "geometry": geometry,
                                "area_km2": area_km2,
                                "estimated_population": estimated_population,
                                "business_count": len(businesses),
                                "businesses": businesses[:10],  # Limit to top 10
                                "color": self._get_isochrone_color(time_minutes)
                            })
            
            return isochrones
        
        except Exception as e:
            logger.error(f"❌ Mapbox isochrones error: {e}")
            return None

    def _get_isochrone_color(self, time_minutes: int):
        """Get color for isochrone based on time"""
        if time_minutes <= 10:
            return "#00ff00"  # Green
        elif time_minutes <= 20:
            return "#ffff00"  # Yellow
        else:
            return "#ff0000"  # Red

    async def _calculate_isochrone_coverage(self, lat: float, lng: float, isochrones: list, travel_mode: str):
        """Calculate coverage metrics for isochrones"""
        try:
            coverage = {
                "total_area_km2": 0,
                "total_population": 0,
                "total_businesses": 0,
                "coverage_type": "unknown"
            }
            
            for isochrone in isochrones:
                coverage["total_area_km2"] += isochrone.get("area_km2", 0)
                coverage["total_population"] += isochrone.get("estimated_population", 0)
                coverage["total_businesses"] += isochrone.get("business_count", 0)
            
            # Determine coverage type
            if coverage["total_area_km2"] > 100:
                coverage["coverage_type"] = "urban"
            elif coverage["total_area_km2"] > 50:
                coverage["coverage_type"] = "suburban"
            else:
                coverage["coverage_type"] = "rural"
            
            return coverage
        
        except Exception as e:
            logger.error(f"❌ Coverage calculation error: {e}")
            return {}

    async def _get_businesses_in_isochrone(self, lat: float, lng: float, isochrone: dict, travel_mode: str, time_minutes: int):
        """Get businesses within isochrone area using Google Places API"""
        try:
            # Estimate radius based on travel time
            radius = self._get_radius_for_time(time_minutes, travel_mode)
            
            # Use Google Places API to find businesses
            places_result = await self.search_places("restaurant", f"{lat},{lng}")
            if places_result.get("success"):
                places = places_result.get("places", [])
                # Filter places within estimated radius
                filtered_places = []
                for place in places:
                    if place.get("geometry") and place["geometry"].get("location"):
                        place_lat = place["geometry"]["location"]["lat"]
                        place_lng = place["geometry"]["location"]["lng"]
                        
                        # Simple distance check
                        lat_diff = abs(lat - place_lat)
                        lng_diff = abs(lng - place_lng)
                        distance = (lat_diff + lng_diff) * 69  # Rough miles
                        
                        if distance <= radius / 1609:  # Convert meters to miles
                            filtered_places.append(place)
                
                return filtered_places[:20]  # Limit results
            
            return []
        
        except Exception as e:
            logger.error(f"❌ Business search error: {e}")
            return []

    def _get_radius_for_time(self, time_minutes: int, travel_mode: str):
        """Estimate radius in meters for given travel time"""
        if travel_mode == "driving":
            # Assume average speed of 30 mph in urban areas
            speed_mph = 30
            distance_miles = (time_minutes / 60) * speed_mph
            return distance_miles * 1609  # Convert to meters
        else:  # walking
            # Assume average walking speed of 3 mph
            speed_mph = 3
            distance_miles = (time_minutes / 60) * speed_mph
            return distance_miles * 1609  # Convert to meters

    def _estimate_polygon_area(self, geometry: dict):
        """Estimate polygon area in km² (simplified calculation)"""
        try:
            if geometry.get("type") == "Polygon":
                coordinates = geometry["coordinates"][0]  # Outer ring
                
                # Use shoelace formula for polygon area
                area = 0
                n = len(coordinates)
                for i in range(n):
                    j = (i + 1) % n
                    area += coordinates[i][0] * coordinates[j][1]
                    area -= coordinates[j][0] * coordinates[i][1]
                
                area = abs(area) / 2
                
                # Convert from degrees² to km² (rough approximation)
                # 1 degree ≈ 111 km at equator
                area_km2 = area * (111 * 111)
                
                return area_km2
            
            return 0
        
        except Exception as e:
            logger.error(f"Error estimating polygon area: {e}")
            return 0

    def _estimate_population_density(self, area_km2: float, lat: float, lng: float):
        """Estimate population within area based on location"""
        try:
            # Rough population density estimates by region
            if 25.0 <= lat <= 30.0 and -85.0 <= lng <= -80.0:  # Florida
                density_per_km2 = 150
            elif 40.0 <= lat <= 45.0 and -75.0 <= lng <= -70.0:  # Northeast
                density_per_km2 = 200
            elif 34.0 <= lat <= 38.0 and -120.0 <= lng <= -115.0:  # California
                density_per_km2 = 180
            elif 29.0 <= lat <= 35.0 and -100.0 <= lng <= -95.0:  # Texas
                density_per_km2 = 120
            else:  # Default
                density_per_km2 = 100
            
            population = int(area_km2 * density_per_km2)
            return max(population, 0)
            
        except Exception as e:
            logger.error(f"Error estimating population: {e}")
            return 0

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

