# Backend architecture

Status: accepted target architecture
Scope: backend repository
Style: FastAPI modular monolith with ports and adapters

## 1. Architectural decisions

- The installable application package is `app/` at repository root. There is no parallel `src/` tree.
- One deployable contains independently owned platform contexts and reusable engines.
- Each module uses `domain`, `application`, `infrastructure`, and `interface` layers.
- PostgreSQL is accessed with parameterized raw SQL through `asyncpg`; repositories contain all SQL.
- Cross-module collaboration uses versioned contracts, events, or a module's declared public application API.
- Every tenant-owned table carries `tenant_id` and is protected by PostgreSQL row-level security.
- External vendors are replaceable adapters under `app/integrations/`.
- A niche is configuration that composes engines. Niche folders never reimplement an engine.

## 2. Repository structure

```text
connect-be/
├── app/
│   ├── main.py
│   ├── api/v1/{admin,public,platform,onboarding}/
│   ├── core/
│   ├── contracts/events/
│   ├── integrations/
│   ├── engines/
│   │   ├── scheduling/       ├── catalog/          ├── forms/
│   │   ├── payments/         ├── crm/              ├── portal/
│   │   ├── documents/        ├── notifications/    ├── reviews/
│   │   ├── search/           ├── loyalty/          ├── calculators/
│   │   ├── media/            ├── content/          ├── commerce/
│   │   ├── memberships/      ├── workflows/        ├── learning/
│   │   ├── analytics/        ├── locations/        └── communications/
│   ├── identity/
│   ├── tenants/
│   ├── billing/
│   ├── themes/
│   ├── niches/
│   └── workers/{handlers}/
├── docs/
├── migrations/{versions}/
├── scripts/{init-db}/
├── seeds/
└── tests/{unit,application,infrastructure,interface,contract,architecture,security,e2e}/
```

`app/engines/` contains customer-facing business capabilities. `identity`, `tenants`, `billing`, and `themes` are platform contexts and therefore remain directly under `app/`. This distinction is ownership, not a shortcut around layering.

## 3. Module shape and dependency rule

Every engine and platform context follows this shape when implementation begins:

```text
module/
├── README.md
├── domain/
├── application/
│   └── use_cases/
├── infrastructure/
│   └── sql/
└── interface/
```

| Layer | Owns | Allowed dependencies | Forbidden dependencies |
|---|---|---|---|
| `domain` | Entities, value objects, invariants, domain services, repository protocols | Standard library and same module domain | FastAPI, asyncpg, provider SDKs, other modules |
| `application` | Commands, queries, use cases, transaction orchestration, ports | Same module domain, shared contracts | HTTP details, SQL, provider SDKs, other module internals |
| `infrastructure` | SQL repositories, row mapping, adapter implementations | Domain protocols, core database tools, integrations | Other module internals |
| `interface` | HTTP schemas, routers, auth/feature dependencies, error mapping | Application public surface, domain errors | SQL and provider SDKs |

`app/core/` is limited to configuration, database transactions, tenant scoping, security primitives, errors, idempotency, events, logging, query conventions, and telemetry. Shared business concepts belong in a context or engine.

## 4. Module ownership

### Platform contexts

| Context | Owns |
|---|---|
| Identity | Accounts, credentials/federated identities, sessions, tenant memberships, staff roles and permission grants |
| Tenants | Tenant lifecycle, onboarding, host/domain resolution, enabled features, locations' tenant-level defaults |
| Billing | The platform's SaaS plans, subscriptions, entitlements, metering, and platform invoices |
| Themes | Theme registry, versions, compatibility, tenant design tokens, and theme configuration |

Platform Billing does not process a tenant's customer purchases or memberships. Those belong to Payments, Commerce, and Memberships.

### Reusable engines

| Engine | Owns |
|---|---|
| Scheduling | Availability, resources, appointments, classes, reservations, waitlists, recurring bookings |
| Catalog | Generic listings, products, services, menus, tours, properties, packages, profiles, categories, variants |
| Forms | Form definitions, conditional fields, submissions, secure intake, questionnaires, RSVP |
| Payments | Customer payment intents, deposits, refunds, payouts, receipts, donations, provider webhooks |
| CRM | Leads, contacts, notes, tags, assignment, sales pipeline, marketing audiences |
| Portal | Customer-facing access spaces and visibility policies over records owned by other engines |
| Documents | Files with business meaning, document sharing, templates, signature lifecycle, certificates |
| Notifications | Templates, preferences, channel routing, delivery attempts, reminders, push/email/SMS |
| Reviews | Reviews, testimonials, ratings, moderation, before/after consent references |
| Search | Search documents, filters, indexing state, saved searches, comparisons, favorites |
| Loyalty | Points, tiers, rewards, vouchers, referral and redemption rules |
| Calculators | Versioned rule sets for quotes, fees, prices, finance, eligibility, and assessments |
| Media | Uploads, transformations, galleries, proofing, private delivery, retention metadata |
| Content | Pages, reusable sections, navigation, blog, SEO, schema markup, localization, legal banners |
| Commerce | Cart, customer order, inventory, fulfillment, delivery/pickup, returns, gift cards, POS sync |
| Memberships | Customer plans, enrollments, recurring service agreements, attendance, progress, pauses/cancellations |
| Workflows | Cases, tickets, claims, maintenance requests, projects, checklists, timelines, assignments and status |
| Learning | Courses, lessons, assessments, attempts, grades, progress and certificate eligibility |
| Analytics | Tenant metrics, dashboard definitions, event facts, reports and external analytics connections |
| Locations | Branches, addresses, service/delivery zones, radius/postcode rules, map and neighborhood data |
| Communications | Two-way conversations, live chat, WhatsApp threads, participants, consent and message history |

