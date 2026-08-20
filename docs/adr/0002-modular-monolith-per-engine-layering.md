# ADR 0002: Modular monolith with per-engine layering

- Status: Accepted
- Date: 2026-08-20

## Context

The product serves many niches with heavily reused capabilities. Separate niche applications would duplicate booking, payments, forms, content, and portals. Early microservices would add deployment and consistency cost before module boundaries are proven.

## Decision

Build one deployable modular monolith. Platform contexts and reusable engines own their data and expose application APIs/events. Each module separates domain, application, infrastructure, and interface layers. Imports and SQL access across module internals are prohibited and checked in CI.

## Consequences

- Development, transactions, and deployment stay simple while ownership remains explicit.
- Niches compose engines instead of forking implementations.
- Cross-module projections and events require discipline.
- A module can be extracted later only after traffic/team/availability evidence justifies it.
