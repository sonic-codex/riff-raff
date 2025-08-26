#!/bin/bash

# Riff Raff Generator Startup Script
echo "🎤 Starting Riff Raff Generator..."

# Check if virtual environment exists
if [ ! -d "env" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv env
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source env/bin/activate

# Install dependencies if needed
if [ ! -f "env/lib/python*/site-packages/streamlit" ]; then
    echo "📥 Installing dependencies..."
    pip install -r requirements.txt
fi

# Start the application
echo "🚀 Starting Streamlit app..."
echo "🌐 App will be available at: http://localhost:8501"
echo "🛑 Press Ctrl+C to stop the server"
echo ""

streamlit run streamlit_app.py --server.headless true --server.port 8501