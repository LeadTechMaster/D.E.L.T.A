#!/bin/bash

echo "🚀 Starting D.E.L.T.A 2 System..."
echo ""

# Start Backend
echo "📡 Starting Backend API Server (Port 8001)..."
cd /Users/udishkolnik/Downloads/D.E.L.T.A\ 2/backend
python3 real_api_server.py > /tmp/delta_backend.log 2>&1 &
BACKEND_PID=$!
echo "   Backend PID: $BACKEND_PID"
echo "   Logs: /tmp/delta_backend.log"

# Wait for backend to start
echo "   Waiting for backend to initialize..."
sleep 5

# Test backend
if curl -s http://localhost:8001/ > /dev/null 2>&1; then
    echo "   ✅ Backend is running!"
else
    echo "   ⚠️  Backend may still be starting..."
fi

# Start Frontend
echo ""
echo "🎨 Starting Frontend Dev Server (Port 5173)..."
cd /Users/udishkolnik/Downloads/D.E.L.T.A\ 2/frontend
npm run dev > /tmp/delta_frontend.log 2>&1 &
FRONTEND_PID=$!
echo "   Frontend PID: $FRONTEND_PID"
echo "   Logs: /tmp/delta_frontend.log"

# Wait for frontend to start
echo "   Waiting for frontend to initialize..."
sleep 5

# Test frontend
if curl -s http://localhost:5173/ > /dev/null 2>&1; then
    echo "   ✅ Frontend is running!"
else
    echo "   ⚠️  Frontend may still be starting..."
fi

echo ""
echo "====================================="
echo "✅ D.E.L.T.A 2 System Started!"
echo "====================================="
echo ""
echo "🌐 Access URLs:"
echo "   Frontend: http://localhost:5173"
echo "   Backend API: http://localhost:8001"
echo "   API Docs: http://localhost:8001/docs"
echo ""
echo "📊 Process IDs:"
echo "   Backend: $BACKEND_PID"
echo "   Frontend: $FRONTEND_PID"
echo ""
echo "📝 Logs:"
echo "   Backend: tail -f /tmp/delta_backend.log"
echo "   Frontend: tail -f /tmp/delta_frontend.log"
echo ""
echo "🛑 To stop:"
echo "   kill $BACKEND_PID $FRONTEND_PID"
echo ""
echo "Run ./test_system.sh to test all endpoints"
echo "====================================="

