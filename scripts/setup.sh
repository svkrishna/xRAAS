#!/bin/bash

# XReason Setup Script
# This script sets up the development environment for XReason

set -e

echo "🚀 Setting up XReason development environment..."

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

# Create .env file if it doesn't exist
if [ ! -f backend/.env ]; then
    echo "📝 Creating backend/.env file..."
    cp backend/env.example backend/.env
    echo "⚠️  Please edit backend/.env and add your OpenAI API key"
fi

# Create frontend .env file if it doesn't exist
if [ ! -f frontend/.env ]; then
    echo "📝 Creating frontend/.env file..."
    cat > frontend/.env << EOF
REACT_APP_API_URL=http://localhost:8000
EOF
fi

# Build and start services
echo "🔨 Building Docker images..."
docker-compose build

echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit backend/.env and add your OpenAI API key"
echo "2. Run: docker-compose up -d"
echo "3. Access the application at:"
echo "   - Frontend: http://localhost:3000"
echo "   - Backend API: http://localhost:8000"
echo "   - API Docs: http://localhost:8000/docs"
echo ""
echo "For development with hot reloading:"
echo "   docker-compose --profile dev up -d"
echo "   Frontend dev: http://localhost:3001"
