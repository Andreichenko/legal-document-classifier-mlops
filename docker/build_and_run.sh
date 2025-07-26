#!/bin/bash

# Build and run script for Legal Document Classifier API

set -e

echo "🐳 Building Legal Document Classifier Docker image..."

# Build the Docker image
docker build -f docker/Dockerfile -t legal-classifier:latest .

echo "✅ Docker image built successfully!"

echo "🚀 Starting the API container..."

# Run the container
docker run -d \
  --name legal-classifier-api \
  -p 8000:8000 \
  --health-cmd="curl -f http://localhost:8000/health || exit 1" \
  --health-interval=30s \
  --health-timeout=10s \
  --health-retries=3 \
  legal-classifier:latest

echo "✅ Container started successfully!"
echo "📊 API is running at: http://localhost:8000"
echo "📚 Documentation: http://localhost:8000/docs"
echo "🏥 Health check: http://localhost:8000/health"

# Wait a moment for the container to start
sleep 5

# Test the API
echo "🧪 Testing the API..."
curl -s http://localhost:8000/health | jq . || echo "Health check failed, but container is running"

echo ""
echo "🎉 Legal Document Classifier API is ready!"
echo ""
echo "Commands:"
echo "  Stop container: docker stop legal-classifier-api"
echo "  View logs: docker logs legal-classifier-api"
echo "  Remove container: docker rm legal-classifier-api" 