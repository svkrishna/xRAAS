#!/bin/bash

# AI Agent Demo Runner for XReason
# This script runs the advanced AI agent demo showcasing intelligent reasoning capabilities

set -e

echo "🤖 XReason Advanced AI Agent Demo"
echo "================================="

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
    exit 1
fi

# Activate virtual environment
echo "📦 Activating virtual environment..."
source .venv/bin/activate

# Check if httpx is installed
if ! python -c "import httpx" 2>/dev/null; then
    echo "📦 Installing httpx..."
    pip install httpx
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

# Check if agent endpoints are available
echo "🔍 Checking if AI agent endpoints are available..."
if ! curl -s http://localhost:8000/api/v1/agents/health > /dev/null; then
    echo "⚠️  AI agent endpoints not available. Please ensure the backend includes agent services."
    echo "   Check that the agent router is properly included in the main application."
    exit 1
else
    echo "✅ AI agent endpoints are available"
fi

# Run the AI agent demo
echo ""
echo "🎯 Running Advanced AI Agent Demo..."
echo "==================================="

# Run the demo
python examples/ai_agent_demo.py

echo ""
echo "🎉 AI Agent demo completed!"
echo ""
echo "📊 Check the generated results file for detailed analysis"
echo "🌐 View the web interface at: http://localhost:3000"
echo "📈 View metrics at: http://localhost:3002 (Grafana)"
echo "📚 API documentation at: http://localhost:8000/docs"
echo ""
echo "🤖 AI Agent Features Demonstrated:"
echo "   • Session Management"
echo "   • Reasoning Agent (Advanced Logic)"
echo "   • Knowledge Agent (Knowledge Integration)"
echo "   • Validation Agent (Fact Checking)"
echo "   • Memory Operations (Short/Long Term)"
echo "   • Learning Operations (Pattern Recognition)"
echo "   • Knowledge Integration (Fact Management)"
echo "   • System Status Monitoring"
echo ""
echo "To stop the backend:"
echo "   docker-compose down"
