#!/bin/bash
cd "$(dirname "$0")"

echo "=========================================="
echo "⚡ Starting AgentX Platform..."
echo "=========================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required. Please install Python 3."
    read -p "Press Enter to exit..."
    exit 1
fi

# Set up virtual environment if not present or broken
if [ ! -f ".venv/bin/activate" ]; then
    echo "📦 Setting up Python virtual environment..."
    rm -rf .venv venv
    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
else
    source .venv/bin/activate
fi

PORT="${PORT:-5001}"

# Open browser after 1.5 seconds in background
(sleep 1.5 && open "http://127.0.0.1:${PORT}") &

# Start Flask server
echo "🚀 Server running at http://127.0.0.1:${PORT}"
echo "Press Ctrl+C to stop the server."
echo ""
python3 app.py
