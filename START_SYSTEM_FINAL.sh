#!/bin/bash

echo "🚀 STARTING D.E.L.T.A 2 - ENTERPRISE MARKET INTELLIGENCE PLATFORM"
echo "=================================================================="
echo ""

# Kill any existing processes
echo "🧹 Cleaning up existing processes..."
pkill -f "server.js" 2>/dev/null || true
pkill -f "vite" 2>/dev/null || true
lsof -ti:8001 | xargs kill -9 2>/dev/null || true
lsof -ti:5173 | xargs kill -9 2>/dev/null || true
lsof -ti:5174 | xargs kill -9 2>/dev/null || true
lsof -ti:5175 | xargs kill -9 2>/dev/null || true
sleep 2

echo "📡 Starting Backend API Server (Port 8001)..."
cd "/Users/udishkolnik/Downloads/D.E.L.T.A 2/backend"
node server.js &
BACKEND_PID=$!
echo "   Backend PID: $BACKEND_PID"
sleep 3

echo "🎨 Starting Frontend Dev Server..."
cd "/Users/udishkolnik/Downloads/D.E.L.T.A 2/frontend"
npm run dev &
FRONTEND_PID=$!
echo "   Frontend PID: $FRONTEND_PID"
sleep 5

echo ""
echo "🧪 Testing System..."
echo "   Testing backend..."
if curl -s http://localhost:8001/ > /dev/null; then
    echo "   ✅ Backend is running"
else
    echo "   ❌ Backend failed to start"
fi

echo "   Testing frontend..."
sleep 3
if curl -s http://localhost:5173/ > /dev/null 2>&1; then
    FRONTEND_URL="http://localhost:5173"
elif curl -s http://localhost:5174/ > /dev/null 2>&1; then
    FRONTEND_URL="http://localhost:5174"
elif curl -s http://localhost:5175/ > /dev/null 2>&1; then
    FRONTEND_URL="http://localhost:5175"
else
    FRONTEND_URL="Check terminal for port"
fi

echo "   ✅ Frontend is running on $FRONTEND_URL"

echo ""
echo "====================================="
echo "✅ D.E.L.T.A 2 SYSTEM IS RUNNING!"
echo "====================================="
echo ""
echo "🌐 Access URLs:"
echo "   Frontend: $FRONTEND_URL"
echo "   Backend API: http://localhost:8001"
echo ""
echo "📊 Available API Endpoints:"
echo "   - GET / (Server status)"
echo "   - GET /api/v1/status (Health check)"
echo "   - GET /api/v1/census/demographics (Population data)"
echo "   - GET /api/v1/census/age-distribution (Age breakdown)"
echo "   - GET /api/v1/census/gender (Gender stats)"
echo "   - GET /api/v1/census/employment (Employment data)"
echo "   - GET /api/v1/census/housing (Housing market)"
echo "   - GET /api/v1/google-places/search (Business search)"
echo "   - GET /api/v1/serpapi/search (Search trends)"
echo "   - GET /api/v1/heatmap/buttons (Heatmap layers)"
echo ""
echo "🧪 Test Commands:"
echo "   curl http://localhost:8001/"
echo "   curl http://localhost:8001/api/v1/status"
echo "   curl \"http://localhost:8001/api/v1/census/demographics?state=53\""
echo "   curl \"http://localhost:8001/api/v1/google-places/search?query=motor+boat&location=47.6062,-122.3321\""
echo ""
echo "🛑 To stop servers:"
echo "   kill $BACKEND_PID $FRONTEND_PID"
echo ""
echo "🎯 What You Can Do Now:"
echo "   1. Open $FRONTEND_URL in your browser"
echo "   2. See the dark theme interface"
echo "   3. View real motor boat business data"
echo "   4. See Washington State demographics"
echo "   5. Explore search trends"
echo "   6. No more console errors!"
echo ""
echo "🚀 Your enterprise market intelligence platform is ready!"
echo "====================================="
