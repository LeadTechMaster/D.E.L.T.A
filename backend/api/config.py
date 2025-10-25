#!/usr/bin/env python3
"""
Configuration for Franchise Intelligence Platform
Environment variables, settings, and API configurations
"""
import os
from pathlib import Path
from typing import Dict, Any
from pydantic import BaseSettings

class Settings(BaseSettings):
    """Application settings"""
    
    # Application
    app_name: str = "Franchise Intelligence Platform"
    app_version: str = "1.0.0"
    debug: bool = False
    
    # Database
    database_url: str = "postgresql://postgres:password@localhost:5433/franchise_intelligence"
    db_host: str = "localhost"
    db_port: int = 5433
    db_name: str = "franchise_intelligence"
    db_user: str = "postgres"
    db_password: str = "password"
    
    # Redis
    redis_url: str = "redis://localhost:6380"
    redis_host: str = "localhost"
    redis_port: int = 6380
    
    # API Keys - REAL KEYS ONLY
    serpapi_api_key: str = "850faf17d2e379f54ffdd1e300daaa7bdb1dee8abdc2536f1de3430d137e563c"
    census_api_key: str = "ab4c49e507688c08e5346543c6d355a2e6b37c8c"
    mapbox_access_token: str = "pk.eyJ1Ijoic3VwcG9ydG1vdmVkaW4iLCJhIjoiY21kZmdxdHh6MGQ2aDJqcHE2YTIwbTFrMiJ9.I1xkq82JXLMlgB02xT8LMw"
    google_places_api_key: str = "AIzaSyAzyKYxbA7HWHTU9UV9Z-ELGRQTTeN9dkw"
    meta_ads_access_token: str = "EAA40mj0BFQYBPXUVZAWCEv0ZBFOXjEmLUd3o26dfD1yzBbCg6PodDpKvYZA4O4WZBHIag9fcUxrmTtUwtzmDICOSJua4YrlSDjyDYI5JcsKfWKbHP2ZCRutPaq069nmN2hzCx3R6R6M1vniJ6x2RYU79cdBiyluoLkp3U4OdqmV6yOOujAGdMKCn0LPBAEUboIgZDZD"
    meta_ads_app_token: str = "3998486727038214|Y7kOLPL2Wy8hridK2rO05qJmxRc"
    brightlocal_api_key: str = "2efdc9f13ec8a5b8fc0d83cddba7f5cc671ca3ec"
    
    # Service Ports
    fastapi_backend_port: int = 8001
    fastapi_docs_port: int = 8007
    fastapi_health_port: int = 8008
    postgresql_port: int = 5433
    redis_port: int = 6380
    
    # Data Policy
    data_policy: str = "real_data_only"
    collection_policy: str = "request_based_only"
    no_mock_data: bool = True
    no_demo_data: bool = True
    no_fallback_data: bool = True
    
    # Rate Limiting
    rate_limit_requests_per_minute: int = 60
    rate_limit_burst: int = 100
    
    # Caching
    cache_ttl: int = 3600  # 1 hour
    cache_max_size: int = 1000
    
    # Logging
    log_level: str = "INFO"
    log_format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    class Config:
        env_file = ".env"
        case_sensitive = False

# Global settings instance
settings = Settings()

# API Configuration
API_CONFIG = {
    "serpapi": {
        "base_url": "https://serpapi.com/search.json",
        "rate_limit": 100,  # requests per minute
        "timeout": 15
    },
    "census": {
        "base_url": "https://api.census.gov/data",
        "rate_limit": 500,  # requests per day
        "timeout": 10
    },
    "mapbox": {
        "base_url": "https://api.mapbox.com",
        "rate_limit": 1000,  # requests per minute
        "timeout": 10
    },
    "google_places": {
        "base_url": "https://maps.googleapis.com/maps/api/place",
        "rate_limit": 1000,  # requests per day
        "timeout": 10
    }
}

