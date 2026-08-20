# System overview

## Product

Connect is a multi-tenant website and business-operations platform. A tenant selects a niche profile, enables reusable capabilities, configures a theme, publishes a site, and operates the business through admin and customer portals.

The product supports the 25 niches listed in [niche-feature-breakdown.md](niche-feature-breakdown.md). Niches are compositions of shared capabilities; they are not separate applications and do not get duplicate business logic.

## Runtime shape

The backend starts as one FastAPI modular monolith with two process types:

- API process: synchronous HTTP request handling under `/api/v1`.
- Worker process: outbox delivery, scheduled jobs, notifications, indexing, and provider callbacks.

PostgreSQL is the source of truth. Redis supports jobs, rate limits, and short-lived coordination. Object storage holds customer files and media. External providers are accessed only through adapters in `app/integrations/`.

## Product boundaries

- Platform contexts manage tenant identity, SaaS billing, themes, and feature access.
- Engines provide reusable business capabilities such as scheduling, commerce, forms, and portals.
- Niche definitions select and configure engines for a market; they contain no domain implementation.
- Contracts provide stable identifiers and versioned events between modules.
- Core contains technical primitives only. It must not become a home for business features.

## Primary flows

1. Platform onboarding creates a tenant, owner identity, default theme, domain, and enabled feature set.
2. Site management composes content, catalog entries, forms, media, SEO, and niche configuration.
3. Public APIs resolve the tenant from the host, enforce publication state, and expose enabled capabilities.
4. Admin APIs authenticate staff, enforce tenant scope, permission, and feature entitlement, then invoke one application use case.
5. Use cases commit state and outbox events in one database transaction.
6. Workers deliver side effects through provider adapters with retries and idempotency.

## Non-negotiable qualities

- Tenant isolation through request scoping and PostgreSQL row-level security.
- No cross-engine database access or imports of another engine's internals.
- Provider-neutral application code.
- Idempotent public writes, webhooks, payments, and jobs.
- Accessible, localized, auditable, and observable behavior.
- Sensitive healthcare, legal, child, financial, and identity data receives explicit retention and authorization rules before implementation.

The detailed rules are in [01-architecture.md](01-architecture.md), the complete product mapping is in [03-capability-map.md](03-capability-map.md), and implementation order is in [backend-implementation-guide.md](backend-implementation-guide.md).
