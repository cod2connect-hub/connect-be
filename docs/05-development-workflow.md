# Development workflow

## Local prerequisites

- Python 3.12 or newer
- `uv`
- Docker with Compose for Redis, Mailpit, and MinIO
- A Neon PostgreSQL branch or another compatible PostgreSQL database

Copy `.env.example` to `.env`, provide development-only credentials, then use the Makefile as the supported command surface.

## Commands

| Command | Purpose |
|---|---|
| `make install` | Install locked development dependencies |
| `make services-up` | Start local supporting services |
| `make dev` | Run the API with reload |
| `make worker` | Run the background worker |
| `make migrate` | Apply database migrations |
| `make migration name=...` | Create a named migration skeleton |
| `make test` | Run the normal test suite |
| `make test-unit` | Run fast unit and application tests |
| `make test-integration` | Run infrastructure/interface/contract/security tests |
| `make test-e2e` | Run end-to-end tests |
| `make lint` | Run static lint checks |
| `make format` | Format code |
| `make invariants` | Run architecture and safety checks |
| `make check` | Run the local CI-equivalent checks |

## Adding a feature

1. Find the owning engine in [03-capability-map.md](03-capability-map.md).
2. If ownership is unclear or a new boundary is proposed, write an ADR before creating a package.
3. Define the use case, authorization, entitlement, idempotency, events, and data ownership.
4. Add tests from the outside of the layer inward.
5. Add a migration with RLS for tenant-owned tables.
6. Implement domain/application behavior, then infrastructure and interface adapters.
7. Register public surfaces only in the composition root.
8. Update module README and architecture docs in the same change.

## Repository hygiene

- Do not create a `src/` package or parallel application tree.
- Do not place business services in `app/core/`.
- Do not add niche-specific copies of shared engines.
- Do not commit caches, local environments, secrets, generated coverage, or build artifacts.
- Do not hand-edit `uv.lock`; update dependencies through `uv`.
