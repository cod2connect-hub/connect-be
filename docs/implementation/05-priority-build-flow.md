# Priority build flow

Status: authoritative implementation sequence  
Purpose: prevent dependency inversion, half-built modules, and feature-first development on an unsafe foundation

This flow adopts the useful planning pattern from the external `02-mvp-scope.md` reference: one complete business loop, stable component IDs, explicit ownership and dependencies, dependency waves, and measurable wave exits. The product scope and architecture here remain Connect's own.

## 1. First complete business loop

The first implementation target is not "all engines partially working." It is one complete, auditable revenue loop:

> A tenant owner onboards → configures and publishes an offering with a lead form → a visitor submits an enquiry → staff qualify the lead and produce a versioned quote → the customer books an available slot → a deposit/payment is confirmed → notification and analytics reflect the result.

If any link is absent, the tenant must use another system to finish the transaction and the backend has not yet proven product value. Supporting components are included only when they make this loop secure, operable, or complete.

The first reference composition is a generic appointment-based service business. Home services and salons can validate it with terminology/configuration changes rather than separate code. Real-estate inquiry is a second composition after the shared loop is stable.

## 2. Priority rules

When two work items compete, choose in this order:

1. Tenant isolation, identity/access, data integrity, audit, idempotency, and recovery blockers.
2. A missing dependency on the first complete revenue loop.
3. The next unfinished vertical slice in the current wave.
4. Failure handling and operational evidence for an already-built slice.
5. Additional behavior in a current-loop component.
6. A component for the next validated niche.
7. Convenience, optimization without evidence, or breadth across future engines.

Do not prioritize by which package is easiest to scaffold. Starting a later module does not count as progress if a prerequisite is incomplete.

## 3. Component register

The IDs below are stable planning identifiers. They do not rename repository packages.

| ID | Component | Owns | Provides | Hard prerequisites |
|---|---|---|---|---|
| C00 | Core/runtime guardrails | Config, transaction/tenant context, errors, idempotency/outbox plumbing, telemetry primitives | Safe API/worker/database foundation | None; build first |
| C01 | Tenants | Tenant lifecycle, onboarding state, domains/host resolution, feature configuration | Trusted tenant context and tenant references | C00 |
| C02 | Identity, access, audit | Accounts, sessions, memberships, roles/grants, identity audit | Actor context, authentication, membership and permission decisions | C00; C01 tenant identity contract |
| C03 | Billing and entitlements | SaaS plans/subscriptions/entitlements/metering | Feature access decision | C00, C01; C02 operator access |
| C04 | Niches and themes | Declarative niche manifests; theme versions/tokens/configuration | Validated capability composition and visual configuration | C01, C03; C02 admin access |
| C05 | Workers and contracts | Versioned events, outbox dispatch, schedules, retries/dead letters | Reliable asynchronous execution | C00; C01/C02 context contracts |
| C06 | Media/storage | Upload/object/transform/privacy lifecycle | Authorized media references and delivery | C00–C02, storage port, C05 for processing |
| C07 | Content/site publishing | Pages, sections, navigation, localization, SEO, publication | Published tenant site content | C01, C04, C06 |
| C08 | Locations | Branches, addresses and service zones | Location/zone references and eligibility | C01–C02; maps port only when needed |
| C09 | Forms | Definitions/versions/submissions/consent metadata | Validated intake submission event | C01–C02, C05; C07 for public embedding |
| C10 | CRM | Leads, contacts, assignment, pipeline, notes/tags | Lead/contact lifecycle | C01–C02, C05; consumes C09 event |
| C11 | Notifications | Templates/preferences/routing/delivery attempts | Provider-neutral outbound delivery | C01–C02, C05; email adapter first |
| C12 | Catalog | Offerings/listings/categories/variants and publication | Published sellable/bookable references | C01–C02, C06; C08 when location-bound |
| C13 | Scheduling | Availability/resources/bookings/classes/waitlists/recurrence | Conflict-safe booking lifecycle | C01–C02, C05, C12; C08 when location-bound |
| C14 | Calculators | Versioned quote/fee/eligibility rules and results | Explainable, reproducible quote result | C01–C02, C12; C08/C09 inputs as required |
| C15 | Payments | Customer intents/deposits/refunds/receipts/webhooks | Verified monetary outcome events | C01–C02, C05; C13/C14 opaque context; payment port |
| C16 | Analytics | Tenant facts, metric/report definitions | Operational/revenue visibility | C05 plus accepted events from source modules |
| C17 | Reviews | Reviews/ratings/moderation/consent refs | Publishable reputation records | C01–C02; C12 subject and completed-journey refs |
| C18 | Search | Index projection, filters, saved searches/favorites | Public/admin search | C05; published C07/C12 events |
| C19 | Commerce | Cart/order/inventory/fulfillment/returns/discounts | Order lifecycle | C12, C15, C05; C08 for fulfillment |
| C20 | Loyalty | Points/tiers/rewards/vouchers/referrals | Auditable earn/redeem decisions | C05; C19 and C15 outcome events |
| C21 | Memberships | Customer plans/enrollment/attendance/renewal | Recurring customer-plan lifecycle | C12, C13, C15, C05 |
| C22 | Portal | Customer access spaces and visibility policy | Scoped access to referenced records | C02 plus owning-module record-policy contracts |
| C23 | Documents | Business documents/templates/sharing/signature/certificates | Versioned, authorized document lifecycle | C06, C05; e-signature port when needed |
| C24 | Workflows | Cases/tickets/projects/checklists/assignment/timeline | Typed operational workflow lifecycle | C02, C05; C09/C10 refs as required |
| C25 | Communications | Conversations/participants/consent/message history | Two-way messaging and handover | C02, C05, C10; chat adapter |
| C26 | Learning | Courses/lessons/assessments/grades/progress/certification | Learning lifecycle | C06, C12, C21/C22, C23 as selected |

