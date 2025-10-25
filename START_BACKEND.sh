#!/bin/bash

echo "🚀 Starting D.E.L.T.A 2 Backend Server..."
echo ""

# Check if port 8001 is already in use
if lsof -Pi :8001 -sTCP:LISTEN -t >/dev/null ; then
    echo "⚠️  Port 8001 is already in use. Stopping existing process..."
    kill $(lsof -t -i:8001) 2>/dev/null || true
    sleep 2
fi

# Change to backend directory
cd /Users/udishkolnik/Downloads/D.E.L.T.A\ 2/backend

echo "📡 Starting backend server on port 8001..."
echo "   Logs will be shown below:"
echo "   Press Ctrl+C to stop"
echo ""

# Start the server with visible output
python3 real_api_server.py
