# D.E.L.T.A 2 - Complete System Overview

## 🎯 What You Have

A **Location Intelligence & Business Analysis Platform** with real-time data from multiple sources.

---

## 📁 System Architecture

### Backend (`/backend`)
- **Language**: Python 3
- **Framework**: FastAPI + Uvicorn
- **Port**: 8001
- **Entry Point**: `real_api_server.py`
- **Database**: SQLite at `/Users/udishkolnik/Downloads/D.E.L.T.A/DB/real_data.db`

### Frontend (`/frontend`)
- **Framework**: React 19 + TypeScript
- **Build Tool**: Vite (Rolldown)
- **State Management**: Redux Toolkit
- **UI Framework**: Material-UI (MUI)
- **Maps**: Mapbox GL JS
- **Port**: 5173

### Heatmap System (`/HEATMAP`)
- Business competition analysis
- Demographic density mapping
- Foot traffic patterns
- Market opportunity scoring
- Income/wealth distribution
- Review power analysis

---

## 🔑 Live APIs Integrated

### 1. **Mapbox** (Maps & Geocoding)
- Interactive maps
- Geocoding & reverse geocoding
- Autocomplete
- Isochrone (travel time areas)
- Directions & routing
- API Key: `pk.eyJ1Ijoic3VwcG9ydG1vdmVkaW4...`

### 2. **Google Places** (Business Data)
- Business search
- Ratings & reviews
- Hours & pricing
- Business density analysis
- API Key: `AIzaSyAzyKYxbA7HWHTU9UV9Z-ELGRQTTeN9dkw`

### 3. **US Census Bureau** (Demographics)
- Population statistics
- Age distribution
- Gender breakdown
- Employment data
- Housing statistics
- Income data
- API Key: `ab4c49e507688c08e5346543c6d355a2e6b37c8c`

### 4. **SerpAPI** (Search Intelligence)
- Google search results
- Local business data
- Competitor research
- Trends & insights
- API Key: `850faf17d2e379f54ffdd1e300daaa7bdb1dee8abdc2536f1de3430d137e563c`

### 5. **Meta Ads Library**
- Facebook/Instagram ad data
- Competitor analysis
- Ad spend insights
- Access Token: `EAA40mj0BFQYBPXUVZAWCEv0ZBFOXjEmLUd3o26dfD1yz...`

### 6. **BrightLocal** (Local SEO)
- Citations
- Rankings
- Reviews
- API Key: `2efdc9f13ec8a5b8fc0d83cddba7f5cc671ca3ec`

---

## 🛠️ How to Run

### Option 1: Using the Start Script
```bash
cd "/Users/udishkolnik/Downloads/D.E.L.T.A 2"
./START_SYSTEM.sh
```

### Option 2: Manual Start

**Terminal 1 - Backend:**
```bash
cd "/Users/udishkolnik/Downloads/D.E.L.T.A 2/backend"
python3 real_api_server.py
```

**Terminal 2 - Frontend:**
```bash
cd "/Users/udishkolnik/Downloads/D.E.L.T.A 2/frontend"
npm run dev
```

### Option 3: Background Mode
```bash
# Backend
cd "/Users/udishkolnik/Downloads/D.E.L.T.A 2/backend"
nohup python3 real_api_server.py > backend.log 2>&1 &

# Frontend
cd "/Users/udishkolnik/Downloads/D.E.L.T.A 2/frontend"
nohup npm run dev > frontend.log 2>&1 &
```

---

## 🌐 Access URLs

- **Frontend Dashboard**: http://localhost:5173
- **Backend API**: http://localhost:8001
- **API Documentation**: http://localhost:8001/docs (Swagger UI)
- **Alternative API Docs**: http://localhost:8001/redoc (ReDoc)

---

## 📡 Available API Endpoints

### Mapbox Endpoints
```
GET /api/v1/mapbox/geocode?location=Seattle,WA
GET /api/v1/mapbox/autocomplete?query=Seattle
GET /api/v1/mapbox/isochrone?lat=47.6062&lng=-122.3321&minutes=10&mode=driving
GET /api/v1/mapbox/directions?start_lat=47.6&start_lng=-122.3&end_lat=47.7&end_lng=-122.4&mode=driving
GET /api/v1/mapbox/reverse-geocode?lat=47.6062&lng=-122.3321
```

### Google Places Endpoints
```
GET /api/v1/google-places/search?query=restaurants&location=Seattle,WA&radius=5000
GET /api/v1/business/density?lat=47.6062&lng=-122.3321&radius_miles=5&business_type=restaurant
```

### US Census Endpoints
```
GET /api/v1/census/demographics?state=53&county=
GET /api/v1/census/age-distribution?state=53&county=
GET /api/v1/census/gender?state=53&county=
GET /api/v1/census/employment?state=53&county=
GET /api/v1/census/housing?state=53&county=
```

### SerpAPI Endpoints
```
GET /api/v1/serpapi/search?query=coffee+shops&location=Seattle,WA
```

### Heatmap Endpoints
```
GET /api/v1/heatmap/buttons
GET /api/v1/heatmap/business_competition?lat=47.6062&lng=-122.3321&radius_km=5&business_type=restaurant
GET /api/v1/heatmap/demographic_density?lat=47.6062&lng=-122.3321&radius_km=5&business_type=restaurant
GET /api/v1/heatmap/foot_traffic?lat=47.6062&lng=-122.3321&radius_km=5&business_type=restaurant
GET /api/v1/heatmap/market_opportunity?lat=47.6062&lng=-122.3321&radius_km=5&business_type=restaurant
GET /api/v1/heatmap/income_wealth?lat=47.6062&lng=-122.3321&radius_km=5&business_type=restaurant
GET /api/v1/heatmap/review_power?lat=47.6062&lng=-122.3321&radius_km=5&business_type=restaurant
GET /api/v1/metrics/postal?bbox=-122.5,47.5,-122.1,47.7&metric_type=opportunity
```

