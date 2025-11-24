#!/bin/bash

# Quick script to start backend locally for development

echo "🚀 Starting EdweavePack backend..."

# Check if we're in the backend directory
if [ ! -f "main.py" ]; then
    echo "📁 Changing to backend directory..."
    cd backend
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "🐍 Creating virtual environment..."
    python -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    source venv/Scripts/activate
else
    source venv/bin/activate
fi

# Install dependencies if needed
if [ ! -f "venv/installed" ]; then
    echo "📦 Installing dependencies..."
    pip install -r requirements.txt
    touch venv/installed
fi

# Start the server
echo "🌐 Starting FastAPI server..."
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000