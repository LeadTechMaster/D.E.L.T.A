#!/usr/bin/env python3
"""
D.E.L.T.A Database Setup - Real Data Storage
SQLite database for storing real API responses and cached data
"""
import sqlite3
import json
import os
from datetime import datetime, timedelta
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Database path
DB_PATH = "/Users/udishkolnik/Downloads/D.E.L.T.A/DB/real_data.db"

def init_database():
    """Initialize the real data database with all necessary tables"""
    try:
        # Create DB directory if it doesn't exist
        os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
        
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Create API requests log table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS api_requests (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                endpoint TEXT NOT NULL,
                params TEXT,
                response TEXT,
                status_code INTEGER,
                response_time_ms INTEGER,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                data_source TEXT,
                data_policy TEXT DEFAULT 'REAL_DATA_ONLY'
            )
        ''')
        
        # Create cached data table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS cached_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                cache_key TEXT UNIQUE NOT NULL,
                data TEXT NOT NULL,
                expires_at DATETIME NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                data_source TEXT,
                data_policy TEXT DEFAULT 'REAL_DATA_ONLY'
            )
        ''')
        
        # Create business data table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS business_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                business_name TEXT NOT NULL,
                address TEXT,
                coordinates_lat REAL,
                coordinates_lng REAL,
                rating REAL,
                user_ratings_total INTEGER,
                price_level INTEGER,
                business_type TEXT,
                place_id TEXT UNIQUE,
                data_source TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                data_policy TEXT DEFAULT 'REAL_DATA_ONLY'
            )
        ''')
        
        # Create territory analysis table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS territory_analysis (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                center_lat REAL NOT NULL,
                center_lng REAL NOT NULL,
                radius_miles REAL NOT NULL,
                business_type TEXT NOT NULL,
                competitor_count INTEGER,
                opportunity_score REAL,
                market_saturation TEXT,
                recommendation TEXT,
                analysis_data TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                data_policy TEXT DEFAULT 'REAL_DATA_ONLY'
            )
        ''')
        
        # Create demographics table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS demographics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                location_name TEXT NOT NULL,
                state_fips TEXT,
                county_fips TEXT,
                total_population INTEGER,
                median_household_income INTEGER,
                mean_commute_time REAL,
                data_source TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                data_policy TEXT DEFAULT 'REAL_DATA_ONLY'
            )
        ''')
        
        # Create search results table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS search_results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                query TEXT NOT NULL,
                location TEXT,
                search_engine TEXT,
                results_data TEXT,
                total_results INTEGER,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                data_policy TEXT DEFAULT 'REAL_DATA_ONLY'
            )
        ''')
        
        # Create indexes for better performance
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_api_requests_endpoint ON api_requests(endpoint)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_api_requests_timestamp ON api_requests(timestamp)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_cached_data_key ON cached_data(cache_key)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_business_data_coordinates ON business_data(coordinates_lat, coordinates_lng)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_territory_analysis_center ON territory_analysis(center_lat, center_lng)')
        
        conn.commit()
        conn.close()
        
        logger.info("✅ Database initialized successfully")
        return True
        
    except Exception as e:
        logger.error(f"❌ Database initialization failed: {e}")
        return False

