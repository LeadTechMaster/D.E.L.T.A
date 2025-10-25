#!/bin/bash

echo "🚀 STARTING D.E.L.T.A 2 - ENTERPRISE MARKET INTELLIGENCE PLATFORM"
echo "=================================================================="
echo ""

# Kill any existing processes
echo "🧹 Cleaning up existing processes..."
pkill -f "real_api_server.py" 2>/dev/null || true
pkill -f "working_server.py" 2>/dev/null || true
lsof -ti:8001 | xargs kill -9 2>/dev/null || true
sleep 2

# Change to backend directory
cd "/Users/udishkolnik/Downloads/D.E.L.T.A 2/backend"

echo "📡 Starting Backend API Server..."
echo "   Port: 8001"
echo "   Data Policy: 100% REAL DATA ONLY"
echo ""

# Start backend with visible output
python3 working_server.py
