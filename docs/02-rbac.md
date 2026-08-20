# Identity, tenancy, RBAC, and feature access

## Security boundaries

Four independent checks protect a request:

1. Authentication proves the actor identity.
2. Tenant membership proves the actor belongs to the resolved tenant.
3. RBAC proves the actor may perform the action.
4. Entitlement proves the tenant has the required product feature.

Passing one check never implies another. PostgreSQL RLS remains the final tenant data boundary.

## Actors

- Platform operator: manages the SaaS itself through explicitly privileged platform routes.
- Tenant owner/staff: belongs to one or more tenants through separate memberships and roles.
- Customer/portal user: has scoped access to their own portal records.
- Public visitor: can access only published resources and rate-limited public actions.
- Worker/service actor: processes a signed job with an explicit tenant and handler identity.

## Permission model

Permissions use stable `resource.action` names such as `booking.read`, `booking.manage`, `order.refund`, and `staff.invite`. Roles are tenant-scoped collections of permissions. A membership can hold roles and narrowly scoped direct grants only when the audit trail records why.

Routes declare required permissions at registration time. Ownership and record-level policies are evaluated inside the owning application use case. Platform operator permissions are separate from tenant permissions.

## Feature access

Feature access is evaluated from Billing entitlements and tenant feature configuration. A route that requires an unavailable engine returns a stable feature-not-enabled problem; it does not silently expose partial behavior.

Feature dependency examples:

- `commerce.online_ordering` requires Catalog, Commerce, and Payments.
- `scheduling.reminders` requires Scheduling and Notifications.
- `content.custom_domain` requires Tenants, Content, and DNS integration readiness.

## Database enforcement

- Every tenant-owned table contains non-null `tenant_id`.
- RLS is enabled and forced on tenant-owned tables.
- Policies read transaction-local tenant context, never a connection-global value.
- The runtime role is not the table owner and cannot bypass RLS.
- Connection-pool release clears transaction state by ending the transaction.
- Cross-tenant platform operations use a separately audited role and code path.

## Sensitive records

Portal access is not a universal permission to all portal-linked data. Medical records, legal cases, children, insurance, financial documents, and private media require explicit relationship and purpose checks. Logging must omit secrets, message bodies, health data, uploaded documents, and form answers unless a reviewed audit requirement says otherwise.

## CI invariants

- Every non-public admin route declares a permission dependency.
- Every feature route declares its entitlement dependency.
- Every tenant table has RLS and a policy.
- Tests prove two tenants cannot read or mutate one another's records.
- Permission and entitlement seeds are append-only identifiers with migration review.
