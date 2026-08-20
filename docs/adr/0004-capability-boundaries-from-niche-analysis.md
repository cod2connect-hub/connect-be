# ADR 0004: Expand reusable capability boundaries after niche analysis

- Status: Accepted
- Date: 2026-08-20

## Context

Comparing the original 13-engine design with all 25 niche requirements exposed capabilities that had no clear owner or would overload Catalog, Portal, Notifications, Billing, or Core. The missing areas were site content, transaction operations, customer memberships, operational workflows, learning, business analytics, geographic rules, and two-way conversations.

## Decision

Add Content, Commerce, Memberships, Workflows, Learning, Analytics, Locations, and Communications engines. Add Identity as a platform context. Keep niche packages declarative and map all niche behavior to shared engines.

## Consequences

- Carts are no longer confused with catalog or payments.
- Customer memberships are separate from platform SaaS billing.
- Portals expose records without becoming their owner.
- Outbound notifications remain separate from interactive conversations.
- The larger module list increases boundary checks and documentation needs but avoids hidden catch-all modules.
