# Testing strategy

## Test suites

| Suite | Location | Purpose | External dependencies |
|---|---|---|---|
| Unit | `tests/unit/` | Pure entities, value objects, rules, parsers | None |
| Application | `tests/application/` | Use-case orchestration with fake ports | None |
| Infrastructure | `tests/infrastructure/` | SQL repositories, mappings, RLS, migrations | Ephemeral PostgreSQL |
| Interface | `tests/interface/` | HTTP validation, auth, permissions, problem responses | In-process API and fakes |
| Contract | `tests/contract/` | Event/schema compatibility and adapter contracts | Fakes or provider sandbox when isolated |
| Architecture | `tests/architecture/` | Import boundaries, ownership, route declarations, SQL location | None |
| Security | `tests/security/` | Cross-tenant isolation, authorization matrix, webhook verification | PostgreSQL where needed |
| End-to-end | `tests/e2e/` | Critical API → database → outbox → worker flows | Local service stack |

## Required patterns

- Domain tests are deterministic and do not use FastAPI or a database.
- Application tests use protocol-compatible fakes and assert state plus emitted events.
- Repository tests execute real PostgreSQL SQL; SQLite is not an acceptable substitute.
- Every tenant-owned repository has a two-tenant isolation test.
- Every state-changing route tests permission, feature entitlement, idempotency, and invalid-state behavior.
- Contract tests freeze event name, version, required fields, and compatibility behavior.
- Worker tests prove retry safety and duplicate delivery behavior.
- Migration tests upgrade a blank database and validate RLS coverage.

## Test data

Factories create explicit tenant, actor, clock, and identifier values. Tests do not depend on execution order, wall-clock time, or shared database state. Sensitive niche fixtures must be synthetic.

## Markers

- `integration`: requires PostgreSQL or another local service.
- `e2e`: exercises a complete runtime flow.
- `slow`: intentionally excluded from the quickest feedback loop.

The default `make test` runs all tests except `e2e`. `make test-unit`, `make test-integration`, and `make test-e2e` provide focused suites. CI runs architecture and security checks before the slower suites.

## Definition of done for a module slice

A slice is complete only when its domain behavior, use-case orchestration, repository SQL, tenant isolation, HTTP contract, authorization, event compatibility, failure behavior, and observability are tested at the appropriate level.
