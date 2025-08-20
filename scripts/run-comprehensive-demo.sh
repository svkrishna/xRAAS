#!/bin/bash

# Comprehensive XReason Pilot Demo Runner
# This script runs the comprehensive demo showcasing all domain pilots

set -e

echo "🚀 XReason Comprehensive Pilot Demo"
echo "=================================="

# Check if we're in the right directory
if [ ! -f "docker-compose.yml" ]; then
    echo "❌ Error: Please run this script from the project root directory"
    exit 1
fi

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "❌ Error: Virtual environment not found. Please run setup first:"
    echo "   python -m venv .venv"
    echo "   source .venv/bin/activate"
    echo "   pip install -r backend/requirements.txt"
    echo "   pip install -e ./sdk"
    exit 1
fi

# Activate virtual environment
echo "📦 Activating virtual environment..."
source .venv/bin/activate

# Check if SDK is installed
if ! python -c "import xreason_sdk" 2>/dev/null; then
    echo "📦 Installing XReason SDK..."
    pip install -e ./sdk
fi

# Check if backend is running
echo "🔍 Checking if XReason backend is running..."
if ! curl -s http://localhost:8000/health > /dev/null; then
    echo "⚠️  XReason backend is not running. Starting it now..."
    echo "   This may take a few minutes..."
    
    # Start the backend in the background
    docker-compose up -d backend
    
    # Wait for backend to be ready
    echo "⏳ Waiting for backend to be ready..."
    for i in {1..30}; do
        if curl -s http://localhost:8000/health > /dev/null; then
            echo "✅ Backend is ready!"
            break
        fi
        echo "   Waiting... ($i/30)"
        sleep 2
    done
    
    if ! curl -s http://localhost:8000/health > /dev/null; then
        echo "❌ Backend failed to start. Please check the logs:"
        echo "   docker-compose logs backend"
        exit 1
    fi
else
    echo "✅ Backend is already running"
fi

# Run the comprehensive demo
echo ""
echo "🎯 Running Comprehensive Pilot Demo..."
echo "====================================="

# Run the demo
python examples/comprehensive_pilot_demo.py

echo ""
echo "🎉 Comprehensive demo completed!"
echo ""
echo "📊 Check the generated results file for detailed analysis"
echo "🌐 View the web interface at: http://localhost:3000"
echo "📈 View metrics at: http://localhost:3002 (Grafana)"
echo ""
echo "To stop the backend:"
echo "   docker-compose down"
