# Connect Backend

Multi-Niche Website Builder SaaS Backend built with FastAPI, PostgreSQL (Neon), and modern Python tools.

## Architecture

This is a **modular monolith** with 13 reusable engines that power 25+ niches:

- **Scheduling & Booking** - appointments, reservations, classes
- **Catalog & Inventory** - products, services, menu items
- **Forms & Intake** - contact forms, questionnaires, applications
- **Payments & Billing** - checkout, invoicing, subscriptions
- **CRM & Leads** - lead capture, contact management
- **Client Portal** - customer/patient/tenant portals
- **Documents & E-Signature** - contracts, lease signing
- **Notifications** - email/SMS/push reminders
- **Reviews & Testimonials** - ratings, feedback
- **Search & Comparison** - property search, filters
- **Loyalty & Membership** - rewards, tiers, gift cards
- **Calculators** - quotes, estimates, cost calculators
- **Media & Content** - galleries, blogs, virtual tours

## Tech Stack

- **Framework**: FastAPI 0.115+
- **Database**: PostgreSQL (Neon for development)
- **ORM**: SQLAlchemy 2.0 (async)
- **Migrations**: Alembic
- **Package Manager**: uv
- **Authentication**: JWT with python-jose
- **Payments**: Stripe
- **Python**: 3.11+

## Project Structure

```
connect-be/
├── src/                          # Source code (not 'app')
│   ├── core/                     # Config, database, security, events
│   ├── tenants/                  # Tenant lifecycle, onboarding
│   ├── engines/                  # 13 reusable engines
│   │   ├── scheduling/
│   │   ├── catalog/
│   │   ├── forms/
│   │   ├── payments/
│   │   ├── crm/
│   │   ├── portal/
│   │   ├── documents/
│   │   ├── notifications/
│   │   ├── reviews/
│   │   ├── search/
│   │   ├── loyalty/
│   │   ├── calculators/
│   │   └── media/
│   ├── features/                 # Niche configurations
│   ├── billing/                  # Platform billing
│   ├── themes/                   # Theme registry
│   ├── admin_api/                # Admin panel endpoints
│   ├── public_api/               # Public site endpoints
│   ├── platform_api/             # Super-admin endpoints
│   └── main.py                   # FastAPI app
├── alembic/                      # Database migrations
├── tests/                        # Test suite
├── workers/                      # Background jobs (future)
├── pyproject.toml                # Project dependencies
└── .env                          # Environment variables
```

## Getting Started

### Prerequisites

- Python 3.11+
- uv (Python package manager)
- Neon PostgreSQL account (or any PostgreSQL database)

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/cod2connect-hub/connect-be.git
   cd connect-be
   ```

2. **Install uv** (if not already installed):
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

3. **Create virtual environment and install dependencies**:
   ```bash
   uv venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   uv pip install -e ".[dev]"
   ```

4. **Set up environment variables**:
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` and configure your database:
   ```env
   DATABASE_URL=postgresql+asyncpg://user:password@ep-xxx.us-east-2.aws.neon.tech/connectdb?sslmode=require
   SECRET_KEY=your-secret-key-here-change-in-production
   ```

5. **Create initial migration**:
   ```bash
   alembic revision --autogenerate -m "Initial tables"
   ```

6. **Run migrations**:
   ```bash
   alembic upgrade head
   ```

7. **Start the development server**:
   ```bash
   uvicorn src.main:app --reload --port 8000
   ```

8. **Visit the API docs**:
   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

## Setting Up Neon Database

1. **Create Neon account**: https://neon.tech
2. **Create a new project** and database
3. **Get connection string**:
   - Go to your project dashboard
   - Copy the connection string (it looks like: `postgresql://user:password@ep-xxx.us-east-2.aws.neon.tech/dbname`)
4. **Update .env file**:
   ```env
   DATABASE_URL=postgresql+asyncpg://user:password@ep-xxx.us-east-2.aws.neon.tech/connectdb?sslmode=require
   ```
   Note: Change `postgresql://` to `postgresql+asyncpg://` for async support

## Available API Endpoints

### Public Endpoints (Onboarding)

- `POST /public/tenants/check-subdomain` - Check subdomain availability
- `POST /public/tenants` - Create new tenant account
- `POST /public/auth/login` - Login and get JWT token

### Health & Info

- `GET /health` - Health check
- `GET /` - API info

### Future Endpoints (Coming Soon)

- Feature selection & pricing
- Theme configuration
- Admin panel APIs
- Engine-specific endpoints

## Testing the API

### 1. Check subdomain availability

```bash
curl -X POST http://localhost:8000/public/tenants/check-subdomain \
  -H "Content-Type: application/json" \
  -d '{"business_name": "My Restaurant"}'
```

### 2. Create a new tenant

```bash
curl -X POST http://localhost:8000/public/tenants \
  -H "Content-Type: application/json" \
  -d '{
    "business_name": "My Restaurant",
    "subdomain": "myrestaurant",
    "owner_email": "owner@myrestaurant.com",
    "owner_password": "securepassword123",
    "niche_type": "restaurant"
  }'
```

### 3. Login

```bash
curl -X POST http://localhost:8000/public/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "owner@myrestaurant.com",
    "password": "securepassword123"
  }'
```

## Development

### Run with auto-reload:
```bash
uvicorn src.main:app --reload --port 8000
```

### Create new migration:
```bash
alembic revision --autogenerate -m "Description of changes"
```

### Apply migrations:
```bash
alembic upgrade head
```

### Run tests:
```bash
pytest
```

### Format code:
```bash
black src/ tests/
```

### Lint code:
```bash
ruff check src/ tests/
```

## Implementation Status

### ✅ Phase 1 (Completed)
- [x] Project structure with `src/` directory
- [x] Core configuration and settings
- [x] Database setup with SQLAlchemy async
- [x] Event bus for cross-engine communication
- [x] Security utilities (JWT, password hashing)
- [x] Tenant model and user model
- [x] Tenant middleware for subdomain resolution
- [x] Initial API routes (subdomain check, tenant creation, login)
- [x] Alembic migrations setup

### 🚧 Phase 2 (Next)
- [ ] Feature & billing models
- [ ] Scheduling engine
- [ ] Catalog engine
- [ ] Forms engine
- [ ] Payments engine (Stripe integration)
- [ ] Notifications engine

### 📋 Phase 3 (Planned)
- [ ] Remaining 8 engines
- [ ] Admin API completion
- [ ] Platform API
- [ ] Background jobs with ARQ

## Environment Variables

See `.env.example` for all available configuration options.

Key variables:
- `DATABASE_URL` - PostgreSQL connection string (required)
- `SECRET_KEY` - JWT secret key (required)
- `STRIPE_SECRET_KEY` - Stripe API key (required for payments)
- `CLOUDFLARE_API_TOKEN` - For subdomain DNS management

## Contributing

1. Create a feature branch
2. Make your changes
3. Add tests
4. Run linting and tests
5. Submit a pull request

## License

Proprietary - All rights reserved
