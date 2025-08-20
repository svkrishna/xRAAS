#!/bin/bash

# XReason Demo Runner Script
echo "🎮 Running XReason Pilot Demo..."

# Check if we're in the right directory
if [ ! -f "docker-compose.yml" ]; then
    echo "❌ Error: Please run this script from the xreason project root"
    exit 1
fi

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "❌ Error: Virtual environment not found. Please run setup first."
    exit 1
fi

# Check if demo file exists
if [ ! -f "examples/pilot_demo.py" ]; then
    echo "❌ Error: Demo file not found. Please check the examples directory."
    exit 1
fi

# Activate virtual environment and run demo
echo "🚀 Starting demo with virtual environment..."
source .venv/bin/activate

# Check if services are running
echo "🔍 Checking if XReason services are running..."
if curl -s http://localhost:8000/health/ > /dev/null 2>&1; then
    echo "✅ Services are running!"
    python examples/pilot_demo.py
else
    echo "⚠️ Services are not running."
    echo ""
    echo "To start the services, run:"
    echo "  ./scripts/start-xreason.sh"
    echo ""
    echo "Or to run the demo anyway (it will show connection errors):"
    echo "  python examples/pilot_demo.py"
    echo ""
    read -p "Do you want to run the demo anyway? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        python examples/pilot_demo.py
    else
        echo "Demo cancelled. Start the services first to see the full demo."
    fi
fi
