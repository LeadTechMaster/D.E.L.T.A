"""
D.E.L.T.A Heatmap API Endpoints
FastAPI endpoints for intelligent heatmap generation
"""

import asyncio
import logging
from typing import Dict, List, Any, Optional
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel

from .heatmap_engine import IntelligentHeatmapEngine, HeatmapType
from .heatmap_config import HeatmapConfig, HeatmapButtonConfig

logger = logging.getLogger(__name__)

# Create router for heatmap endpoints
router = APIRouter(prefix="/api/v1/heatmap", tags=["heatmap"])

# Global heatmap engine instance
heatmap_engine: Optional[IntelligentHeatmapEngine] = None

def get_heatmap_engine(api_client):
    """Get or create heatmap engine instance"""
    global heatmap_engine
    if heatmap_engine is None:
        heatmap_engine = IntelligentHeatmapEngine(api_client)
    return heatmap_engine

class HeatmapRequest(BaseModel):
    """Request model for heatmap generation"""
    businesses: List[Dict[str, Any]]
    demographics: Dict[str, Any]
    location_data: Dict[str, Any]
    business_type: str
    layer_types: Optional[List[str]] = None

class HeatmapResponse(BaseModel):
    """Response model for heatmap data"""
    status: str
    layers: Dict[str, Dict[str, Any]]
    available_layers: List[Dict[str, Any]]
    total_points: int
    timestamp: str

@router.post("/generate", response_model=HeatmapResponse)
async def generate_intelligent_heatmap(
    request: HeatmapRequest,
    api_client = None
):
    """
    Generate intelligent heatmap layers based on business and demographic data
    """
    try:
        logger.info(f"🔥 Generating intelligent heatmap for {request.business_type}")
        
        # Get heatmap engine
        engine = get_heatmap_engine(api_client)
        
        # Generate all heatmap layers
        layers = await engine.generate_all_heatmap_layers(
            businesses=request.businesses,
            demographics=request.demographics,
            location_data=request.location_data,
            business_type=request.business_type
        )
        
        # Convert layers to GeoJSON format
        geojson_layers = {}
        total_points = 0
        
        for layer_id, layer in layers.items():
            geojson_data = engine.get_layer_geojson(layer_id)
            geojson_layers[layer_id] = geojson_data
            total_points += len(layer.points)
        
        # Get available layers info
        available_layers = engine.get_available_layers()
        
        response = HeatmapResponse(
            status="success",
            layers=geojson_layers,
            available_layers=available_layers,
            total_points=total_points,
            timestamp=str(asyncio.get_event_loop().time())
        )
        
        logger.info(f"✅ Generated {len(layers)} heatmap layers with {total_points} total points")
        return response
        
    except Exception as e:
        logger.error(f"❌ Heatmap generation error: {e}")
        raise HTTPException(status_code=500, detail=f"Heatmap generation failed: {str(e)}")

