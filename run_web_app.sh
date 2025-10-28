#!/bin/bash

# Kaizen Web Application Startup Script

echo "========================================="
echo "🌱 Kaizen - Adaptive Learning Platform"
echo "========================================="
echo ""

# Set Python path
export PYTHONPATH=/usr/local/lib/python3.12/site-packages:$PYTHONPATH

# Check if ML model exists
if [ ! -f "data/adaptive_model.pkl" ]; then
    echo "⚠️  ML model not found. Training model..."
    python3 ml_model.py
    echo ""
fi

# Start Flask app
echo "🚀 Starting web server..."
echo "Access the app at: http://localhost:5000"
echo ""
echo "Press Ctrl+C to stop"
echo ""

python3 app.py
