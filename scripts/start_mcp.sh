#!/bin/bash

# Meyers Scraper MCP Server Startup Script

echo "🚀 Starting Meyers Scraper MCP Server..."

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

# Install/update dependencies
echo "📥 Installing dependencies..."
pip install -r "$PROJECT_ROOT/requirements.txt"

# Set environment variables (if not already set)
export MCP_PORT=${MCP_PORT:-8001}
export SCHOOL_ID=${SCHOOL_ID:-"CxnRNYOtBo6VrqiCb4AA"}
export DEFAULT_LANGUAGE=${DEFAULT_LANGUAGE:-"en"}
export TARGET_OFFER_ID=${TARGET_OFFER_ID:-"ob6V4HfZK9Gs95sii4Cf"}
export LOG_LEVEL=${LOG_LEVEL:-"INFO"}

echo "⚙️  Configuration:"
echo "   - MCP Port: $MCP_PORT"
echo "   - School ID: $SCHOOL_ID"
echo "   - Language: $DEFAULT_LANGUAGE"
echo "   - Target Offer ID: $TARGET_OFFER_ID"
echo "   - Log Level: $LOG_LEVEL"

# Start the MCP server
echo "🎯 Starting MCP server..."
python "$PROJECT_ROOT/mcp_server.py" 