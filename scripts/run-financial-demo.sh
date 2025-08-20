#!/bin/bash

# Financial Analysis Demo Runner for XReason
# This script runs the specialized financial analysis demo showcasing compliance and risk analysis

set -e

echo "🏦 XReason Financial Analysis Demo"
echo "=================================="

# Check if we're in the right directory
if [ ! -f "docker-compose.yml" ]; then
    echo "❌ Error: Please run this script from the xreason project root directory"
    exit 1
fi

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "❌ Error: Virtual environment not found. Please run setup-dev.sh first"
    exit 1
fi

# Check if httpx is installed
if ! .venv/bin/python -c "import httpx" 2>/dev/null; then
    echo "📦 Installing httpx..."
    .venv/bin/pip install httpx
fi

# Check if backend is running
echo "🔍 Checking if XReason backend is running..."
if ! curl -s http://localhost:8000/health > /dev/null; then
    echo "🚀 Starting XReason backend..."
    docker-compose up -d backend
    
    echo "⏳ Waiting for backend to be ready..."
    for i in {1..30}; do
        if curl -s http://localhost:8000/health > /dev/null; then
            break
        fi
        sleep 2
    done
fi

# Check if financial analysis endpoint is available
echo "🔍 Checking financial analysis endpoint..."
if ! curl -s http://localhost:8000/api/v1/financial/health > /dev/null; then
    echo "❌ Error: Financial analysis endpoint not available"
    echo "   Please ensure the backend is running and the financial analysis service is loaded"
    exit 1
fi

# Run the financial analysis demo
echo ""
echo "🎯 Running Financial Analysis Demo..."
echo "==================================="

.venv/bin/python examples/financial_analysis_demo.py

echo ""
echo "🎉 Financial analysis demo completed!"
echo ""
echo "📊 What was demonstrated:"
echo "   • Individual company financial analysis"
echo "   • Batch analysis for multiple companies"
echo "   • Risk assessment and scoring"
echo "   • Regulatory compliance analysis"
echo "   • Financial health evaluation"
echo "   • AI-powered recommendations"
echo ""
echo "🔗 Access the services:"
echo "   • API Documentation: http://localhost:8000/docs"
echo "   • Financial Analysis: http://localhost:8000/api/v1/financial/*"
echo "   • Health Check: http://localhost:8000/api/v1/financial/health"
echo ""
echo "📚 Next steps:"
echo "   • Review the API documentation"
echo "   • Try different financial scenarios"
echo "   • Integrate with your financial data"
echo "   • Customize regulatory frameworks"
echo ""
echo "To stop the backend:"
echo "   docker-compose down"
