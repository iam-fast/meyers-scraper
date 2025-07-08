#!/bin/bash

# Meyers Scraper FastAPI Startup Script

echo "🚀 Starting Meyers Scraper FastAPI..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# Check if virtual environment exists
if [ ! -d "$PROJECT_ROOT/venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv "$PROJECT_ROOT/venv"
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source "$PROJECT_ROOT/venv/bin/activate"

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r "$PROJECT_ROOT/requirements.txt"

# Check if .env file exists
if [ ! -f "$PROJECT_ROOT/config/.env" ]; then
    echo "⚠️  No .env file found. Creating default .env file..."
    cp "$PROJECT_ROOT/config/.env.example" "$PROJECT_ROOT/config/.env" 2>/dev/null || echo "No .env.example found. Please create a .env file manually."
fi

# Start the FastAPI
echo "🌐 Starting FastAPI server..."
echo "📋 API will be available at: http://localhost:5015"
echo "📋 Health check: http://localhost:5015/api/health/"
echo "📋 Swagger docs: http://localhost:5015/docs"
echo "📋 ReDoc docs: http://localhost:5015/redoc"
echo "📋 OpenAPI JSON: http://localhost:5015/openapi.json"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

python "$PROJECT_ROOT/app.py" 