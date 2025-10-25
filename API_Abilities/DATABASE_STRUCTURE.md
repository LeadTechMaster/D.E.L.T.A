# API Abilities - Database Structure Documentation

This document outlines the complete database structure for all API services. Each service has its own SQLite database with specific schemas for storing and searching data.

---

## Overview

**Total Databases**: 7 (one per API service)
**Database Type**: SQLite3
**Location**: Each service's `DB/` folder

---

## 1. MAPBOX DATABASE (`mapbox.db`)

**Purpose**: Store geocoding, routing, and map data for caching and offline access

### Tables:
- **geocoding_cache** - Cached address-to-coordinates conversions
- **reverse_geocoding_cache** - Cached coordinates-to-address conversions
- **routes** - Saved routing data between points
- **isochrones** - Reachable areas within time limits
- **distance_matrix** - Distance/time calculations between multiple points

### Use Cases:
- Cache geocoding results to reduce API calls
- Store frequently used routes
- Historical route analysis
- Area accessibility mapping

---

## 2. SERPAPI DATABASE (`serpapi.db`)

**Purpose**: Store keyword research data, search results, and local business information

### Tables:
- **keywords** - Keyword search volume, difficulty, and competition data
- **keyword_suggestions** - Related keyword suggestions
- **people_also_ask** - PAA questions for keywords
- **local_pack** - Local 3-pack search results
- **search_results** - Organic search results
- **serp_features** - SERP feature data (snippets, knowledge graph, etc.)
- **competitor_keywords** - Keywords competitors rank for
- **related_searches** - Related search queries
- **search_trends** - Search trend data over time

### Use Cases:
- Keyword research and planning
- Competitor analysis
- Local SEO tracking
- Search trend analysis
- Content planning based on PAA questions

---

## 3. META ADS DATABASE (`meta_ads.db`)

**Purpose**: Store Facebook/Instagram ad data and competitor intelligence

### Tables:
- **ads** - Ad catalog with creative and metadata
- **ad_spend** - Spending data and impressions
- **ad_targeting** - Targeting demographics and locations
- **ad_creatives** - Creative assets (images, videos, copy)
- **ad_performance** - Performance metrics
- **competitors** - Competitor analysis data
- **ad_searches** - Ad search history

### Use Cases:
- Competitive ad analysis
- Ad spend tracking
- Creative strategy insights
- Targeting strategy research
- Market intelligence

---

## 4. US CENSUS DATABASE (`us_census.db`)

**Purpose**: Store demographic, economic, and housing statistics

### Tables:
- **population** - Population statistics by area
- **demographics** - Age, gender, race demographics
- **economic_data** - Income, employment, poverty data
- **housing** - Housing units, values, rent data
- **education** - Education level statistics
- **business_patterns** - Business demographics by industry
- **commute_data** - Commute patterns and transportation

### Use Cases:
- Market demographic analysis
- Location targeting
- Economic opportunity assessment
- Housing market analysis
- Business location planning

---

## 5. GOOGLE PLACES & GMB DATABASE (`google_places.db`)

**Purpose**: Store business listings, reviews, and GMB management data

### Tables:
- **places** - Business listings and details
- **business_hours** - Operating hours
- **reviews** - Customer reviews and ratings
- **photos** - Business photos
- **gmb_insights** - GMB analytics and metrics
- **gmb_posts** - GMB posts and updates
- **gmb_qa** - Questions and answers
- **gmb_attributes** - Business attributes
- **place_searches** - Search history

### Use Cases:
- Business intelligence
- Competitor review analysis
- GMB performance tracking
- Local business discovery
- Reputation management

---

## 6. BRIGHTLOCAL DATABASE (`brightlocal.db`)

**Purpose**: Store local SEO data, citations, and reputation metrics

### Tables:
- **businesses** - Business information
- **local_rankings** - Current local search rankings
- **rank_history** - Historical ranking data
- **citations** - Business citations across directories
- **review_analytics** - Aggregated review data
- **seo_audits** - SEO audit results
- **competitor_analysis** - Competitor SEO metrics
- **reputation_scores** - Reputation scores by platform
- **directory_scan** - Directory presence data

### Use Cases:
- Local SEO tracking
- Citation building and management
- Reputation monitoring
- Competitor benchmarking
- SEO audit tracking

---

## 7. GOOGLE OAUTH DATABASE (`google_oauth.db`)

**Purpose**: Store user authentication, tokens, and session data

### Tables:
- **users** - User profiles
- **oauth_tokens** - Access and refresh tokens
- **token_history** - Token usage history
- **sessions** - Active user sessions
- **authorization_codes** - Temporary auth codes
- **oauth_state** - CSRF protection states
- **login_history** - Login attempt logs

### Use Cases:
- User authentication
- Session management
- Security tracking
- Token management
- Login analytics

---

## Database Helper Functions

Each database has a `db_helper.py` file with common functions:

### Standard Functions:
- `init_database()` - Initialize database with schema
- `save_*()` - Save data to specific tables
- `get_*()` - Retrieve data from tables
- `search_*()` - Search functions with filters
- `update_*()` - Update existing records
- `delete_*()` - Delete records

---

## Search Capabilities

### Advanced Search Features:
1. **Full-text search** on text fields
2. **Range queries** for numeric fields (income, population, etc.)
3. **Geospatial searches** for location-based queries
4. **Time-based queries** for historical data
5. **Aggregation queries** for analytics
6. **Join queries** across related tables

### Indexing:
All tables have appropriate indexes for fast searches on:
- Primary keys
- Foreign keys
- Frequently queried fields
- Location coordinates
- Date fields

---

## Initialization

To initialize all databases:

```bash
python /Users/udishkolnik/543/D.E.L.T.A/API_Abilities/init_all_databases.py
```

Or initialize individual databases:

```python
from API_Abilities.Mapbox.DB.db_helper import init_database as init_mapbox
from API_Abilities.SerpApi.DB.db_helper import init_database as init_serpapi
# ... etc

init_mapbox()
init_serpapi()
```

---

## Best Practices

1. **Cache First**: Always check database cache before making API calls
2. **Update Regularly**: Refresh stale data periodically
3. **Index Maintenance**: Rebuild indexes periodically for performance
4. **Backup**: Regular backups of all database files
5. **Clean Old Data**: Remove outdated cached data
6. **Transaction Safety**: Use transactions for batch operations

---

## File Locations

```
API_Abilities/
├── Mapbox/DB/
│   ├── schema.sql
│   ├── db_helper.py
│   └── mapbox.db
├── SerpApi/DB/
│   ├── schema.sql
│   ├── db_helper.py
│   └── serpapi.db
├── Meta_Ads/DB/
│   ├── schema.sql
│   ├── db_helper.py
│   └── meta_ads.db
├── US_Census/DB/
│   ├── schema.sql
│   ├── db_helper.py
│   └── us_census.db
├── Google_Places/DB/
│   ├── schema.sql
│   ├── db_helper.py
│   └── google_places.db
├── Brightlocal/DB/
│   ├── schema.sql
│   ├── db_helper.py
│   └── brightlocal.db
└── Google_OAuth/DB/
    ├── schema.sql
    ├── db_helper.py
    └── google_oauth.db
```

