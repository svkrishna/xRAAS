#!/bin/bash

# XReason Development Setup Script
echo "🚀 Setting up XReason development environment..."

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

# Activate virtual environment
echo "📦 Activating virtual environment..."
source .venv/bin/activate

# Install SDK in development mode
echo "🔧 Installing XReason SDK in development mode..."
cd sdk
pip install -e .
cd ..

# Install additional development dependencies
echo "📚 Installing development dependencies..."
pip install httpx pydantic

# Create examples directory if it doesn't exist
mkdir -p examples

echo "✅ Development setup complete!"
echo ""
echo "🎯 Next steps:"
echo "   1. Start the services: ./scripts/start-xreason.sh"
echo "   2. Run the demo: python examples/pilot_demo.py"
echo "   3. Access the API docs: http://localhost:8000/docs"
echo ""
echo "📖 Available demos:"
echo "   - examples/pilot_demo.py (Legal & Scientific pilots)"
echo ""
echo "🔧 Development tools:"
echo "   - SDK installed in development mode"
echo "   - Hot reloading available"
echo "   - Full type checking support"
