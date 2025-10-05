#!/usr/bin/env python3
"""
🔍 Enhanced Brightlocal Integration
Adds local SEO intelligence and competitor analysis
"""

import httpx
import logging
from typing import Dict, Any, List
import json

logger = logging.getLogger(__name__)

class BrightlocalIntelligence:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://tools.brightlocal.com/seo-tools/api/v4"
        
    async def get_local_seo_analysis(self, business_type: str, location: str) -> Dict[str, Any]:
        """Get local SEO analysis for business type and location"""
        try:
            # Search for local businesses
            search_params = {
                "api-key": self.api_key,
                "q": f"{business_type} {location}",
                "type": "local",
                "limit": 20
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/local-search-results",
                    params=search_params
                )
                
                if response.status_code == 200:
                    data = response.json()
                    results = data.get("results", [])
                    
                    # Analyze local SEO data
                    analysis = self._analyze_local_seo(results, business_type)
                    
                    return {
                        "success": True,
                        "total_results": len(results),
                        "analysis": analysis,
                        "top_competitors": results[:5]
                    }
                else:
                    logger.error(f"Brightlocal API error: {response.status_code}")
                    return {"success": False, "error": f"API error: {response.status_code}"}
                    
        except Exception as e:
            logger.error(f"Brightlocal analysis error: {e}")
            return {"success": False, "error": str(e)}
    
    def _analyze_local_seo(self, results: List[Dict], business_type: str) -> Dict[str, Any]:
        """Analyze local SEO results for insights"""
        if not results:
            return {"insights": "No local SEO data found"}
        
        # Extract insights
        avg_rating = 0
        total_reviews = 0
        citation_sources = set()
        local_pack_presence = 0
        
        for result in results:
            # Rating analysis
            rating = result.get("rating", 0)
            reviews = result.get("review_count", 0)
            avg_rating += rating
            total_reviews += reviews
            
            # Citation analysis
            citations = result.get("citations", [])
            for citation in citations:
                citation_sources.add(citation.get("source", "unknown"))
            
            # Local pack presence
            if result.get("local_pack_position"):
                local_pack_presence += 1
        
        avg_rating = avg_rating / len(results) if results else 0
        
        return {
            "average_rating": round(avg_rating, 2),
            "total_reviews": total_reviews,
            "citation_sources": len(citation_sources),
            "local_pack_presence": local_pack_presence,
            "seo_competition_level": "High" if avg_rating > 4.0 else "Medium" if avg_rating > 3.5 else "Low",
            "insights": [
                f"Average competitor rating: {avg_rating:.1f}⭐",
                f"Total reviews in market: {total_reviews:,}",
                f"Citation sources: {len(citation_sources)}",
                f"Local pack presence: {local_pack_presence}/{len(results)} businesses"
            ]
        }

# Integration function for BOT system
async def get_brightlocal_intelligence(business_type: str, location: str) -> Dict[str, Any]:
    """Get Brightlocal intelligence for business analysis"""
    brightlocal = BrightlocalIntelligence(
        api_key="2efdc9f13ec8a5b8fc0d83cddba7f5cc671ca3ec"
    )
    
    return await brightlocal.get_local_seo_analysis(business_type, location)
