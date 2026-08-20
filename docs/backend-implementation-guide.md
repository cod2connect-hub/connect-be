# Backend implementation guide

This is a sequencing and definition-of-done guide. It intentionally contains no starter implementation; [01-architecture.md](01-architecture.md) remains the design authority.

For the executable scope, component dependencies, detailed work packages, security gates, and project-completion definition, use the [phase-wise implementation playbook](implementation/README.md). This file remains the short roadmap.

Use the playbook's [priority build flow](implementation/05-priority-build-flow.md) as the authoritative module sequence. It prevents later capabilities from being built on unfinished tenancy, access, data, event, and revenue foundations.

## Phase 0: repository guardrails

- Confirm one root `app/` package and one migration tree.
- Make CI, Makefile, pytest, Ruff, and import-boundary checks agree on paths.
- Establish runtime and migration database roles.
- Turn placeholder invariant scripts into failing checks before feature implementation.
- Add architecture tests for prohibited cross-engine imports.

Exit: a blank module can be added without inventing conventions, and CI detects boundary/RLS/route violations.

## Phase 1: platform foundation

Implement Core technical primitives, Identity, Tenants, Billing, and Themes. Complete host-to-tenant resolution, authentication/session lifecycle, membership/RBAC, feature entitlements, onboarding, RLS context, RFC 7807 errors, idempotency, audit events, and outbox storage.

Exit: a tenant owner can onboard, authenticate, configure a theme, and access only entitled tenant data.

## Phase 2: site foundation

Implement Content, Media, Forms, CRM, Locations, Notifications, and Analytics. Add DNS/storage/email/SMS/map/analytics adapter contracts and local fakes.

Exit: a tenant can publish a localized basic site, receive a form lead, manage media, and observe basic metrics.

## Phase 3: first revenue capabilities

Implement Catalog, Scheduling, Calculators, Payments, Reviews, and Search in that order. Scheduling is the reference rich-domain engine. Payment and booking writes require idempotency from the first endpoint.

Exit: home-service, salon, and real-estate MVP compositions can list offerings, quote, book, collect money, and manage leads.

## Phase 4: transaction operations

Implement Commerce, Loyalty, Memberships, Portal, Documents, Workflows, and Communications. Add provider adapters only as demanded by an enabled vertical.

Exit: restaurant and small-commerce flows support order lifecycle; service businesses support customer plans and portals; staff can operate cases/tickets/projects.

## Phase 5: learning and advanced niches

Implement Learning and the advanced feature combinations for education, daycare, clinics, nonprofits, legal, insurance, property management, and IT support. Complete niche-specific threat models and retention rules before enabling sensitive production data.

Exit: each supported niche has a validated feature dependency manifest, authorization matrix, end-to-end journey, and operational runbook.

## Per-module implementation order

1. README ownership and terminology.
2. Domain entities, value objects, invariants, and errors.
3. Application input/output DTOs, ports, commands, and queries.
4. Unit and application tests.
5. Migration, table ownership, indexes, constraints, and RLS.
6. SQL repository and mapping tests against PostgreSQL.
7. HTTP schemas, permission/entitlement dependencies, and interface tests.
8. Versioned events, outbox handlers, retries, and contract tests.
9. Logs, metrics, tracing, dashboards, and runbook updates.

## Slice acceptance checklist

- Ownership is unambiguous and no cross-module table access exists.
- Tenant, actor, permission, entitlement, and record-level policy are tested.
- Concurrency and invalid state transitions have database-backed protection.
- Writes and handlers are idempotent where retries are possible.
- Events are versioned and contain references rather than another module's entity model.
- Provider failure, timeout, retry, and webhook behavior are specified.
- API errors and pagination follow repository conventions.
- Migrations upgrade cleanly and preserve rollback/expand-contract expectations.
- Sensitive fields have classification, retention, export, deletion, and logging decisions.
- README, capability map, ADRs, and tests match the implementation.
