# ⚡ Quick Reference Card

Quick commands for daily development.

## 🚀 Common Commands

### Setup & Installation
```bash
./scripts/setup.sh                    # Full automated setup
uv venv                               # Create virtual environment
source .venv/bin/activate             # Activate venv (Linux/Mac)
.venv\Scripts\activate                # Activate venv (Windows)
uv pip install -e ".[dev]"           # Install dependencies
```

### Development Server
```bash
./scripts/run_dev.sh                  # Start dev server (script)
uvicorn src.main:app --reload         # Start dev server (manual)
uvicorn src.main:app --reload --port 8000 --host 0.0.0.0  # Full command
```

### Database Migrations
```bash
alembic revision --autogenerate -m "Description"  # Create migration
./scripts/create_migration.sh "Description"       # Create (script)
alembic upgrade head                              # Apply all migrations
alembic downgrade -1                              # Rollback one migration
alembic current                                   # Show current version
alembic history                                   # Show migration history
```

### Testing
```bash
pytest                                # Run all tests
pytest tests/test_example.py          # Run specific test file
pytest -v                             # Verbose output
pytest --cov=src                      # With coverage report
```

### Code Quality
```bash
black src/ tests/                     # Format code
ruff check src/ tests/                # Lint code
mypy src/                             # Type checking
```

### Git Commands
```bash
git status                            # Check status
git add .                             # Stage all changes
git commit -m "message"               # Commit with message
git push origin main                  # Push to main branch
```

## 📍 Important URLs

| URL | Description |
|-----|-------------|
| http://localhost:8000 | Root API endpoint |
| http://localhost:8000/docs | Swagger UI (API documentation) |
| http://localhost:8000/redoc | ReDoc (Alternative API docs) |
| http://localhost:8000/health | Health check endpoint |
| https://neon.tech | Neon database dashboard |
| https://github.com/cod2connect-hub/connect-be | GitHub repository |

## 🧪 Test Endpoints (cURL)

### Health Check
```bash
curl http://localhost:8000/health
```

### Check Subdomain
```bash
curl -X POST http://localhost:8000/public/tenants/check-subdomain \
  -H "Content-Type: application/json" \
  -d '{"business_name": "My Business"}'
```

### Create Tenant
```bash
curl -X POST http://localhost:8000/public/tenants \
  -H "Content-Type: application/json" \
  -d '{
    "business_name": "My Business",
    "subdomain": "mybusiness",
    "owner_email": "owner@example.com",
    "owner_password": "SecurePass123!",
    "niche_type": "restaurant"
  }'
```

### Login
```bash
curl -X POST http://localhost:8000/public/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "owner@example.com", "password": "SecurePass123!"}'
```

### Authenticated Request (Example)
```bash
TOKEN="your-jwt-token-here"
curl http://localhost:8000/admin_api/endpoint \
  -H "Authorization: Bearer $TOKEN"
```

## 📂 Project Structure Quick Reference

```
src/
├── core/           # Config, database, security, events, middleware
├── tenants/        # Tenant & user management, onboarding
├── engines/        # 13 reusable engines
│   ├── scheduling/
│   ├── catalog/
│   ├── forms/
│   ├── payments/
│   ├── crm/
│   ├── portal/
│   ├── documents/
│   ├── notifications/
│   ├── reviews/
│   ├── search/
│   ├── loyalty/
│   ├── calculators/
│   └── media/
├── features/       # Niche configurations
├── billing/        # Platform billing
├── themes/         # Theme registry
├── admin_api/      # Admin panel endpoints
├── public_api/     # Public site endpoints
├── platform_api/   # Super-admin endpoints
└── main.py         # FastAPI application entry point
```

## 🔧 Useful Python Snippets

### Generate Secret Key
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

### Open Python REPL with app context
```bash
python
>>> from src.core.config import settings
>>> from src.core.database import async_session_maker
>>> print(settings.DATABASE_URL)
```

### Test Database Connection
```python
import asyncio
from src.core.database import engine

async def test_connection():
    async with engine.connect() as conn:
        print("✅ Database connection successful!")

asyncio.run(test_connection())
```

## 🐛 Troubleshooting Quick Fixes

### Module Not Found Error
```bash
uv pip install -e ".[dev]"
```

### Database Connection Error
Check `.env` file:
- Must use `postgresql+asyncpg://` (not `postgresql://`)
- Must include `?sslmode=require` for Neon
- Verify credentials in Neon dashboard

### Port Already in Use
```bash
lsof -ti:8000 | xargs kill -9    # Kill process on port 8000
uvicorn src.main:app --reload --port 8001  # Use different port
```

### Migration Issues
```bash
alembic downgrade -1              # Rollback one migration
rm alembic/versions/*.py          # Delete migration files
alembic revision --autogenerate -m "Fresh migration"
alembic upgrade head
```

## 📝 Environment Variables Checklist

Essential `.env` variables:
```env
DATABASE_URL=postgresql+asyncpg://user:pass@xxx.neon.tech/db?sslmode=require
SECRET_KEY=your-generated-secret-key
DEBUG=True
ENVIRONMENT=development
```

Optional variables:
```env
STRIPE_SECRET_KEY=sk_test_xxx
REDIS_URL=redis://localhost:6379/0
CLOUDFLARE_API_TOKEN=xxx
ALLOWED_ORIGINS=["http://localhost:3000"]
```

## 📚 Documentation Files

| File | Description |
|------|-------------|
| `README.md` | Main project documentation |
| `SETUP_GUIDE.md` | Step-by-step setup instructions |
| `PROJECT_SUMMARY.md` | What's been built, architecture overview |
| `CHECKLIST.md` | Interactive setup checklist |
| `QUICK_REFERENCE.md` | This file - quick commands |
| `backend-implementation-plan.md` | Complete implementation roadmap |

## 🎯 Next Implementation Priorities

1. **Scheduling Engine** - Bookings & appointments
2. **Catalog Engine** - Products & services
3. **Forms Engine** - Dynamic forms
4. **Payments Engine** - Stripe integration
5. **Notifications Engine** - Email/SMS

## 💡 Tips

- Use `./scripts/` for common tasks
- Check `/docs` endpoint for API documentation
- Run `pytest` before committing
- Keep `.env` secrets secure (never commit!)
- Use Alembic for all schema changes
- Test endpoints with Swagger UI at `/docs`

---

**Keep this file handy for quick reference during development!** 📌
