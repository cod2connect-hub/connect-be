# Quality, security, and completion gates

## Functional requirements that apply to every slice

- Validate inputs at the interface and invariants in the domain; never rely on the client for authority.
- Resolve and enforce actor, tenant, membership, permission, entitlement, and record relationship independently.
- Define allowed state transitions and reject stale, invalid, duplicate, and conflicting operations consistently.
- Persist owned state with constraints that protect critical invariants under concurrency.
- Return stable RFC 7807 problem types; do not expose internals, secrets, SQL, or provider payloads.
- Define idempotency scope, key, request fingerprint, stored result, expiry, and conflict behavior for retryable writes.
- Emit versioned events atomically with state; consumers handle duplicates, retries, ordering assumptions, and poison messages.
- Define pagination, filtering, sorting, locale, time-zone, money/decimal, and date/time semantics where relevant.
- Define provider timeout, retry, circuit/degradation, reconciliation, and webhook behavior before integration.
- Supply audit and user-visible history for security-sensitive, financial, access, and irreversible actions.

## Non-functional requirements

Numeric targets must be agreed per journey before production load testing; they may not be invented during an incident.

| Quality | Required definition/evidence |
|---|---|
| Availability | Journey-specific SLO, dependency/degraded-mode policy, error budget, readiness behavior |
| Performance | p50/p95/p99 latency and throughput targets; query plans/indexes for critical queries; bounded lists/payloads |
| Scalability | Tenant/data-volume assumptions, worker concurrency, backpressure, queue-lag and pool limits |
| Reliability | Timeout/retry budgets, idempotency, reconciliation, dead-letter handling, graceful shutdown |
| Consistency | Named transaction boundary and explicit strong/eventual consistency expectations and lag objective |
| Recoverability | RPO/RTO, automated backups, verified restore, migration recovery, replay/reconciliation procedure |
| Maintainability | Enforced boundaries, typed public contracts, focused modules, ADRs, no undocumented special path |
| Compatibility | API/event support window, additive evolution, consumer contract tests, expand/migrate/contract plan |
| Observability | Structured redacted logs, metrics, traces, correlation across API/outbox/worker/provider, actionable alerts |
| Accessibility/localization | API supports labels/errors/content needed for accessible clients; locale, Unicode, time-zone and currency tested |
| Cost control | Provider usage/queue/storage/cardinality limits, tenant quotas where needed, anomaly metrics |

## Security baseline

### Identity and access

- Reviewed password/federation/session/token lifecycle, secure credential storage, rotation/revocation, and step-up authentication for defined high-risk actions.
- Deny by default. Server-side route declaration plus use-case record policy; object identifiers never imply authorization.
- Separate, audited platform-operator path; no hidden superuser behavior in tenant routes.
- Rate limits and abuse controls are actor-, tenant-, IP-, and action-aware as appropriate and fail safely.

### Tenant and database security

- Non-null `tenant_id`, forced RLS, transaction-local context, restricted runtime role, parameterized SQL, least-privilege grants.
- Two-tenant read/write/delete tests for every tenant repository and representative API/worker paths.
- Database constraints protect uniqueness, referential validity within owned boundaries, valid states, and concurrency-sensitive invariants.
- Privileged migrations/maintenance are separated, reviewed, logged, and never exposed through ordinary application paths.

### Data protection and privacy

- Classify each field as public, internal, confidential, or restricted/sensitive; collect only necessary data.
- Encrypt in transit and at rest; use field/token-level protection where threat models require it.
- Store secrets only in the approved secret facility; never repository/config samples/logs/events/analytics.
- Define purpose, consent where applicable, residency/vendor flow, retention, legal hold, export, correction, and deletion.
- Redact logs/traces/errors/events. Sensitive form answers, documents, messages, health/legal/child/financial data require explicit reviewed schemas.

### API, file, and integration security

- Apply strict schema/content-type/size limits, safe parsing, output encoding, CORS/host policy, and replay/CSRF controls appropriate to the auth mechanism.
- File flows use authorized upload intents, type/signature/size checks, quarantine/scanning where required, non-guessable keys, signed delivery, and safe disposition.
- Verify webhook signature, timestamp/replay window, endpoint secret, event identity, account/tenant mapping, and idempotency before changing state.
- Pin/review dependencies, scan artifacts and secrets, produce deployment provenance/SBOM as required, and patch by severity policy.
- Prevent SSRF and unsafe redirects when accepting URLs; bound provider responses and normalize errors.

### Security assurance

- Threat-model each new trust boundary and every sensitive niche before implementation/release.
- CI includes static/dependency/secret checks, architecture rules, authorization matrices, RLS, SQL safety, webhook tests, and targeted abuse cases.
- Critical/high findings block release. Accepted risk has owner, expiry, compensating controls, and approval.
- Incident response covers credential compromise, tenant-isolation breach, provider compromise, malicious upload, payment inconsistency, and data-loss scenarios.

## Slice definition of ready

A slice may enter implementation when:

- one owner, outcome, actors, scope, states, inputs/outputs, and dependencies are named;
- authorization/entitlement/relationship rules and data classification are reviewed;
- API/event/port contracts and compatibility expectations are written;
- concurrency, idempotency, consistency, provider failure, retention, and observability behavior are decided;
- acceptance tests are concrete and dependencies from prior phases are available.

## Slice definition of done

- Domain/application behavior and negative paths are tested.
- Migration owns tables clearly, uses safe constraints/indexes, and applies forced RLS to tenant data.
- Real-PostgreSQL repository tests include two tenants and concurrency where relevant.
- Interface tests cover validation, authentication, permission, entitlement, record policy, error contract, and idempotency.
- Events/adapters pass versioned contract, retry, duplicate, timeout, and redaction tests.
- Logs, metrics, traces, dashboard/alert impact, and runbook are implemented.
- Security/privacy review findings are resolved; docs and module README match behavior.
- `make check` and the relevant E2E journey pass from a clean state.

## Phase release gate

At the end of every phase, record a dated evidence packet containing:

1. Delivered and explicitly deferred requirements, with owners for approved deferrals.
2. Passing CI, migration, security, contract, performance, and critical E2E results.
3. Open risks/vulnerabilities and signed acceptance where permitted.
4. Data inventory/retention changes and provider/subprocessor changes.
5. SLO/dashboard/alert status and capacity/cost results.
6. Deployment, rollback, migration, reconciliation, restore, and incident-runbook verification.
7. Approval from the accountable engineering, product, security/privacy, and operations owners.

No phase exit waives the hard constraints in the delivery charter. A feature flag may limit exposure; it does not make unsafe or untested code complete.

## Project acceptance matrix

| Area | Minimum acceptance evidence |
|---|---|
| Scope | All promised niches/journeys trace to accepted requirements and owners |
| Architecture | Boundary/invariant tests pass; deviations have accepted ADRs |
| Functionality | Critical journeys and phase-specific negative paths pass E2E |
| Tenancy/access | Cross-tenant and authorization matrix tests pass for API, SQL, worker, portal |
| Data | Migrations, constraints, classification, retention/export/deletion, restore evidence pass |
| Integrations | Required adapters pass contracts, webhook security, outage/reconciliation exercises |
| Reliability | SLO/load results, retry/idempotency/dead-letter behavior, RPO/RTO drills accepted |
| Operations | Dashboards, alerts, on-call ownership, runbooks and rollback/disable procedures exercised |
| Security/privacy | Threat models and reviews complete; no blocking findings; risk acceptance current |
| Documentation | API/events/modules/ADRs/runbooks reflect the deployed release |

Only the accountable owners can declare production completion after this matrix and the delivery charter's completion definition are satisfied.
