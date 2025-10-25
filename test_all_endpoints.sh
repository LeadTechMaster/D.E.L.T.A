#!/bin/bash

echo "🧪 Testing All D.E.L.T.A API Endpoints"
echo "======================================"
echo ""

BASE_URL="http://localhost:8001"

# Function to test endpoint
test_endpoint() {
    local name=$1
    local url=$2
    echo "Testing: $name"
    curl -s "$url" | python3 -m json.tool | head -30
    echo ""
    echo "---"
    echo ""
}

echo "Waiting for server to start..."
sleep 3

echo "✅ ORIGINAL ENDPOINTS"
echo "===================="

test_endpoint "1. System Status" "$BASE_URL/"

test_endpoint "2. Mapbox Geocode" "$BASE_URL/api/v1/mapbox/geocode?location=Seattle,WA"

test_endpoint "3. Google Places Search" "$BASE_URL/api/v1/google-places/search?query=coffee&location=Seattle,WA&radius=5000"

test_endpoint "4. Territory Analysis" "$BASE_URL/api/v1/territory/analyze?center_lat=47.6062&center_lng=-122.3321&radius_miles=5&business_type=restaurant"

test_endpoint "5. Census Demographics (Basic)" "$BASE_URL/api/v1/census/demographics?state=53"

echo ""
echo "🆕 NEW CENSUS ENDPOINTS"
echo "======================="

test_endpoint "6. Age Distribution" "$BASE_URL/api/v1/census/age-distribution?state=53"

test_endpoint "7. Gender Breakdown" "$BASE_URL/api/v1/census/gender?state=53"

test_endpoint "8. Employment Statistics" "$BASE_URL/api/v1/census/employment?state=53"

test_endpoint "9. Housing Data" "$BASE_URL/api/v1/census/housing?state=53"

echo ""
echo "🆕 NEW MAPBOX ENDPOINTS"
echo "======================"

test_endpoint "10. Isochrone (Travel Time Area)" "$BASE_URL/api/v1/mapbox/isochrone?lat=47.6062&lng=-122.3321&minutes=10&mode=driving"

test_endpoint "11. Directions (Route)" "$BASE_URL/api/v1/mapbox/directions?start_lat=47.6062&start_lng=-122.3321&end_lat=47.6205&end_lng=-122.3493&mode=driving"

test_endpoint "12. Reverse Geocode" "$BASE_URL/api/v1/mapbox/reverse-geocode?lat=47.6062&lng=-122.3321"

echo ""
echo "🆕 NEW BUSINESS ENDPOINT"
echo "======================="

test_endpoint "13. Business Density Analysis" "$BASE_URL/api/v1/business/density?lat=47.6062&lng=-122.3321&radius_miles=3&business_type=restaurant"

echo ""
echo "🎯 HEATMAP ENDPOINTS"
echo "==================="

test_endpoint "14. Competition Heatmap" "$BASE_URL/api/v1/heatmap/business_competition?lat=47.6062&lng=-122.3321&radius_km=5&business_type=restaurant"

echo ""
echo "✅ Testing Complete!"
echo ""
echo "📊 SUMMARY:"
echo "- Original Endpoints: 5"
echo "- New Census Endpoints: 4"  
echo "- New Mapbox Endpoints: 3"
echo "- New Business Endpoints: 1"
echo "- Heatmap Endpoints: 6"
echo "============================"
echo "TOTAL ENDPOINTS: 19+"

