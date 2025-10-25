# Missing Endpoints Research & Questions

**Date**: October 25, 2025  
**Status**: Research Phase - Need User Input Before Implementation

---

## 📋 Overview

We have 20 working endpoints. We need to research and plan 6 additional endpoints before implementation. This document outlines what each endpoint should do and asks critical questions.

---

## 1️⃣ Heatmap Data Aggregation Endpoint

### **Purpose**
Generate density data for visualizing heatmaps on the map (population density, income levels, business density, etc.)

### **What It Should Return**
GeoJSON with density values for each geographic area (ZIP codes or census tracts) within the map bounds.

### **Example Use Case**
User opens HeatmapBox, selects "Population Density" + "ZIP Codes" boundary type → Map shows color-coded ZIP codes based on population density.

### **Research Questions:**

#### Q1: What geographic granularity should heatmaps support?
- [ ] ZIP Codes only?
- [ ] Census Tracts?
- [ ] Counties?
- [ ] Custom grid (e.g., 1km x 1km squares)?
- [ ] All of the above?

#### Q2: What data types should be available for heatmaps?
Based on HeatmapBox component, it shows these categories:
- **Demographics**: Population, Age, Households, Income, Education, Diversity
  - Specific metrics: Population Density, Median Age, Household Size, Median Income, College Educated %, etc.
- **Custom Metrics**: User-defined data (Phase 8)
- **Points of Interest**: Business density
- **Competitor**: Competitor density
- **Demand/SEO**: Search volume

**Which ones should we implement first?**
- [ ] Priority 1: Population-based (use existing Census data)
- [ ] Priority 2: Business density (use Google Places)
- [ ] Priority 3: Custom metrics (Phase 8)

#### Q3: How should we aggregate the data?
**Option A**: Pre-calculate and cache
- Backend pre-calculates density values for all ZIP codes
- Fast response time
- Requires database or file storage
- Updates periodically (monthly/quarterly)

**Option B**: Calculate on-demand
- Backend calculates when requested
- Always up-to-date
- Slower response time
- No storage needed

**Which approach do you prefer?**

#### Q4: What should the API response look like?

**Option A - GeoJSON FeatureCollection**:
```json
{
  "type": "FeatureCollection",
  "features": [
    {
      "type": "Feature",
      "properties": {
        "zipcode": "94103",
        "value": 42319,
        "density": 15234.5,
        "normalized": 0.85
      },
      "geometry": {
        "type": "Polygon",
        "coordinates": [[[-122.4, 37.7], ...]]
      }
    }
  ]
}
```

**Option B - Simple Array**:
```json
{
  "data": [
    { "area_id": "94103", "value": 42319, "density": 15234.5 }
  ],
  "bounds": { "north": 37.8, "south": 37.7, "east": -122.3, "west": -122.5 }
}
```

**Which format is better for the frontend?**

#### Q5: Should we use the tract weighting methodology from the documentation?
The API_DOCUMENTATION_COMPLETE.md shows a sophisticated tract-weighted aggregation for ZIP codes. Should we:
- [ ] Use the documented tract weighting for accurate ZIP-level data?
- [ ] Use simple ZIP code tabulation areas from Census?
- [ ] Implement both and let user choose?

---

## 2️⃣ Batch Area Data Retrieval Endpoint

### **Purpose**
When user selects multiple ZIP codes at once (MassSelector), fetch demographics for all of them in one request instead of multiple individual requests.

### **What It Should Return**
Combined demographic data for multiple ZIP codes.

### **Example Use Case**
User clicks 5 different ZIP codes on the map → Backend returns demographics for all 5 in one response.

### **Research Questions:**

#### Q6: What's the maximum number of areas a user should be able to select at once?
- [ ] 10 ZIP codes?
- [ ] 25 ZIP codes?
- [ ] 50 ZIP codes?
- [ ] 100 ZIP codes?
- [ ] Unlimited?

**Consider**: Census API rate limits (500 requests/day)

