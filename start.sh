#!/bin/bash

echo "🚀 Starting EventPulse NC..."

# Start backend in background
echo "📡 Starting backend server..."
cd backend && npm start &
BACKEND_PID=$!

# Wait a moment for backend to start
sleep 3

# Start frontend in background
echo "🎨 Starting frontend server..."
cd ../frontend && npm start &
FRONTEND_PID=$!

echo "✅ EventPulse NC is starting up!"
echo "📡 Backend: http://localhost:3001"
echo "🎨 Frontend: http://localhost:3000"
echo ""
echo "Press Ctrl+C to stop both servers"

# Wait for user to stop
wait 