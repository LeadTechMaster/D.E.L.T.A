#!/usr/bin/env python3
"""
Database Cache System for API Responses
Stores and retrieves API responses to avoid redundant calls
"""

import sqlite3
import json
import logging
import hashlib
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
import asyncio

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DatabaseCache:
    """Database cache for API responses"""
    
    def __init__(self, db_path: str = "api_cache.db"):
        """Initialize database cache"""
        self.db_path = db_path
        self.init_database()
        logger.info(f"🗄️ Database cache initialized: {db_path}")
    
    def init_database(self):
        """Initialize database tables"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Create cache table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS api_cache (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    cache_key TEXT UNIQUE NOT NULL,
                    api_type TEXT NOT NULL,
                    query TEXT NOT NULL,
                    response_data TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    expires_at TIMESTAMP NOT NULL,
                    hit_count INTEGER DEFAULT 0,
                    last_accessed TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Create indexes
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_cache_key ON api_cache(cache_key)
            """)
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_api_type ON api_cache(api_type)
            """)
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_expires_at ON api_cache(expires_at)
            """)
            
            conn.commit()
    
    def _generate_cache_key(self, api_type: str, query: str, params: Dict[str, Any] = None) -> str:
        """Generate unique cache key for API request"""
        # Combine all parameters into a string
        key_data = f"{api_type}:{query}"
        if params:
            key_data += f":{json.dumps(params, sort_keys=True)}"
        
        # Generate hash
        return hashlib.md5(key_data.encode()).hexdigest()
    
    def _get_cache_duration(self, api_type: str) -> timedelta:
        """Get cache duration for different API types"""
        cache_durations = {
            "geocoding": timedelta(hours=24),  # Locations don't change often
            "places": timedelta(hours=6),      # Business data changes more frequently
            "demographics": timedelta(days=7), # Census data is updated annually
            "serpapi": timedelta(hours=12),    # Search results change frequently
            "territory": timedelta(hours=6),   # Territory analysis changes moderately
            "franchise": timedelta(hours=12)   # Franchise opportunities change moderately
        }
        return cache_durations.get(api_type, timedelta(hours=6))
    
    async def get_cached_response(self, api_type: str, query: str, params: Dict[str, Any] = None) -> Optional[Dict[str, Any]]:
        """Get cached API response if available and not expired"""
        cache_key = self._generate_cache_key(api_type, query, params)
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Get cached response
            cursor.execute("""
                SELECT response_data, expires_at FROM api_cache 
                WHERE cache_key = ? AND expires_at > CURRENT_TIMESTAMP
            """, (cache_key,))
            
            result = cursor.fetchone()
            
            if result:
                response_data, expires_at = result
                
                # Update hit count and last accessed
                cursor.execute("""
                    UPDATE api_cache 
                    SET hit_count = hit_count + 1, last_accessed = CURRENT_TIMESTAMP
                    WHERE cache_key = ?
                """, (cache_key,))
                
                conn.commit()
                
                logger.info(f"🗄️ Cache hit for {api_type}: {query}")
                return json.loads(response_data)
            else:
                logger.info(f"🗄️ Cache miss for {api_type}: {query}")
                return None
    
    async def cache_response(self, api_type: str, query: str, response_data: Dict[str, Any], params: Dict[str, Any] = None):
        """Cache API response"""
        cache_key = self._generate_cache_key(api_type, query, params)
        cache_duration = self._get_cache_duration(api_type)
        expires_at = datetime.now() + cache_duration
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Insert or update cache entry
            cursor.execute("""
                INSERT OR REPLACE INTO api_cache 
                (cache_key, api_type, query, response_data, expires_at)
                VALUES (?, ?, ?, ?, ?)
            """, (
                cache_key,
                api_type,
                query,
                json.dumps(response_data),
                expires_at
            ))
            
            conn.commit()
            logger.info(f"🗄️ Cached response for {api_type}: {query} (expires: {expires_at})")
    
    async def clear_expired_cache(self):
        """Clear expired cache entries"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute("DELETE FROM api_cache WHERE expires_at < CURRENT_TIMESTAMP")
            deleted_count = cursor.rowcount
            
            conn.commit()
            
            if deleted_count > 0:
                logger.info(f"🗄️ Cleared {deleted_count} expired cache entries")
    
    async def get_cache_stats(self) -> Dict[str, Any]:
        """Get cache statistics"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Total entries
            cursor.execute("SELECT COUNT(*) FROM api_cache")
            total_entries = cursor.fetchone()[0]
            
            # Active entries (not expired)
            cursor.execute("SELECT COUNT(*) FROM api_cache WHERE expires_at > CURRENT_TIMESTAMP")
            active_entries = cursor.fetchone()[0]
            
            # Entries by API type
            cursor.execute("""
                SELECT api_type, COUNT(*) FROM api_cache 
                WHERE expires_at > CURRENT_TIMESTAMP
                GROUP BY api_type
            """)
            api_type_counts = dict(cursor.fetchall())
            
            # Total hits
            cursor.execute("SELECT SUM(hit_count) FROM api_cache")
            total_hits = cursor.fetchone()[0] or 0
            
            return {
                "total_entries": total_entries,
                "active_entries": active_entries,
                "api_type_counts": api_type_counts,
                "total_hits": total_hits
            }
    
    async def clear_all_cache(self):
        """Clear all cache entries"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute("DELETE FROM api_cache")
            deleted_count = cursor.rowcount
            
            conn.commit()
            logger.info(f"🗄️ Cleared all cache entries: {deleted_count}")

# Global instance
database_cache = DatabaseCache()

# Convenience functions
async def get_cached_response(api_type: str, query: str, params: Dict[str, Any] = None) -> Optional[Dict[str, Any]]:
    """Convenience function for getting cached response"""
    return await database_cache.get_cached_response(api_type, query, params)

async def cache_response(api_type: str, query: str, response_data: Dict[str, Any], params: Dict[str, Any] = None):
    """Convenience function for caching response"""
    await database_cache.cache_response(api_type, query, response_data, params)

async def clear_expired_cache():
    """Convenience function for clearing expired cache"""
    await database_cache.clear_expired_cache()

async def get_cache_stats():
    """Convenience function for getting cache stats"""
    return await database_cache.get_cache_stats()

if __name__ == "__main__":
    # Test the cache system
    async def test_cache():
        print("🧪 Testing Database Cache:")
        print("=" * 30)
        
        # Test caching
        test_data = {"test": "data", "timestamp": datetime.now().isoformat()}
        await cache_response("test", "test_query", test_data)
        
        # Test retrieval
        cached = await get_cached_response("test", "test_query")
        print(f"Cached data: {cached}")
        
        # Test stats
        stats = await get_cache_stats()
        print(f"Cache stats: {stats}")
    
    asyncio.run(test_cache())



