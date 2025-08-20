#!/bin/bash

# Start XReason with Full Observability Stack
echo "🚀 Starting XReason with Full Observability Stack..."

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker first."
    exit 1
fi

# Create network if it doesn't exist
if ! docker network ls | grep -q "xreason-network"; then
    echo "🌐 Creating xreason-network..."
    docker network create xreason-network
fi

# Start all services including observability
echo "📊 Starting XReason with full observability stack..."
docker-compose up -d

# Wait for services to be ready
echo "⏳ Waiting for services to be ready..."
sleep 15

# Check service status
echo "🔍 Checking service status..."
docker-compose ps

echo ""
echo "✅ Observability Stack Started!"
echo ""
echo "📊 Access URLs:"
echo "   Backend API: http://localhost:8000"
echo "   Frontend:    http://localhost:3000"
echo "   API Docs:    http://localhost:8000/docs"
echo "   Prometheus:  http://localhost:9090"
echo "   Grafana:     http://localhost:3002 (admin/xreason123)"
echo "   Alertmanager: http://localhost:9093"
echo ""
echo "📋 Next steps:"
echo "   1. Open the frontend at http://localhost:3000"
echo "   2. Open Grafana at http://localhost:3002"
echo "   3. Login with admin/xreason123"
echo "   4. The XReason dashboard should be automatically loaded"
echo "   5. Configure alerts in Alertmanager if needed"
echo ""
echo "🛑 To stop: docker-compose down"
