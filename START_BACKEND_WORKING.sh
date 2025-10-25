#!/bin/bash

echo "🚀 Starting D.E.L.T.A 2 Backend Server (Working Version)"
echo ""

# Kill any existing processes on port 8001
echo "🧹 Cleaning up existing processes..."
lsof -ti:8001 | xargs kill -9 2>/dev/null || true
sleep 2

# Change to backend directory
cd "/Users/udishkolnik/Downloads/D.E.L.T.A 2/backend"

echo "📡 Starting backend server on port 8001..."
echo "   This will show real-time logs"
echo "   Press Ctrl+C to stop"
echo ""

# Start the working server
python3 working_server.py
