# ADR 0001: Raw SQL over ORM

- Status: Accepted
- Date: 2026-08-20

## Context

The system depends on PostgreSQL row-level security, JSONB configuration, explicit locking, outbox writes, and query plans for scheduling/search-heavy operations. Hiding those behaviors behind generated ORM queries would weaken reviewability at the most important boundaries.

## Decision

Use parameterized SQL through `asyncpg`. Repository protocols live in the domain layer; SQL, row mapping, and database-specific behavior live only in each module's infrastructure layer. Alembic remains the ordered migration runner, with migrations authored explicitly.

## Consequences

- SQL and transaction behavior are visible and can be tested with real PostgreSQL.
- RLS, constraints, indexes, locking, and query plans receive direct review.
- Mapping and migrations require more deliberate work.
- String-built SQL is prohibited; dynamic filters use allowlisted fragments plus bound values.
