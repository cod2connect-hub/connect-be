# Phases 3–5: revenue, operations, and advanced niches

## Phase 3 — First revenue capabilities

### Objective

Deliver complete list-to-lead, quote, booking, and payment journeys for the first service niches. Scheduling is the reference rich-domain engine and establishes the pattern for later engines.

### Build order and minimum slices

1. **Catalog:** categories -> offerings/listings -> variants/options -> pricing/display state -> publish/archive.
2. **Scheduling:** resources -> availability/time zones -> hold -> confirm/reschedule/cancel -> recurrence/classes/waitlist.
3. **Calculators:** immutable rule-set version -> evaluation -> explainable result -> expiry/recalculation.
4. **Payments:** intent/deposit -> provider confirmation/webhook -> receipt -> refund; ledger-like immutable history.
5. **Reviews:** eligibility/request -> submit -> moderate/respond -> publish/unpublish with consent refs.
6. **Search:** index published catalog/content -> query/filter -> saved search/favorite/compare as required.
7. Compose home-service, salon, and real-estate MVP journeys without niche-owned business code.

### Required behavior

- Catalog publication validates required media/location/category/variant data and preserves historical references after archive.
- Scheduling handles time zones, daylight-saving changes, capacity, resource conflicts, holds, expirations, concurrent booking, cancellation policy, and recurrence exceptions.
- Calculations name the exact rule-set/version and inputs used, distinguish estimate from binding price, and support deterministic replay.
- Payment amounts/currency are server-derived or verified, transitions are monotonic, webhook authenticity is checked, and duplicate/out-of-order callbacks are safe.
- Refund/deposit/receipt behavior is permissioned and audited; secrets and payment instrument data never enter application storage/logs.
- Reviews enforce subject/author eligibility, moderation, consent for linked media, and abuse controls.
- Search is an eventually consistent projection; source modules remain authoritative and removed/private items disappear within the defined objective.

### Exit evidence

- E2E journeys for home service quote/booking/deposit, salon appointment/payment/reminder, and real-estate listing/search/inquiry.
- Database constraints and concurrency tests prove no accidental double booking or duplicate monetary effect.
- Payment reconciliation, webhook replay, refund failure, expired hold, DST boundary, search lag/removal, and moderation tests pass.
- Financial and booking audit trails can reconstruct every transition without sensitive provider payloads.

## Phase 4 — Transaction operations

### Objective

Support order operations and longer-lived customer/staff workflows after the foundational revenue flows are stable.

### Build order and minimum slices

1. **Commerce:** cart -> price snapshot -> order placement -> payment -> inventory reservation -> fulfillment/cancel/refund.
2. **Loyalty:** append-only points/reward entries -> tier calculation -> voucher/referral -> atomic redemption.
3. **Memberships:** plan/enrollment -> billing link -> attendance/usage -> pause/cancel/renew.
4. **Portal:** customer access grant -> relationship/record policy -> scoped referenced views/actions.
5. **Documents:** business document metadata/version -> access/share -> e-signature status -> retention/deletion.
6. **Workflows:** typed case/ticket/project -> assignment/checklist -> transition/timeline -> closure/reopen.
7. **Communications:** consent/participants -> inbound/outbound message -> provider status -> case/contact linkage.
8. Add POS, shipping, supplier, e-signature, chat, and other adapters only for enabled verticals.

### Required behavior

- Order pricing and discounts are server-authoritative snapshots; inventory, payment, fulfillment, return, and cancellation states have explicit compensation rules.
- Loyalty value cannot be duplicated by concurrency, replay, refund, or cancellation; every balance derives from an auditable entry history.
- Membership renewals and usage are idempotent, time-zone aware, and correctly respond to payment failure, pause, cancellation, and plan change.
- Portal grants visibility, not ownership; each referenced record is authorized by its owning engine and customer relationship/purpose.
- Documents distinguish storage object from business meaning, enforce classification/access/versioning, and record signature evidence without trusting client status.
- Workflow types declare allowed transitions, required fields, SLA clocks, assignment rules, and closure/reopen policy.
- Communications enforce consent/channel rules, participant scoping, attachment policy, webhook authenticity, retention, and safe redaction.

### Exit evidence

- Restaurant/commerce E2E: menu/cart/order/payment/fulfillment/cancel or return/notification/loyalty.
- Service E2E: membership renewal plus portal access to allowed booking/document/workflow records.
- Staff E2E: intake -> case/ticket -> assignment -> communication/document -> resolution with complete timeline.
- Replay, partial provider failure, inventory race, double redemption, portal object-reference attack, unsafe attachment, and retention tests pass.

## Phase 5 — Learning and advanced niches

### Objective

Complete Learning and safely validate advanced compositions for education, daycare, clinics, nonprofits, legal, insurance, property management, and IT support.

### Build order

1. Learning content/lesson model and publication.
2. Enrollment/member linkage and learner access.
3. Assessments, attempts, grading, progress, and certificate eligibility.
4. Portal/document/video/communication integrations through contracts.
5. Per-niche capability manifest and dependency validation.
6. Per-niche authorization/relationship matrix, data inventory, threat model, retention schedule, vendor review, and abuse analysis.
7. Per-niche end-to-end journeys, operational runbook, support training, rollout controls, and approval.

### Required behavior

- Learning attempts and grades preserve history, limit retries according to rule version, and calculate progress/certification deterministically.
- Certificates reference immutable eligibility evidence and a document lifecycle.
- Child, medical, legal, insurance, identity, and financial records use explicit subject/guardian/client/staff relationships and purpose-scoped access.
- Exports, corrections, legal holds, retention, deletion, emergency access if applicable, and audit review are designed per data class and jurisdiction.
- Niche terminology remains presentation/configuration; it does not fork engine state machines.
- Provider contracts required for video/telehealth, e-signature, property feeds, donations, or support chat are reviewed against the niche threat model.

### Niche release packet

Each niche needs:

- versioned feature/dependency manifest and supported journey list;
- actor-to-action-to-record authorization matrix;
- data classification/inventory, lawful-purpose record, retention/deletion rules, and logging redaction map;
- threat model, provider/subprocessor review, security test report, and unresolved-risk acceptance;
- load/capacity assumptions and failure/degradation behavior;
- end-to-end test evidence, dashboard/alert links, incident and customer-support runbook;
- controlled rollout, rollback/disable plan, and named business/security/operations approvers.

### Exit evidence

- Learning E2E covers publish -> enroll -> learn -> assess -> grade -> certificate -> portal access.
- Every enabled advanced niche passes its complete release packet; unsupported or unapproved capabilities fail closed.
- Cross-role/cross-relationship/cross-tenant attacks and sensitive-data leakage checks pass.
- Retention cleanup, export, deletion, backup restore, key rotation, and relevant provider outage exercises are demonstrated with synthetic data.
