# 📚 D.E.L.T.A 2 - Complete API Reference

## 🎯 **Overview**

D.E.L.T.A 2 provides a comprehensive REST API for location intelligence and market analysis. All endpoints return **100% real-time data** from authoritative sources including US Census Bureau, Google Places, SerpAPI, and Mapbox.

**Base URL:** `http://localhost:8001/api/v1`

---

## 📊 **US Census Bureau Integration**

### **State-Level Demographics**

#### `GET /census/demographics`
Retrieve comprehensive demographic data for a state.

**Parameters:**
- `state` (string, required): FIPS state code (e.g., "53" for Washington)

**Example Request:**
```http
GET /api/v1/census/demographics?state=53
```

**Response:**
```json
{
  "status": "success",
  "data": {
    "name": "Washington",
    "total_population": 7705281,
    "median_household_income": 78200,
    "median_age": 37.7,
    "employment_rate": 94.2,
    "unemployment_rate": 5.8,
    "median_home_value": 397600,
    "median_gross_rent": 1418
  },
  "timestamp": "2025-01-09T20:30:00.000Z"
}
```

**Census Variables Used:**
- `B01003_001E` - Total population
- `B19013_001E` - Median household income
- `B01002_001E` - Median age
- `B23025_004E` - Employed population
- `B23025_005E` - Unemployed population
- `B25077_001E` - Median home value
- `B25064_001E` - Median gross rent

---

#### `GET /census/age-distribution`
Get detailed age distribution data for a state.

**Parameters:**
- `state` (string, required): FIPS state code

**Example Request:**
```http
GET /api/v1/census/age-distribution?state=53
```

**Response:**
```json
{
  "status": "success",
  "data": {
    "name": "Washington",
    "age_groups": {
      "0_17": "21.2",
      "18_24": "8.1",
      "25_34": "14.3",
      "35_44": "12.8",
      "45_54": "12.9",
      "55_64": "13.2",
      "65_plus": "17.5"
    }
  },
  "timestamp": "2025-01-09T20:30:00.000Z"
}
```

**Census Variables Used (47 total):**
- `B01001_003E` through `B01001_049E` - Detailed male/female age groups
- Calculated percentages for standard age brackets

---

#### `GET /census/gender`
Retrieve gender distribution for a state.

**Parameters:**
- `state` (string, required): FIPS state code

**Example Request:**
```http
GET /api/v1/census/gender?state=53
```

**Response:**
```json
{
  "status": "success",
  "data": {
    "name": "Washington",
    "gender_breakdown": {
      "male": "50.1",
      "female": "49.9"
    }
  },
  "timestamp": "2025-01-09T20:30:00.000Z"
}
```

**Census Variables Used:**
- `B01001_002E` - Male population
- `B01001_026E` - Female population

---

#### `GET /census/housing`
Get housing statistics for a state.

**Parameters:**
- `state` (string, required): FIPS state code

**Example Request:**
```http
GET /api/v1/census/housing?state=53
```

**Response:**
```json
{
  "status": "success",
  "data": {
    "name": "Washington",
    "total_housing_units": 3123456,
    "owner_occupied": 2134567,
    "renter_occupied": 989889,
    "ownership_rate": "68.3",
    "rental_rate": "31.7",
    "median_home_value": 397600,
    "median_gross_rent": 1418
  },
  "timestamp": "2025-01-09T20:30:00.000Z"
}
```

**Census Variables Used:**
- `B25003_001E` - Total housing units
- `B25003_002E` - Owner occupied
- `B25003_003E` - Renter occupied
- `B25077_001E` - Median home value
- `B25064_001E` - Median gross rent

---

## 📍 **ZIP Code Analysis**

### **ZIP Code Demographics**

#### `GET /zipcode/demographics`
Retrieve demographic data for a specific ZIP code.

**Parameters:**
- `zipcode` (string, required): 5-digit ZIP code

**Example Request:**
```http
GET /api/v1/zipcode/demographics?zipcode=98101
```

**Response:**
```json
{
  "status": "success",
  "data": {
    "name": "ZIP Code 98101",
    "total_population": 12345,
    "median_household_income": 95000,
    "median_home_value": 650000
  },
  "timestamp": "2025-01-09T20:30:00.000Z"
}
```

---

#### `GET /zipcode/age-distribution`
Get age distribution for a ZIP code.

**Parameters:**
- `zipcode` (string, required): 5-digit ZIP code

