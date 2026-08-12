# Backend Implementation Plan
### Multi-Niche Website Builder SaaS — FastAPI Modular Monolith

This plan maps **every feature from the niche breakdown doc** (25 niches + core platform features) into a finite set of reusable backend engines, then defines the schema, APIs, and implementation sequence needed to support the full signup → subdomain → feature selection/billing → theme → setup → instant admin panel flow.

---

## 1. Feature-to-Engine Mapping (the missing piece)

Every single feature across all 25 niches maps to one of **13 core engines**. This is the master map — nothing in the niche doc falls outside it. Build the engine once, configure per niche/tenant.

| # | Engine | Covers features like... |
|---|---|---|
| 1 | **Scheduling & Booking** | appointments, table reservations, class bookings, service visits, consultation booking, boarding/grooming booking, tutoring sessions |
| 2 | **Catalog & Inventory** | products, services, packages, menu items, courses, insurance types, tour packages, retail items, variants/stock |
| 3 | **Forms & Intake** | contact forms, quote requests, patient intake, document upload requests, client questionnaires, enrollment applications, claims filing |
| 4 | **Payments & Billing** | checkout, invoicing, deposits, financing calculators, membership billing, donation processing, platform subscription billing |
| 5 | **CRM & Leads** | lead capture, contact tags/notes, agent/staff assignment, follow-up tracking |
| 6 | **Client/Customer Portal** | patient portal, tenant portal (property), student portal, donor portal, member portal, parent portal — all = one generic "Portal" engine scoped by role |
| 7 | **Documents & E-Signature** | lease signing, engagement letters, contracts, proofing galleries, secure document upload |
| 8 | **Notifications** | email/SMS/push reminders, renewal reminders, vaccination reminders, order tracking updates |
| 9 | **Reviews & Testimonials** | reviews carousel, case results, before/after galleries (paired with Catalog/Media) |
| 10 | **Search & Comparison** | property search/filters, MLS/IDX, insurance/tour comparison tools, service area/zip checkers |
| 11 | **Loyalty & Membership** | rewards points, membership tiers, gift cards/vouchers, waitlists |
| 12 | **Calculators/Estimators** | quote calculators, mortgage/EMI, cost estimators, fee estimators — one generic rule-based calculator engine, configured per niche |
| 13 | **Media & Content** | blog, portfolio galleries, virtual tours, digital downloads, menu/photo libraries |

Cross-cutting (not engines, but platform infrastructure): **Tenant Management, Theme Rendering, Auth/RBAC, Feature Flags/Billing enforcement, Event Bus, Search indexing, Multi-location.**

> Nothing in the 25-niche list requires a 14th engine. E.g., "Symptom checker" = Forms engine with conditional logic. "Telemedicine" = Scheduling engine + third-party video SDK integration. "POS integration" = Catalog + Payments + external adapter. Treat any new niche's "unique-looking" feature as a recombination of these 13 before building something new.

---

## 2. High-Level Architecture

```
platform-backend/
├── app/
│   ├── core/                      # config, db, security, event bus, middleware
│   ├── tenants/                   # tenant lifecycle, subdomain, onboarding
│   ├── engines/
│   │   ├── scheduling/
│   │   ├── catalog/
│   │   ├── forms/
│   │   ├── payments/
│   │   ├── crm/
│   │   ├── portal/
│   │   ├── documents/
│   │   ├── notifications/
│   │   ├── reviews/
│   │   ├── search/
│   │   ├── loyalty/
│   │   ├── calculators/
│   │   └── media/
│   ├── features/                  # niche configs (which engines + fields + pages)
│   │   ├── restaurant/
│   │   ├── salon_fitness/
│   │   ├── real_estate/
│   │   ├── home_services/
│   │   ├── clinics/
│   │   └── ecommerce/
│   ├── billing/                   # platform subscription + per-feature billing
│   ├── themes/                    # theme registry, compatibility rules
│   ├── admin_api/                 # admin panel endpoints (tenant-scoped)
│   ├── public_api/                # public tenant-site endpoints
│   ├── platform_api/              # platform-owner endpoints (super-admin)
│   └── main.py
├── alembic/                       # migrations
├── workers/                       # background jobs (ARQ/Celery)
└── tests/
```

---

## 3. Core Data Model

### 3.1 Platform-level tables

```
tenants (id, business_name, subdomain, custom_domain, niche_type, status, created_at)
users (id, tenant_id NULL for platform staff, email, role, auth_provider_id)
tenant_staff (tenant_id, user_id, role, permissions JSON)
end_customers (id, tenant_id, name, email, phone, metadata JSONB)   -- tenant's own customers

features (id, key, name, category, engine, dependencies JSONB, base_price, billing_type)
tenant_features (id, tenant_id, feature_id, enabled, config JSONB, activated_at, billing_status)

themes (id, key, name, supported_engines JSONB, preview_url)
tenant_theme_config (tenant_id, theme_id, customizations JSONB)

subscriptions (id, tenant_id, stripe_subscription_id, status, current_period_end)
subscription_items (id, subscription_id, feature_id, quantity, unit_price)
invoices (id, tenant_id, amount, status, period_start, period_end)
```

