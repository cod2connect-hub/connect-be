# Global Gateway Travel ERP — MVP Scope & Requirements

**Client:** Global Gateway Int'l Travels & Tours P. Ltd.
**Document purpose:** Define the minimum system that is genuinely usable end-to-end in daily agency operations, decomposed into independently buildable components, with functional and non-functional requirements. This is the input document for the next three deliverables: Architecture Design, API Design, Schema Design.
**Status:** Draft v1 — requires client sign-off on Section 2 (cut list) before architecture work begins.

---

## 1. MVP definition and guiding principle

The proposal describes six modules. Building all six before anything goes live is a 16-week bet with no feedback. The MVP instead targets **one complete revenue loop**:

> An enquiry arrives on any channel → becomes a lead → becomes a quotation → becomes a booking with a ticket → becomes an invoice and a recorded payment → shows up in a report.

If any link in that chain is missing, the agency still needs a spreadsheet, and adoption fails. Everything in the MVP exists to close that loop. Everything that improves, automates or extends the loop is deferred.

**Two hard constraints that drive the cut list:**

1. **GDS access is not a software problem.** Amadeus/Sabre/Galileo require a commercial contract, IATA/agency credentials, a certification cycle and per-transaction fees. That process is owned by the client and typically runs longer than the MVP build. The MVP therefore treats ticketing as a **record-keeping and document workflow**, with the GDS adapter designed for but not implemented.
2. **AI calling is the highest-cost, lowest-certainty item.** Nepali speech recognition and synthesis at production quality, telephony provisioning, call recording consent and script tuning are a project in their own right. It is deferred entirely.

---

## 2. In / Out of MVP

| Proposal module | MVP decision | Rationale |
|---|---|---|
| 01 CRM & Sales Pipeline | **In (core)** | This is the product. Without it nothing else has a customer record to attach to. |
| 02 AI Calling System | **Out** | Telephony + Nepali ASR/TTS + consent handling. Separate project, post-MVP. |
| 03 AI Chatbot | **In (reduced)** | WhatsApp + website widget only. FAQ answering, lead capture, human handover. Facebook/Instagram deferred. |
| 04 Ticketing & GDS API | **In (reduced)** | Booking/PNR/ticket records, e-ticket issue-and-send, refunds/cancellations as status changes. Live fare search via GDS deferred behind an adapter interface. |
| 05 Accounts & Finance | **In (reduced)** | Invoices, receipts, payments, supplier cost, commission and margin per booking, AR ageing. Full double-entry ledger, BSP settlement, multi-currency FX revaluation and VAT filing deferred. |
| 06 HR & Employees | **In (minimal)** | Employee records, roles/permissions, agent targets vs. actuals. Attendance, leave, payroll, SSF and tax deferred. |

**Explicitly deferred to v2+ (record this so it is not re-litigated mid-build):**
AI calling · Facebook/Instagram channel · live GDS fare search and auto-issue · full double-entry general ledger and chart of accounts · BSP reconciliation · multi-currency revaluation · VAT/audit statutory reports · payroll, SSF, tax and payslips · attendance and leave · tour package library with seasonal pricing · visa/passport-expiry reminder engine · customer self-service portal · mobile app.

**Non-negotiable even though "small":** role-based access control and the audit trail. Both are cross-cutting; retrofitting them after go-live means touching every table and every endpoint. They are MVP.

---

## 3. Component breakdown

Twelve components. Each is a separable build unit with its own owner, its own data, and a defined interface. The split is deliberately along **data ownership** lines so it survives either a modular-monolith or a service-oriented architecture decision later.

### C1 — Identity, Access & Audit (platform)
- **Owns:** users, roles, permissions, sessions, refresh tokens, password/reset flows, audit log.
- **Provides:** authentication for all components; a permission-check interface; an append-only audit writer used by every other component.
- **Depends on:** nothing. Build first.
- **Out of MVP:** SSO, 2FA (design the user table for it), IP allowlisting.

