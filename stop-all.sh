#!/bin/bash

echo "🛑 Stopping AirWatch Station..."

# Stop frontend and chatbot by PID
if [ -f .airwatch-pids ]; then
    echo "🎨 Stopping Frontend..."
    FRONTEND_PID=$(tail -1 .airwatch-pids)
    kill $FRONTEND_PID 2>/dev/null
    
    echo "🐍 Stopping Chatbot Backend..."
    CHATBOT_PID=$(head -1 .airwatch-pids)
    kill $CHATBOT_PID 2>/dev/null
    
    rm .airwatch-pids
else
    echo "⚠️  No PIDs file found. Trying fallback method..."
    pkill -f "npm run dev"
    pkill -f "python app.py"
fi

# Wait a moment for processes to terminate
sleep 2

# Stop backend
echo "📦 Stopping ThingsBoard..."
cd thingsboard_docker
docker-compose down
cd ..

echo ""
echo "✅ All services stopped!"
echo ""