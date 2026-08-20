# Components, ownership, and boundaries

## Universal module contract

Every platform context and engine provides a narrow public application surface and versioned events. Its internal layers remain private.

| Layer | Owns/provides | May depend on | Must not depend on |
|---|---|---|---|
| Domain | Entities, value objects, policies, transitions, domain errors/events | Standard library; same module domain | FastAPI, SQL, SDKs, other modules |
| Application | Commands/queries, use cases, DTOs, ports, transaction orchestration | Own domain; shared refs/contracts | HTTP types, raw SQL, SDKs, other internals |
| Infrastructure | Repositories, mappings, port implementations | Own protocols; core DB primitives; integration seams | Other modules' tables/internals |
| Interface | Routers, schemas, auth/feature dependencies, error mapping | Public application surface | SQL, repositories, SDKs, business-rule implementation |

`app/core/` provides technical primitives only: configuration, transactions, tenant context, security primitives, errors, idempotency, outbox/event plumbing, logging, query conventions, and telemetry. `app/contracts/` provides opaque references and versioned cross-module schemas. Neither owns business workflows.

## Platform and composition components

| Component | Owns | Provides | Depends on |
|---|---|---|---|
| Core/runtime | Configuration, DB/session primitives, request context, problem details, idempotency/outbox plumbing, telemetry | Stable technical services to all modules | PostgreSQL, Redis where required; no business module |
| Identity | Accounts, credentials/federation, sessions, memberships, roles, grants, identity audit | Actor/session validation, membership and permission decisions, identity references/events | Core security; Tenants by opaque reference/contract |
| Tenants | Tenant lifecycle, onboarding state, domains/host resolution, enabled-feature configuration, tenant defaults | Resolved tenant context, lifecycle and feature configuration events | Identity refs; Billing entitlement result; DNS port |
| Billing | Connect SaaS plans, tenant subscriptions, entitlements, metering, platform invoices | Feature-entitlement decisions and subscription events | Tenants refs; external billing/payment adapter if selected |
| Themes | Theme registry/version compatibility, tenant tokens/configuration | Resolved theme configuration and compatibility validation | Tenants refs; Media refs where required |
| Niches | Declarative manifests, engine dependencies, defaults, terminology, policy flags | Validated composition used by onboarding/runtime | Public capability metadata only; no domain implementation |
| API composition | Route registration and dependency wiring | `/api/v1` admin/public/platform/onboarding surfaces | Public module interfaces only |
| Workers | Outbox claim/delivery, scheduled dispatch, retry/dead-letter coordination | At-least-once execution with traceable results | Core event plumbing; public handler/use-case entry points |

Billing never owns customer purchases. Tenant-customer payments belong to Payments; orders to Commerce; customer plans to Memberships.

## Reusable engine ownership and dependency contract

Dependencies below mean public API, opaque reference, or event contract—not internal imports or table access.