### C2 — Master Data & Configuration
- **Owns:** airlines, airports, countries, currencies, exchange rates (manually entered), tax rates, service/fee types, lead sources, cancellation-reason codes, quotation and invoice numbering series, branch/office records.
- **Provides:** lookups to every other component.
- **Note:** Seeded reference data (IATA airline and airport codes) is an import task, not a build task.

### C3 — Customer & Traveller Master
- **Owns:** customer records (individual and corporate), traveller profiles, passport details, contact channels, relationships (family/company group), deduplication and merge.
- **Critical:** one traveller can appear on many bookings; a corporate customer bills, but travellers fly. Model these separately from day one.
- **Depends on:** C1, C2, C11.

### C4 — Enquiry & Lead Intake
- **Owns:** raw inbound messages from all channels, normalisation into a lead, channel-identity mapping (phone/WhatsApp ID/email → customer), deduplication against open leads, assignment rules, ownership.
- **Provides:** a lead to C5.
- **Depends on:** C3, C9 (messaging), C10 (jobs).
- **This is the component most likely to be underestimated.** Matching an unknown WhatsApp number to an existing customer, and deciding whether a new message is a new lead or a reply to an open one, is real logic.

### C5 — Sales Pipeline & Quotation
- **Owns:** lead lifecycle and stages (enquiry → qualified → quoted → booked → lost), quotation documents with line items and validity, versioning of quotations, activity timeline, follow-up tasks and reminders, lost-reason capture.
- **Provides:** an accepted quotation to C6.
- **Depends on:** C3, C4, C2, C11, C10.

### C6 — Booking & Ticketing
- **Owns:** booking records, passenger list per booking, itinerary segments, PNR reference, ticket numbers, fare and tax breakdown, supplier/airline, issue and void/refund/cancellation status, change history.
- **Interface (not implementation):** `FareSearchProvider` and `TicketIssuanceProvider` defined as ports with a **manual provider** as the only MVP implementation — the agent enters what they got from the airline portal. A GDS adapter slots in later without touching the booking model.
- **Depends on:** C3, C5, C2, C11.

### C7 — Billing & Payments
- **Owns:** invoices, credit notes, receipts, payment records (cash/bank/cheque/online, partial payments), supplier cost per booking, commission earned, per-booking margin, customer outstanding and AR ageing.
- **Explicitly not:** journals, trial balance, balance sheet. Those are v2. The MVP answers "who owes us what, and what did we make on this booking" — which is what the agency actually lacks today.
- **Depends on:** C6, C3, C2, C11.

### C8 — AI Assistant / Chatbot
- **Owns:** conversation state, knowledge base of agency FAQs and package information, LLM orchestration and prompt management, language detection (Nepali/English), structured extraction of trip details, confidence thresholds, human-handover triggers, conversation transcripts.
- **Boundary:** the chatbot **never writes directly to CRM tables**. It emits a structured lead payload to C4 and reads a small, explicitly permitted set of customer context. This keeps a probabilistic component from corrupting the system of record.
- **Depends on:** C9, C4.

### C9 — Messaging & Notification Gateway
- **Owns:** WhatsApp Business Cloud API integration (webhooks in, messages out, template management and approval status), transactional email, SMS, delivery status tracking, retry and dead-letter handling, template rendering in Nepali and English.
- **Provides:** a single send interface to C5, C6, C7, C8, C10.
- **Note:** WhatsApp's 24-hour customer-service window and pre-approved template rules constrain what can be sent when. This must be enforced in code, not left to agents.

### C10 — Scheduler & Background Jobs
- **Owns:** the job queue and scheduled work: follow-up reminders, quotation-expiry alerts, payment-due reminders, outbound message dispatch, report pre-computation, retries.
- **Depends on:** C1 (for acting as a system principal), C9.

### C11 — Document & File Storage
- **Owns:** file upload/download, storage abstraction, access authorisation per file, e-ticket attachment handling.
- **Sensitive:** passport scans live here. Encryption at rest and per-file authorisation are requirements, not enhancements.

### C12 — Reporting & Dashboards
- **Owns:** read-only aggregate queries and the dashboards over them: pipeline funnel and conversion, agent performance against target, revenue and margin by period/route/airline, AR ageing, enquiry volume by channel and hour, chatbot deflection rate.
- **Depends on:** read access to C4–C7.
- **MVP approach:** query the operational database with materialised summary tables for anything slow. No separate warehouse.

