#!/bin/bash

echo "🚀 Starting OpenWebUI Frontend (Local Development)"
echo "📍 Frontend will be available at: http://localhost:6969"
echo "🔗 Backend API: http://localhost:8000"
echo ""

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo "📦 Installing dependencies..."
    npm install
    if [ $? -ne 0 ]; then
        echo "❌ Failed to install dependencies"
        exit 1
    fi
fi

# Check if backend is running
echo "🔍 Checking if backend is running..."
if curl -s http://localhost:8000/health > /dev/null 2>&1; then
    echo "✅ Backend is running at http://localhost:8000"
else
    echo "⚠️  Backend is not running at http://localhost:8000"
    echo "   Please start the backend first with: cd ../backend-render && python start_local.py"
    echo "   Or continue without backend (some features may not work)"
    echo ""
fi

echo ""
echo "🌐 Starting frontend development server..."
echo "Press Ctrl+C to stop the server"
echo ""

# Start the development server
npm run dev