@router.get("/layers/{layer_id}")
async def get_heatmap_layer(
    layer_id: str,
    api_client = None
):
    """
    Get specific heatmap layer data
    """
    try:
        engine = get_heatmap_engine(api_client)
        
        if layer_id not in engine.layers:
            raise HTTPException(status_code=404, detail=f"Layer {layer_id} not found")
        
        geojson_data = engine.get_layer_geojson(layer_id)
        
        return {
            "status": "success",
            "layer_id": layer_id,
            "data": geojson_data,
            "timestamp": str(asyncio.get_event_loop().time())
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Error getting layer {layer_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get layer: {str(e)}")

@router.get("/available-layers")
async def get_available_layers(api_client = None):
    """
    Get list of available heatmap layers
    """
    try:
        engine = get_heatmap_engine(api_client)
        available_layers = engine.get_available_layers()
        
        return {
            "status": "success",
            "layers": available_layers,
            "timestamp": str(asyncio.get_event_loop().time())
        }
        
    except Exception as e:
        logger.error(f"❌ Error getting available layers: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get available layers: {str(e)}")

@router.get("/buttons")
async def get_heatmap_buttons():
    """
    Get heatmap control button configurations
    """
    try:
        buttons = HeatmapButtonConfig.get_all_buttons()
        
        return {
            "status": "success",
            "buttons": buttons,
            "timestamp": str(asyncio.get_event_loop().time())
        }
        
    except Exception as e:
        logger.error(f"❌ Error getting heatmap buttons: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get heatmap buttons: {str(e)}")

@router.get("/config/{layer_type}")
async def get_heatmap_config(layer_type: str):
    """
    Get heatmap configuration for specific layer type
    """
    try:
        # Get button config
        button_config = HeatmapButtonConfig.get_button_config(layer_type)
        
        # Get Mapbox config
        mapbox_config = HeatmapConfig.get_mapbox_heatmap_config(
            layer_type, 
            button_config["color_scheme"]
        )
        
        return {
            "status": "success",
            "layer_type": layer_type,
            "button_config": button_config,
            "mapbox_config": mapbox_config,
            "timestamp": str(asyncio.get_event_loop().time())
        }
        
    except Exception as e:
        logger.error(f"❌ Error getting config for {layer_type}: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get config: {str(e)}")

@router.post("/analyze-opportunity")
async def analyze_market_opportunity(
    center_lat: float = Query(..., description="Center latitude"),
    center_lng: float = Query(..., description="Center longitude"),
    radius_miles: float = Query(5.0, description="Analysis radius in miles"),
    business_type: str = Query(..., description="Business type to analyze"),
    api_client = None
):
    """
    Analyze market opportunity and generate heatmap data
    """
    try:
        logger.info(f"🎯 Analyzing market opportunity for {business_type} at ({center_lat}, {center_lng})")
        
        # Get businesses in area
        places_result = await api_client.search_places(
            query=business_type,
            location=f"{center_lat},{center_lng}"
        )
        
        if not places_result["success"]:
            raise HTTPException(status_code=500, detail="Failed to get business data")
        
        businesses = places_result.get("data", {}).get("businesses", [])
        
        # Get demographics (using state code for now)
        demo_result = await api_client.get_demographics("53")  # Washington state
        
        demographics = {}
        if demo_result["success"]:
            demographics = demo_result.get("demographics", {})
        
        # Prepare location data
        location_data = {
            "latitude": center_lat,
            "longitude": center_lng,
            "radius_miles": radius_miles
        }
        
        # Generate heatmap layers
        engine = get_heatmap_engine(api_client)
        layers = await engine.generate_all_heatmap_layers(
            businesses=businesses,
            demographics=demographics,
            location_data=location_data,
            business_type=business_type
        )
        
        # Convert to response format
        response_layers = {}
        for layer_id, layer in layers.items():
            response_layers[layer_id] = engine.get_layer_geojson(layer_id)
        
        return {
            "status": "success",
            "business_type": business_type,
            "location": location_data,
            "business_count": len(businesses),
            "layers": response_layers,
            "analysis": {
                "total_competitors": len(businesses),
                "demographic_data_available": bool(demographics),
                "layers_generated": len(layers)
            },
            "timestamp": str(asyncio.get_event_loop().time())
        }
        
    except Exception as e:
        logger.error(f"❌ Market opportunity analysis error: {e}")
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

@router.get("/health")
async def heatmap_health_check():
    """
    Health check for heatmap service
    """
    return {
        "status": "healthy",
        "service": "intelligent_heatmap",
        "version": "1.0.0",
        "features": [
            "business_competition_analysis",
            "demographic_density_mapping", 
            "foot_traffic_analysis",
            "market_opportunity_mapping",
            "multi_layer_visualization",
            "intelligent_data_logic"
        ],
        "timestamp": str(asyncio.get_event_loop().time())
    }



