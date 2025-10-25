"""
D.E.L.T.A Individual Heatmap API Endpoints
Each endpoint returns GeoJSON with distinct scoring for real-time heatmap generation
"""

from fastapi import APIRouter, HTTPException, Query
from typing import Dict, List, Any, Optional
import asyncio
import logging
from .heatmap_scorers import HeatmapScorers

logger = logging.getLogger(__name__)

# Create router for individual heatmap endpoints
router = APIRouter(prefix="/api/v1/heatmap", tags=["heatmap-individual"])

@router.get("/business_competition")
async def get_business_competition_heatmap(
    lat: float = Query(..., description="Center latitude"),
    lng: float = Query(..., description="Center longitude"),
    radius_km: float = Query(5.0, description="Search radius in kilometers"),
    business_type: str = Query("coffee shop", description="Target business type")
):
    """
    Get business competition heatmap data with distinct scoring
    """
    try:
        logger.info(f"🏢 Generating business competition heatmap for {business_type} at ({lat}, {lng})")
        
        # Fetch real business data and apply DRAMATIC scoring
        businesses = await _fetch_businesses_near_location(lat, lng, radius_km, business_type)
        
        # Convert to GeoJSON with DRAMATIC distinct scoring
        features = []
        for business in businesses:
            # Calculate distinct competition score with DRAMATIC differences
            poi_data = {
                'rating': business.get('rating', 0),
                'user_ratings_total': business.get('user_ratings_total', 0),
                'category_match': HeatmapScorers.calculate_category_match(
                    business_type, 
                    business.get('types', [])
                ),
                'is_brand': business.get('is_brand', False)
            }
            
            # Apply DRAMATIC competition scoring
            weight = HeatmapScorers.competition_score(poi_data)
            
            features.append({
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [business['coordinates']['longitude'], business['coordinates']['latitude']]
                },
                "properties": {
                    "weight": weight,
                    "rating": business.get('rating', 0),
                    "review_count": business.get('user_ratings_total', 0),
                    "name": business.get('name', ''),
                    "address": business.get('address', ''),
                    "price_level": business.get('price_level', 0),
                    "types": business.get('types', [])
                }
            })
        
        return {
            "type": "FeatureCollection",
            "features": features,
            "layer_id": "business_competition",
            "total_points": len(features),
            "scoring_method": "competition_score"
        }
        
    except Exception as e:
        logger.error(f"❌ Business competition heatmap error: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to generate business competition heatmap: {str(e)}")

@router.get("/review_power")
async def get_review_power_heatmap(
    lat: float = Query(..., description="Center latitude"),
    lng: float = Query(..., description="Center longitude"),
    radius_km: float = Query(5.0, description="Search radius in kilometers"),
    business_type: str = Query("coffee shop", description="Target business type")
):
    """
    Get review power heatmap data with distinct scoring
    """
    try:
        logger.info(f"⭐ Generating review power heatmap for {business_type} at ({lat}, {lng})")
        
        businesses = await _fetch_businesses_near_location(lat, lng, radius_km, business_type)
        
        features = []
        for business in businesses:
            # Calculate distinct review power score
            poi_data = {
                'rating': business.get('rating', 0),
                'user_ratings_total': business.get('user_ratings_total', 0)
            }
            
            weight = HeatmapScorers.review_power_score(poi_data)
            
            features.append({
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [business['coordinates']['longitude'], business['coordinates']['latitude']]
                },
                "properties": {
                    "weight": weight,
                    "rating": business.get('rating', 0),
                    "review_count": business.get('user_ratings_total', 0),
                    "name": business.get('name', '')
                }
            })
        
        return {
            "type": "FeatureCollection",
            "features": features,
            "layer_id": "review_power",
            "total_points": len(features),
            "scoring_method": "review_power_score"
        }
        
    except Exception as e:
        logger.error(f"❌ Review power heatmap error: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to generate review power heatmap: {str(e)}")

@router.get("/demographics_density")
async def get_demographics_density_heatmap(
    lat: float = Query(..., description="Center latitude"),
    lng: float = Query(..., description="Center longitude"),
    radius_km: float = Query(5.0, description="Search radius in kilometers")
):
    """
    Get demographic density heatmap data with distinct scoring
    """
    try:
        logger.info(f"👥 Generating demographic density heatmap at ({lat}, {lng})")
        
        # Fetch demographic data (this would integrate with your Census API)
        demographics = await _fetch_demographics_data(lat, lng, radius_km)
        
        features = []
        # Create grid points around the center
        grid_size = 8
        for i in range(grid_size):
            for j in range(grid_size):
                # Calculate position in grid
                lat_offset = (i - grid_size/2) * (radius_km * 0.1)
                lng_offset = (j - grid_size/2) * (radius_km * 0.1)
                
                point_lat = lat + lat_offset
                point_lng = lng + lng_offset
                
                # Calculate distinct demographic score
                weight = HeatmapScorers.demographics_score(demographics)
                
                features.append({
                    "type": "Feature",
                    "geometry": {
                        "type": "Point",
                        "coordinates": [point_lng, point_lat]
                    },
                    "properties": {
                        "weight": weight,
                        "population_density": demographics.get('population_density', 0),
                        "education_ratio": demographics.get('bachelor_plus_ratio', 0),
                        "median_age": demographics.get('median_age', 35)
                    }
                })
        
        return {
            "type": "FeatureCollection",
            "features": features,
            "layer_id": "demographics_density",
            "total_points": len(features),
            "scoring_method": "demographics_score"
        }
        
    except Exception as e:
        logger.error(f"❌ Demographics density heatmap error: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to generate demographics density heatmap: {str(e)}")

