# Phase-wise implementation playbook

Status: implementation contract  
Applies to: the complete Connect backend  
Architecture authority: [Backend architecture](../01-architecture.md)

This playbook turns the target architecture into buildable work. It defines what completion means, what may not be traded away as "small," who owns each capability, the order in which it is built, and the evidence required to pass each phase.

It is a plan, not a statement that the repository already satisfies every item. An item is complete only when its named evidence exists and passes in CI.

## How to use this playbook

Read and apply these documents in order:

1. [Delivery charter](00-delivery-charter.md): guiding principles, scope, hard constraints, change control, and project completion.
2. [Components and boundaries](01-components-and-boundaries.md): ownership, provided surfaces, dependencies, and forbidden coupling.
3. [Foundation phases](02-phases-0-to-2.md): repository guardrails, platform foundation, and site foundation.
4. [Product phases](03-phases-3-to-5.md): revenue, operations, learning, and advanced-niche delivery.
5. [Quality, security, and completion gates](04-quality-security-and-gates.md): functional and non-functional requirements, security controls, evidence, and release gates.
6. [Priority build flow](05-priority-build-flow.md): strict dependency waves, component IDs, implementation sequence, and the first complete revenue loop.

The shorter [backend implementation guide](../backend-implementation-guide.md) is the roadmap; this directory is the detailed delivery contract. If they disagree, the accepted architecture and ADRs take precedence, then this playbook. Correct both documents in the same change.

## Delivery unit

The smallest acceptable unit is a vertical slice: one useful behavior from API or worker entry point through authorization, application orchestration, domain rules, persistence, events, observability, and tests. A directory, table, route stub, or provider client by itself is not delivered value.

Every slice moves through:

`defined -> tested at domain/application level -> persisted safely -> exposed securely -> integrated asynchronously -> observable -> documented -> accepted`

## Phase dependency map

| Phase | Depends on | Outcome |
|---|---|---|
| 0. Guardrails | None | The repository rejects architectural and security violations automatically. |
| 1. Platform foundation | Phase 0 | A tenant can onboard, authenticate, and operate inside isolated, entitled access. |
| 2. Site foundation | Phase 1 | A tenant can publish a localized site and capture/manage leads. |
| 3. Revenue capabilities | Phase 2 | Initial service niches can list, quote, book, take payment, and collect reviews. |
| 4. Transaction operations | Phase 3 | Commerce and service operations work across orders, plans, portals, documents, and cases. |
| 5. Advanced niches | Phase 4 plus niche-specific controls | Learning and sensitive/advanced niche compositions are production-ready. |

Phases are gates, not necessarily release names. Teams may develop independent slices in parallel only after their shared prerequisites and contracts are stable. No later phase may bypass an earlier security or data-integrity gate.

Within each phase, the [priority build flow](05-priority-build-flow.md) is authoritative for sequencing. A component may start early only when every prerequisite contract named there is accepted; early scaffolding does not change its completion order.

## Standard work package

Every implementation ticket must state:

- owning module and affected public contract;
- user or worker outcome and explicit out-of-scope behavior;
- actors, permission, entitlement, tenant, and record-level policy;
- state transitions, invariants, idempotency, and concurrency rules;
- owned tables and migration/RLS impact;
- emitted and consumed event versions;
- provider failure behavior, when applicable;
- data classification, retention, export, and deletion behavior;
- test and observability evidence;
- rollout, compatibility, and rollback plan.

If these cannot be stated, the slice is not ready to implement.
