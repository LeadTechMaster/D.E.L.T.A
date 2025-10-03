#!/bin/bash

# D.E.L.T.A Production Startup Script for Render

echo "🚀 Starting D.E.L.T.A Franchise Intelligence Bot (Production Mode)"

# Set Python path
export PYTHONPATH="${PYTHONPATH}:$(pwd)"

# Check if required environment variables are set
required_vars=("MAPBOX_ACCESS_TOKEN" "GOOGLE_PLACES_API_KEY" "SERPAPI_API_KEY")
missing_vars=()

for var in "${required_vars[@]}"; do
    if [ -z "${!var}" ]; then
        missing_vars+=("$var")
    fi
done

if [ ${#missing_vars[@]} -ne 0 ]; then
    echo "⚠️  Warning: Missing environment variables: ${missing_vars[*]}"
    echo "   The application will start but API functionality may be limited."
fi

# Start the application with Gunicorn
echo "🔧 Starting Gunicorn server..."
exec gunicorn app:app \
    --bind 0.0.0.0:$PORT \
    --workers 1 \
    --worker-class uvicorn.workers.UvicornWorker \
    --timeout 120 \
    --keep-alive 2 \
    --max-requests 1000 \
    --max-requests-jitter 100 \
    --log-level info \
    --access-logfile - \
    --error-logfile -