@router.get("/income_wealth")
async def get_income_wealth_heatmap(
    lat: float = Query(..., description="Center latitude"),
    lng: float = Query(..., description="Center longitude"),
    radius_km: float = Query(5.0, description="Search radius in kilometers")
):
    """
    Get income & wealth heatmap data with distinct scoring
    """
    try:
        logger.info(f"💰 Generating income & wealth heatmap at ({lat}, {lng})")
        
        demographics = await _fetch_demographics_data(lat, lng, radius_km)
        
        features = []
        grid_size = 8
        for i in range(grid_size):
            for j in range(grid_size):
                lat_offset = (i - grid_size/2) * (radius_km * 0.1)
                lng_offset = (j - grid_size/2) * (radius_km * 0.1)
                
                point_lat = lat + lat_offset
                point_lng = lng + lng_offset
                
                # Calculate distinct income & wealth score
                weight = HeatmapScorers.income_wealth_score(demographics)
                
                features.append({
                    "type": "Feature",
                    "geometry": {
                        "type": "Point",
                        "coordinates": [point_lng, point_lat]
                    },
                    "properties": {
                        "weight": weight,
                        "median_income": demographics.get('median_household_income', 0),
                        "education_ratio": demographics.get('bachelor_plus_ratio', 0)
                    }
                })
        
        return {
            "type": "FeatureCollection",
            "features": features,
            "layer_id": "income_wealth",
            "total_points": len(features),
            "scoring_method": "income_wealth_score"
        }
        
    except Exception as e:
        logger.error(f"❌ Income & wealth heatmap error: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to generate income & wealth heatmap: {str(e)}")

@router.get("/opportunity")
async def get_opportunity_heatmap(
    lat: float = Query(..., description="Center latitude"),
    lng: float = Query(..., description="Center longitude"),
    radius_km: float = Query(5.0, description="Search radius in kilometers"),
    business_type: str = Query("coffee shop", description="Target business type")
):
    """
    Get market opportunity heatmap data with distinct scoring
    """
    try:
        logger.info(f"🎯 Generating market opportunity heatmap for {business_type} at ({lat}, {lng})")
        
        # Fetch both demographics and competition data
        demographics = await _fetch_demographics_data(lat, lng, radius_km)
        businesses = await _fetch_businesses_near_location(lat, lng, radius_km, business_type)
        
        # Calculate competition density
        competition_density = len(businesses) / (radius_km * radius_km * 3.14159)  # businesses per km²
        
        features = []
        grid_size = 8
        for i in range(grid_size):
            for j in range(grid_size):
                lat_offset = (i - grid_size/2) * (radius_km * 0.1)
                lng_offset = (j - grid_size/2) * (radius_km * 0.1)
                
                point_lat = lat + lat_offset
                point_lng = lng + lng_offset
                
                # Calculate distinct opportunity score
                weight = HeatmapScorers.opportunity_score(demographics, competition_density)
                
                features.append({
                    "type": "Feature",
                    "geometry": {
                        "type": "Point",
                        "coordinates": [point_lng, point_lat]
                    },
                    "properties": {
                        "weight": weight,
                        "demand_score": HeatmapScorers.demographics_score(demographics),
                        "competition_density": competition_density,
                        "opportunity_level": "high" if weight > 0.7 else "medium" if weight > 0.4 else "low"
                    }
                })
        
        return {
            "type": "FeatureCollection",
            "features": features,
            "layer_id": "opportunity",
            "total_points": len(features),
            "scoring_method": "opportunity_score"
        }
        
    except Exception as e:
        logger.error(f"❌ Market opportunity heatmap error: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to generate market opportunity heatmap: {str(e)}")

