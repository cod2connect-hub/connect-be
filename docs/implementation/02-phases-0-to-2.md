# Phases 0–2: guardrails and foundations

## Phase 0 — Repository guardrails

### Objective

Make the safe implementation path the easiest path and cause violations to fail before feature development scales.

### Build order

1. Align package paths, settings, Make targets, pytest markers, Ruff, typing policy, and CI.
2. Complete configuration loading, RFC 7807 errors, correlation IDs, structured logging, health endpoints, and composition-root conventions.
3. Establish transaction handling, runtime/migration roles, tenant/actor transaction-local context, and clean pool behavior.
4. Establish migration conventions, RLS helpers, idempotency store, transactional outbox, worker claim/retry/dead-letter primitives.
5. Turn invariant scripts into enforced architecture, route, SQL, migration, and RLS checks.
6. Add test factories/fakes and a minimal API-to-database-to-worker proving slice.
7. Wire CI in fast-fail order: format/lint -> architecture/security invariants -> unit/application -> integration/contract -> migration/e2e.

### Required behavior

- App and worker start with validated configuration and fail safely on invalid configuration.
- Liveness does not depend on external services; readiness reflects required dependencies.
- Transactions always clear tenant/actor context on completion.
- Duplicate outbox delivery is safe, failures retry with bounded backoff, and terminal failures are inspectable.
- Migration and runtime privileges are demonstrably separate.
- A sample tenant-owned row cannot be accessed by another tenant.

### Exit evidence

- `make check` is deterministic on a clean clone.
- Blank-database migration and downgrade/upgrade policy checks pass.
- Architecture tests reject forbidden imports/SQL locations and unprotected routes/tables.
- Security tests prove runtime role limitations and two-tenant denial.
- A reference slice proves request -> transaction -> outbox -> worker -> observable result.

## Phase 1 — Platform foundation

### Objective

Allow a tenant owner to create and securely enter an isolated, entitled tenant workspace.

### Component build order

1. Identity core: account, credential/federation seam, sessions, token/session revocation.
2. Tenants core: tenant lifecycle, verified host/domain resolution, onboarding state.
3. Identity tenancy: memberships, invitations, roles, permissions, record-independent authorization.
4. Billing: plans, subscriptions, entitlements, feature dependency evaluation.
5. Themes: registry/version, tenant design tokens, compatibility and defaults.
6. Onboarding orchestration: tenant, owner membership, plan/features, default theme/domain, audit/outbox events.
7. Platform/admin interfaces and privileged operator path with separate audit.

### Functional requirements

- Create, verify, suspend, reactivate, and safely delete/decommission accounts and tenants according to policy.
- Authenticate, refresh/rotate, revoke, expire, and audit sessions without exposing credentials or tokens.
- Invite staff, accept/expire/revoke invitations, assign tenant-scoped roles, and evaluate stable permissions.
- Resolve a tenant only from a trusted host, signed claim, or explicit privileged route context; reject ambiguity.
- Create onboarding exactly once despite retries and recover or compensate incomplete steps.
- Evaluate plan entitlement separately from tenant feature configuration and feature dependencies.
- Configure a compatible versioned theme without embedding frontend rendering logic.
- Audit sensitive identity, membership, role, subscription, feature, domain, and operator actions.

### Security requirements

- Password/federation/session controls follow the reviewed authentication threat model.
- Enumeration-resistant authentication/recovery responses and abuse throttles are enforced.
- Session fixation, replay, cross-tenant membership confusion, host-header abuse, and privilege escalation are tested.
- Platform operator actions use distinct permissions/path/role and immutable audit evidence.
- Default roles grant least privilege; permission identifiers and feature keys are stable and append-only through reviewed migrations.

### Exit evidence

- E2E: onboard owner -> authenticate -> resolve tenant -> configure theme -> call entitled admin route.
- Negative E2E: wrong host, wrong tenant membership, missing permission, missing entitlement, suspended tenant, revoked session.
- Concurrent/retried onboarding creates one coherent tenant, owner membership, subscription, feature set, and theme.
- Audit entries and outbox events are complete, redacted, and traceable.

## Phase 2 — Site foundation

### Objective

Allow a tenant to publish a localized basic site, receive a submission, create/manage a lead, and observe the journey.

### Component build order

1. Media: direct upload authorization, validation, object lifecycle, private/public delivery, transform seam.
2. Content: drafts/versions, sections/navigation, localization, SEO, preview and atomic publish.
3. Locations: branches, addresses and service zones, then maps/geocoding adapter.
4. Forms: versioned definitions, validation/conditional fields, submission and consent/retention metadata.
5. CRM: contact/lead deduplication policy, notes/tags/assignment/pipeline.
6. Notifications: templates/preferences, email first, delivery attempts and retry/suppression.
7. Analytics: consent-aware event facts and minimum tenant dashboard metrics.
8. Search/DNS/storage/email/SMS/map/analytics adapters only to the production depth required by the release.

### Functional requirements

- Draft and publish content atomically; public routes return only published, host-matched, entitled content.
- Support locale fallback, canonical/SEO metadata, navigation integrity, preview authorization, and cache invalidation semantics.
- Validate media type/size/ownership before upload completion; scan/quarantine as required; enforce signed private delivery.
- Model locations and zones independently of a map vendor; handle invalid/ambiguous geocoding.
- Freeze the form version used for each submission and validate server-side regardless of client behavior.
- Record consent and source, then emit a minimal submission event that CRM consumes idempotently.
- Create/update leads under an explicit deduplication rule; preserve attribution and audit assignment/status changes.
- Render notifications from versioned templates; respect preference, consent, suppression, retry, and provider status.
- Record privacy-aware analytics without making third-party analytics the system of record.

### Exit evidence

- E2E: upload media -> author localized page/form -> publish -> public visitor submits -> CRM receives lead -> notification is attempted -> metric appears.
- Unpublished/cross-host/private content and media cannot be retrieved.
- Duplicate submissions/events do not create unintended duplicate leads or notifications.
- Provider timeout, rejection, webhook replay, and unavailable-map/storage/email behavior are covered by contract and application tests.
- Accessibility-relevant API data, locale behavior, consent, retention, deletion, and observability decisions are documented.