### Build order

```
Wave 1 (foundation)   C1 · C2 · C11 · C10
Wave 2 (core loop)    C3 · C5 · C6
Wave 3 (money)        C7
Wave 4 (channels)     C9 · C4 · C8
Wave 5 (visibility)   C12 + minimal HR (employee records, targets — folded into C1/C12)
```

C4 depends on C9, so the manual/web-form path into C5 is built in Wave 2 and the channel path lights up in Wave 4. The system is demonstrable and internally usable at the end of Wave 3.

---

## 4. Functional requirements

IDs are stable and should be referenced from the API and schema documents.

### FR-C1 · Identity, Access & Audit
- **FR-C1-01** Users authenticate with email/username and password; sessions expire and are refreshable.
- **FR-C1-02** Passwords are stored using a modern adaptive hash; reset is via a time-limited single-use token sent by email.
- **FR-C1-03** The system supports at minimum the roles: Admin, Manager, Sales Agent, Accountant, Ticketing Officer, Viewer. Roles are collections of permissions, not hard-coded checks.
- **FR-C1-04** Permissions are enforced per resource and per action (e.g. `invoice:create`, `booking:void`, `customer:export`).
- **FR-C1-05** An agent can see only leads and customers assigned to them, unless granted a wider scope; managers see their branch; admins see all.
- **FR-C1-06** Every create, update, delete and status transition on customer, lead, quotation, booking, invoice and payment records writes an audit entry containing actor, timestamp, entity, action and before/after values.
- **FR-C1-07** Audit entries are append-only and cannot be edited or deleted through any application interface.
- **FR-C1-08** Admins can deactivate a user; deactivation revokes sessions immediately and reassigns or flags that user's open records.

### FR-C2 · Master Data & Configuration
- **FR-C2-01** Maintain airlines, airports, countries, currencies and tax rates, with search by IATA code and by name.
- **FR-C2-02** Maintain exchange rates (NPR, USD, AED) with an effective date; rates are entered manually and the rate used is stamped onto each transaction.
- **FR-C2-03** Configure document numbering series per document type, with prefix, running number and fiscal-year reset. Numbers are gapless and never reused.
- **FR-C2-04** Maintain lead sources, service types, fee types and lost-reason codes.
- **FR-C2-05** Configure agency profile: legal name, address, PAN/VAT number, logo — used on all generated documents.

### FR-C3 · Customer & Traveller Master
- **FR-C3-01** Create, search and update customers, distinguished as individual or corporate.
- **FR-C3-02** Store multiple contact channels per customer (phone, WhatsApp number, email) with one marked primary per channel type.
- **FR-C3-03** Store traveller profiles with full name as per passport, date of birth, gender, nationality, passport number, issue and expiry dates.
- **FR-C3-04** Link travellers to a customer (family or corporate group) and to bookings independently.
- **FR-C3-05** Attach documents (passport scan, visa, photo) to a traveller.
- **FR-C3-06** Warn on probable duplicates during creation (matching phone, email or passport number) and allow an authorised user to merge two customer records, preserving history from both.
- **FR-C3-07** Display a full customer timeline: enquiries, quotations, bookings, invoices, payments and messages.
- **FR-C3-08** Passport numbers are masked in list views and visible in full only to permitted roles; every full view is audited.

### FR-C4 · Enquiry & Lead Intake
- **FR-C4-01** Capture enquiries from: WhatsApp, website chat widget, website contact form, manual entry (phone call or walk-in logged by an agent).
- **FR-C4-02** Every enquiry records its source channel and the raw inbound content.
- **FR-C4-03** Resolve the sender to an existing customer by phone/WhatsApp ID/email; if unresolved, create a provisional customer record.
- **FR-C4-04** If an open lead already exists for that customer on the same channel within a configurable window, append the message to that lead rather than creating a new one.
- **FR-C4-05** Assign new leads to an agent by configurable rule (round-robin, by channel, or unassigned queue) and allow manual reassignment.
- **FR-C4-06** Every lead is visible in a queue with age; unassigned and unanswered leads are visually flagged past an SLA threshold.
- **FR-C4-07** No enquiry can be silently dropped: intake failures are queued, retried and surfaced to an admin.