| Engine | Owns and provides | Common upstream inputs | Common downstream consumers/events |
|---|---|---|---|
| Content | Pages, sections, navigation, blog, SEO, localization, publishing/legal banners | Themes, Media refs, Tenants | Search indexing, Analytics facts |
| Media | Upload lifecycle, object metadata, transforms, galleries, proofing, privacy/retention metadata | Storage adapter, Tenants | Content, Catalog, Reviews, Portal, Documents via refs |
| Forms | Definitions, conditional fields, submissions, intake/questionnaires/RSVP | Content embedding, tenant policy | CRM lead event, Workflows intake, Notifications |
| CRM | Leads, contacts, notes, tags, assignments, pipeline, audiences | Forms/events, Identity assignee refs | Communications, Workflows, Analytics |
| Locations | Branches, addresses, service/delivery zones, radius/postcode rules | Maps/geocoding adapter | Catalog, Scheduling, Commerce, Search |
| Notifications | Templates, preferences, routing, attempts, reminders | Domain events and recipient refs | Email/SMS/push adapters, Analytics delivery facts |
| Analytics | Tenant event facts, metrics, dashboard/report definitions, external connections | Versioned events from all modules | Admin reports, analytics adapter |
| Catalog | Listings, products, services, menus, tours, properties, packages, profiles, categories, variants | Media/Location refs | Scheduling, Calculators, Commerce, Search, Reviews |
| Scheduling | Availability, resources, appointments, classes, reservations, waitlists, recurrence | Catalog offering refs, Location/Identity refs | Payments, Notifications, CRM, Analytics |
| Calculators | Versioned quote/fee/price/finance/eligibility/assessment rules and results | Catalog/location/form inputs | Scheduling, Payments, CRM, Workflows |
| Payments | Customer intents, deposits, refunds, payouts, receipts, donations, webhooks | Order/booking/plan opaque context refs | Owning-context payment-status events, Analytics |
| Reviews | Reviews, testimonials, ratings, moderation, consent refs | Customer and subject refs; Media refs | Content, Catalog, Search, Analytics |
| Search | Search documents, indexing state, filters, saved searches, comparisons/favorites | Published/index events | Public/admin query results; Analytics |
| Commerce | Cart, orders, inventory, fulfillment, delivery/pickup, returns, gift cards, discounts/POS sync | Catalog, Location and customer refs | Payments, Notifications, Loyalty, Analytics |
| Loyalty | Points, tiers, rewards, vouchers, referrals, redemption | Commerce/Payments/Membership events | Commerce redemption decisions, Notifications |
| Memberships | Customer plans, enrollments, recurring service agreements, attendance/progress, pause/cancel | Catalog, customer, schedule refs | Payments, Portal, Notifications, Learning |
| Portal | Access spaces and visibility policies over referenced records | Identity customer access; record refs | Customer navigation/access decisions only |
| Documents | Business documents, sharing, templates, signature lifecycle, certificates | Media object refs, e-signature adapter | Portal, Workflows, Learning via refs/events |
| Workflows | Cases, tickets, claims, maintenance requests, projects, checklists, assignments/status/timeline | Forms/CRM refs, Identity assignees | Portal, Documents, Communications, Analytics |
| Communications | Conversations, participants, consent, messages/history | Identity/CRM refs, chat adapter | Notifications escalation, Workflows, Analytics |
| Learning | Courses, lessons, assessments, attempts, grades, progress/certificate eligibility | Catalog/member/student refs, Media | Documents certificates, Portal, Notifications |

## Integration boundary

Each adapter category under `app/integrations/` must expose a provider-neutral port, normalized errors, timeout/retry classification, idempotency rules, webhook verification where relevant, redacted observability fields, and a local/test fake. Current seams cover payments, email, SMS, push, storage, DNS, search, calendar, maps, video, e-signature, chat, analytics, social, POS, shipping, property data, and suppliers.

An adapter does not decide domain state. It reports a normalized result to the owning use case, which decides the transition.

## Boundary rules for cross-component flows

1. The initiating module records its state and outbox event atomically.
2. The event carries stable identifiers and necessary facts, never another module's entity object.
3. A consuming handler deduplicates by event ID/version and calls its own module's use case.
4. Each module records its own failure/retry state; distributed transactions are not introduced.
5. Queries needing cross-module presentation use API composition or event-built projections, never direct joins across private tables.
6. Synchronous calls are reserved for decisions required before the initiating transaction can complete; cyclic synchronous dependencies are forbidden.

## Boundary review checklist

- Is there exactly one owner for every new fact and invariant?
- Can consumers work through an opaque ref, public query/command, or versioned event?
- Does the design avoid a synchronous dependency cycle?
- Are transaction, timeout, retry, duplicate, ordering, and stale-data behavior explicit?
- Is sensitive data minimized in contracts and logs?
- Does an existing engine own the behavior regardless of niche terminology?
- Would changing a provider leave domain/application code unchanged?

Any "no" blocks implementation until the boundary is corrected or an ADR is accepted.
