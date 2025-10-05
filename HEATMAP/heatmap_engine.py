"""
D.E.L.T.A Intelligent Heatmap Engine
Advanced multi-layer heatmap system with smart data logic
"""

import asyncio
import logging
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import math

logger = logging.getLogger(__name__)

class HeatmapType(Enum):
    """Different types of heatmaps based on data logic"""
    BUSINESS_COMPETITION = "business_competition"
    DEMOGRAPHIC_DENSITY = "demographic_density"
    FOOT_TRAFFIC = "foot_traffic"
    MARKET_OPPORTUNITY = "market_opportunity"
    INCOME_WEALTH = "income_wealth"
    REVIEW_POWER = "review_power"
    POPULATION_DENSITY = "population_density"
    EDUCATION_LEVEL = "education_level"
    COMMUTE_PATTERNS = "commute_patterns"

@dataclass
class HeatmapPoint:
    """Individual heatmap data point"""
    latitude: float
    longitude: float
    intensity: float  # 0.0 to 1.0
    weight: float     # For Mapbox heatmap weight
    data_type: str
    metadata: Dict[str, Any]

@dataclass
class HeatmapLayer:
    """Complete heatmap layer with points and configuration"""
    layer_id: str
    heatmap_type: HeatmapType
    points: List[HeatmapPoint]
    color_scheme: str
    radius_config: Dict[str, Any]
    intensity_config: Dict[str, Any]
    description: str