### FR-C5 · Sales Pipeline & Quotation
- **FR-C5-01** A lead moves through defined stages; every stage change is recorded with actor and timestamp.
- **FR-C5-02** Capture trip requirements: origin, destination, travel dates, passenger counts by type (adult/child/infant), trip type, service type (ticket / package / visa support), budget and notes.
- **FR-C5-03** Create a quotation with multiple line items (fare, taxes, service fee, other charges), quantity, unit price, currency and total.
- **FR-C5-04** Quotations have a validity date and support revisions; each revision is retained and the version sent to the customer is identifiable.
- **FR-C5-05** Generate a printable quotation view in the browser and send it to the customer by WhatsApp or email from within the system.
- **FR-C5-06** Record quotation outcome: accepted, rejected (with reason), or expired.
- **FR-C5-07** Schedule follow-up tasks against a lead with a due date and assignee; overdue tasks appear on the agent's dashboard and trigger a notification.
- **FR-C5-08** Automatic reminder to the owning agent when a quotation approaches expiry without a response.
- **FR-C5-09** Convert an accepted quotation into a booking, carrying customer, travellers, itinerary and pricing forward without re-entry.
- **FR-C5-10** Record a lost lead with a mandatory reason code.

### FR-C6 · Booking & Ticketing
- **FR-C6-01** Create a booking from a quotation or directly, with a unique booking reference.
- **FR-C6-02** Record passengers on the booking, selected from existing traveller profiles or created inline.
- **FR-C6-03** Record itinerary segments: airline, flight number, origin, destination, departure and arrival date/time, cabin class, baggage.
- **FR-C6-04** Record the airline PNR and, per passenger, the ticket number.
- **FR-C6-05** Record the fare breakdown per passenger: base fare, taxes, supplier/net cost, markup, service fee, total selling price, currency and exchange rate used.
- **FR-C6-06** Booking status lifecycle: draft → confirmed → ticketed → completed, with branches to cancelled and refunded. Transitions are validated (a booking cannot be ticketed before it is confirmed) and audited.
- **FR-C6-07** Attach the e-ticket file to the booking and send it to the customer by WhatsApp or email; the send is logged.
- **FR-C6-08** Record cancellations and refunds with reason, refund amount, airline penalty and agency service charge; the resulting financial effect flows to C7.
- **FR-C6-09** Record date changes and reissues as a linked child booking, preserving the original.
- **FR-C6-10** Fare search and ticket issuance are invoked through a provider interface. The MVP ships a manual provider; the contract must accommodate a future GDS provider without changing the booking data model.
- **FR-C6-11** Search bookings by PNR, ticket number, passenger name, customer, agent, airline and departure date range.

### FR-C7 · Billing & Payments
- **FR-C7-01** Generate an invoice from a booking, with line items derived from the booking pricing; invoices use the configured numbering series.
- **FR-C7-02** Support applicable tax/VAT lines on invoices per configured rate.
- **FR-C7-03** Issue a credit note against an invoice for cancellations, refunds and corrections; invoices are never edited after issue.
- **FR-C7-04** Record payments received against an invoice, including partial and multiple payments, with method, reference, date and currency.
- **FR-C7-05** Generate a numbered receipt view in the browser for each payment and send it to the customer.
- **FR-C7-06** Track invoice status: unpaid, partially paid, paid, overdue, credited.
- **FR-C7-07** Record supplier/airline cost and payable per booking.
- **FR-C7-08** Compute gross margin per booking as selling price minus supplier cost, and commission earned per booking and per airline.
- **FR-C7-09** Produce an accounts-receivable ageing report by customer with buckets (current, 30, 60, 90+).
- **FR-C7-10** Automatic payment reminders to customers with outstanding balances past due date, on a configurable schedule.
- **FR-C7-11** All monetary amounts store both the transaction currency amount and the base-currency (NPR) equivalent with the rate applied.

