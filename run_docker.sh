#!/bin/bash

echo "� Starting Graph-RAG with API-based LLM using Docker..."
echo ""
echo "This will:"
echo "1. 🗄️  Start Neo4j database"
echo "2. 🤖 Build the lightweight app with API LLM support"
echo "3. 🚀 Launch the Streamlit interface"
echo ""

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker first."
    exit 1
fi

# Check for .env file
if [ -f .env ]; then
    echo "📝 Found .env file - loading API keys..."
    export $(grep -v '^#' .env | xargs)
else
    echo "ℹ️  No .env file found - using mock responses (perfect for testing!)"
    echo "   To use real APIs, copy .env.example to .env and add your API keys"
fi

# Build and start services
echo "🔄 Building and starting services..."

# Use docker compose
if docker compose version &> /dev/null 2>&1; then
    docker compose up --build
elif command -v docker-compose &> /dev/null; then
    docker-compose up --build
else
    echo "❌ Docker Compose not found. Please install Docker Compose"
    exit 1
fi

echo ""
echo "🎉 Once started, access the app at:"
echo "📱 Streamlit App: http://localhost:8501"
echo "🗄️  Neo4j Browser: http://localhost:7474"
echo ""
echo "Default Neo4j credentials:"
echo "Username: neo4j"
echo "Password: password"
echo ""
echo "💡 The app uses mock responses by default (instant!)"
echo "   Add API keys to .env file for real LLM responses"
echo ""
echo "Press Ctrl+C to stop all services"
