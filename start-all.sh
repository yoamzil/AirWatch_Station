#!/bin/bash

echo "🚀 Starting AirWatch Station..."

# Start backend
echo "📦 Starting ThingsBoard..."
cd thingsboard_docker
docker-compose up -d
if [ $? -ne 0 ]; then
    echo "❌ Failed to start ThingsBoard"
    exit 1
fi
cd ..

# Wait for ThingsBoard
echo "⏳ Waiting for ThingsBoard (3 minutes)..."
sleep 180

# Start Chatbot backend
echo "🐍 Starting Chatbot Backend..."
cd ems-chatbot
source venv/bin/activate
python app.py &
CHATBOT_PID=$!
cd ..
sleep 5

# Start frontend
echo "🎨 Starting Frontend..."
cd air-watch
npm run dev &
FRONTEND_PID=$!
cd ..

# Save PIDs to file for later cleanup
echo "$CHATBOT_PID" > .airwatch-pids
echo "$FRONTEND_PID" >> .airwatch-pids

echo ""
echo "✅ All services started!"
echo "   Chatbot PID: $CHATBOT_PID"
echo "   Frontend PID: $FRONTEND_PID"
echo ""
echo "To stop all services, run: ./stop-all.sh"
echo ""