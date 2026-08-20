# Capability map and niche comparison

This document compares [niche-feature-breakdown.md](niche-feature-breakdown.md) with the backend architecture. It is the ownership map used to prevent missing capabilities and niche-specific duplication.

## Gap analysis

The original architecture had 13 engines. They remain valid, but eight reusable boundaries were implicit or overloaded. The clean target adds these explicit engines:

| Added engine | Why it cannot remain implicit |
|---|---|
| Content | Page builder, blog, SEO, localization, navigation, policies, and publishing have their own lifecycle and versioning. |
| Commerce | Catalog and Payments do not own carts, orders, inventory, fulfillment, returns, gift cards, or POS synchronization. |
| Memberships | Customer memberships, recurring services, enrollments, attendance, and progress are not SaaS Billing. |
| Workflows | Cases, claims, maintenance, support tickets, projects, and checklists share state/assignment/timeline rules. |
| Learning | Courses, assessments, attempts, grades, and certificate eligibility form a distinct reusable domain. |
| Analytics | Tenant business dashboards and reports are different from platform telemetry. |
| Locations | Branches, service/delivery zones, radius/postcode rules, and neighborhood data need one geographic owner. |
| Communications | Two-way chat and conversation history are different from outbound Notifications. |

Identity is also promoted to a platform context because accounts, sessions, memberships, roles, and permission grants are business data, not technical helpers in `core`.

## Core platform feature ownership

| Product capability | Owner/composition |
|---|---|
| Domains and subdomains | Tenants + DNS adapter |
| Page builder, templates, blog, SEO, schema, localization, cookie/privacy content | Content + Themes + Media |
| Admin panel and feature configuration | API composition + Identity + Tenants + Billing entitlements |
| Staff roles and permissions | Identity |
| Forms and lead inbox | Forms emits submission events to CRM |
| Maps, branches and service areas | Locations + Maps adapter |
| Live/WhatsApp chat | Communications + Chat adapter |
| Email, SMS and push center | Notifications + channel adapters |
| Customer payments, invoices and receipts | Payments; Commerce supplies order context |
| Tenant SaaS subscription and feature pricing | Billing |
| Analytics dashboard, GA and heatmaps | Analytics + Analytics adapter |
| Reviews and testimonials | Reviews |
| Social feeds | Content + Social adapter |
| Media and files | Media; Documents owns business document state |
| Leads and contacts | CRM |
| Coupons and discounts | Commerce; Loyalty owns points/rewards |

## Niche-to-engine composition

The table names primary engines only. Content, Media, Notifications, Analytics, Identity, Tenants, Billing, and Themes are available to every niche.

| Niche | Primary reusable engines |
|---|---|
| Real estate/property management | Catalog, Search, Locations, Calculators, Scheduling, CRM, Portal, Workflows, Documents, Payments |
| Law firms/legal | Catalog, Scheduling, Forms, CRM, Portal, Workflows, Documents, Calculators, Communications, Reviews |
| Medical clinics | Catalog, Scheduling, Forms, Portal, Workflows, Documents, Notifications, Locations, Communications |
| Dental/specialized clinics | Catalog, Scheduling, Forms, Calculators, Payments, Reviews, Media |
| Accounting/bookkeeping | Catalog, Scheduling, Forms, Portal, Documents, Calculators, Payments, Notifications |
| Insurance agencies | Catalog, Forms, Calculators, Search, Workflows, Portal, Documents, Notifications, Communications |
| Home improvement/HVAC | Catalog, Locations, Forms, Calculators, Scheduling, Workflows, Media, Reviews, Payments |
| Restaurants/food | Catalog, Commerce, Scheduling, Locations, Payments, Loyalty, Notifications, Forms |
| Fitness/trainers | Catalog, Scheduling, Memberships, Payments, Portal, Learning, Notifications, Loyalty |
| Salons/spas | Catalog, Scheduling, Memberships, Payments, Loyalty, Commerce, Media, Notifications |
| Bakeries/event vendors | Catalog, Forms, Scheduling, Payments, Media, Workflows, CRM |
| E-commerce/dropshipping | Catalog, Commerce, Payments, Search, Reviews, Loyalty, Notifications, Locations |
| Travel/tours | Catalog, Scheduling, Calculators, Payments, Locations, Forms, Reviews, Documents |
| Cleaning services | Catalog, Calculators, Scheduling, Memberships, Locations, Workflows, Portal, Media |
| Landscaping/lawn care | Catalog, Forms, Media, Memberships, Locations, Scheduling, Calculators |
| Construction/remodeling | Media, Calculators, Catalog, Scheduling, Workflows, Portal, Documents, CRM |
| Photography/creative | Media, Catalog, Scheduling, Payments, Portal, Commerce, Documents |
| Tutors/training centers | Learning, Catalog, Scheduling, Payments, Memberships, Portal, Documents, Communications |
| Daycare/children's activities | Catalog, Forms, Scheduling, Memberships, Portal, Workflows, Documents, Notifications |
| IT support/MSP | Catalog, Forms, Workflows, Portal, Communications, Documents, Notifications, Analytics |
| Chiropractic/physical therapy | Catalog, Scheduling, Forms, Workflows, Portal, Reviews, Analytics |
| Veterinary/pet care | Catalog, Scheduling, Workflows, Portal, Notifications, Commerce, Forms |
| Wedding/event planning | Catalog, Media, Workflows, Forms, Calculators, Scheduling, Payments, Portal |
| Nonprofits/fundraisers | CRM, Content, Payments, Forms, Scheduling, Portal, Documents, Notifications, Analytics |
| Local/specialty clinics | Catalog, Scheduling, Forms, Workflows, Portal, Documents, Calculators, Communications |

## External adapter coverage

The niche list also requires provider-neutral skeletons beyond the original Stripe/email/SMS/DNS/storage set:

- calendar synchronization;
- maps/geocoding;
- video/telehealth/webinars;
- e-signature;
- search indexing;
- push and two-way chat;
- analytics and heatmaps;
- social feeds;
- POS, shipping, supplier, and property-feed synchronization.

Provider choice is deferred. Adding an adapter directory records the seam, not a vendor commitment.

## Deliberate non-engines

- Provider/agent/trainer/staff profile pages are typed Catalog entries with Identity references.
- Galleries and before/after showcases compose Media + Content + Reviews.
- Portals provide access and navigation; they do not own medical records, cases, grades, orders, or documents.
- Niche terminology and default fields are declarative niche configuration.
- Regulatory claims such as HIPAA compliance are release requirements, not folder names. They require a separate threat model, vendor review, audit controls, retention policy, and operational evidence.