@router.get("/foot_traffic")
async def get_foot_traffic_heatmap(
    lat: float = Query(..., description="Center latitude"),
    lng: float = Query(..., description="Center longitude"),
    radius_km: float = Query(5.0, description="Search radius in kilometers")
):
    """
    Get foot traffic heatmap data with distinct scoring
    """
    try:
        logger.info(f"🚶 Generating foot traffic heatmap at ({lat}, {lng})")
        
        # Fetch various POI types for foot traffic analysis
        businesses = await _fetch_businesses_near_location(lat, lng, radius_km, "all")
        
        # Categorize businesses for foot traffic analysis
        cell_data = {
            'transit_count': 0,
            'cafe_count': 0,
            'attraction_count': 0,
            'mall_count': 0
        }
        
        for business in businesses:
            types = business.get('types', [])
            if any(t in ['transit_station', 'subway_station', 'bus_station'] for t in types):
                cell_data['transit_count'] += 1
            elif any(t in ['cafe', 'coffee', 'restaurant'] for t in types):
                cell_data['cafe_count'] += 1
            elif any(t in ['tourist_attraction', 'museum', 'park'] for t in types):
                cell_data['attraction_count'] += 1
            elif any(t in ['shopping_mall', 'store'] for t in types):
                cell_data['mall_count'] += 1
        
        features = []
        grid_size = 8
        for i in range(grid_size):
            for j in range(grid_size):
                lat_offset = (i - grid_size/2) * (radius_km * 0.1)
                lng_offset = (j - grid_size/2) * (radius_km * 0.1)
                
                point_lat = lat + lat_offset
                point_lng = lng + lng_offset
                
                # Calculate distinct foot traffic score
                weight = HeatmapScorers.foot_traffic_score(cell_data)
                
                features.append({
                    "type": "Feature",
                    "geometry": {
                        "type": "Point",
                        "coordinates": [point_lng, point_lat]
                    },
                    "properties": {
                        "weight": weight,
                        "transit_count": cell_data['transit_count'],
                        "cafe_count": cell_data['cafe_count'],
                        "attraction_count": cell_data['attraction_count'],
                        "mall_count": cell_data['mall_count']
                    }
                })
        
        return {
            "type": "FeatureCollection",
            "features": features,
            "layer_id": "foot_traffic",
            "total_points": len(features),
            "scoring_method": "foot_traffic_score"
        }
        
    except Exception as e:
        logger.error(f"❌ Foot traffic heatmap error: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to generate foot traffic heatmap: {str(e)}")

# Helper functions (integrated with existing APIs)
async def _fetch_businesses_near_location(lat: float, lng: float, radius_km: float, business_type: str) -> List[Dict[str, Any]]:
    """Fetch businesses near location using existing Google Places API"""
    import httpx
    
    # Convert km to meters
    radius_meters = int(radius_km * 1000)
    
    # Use Google Places API
    url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
    params = {
        "query": f"{business_type} in {lat},{lng}",
        "location": f"{lat},{lng}",
        "radius": radius_meters,
        "key": "AIzaSyAzyKYxbA7HWHTU9UV9Z-ELGRQTTeN9dkw"
    }
    
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.get(url, params=params)
            data = response.json()
            
            businesses = []
            if data.get("results"):
                for place in data["results"]:
                    businesses.append({
                        "name": place.get("name", ""),
                        "address": place.get("formatted_address", ""),
                        "rating": place.get("rating", 0),
                        "user_ratings_total": place.get("user_ratings_total", 0),
                        "price_level": place.get("price_level", 0),
                        "types": place.get("types", []),
                        "coordinates": {
                            "latitude": place["geometry"]["location"]["lat"],
                            "longitude": place["geometry"]["location"]["lng"]
                        },
                        "place_id": place.get("place_id", "")
                    })
            
            return businesses
    except Exception as e:
        logger.error(f"Error fetching businesses: {e}")
        return []

async def _fetch_demographics_data(lat: float, lng: float, radius_km: float) -> Dict[str, Any]:
    """Fetch demographic data using existing Census API"""
    import httpx
    
    # For now, use Florida state data (FIPS code 12)
    # In a real implementation, you'd geocode to get the specific county/tract
    url = "https://api.census.gov/data/2021/acs/acs5"
    params = {
        "get": "NAME,B01001_001E,B01001_002E,B01001_026E,B19013_001E,B08301_001E,B08301_002E,B08301_010E,B15003_001E,B15003_022E,B15003_023E,B15003_024E,B15003_025E",
        "for": "state:12",  # Florida
        "key": "ab4c49e507688c08e5346543c6d355a2e6b37c8c"
    }
    
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.get(url, params=params)
            data = response.json()
            
            if len(data) > 1:
                row = data[1]
                total_pop = int(row[1]) if row[1] else 0
                median_income = int(row[4]) if row[4] else 0
                education_total = int(row[8]) if row[8] else 0
                bachelors = int(row[9]) if row[9] else 0
                
                return {
                    'population_density': total_pop / 1000,  # Approximate per km²
                    'median_household_income': median_income,
                    'bachelor_plus_ratio': bachelors / max(education_total, 1),
                    'median_age': 35  # Default reasonable value
                }
    except Exception as e:
        logger.error(f"Error fetching demographics: {e}")
    
    # Fallback data
    return {
        'population_density': 1000,
        'median_household_income': 75000,
        'bachelor_plus_ratio': 0.4,
        'median_age': 35
    }