The rationale and complete niche mapping are in [03-capability-map.md](03-capability-map.md).

## 5. API boundaries

- `/api/v1/public/{engine}` serves published tenant sites and customer actions.
- `/api/v1/admin/{engine}` serves tenant staff operations.
- `/api/v1/platform` serves SaaS operator operations.
- `/api/v1/onboarding` serves tenant creation and setup.
- Webhook endpoints live with the owning interface and authenticate the provider before dispatch.

Routers validate transport data and invoke one application use case. They do not contain SQL or business rules. API errors use RFC 7807 problem details. List endpoints share cursor pagination, filtering, and sort conventions. Mutating public endpoints and provider callbacks require idempotency keys or provider event IDs.

## 6. Tenant isolation and authorization

1. Resolve tenant from a verified host, platform route parameter, or signed identity claim.
2. Open one database transaction per request or job.
3. Set transaction-local tenant and actor context.
4. Apply application authorization and feature-entitlement checks.
5. Let RLS provide the final database boundary.

The migration owner bypasses RLS; the runtime role must not own tables and must not have `BYPASSRLS`. Platform-wide operations use an explicit privileged path with separate audit requirements. Detailed rules are in [02-rbac.md](02-rbac.md).

## 7. Data ownership and transactions

- Each table has one owning module and is queried only by that module's infrastructure layer.
- A use case may atomically update its own tables and append outbox events.
- Cross-module projections are built from events; modules do not join directly across owned tables.
- References to another module use opaque identifiers from `app/contracts/refs.py`.
- Schema migrations are ordered globally but named by owning context/engine.
- Destructive schema changes use expand/migrate/contract deployment steps.

## 8. Events and background work

Versioned event contracts live in `app/contracts/events/`. The transaction writes domain state and an outbox row together. Workers claim outbox messages, invoke registered handlers, and record retries/dead letters. Handlers are idempotent and call an application use case; they do not update another module's tables directly.

Typical asynchronous work includes notifications, search indexing, analytics facts, media processing, recurring billing/booking actions, provider synchronization, exports, and retention cleanup.

## 9. Integrations

Application layers depend on provider-neutral ports. Provider SDK usage is confined to `app/integrations/`. Adapter categories include payments, email, SMS, push, storage, DNS, search, calendar, maps, video, e-signature, chat, analytics, social feeds, POS, shipping, property data, and supplier feeds.

Every adapter defines timeouts, retry classification, idempotency behavior, webhook verification, observability fields, and a local/test substitute before production implementation.

## 10. Niche composition

`app/niches/` will contain validated declarative definitions: enabled engines, required dependencies, default forms/content, theme compatibility, and terminology overrides. It may not contain routers, repositories, domain entities, or provider clients.

Feature dependencies are explicit. For example, online ordering requires Catalog + Commerce + Payments; appointment reminders require Scheduling + Notifications; a patient portal composes Portal + Workflows + Documents + Forms with stricter policy.

## 11. Testing and enforcement

Tests are organized by architectural concern, not by a mirror of every source file. CI must run formatting/lint checks, module-boundary checks, route authorization checks, SQL-safety checks, RLS coverage, unit/application tests, integration tests, contract tests, and migration verification. See [04-testing-strategy.md](04-testing-strategy.md).

## 12. Operational baseline

- Structured logs include request, tenant, actor, module, use case, and correlation identifiers without sensitive payloads.
- Metrics cover latency, error rate, queue lag, outbox retries, provider failures, pool usage, and tenant-facing business events.
- Traces cross API, database, worker, and provider boundaries.
- Health endpoints distinguish liveness from dependency readiness.
- Backups, restore drills, key rotation, data export, retention, and deletion workflows are required before regulated niches launch.

## 13. Decision process

Changes to module ownership, data boundaries, cross-module contracts, tenancy, security, persistence, or deployment require an ADR under `docs/adr/`. The architecture document is updated in the same change so it remains the source of truth.