### FR-C8 · AI Assistant / Chatbot
- **FR-C8-01** Respond to inbound customer messages on WhatsApp and the website widget within seconds, 24/7.
- **FR-C8-02** Detect and reply in the customer's language (Nepali or English).
- **FR-C8-03** Answer from a maintained knowledge base: services offered, office hours, contact details, documents required, general process questions.
- **FR-C8-04** Collect structured trip details in conversation: destination, travel dates, passenger count, name and contact.
- **FR-C8-05** Emit a structured lead payload to C4 when sufficient detail is captured, or at the end of the conversation.
- **FR-C8-06** Hand over to a human when the customer asks, when confidence is low, or when the topic is outside the knowledge base — passing the full transcript to the agent.
- **FR-C8-07** Never quote a fare, confirm a price, or state a booking as confirmed. Pricing is an agent action.
- **FR-C8-08** Store every conversation transcript, searchable and linked to the customer record.
- **FR-C8-09** Admins can edit the knowledge base and the bot's greeting and tone without a code deployment.
- **FR-C8-10** A global kill switch disables the bot and routes all traffic to the human queue.

### FR-C9 · Messaging & Notification Gateway
- **FR-C9-01** Receive WhatsApp inbound messages via webhook, verify signatures, and deliver them to C4/C8.
- **FR-C9-02** Send WhatsApp messages, including approved template messages outside the 24-hour service window, and enforce that rule in code.
- **FR-C9-03** Send transactional email with attachments (quotation, invoice, receipt, e-ticket).
- **FR-C9-04** Send SMS as a fallback channel.
- **FR-C9-05** Maintain message templates with Nepali and English variants and named variables.
- **FR-C9-06** Record delivery status per outbound message (queued, sent, delivered, read, failed) and surface failures.
- **FR-C9-07** Retry transient failures with backoff; move permanent failures to a dead-letter queue visible to admins.
- **FR-C9-08** All inbound and outbound messages are linked to the customer and the related lead or booking.

### FR-C10 · Scheduler & Background Jobs
- **FR-C10-01** Execute scheduled jobs: follow-up reminders, quotation-expiry alerts, payment reminders, daily summary emails, report refresh.
- **FR-C10-02** Process asynchronous work: outbound messaging, chatbot calls.
- **FR-C10-03** Jobs are idempotent and retried with backoff on failure.
- **FR-C10-04** Admins can view job status, failures and retry history.

### FR-C11 · Document & File Storage
- **FR-C11-01** Upload files against a customer, traveller, lead, booking or invoice, with type and size validation.
- **FR-C11-02** Download is authorised per file according to the requester's permissions; direct object URLs are not publicly guessable and expire.
- **FR-C11-03** Generate PDFs for quotations, invoices, receipts and vouchers from templates carrying the agency's branding.
- **FR-C11-04** Scan uploaded files for malware before they are made available.
- **FR-C11-05** File deletions are soft; the audit trail retains the record of what existed.

### FR-C12 · Reporting, Dashboards & Minimal HR
- **FR-C12-01** Agent dashboard: my open leads, overdue follow-ups, quotations awaiting response, my bookings this month, my target vs. actual.
- **FR-C12-02** Manager dashboard: pipeline funnel with counts and conversion rate by stage, enquiries by channel, response-time distribution, revenue and margin for the period.
- **FR-C12-03** Sales report by agent, by period, by destination and by airline.
- **FR-C12-04** Financial summary: invoiced, collected, outstanding, margin, commission — for a selected period.
- **FR-C12-05** AR ageing report (shared with FR-C7-09).
- **FR-C12-06** Enquiry volume by hour of day and day of week — this validates or corrects the "43% after hours" claim with the client's real data.
- **FR-C12-07** Chatbot report: conversations handled, leads created, handover rate.
- **FR-C12-08** Export any report to CSV/Excel; exports are audited.
- **FR-C12-09** Employee records: personal details, designation, join date, branch, linked user account, documents.
- **FR-C12-10** Set a monthly sales target per agent and report actual against it, computed from bookings.

---

