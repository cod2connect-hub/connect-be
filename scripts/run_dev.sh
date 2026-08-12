#!/bin/bash
# Run development server

set -e

# Activate virtual environment
if [ -f ".venv/bin/activate" ]; then
    source .venv/bin/activate
else
    echo "❌ Virtual environment not found. Run ./scripts/setup.sh first"
    exit 1
fi

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "❌ .env file not found. Copy .env.example to .env and configure it"
    exit 1
fi

echo "🚀 Starting development server..."
uvicorn src.main:app --reload --port 8000 --host 0.0.0.0
