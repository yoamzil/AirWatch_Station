#!/bin/bash

echo "🛑 Stopping AirWatch Station..."

# Stop backend
echo "📦 Stopping ThingsBoard..."
cd thingsboard_docker
docker-compose down
cd ..

# Stop frontend
echo "🎨 Stopping Frontend..."
pkill -f "vite"

echo ""
echo "✅ All services stopped!"
echo ""