#### Q7: What data should be included in batch responses?
**Option A - Full data for each**:
```json
{
  "areas": [
    {
      "zipcode": "94103",
      "demographics": { /* full data */ },
      "age_distribution": { /* full data */ },
      "housing": { /* full data */ }
    },
    { "zipcode": "94104", ... }
  ]
}
```

**Option B - Aggregated summary**:
```json
{
  "summary": {
    "total_population": 150000,
    "avg_income": 95000,
    "total_households": 65000
  },
  "by_area": [
    { "zipcode": "94103", "population": 42319, "income": 98237 },
    { "zipcode": "94104", "population": 35000, "income": 87000 }
  ]
}
```

**Which approach is more useful?**

#### Q8: Should this endpoint support different data types?
```
POST /api/v1/area/batch-data
Body: {
  "areas": [
    { "type": "zipcode", "code": "94103" },
    { "type": "zipcode", "code": "94104" }
  ],
  "data_types": ["demographics", "housing", "education"]
}
```

**Or should it always return everything?**

---

## 3️⃣ User Territory Storage (Database Required)

### **Purpose**
Save user-created territories (folders with saved areas/polygons) so they persist across sessions.

### **What It Stores**
- Folders (projects/collections)
- Areas (saved ZIP codes, drawn polygons)
- User preferences

### **Research Questions:**

#### Q9: What database should we use?
**Options**:
- [ ] **SQLite** - Simple file-based, no server needed, easy setup
- [ ] **PostgreSQL** - Full-featured, PostGIS for geo data, production-ready
- [ ] **MongoDB** - Document-based, flexible schema
- [ ] **File-based JSON** - No database, just save to files

**Your infrastructure preference?**

#### Q10: What should the database schema look like?

**Option A - Hierarchical (Projects → Folders → Areas)**:
```sql
CREATE TABLE projects (
  id UUID PRIMARY KEY,
  name TEXT,
  description TEXT,
  color TEXT,
  created_at TIMESTAMP
);

CREATE TABLE folders (
  id UUID PRIMARY KEY,
  project_id UUID REFERENCES projects(id),
  name TEXT,
  description TEXT,
  color TEXT,
  created_at TIMESTAMP
);

CREATE TABLE areas (
  id UUID PRIMARY KEY,
  folder_id UUID REFERENCES folders(id),
  name TEXT,
  type TEXT, -- 'zipcode', 'polygon', 'census_tract'
  code TEXT, -- ZIP code or tract ID
  geometry JSONB, -- GeoJSON for polygons
  visible BOOLEAN,
  color TEXT,
  created_at TIMESTAMP
);
```

**Option B - Flat (Just Territories)**:
```sql
CREATE TABLE territories (
  id UUID PRIMARY KEY,
  user_id TEXT,
  name TEXT,
  description TEXT,
  geometry JSONB,
  color TEXT,
  metadata JSONB,
  created_at TIMESTAMP
);
```

**Which schema fits your needs better?**

#### Q11: Do you need multi-user support?
- [ ] Yes - Add `user_id` field, implement authentication
- [ ] No - Single-user app, skip auth for now
- [ ] Later - Implement without auth, add later

#### Q12: Should territories be shareable between users?
- [ ] Yes - Add sharing/permissions system
- [ ] No - Private to each user
- [ ] Later - Add sharing in Phase 9+

---

## 4️⃣ Custom User Data Upload (Database Required)

### **Purpose**
Allow users to upload their own CSV/JSON data and visualize it on the map (e.g., customer addresses, sales data, custom metrics).

### **What It Should Do**
- Accept file uploads (CSV, JSON, Excel)
- Parse and validate data
- Store in database
- Make available for heatmaps and analysis

### **Research Questions:**

#### Q13: What file formats should we support?
- [ ] CSV (most common)
- [ ] JSON
- [ ] Excel (.xlsx)
- [ ] GeoJSON
- [ ] All of the above

#### Q14: How should we handle geocoding?
If user uploads data with addresses but no coordinates:
- [ ] Auto-geocode using Google Geocoding API (costs money per request)
- [ ] Require user to provide lat/lng in their file
- [ ] Offer geocoding as optional paid feature
- [ ] Use free geocoding service (Nominatim, slower and less accurate)

