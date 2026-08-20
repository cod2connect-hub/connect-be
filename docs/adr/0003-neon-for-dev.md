# ADR 0003: Neon PostgreSQL for development

- Status: Accepted
- Date: 2026-08-20

## Context

The application requires PostgreSQL behavior that SQLite cannot reproduce, especially RLS, transaction-local settings, constraints, and concurrency. The team also benefits from isolated database branches.

## Decision

Use Neon PostgreSQL for normal development and CI branches. Use a pooled runtime URL and a direct migrator URL with separate non-owner runtime and owner migration roles. Redis, Mailpit, and MinIO remain local Docker services.

## Consequences

- Development exercises production-relevant PostgreSQL semantics.
- Network availability and branch lifecycle become development concerns.
- The SQL remains portable to another managed PostgreSQL provider.
- Integration tests may use ephemeral local PostgreSQL when isolation or offline execution is preferable.
