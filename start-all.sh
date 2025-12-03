#!/bin/bash

echo "🚀 Starting AirWatch Station..."

# Start backend
echo "📦 Starting ThingsBoard..."
cd thingsboard_docker
docker-compose up -d
cd ..

# Wait for ThingsBoard
echo "⏳ Waiting for ThingsBoard (3 minutes)..."
sleep 180

# Start frontend
echo "🎨 Starting Frontend..."
cd air-watch
npm run dev &
cd ..

echo ""
echo "✅ All services started!"
echo ""