# Business Categories Configuration
BUSINESS_CATEGORIES = {
    "food_beverage": {
        "coffee": {
            "keywords": ["coffee", "cafe", "espresso", "latte", "coffee shop"],
            "search_terms": ["coffee near me", "best coffee", "coffee shop"]
        },
        "fast_food": {
            "keywords": ["fast food", "burger", "pizza", "sandwich", "quick food"],
            "search_terms": ["fast food near me", "burger joint", "pizza place"]
        },
        "casual_dining": {
            "keywords": ["restaurant", "dining", "food", "meal", "dinner"],
            "search_terms": ["restaurant near me", "best restaurant", "dining"]
        }
    },
    "retail_services": {
        "fitness": {
            "keywords": ["gym", "fitness", "workout", "exercise", "training"],
            "search_terms": ["gym near me", "fitness center", "workout"]
        },
        "beauty": {
            "keywords": ["salon", "beauty", "hair", "spa", "nail"],
            "search_terms": ["salon near me", "hair salon", "beauty salon"]
        },
        "automotive": {
            "keywords": ["auto", "car", "repair", "service", "mechanic"],
            "search_terms": ["auto repair near me", "car service", "mechanic"]
        }
    },
    "professional_services": {
        "cleaning": {
            "keywords": ["cleaning", "maid", "housekeeping", "janitorial"],
            "search_terms": ["cleaning service near me", "maid service", "housekeeping"]
        },
        "landscaping": {
            "keywords": ["landscaping", "lawn", "garden", "yard", "outdoor"],
            "search_terms": ["landscaping near me", "lawn service", "garden care"]
        },
        "real_estate": {
            "keywords": ["real estate", "property", "homes", "houses", "realtor"],
            "search_terms": ["real estate near me", "realtor", "property"]
        }
    }
}

# Market Metrics Configuration
MARKET_METRICS_CONFIG = {
    "white_space_index": {
        "weights": {
            "competitor_count": 0.4,
            "demographics": 0.3,
            "keyword_demand": 0.3
        },
        "thresholds": {
            "excellent": 0.8,
            "good": 0.6,
            "fair": 0.4,
            "poor": 0.2
        }
    },
    "suitability_score": {
        "weights": {
            "demographics": 0.4,
            "competition": 0.3,
            "keywords": 0.3
        },
        "thresholds": {
            "excellent": 0.8,
            "good": 0.6,
            "fair": 0.4,
            "poor": 0.2
        }
    },
    "market_saturation": {
        "weights": {
            "competitor_count": 0.5,
            "avg_rating": 0.3,
            "review_velocity": 0.2
        },
        "thresholds": {
            "oversaturated": 0.9,
            "saturated": 0.7,
            "competitive": 0.5,
            "opportunity": 0.3
        }
    }
}

# Database Configuration
DATABASE_CONFIG = {
    "pool_size": 10,
    "max_overflow": 20,
    "pool_timeout": 30,
    "pool_recycle": 3600,
    "echo": False
}

# Redis Configuration
REDIS_CONFIG = {
    "host": "localhost",
    "port": 6380,
    "db": 0,
    "decode_responses": True,
    "socket_timeout": 5,
    "socket_connect_timeout": 5,
    "retry_on_timeout": True
}

# Logging Configuration
LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        },
        "detailed": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(module)s - %(funcName)s - %(message)s"
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "INFO",
            "formatter": "default",
            "stream": "ext://sys.stdout"
        },
        "file": {
            "class": "logging.FileHandler",
            "level": "DEBUG",
            "formatter": "detailed",
            "filename": "franchise_intelligence.log"
        }
    },
    "loggers": {
        "": {
            "level": "INFO",
            "handlers": ["console", "file"],
            "propagate": False
        }
    }
}

# Environment Configuration
ENVIRONMENT_CONFIG = {
    "development": {
        "debug": True,
        "log_level": "DEBUG",
        "rate_limit": 1000,
        "cache_ttl": 300
    },
    "production": {
        "debug": False,
        "log_level": "INFO",
        "rate_limit": 60,
        "cache_ttl": 3600
    },
    "testing": {
        "debug": True,
        "log_level": "DEBUG",
        "rate_limit": 10000,
        "cache_ttl": 60
    }
}

def get_environment_config(env: str = "development") -> Dict[str, Any]:
    """Get configuration for specific environment"""
    return ENVIRONMENT_CONFIG.get(env, ENVIRONMENT_CONFIG["development"])

def load_api_keys() -> Dict[str, str]:
    """Load API keys from files"""
    api_keys = {}
    
    # SerpAPI key
    try:
        with open("../../serpapi/api_key.txt", "r") as f:
            api_keys["serpapi"] = f.read().strip()
    except:
        api_keys["serpapi"] = "your_serpapi_key"
    
    # Census API key
    try:
        with open("../../census/api_key.txt", "r") as f:
            api_keys["census"] = f.read().strip()
    except:
        api_keys["census"] = "your_census_key"
    
    # Mapbox token
    try:
        with open("../../mapbox/access_token.txt", "r") as f:
            api_keys["mapbox"] = f.read().strip()
    except:
        api_keys["mapbox"] = "your_mapbox_token"
    
    # Google Places API key
    try:
        with open("../../google_places/api_key.txt", "r") as f:
            api_keys["google_places"] = f.read().strip()
    except:
        api_keys["google_places"] = "your_google_places_key"
    
    return api_keys