**Example Request:**
```http
GET /api/v1/zipcode/age-distribution?zipcode=98101
```

**Response:**
```json
{
  "status": "success",
  "data": {
    "name": "ZIP Code 98101",
    "age_groups": {
      "0_17": "15.2",
      "18_24": "12.8",
      "25_34": "25.3",
      "35_44": "18.7",
      "45_54": "12.1",
      "55_64": "9.8",
      "65_plus": "6.1"
    }
  },
  "timestamp": "2025-01-09T20:30:00.000Z"
}
```

---

### **Enhanced ZIP Code Variables**

#### `GET /zipcode/economic`
Economic indicators for a ZIP code.

**Parameters:**
- `zipcode` (string, required): 5-digit ZIP code

**Census Variables Used:**
- `B17001_002E` - Population below poverty level
- `B17001_001E` - Total population for poverty calculation
- `B08134_011E` through `B08134_021E` - Travel time to work distribution

---

#### `GET /zipcode/housing`
Housing analysis for a ZIP code.

**Parameters:**
- `zipcode` (string, required): 5-digit ZIP code

**Census Variables Used:**
- `B25002_001E` - Total housing units
- `B25002_002E` - Occupied housing units
- `B25002_003E` - Vacant housing units
- `B25003_001E` through `B25003_003E` - Ownership breakdown

---

#### `GET /zipcode/social`
Social demographics for a ZIP code.

**Parameters:**
- `zipcode` (string, required): 5-digit ZIP code

**Census Variables Used:**
- `B27001_002E` - Population without health insurance
- `B27001_001E` - Total population for health insurance calculation
- `B18101_002E` - Population with disability
- `B18101_001E` - Total population for disability calculation
- `B21001_002E` - Veteran population
- `B21001_001E` - Total population for veteran calculation

---

#### `GET /zipcode/transportation-infrastructure`
Transportation and commute data for a ZIP code.

**Parameters:**
- `zipcode` (string, required): 5-digit ZIP code

**Census Variables Used:**
- `B08134_001E` - Total workers 16+
- `B08134_011E` through `B08134_021E` - Commute time distribution

---

#### `GET /zipcode/education`
Educational attainment for a ZIP code.

**Parameters:**
- `zipcode` (string, required): 5-digit ZIP code

**Census Variables Used:**
- `B15003_022E` through `B15003_025E` - Educational attainment levels

---

## 🏢 **Business Intelligence**

### **Google Places Integration**

#### `GET /google-places/search`
Search for businesses using Google Places API.

**Parameters:**
- `query` (string, optional): Business type to search (default: "motor boat")
- `location` (string, optional): Lat,lng coordinates (default: "47.6062,-122.3321")
- `radius` (number, optional): Search radius in meters (default: 50000)

**Example Request:**
```http
GET /api/v1/google-places/search?query=motor boat&location=47.6062,-122.3321&radius=50000
```

**Response:**
```json
{
  "status": "success",
  "data": {
    "query": "motor boat",
    "location": "47.6062,-122.3321",
    "radius": 50000,
    "results": [
      {
        "place_id": "ChIJ...",
        "name": "Seattle Yacht Sales",
        "rating": 4.5,
        "user_ratings_total": 127,
        "vicinity": "1234 Harbor Ave, Seattle, WA",
        "types": ["boat_dealer", "establishment"],
        "geometry": {
          "location": {
            "lat": 47.6123,
            "lng": -122.3456
          }
        },
        "price_level": 3
      }
    ],
    "total_results": 20,
    "data_source": "Google Places API"
  },
  "timestamp": "2025-01-09T20:30:00.000Z"
}
```

---

#### `GET /zipcode/businesses`
Search for businesses within a ZIP code area.

**Parameters:**
- `zipcode` (string, required): 5-digit ZIP code
- `query` (string, optional): Business type (default: "motor boat")
- `radius` (number, optional): Search radius in meters (default: 50000)

**Example Request:**
```http
GET /api/v1/zipcode/businesses?zipcode=98101&query=motor boat&radius=50000
```

**Process:**
1. Geocodes ZIP code to get center coordinates
2. Searches for businesses within radius
3. Returns business listings with location data

---

#### `GET /businesses/locations`
Get business locations optimized for mapping.

**Parameters:**
- `query` (string, optional): Business type (default: "motor boat")
- `location` (string, optional): Lat,lng coordinates
- `radius` (number, optional): Search radius in meters (default: 50000)

