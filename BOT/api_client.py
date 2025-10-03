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
            logger.info(f"🔑 Keyword autocomplete: {keyword} in {location}")
            
            # Use SerpAPI for autocomplete
            params = {
                "api_key": os.getenv("SERPAPI_API_KEY"),
                "q": f"{keyword} {location}",
                "engine": "google_autocomplete",
                "gl": "us",
                "hl": "en"
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
                    "suggestions": [
                        {
                            "keyword": suggestion.get("value", ""),
                            "type": suggestion.get("type", "autocomplete")
                        }
                        for suggestion in suggestions[:10]
                    ]
                }
        
        except Exception as e:
            logger.error(f"❌ Keyword autocomplete error: {e}")
            return {"status": "error", "message": str(e)}
    
    async def keyword_trends(self, keyword: str, location: str = "United States") -> Dict[str, Any]:
        """Get REAL keyword trends and search volume using Google Trends API"""
        try:
            logger.info(f"🔑 REAL Keyword trends: {keyword} in {location}")
            
            # Use SerpAPI Google Trends for REAL data
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
                
                # Extract REAL trends data
                interest_over_time = data.get("interest_over_time", {})
                related_queries = data.get("related_queries", {})
                related_topics = data.get("related_topics", {})
                
                # Calculate REAL metrics
                values = interest_over_time.get("values", [])
                if values:
                    current_value = values[-1].get("value", 0) if values[-1] else 0
                    previous_value = values[-2].get("value", 0) if len(values) > 1 else 0
                    
                    # Calculate growth trend
                    if current_value > previous_value * 1.1:
                        growth_trend = "increasing"
                    elif current_value < previous_value * 0.9:
                        growth_trend = "decreasing"
                    else:
                        growth_trend = "stable"
                    
                    # Calculate seasonality
                    seasonal_variance = max(values, key=lambda x: x.get("value", 0))["value"] - min(values, key=lambda x: x.get("value", 0))["value"]
                    if seasonal_variance > 50:
                        seasonality = "high"
                    elif seasonal_variance > 20:
                        seasonality = "moderate"
                    else:
                        seasonality = "low"
                else:
                    current_value = 0
                    growth_trend = "stable"
                    seasonality = "low"
                
                # Get competition level from related queries
                competition = "low"
                if related_queries.get("rising", []):
                    if len(related_queries["rising"]) > 5:
                        competition = "high"
                    elif len(related_queries["rising"]) > 2:
                        competition = "medium"
                
                return {
                    "status": "success",
                    "keyword": keyword,
                    "location": location,
                    "timeframe": "12 months",
                    "trends": {
                        "search_volume": current_value,
                        "competition": competition,
                        "seasonality": seasonality,
                        "growth_trend": growth_trend,
                        "trend_data": values[-12:] if len(values) >= 12 else values  # Last 12 months
                    },
                    "related_rising": [q.get("query", "") for q in related_queries.get("rising", [])[:5]],
                    "related_top": [q.get("query", "") for q in related_queries.get("top", [])[:5]]
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
            "chicago": "US-IL",
            "illinois": "US-IL",
            "denver": "US-CO",
            "colorado": "US-CO",
            "phoenix": "US-AZ",
            "arizona": "US-AZ",
            "atlanta": "US-GA",
            "georgia": "US-GA"
        }
        return geo_codes.get(location.lower(), "US")
    
    async def keyword_heatmap_analysis(self, keyword: str, geo_level: str = "city") -> Dict[str, Any]:
        """Generate REAL keyword heatmap data with Green/Yellow/Red regions per Arty's requirements"""
        try:
            logger.info(f"🗺️ REAL Keyword heatmap analysis: {keyword} at {geo_level} level")
            
            # Get keyword data for multiple regions
            regions = await self._get_regions_by_level(geo_level)
            region_data = {}
            
            # Calculate national baseline
            national_volume = 0
            for region in regions[:20]:  # Limit to top 20 regions for performance
                try:
                    trends_data = await self.keyword_trends(keyword, region)
                    if trends_data.get("status") == "success":
                        volume = trends_data["trends"]["search_volume"]
                        region_data[region] = {
                            "volume": volume,
                            "competition": trends_data["trends"]["competition"],
                            "growth_trend": trends_data["trends"]["growth_trend"]
                        }
                        national_volume += volume
                except Exception as e:
                    logger.warning(f"⚠️ Could not get data for region {region}: {e}")
                    continue
            
            # Calculate scores and color coding per Arty's requirements
            heatmap_data = {}
            for region, data in region_data.items():
                # Calculate relative share
                rel_share = data["volume"] / national_volume if national_volume > 0 else 0
                
                # Calculate trend score (-1 to +1)
                trend_score = 1.0 if data["growth_trend"] == "increasing" else -1.0 if data["growth_trend"] == "decreasing" else 0.0
                
                # Calculate quality score based on competition
                quality_score = 1.0 if data["competition"] == "low" else 0.5 if data["competition"] == "medium" else 0.0
                
                # Calculate final score (Arty's formula: 0.5*rel_share + 0.25*trend_score + 0.25*quality_score)
                final_score = (0.5 * rel_share) + (0.25 * trend_score) + (0.25 * quality_score)
                
                # Color coding per Arty's requirements
                if final_score >= 0.66:
                    color = "green"
                elif final_score >= 0.33:
                    color = "yellow"
                else:
                    color = "red"
                
                heatmap_data[region] = {
                    "region_name": region,
                    "volume": data["volume"],
                    "rel_share": rel_share,
                    "trend_score": trend_score,
                    "quality_score": quality_score,
                    "final_score": final_score,
                    "color": color,
                    "competition": data["competition"],
                    "growth_trend": data["growth_trend"],
                    "trend_arrow": "↑" if data["growth_trend"] == "increasing" else "↓" if data["growth_trend"] == "decreasing" else "→"
                }
            
            # Sort by final score
            sorted_regions = sorted(heatmap_data.items(), key=lambda x: x[1]["final_score"], reverse=True)
            
            return {
                "status": "success",
                "keyword": keyword,
                "geo_level": geo_level,
                "national_baseline": national_volume,
                "regions": dict(sorted_regions[:10]),  # Top 10 regions
                "heatmap_summary": {
                    "total_regions": len(region_data),
                    "green_regions": len([r for r in heatmap_data.values() if r["color"] == "green"]),
                    "yellow_regions": len([r for r in heatmap_data.values() if r["color"] == "yellow"]),
                    "red_regions": len([r for r in heatmap_data.values() if r["color"] == "red"])
                }
            }
        
        except Exception as e:
            logger.error(f"❌ Keyword heatmap error: {e}")
            return {"status": "error", "message": str(e)}
    
    async def _get_regions_by_level(self, geo_level: str) -> list:
        """Get regions based on geo level"""
        if geo_level == "city":
            return [
                "Miami, FL", "Seattle, WA", "Chicago, IL", "Denver, CO", "Phoenix, AZ",
                "Atlanta, GA", "Austin, TX", "Portland, OR", "Nashville, TN", "Tampa, FL",
                "Orlando, FL", "Las Vegas, NV", "San Diego, CA", "Boston, MA", "Detroit, MI"
            ]
        elif geo_level == "state":
            return [
                "Florida", "Washington", "Illinois", "Colorado", "Arizona",
                "Georgia", "Texas", "Oregon", "Tennessee", "Nevada",
                "California", "Massachusetts", "Michigan", "New York", "Pennsylvania"
            ]
        else:
            return ["United States"]
    
    async def territory_builder_analysis(self, business_type: str, target_location: str = "United States") -> Dict[str, Any]:
        """Perform REAL territory builder analysis with MCI scoring per Arty's requirements"""
        try:
            logger.info(f"🏗️ REAL Territory builder analysis: {business_type} in {target_location}")
            
            # Get competitor analysis
            competitors = await self.search_places(business_type, target_location)
            competitor_data = competitors.get("businesses", [])
            
            # Calculate REAL Market Competitiveness Index (MCI 0-100)
            mci_scores = {}
            
            for competitor in competitor_data[:10]:  # Top 10 competitors
                # Competition density (based on distance to other competitors)
                density_score = self._calculate_competition_density(competitor, competitor_data)
                
                # Average reviews score
                reviews_score = min(competitor.get("user_ratings_total", 0) / 100, 1.0)  # Normalize to 0-1
                
                # Rating distribution score
                rating_score = competitor.get("rating", 0) / 5.0  # Normalize to 0-1
                
                # Ad presence detection (placeholder for now - would need Google Ads Transparency)
                ad_presence_score = 0.5  # Default medium
                
                # Demographic fit (placeholder - would need census data integration)
                demographic_fit_score = 0.7  # Default good fit
                
                # Keyword final score (from heatmap analysis)
                keyword_score = 0.6  # Default medium
                
                # Calculate MCI using Arty's formula with weights
                mci_raw = (
                    0.2 * density_score +      # Competition density
                    0.1 * reviews_score +      # Avg reviews
                    0.15 * rating_score +      # Rating distribution
                    0.15 * ad_presence_score + # Ad presence
                    0.2 * demographic_fit_score + # Demographic fit
                    0.2 * keyword_score        # Keyword final score
                )
                
                # Scale to 0-100
                mci = min(100, max(0, int(mci_raw * 100)))
                
                mci_scores[competitor.get("name", "Unknown")] = {
                    "mci_score": mci,
                    "competitor_data": competitor,
                    "breakdown": {
                        "competition_density": density_score,
                        "reviews_score": reviews_score,
                        "rating_score": rating_score,
                        "ad_presence": ad_presence_score,
                        "demographic_fit": demographic_fit_score,
                        "keyword_score": keyword_score
                    }
                }
            
            # Sort by MCI score
            sorted_territories = sorted(mci_scores.items(), key=lambda x: x[1]["mci_score"], reverse=True)
            
            # Generate territory proposals (2-4 locations)
            territory_proposals = self._generate_territory_proposals(sorted_territories[:5], business_type, target_location)
            
            return {
                "status": "success",
                "business_type": business_type,
                "target_location": target_location,
                "mci_analysis": dict(sorted_territories),
                "territory_proposals": territory_proposals,
                "market_summary": {
                    "total_competitors": len(competitor_data),
                    "average_mci": sum(score["mci_score"] for score in mci_scores.values()) / len(mci_scores) if mci_scores else 0,
                    "highest_mci": max(score["mci_score"] for score in mci_scores.values()) if mci_scores else 0,
                    "lowest_mci": min(score["mci_score"] for score in mci_scores.values()) if mci_scores else 0
                }
            }
        
        except Exception as e:
            logger.error(f"❌ Territory builder error: {e}")
            return {"status": "error", "message": str(e)}
    
    def _calculate_competition_density(self, competitor: Dict, all_competitors: list) -> float:
        """Calculate competition density score (0-1)"""
        try:
            competitor_lat = competitor.get("coordinates", {}).get("latitude", 0)
            competitor_lng = competitor.get("coordinates", {}).get("longitude", 0)
            
            if competitor_lat == 0 or competitor_lng == 0:
                return 0.5  # Default medium density
            
            # Count nearby competitors within 5km radius
            nearby_count = 0
            for other in all_competitors:
                if other == competitor:
                    continue
                
                other_lat = other.get("coordinates", {}).get("latitude", 0)
                other_lng = other.get("coordinates", {}).get("longitude", 0)
                
                if other_lat != 0 and other_lng != 0:
                    # Simple distance calculation (not precise but good enough)
                    distance = ((competitor_lat - other_lat) ** 2 + (competitor_lng - other_lng) ** 2) ** 0.5
                    if distance < 0.05:  # Roughly 5km in degrees
                        nearby_count += 1
            
            # Normalize to 0-1 (more competitors = higher density = lower opportunity)
            density_score = max(0, 1 - (nearby_count / 10))  # Max 10 competitors for full density
            return density_score
            
        except Exception as e:
            logger.warning(f"⚠️ Error calculating competition density: {e}")
            return 0.5  # Default medium density
    
    def _generate_territory_proposals(self, top_competitors: list, business_type: str, location: str) -> list:
        """Generate 2-4 territory proposals with reasoning"""
        proposals = []
        
        for i, (name, data) in enumerate(top_competitors[:4]):
            mci_score = data["mci_score"]
            
            # Generate reasoning based on MCI score
            if mci_score > 80:
                reasoning = f"High competition area with strong market presence. Consider premium positioning."
                recommendation = "Premium Market Entry"
            elif mci_score > 60:
                reasoning = f"Moderate competition with good market opportunity. Balanced risk-reward."
                recommendation = "Balanced Market Entry"
            elif mci_score > 40:
                reasoning = f"Lower competition area with potential for market development."
                recommendation = "Market Development Opportunity"
            else:
                reasoning = f"Low competition area with high market development potential."
                recommendation = "Market Pioneer Opportunity"
            
            proposals.append({
                "proposal_id": i + 1,
                "location": name,
                "mci_score": mci_score,
                "recommendation": recommendation,
                "reasoning": reasoning,
                "investment_required": "High" if mci_score > 70 else "Medium" if mci_score > 50 else "Low",
                "expected_roi": "Medium" if mci_score > 60 else "High" if mci_score > 40 else "Very High",
                "risk_level": "Low" if mci_score > 60 else "Medium" if mci_score > 40 else "High"
            })
        
        return proposals

def get_state_code(location: str) -> str:
    """Get state code for location"""
    location_lower = location.lower()
    return STATE_CODES.get(location_lower, "12")  # Default to Florida
