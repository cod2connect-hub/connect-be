# 🚀 Quick Setup Guide

This guide will help you set up the Connect Backend project in minutes.

## Prerequisites

- **Python 3.11+**
- **Neon PostgreSQL account** (free tier available at https://neon.tech)
- **Git**

## Step-by-Step Setup

### 1. Install uv (Python Package Manager)

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Or use the automated setup script:

```bash
./scripts/setup.sh
```

### 2. Set Up Neon Database

1. Go to https://neon.tech and create a free account
2. Create a new project (choose a region close to you)
3. Create a database called `connectdb`
4. Copy your connection string from the dashboard

Your connection string will look like:
```
postgresql://user:password@ep-xxx.us-east-2.aws.neon.tech/connectdb
```

### 3. Configure Environment Variables

```bash
cp .env.example .env
```

Edit `.env` and update these required values:

```env
# Change the connection string to your Neon database
# IMPORTANT: Use postgresql+asyncpg:// instead of postgresql://
DATABASE_URL=postgresql+asyncpg://user:password@ep-xxx.us-east-2.aws.neon.tech/connectdb?sslmode=require

# Generate a secure secret key (use: openssl rand -hex 32)
SECRET_KEY=your-generated-secret-key-here
```

### 4. Install Dependencies

```bash
# Create virtual environment
uv venv

# Activate it
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
uv pip install -e ".[dev]"
```

### 5. Run Database Migrations

```bash
# Create initial migration
alembic revision --autogenerate -m "Initial tables"

# Apply migrations
alembic upgrade head
```

### 6. Start the Development Server

```bash
uvicorn src.main:app --reload --port 8000
```

Or use the convenience script:

```bash
./scripts/run_dev.sh
```

### 7. Test the API

Visit http://localhost:8000/docs to see the interactive API documentation.

Or test with curl:

```bash
# Health check
curl http://localhost:8000/health

# Check subdomain availability
curl -X POST http://localhost:8000/public/tenants/check-subdomain \
  -H "Content-Type: application/json" \
  -d '{"business_name": "My Cool Restaurant"}'
```

## Common Issues & Solutions

### Issue: "ModuleNotFoundError: No module named 'src'"

**Solution**: Make sure you installed with `-e` flag:
```bash
uv pip install -e ".[dev]"
```

### Issue: Database connection error

**Solution**: 
1. Check your `DATABASE_URL` in `.env`
2. Make sure it starts with `postgresql+asyncpg://` (not just `postgresql://`)
3. Add `?sslmode=require` at the end for Neon
4. Test connection in Neon dashboard

### Issue: "SECRET_KEY not set"

**Solution**: Generate a secure key:
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```
Copy the output to `SECRET_KEY` in `.env`

## API Testing Examples

### 1. Create a New Tenant

```bash
curl -X POST http://localhost:8000/public/tenants \
  -H "Content-Type: application/json" \
  -d '{
    "business_name": "My Restaurant",
    "subdomain": "myrestaurant",
    "owner_email": "owner@myrestaurant.com",
    "owner_password": "SecurePass123!",
    "niche_type": "restaurant"
  }'
```

### 2. Login

```bash
curl -X POST http://localhost:8000/public/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "owner@myrestaurant.com",
    "password": "SecurePass123!"
  }'
```

Response will include an `access_token` - save this for authenticated requests!

### 3. Make Authenticated Request (Example for future endpoints)

```bash
# Replace YOUR_TOKEN with the access_token from login
curl http://localhost:8000/admin_api/something \
  -H "Authorization: Bearer YOUR_TOKEN"
```

## Development Commands

### Create New Migration

```bash
./scripts/create_migration.sh "Add feature table"
# or
alembic revision --autogenerate -m "Add feature table"
```

### Apply Migrations

```bash
alembic upgrade head
```

### Rollback Migration

```bash
alembic downgrade -1
```

### Format Code

```bash
black src/ tests/
```

### Lint Code

```bash
ruff check src/ tests/
```

### Run Tests

```bash
pytest
```

## Project Structure Overview

```
connect-be/
├── src/                    # Source code (not 'app')
│   ├── core/              # Config, database, security
│   ├── tenants/           # Tenant management ✅
│   ├── engines/           # 13 reusable engines
│   │   ├── scheduling/    # 🚧 Next
│   │   ├── catalog/       # 🚧 Next
│   │   └── ...
│   └── main.py           # FastAPI app ✅
├── alembic/              # Migrations ✅
├── scripts/              # Helper scripts ✅
└── tests/               # Tests 📋
```

## Next Steps After Setup

1. **Explore the API**: Visit http://localhost:8000/docs
2. **Read the Implementation Plan**: Check `backend-implementation-plan.md`
3. **Start Building**: Next phase is implementing the core engines (scheduling, catalog, forms, etc.)

## Getting Help

- Check the main README.md for detailed documentation
- Review the implementation plan in `backend-implementation-plan.md`
- Look at API docs at `/docs` endpoint

## Quick Reference

| Command | Description |
|---------|-------------|
| `./scripts/setup.sh` | Full setup (install uv, create venv, install deps) |
| `./scripts/run_dev.sh` | Start development server |
| `./scripts/create_migration.sh "msg"` | Create new migration |
| `alembic upgrade head` | Apply all migrations |
| `pytest` | Run tests |
| `black src/` | Format code |

---

**Ready to build!** 🎉

The backend is now configured with:
- ✅ FastAPI with async support
- ✅ PostgreSQL (Neon) with SQLAlchemy
- ✅ Tenant model & authentication
- ✅ Event bus for cross-engine communication
- ✅ Initial API routes for onboarding
- ✅ Migration system with Alembic

Next: Implement the 13 core engines! 🚀