## 5. Non-functional requirements

### NFR-1 · Performance
- **NFR-1-01** 95th-percentile server response time under 500 ms for list and detail views at expected MVP load; under 1.5 s for report queries.
- **NFR-1-02** Chatbot first reply within 5 seconds of an inbound message.
- **NFR-1-03** Search across customers and bookings returns within 1 second at 100,000 records.
- **NFR-1-04** Long-running browser-side exports never block the main request path.
- **NFR-1-05** Expected MVP scale to design for: 30 concurrent internal users, 25,000 customers, 60,000 bookings, 500 inbound messages/day. Design for 10× headroom, do not build for 1000×.

### NFR-2 · Availability & Reliability
- **NFR-2-01** Target 99.5% monthly availability for the internal application during Nepal business hours.
- **NFR-2-02** The inbound message webhook endpoint must accept and durably queue messages even when downstream processing is degraded — a lost enquiry is the most expensive failure in the system.
- **NFR-2-03** No single background job failure may block the queue.
- **NFR-2-04** Planned maintenance windows outside 07:00–22:00 NPT.

### NFR-3 · Security
- **NFR-3-01** All traffic over TLS 1.2+; HTTP redirects to HTTPS.
- **NFR-3-02** Authorisation is enforced server-side on every endpoint. UI hiding is not access control.
- **NFR-3-03** Passport numbers, passport scans and payment references are encrypted at rest.
- **NFR-3-04** Secrets and API credentials are held in environment configuration or a secret store, never in source control.
- **NFR-3-05** Protection against OWASP Top 10: parameterised queries, output encoding, CSRF protection on session-based endpoints, rate limiting on authentication and public endpoints.
- **NFR-3-06** All uploads validated by type and size and stored outside the web root.
- **NFR-3-07** Webhook payloads from WhatsApp and payment providers are signature-verified.
- **NFR-3-08** Session tokens expire; refresh tokens are revocable and revoked on password change and deactivation.

### NFR-4 · Data protection & privacy
- **NFR-4-01** All customer, booking and financial data is the exclusive property of Global Gateway, exportable in full on request in a documented open format.
- **NFR-4-02** Passport and personal data access is restricted by role and logged.
- **NFR-4-03** Data retention policy defined per entity before go-live; transcripts and messages are retained for a defined period, not indefinitely by default.
- **NFR-4-04** Customer-facing chat states clearly that the assistant is automated.
- **NFR-4-05** Personal data is not sent to any third-party AI provider beyond what is necessary to answer the message; no passport or payment data is included in LLM prompts.

### NFR-5 · Auditability
- **NFR-5-01** Every financially significant record — booking, invoice, credit note, payment — carries an immutable audit history.
- **NFR-5-02** Issued invoices and receipts are immutable; corrections are made by credit note only.
- **NFR-5-03** Document numbers are gapless, sequential per series, and never reused, including under concurrent creation.

### NFR-6 · Backup & Recovery
- **NFR-6-01** Automated daily database backup with 30-day retention; file storage backed up on the same schedule.
- **NFR-6-02** Recovery Point Objective 24 hours; Recovery Time Objective 4 hours.
- **NFR-6-03** Restore procedure tested at least once before go-live and documented.

### NFR-7 · Usability & Localisation
- **NFR-7-01** Internal UI in English; all customer-facing messages, templates and documents available in Nepali and English.
- **NFR-7-02** Full UTF-8/Devanagari support across storage, search and messaging.
- **NFR-7-03** Dates displayed in a configured format; store in UTC, display in Asia/Kathmandu (UTC+05:45 — verify all libraries handle the 45-minute offset correctly).
- **NFR-7-04** Nepali (Bikram Sambat) date display is v2 unless the client requires it for invoices — confirm at kickoff, as it affects the schema.
- **NFR-7-05** Core agent workflows (view lead, log a call, send a quotation) usable on a mobile browser.
- **NFR-7-06** A new agent can be productive on lead-to-quotation after a 2-hour training session.

