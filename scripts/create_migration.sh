#!/bin/bash
# Create a new database migration

set -e

if [ -z "$1" ]; then
    echo "Usage: ./scripts/create_migration.sh 'migration description'"
    exit 1
fi

# Activate virtual environment
if [ -f ".venv/bin/activate" ]; then
    source .venv/bin/activate
else
    echo "❌ Virtual environment not found. Run ./scripts/setup.sh first"
    exit 1
fi

echo "📝 Creating migration: $1"
alembic revision --autogenerate -m "$1"
echo "✅ Migration created"