### 3.2 Engine tables (generic, reused across every niche)

```
-- Scheduling
resources (id, tenant_id, type, name, capacity, metadata JSONB)         -- table, room, staff, class slot
bookings (id, tenant_id, resource_id, customer_id, start_at, end_at, status, metadata JSONB)
availability_rules (id, tenant_id, resource_id, day_of_week, start_time, end_time)

-- Catalog
catalog_items (id, tenant_id, type, name, description, price, media JSONB, metadata JSONB)
catalog_variants (id, item_id, name, price_delta, stock_qty)
catalog_categories (id, tenant_id, name, parent_id)

-- Forms
form_templates (id, tenant_id, key, schema JSONB)          -- schema-driven, supports conditional fields
form_submissions (id, tenant_id, form_template_id, customer_id, data JSONB, status)

-- Payments
transactions (id, tenant_id, type, amount, status, provider_ref, related_entity_type, related_entity_id)
orders (id, tenant_id, customer_id, items JSONB, total, status)

-- CRM
leads (id, tenant_id, source, contact_info JSONB, status, assigned_staff_id, tags JSONB)
lead_notes (id, lead_id, staff_id, note, created_at)

-- Portal (generic, role-scoped)
portal_access (id, tenant_id, customer_id, portal_type, permissions JSONB)

-- Documents
documents (id, tenant_id, owner_type, owner_id, file_url, status, signed_at)

-- Notifications
notification_templates (id, tenant_id, channel, trigger_event, template_body)
notification_log (id, tenant_id, recipient, channel, status, sent_at)

-- Reviews
reviews (id, tenant_id, customer_id, subject_type, subject_id, rating, comment, media JSONB)

-- Loyalty
loyalty_accounts (id, tenant_id, customer_id, points_balance, tier)
loyalty_transactions (id, loyalty_account_id, points, reason)

-- Calculators
calculator_configs (id, tenant_id, key, rules JSONB)   -- e.g. quote/EMI/fee logic as data, not code

-- Media
media_assets (id, tenant_id, type, url, alt_text, metadata JSONB)
```

**Design rule:** every engine table has `tenant_id` + a `metadata`/`config JSONB` column so niche-specific fields (e.g., "square footage" for cleaning quotes, "bar admission year" for lawyers) live as data, not schema changes. This is what lets you add niche #26 without a migration.

---

## 4. Feature Dependency & Billing Enforcement

```python
# features table entry example
{
  "key": "table_reservation",
  "engine": "scheduling",
  "dependencies": ["notifications"],   # auto-bundled, not separately charged
  "billing_type": "flat_monthly",
  "base_price": 9.00
}
```

```python
# core/deps.py — FastAPI dependency enforced on every engine router
async def require_feature(feature_key: str):
    async def checker(tenant: Tenant = Depends(get_current_tenant), db=Depends(get_db)):
        if not await tenant_features_service.is_enabled(db, tenant.id, feature_key):
            raise HTTPException(402, f"Feature '{feature_key}' not enabled for this tenant")
    return checker

# usage
@router.post("/bookings", dependencies=[Depends(require_feature("table_reservation"))])
async def create_booking(...): ...
```

**Activation logic:**
1. Tenant selects feature in onboarding/admin → `POST /admin/features/{key}/enable`
2. Service resolves `dependencies[]` → hard/infra deps (Notifications, Auth) auto-enabled at $0; billable deps prompt confirmation with combined price shown
3. On confirm → `tenant_features` row created, `subscriptions` updated via Stripe, event `feature.enabled` published
4. Deactivation → check `reverse_dependencies` (which enabled features declare this as a dependency) → block or cascade-disable with warning

---

## 5. Event Bus (cross-engine communication)

```python
# core/events.py
class EventBus:
    def __init__(self):
        self._subscribers: dict[str, list[Callable]] = {}
    def subscribe(self, event: str):
        def decorator(fn):
            self._subscribers.setdefault(event, []).append(fn)
            return fn
        return decorator
    async def publish(self, event: str, payload: dict):
        for fn in self._subscribers.get(event, []):
            await fn(payload)

event_bus = EventBus()
```

Example chains this replaces with loose coupling:
- `booking.created` → notifications sends confirmation, CRM logs lead-to-customer conversion, loyalty adds points
- `order.paid` → invoice generated, inventory decremented, notification sent, CRM tagged
- `form.submitted` (quote request) → lead created, notification to staff, calculator engine can pre-fill estimate

