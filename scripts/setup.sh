#!/bin/bash

# Meyers Scraper Setup Script

echo "🚀 Setting up Meyers Scraper..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# Create virtual environment if it doesn't exist
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

# Set up environment file
if [ ! -f "$PROJECT_ROOT/config/.env" ]; then
    echo "⚙️  Setting up environment configuration..."
    if [ -f "$PROJECT_ROOT/config/.env.example" ]; then
        cp "$PROJECT_ROOT/config/.env.example" "$PROJECT_ROOT/config/.env"
        echo "✅ Created .env file from template"
        echo "📝 Please edit config/.env with your specific settings"
    else
        echo "⚠️  No .env.example found. Please create config/.env manually"
    fi
fi

echo ""
echo "🎉 Setup complete!"
echo ""
echo "📋 Next steps:"
echo "   • Edit config/.env with your settings"
echo "   • Run './scripts/start_api.sh' to start the API server"
echo "   • Run './scripts/start_mcp.sh' to start the MCP server"
echo "   • Run 'python scripts/run_tests.py' to run tests"
echo ""
echo "📚 Documentation:"
echo "   • Main README: README.md"
echo "   • API docs: docs/API_README.md"
echo "   • MCP docs: docs/MCP_README.md"
echo "" 