"Hard prerequisite" means the dependency's required contract and safety behavior must be accepted. It does not require every future feature in that dependency.

## 4. Dependency waves and strict build order

### Wave 0 — Prove the safety rails

**Order:** C00 → minimum C05

Build configuration, request/job context, transaction boundaries, runtime and migration roles, forced-RLS conventions, RFC 7807 errors, idempotency, outbox storage/claiming, logging/tracing, health, and architecture/security checks.

**Stop gate:** do not create business tables or routes until a reference tenant-owned slice proves isolation, transactional outbox, duplicate delivery safety, and CI enforcement.

### Wave 1 — Establish tenant and actor authority

**Order:** C01 → C02 → C03 → C04; mature C05 alongside their events

The order matters:

1. C01 defines the tenant identity/lifecycle and trusted resolution contract.
2. C02 attaches actors and permissions to that tenant and supplies audit behavior.
3. C03 evaluates paid product entitlement independently from permission.
4. C04 validates which capabilities/configuration a tenant may use.

Onboarding orchestration is implemented only after all four components expose stable minimum contracts.

**Stop gate:** no public business engine is exposed until wrong-host, wrong-tenant, missing-membership, missing-permission, missing-entitlement, suspended-tenant, revoked-session, and retried-onboarding tests pass.

### Wave 2 — Publish and capture demand

**Order:** C06 → C07; C08 can proceed after C01/C02; then C09 → C10 → C11 → C16 foundation

1. C06 supplies authorized assets rather than embedding storage behavior elsewhere.
2. C07 creates the publish/preview boundary and public tenant site.
3. C08 supplies reusable branch/zone facts before offerings and schedules depend on them.
4. C09 captures a versioned, consent-aware submission.
5. C10 consumes that event into an assigned lead without direct table access.
6. C11 delivers staff/customer acknowledgements asynchronously.
7. C16 first records consent-aware site, submission, lead, and delivery facts; it does not yet provide revenue reporting.

Use a local/test email adapter first. DNS, SMS, maps, and analytics providers are added only when the selected deployment needs them.

**Wave exit:** owner publishes a localized page/form; a visitor submits; one lead is created/assigned despite retries; acknowledgement delivery and audit/metrics are visible.

### Wave 3 — Close the first revenue loop

**Order:** C12 → C13 → C14 → C15 → extend C16

1. C12 produces the stable offering/variant reference.
2. C13 proves availability and conflict-safe booking before money is attached.
3. C14 versions quote calculation and stores explainable results used by booking/payment.
4. C15 attaches an idempotent, provider-confirmed deposit/payment to opaque booking/quote context.
5. C16 extends its accepted-event projections into minimum funnel, booking, and revenue metrics.

The first implementation can create a simple manually adjusted quote in CRM before the full C14 rule engine, but the accepted monetary amount must be server-validated and immutable once attached to payment. C14 is required before configurable calculators are advertised.

**Stop gate:** do not begin Commerce or Memberships until concurrency tests prevent double booking, payment webhook replay/out-of-order tests prevent duplicate monetary effects, reconciliation exists, and the complete first loop passes E2E.

### Wave 4 — Complete discovery and trust

**Order:** C17 → C18

C17 uses completed-journey eligibility and moderation. C18 indexes published Content/Catalog through events. These enrich the proven loop but do not block its first internal use.

**Wave exit:** eligible customers can submit moderated reviews; public search returns only current published/entitled records and removes private/archived records within the agreed lag.

### Wave 5 — Add transaction operations