Start in-process (async function calls). Move `publish()` to Redis pub/sub or a task queue (ARQ) once you need retries, delays (e.g., "reminder 24h before booking"), or multi-process scaling.

---

## 6. The Core Onboarding Flow — Backend Implementation

### Step 1: Business name → subdomain
```
POST /public/tenants/check-subdomain   {business_name} → suggested_subdomain, available: bool
POST /public/tenants                   {business_name, subdomain, owner_email} → tenant_id, draft status
```
- Subdomain slugified + uniqueness check against `tenants.subdomain`
- Tenant created with `status = "onboarding"` (not live yet — prevents incomplete tenants from resolving publicly)
- Cloudflare API call (async job) to register subdomain DNS + SSL (can run in background while user continues wizard)

### Step 2: Feature selection + pricing
```
GET  /public/tenants/{id}/recommended-features?niche=restaurant
POST /public/tenants/{id}/features       {feature_keys: [...]}  → dependency resolution + price breakdown
```
- Returns live price calculation including auto-bundled dependencies
- Does NOT charge yet — stores selection in `tenant_features` as `pending`

### Step 3: Theme selection
```
GET  /public/themes?compatible_features=[...]   → filtered theme list
POST /public/tenants/{id}/theme          {theme_id}
```
- Theme's `supported_engines` checked against tenant's selected features; incompatible themes filtered server-side, not just UI

### Step 4: Basic info setup
```
POST /public/tenants/{id}/basic-info     {logo, address, hours, phone, description}
```

### Step 5: Instant provisioning
```
POST /public/tenants/{id}/activate
```
This single call, run as an async pipeline:
1. Charge via Stripe (first invoice/subscription creation)
2. Set `tenants.status = "active"`
3. Materialize `tenant_features` from `pending` → `enabled`
4. Provision default data (empty catalog categories, default notification templates per enabled engine)
5. Publish `tenant.activated` event → triggers welcome email, admin panel first-run checklist generation
6. Return `admin_panel_url` + `site_url`

Target: this whole pipeline completes in seconds, not minutes — keep it mostly synchronous with only slow steps (DNS propagation confirmation) deferred to background polling shown as a progress state in the UI.

---

## 7. Multi-Tenancy Enforcement

- **Middleware** resolves `Host` header → subdomain/custom domain → `tenant_id`, attached to `request.state`
- **Repository base class**: every query method requires `tenant_id` param, no "list all" method exists without it — prevents accidental cross-tenant leaks by construction
- **Postgres Row-Level Security** as second layer: policy `USING (tenant_id = current_setting('app.tenant_id')::uuid)`, set per-connection at request start
- Platform super-admin endpoints (`/platform_api`) explicitly bypass tenant scoping — kept in a completely separate router with separate auth scope, never mixed with tenant-scoped routers

---

## 8. API Surface Structure

| Namespace | Audience | Auth |
|---|---|---|
| `/public_api/*` | Anonymous site visitors (tenant's own customers) | none / end-customer session |
| `/admin_api/*` | Tenant owner/staff | tenant-scoped JWT, role-checked |
| `/platform_api/*` | Your internal team | platform-admin auth |
| `/onboarding/*` | New signups mid-wizard | temporary onboarding token |

Each engine exposes routers under both `public_api` (read-mostly, e.g., see available booking slots, browse catalog) and `admin_api` (manage bookings, catalog CRUD) — same service layer, different permission checks.

---

## 9. Background Jobs (ARQ + Redis recommended)

- Subdomain DNS/SSL provisioning
- Scheduled notifications (booking reminders, renewal reminders)
- Recurring billing cycles
- Report/analytics aggregation (nightly)
- Search index rebuilding (Meilisearch) for catalog/property search
- Abandoned cart / incomplete onboarding follow-up emails

---

## 10. Implementation Sequence (maps to earlier roadmap)

| Phase | Backend deliverables |
|---|---|
| 1 | Tenant model, subdomain middleware, auth, Stripe skeleton, event bus |
| 2 | Scheduling, Catalog, Forms, Payments, Notifications engines (generic) |
| 3 | CRM, Portal, Documents, Reviews, Loyalty, Calculators, Media engines |
| 4 | Feature dependency/billing enforcement layer, onboarding pipeline endpoints |
| 5 | Niche configs for 3 MVP niches (feature bundles, default form schemas, default calculator rules) |
| 6 | Admin API completion (all engine CRUD + RBAC), Platform API (tenant management, billing overrides) |
| 7 | Background jobs, search indexing, load testing, beta |

---

## 11. Testing Strategy Notes

- Per-engine unit tests with a fixture tenant + fixture data
- Cross-tenant isolation test suite (attempt cross-tenant reads/writes, must always fail)
- Dependency resolution test matrix (enable/disable combinations across all 13 engines)
- Onboarding pipeline integration test: full flow from subdomain check → activation, asserting site is live and billed correctly
