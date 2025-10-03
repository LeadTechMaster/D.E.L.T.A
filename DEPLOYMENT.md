# 🚀 D.E.L.T.A Deployment Guide for Render

## Overview
This guide will help you deploy the D.E.L.T.A Franchise Intelligence Platform to Render with three services:
1. **Backend API** (Python FastAPI)
2. **Database** (PostgreSQL)
3. **Frontend** (Static Site)

## Prerequisites
- GitHub repository: `https://github.com/SirShkolnik-WonderLand/D.E.L.T.A.git`
- API keys for external services (Mapbox, Google Places, SerpAPI, US Census)

## Deployment Steps

### Option 1: Blueprint Deployment (Recommended)

1. **Go to [render.com](https://render.com)**
2. **Connect your GitHub account**
3. **Import the `D.E.L.T.A` repository**
4. **Create a new Blueprint from `render.yaml`**
5. **Set your environment variables in the Blueprint**

This will automatically deploy:
- **Backend API Service** (`delta-backend-api`)
- **Frontend Service** (`delta-frontend`)

### Option 2: Manual Deployment

#### 1. Backend API Service

**Service Type:** Web Service
**Environment:** Python 3.11
**Plan:** Free

**Configuration:**
- **Name:** `delta-backend-api`
- **Region:** Choose closest to your users
- **Branch:** `main`
- **Root Directory:** `BOT`
- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `gunicorn app:app --bind 0.0.0.0:$PORT --workers 1 --timeout 120`

**Environment Variables:**
```
MAPBOX_ACCESS_TOKEN=your_mapbox_token
GOOGLE_PLACES_API_KEY=your_google_places_key
SERPAPI_API_KEY=your_serpapi_key
CENSUS_API_KEY=your_census_key
PYTHON_VERSION=3.11.0
```

#### 2. Database Service (Optional - Manual Creation)

**Service Type:** PostgreSQL
**Plan:** Free

**Note:** Create this manually in Render Dashboard if you need persistent storage:
1. Go to Render Dashboard
2. Click "New" → "PostgreSQL"
3. Name: `delta-database`
4. Plan: Free
5. Copy the connection string for environment variables

#### 3. Frontend Service

**Service Type:** Static Site
**Plan:** Free

**Configuration:**
- **Name:** `delta-frontend`
- **Build Command:** `echo "Frontend deployment"`
- **Publish Directory:** `frontend`

**Environment Variables:**
```
REACT_APP_API_URL=https://delta-backend-api.onrender.com
```

## API Keys Setup

You'll need to obtain API keys from these services:

1. **Mapbox** (Geocoding): https://www.mapbox.com/
2. **Google Places API** (Business data): https://console.cloud.google.com/
3. **SerpAPI** (Franchise search): https://serpapi.com/
4. **US Census API** (Demographics): https://api.census.gov/

## Deployment URLs

After deployment, your services will be available at:
- **Backend API:** `https://delta-backend-api.onrender.com`
- **Frontend:** `https://delta-frontend.onrender.com`
- **Database:** Internal connection string provided by Render

## Health Check

The backend API includes a health check endpoint:
- **URL:** `https://delta-backend-api.onrender.com/status`
- **Expected Response:** `{"status": "active", "bot_name": "FranchiseBot"}`

## Troubleshooting

### Common Issues:

1. **Build Failures:**
   - Check that all dependencies are in `requirements.txt`
   - Ensure Python version is compatible

2. **API Key Errors:**
   - Verify all environment variables are set correctly
   - Check that API keys are valid and have proper permissions

3. **Database Connection:**
   - Ensure database service is running
   - Check connection string format

4. **CORS Issues:**
   - Verify frontend URL is in allowed origins
   - Check CORS configuration in backend

## Monitoring

Render provides built-in monitoring for:
- Application logs
- Performance metrics
- Error tracking
- Uptime monitoring

## Scaling

For production use beyond the free tier:
- Upgrade to paid plans for better performance
- Add more workers for higher concurrency
- Use managed databases for better reliability

## Security Notes

- API keys are stored as environment variables (secure)
- Database credentials are auto-generated and secure
- CORS is configured for specific origins
- All sensitive files are in `.gitignore`
