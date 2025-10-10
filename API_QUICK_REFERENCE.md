# 🚀 D.E.L.T.A 2 - API Quick Reference

## 📍 **ZIP Code APIs (Primary)**

### **Demographics**
```bash
curl "http://localhost:8001/api/v1/zipcode/demographics?zipcode=98101"
```

### **Age Distribution**
```bash
curl "http://localhost:8001/api/v1/zipcode/age-distribution?zipcode=98101"
```

### **Coordinates**
```bash
curl "http://localhost:8001/api/v1/zipcode/coordinates?zipcode=98101"
```

### **Businesses**
```bash
curl "http://localhost:8001/api/v1/zipcode/businesses?zipcode=98101&query=motor+boat&radius=50000"
```

### **Isochrone**
```bash
curl "http://localhost:8001/api/v1/zipcode/isochrone?zipcode=98101&minutes=10&mode=driving"
```

---

## 🏛️ **Census APIs**

### **State Demographics**
```bash
curl "http://localhost:8001/api/v1/census/demographics?state=53"
```

### **State Age Distribution**
```bash
curl "http://localhost:8001/api/v1/census/age-distribution?state=53"
```

### **State Gender**
```bash
curl "http://localhost:8001/api/v1/census/gender?state=53"
```

---

## 🗺️ **Mapbox APIs**

### **Isochrone**
```bash
curl "http://localhost:8001/api/v1/mapbox/isochrone?coordinates=-122.336407,47.6084921&minutes=10&mode=driving"
```

### **Directions**
```bash
curl "http://localhost:8001/api/v1/mapbox/directions?origin=Seattle,WA&destination=Bellevue,WA&mode=driving"
```

### **Reverse Geocoding**
```bash
curl "http://localhost:8001/api/v1/mapbox/reverse-geocode?coordinates=-122.336407,47.6084921"
```

---

## 🔍 **Search APIs**

### **SerpAPI Search**
```bash
curl "http://localhost:8001/api/v1/serpapi/search?query=motor+boat&location=Seattle,WA"
```

### **Google Places**
```bash
curl "http://localhost:8001/api/v1/google-places/search?query=motor+boat&location=47.6062,-122.3321&radius=50000"
```

---

## 📊 **Sample ZIP Codes for Testing**

| ZIP Code | Location | Population | Income | Notes |
|----------|----------|------------|---------|-------|
| 98101 | Downtown Seattle | 14,528 | $96,893 | Retirement area (94.3% 65+) |
| 98112 | Capitol Hill | 24,412 | $133,267 | Higher income area |
| 98103 | Fremont | ~35,000 | ~$85,000 | Residential area |
| 98104 | Pioneer Square | ~8,000 | ~$75,000 | Historic district |

---

## 🎯 **Response Format**

All APIs return consistent format:
```json
{
  "status": "success|error",
  "data": {...},
  "error": "Error message if applicable",
  "timestamp": "2025-10-10T20:54:22.925Z"
}
```

---

## ⚡ **Quick Test Commands**

### **Test All ZIP Code APIs**
```bash
# Demographics
curl -s "http://localhost:8001/api/v1/zipcode/demographics?zipcode=98101" | jq '.data.total_population'

# Age Distribution  
curl -s "http://localhost:8001/api/v1/zipcode/age-distribution?zipcode=98101" | jq '.data.age_groups'

# Coordinates
curl -s "http://localhost:8001/api/v1/zipcode/coordinates?zipcode=98101" | jq '.data.center'

# Businesses
curl -s "http://localhost:8001/api/v1/zipcode/businesses?zipcode=98101" | jq '.data.total_results'

# Isochrone
curl -s "http://localhost:8001/api/v1/zipcode/isochrone?zipcode=98101" | jq '.data.travel_time_minutes'
```

### **Compare ZIP Codes**
```bash
# Compare two ZIP codes
echo "ZIP 98101:" && curl -s "http://localhost:8001/api/v1/zipcode/demographics?zipcode=98101" | jq '.data | {population: .total_population, income: .median_household_income}'
echo "ZIP 98112:" && curl -s "http://localhost:8001/api/v1/zipcode/demographics?zipcode=98112" | jq '.data | {population: .total_population, income: .median_household_income}'
```

---

## 🚨 **Error Testing**

### **Invalid ZIP Code**
```bash
curl "http://localhost:8001/api/v1/zipcode/demographics?zipcode=99999"
# Returns: {"status":"error","error":"ZIP code demographics API request failed..."}
```

### **Missing Parameters**
```bash
curl "http://localhost:8001/api/v1/zipcode/demographics"
# Returns: Defaults to ZIP 98101
```

---

## 🌐 **System Status**

- **Backend**: http://localhost:8001/ ✅ Running
- **Frontend**: http://localhost:5174/ ✅ Running
- **Real Data Only**: ✅ Enforced
- **No Mock Data**: ✅ Confirmed
- **ZIP Code Precision**: ✅ Implemented

---

## 🎮 **User Journey Testing**

1. **Open**: http://localhost:5174/
2. **Type**: "98101" in search bar
3. **See**: ZIP Info Panel with real demographics
4. **Adjust**: Distance tool (cycling, 5km)
5. **Watch**: Isochrone polygon appears
6. **Change**: Heat maps to business density
7. **Switch**: Try "98112" for comparison

**🎯 All with REAL API data - no mock responses!**
