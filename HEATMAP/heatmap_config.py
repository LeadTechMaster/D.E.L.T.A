"""
D.E.L.T.A Heatmap Configuration
Color schemes, radius configurations, and visual settings for different heatmap types
"""

from typing import Dict, List, Any
from enum import Enum

class ColorScheme(Enum):
    """Predefined color schemes for different heatmap types"""
    RED_ORANGE_YELLOW = "red_orange_yellow"      # Competition/High intensity
    BLUE_GREEN_YELLOW = "blue_green_yellow"      # Demographics/Population
    PURPLE_PINK_RED = "purple_pink_red"          # Foot traffic/Movement
    GREEN_YELLOW_RED = "green_yellow_red"        # Opportunity/Growth
    BLUE_PURPLE_PINK = "blue_purple_pink"        # Income/Wealth
    ORANGE_RED_PURPLE = "orange_red_purple"      # Reviews/Marketing power

class HeatmapConfig:
    """Configuration for heatmap visualization"""
    
    COLOR_SCHEMES = {
        ColorScheme.RED_ORANGE_YELLOW.value: {
            "name": "Competition Intensity",
            "colors": [
                "rgba(0,0,0,0)",           # Transparent
                "rgba(255,0,0,0.3)",       # Red - High competition
                "rgba(255,165,0,0.5)",     # Orange - Medium competition
                "rgba(255,255,0,0.7)",     # Yellow - Low competition
                "rgba(255,255,0,0.9)"      # Bright yellow - Very low
            ],
            "description": "Red areas show high business competition, yellow areas show low competition"
        },
        
        ColorScheme.BLUE_GREEN_YELLOW.value: {
            "name": "Demographic Density",
            "colors": [
                "rgba(0,0,0,0)",           # Transparent
                "rgba(0,100,200,0.3)",     # Blue - High population
                "rgba(0,200,100,0.5)",     # Green - Medium population
                "rgba(255,255,0,0.7)",     # Yellow - Low population
                "rgba(255,255,0,0.9)"      # Bright yellow - Very low
            ],
            "description": "Blue areas show high demographic density, yellow areas show low density"
        },
        
        ColorScheme.PURPLE_PINK_RED.value: {
            "name": "Foot Traffic",
            "colors": [
                "rgba(0,0,0,0)",           # Transparent
                "rgba(128,0,128,0.3)",     # Purple - High foot traffic
                "rgba(255,192,203,0.5)",   # Pink - Medium foot traffic
                "rgba(255,0,0,0.7)",       # Red - Low foot traffic
                "rgba(255,0,0,0.9)"        # Bright red - Very low
            ],
            "description": "Purple areas show high foot traffic, red areas show low foot traffic"
        },
        
        ColorScheme.GREEN_YELLOW_RED.value: {
            "name": "Market Opportunity",
            "colors": [
                "rgba(0,0,0,0)",           # Transparent
                "rgba(0,100,255,0.4)",     # Deep Blue - Very high opportunity
                "rgba(0,200,100,0.6)",     # Teal - High opportunity
                "rgba(100,255,100,0.8)",   # Bright Green - Medium opportunity
                "rgba(255,255,0,0.9)"      # Bright Yellow - Low opportunity
            ],
            "description": "Blue areas show very high market opportunity, yellow areas show low opportunity"
        },
        
        ColorScheme.BLUE_PURPLE_PINK.value: {
            "name": "Income & Wealth",
            "colors": [
                "rgba(0,0,0,0)",           # Transparent
                "rgba(0,0,255,0.3)",       # Blue - High income
                "rgba(128,0,128,0.5)",     # Purple - Medium income
                "rgba(255,192,203,0.7)",   # Pink - Low income
                "rgba(255,192,203,0.9)"    # Bright pink - Very low
            ],
            "description": "Blue areas show high income levels, pink areas show low income levels"
        },
        
        ColorScheme.ORANGE_RED_PURPLE.value: {
            "name": "Review & Marketing Power",
            "colors": [
                "rgba(0,0,0,0)",           # Transparent
                "rgba(255,165,0,0.3)",     # Orange - High marketing power
                "rgba(255,0,0,0.5)",       # Red - Medium marketing power
                "rgba(128,0,128,0.7)",     # Purple - Low marketing power
                "rgba(128,0,128,0.9)"      # Bright purple - Very low
            ],
            "description": "Orange areas show high marketing power, purple areas show low marketing power"
        }
    }
    
    RADIUS_CONFIGS = {
        "business_competition": {
            "min_radius": 10,
            "max_radius": 50,
            "zoom_factor": 1.5,
            "description": "Medium radius for business competition visibility"
        },
        "demographic_density": {
            "min_radius": 15,
            "max_radius": 60,
            "zoom_factor": 2.0,
            "description": "Large radius for demographic area coverage"
        },
        "foot_traffic": {
            "min_radius": 8,
            "max_radius": 40,
            "zoom_factor": 1.8,
            "description": "Small-medium radius for precise foot traffic"
        },
        "market_opportunity": {
            "min_radius": 12,
            "max_radius": 55,
            "zoom_factor": 1.7,
            "description": "Medium-large radius for opportunity zones"
        },
        "income_wealth": {
            "min_radius": 20,
            "max_radius": 70,
            "zoom_factor": 2.2,
            "description": "Large radius for income area analysis"
        },
        "review_power": {
            "min_radius": 6,
            "max_radius": 35,
            "zoom_factor": 1.6,
            "description": "Small radius for precise review analysis"
        }
    }
    
    INTENSITY_CONFIGS = {
        "business_competition": {
            "min_intensity": 0.5,
            "max_intensity": 3.0,
            "description": "High intensity for competition visibility"
        },
        "demographic_density": {
            "min_intensity": 0.8,
            "max_intensity": 2.5,
            "description": "Medium-high intensity for demographic clarity"
        },
        "foot_traffic": {
            "min_intensity": 0.6,
            "max_intensity": 2.8,
            "description": "High intensity for foot traffic patterns"
        },
        "market_opportunity": {
            "min_intensity": 0.7,
            "max_intensity": 2.2,
            "description": "Medium intensity for opportunity analysis"
        },
        "income_wealth": {
            "min_intensity": 0.9,
            "max_intensity": 2.0,
            "description": "Medium intensity for income visualization"
        },
        "review_power": {
            "min_intensity": 0.4,
            "max_intensity": 3.2,
            "description": "Very high intensity for review analysis"
        }
    }
    
    @classmethod
    def get_color_scheme(cls, scheme_name: str) -> Dict[str, Any]:
        """Get color scheme configuration"""
        return cls.COLOR_SCHEMES.get(scheme_name, cls.COLOR_SCHEMES[ColorScheme.RED_ORANGE_YELLOW.value])
    
    @classmethod
    def get_radius_config(cls, layer_type: str) -> Dict[str, Any]:
        """Get radius configuration for layer type"""
        return cls.RADIUS_CONFIGS.get(layer_type, cls.RADIUS_CONFIGS["business_competition"])
    
    @classmethod
    def get_intensity_config(cls, layer_type: str) -> Dict[str, Any]:
        """Get intensity configuration for layer type"""
        return cls.INTENSITY_CONFIGS.get(layer_type, cls.INTENSITY_CONFIGS["business_competition"])
    
    @classmethod
    def get_mapbox_heatmap_config(cls, layer_type: str, color_scheme: str) -> Dict[str, Any]:
        """Get complete Mapbox heatmap configuration"""
        radius_config = cls.get_radius_config(layer_type)
        intensity_config = cls.get_intensity_config(layer_type)
        colors = cls.get_color_scheme(color_scheme)["colors"]
        
        return {
            "paint": {
                "heatmap-weight": [
                    "interpolate", ["linear"], ["coalesce", ["get", "weight"], 1],
                    0, 0, 50, 0.5, 100, 1
                ],
                "heatmap-intensity": [
                    "interpolate", ["linear"], ["zoom"],
                    0, intensity_config["min_intensity"],
                    15, intensity_config["max_intensity"]
                ],
                "heatmap-radius": [
                    "interpolate", ["linear"], ["zoom"],
                    0, radius_config["min_radius"],
                    9, radius_config["min_radius"] + (radius_config["max_radius"] - radius_config["min_radius"]) * 0.5,
                    15, radius_config["max_radius"]
                ],
                "heatmap-color": [
                    "interpolate", ["linear"], ["heatmap-density"],
                    0, colors[0],
                    0.2, colors[1],
                    0.4, colors[2],
                    0.6, colors[3],
                    1, colors[4]
                ],
                "heatmap-opacity": [
                    "interpolate", ["linear"], ["zoom"],
                    8, 0.8,
                    15, 0.6
                ]
            }
        }

