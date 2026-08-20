# Delivery charter

## Goal

Deliver one secure, maintainable multi-tenant backend that lets configured niches compose reusable business capabilities without creating separate applications or duplicated domain logic.

## Guiding principles

1. **Tenant safety before convenience.** Application checks and PostgreSQL RLS jointly enforce isolation.
2. **One owner for every fact.** One module owns each table, invariant, and lifecycle; other modules use public APIs or versioned events.
3. **Vertical outcomes over horizontal scaffolding.** Finish an observable, tested behavior before broadening a module.
4. **Configuration over niche forks.** Niche packages select capabilities, defaults, terminology, and policies; engines implement behavior.
5. **Provider neutrality.** Business logic depends on ports. SDKs and vendor payloads stop at integration adapters.
6. **Explicit failure semantics.** Retries, duplicates, timeouts, partial failures, and invalid transitions are designed behavior.
7. **Contracts evolve compatibly.** APIs and events are versioned; database changes use expand/migrate/contract.
8. **Security and operations are product behavior.** Audit, retention, deletion, recovery, metrics, and runbooks are part of completion.
9. **Evidence over assertion.** A requirement is complete only when an automated test, review artifact, or operational drill proves it.

## Hard constraints

These are non-negotiable even for a small feature, internal endpoint, prototype, or urgent release:

- Keep one root `app/` package, one FastAPI deployable, and one ordered migration tree.
- Use Python 3.12+, FastAPI, PostgreSQL, `asyncpg`, and parameterized raw SQL unless an accepted ADR changes the decision.
- Put SQL only in an owning module's infrastructure/repository layer or reviewed migration/operational script.
- Give every tenant-owned row a non-null `tenant_id`; enable and force RLS; test two-tenant denial.
- Never use the migration/table-owner role as the normal runtime role.
- Resolve tenant context before tenant data access and set it transaction-locally.
- Require authentication, membership, permission, entitlement, and record policy independently where applicable.
- Do not import another module's domain, infrastructure, or private application internals.
- Do not query, join, update, or foreign-key directly to another module's privately owned table merely for convenience. Exchange opaque references and contracts.
- Commit owned state and outbox messages in the same transaction.
- Make retryable writes, public mutations, payments, webhooks, jobs, and event handlers idempotent.
- Keep provider SDKs and vendor models under `app/integrations/`; verify webhook authenticity before dispatch.
- Use RFC 7807 errors and shared pagination/filter/sort conventions.
- Never log secrets or sensitive payloads; classify new sensitive fields before storing them.
- Do not claim regulatory compliance until required legal, vendor, technical, and operational evidence is approved.
- Do not merge a slice with missing migration, authorization, security, failure-path, observability, or documentation work under a future-cleanup promise.

## In scope for project completion

- API and worker runtime composition, configuration, health, telemetry, and graceful operation.
- Identity, tenants, SaaS billing/entitlements, themes, all reusable engines in the accepted capability map, and declarative niche definitions.
- Versioned admin, public, platform, onboarding, portal, and webhook interfaces required by supported journeys.
- Raw-SQL repositories, PostgreSQL schema, constraints, indexes, RLS, migrations, seed data, idempotency, and transactional outbox.
- Provider-neutral ports plus production adapters needed by enabled niches and deterministic local/test substitutes.
- Authorization, auditing, privacy lifecycle, retention/deletion/export, abuse protection, secrets management, and recovery procedures.
- Unit, application, infrastructure, interface, contract, architecture, security, and critical end-to-end tests.
- Deployment configuration, dashboards, alerts, runbooks, backup/restore drills, migration verification, and incident ownership.
- Validated niche manifests, authorization matrices, threat models, end-to-end journeys, and operational acceptance evidence.

## Out of scope unless added by ADR and roadmap change

- Separate per-niche backends, duplicated niche business logic, or microservice extraction.
- Frontend page-builder/editor implementation, native mobile apps, and theme rendering UI.
- Building proprietary replacements for payment, email, SMS, DNS, storage, maps, search, video, signing, POS, shipping, or other external providers.
- Data warehouse/lake, general-purpose BI platform, or arbitrary cross-module SQL reporting.
- Real-time collaboration infrastructure beyond declared communication and notification use cases.
- Unsupported country-specific tax, payroll, clinical-record, legal-practice, or insurance-core systems.
- Production enablement for a niche whose legal, privacy, retention, and vendor requirements are unresolved.
- Premature service extraction, multi-region active-active operation, or unlimited extension/plugin execution.

Out of scope means "not promised," not "forbidden forever." Adding it requires ownership, dependencies, security impact, delivery phase, and acceptance evidence to be recorded through change control.

## Non-negotiable project-completion definition

The project is complete only when all of the following are true:

- Every promised niche maps to a validated feature manifest with no unowned capability.
- Every required component has at least one accepted end-to-end slice; components promised for production have all agreed functional requirements accepted.
- Critical journeys pass from HTTP request through database/outbox/worker/provider substitute and back to observable result.
- No open critical/high security finding exists; medium findings have an owner and approved remediation date.
- Tenant-isolation, permission, entitlement, record-access, webhook, idempotency, concurrency, and sensitive-data tests pass.
- A clean database upgrades to the current schema; the previous supported release upgrades safely; expand/contract compatibility is proven.
- Production adapters used by an enabled niche pass contract tests and failure-mode verification.
- SLOs, dashboards, alerts, on-call ownership, incident procedures, capacity limits, and cost signals are documented and exercised.
- Backup restore, key rotation, data export, tenant deletion, and required retention cleanup are successfully rehearsed.
- API/event documentation, module READMEs, ADRs, data inventory, threat models, and runbooks match deployed behavior.
- Product, engineering, security/privacy, and operations sign off on the release evidence.

Passing unit tests alone, implementing every folder, or demoing a happy path does not constitute completion.

## Change control

An ADR is required before changing module ownership, dependency direction, persistence technology, tenancy/RLS strategy, API versioning, event compatibility, deployment shape, or a hard constraint. Scope changes must update this charter, the capability map, affected phase plan, requirements, and acceptance evidence in the same pull request.
