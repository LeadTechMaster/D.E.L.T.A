# API Abilities - Master List

This document provides a comprehensive list of all API abilities organized by service. Each file handles ONE specific function.

---

## 1. MAPBOX API
**Purpose**: Interactive maps, geocoding, routing, satellite imagery

### Files:
1. **geocoding.py** - Convert addresses to geographic coordinates (lat/lng)
2. **reverse_geocoding.py** - Convert coordinates to addresses
3. **routing.py** - Get directions and routes between points
4. **satellite_imagery.py** - Fetch satellite and aerial imagery tiles
5. **street_maps.py** - Get street map tiles and styles
6. **distance_matrix.py** - Calculate travel times and distances between multiple points
7. **isochrone.py** - Get areas reachable within specified time from a location

---

## 2. SERPAPI
**Purpose**: Google search results, trends, local businesses, news, images, keyword research

### Files:
1. **google_search.py** - Perform general Google search
2. **local_businesses.py** - Search for local businesses via Google Maps
3. **search_trends.py** - Get Google search trends and related searches
4. **news_search.py** - Search Google News results
5. **image_search.py** - Search Google Images
6. **shopping_search.py** - Search Google Shopping results
7. **related_searches.py** - Get related search queries for a keyword
8. **keyword_search_volume.py** - Get search volume data for keywords
9. **keyword_suggestions.py** - Get keyword suggestions and related keywords
10. **keyword_difficulty.py** - Analyze keyword competition and difficulty
11. **people_also_ask.py** - Get "People Also Ask" questions for keywords
12. **autocomplete_suggestions.py** - Get Google autocomplete/suggest keywords
13. **local_pack_results.py** - Get local pack (3-pack) results for keywords
14. **serp_analysis.py** - Analyze search engine results page (SERP) features
15. **competitor_keywords.py** - Find keywords competitors are ranking for

---

## 3. META ADS LIBRARY
**Purpose**: Facebook/Instagram ad data, competitor analysis, spend insights

### Files:
1. **ad_search.py** - Search for ads by keywords or advertiser
2. **competitor_ads.py** - Get competitor ad data and strategies
3. **ad_spend_insights.py** - Analyze ad spending patterns and budgets
4. **ad_creatives.py** - Get ad creative assets (images, videos, copy)
5. **ad_targeting.py** - Get ad targeting information and demographics
6. **ad_performance.py** - Get ad performance metrics and reach
7. **active_ads.py** - Get currently active ads by page or advertiser

---

## 4. US CENSUS BUREAU
**Purpose**: Population demographics, economic data, housing statistics

### Files:
1. **population_data.py** - Get population statistics by area
2. **demographic_data.py** - Get age, gender, race demographics
3. **economic_data.py** - Get income, employment, and economic statistics
4. **housing_data.py** - Get housing statistics and home values
5. **education_data.py** - Get education levels and school enrollment
6. **poverty_data.py** - Get poverty statistics and household assistance
7. **business_patterns.py** - Get business demographics and industry data
8. **commute_data.py** - Get commute patterns and transportation statistics

---

## 5. GOOGLE PLACES API & GOOGLE MY BUSINESS (GMB)
**Purpose**: Business listings, reviews, photos, hours, pricing, GMB management

### Files:
1. **business_search.py** - Search for businesses by type or keyword
2. **place_details.py** - Get detailed information about a specific place
3. **reviews.py** - Get customer reviews and ratings for a place
4. **photos.py** - Get photos of a place
5. **hours.py** - Get operating hours for a place
6. **nearby_search.py** - Find places near a location
7. **autocomplete.py** - Get place suggestions as user types
8. **contact_info.py** - Get phone, website, and contact details

### Google My Business (GMB) Management:
9. **gmb_listing_info.py** - Get GMB listing details and profile information
10. **gmb_insights.py** - Get GMB insights, views, and engagement metrics
11. **gmb_reviews_management.py** - Manage GMB reviews (read, reply, delete)
12. **gmb_posts.py** - Create, read, update, delete GMB posts
13. **gmb_questions_answers.py** - Manage GMB Q&A section
14. **gmb_media.py** - Upload and manage GMB photos and videos
15. **gmb_verification.py** - Handle GMB listing verification process
16. **gmb_attributes.py** - Manage GMB business attributes (accessibility, amenities)

---

## 6. BRIGHTLOCAL API
**Purpose**: Local SEO data, citations, reviews, rankings, keyword tracking

### Files:
1. **local_rankings.py** - Get local search rankings for businesses
2. **citations.py** - Get business citations and directory listings
3. **reviews_analysis.py** - Analyze reviews across multiple platforms
4. **seo_audit.py** - Perform local SEO audit
5. **competitor_analysis.py** - Analyze competitor local SEO performance
6. **reputation_score.py** - Get overall reputation score for a business
7. **directory_scan.py** - Scan business presence across directories
8. **keyword_rank_tracker.py** - Track keyword rankings over time for local searches

---

## 7. GOOGLE OAUTH
**Purpose**: Authentication and user data

### Files:
1. **authenticate.py** - Handle user authentication flow
2. **user_profile.py** - Get authenticated user profile data
3. **refresh_token.py** - Refresh expired access tokens
4. **revoke_token.py** - Revoke access tokens and logout
5. **validate_token.py** - Validate token status and expiration
6. **exchange_code.py** - Exchange authorization code for tokens

---

## Summary

**Total API Services**: 7
**Total API Functions**: 68 individual files
**Total Databases**: 7 (one per service)

### File Counts by Service:
- Mapbox: 7 API files
- SerpApi: 15 API files (includes extensive keyword research)
- Meta Ads: 7 API files
- US Census: 8 API files
- Google Places & GMB: 16 API files (includes GMB management)
- Brightlocal: 8 API files (includes keyword tracking)
- Google OAuth: 6 API files

Each file is designed to handle ONE specific API function, making the codebase modular, maintainable, and easy to expand.

---

## Database Structure

Each API service has its own **DB folder** with:
1. **schema.sql** - Database table definitions
2. **db_helper.py** - Helper functions for database operations
3. **{service}.db** - SQLite database file (created after initialization)

### Database Features:
- ✅ **Caching** - Reduce API calls by storing results
- ✅ **Search capabilities** - Full-text and advanced search
- ✅ **Historical data** - Track changes over time
- ✅ **Offline access** - Access data without API calls
- ✅ **Analytics** - Query and analyze stored data

See `DATABASE_STRUCTURE.md` for complete documentation.

---

## Initialization

To initialize all databases:
```bash
python /Users/udishkolnik/543/D.E.L.T.A/API_Abilities/init_all_databases.py
```

---

### Next Steps:
1. ✓ Database schemas created for all services
2. ✓ Database helper functions templated
3. TODO: Implement actual API calls in each file
4. TODO: Connect API files to database helpers
5. TODO: Add error handling and response validation
6. TODO: Add environment variable loading for API keys
7. TODO: Add unit tests for each function
8. TODO: Add rate limiting
9. TODO: Implement cache-first logic

