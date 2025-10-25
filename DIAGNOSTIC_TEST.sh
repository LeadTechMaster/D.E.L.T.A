#!/bin/bash

echo "🔍 D.E.L.T.A 2 SYSTEM DIAGNOSTIC TEST"
echo "====================================="
echo ""

# Test 1: Check Python
echo "1. Testing Python..."
if python3 --version > /dev/null 2>&1; then
    echo "   ✅ Python3 is installed: $(python3 --version)"
else
    echo "   ❌ Python3 not found"
    exit 1
fi

# Test 2: Check if ports are free
echo ""
echo "2. Checking ports..."
if lsof -i :8001 > /dev/null 2>&1; then
    echo "   ⚠️  Port 8001 is in use"
    echo "   Killing existing processes..."
    lsof -ti:8001 | xargs kill -9 2>/dev/null || true
    sleep 2
else
    echo "   ✅ Port 8001 is free"
fi

if lsof -i :5173 > /dev/null 2>&1; then
    echo "   ⚠️  Port 5173 is in use"
else
    echo "   ✅ Port 5173 is free"
fi

# Test 3: Check backend files
echo ""
echo "3. Checking backend files..."
cd "/Users/udishkolnik/Downloads/D.E.L.T.A 2/backend"

if [ -f "test_server.py" ]; then
    echo "   ✅ test_server.py exists"
else
    echo "   ❌ test_server.py not found"
fi

if [ -f "working_server.py" ]; then
    echo "   ✅ working_server.py exists"
else
    echo "   ❌ working_server.py not found"
fi

# Test 4: Start backend server
echo ""
echo "4. Starting backend server..."
python3 test_server.py &
BACKEND_PID=$!
echo "   Backend PID: $BACKEND_PID"
sleep 5

# Test 5: Test backend endpoints
echo ""
echo "5. Testing backend endpoints..."

# Test root endpoint
echo "   Testing root endpoint..."
if curl -s http://localhost:8001/ > /dev/null; then
    echo "   ✅ Root endpoint working"
    curl -s http://localhost:8001/ | head -1
else
    echo "   ❌ Root endpoint failed"
fi

# Test status endpoint
echo "   Testing status endpoint..."
if curl -s http://localhost:8001/api/v1/status > /dev/null; then
    echo "   ✅ Status endpoint working"
else
    echo "   ❌ Status endpoint failed"
fi

# Test census endpoint
echo "   Testing census endpoint..."
if curl -s http://localhost:8001/api/v1/census/demographics > /dev/null; then
    echo "   ✅ Census endpoint working"
else
    echo "   ❌ Census endpoint failed"
fi

# Test 6: Check frontend
echo ""
echo "6. Checking frontend..."
cd "/Users/udishkolnik/Downloads/D.E.L.T.A 2/frontend"

if [ -f "package.json" ]; then
    echo "   ✅ package.json exists"
else
    echo "   ❌ package.json not found"
fi

if [ -d "node_modules" ]; then
    echo "   ✅ node_modules exists"
else
    echo "   ❌ node_modules not found - run 'npm install'"
fi

# Test 7: Start frontend
echo ""
echo "7. Starting frontend..."
npm run dev &
FRONTEND_PID=$!
echo "   Frontend PID: $FRONTEND_PID"
sleep 8

# Test 8: Test frontend
echo ""
echo "8. Testing frontend..."
if curl -s http://localhost:5173/ > /dev/null; then
    echo "   ✅ Frontend is responding"
else
    echo "   ❌ Frontend not responding"
fi

# Summary
echo ""
echo "====================================="
echo "🎯 DIAGNOSTIC SUMMARY"
echo "====================================="
echo ""
echo "Backend PID: $BACKEND_PID"
echo "Frontend PID: $FRONTEND_PID"
echo ""
echo "🌐 Access URLs:"
echo "   Frontend: http://localhost:5173"
echo "   Backend: http://localhost:8001"
echo ""
echo "🛑 To stop servers:"
echo "   kill $BACKEND_PID $FRONTEND_PID"
echo ""
echo "📊 Test endpoints:"
echo "   curl http://localhost:8001/"
echo "   curl http://localhost:8001/api/v1/status"
echo "   curl http://localhost:8001/api/v1/census/demographics"
echo ""
echo "====================================="