### Territory Analysis
```
GET /api/v1/territory/analyze?center_lat=47.6062&center_lng=-122.3321&radius_miles=10&business_type=restaurant
```

### System Status
```
GET /
GET /api/v1/status
```

---

## 🧪 Testing the System

### Quick Test (when servers are running)
```bash
# Test backend
curl http://localhost:8001/ | jq .

# Test status
curl "http://localhost:8001/api/v1/status" | jq .

# Test geocoding
curl "http://localhost:8001/api/v1/mapbox/geocode?location=Seattle,WA" | jq .

# Test census data
curl "http://localhost:8001/api/v1/census/demographics?state=53" | jq .

# Test heatmap buttons
curl "http://localhost:8001/api/v1/heatmap/buttons" | jq .
```

### Comprehensive Test
```bash
./test_system.sh
```

---

## 📊 Features

### Dashboard Components
1. **DashboardHeader** - Navigation and controls
2. **MapView** - Interactive Mapbox visualization
3. **CompetitorPanel** - Competitor analysis and insights
4. **DemandPanel** - Demand metrics and trends
5. **DemographicsPanel** - Population and demographic data
6. **OpportunityPanel** - Market opportunity scoring

### Heatmap Layers
1. **🏢 Business Competition** - Competitor density and saturation
2. **👥 Demographics** - Population and demographic density
3. **🚶 Foot Traffic** - Movement and activity patterns
4. **🎯 Market Opportunity** - High-opportunity zones
5. **💰 Income/Wealth** - Economic distribution
6. **⭐ Review Power** - Online reputation and influence

---

## 🗂️ Data Sources

### Real-Time Data
- Mapbox: Map tiles, geocoding, routing
- Google Places: 100M+ businesses worldwide
- US Census: 330M+ population records
- SerpAPI: Live search results

### Data Storage
- SQLite database for caching
- API request logging
- Response time tracking

---

## 📝 Logs and Debugging

### Log Files (when using START_SYSTEM.sh)
```bash
tail -f /tmp/delta_backend.log
tail -f /tmp/delta_frontend.log
```

### Backend Log (backend/backend.log)
```bash
tail -f backend/backend.log
```

### Check Processes
```bash
# Find running processes
lsof -i :8001  # Backend
lsof -i :5173  # Frontend

# Kill processes
kill $(lsof -t -i:8001)
kill $(lsof -t -i:5173)
```

---

## 🚨 Troubleshooting

### Backend Won't Start
1. Check Python dependencies:
```bash
cd backend
pip3 install -r requirements.txt
```

2. Check database path in `real_api_server.py` line 41:
```python
DB_PATH = "/Users/udishkolnik/Downloads/D.E.L.T.A/DB/real_data.db"
```

3. Check HEATMAP path (line 71):
```python
sys.path.append('/Users/udishkolnik/Downloads/D.E.L.T.A 2')
```

### Frontend Won't Start
1. Reinstall dependencies:
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
```

2. Check Node version:
```bash
node --version  # Should be v18+ or v20+
```

### API Errors
- Check API keys in `backend/real_api_server.py` lines 32-38
- Verify API key quotas haven't been exceeded
- Check network connectivity

---

## 📦 Dependencies

### Backend (`backend/requirements.txt`)
- fastapi==0.104.1
- uvicorn==0.24.0
- httpx==0.25.2
- pydantic==2.5.0
- python-multipart==0.0.6

### Frontend (`frontend/package.json`)
- react: ^19.1.1
- @mui/material: ^7.3.4
- @reduxjs/toolkit: ^2.9.0
- mapbox-gl: ^3.15.0
- typescript: ~5.9.3
- vite (rolldown-vite): 7.1.14

---

## 🎯 Use Cases

1. **Site Selection** - Find optimal locations for new business
2. **Competitor Analysis** - Understand market saturation
3. **Demographic Research** - Identify target customer areas
4. **Market Opportunity** - Discover underserved areas
5. **Territory Planning** - Define sales/service territories
6. **Business Intelligence** - Data-driven decisions

---

## 📄 Additional Documentation

- `CAPABILITIES_SUMMARY.md` - System capabilities overview
- `COMPLETE_API_LIST.md` - Full API endpoint list
- `DATA_CAPABILITIES.md` - Data analysis features
- `DATA_SOURCES_MAP.md` - Data source details
- `MARKETING_CAPABILITIES.md` - Marketing features
- `REAL_DATA_COMPLETE.md` - Real data integration status
- `MOTOR_BOAT_SYSTEM_READY.md` - Motor boat analysis ready

---

## 🔐 Security Note

**⚠️ IMPORTANT**: API keys are currently hardcoded in the source. For production:
1. Move keys to environment variables
2. Use `.env` file (add to `.gitignore`)
3. Implement key rotation
4. Set up proper authentication
5. Add rate limiting

---

## 📞 Support

For issues or questions:
1. Check logs in `/tmp/` directory
2. Review `backend/backend.log`
3. Test individual endpoints using curl
4. Verify API keys are valid

---

**Last Updated**: October 10, 2025
**Version**: 2.0.0
**Status**: ✅ REAL DATA ONLY - No Mock, No Demo, No Hardcoded Data

