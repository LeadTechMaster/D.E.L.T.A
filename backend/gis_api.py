"""
D.E.L.T.A GIS API - Census Tract Overlap Calculator

This Flask API calculates which Census tracts overlap with a user-drawn polygon
and returns weighted demographics data.

Endpoints:
    POST /api/v1/gis/calculate-tracts
        Input: { "polygon": [[lat, lng], [lat, lng], ...] }
        Output: { "tracts": [{"tractId": "123", "overlap": 0.75}, ...], "demographics": {...} }

Requirements:
    - geopandas
    - shapely
    - requests
    - flask
    - flask-cors
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import geopandas as gpd
from shapely.geometry import Polygon as ShapelyPolygon, Point
import requests
import json
import os
import tempfile

app = Flask(__name__)
CORS(app)

# Cache directory for Census tract data
CACHE_DIR = os.path.join(tempfile.gettempdir(), 'delta_gis_cache')
os.makedirs(CACHE_DIR, exist_ok=True)

# Census API configuration
CENSUS_API_KEY = "ab4c49e507688c08e5346543c6d355a2e6b37c8c"
NODE_API_URL = "http://localhost:8001"

def load_census_tracts(state_fips="06", county_fips="075"):
    """
    Load Census tracts for a given state/county.
    Defaults to San Francisco County (state=06, county=075)
    
    Caches the shapefile locally to avoid repeated downloads.
    """
    cache_file = os.path.join(CACHE_DIR, f'tracts_{state_fips}_{county_fips}.geojson')
    
    # Check cache
    if os.path.exists(cache_file):
        print(f"Loading tracts from cache: {cache_file}")
        return gpd.read_file(cache_file)
    
    # Download from Census TIGER/Line
    url = f"https://www2.census.gov/geo/tiger/TIGER2023/TRACT/tl_2023_{state_fips}_tract.zip"
    print(f"Downloading Census tracts from: {url}")
    
    try:
        # Read directly from URL
        tracts = gpd.read_file(url)
        
        # Filter to specific county
        tracts = tracts[tracts['COUNTYFP'] == county_fips]
        
        # Save to cache
        tracts.to_file(cache_file, driver='GeoJSON')
        print(f"Cached {len(tracts)} tracts")
        
        return tracts
    except Exception as e:
        print(f"Error loading tracts: {e}")
        return None

def calculate_tract_overlaps(polygon_coords, state_fips="06", county_fips="075"):
    """
    Calculate which Census tracts overlap with the given polygon.
    
    Args:
        polygon_coords: List of [lat, lng] coordinates
        state_fips: State FIPS code (default: California = 06)
        county_fips: County FIPS code (default: San Francisco = 075)
    
    Returns:
        List of dicts: [{"tractId": "123400", "geoid": "06075123400", "overlap": 0.75}, ...]
    """
    try:
        # Load Census tracts
        tracts = load_census_tracts(state_fips, county_fips)
        if tracts is None or len(tracts) == 0:
            return {"error": "Failed to load Census tracts"}
        
        # Create polygon from coordinates (note: coordinates are [lat, lng] but shapely uses [lng, lat])
        polygon_points = [(lng, lat) for lat, lng in polygon_coords]
        polygon = ShapelyPolygon(polygon_points)
        
        # Create GeoDataFrame with the drawn polygon
        polygon_gdf = gpd.GeoDataFrame([1], geometry=[polygon], crs="EPSG:4326")
        
        # Reproject to projected CRS for accurate area calculation
        # California State Plane Zone 3 (NAD83) - EPSG:26943
        target_crs = "EPSG:26943"
        polygon_proj = polygon_gdf.to_crs(target_crs)
        tracts_proj = tracts.to_crs(target_crs)
        
        # Calculate overlaps
        overlaps = []
        for idx, tract in tracts_proj.iterrows():
            tract_geom = tract.geometry
            polygon_geom = polygon_proj.geometry.iloc[0]
            
            # Calculate intersection
            if tract_geom.intersects(polygon_geom):
                intersection = tract_geom.intersection(polygon_geom)
                overlap_area = intersection.area
                total_area = tract_geom.area
                
                if total_area > 0:
                    overlap_pct = overlap_area / total_area
                    
                    # Only include tracts with > 1% overlap
                    if overlap_pct > 0.01:
                        overlaps.append({
                            'tractId': tract['TRACTCE'],
                            'geoid': tract['GEOID'],
                            'overlap': round(overlap_pct, 4),
                            'overlap_pct': f"{overlap_pct*100:.1f}%"
                        })
        
        # Sort by overlap percentage (highest first)
        overlaps.sort(key=lambda x: x['overlap'], reverse=True)
        
        return overlaps
        
    except Exception as e:
        print(f"Error calculating overlaps: {e}")
        import traceback
        traceback.print_exc()
        return {"error": str(e)}

def fetch_tract_demographics(geoid):
    """
    Fetch demographics for a specific Census tract from the Node.js backend.
    """
    try:
        # Use the existing Node.js API endpoint
        # Note: Need to add this endpoint to real_api_server_final.js
        response = requests.get(f"{NODE_API_URL}/api/v1/census/tract-demographics?geoid={geoid}", timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if data.get('status') == 'success':
                return data['data']
        
        # Fallback: Return None if endpoint doesn't exist yet
        return None
        
    except Exception as e:
        print(f"Error fetching tract demographics: {e}")
        return None

def calculate_weighted_demographics(tract_overlaps):
    """
    Calculate population-weighted demographics based on tract overlaps.
    
    Args:
        tract_overlaps: List of {"geoid": "...", "overlap": 0.75, ...}
    
    Returns:
        Aggregated demographics dict
    """
    total_weighted_pop = 0
    weighted_income_sum = 0
    weighted_home_value_sum = 0
    
    tract_details = []
    
    for tract in tract_overlaps:
        geoid = tract['geoid']
        overlap = tract['overlap']
        
        # Fetch demographics for this tract
        demo = fetch_tract_demographics(geoid)
        
        if demo:
            pop = demo.get('total_population', 0)
            income = demo.get('median_household_income', 0)
            home_value = demo.get('median_home_value', 0)
            
            # Weight by overlap percentage
            weighted_pop = pop * overlap
            total_weighted_pop += weighted_pop
            
            weighted_income_sum += income * weighted_pop
            weighted_home_value_sum += home_value * weighted_pop
            
            tract_details.append({
                'geoid': geoid,
                'tractId': tract['tractId'],
                'overlap': tract['overlap'],
                'population': pop,
                'income': income,
                'home_value': home_value
            })
    
    # Calculate weighted averages
    if total_weighted_pop > 0:
        avg_income = round(weighted_income_sum / total_weighted_pop)
        avg_home_value = round(weighted_home_value_sum / total_weighted_pop)
    else:
        avg_income = 0
        avg_home_value = 0
    
    return {
        'total_population': round(total_weighted_pop),
        'median_household_income': avg_income,
        'median_home_value': avg_home_value,
        'tract_count': len(tract_overlaps),
        'tract_details': tract_details,
        'data_source': 'US Census Bureau (Tract-weighted)'
    }

@app.route('/api/v1/gis/calculate-tracts', methods=['POST'])
def calculate_tracts():
    """
    Calculate Census tract overlaps for a drawn polygon.
    
    Expected JSON body:
    {
        "polygon": [[37.7749, -122.4194], [37.7849, -122.4094], ...],
        "state_fips": "06",  // Optional, defaults to CA
        "county_fips": "075"  // Optional, defaults to SF
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'polygon' not in data:
            return jsonify({
                'status': 'error',
                'error': 'Missing polygon coordinates. Expected: {"polygon": [[lat, lng], ...]}'
            }), 400
        
        polygon_coords = data['polygon']
        state_fips = data.get('state_fips', '06')  # Default to California
        county_fips = data.get('county_fips', '075')  # Default to San Francisco
        
        # Validate polygon
        if len(polygon_coords) < 3:
            return jsonify({
                'status': 'error',
                'error': 'Polygon must have at least 3 points'
            }), 400
        
        print(f"Calculating tract overlaps for polygon with {len(polygon_coords)} points")
        
        # Calculate overlaps
        tract_overlaps = calculate_tract_overlaps(polygon_coords, state_fips, county_fips)
        
        if isinstance(tract_overlaps, dict) and 'error' in tract_overlaps:
            return jsonify({
                'status': 'error',
                'error': tract_overlaps['error']
            }), 500
        
        # Calculate weighted demographics
        demographics = calculate_weighted_demographics(tract_overlaps)
        
        return jsonify({
            'status': 'success',
            'data': {
                'tracts': tract_overlaps,
                'demographics': demographics
            }
        })
        
    except Exception as e:
        print(f"Error in calculate_tracts endpoint: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'status': 'error',
            'error': str(e)
        }), 500

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({'status': 'ok', 'service': 'D.E.L.T.A GIS API'})

if __name__ == '__main__':
    print("=" * 70)
    print("🗺️  D.E.L.T.A GIS API Starting...")
    print("=" * 70)
    print(f"📁 Cache directory: {CACHE_DIR}")
    print(f"🔗 Node.js API: {NODE_API_URL}")
    print(f"🌐 Starting Flask server on http://localhost:5001")
    print("=" * 70)
    
    app.run(host='0.0.0.0', port=5001, debug=True)

