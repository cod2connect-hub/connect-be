# 🚀 Setup Checklist

Use this checklist to get your backend up and running.

## Initial Setup

- [ ] **Install uv**
  ```bash
  curl -LsSf https://astral.sh/uv/install.sh | sh
  ```

- [ ] **Create virtual environment**
  ```bash
  uv venv
  source .venv/bin/activate
  ```

- [ ] **Install dependencies**
  ```bash
  uv pip install -e ".[dev]"
  ```

## Database Setup (Neon)

- [ ] **Create Neon account** at https://neon.tech
- [ ] **Create new project** (choose region)
- [ ] **Create database** named `connectdb`
- [ ] **Copy connection string** from dashboard
- [ ] **Update .env file**
  ```bash
  cp .env.example .env
  # Edit .env with your database URL
  ```

## Configuration

- [ ] **Set DATABASE_URL** in `.env`
  ```env
  DATABASE_URL=postgresql+asyncpg://user:pass@ep-xxx.neon.tech/connectdb?sslmode=require
  ```

- [ ] **Generate SECRET_KEY**
  ```bash
  python -c "import secrets; print(secrets.token_hex(32))"
  # Copy output to .env SECRET_KEY
  ```

- [ ] **Configure CORS** (optional)
  ```env
  ALLOWED_ORIGINS=["http://localhost:3000", "http://localhost:5173"]
  ```

## Database Migrations

- [ ] **Create initial migration**
  ```bash
  alembic revision --autogenerate -m "Initial tables"
  ```

- [ ] **Review migration** in `alembic/versions/`

- [ ] **Apply migration**
  ```bash
  alembic upgrade head
  ```

- [ ] **Verify in Neon dashboard** that tables exist

## Start Server

- [ ] **Run development server**
  ```bash
  uvicorn src.main:app --reload --port 8000
  # or use: ./scripts/run_dev.sh
  ```

- [ ] **Check server is running**
  - Visit: http://localhost:8000
  - Should see: `{"message": "Connect Backend API", ...}`

- [ ] **Check health endpoint**
  - Visit: http://localhost:8000/health
  - Should see: `{"status": "healthy", ...}`

- [ ] **Open API docs**
  - Visit: http://localhost:8000/docs
  - Should see Swagger UI with endpoints

## Test API Endpoints

- [ ] **Test subdomain check**
  ```bash
  curl -X POST http://localhost:8000/public/tenants/check-subdomain \
    -H "Content-Type: application/json" \
    -d '{"business_name": "Test Restaurant"}'
  ```
  Expected: `{"suggested_subdomain": "test-restaurant", "available": true, ...}`

- [ ] **Create test tenant**
  ```bash
  curl -X POST http://localhost:8000/public/tenants \
    -H "Content-Type: application/json" \
    -d '{
      "business_name": "Test Restaurant",
      "subdomain": "testrestaurant",
      "owner_email": "test@example.com",
      "owner_password": "TestPass123!",
      "niche_type": "restaurant"
    }'
  ```
  Expected: Tenant object with id, subdomain, status: "onboarding"

- [ ] **Test login**
  ```bash
  curl -X POST http://localhost:8000/public/auth/login \
    -H "Content-Type: application/json" \
    -d '{
      "email": "test@example.com",
      "password": "TestPass123!"
    }'
  ```
  Expected: `{"access_token": "...", "token_type": "bearer", ...}`

## Verify Database

- [ ] **Check Neon dashboard**
  - Go to https://neon.tech
  - Open your project
  - Click "Tables"
  - Should see: `tenants` and `users` tables

- [ ] **Query tenant**
  ```sql
  SELECT * FROM tenants WHERE subdomain = 'testrestaurant';
  ```

- [ ] **Query user**
  ```sql
  SELECT email, role, is_active FROM users WHERE email = 'test@example.com';
  ```

## Development Workflow

- [ ] **Run tests**
  ```bash
  pytest
  ```

- [ ] **Format code**
  ```bash
  black src/ tests/
  ```

- [ ] **Lint code**
  ```bash
  ruff check src/ tests/
  ```

## Git Setup (Already Done ✅)

- [x] Repository connected to https://github.com/cod2connect-hub/connect-be.git
- [ ] **Commit initial code**
  ```bash
  git add .
  git commit -m "feat: initial backend setup with tenant management"
  git push origin main
  ```

## Documentation Review

- [ ] Read `README.md` - Main documentation
- [ ] Read `SETUP_GUIDE.md` - Quick setup instructions
- [ ] Read `PROJECT_SUMMARY.md` - What's been built
- [ ] Review `backend-implementation-plan.md` - Full roadmap

## Next Steps

- [ ] Review Phase 2 in implementation plan
- [ ] Choose which engine to implement first (scheduling, catalog, forms, etc.)
- [ ] Set up Stripe account for payments engine
- [ ] Plan feature & billing models
- [ ] Design first niche configuration (restaurant, salon, etc.)

---

## ✅ Success Criteria

Your setup is complete when:

1. ✅ Server starts without errors
2. ✅ `/docs` shows all API endpoints
3. ✅ Can create a tenant via API
4. ✅ Can login and get JWT token
5. ✅ Tables exist in Neon dashboard
6. ✅ Tests pass with `pytest`

## 🆘 Need Help?

- Check `SETUP_GUIDE.md` for troubleshooting
- Review error logs in terminal
- Verify `.env` configuration
- Check Neon database connection in dashboard

---

**Once all items are checked, you're ready to build! 🎉**