#### Q15: What's the maximum file size?
- [ ] 1 MB (few thousand records)
- [ ] 10 MB (tens of thousands)
- [ ] 100 MB (hundreds of thousands)
- [ ] 1 GB (millions of records)

**Consider**: Server memory, parsing time, storage costs

#### Q16: How should uploaded data be structured?

**Expected CSV format**:
```csv
name,value,latitude,longitude,category
"Location 1",1500,37.7749,-122.4194,"Type A"
"Location 2",2300,37.7849,-122.4294,"Type B"
```

**Or allow flexible schema**:
```csv
address,sales_2024,customer_count
"123 Main St, SF, CA 94103",50000,150
"456 Oak Ave, SF, CA 94110",75000,220
```

**Should we require a specific format or be flexible?**

#### Q17: How long should we store uploaded data?
- [ ] Forever (until user deletes)
- [ ] 30 days
- [ ] 90 days
- [ ] 1 year

---

## 5️⃣ Boundary GeoJSON Endpoint

### **Purpose**
Provide GeoJSON polygon boundaries for ZIP codes, census tracts, counties, etc., so we can draw them on the map.

### **What It Should Return**
GeoJSON polygons for requested geographic areas.

### **Research Questions:**

#### Q18: Where should we get boundary data from?
**Options**:
- [ ] **Census TIGER/Line Shapefiles** (free, official, large files)
- [ ] **Mapbox Boundaries API** (paid, fast, easy)
- [ ] **OpenStreetMap** (free, community-maintained)
- [ ] **Pre-processed and stored in our database** (fast, requires setup)

#### Q19: What boundary types should we support?
- [ ] ZIP Code Tabulation Areas (ZCTAs)
- [ ] Census Tracts
- [ ] Counties
- [ ] States
- [ ] Custom boundaries (user-uploaded)
- [ ] All of the above

#### Q20: Should we simplify geometries for performance?

**Full resolution ZIP code polygons can be 100KB+ each!**

- [ ] Yes - Simplify to reduce size (e.g., Douglas-Peucker algorithm)
- [ ] No - Use full resolution
- [ ] Offer both (full for download, simplified for display)

#### Q21: Should we cache boundaries?

**Option A**: Generate on-demand from Census files
- No storage needed
- Slow (multiple seconds per request)

**Option B**: Pre-process and store in database
- Fast (milliseconds)
- Requires database and storage space (~500MB for all US ZIP codes)

**Option C**: Store as static files
- Fast
- No database needed
- Larger deployment size

**Which approach fits your infrastructure?**

---

## 6️⃣ Detailed Demographics (403 Variables)

### **Purpose**
Implement the complete tract-weighted aggregation for all 403 demographic variables documented in API_DOCUMENTATION_COMPLETE.md.

### **What It Should Return**
Comprehensive demographic data using the documented tract-weighting methodology.

### **Research Questions:**

#### Q22: Should we implement all 403 variables at once?
- [ ] Yes - Build complete endpoint now
- [ ] No - Start with core variables (50-100), add more later
- [ ] Phased - Implement by category:
  - Phase 1: Core demographics (population, age, income) - 50 variables
  - Phase 2: Housing and households - 100 variables
  - Phase 3: Employment and occupation - 130 variables
  - Phase 4: Remaining specialized variables - 123 variables

#### Q23: The documentation provides Python code. Should we:
- [ ] Port the Python code to JavaScript (for Node.js backend)
- [ ] Create a Python microservice (separate Python API)
- [ ] Use existing Python code as-is (add Python backend alongside Node.js)
- [ ] Rewrite in Node.js using the methodology

#### Q24: How should we expose 403 variables to the frontend?

**Option A - Single massive endpoint**:
```
GET /api/v1/zipcode/demographics-complete?zipcode=94103
Returns: All 403 variables in one response (large payload ~100KB)
```

