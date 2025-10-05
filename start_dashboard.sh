#!/bin/bash

# D.E.L.T.A Business Intelligence Dashboard Startup Script
echo "🚀 Starting D.E.L.T.A Business Intelligence Dashboard..."

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js 18+ first."
    exit 1
fi

# Check if npm is installed
if ! command -v npm &> /dev/null; then
    echo "❌ npm is not installed. Please install npm first."
    exit 1
fi

# Navigate to project directory
cd /Users/udishkolnik/3/D.E.L.T.A

echo "📦 Installing dependencies..."
npm install

echo "🔧 Building project..."
npm run build

echo "🌐 Starting development server..."
echo "📍 Dashboard will be available at: http://localhost:3000"
echo "🔗 Make sure your backend services are running:"
echo "   - API Server: http://localhost:8001"
echo "   - Bot Server: http://localhost:8002"
echo ""

# Start the development server
npm run dev