def log_api_request(endpoint, params, response, status_code, response_time, data_source="Unknown"):
    """Log API request to database"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO api_requests (endpoint, params, response, status_code, response_time_ms, data_source)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            endpoint,
            json.dumps(params) if params else None,
            json.dumps(response) if response else None,
            status_code,
            response_time,
            data_source
        ))
        
        conn.commit()
        conn.close()
        return True
        
    except Exception as e:
        logger.error(f"Failed to log API request: {e}")
        return False

def store_business_data(businesses, data_source="Google Places API"):
    """Store business data in database"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        for business in businesses:
            cursor.execute('''
                INSERT OR REPLACE INTO business_data 
                (business_name, address, coordinates_lat, coordinates_lng, rating, 
                 user_ratings_total, price_level, business_type, place_id, data_source)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                business.get('name', ''),
                business.get('address', ''),
                business.get('coordinates', {}).get('latitude'),
                business.get('coordinates', {}).get('longitude'),
                business.get('rating', 0),
                business.get('user_ratings_total', 0),
                business.get('price_level', 0),
                ','.join(business.get('types', [])),
                business.get('place_id', ''),
                data_source
            ))
        
        conn.commit()
        conn.close()
        logger.info(f"✅ Stored {len(businesses)} businesses in database")
        return True
        
    except Exception as e:
        logger.error(f"Failed to store business data: {e}")
        return False

def store_territory_analysis(analysis_data):
    """Store territory analysis in database"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO territory_analysis 
            (center_lat, center_lng, radius_miles, business_type, competitor_count,
             opportunity_score, market_saturation, recommendation, analysis_data)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            analysis_data.get('center', {}).get('lat'),
            analysis_data.get('center', {}).get('lng'),
            analysis_data.get('radius_miles'),
            analysis_data.get('business_type'),
            analysis_data.get('competitor_count'),
            analysis_data.get('opportunity_score'),
            analysis_data.get('market_saturation'),
            analysis_data.get('recommended_action'),
            json.dumps(analysis_data)
        ))
        
        conn.commit()
        conn.close()
        logger.info("✅ Stored territory analysis in database")
        return True
        
    except Exception as e:
        logger.error(f"Failed to store territory analysis: {e}")
        return False

def store_demographics(demographics_data, location_name, data_source="US Census Bureau"):
    """Store demographics data in database"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO demographics 
            (location_name, state_fips, county_fips, total_population, 
             median_household_income, mean_commute_time, data_source)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            location_name,
            demographics_data.get('state_fips'),
            demographics_data.get('county_fips'),
            demographics_data.get('total_population'),
            demographics_data.get('median_household_income'),
            demographics_data.get('mean_commute_time'),
            data_source
        ))
        
        conn.commit()
        conn.close()
        logger.info("✅ Stored demographics in database")
        return True
        
    except Exception as e:
        logger.error(f"Failed to store demographics: {e}")
        return False

def get_cached_data(cache_key, max_age_hours=24):
    """Get cached data if it exists and is not expired"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT data FROM cached_data 
            WHERE cache_key = ? AND expires_at > ?
        ''', (cache_key, datetime.now()))
        
        result = cursor.fetchone()
        conn.close()
        
        if result:
            logger.info(f"✅ Cache hit for key: {cache_key}")
            return json.loads(result[0])
        else:
            logger.info(f"❌ Cache miss for key: {cache_key}")
            return None
            
    except Exception as e:
        logger.error(f"Failed to get cached data: {e}")
        return None

def set_cached_data(cache_key, data, expires_hours=24):
    """Set cached data with expiration"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        expires_at = datetime.now() + timedelta(hours=expires_hours)
        
        cursor.execute('''
            INSERT OR REPLACE INTO cached_data (cache_key, data, expires_at)
            VALUES (?, ?, ?)
        ''', (cache_key, json.dumps(data), expires_at))
        
        conn.commit()
        conn.close()
        logger.info(f"✅ Cached data for key: {cache_key}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to set cached data: {e}")
        return False

def get_database_stats():
    """Get database statistics"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        stats = {}
        
        # Count records in each table
        tables = ['api_requests', 'cached_data', 'business_data', 'territory_analysis', 'demographics', 'search_results']
        for table in tables:
            cursor.execute(f'SELECT COUNT(*) FROM {table}')
            stats[f'{table}_count'] = cursor.fetchone()[0]
        
        # Get recent API requests
        cursor.execute('''
            SELECT endpoint, COUNT(*) as count 
            FROM api_requests 
            WHERE timestamp > datetime('now', '-24 hours')
            GROUP BY endpoint 
            ORDER BY count DESC 
            LIMIT 10
        ''')
        stats['recent_endpoints'] = cursor.fetchall()
        
        # Get data sources
        cursor.execute('''
            SELECT data_source, COUNT(*) as count 
            FROM api_requests 
            GROUP BY data_source 
            ORDER BY count DESC
        ''')
        stats['data_sources'] = cursor.fetchall()
        
        conn.close()
        return stats
        
    except Exception as e:
        logger.error(f"Failed to get database stats: {e}")
        return {}

def cleanup_expired_cache():
    """Clean up expired cache entries"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM cached_data WHERE expires_at < ?', (datetime.now(),))
        deleted_count = cursor.rowcount
        
        conn.commit()
        conn.close()
        
        logger.info(f"✅ Cleaned up {deleted_count} expired cache entries")
        return deleted_count
        
    except Exception as e:
        logger.error(f"Failed to cleanup expired cache: {e}")
        return 0

if __name__ == "__main__":
    print("🚀 Initializing D.E.L.T.A Real Data Database")
    
    if init_database():
        print("✅ Database initialized successfully")
        
        # Show database stats
        stats = get_database_stats()
        print("\n📊 Database Statistics:")
        for key, value in stats.items():
            print(f"  {key}: {value}")
        
        # Cleanup expired cache
        cleaned = cleanup_expired_cache()
        print(f"\n🧹 Cleaned up {cleaned} expired cache entries")
        
    else:
        print("❌ Database initialization failed")