class HeatmapButtonConfig:
    """Configuration for heatmap control buttons"""
    
    BUTTONS = [
        {
            "id": "business_competition",
            "label": "🏢 Competition",
            "description": "Business competition intensity",
            "icon": "🏢",
            "color": "#ff4444",
            "layer_type": "business_competition",
            "color_scheme": "red_orange_yellow"
        },
        {
            "id": "demographic_density", 
            "label": "👥 Demographics",
            "description": "Population and demographic density",
            "icon": "👥",
            "color": "#4444ff",
            "layer_type": "demographic_density",
            "color_scheme": "blue_green_yellow"
        },
        {
            "id": "foot_traffic",
            "label": "🚶 Foot Traffic",
            "description": "Foot traffic and movement patterns",
            "icon": "🚶",
            "color": "#8844ff",
            "layer_type": "foot_traffic", 
            "color_scheme": "purple_pink_red"
        },
        {
            "id": "market_opportunity",
            "label": "🎯 Opportunity",
            "description": "Market opportunity zones",
            "icon": "🎯",
            "color": "#44ff44",
            "layer_type": "market_opportunity",
            "color_scheme": "green_yellow_red"
        },
        {
            "id": "income_wealth",
            "label": "💰 Income",
            "description": "Income and wealth distribution",
            "icon": "💰",
            "color": "#44aaff",
            "layer_type": "income_wealth",
            "color_scheme": "blue_purple_pink"
        },
        {
            "id": "review_power",
            "label": "⭐ Reviews",
            "description": "Review power and marketing influence",
            "icon": "⭐",
            "color": "#ff8844",
            "layer_type": "review_power",
            "color_scheme": "orange_red_purple"
        }
    ]
    
    @classmethod
    def get_button_config(cls, button_id: str) -> Dict[str, Any]:
        """Get button configuration by ID"""
        for button in cls.BUTTONS:
            if button["id"] == button_id:
                return button
        return cls.BUTTONS[0]  # Default to first button
    
    @classmethod
    def get_all_buttons(cls) -> List[Dict[str, Any]]:
        """Get all button configurations"""
        return cls.BUTTONS