### NFR-8 · Maintainability & Extensibility
- **NFR-8-01** External integrations (messaging, GDS, payment, LLM) sit behind provider interfaces so a vendor can be swapped without touching business logic.
- **NFR-8-02** Automated test coverage on money calculations, document numbering, status transitions and permission checks is mandatory, whatever the coverage target elsewhere.
- **NFR-8-03** Database changes are applied via versioned, reversible migrations.
- **NFR-8-04** Structured application logging with correlation IDs across the request and its background jobs.
- **NFR-8-05** Full source code, migrations, deployment scripts and documentation transfer to the client on final payment, per the proposal.

### NFR-9 · Compliance & Third-party constraints
- **NFR-9-01** WhatsApp Business Platform policy compliance: opt-in, approved templates, 24-hour window, no unsolicited marketing.
- **NFR-9-02** Invoice format and tax fields conform to Nepali VAT/PAN requirements — **to be confirmed with the client's accountant during discovery**, as it constrains the invoice schema.
- **NFR-9-03** Third-party costs (WhatsApp conversation fees, LLM token usage, SMS, hosting, future GDS) are billed at actual and monitored with usage alerts.

---

## 6. Assumptions and open questions

These block or reshape the architecture and must be closed at the kickoff workshop.

1. **Does Global Gateway currently hold a GDS contract or IATA accreditation?** If yes, the ticketing module changes materially and certification timelines must be planned.
2. **Which WhatsApp number becomes the Business API number?** Migrating a number to the Cloud API removes it from the WhatsApp mobile app — this is a business decision, not a technical one.
3. **Who is the Meta Business account owner,** and is the business verified? Verification can take weeks and gates the chatbot.
4. **What are the exact VAT/PAN invoice requirements** the agency's accountant needs? Determines invoice fields and numbering.
5. **Is Bikram Sambat dating required on customer-facing documents?**
6. **Is there existing customer data to migrate,** and in what form? Migration is a separate work item, not part of the build estimate.
7. **Which currencies are actually transacted in,** and who sets the exchange rate used for booking?
8. **Are payments ever taken online,** or is it all cash/bank transfer? An online payment gateway would add a component.
9. **The 52 hours/week and 43% after-hours figures are estimates in the proposal.** Baseline them in week 1; FR-C12-06 exists to replace them with measured data.
10. **Where is the system hosted** — local Nepali provider, or cloud region? Affects latency, cost and any data-residency expectation.

---

## 7. MVP acceptance criteria

The MVP is complete when, in a live environment with real staff accounts:

1. A WhatsApp message from an unknown number produces an automated reply and a lead in the CRM within one minute, with no human involvement.
2. An agent opens that lead, sees the full conversation, adds trip details, and sends a quotation from a printable browser view without leaving the system.
3. The quotation converts to a booking; the agent records the PNR, ticket numbers and fare breakdown, and sends the e-ticket to the customer from the system.
4. An invoice is generated from the booking, a partial payment is recorded, a receipt is sent, and the remaining balance shows in the AR ageing report.
5. A manager opens a dashboard and sees the funnel, the agent's target vs. actual, and the margin on that booking — without asking anyone.
6. An accountant cannot see HR data; an agent cannot see another agent's leads; every one of the above actions appears in the audit trail with the correct actor.
7. A restore from backup into a clean environment reproduces all of the above data.

---

## 8. Next deliverables

| Deliverable | Depends on | Key decisions it must settle |
|---|---|---|
| **Architecture Design** | Sections 3, 5, 6 | Modular monolith vs. services; tech stack; hosting and deployment topology; queue and cache choice; provider-interface boundaries; tenancy and branch model. |
| **Schema Design** | Sections 3, 4 | Customer/traveller separation; booking–passenger–segment–ticket structure; money representation (minor units, currency, rate stamping); document numbering under concurrency; audit table design; soft deletes. |
| **API Design** | Architecture + Schema | Resource model and versioning; auth and permission scopes; webhook contracts for WhatsApp; provider interfaces for fare search and issuance; pagination, filtering and error format; idempotency keys on financial endpoints. |

Recommended order: Schema and Architecture in parallel, API after both. Money representation and document numbering are the two schema decisions most expensive to change later — settle them first.