**Response includes:**
- Business name, rating, review count
- Exact coordinates for mapping
- Distance from search center
- Business types and price levels

---

## 🔍 **Search Intelligence**

### **SerpAPI Integration**

#### `GET /serpapi/search`
Get search trends and keyword data using SerpAPI.

**Parameters:**
- `query` (string, optional): Search term (default: "motor boat")
- `location` (string, optional): Geographic location (default: "Seattle, WA")

**Example Request:**
```http
GET /api/v1/serpapi/search?query=motor boat&location=Seattle, WA
```

**Response:**
```json
{
  "status": "success",
  "data": {
    "query": "motor boat",
    "location": "Seattle, WA",
    "search_volume": 8500,
    "average_cpc": 2.45,
    "competition_level": 0.75,
    "related_searches": [
      {
        "keyword": "motor boat sales seattle",
        "monthly_searches": 1200,
        "cpc": 3.20
      },
      {
        "keyword": "boat dealership seattle",
        "monthly_searches": 890,
        "cpc": 2.80
      }
    ],
    "trends": {
      "growing": ["electric boat", "sustainable boating"],
      "declining": ["gas motor boat"],
      "stable": ["boat maintenance", "marine services"]
    },
    "data_source": "SerpAPI"
  },
  "timestamp": "2025-01-09T20:30:00.000Z"
}
```

---

## 🗺️ **Geographic Services**

### **Mapbox Integration**

#### `GET /zipcode/coordinates`
Get ZIP code coordinates and boundary data.

**Parameters:**
- `zipcode` (string, required): 5-digit ZIP code

**Example Request:**
```http
GET /api/v1/zipcode/coordinates?zipcode=98101
```

**Response:**
```json
{
  "status": "success",
  "data": {
    "zipcode": "98101",
    "center": {
      "lat": 47.6123,
      "lng": -122.3456
    },
    "formatted_address": "98101, Seattle, WA, USA",
    "bounds": {
      "northeast": {
        "lat": 47.6200,
        "lng": -122.3300
      },
      "southwest": {
        "lat": 47.6050,
        "lng": -122.3600
      }
    },
    "data_source": "Google Geocoding API"
  },
  "timestamp": "2025-01-09T20:30:00.000Z"
}
```

---

#### `GET /zipcode/isochrone`
Generate travel time polygons for a ZIP code.

**Parameters:**
- `zipcode` (string, required): 5-digit ZIP code
- `minutes` (number, optional): Travel time in minutes (default: 10)
- `mode` (string, optional): Travel mode - driving, walking, cycling (default: "driving")

**Example Request:**
```http
GET /api/v1/zipcode/isochrone?zipcode=98101&minutes=15&mode=driving
```

**Response:**
```json
{
  "status": "success",
  "data": {
    "zipcode": "98101",
    "minutes": 15,
    "mode": "driving",
    "isochrone_polygon": {
      "type": "Feature",
      "geometry": {
        "type": "Polygon",
        "coordinates": [[[-122.4, 47.6], [-122.3, 47.6], ...]]
      },
      "properties": {
        "contour": 15,
        "color": "#00D9FF"
      }
    },
    "data_source": "Mapbox Isochrone API"
  },
  "timestamp": "2025-01-09T20:30:00.000Z"
}
```

---

## 📊 **Heatmap Data**

#### `GET /heatmap/buttons`
Get available heatmap layers.

**Example Request:**
```http
GET /api/v1/heatmap/buttons
```

**Response:**
```json
{
  "status": "success",
  "data": {
    "layers": [
      {
        "id": "business_density",
        "name": "Business Density",
        "active": true
      },
      {
        "id": "competition",
        "name": "Competition",
        "active": true
      },
      {
        "id": "opportunity",
        "name": "Opportunity",
        "active": false
      }
    ]
  },
  "timestamp": "2025-01-09T20:30:00.000Z"
}
```

---

## 🔧 **System Endpoints**

#### `GET /status`
Check API server status.

**Example Request:**
```http
GET /api/v1/status
```

**Response:**
```json
{
  "status": "success",
  "data": {
    "server": "D.E.L.T.A 2 REAL API Server",
    "status": "running",
    "real_apis": true,
    "mock_data": false,
    "timestamp": "2025-01-09T20:30:00.000Z"
  }
}
```

---

#### `GET /`
Get server information and available endpoints.