class IntelligentHeatmapEngine:
    """
    Advanced heatmap engine with multiple data layers and smart logic
    """
    
    def __init__(self, api_client):
        self.api_client = api_client
        self.layers: Dict[str, HeatmapLayer] = {}
        
    async def generate_business_competition_heatmap(self, businesses: List[Dict], location_data: Dict) -> HeatmapLayer:
        """
        Generate heatmap based on business competition logic:
        - More reviews = higher marketing power
        - Better ratings = higher customer satisfaction
        - Price level = market positioning
        """
        logger.info(f"🏢 Generating business competition heatmap for {len(businesses)} businesses")
        
        points = []
        for business in businesses:
            # Calculate marketing power based on reviews and ratings
            review_count = business.get('user_ratings_total', 0)
            rating = business.get('rating', 0)
            price_level = business.get('price_level', 0)
            
            # Marketing power logic: reviews * rating * price factor
            marketing_power = (review_count / 1000) * (rating / 5.0) * (1 + price_level * 0.2)
            marketing_power = min(marketing_power, 1.0)  # Cap at 1.0
            
            # Intensity based on marketing power
            intensity = marketing_power
            weight = review_count / 100  # Weight by review count
            
            point = HeatmapPoint(
                latitude=business['coordinates']['latitude'],
                longitude=business['coordinates']['longitude'],
                intensity=intensity,
                weight=max(weight, 1),
                data_type='business_competition',
                metadata={
                    'business_name': business.get('name', ''),
                    'rating': rating,
                    'review_count': review_count,
                    'price_level': price_level,
                    'marketing_power': marketing_power
                }
            )
            points.append(point)
        
        return HeatmapLayer(
            layer_id="business_competition",
            heatmap_type=HeatmapType.BUSINESS_COMPETITION,
            points=points,
            color_scheme="red_orange_yellow",  # Red = high competition
            radius_config={"min": 10, "max": 50, "zoom_factor": 1.5},
            intensity_config={"min": 0.5, "max": 3.0},
            description="Business competition intensity based on reviews, ratings, and market presence"
        )
    
    async def generate_demographic_density_heatmap(self, demographics: Dict, center_coords: Tuple[float, float]) -> HeatmapLayer:
        """
        Generate heatmap based on demographic density:
        - Population density = more people = higher intensity
        - Income level = spending power
        - Education level = market sophistication
        """
        logger.info("👥 Generating demographic density heatmap")
        
        points = []
        population = demographics.get('total_population', 0)
        income = demographics.get('median_household_income', 50000)
        education = demographics.get('education_data', {})
        
        # Create grid of demographic points around center
        center_lat, center_lng = center_coords
        grid_size = 20  # 20x20 grid
        
        for i in range(grid_size):
            for j in range(grid_size):
                # Calculate position in grid
                lat_offset = (i - grid_size/2) * 0.01  # 0.01 degree spacing
                lng_offset = (j - grid_size/2) * 0.01
                
                lat = center_lat + lat_offset
                lng = center_lng + lng_offset
                
                # Calculate demographic intensity
                population_factor = min(population / 1000000, 1.0)
                income_factor = min(income / 100000, 1.0)
                education_factor = min(education.get('bachelors_degree', 0) / 100000, 1.0)
                
                # Combined demographic intensity
                intensity = (population_factor * 0.4 + income_factor * 0.4 + education_factor * 0.2)
                
                point = HeatmapPoint(
                    latitude=lat,
                    longitude=lng,
                    intensity=intensity,
                    weight=intensity * 50,
                    data_type='demographic_density',
                    metadata={
                        'population': population,
                        'income': income,
                        'education_level': education_factor,
                        'demographic_score': intensity
                    }
                )
                points.append(point)
        
        return HeatmapLayer(
            layer_id="demographic_density",
            heatmap_type=HeatmapType.DEMOGRAPHIC_DENSITY,
            points=points,
            color_scheme="blue_green_yellow",  # Blue = high demographics
            radius_config={"min": 15, "max": 60, "zoom_factor": 2.0},
            intensity_config={"min": 0.8, "max": 2.5},
            description="Demographic density based on population, income, and education levels"
        )
    
    async def generate_foot_traffic_heatmap(self, businesses: List[Dict], demographics: Dict) -> HeatmapLayer:
        """
        Generate heatmap based on foot traffic logic:
        - More reviews = more foot traffic
        - Population density = potential foot traffic
        - Commute patterns = daily foot traffic
        """
        logger.info("🚶 Generating foot traffic heatmap")
        
        points = []
        commute_data = demographics.get('commute_data', {})
        total_commuters = commute_data.get('total_commuters', 0)
        public_transport = commute_data.get('public_transport', 0)
        
        for business in businesses:
            # Calculate foot traffic based on reviews and location
            review_count = business.get('user_ratings_total', 0)
            rating = business.get('rating', 0)
            
            # Foot traffic logic: reviews indicate visits, rating indicates satisfaction
            foot_traffic_score = (review_count / 500) * (rating / 5.0)
            foot_traffic_score = min(foot_traffic_score, 1.0)
            
            # Add commute influence
            commute_factor = min(total_commuters / 1000000, 1.0)
            public_transport_factor = min(public_transport / 100000, 1.0)
            
            # Combined foot traffic intensity
            intensity = foot_traffic_score * (1 + commute_factor * 0.3 + public_transport_factor * 0.2)
            intensity = min(intensity, 1.0)
            
            point = HeatmapPoint(
                latitude=business['coordinates']['latitude'],
                longitude=business['coordinates']['longitude'],
                intensity=intensity,
                weight=intensity * 75,
                data_type='foot_traffic',
                metadata={
                    'business_name': business.get('name', ''),
                    'foot_traffic_score': foot_traffic_score,
                    'commute_factor': commute_factor,
                    'public_transport_factor': public_transport_factor
                }
            )
            points.append(point)
        
        return HeatmapLayer(
            layer_id="foot_traffic",
            heatmap_type=HeatmapType.FOOT_TRAFFIC,
            points=points,
            color_scheme="purple_pink_red",  # Purple = high foot traffic
            radius_config={"min": 8, "max": 40, "zoom_factor": 1.8},
            intensity_config={"min": 0.6, "max": 2.8},
            description="Foot traffic intensity based on business reviews and commute patterns"
        )
    
    async def generate_market_opportunity_heatmap(self, businesses: List[Dict], demographics: Dict, business_type: str) -> HeatmapLayer:
        """
        Generate heatmap based on market opportunity logic:
        - Fewer competitors = higher opportunity
        - High demographics = better market
        - Low competition + high demographics = prime opportunity
        """
        logger.info(f"🎯 Generating market opportunity heatmap for {business_type}")
        
        points = []
        population = demographics.get('total_population', 0)
        income = demographics.get('median_household_income', 50000)
        
        # Calculate average competition level
        total_competitors = len(businesses)
        avg_rating = sum(b.get('rating', 0) for b in businesses) / max(total_competitors, 1)
        
        # Create opportunity grid
        center_lat = sum(b['coordinates']['latitude'] for b in businesses) / max(total_competitors, 1)
        center_lng = sum(b['coordinates']['longitude'] for b in businesses) / max(total_competitors, 1)
        
        grid_size = 15
        for i in range(grid_size):
            for j in range(grid_size):
                lat_offset = (i - grid_size/2) * 0.008
                lng_offset = (j - grid_size/2) * 0.008
                
                lat = center_lat + lat_offset
                lng = center_lng + lng_offset
                
                # Calculate distance to nearest competitor
                min_distance = float('inf')
                for business in businesses:
                    dist = math.sqrt(
                        (lat - business['coordinates']['latitude'])**2 + 
                        (lng - business['coordinates']['longitude'])**2
                    )
                    min_distance = min(min_distance, dist)
                
                # Opportunity logic: far from competitors + good demographics = high opportunity
                distance_factor = min(min_distance * 100, 1.0)  # Convert to 0-1 scale
                demographic_factor = min((population / 1000000) * (income / 100000), 1.0)
                
                # High opportunity = low competition + high demographics
                opportunity_score = distance_factor * demographic_factor
                
                point = HeatmapPoint(
                    latitude=lat,
                    longitude=lng,
                    intensity=opportunity_score,
                    weight=opportunity_score * 60,
                    data_type='market_opportunity',
                    metadata={
                        'opportunity_score': opportunity_score,
                        'distance_to_competitors': min_distance,
                        'demographic_factor': demographic_factor,
                        'competition_level': total_competitors
                    }
                )
                points.append(point)
        
        return HeatmapLayer(
            layer_id="market_opportunity",
            heatmap_type=HeatmapType.MARKET_OPPORTUNITY,
            points=points,
            color_scheme="green_yellow_red",  # Green = high opportunity
            radius_config={"min": 12, "max": 55, "zoom_factor": 1.7},
            intensity_config={"min": 0.7, "max": 2.2},
            description="Market opportunity based on competition density and demographic potential"
        )
    
    async def generate_income_wealth_heatmap(self, demographics: Dict, center_coords: Tuple[float, float]) -> HeatmapLayer:
        """
        Generate heatmap based on income and wealth distribution:
        - Income levels = spending power
        - Education levels = market sophistication
        - Population density = market size
        """
        logger.info("💰 Generating income & wealth heatmap")
        
        points = []
        income = demographics.get('median_household_income', 50000)
        education = demographics.get('education_data', {})
        population = demographics.get('total_population', 0)
        
        center_lat, center_lng = center_coords
        grid_size = 12  # Smaller grid for income analysis
        
        for i in range(grid_size):
            for j in range(grid_size):
                # Calculate position in grid
                lat_offset = (i - grid_size/2) * 0.008
                lng_offset = (j - grid_size/2) * 0.008
                
                lat = center_lat + lat_offset
                lng = center_lng + lng_offset
                
                # Calculate income-based intensity
                income_factor = min(income / 100000, 1.0)  # Normalize to 0-1
                education_factor = min(education.get('bachelors_degree', 0) / 100000, 1.0)
                population_factor = min(population / 1000000, 1.0)
                
                # Wealth intensity: income + education + population
                wealth_intensity = (income_factor * 0.5 + education_factor * 0.3 + population_factor * 0.2)
                
                point = HeatmapPoint(
                    latitude=lat,
                    longitude=lng,
                    intensity=wealth_intensity,
                    weight=wealth_intensity * 40,
                    data_type='income_wealth',
                    metadata={
                        'income': income,
                        'education_level': education_factor,
                        'population': population,
                        'wealth_score': wealth_intensity
                    }
                )
                points.append(point)
        
        return HeatmapLayer(
            layer_id="income_wealth",
            heatmap_type=HeatmapType.INCOME_WEALTH,
            points=points,
            color_scheme="blue_purple_pink",  # Blue = high income
            radius_config={"min": 20, "max": 70, "zoom_factor": 2.2},
            intensity_config={"min": 0.9, "max": 2.0},
            description="Income and wealth distribution based on median income, education, and population"
        )
    
    async def generate_review_power_heatmap(self, businesses: List[Dict], location_data: Dict) -> HeatmapLayer:
        """
        Generate heatmap based on review power and marketing influence:
        - Review count = customer engagement
        - Rating quality = customer satisfaction
        - Review velocity = recent activity
        """
        logger.info("⭐ Generating review power heatmap")
        
        points = []
        for business in businesses:
            # Calculate review power based on quantity and quality
            review_count = business.get('user_ratings_total', 0)
            rating = business.get('rating', 0)
            
            # Review power logic: volume × quality × recency factor
            review_volume = min(review_count / 1000, 1.0)  # Normalize review count
            review_quality = rating / 5.0  # Normalize rating
            recency_factor = 1.0  # Could add time-based factor later
            
            # Combined review power
            review_power = review_volume * review_quality * recency_factor
            
            # Marketing influence based on review power
            marketing_influence = review_power * 1.5  # Amplify for visibility
            marketing_influence = min(marketing_influence, 1.0)  # Cap at 1.0
            
            point = HeatmapPoint(
                latitude=business['coordinates']['latitude'],
                longitude=business['coordinates']['longitude'],
                intensity=marketing_influence,
                weight=review_count / 50,  # Weight by actual review count
                data_type='review_power',
                metadata={
                    'business_name': business.get('name', ''),
                    'review_count': review_count,
                    'rating': rating,
                    'review_power': review_power,
                    'marketing_influence': marketing_influence
                }
            )
            points.append(point)
        
        return HeatmapLayer(
            layer_id="review_power",
            heatmap_type=HeatmapType.REVIEW_POWER,
            points=points,
            color_scheme="orange_red_purple",  # Orange = high review power
            radius_config={"min": 6, "max": 35, "zoom_factor": 1.6},
            intensity_config={"min": 0.4, "max": 3.2},
            description="Review power and marketing influence based on review volume, quality, and engagement"
        )
    
    async def generate_all_heatmap_layers(self, businesses: List[Dict], demographics: Dict, 
                                        location_data: Dict, business_type: str) -> Dict[str, HeatmapLayer]:
        """
        Generate all heatmap layers for comprehensive analysis
        """
        logger.info("🔥 Generating all intelligent heatmap layers")
        
        center_coords = (location_data.get('latitude', 0), location_data.get('longitude', 0))
        
        # Generate all layers
        layers = {}
        
        # Business competition layer
        layers['business_competition'] = await self.generate_business_competition_heatmap(businesses, location_data)
        
        # Demographic density layer
        layers['demographic_density'] = await self.generate_demographic_density_heatmap(demographics, center_coords)
        
        # Foot traffic layer
        layers['foot_traffic'] = await self.generate_foot_traffic_heatmap(businesses, demographics)
        
        # Market opportunity layer
        layers['market_opportunity'] = await self.generate_market_opportunity_heatmap(businesses, demographics, business_type)
        
        # Income & wealth layer
        layers['income_wealth'] = await self.generate_income_wealth_heatmap(demographics, center_coords)
        
        # Review power layer
        layers['review_power'] = await self.generate_review_power_heatmap(businesses, location_data)
        
        self.layers = layers
        logger.info(f"✅ Generated {len(layers)} intelligent heatmap layers")
        
        return layers
    
    def get_layer_geojson(self, layer_id: str) -> Dict[str, Any]:
        """
        Convert heatmap layer to GeoJSON format for Mapbox
        """
        if layer_id not in self.layers:
            return {"type": "FeatureCollection", "features": []}
        
        layer = self.layers[layer_id]
        features = []
        
        for point in layer.points:
            feature = {
                "type": "Feature",
                "properties": {
                    "intensity": point.intensity,
                    "weight": point.weight,
                    "data_type": point.data_type,
                    **point.metadata
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [point.longitude, point.latitude]
                }
            }
            features.append(feature)
        
        return {
            "type": "FeatureCollection",
            "features": features,
            "layer_config": {
                "color_scheme": layer.color_scheme,
                "radius_config": layer.radius_config,
                "intensity_config": layer.intensity_config,
                "description": layer.description
            }
        }
    
    def get_available_layers(self) -> List[Dict[str, Any]]:
        """
        Get list of available heatmap layers
        """
        layers_info = []
        for layer_id, layer in self.layers.items():
            layers_info.append({
                "id": layer_id,
                "type": layer.heatmap_type.value,
                "point_count": len(layer.points),
                "description": layer.description,
                "color_scheme": layer.color_scheme
            })
        return layers_info