**Option B - Category-based endpoints**:
```
GET /api/v1/zipcode/demographics-population?zipcode=94103
GET /api/v1/zipcode/demographics-housing?zipcode=94103
GET /api/v1/zipcode/demographics-employment?zipcode=94103
```

**Option C - Variable selection**:
```
GET /api/v1/zipcode/demographics-detailed?zipcode=94103&variables=B01001001,B19013001
Returns: Only requested variables
```

**Which approach is best for UI performance?**

#### Q25: Should we pre-calculate and cache tract-weighted values?
The tract weighting calculation requires:
1. Fetching data for 17 tracts
2. Applying overlap percentages
3. Summing weighted values

**This takes time and API calls!**

- [ ] Pre-calculate for common ZIP codes, store in database
- [ ] Calculate on-demand, cache for 24 hours
- [ ] Always calculate fresh (slow but always current)

#### Q26: Which ZIP codes should we prioritize?
The documentation focuses on ZIP 94103. Should we:
- [ ] Implement for all US ZIP codes (~43,000 ZIPs)
- [ ] Start with San Francisco ZIPs only (~30 ZIPs)
- [ ] Implement methodology, calculate on-demand for any ZIP
- [ ] Focus on top 1,000 most populous ZIPs

---

## 🎯 Implementation Priority Recommendations

Based on frontend needs, here's my suggested order:

### **Phase 7 (Week 5) - Heatmap**
**Must Have**: Endpoint #1 (Heatmap Data Aggregation)
- Start with simple: Population density by ZIP code
- Use existing Census endpoint data
- Return GeoJSON format
- No database needed initially

**Questions Needed**: Q1-Q5

---

### **Phase 8 (Week 6) - Multiple Areas**
**Must Have**: Endpoint #2 (Batch Area Data)
- Support 10-25 ZIP codes max
- Return full data for each
- No database needed

**Questions Needed**: Q6-Q8

---

### **Phase 9 (Week 7) - Persistence**
**Must Have**: Endpoint #3 (User Territory Storage)
- Choose database (SQLite for simplicity?)
- Hierarchical schema (Projects → Folders → Areas)
- Single-user for now, add auth later

**Questions Needed**: Q9-Q12

---

### **Phase 10 (Week 8+) - Advanced Features**
**Nice to Have**:
- Endpoint #4 (Custom Data Upload) - Q13-Q17
- Endpoint #5 (Boundary GeoJSON) - Q18-Q21
- Endpoint #6 (Detailed Demographics) - Q22-Q26

---

## ✅ Decision Template

Please answer these questions in order of priority:

### **IMMEDIATE (For Phase 7 - Heatmap)**:
1. Q1: Geographic granularity? → **Your answer: _______**
2. Q2: Data types priority? → **Your answer: _______**
3. Q3: Pre-calculate or on-demand? → **Your answer: _______**
4. Q4: GeoJSON or Array format? → **Your answer: _______**
5. Q5: Use tract weighting? → **Your answer: _______**

### **SOON (For Phase 8 - Batch Data)**:
6. Q6: Max areas to select? → **Your answer: _______**
7. Q7: Full data or summary? → **Your answer: _______**
8. Q8: Specify data types or all? → **Your answer: _______**

### **LATER (For Phase 9 - Database)**:
9. Q9: Which database? → **Your answer: _______**
10. Q10: Hierarchical or flat schema? → **Your answer: _______**
11. Q11: Multi-user support? → **Your answer: _______**
12. Q12: Shareable territories? → **Your answer: _______**

### **OPTIONAL (Phase 10+)**:
13-26: We can discuss these when we get to Phase 10.

---

## 🚀 **Ready to Start Phase 1 (80% Implementation)**

While you review these questions, I can start implementing:
- ✅ UI framework setup (shadcn/ui, Tailwind)
- ✅ Component structure
- ✅ Demographics panel with existing 20 endpoints
- ✅ Points of Interest panel
- ✅ All other panels with existing backend
- ✅ Map tools (draw, measure, travel time)

**Should I proceed with Phase 1 while you review the questions?**

This way, when you answer the questions, I'll be ready to immediately implement the missing endpoints in the appropriate phases.