**Order:** C19 → C20; C21 can start after C12/C13/C15; then C22 → C23 → C24 → C25

- Build Commerce before Loyalty because earn/redeem correctness depends on final order/payment outcomes.
- Build Memberships only after scheduling and payment recurrence/failure contracts are stable.
- Build Portal after the first owning-module record policy exists; Portal never becomes a data owner shortcut.
- Build Documents before workflows that require document/signature state.
- Build Workflows before attaching two-way conversations to cases/tickets, while C25 may first expose a narrow standalone conversation slice.

**Wave exit:** order and recurring-service journeys survive retries, refunds/cancellations, inventory/redemption races, portal object-reference attacks, document access tests, and provider outages.

### Wave 6 — Advanced capabilities and niches

**Order:** C26 → one advanced niche at a time

Learning is built only after its selected catalog, enrollment, portal, media, and document contracts are stable. Then enable education, daycare, clinic, nonprofit, legal, insurance, property-management, and IT-support compositions individually—not as one bulk launch.

**Stop gate per niche:** capability manifest, authorization matrix, threat model, data inventory/retention, vendor review, E2E journey, capacity assumptions, runbook, rollout/disable plan, and required approvals must all pass.

## 5. Inside every component: mandatory implementation order

Do not implement all database models first and defer behavior/security. Complete one vertical slice in this order:

1. **Scope:** write outcome, owner, actors, in/out, dependencies, states, sensitive data, and acceptance IDs.
2. **Contract:** define command/query DTO, opaque references, domain/application public surface, events, errors, and compatibility.
3. **Authorization:** define tenant, membership, permission, entitlement, ownership/relationship, and privileged-path rules.
4. **Domain:** implement entities/value objects, invariants, transitions, concurrency expectation, idempotency semantics, and pure tests.
5. **Application:** implement orchestration and ports with fakes; test success, denial, conflict, retry, and dependency failure.
6. **Persistence:** add expand-safe migration, constraints/indexes, forced RLS, repository SQL/mapping, and real-PostgreSQL two-tenant/concurrency tests.
7. **Interface:** add schemas/router or worker handler, dependency declarations, RFC 7807 mapping, pagination, limits, and interface tests.
8. **Events/integrations:** write outbox atomically; add idempotent consumer or provider adapter with timeout/retry/webhook/reconciliation tests.
9. **Operations/security:** add redacted logs, metrics/traces, alerts/runbook, retention/export/deletion behavior, and threat-model updates.
10. **Acceptance:** pass `make check`, relevant E2E journey, migration verification, documentation review, and slice sign-off before the next slice.

Steps 3 and 4 may be designed together, but neither can be postponed until after routes and tables exist.

## 6. What may proceed in parallel

Parallel work is allowed only where it cannot create competing contracts:

- After C00 contracts stabilize: C01 tenant domain and C02 account/session domain, coordinated on the tenant reference.
- After Wave 1: C06 Media and C08 Locations; C07 begins when C06's reference/delivery contract is accepted.
- Within Wave 2: C10 domain/application may use a frozen fake C09 event while C09 persistence/interface is completed.
- Within Wave 3: C14 pure rule evaluation may proceed alongside C13 after C12 references and money conventions are frozen.
- Adapter work may proceed against an accepted port and contract test; it cannot define domain behavior.

The merge/integration order still follows the waves. Parallel branches do not authorize temporary cross-module table reads or duplicate models.

## 7. Decisions to freeze early

These are expensive to repair and must be accepted before the first dependent slice:

- tenant identifier, trusted host resolution, RLS context, and privileged operator path;
- actor/session model, permission naming, entitlement keys, and audit event shape;
- transaction/outbox/idempotency semantics and event envelope/versioning;
- identifier format, UTC/time-zone rules, locale and money/decimal representation;
- API error, cursor pagination, filtering/sorting, and public contract compatibility;
- object storage reference/access model and sensitive-data classification levels;
- booking capacity/conflict model and payment state/reconciliation model;
- retention, deletion, export, and audit immutability expectations.

Changing one requires impact analysis and, where architectural, an ADR before implementation continues.

## 8. Flow acceptance checklist

Before moving to the next wave, confirm:

- The wave's E2E outcome works without direct database repair or an external spreadsheet.
- Every component owns its data and communicates only through accepted surfaces/events.
- Negative authorization, tenant isolation, retry, concurrency, invalid-state, and provider-failure paths pass.
- The runtime can observe, retry/reconcile, support, disable, and recover the delivered behavior.
- Migrations work on a blank database and from the previous supported release.
- No blocking security finding or undocumented deferred requirement remains.
- README, architecture, component register, requirements, dashboards, and runbooks match the implementation.

If a gate fails, fix the current wave. Do not hide the gap with a feature flag and begin a dependent module.
