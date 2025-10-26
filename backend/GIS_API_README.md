# D.E.L.T.A GIS API - Setup & Start Script

## Prerequisites
- Python 3.9+
- pip

## Installation

### 1. Create Virtual Environment (Recommended)
```powershell
cd D.E.L.T.A/backend
python -m venv venv_gis
.\venv_gis\Scripts\Activate.ps1
```

### 2. Install Dependencies
```powershell
pip install -r requirements_gis.txt
```

## Starting the GIS API

### PowerShell:
```powershell
cd D.E.L.T.A/backend
python gis_api.py
```

The GIS API will start on **http://localhost:5001**

## Testing

### Health Check:
```powershell
curl http://localhost:5001/health
```

### Test Tract Calculation:
```powershell
curl -X POST http://localhost:5001/api/v1/gis/calculate-tracts -H "Content-Type: application/json" -d '{\"polygon\": [[37.7749, -122.4194], [37.7849, -122.4094], [37.7849, -122.4294], [37.7749, -122.4294]]}'
```

## Architecture

The GIS API works in tandem with the Node.js API:

1. **Frontend** draws polygon → Sends coordinates to **GIS API (Python/Flask)**
2. **GIS API** calculates tract overlaps using GeoPandas
3. **GIS API** calls **Node.js API** to fetch demographics for each tract
4. **GIS API** returns weighted demographics to **Frontend**

```
Frontend (React/Mapbox)
    ↓ POST polygon coords
GIS API (Python/Flask:5001)
    ↓ Calculate tract overlaps
    ↓ Fetch tract demographics
Node.js API (:8001)
    ↓ Census Bureau API
Real Data
```

## Ports
- Node.js API: **8001**
- GIS API: **5001**
- Frontend: **5173**

## Cache
Census tract shapefiles are cached in:
- Windows: `%TEMP%\delta_gis_cache\`
- Linux/Mac: `/tmp/delta_gis_cache/`

First run will download ~5-10MB of data. Subsequent runs use the cache.