**Example Request:**
```http
GET /
```

**Response:**
```json
{
  "message": "D.E.L.T.A 2 REAL API Server - NO MOCK DATA",
  "status": "running",
  "version": "2.0",
  "note": "ALL DATA FROM REAL APIS - NO FAKE DATA",
  "endpoints": {
    "census": "/api/v1/census/*",
    "google_places": "/api/v1/google-places/*",
    "serpapi": "/api/v1/serpapi/*",
    "heatmap": "/api/v1/heatmap/buttons",
    "zipcode": "/api/v1/zipcode/*"
  }
}
```

---

## 🚨 **Error Handling**

All endpoints return consistent error responses:

```json
{
  "status": "error",
  "error": "Error description",
  "timestamp": "2025-01-09T20:30:00.000Z"
}
```

**Common Error Codes:**
- `400` - Bad Request (invalid parameters)
- `404` - Endpoint not found
- `500` - Internal server error
- `503` - External API unavailable

---

## 📈 **Rate Limits**

**Current Limits:**
- **Census API**: 500 requests/day (free tier)
- **Google Places**: 100,000 requests/day (with billing)
- **SerpAPI**: 100 searches/month (free tier)
- **Mapbox**: 50,000 requests/month (free tier)

**Recommendations:**
- Implement client-side caching
- Use parallel requests efficiently
- Monitor API usage in production

---

## 🔐 **Authentication**

**Current Implementation:**
- API keys stored in environment variables
- No user authentication required for demo
- CORS enabled for all origins

**Production Considerations:**
- Implement API key validation
- Add rate limiting per client
- Secure API key storage
- User authentication for enterprise features

---

## 📊 **Data Aggregation Examples**

### **Area Analysis Flow**
1. **Click coordinates** → Geocode to ZIP code
2. **Fetch demographics** → Census ZIP code data
3. **Fetch businesses** → Google Places search
4. **Fetch search trends** → SerpAPI analysis
5. **Calculate distances** → Business proximity analysis
6. **Generate insights** → Opportunity scoring

### **Competitor Analysis Flow**
1. **Business search** → Google Places results
2. **Rating aggregation** → Average rating calculation
3. **Review analysis** → Total review count
4. **Distance calculation** → Proximity from center
5. **Ranking algorithm** → Competitor scoring

### **Market Opportunity Scoring**
```typescript
opportunityScore = (
  competitionScore * 0.3 +
  demandScore * 0.4 +
  spendingPowerScore * 0.3
) / 100
```

**Where:**
- `competitionScore` = 100 - (businessCount * 2)
- `demandScore` = (searchVolume / 1000) * 10
- `spendingPowerScore` = medianIncome / 1000

---

## 🎯 **Best Practices**

### **API Usage**
1. **Use parallel requests** for multiple data sources
2. **Implement caching** for frequently accessed data
3. **Handle errors gracefully** with fallback strategies
4. **Monitor rate limits** to avoid API blocking
5. **Validate input parameters** before API calls

### **Data Processing**
1. **Parse Census data carefully** - arrays can be complex
2. **Validate coordinates** before geocoding
3. **Handle null/undefined values** in API responses
4. **Use appropriate data types** for calculations
5. **Implement data transformation** for frontend compatibility

### **Performance Optimization**
1. **Batch similar requests** when possible
2. **Use appropriate radius values** for business searches
3. **Cache ZIP code coordinates** to avoid repeated geocoding
4. **Implement request debouncing** for user interactions
5. **Use pagination** for large result sets

---

## 🔮 **Future API Enhancements**

### **Planned Endpoints**
- `/api/v1/analytics/predictions` - ML-powered market predictions
- `/api/v1/export/reports` - PDF/Excel report generation
- `/api/v1/social/trends` - Social media sentiment analysis
- `/api/v1/traffic/real-time` - Live traffic and congestion data
- `/api/v1/weather/impact` - Climate impact on business performance

### **Enhanced Data Sources**
- **Social Media APIs** - Twitter, Instagram location data
- **Traffic APIs** - Real-time traffic and road conditions
- **Weather APIs** - Climate data and seasonal patterns
- **Economic APIs** - Stock market, GDP, employment indicators
- **Real Estate APIs** - Property values, rental rates, market trends

---

This API reference provides complete documentation for all D.E.L.T.A 2 endpoints and data aggregation capabilities. All data comes from real, authoritative sources with no mock data or placeholders.
