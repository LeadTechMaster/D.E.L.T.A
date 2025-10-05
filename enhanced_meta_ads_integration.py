#!/usr/bin/env python3
"""
🔍 Enhanced Meta Ads Integration
Adds competitor ad analysis and market intelligence
"""

import httpx
import logging
from typing import Dict, Any, List
import json

logger = logging.getLogger(__name__)

class MetaAdsIntelligence:
    def __init__(self, access_token: str, app_token: str):
        self.access_token = access_token
        self.app_token = app_token
        self.base_url = "https://graph.facebook.com/v18.0"
        
    async def get_competitor_ads(self, business_type: str, location: str) -> Dict[str, Any]:
        """Get competitor ads for business type and location"""
        try:
            # Search for ads related to business type in location
            search_params = {
                "access_token": self.access_token,
                "search_terms": f"{business_type} {location}",
                "ad_reached_countries": ["US"],
                "ad_active_status": "ACTIVE",
                "limit": 50
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/ads_archive",
                    params=search_params
                )
                
                if response.status_code == 200:
                    data = response.json()
                    ads = data.get("data", [])
                    
                    # Analyze ad data
                    analysis = self._analyze_ads(ads, business_type)
                    
                    return {
                        "success": True,
                        "total_ads": len(ads),
                        "analysis": analysis,
                        "sample_ads": ads[:5]  # First 5 ads for reference
                    }
                else:
                    logger.error(f"Meta Ads API error: {response.status_code}")
                    return {"success": False, "error": f"API error: {response.status_code}"}
                    
        except Exception as e:
            logger.error(f"Meta Ads analysis error: {e}")
            return {"success": False, "error": str(e)}
    
    def _analyze_ads(self, ads: List[Dict], business_type: str) -> Dict[str, Any]:
        """Analyze competitor ads for insights"""
        if not ads:
            return {"insights": "No competitor ads found"}
        
        # Extract insights
        platforms = {}
        ad_types = {}
        estimated_spend = 0
        
        for ad in ads:
            # Platform analysis
            platform = ad.get("publisher_platform", "unknown")
            platforms[platform] = platforms.get(platform, 0) + 1
            
            # Ad type analysis
            ad_type = ad.get("ad_creative_bodies", [{}])[0].get("text", "")
            if "sale" in ad_type.lower():
                ad_types["sales"] = ad_types.get("sales", 0) + 1
            elif "new" in ad_type.lower():
                ad_types["new_business"] = ad_types.get("new_business", 0) + 1
            elif "promotion" in ad_type.lower():
                ad_types["promotions"] = ad_types.get("promotions", 0) + 1
            
            # Estimate spend (rough calculation)
            impressions = ad.get("impressions", {}).get("lower_bound", 0)
            estimated_spend += impressions * 0.01  # Rough estimate
        
        return {
            "platform_distribution": platforms,
            "ad_type_analysis": ad_types,
            "estimated_competitor_spend": round(estimated_spend, 2),
            "market_activity": "High" if len(ads) > 20 else "Medium" if len(ads) > 10 else "Low",
            "insights": [
                f"Most ads on {max(platforms.keys(), key=platforms.get)} platform",
                f"Estimated competitor ad spend: ${estimated_spend:.0f}",
                f"Market activity level: {'High' if len(ads) > 20 else 'Medium' if len(ads) > 10 else 'Low'}"
            ]
        }

# Integration function for BOT system
async def get_meta_ads_intelligence(business_type: str, location: str) -> Dict[str, Any]:
    """Get Meta Ads intelligence for business analysis"""
    meta_ads = MetaAdsIntelligence(
        access_token="EAA40mj0BFQYBPXUVZAWCEv0ZBFOXjEmLUd3o26dfD1yzBbCg6PodDpKvYZA4O4WZBHIag9fcUxrmTtUwtzmDICOSJua4YrlSDjyDYI5JcsKfWKbHP2ZCRutPaq069nmN2hzCx3R6R6M1vniJ6x2RYU79cdBiyluoLkp3U4OdqmV6yOOujAGdMKCn0LPBAEUboIgZDZD",
        app_token="3998486727038214|Y7kOLPL2Wy8hridK2rO05qJmxRc"
    )
    
    return await meta_ads.get_competitor_ads(business_type, location)
