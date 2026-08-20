# Connect Backend

Backend for a multi-tenant website and business-operations platform serving 25 niche markets through reusable capabilities.

The repository is a FastAPI modular monolith. The only application package is root-level `app/`; niches compose shared engines instead of duplicating business logic.

## Start here

- [System overview](docs/00-system-overview.md)
- [Backend architecture](docs/01-architecture.md)
- [Identity, RBAC, and tenant isolation](docs/02-rbac.md)
- [Niche-to-capability comparison](docs/03-capability-map.md)
- [Testing strategy](docs/04-testing-strategy.md)
- [Development workflow](docs/05-development-workflow.md)
- [Implementation guide](docs/backend-implementation-guide.md)
- [Phase-wise implementation playbook](docs/implementation/README.md)
- [Original niche feature breakdown](docs/niche-feature-breakdown.md)

## Repository shape

```text
app/          application package, platform contexts, engines, workers
docs/         architecture, feature map, workflow, and ADRs
migrations/   ordered PostgreSQL/Alembic migrations
scripts/      executable architecture and safety checks
seeds/        permissions, roles, features, and defaults
tests/        tests grouped by architectural concern
```

## Local setup

```bash
cp .env.example .env
make install
make services-up
make migrate
make dev
```

Run `make help` for the complete development command list. PostgreSQL is expected from Neon during development; Docker Compose starts Redis, Mailpit, and MinIO.

## Current scope

The repository has architecture documentation and package skeletons for the complete capability map. Empty skeletons record ownership only; implementation should follow the phases and acceptance checklist in the implementation guide.
