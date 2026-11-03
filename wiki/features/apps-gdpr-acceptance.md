---
type: feature
nav_path: "Apps → GDPR → Acceptance"
route_name: apps.gdpr.acceptance
route_path: /admin/apps/gdpr/acceptance
aliases: ["GDPR Acceptance", "Policy acceptance log", "Consent log", "Acceptance audit"]
tags: [apps, gdpr, compliance, acceptance, audit, log]
plan_gates: []
created: 2026-05-21
updated: 2026-06-10
source_count: 7
---
# GDPR → Acceptance

## Purpose

The **Acceptance** tab is the **append-only audit log of policy + consent acceptances** by customers. Every time a customer checks "I accept the Privacy Policy" at checkout, registration, or any consent-collection point, a row is written here recording who accepted, which policy (and exactly which version of its text), when, and from where (IP + device). This is the merchant's **GDPR audit trail**: if a regulator or the customer asks "did this person agree to X?", the log is the evidence. Records cannot be edited or deleted from the UI, and the **Export** is 2FA-gated.

For overall GDPR coverage, see [[apps-gdpr-overview]].

## Where to find it

Sidebar → Apps → GDPR → **Acceptance tab**. Route: `/admin/apps/gdpr/acceptance`. The data table uses `app-name="gdpr_acceptance"` for table state.

## What the merchant can do here

- **View records** — standard data table (filter, sort, paginate). **Search is restricted to email only** (other columns are filter columns, not free-text). Click a row to open the per-row modal (`AcceptedPolicyModal`), which fetches `GET /api/gdpr/acceptance/view/{log_id}` and shows the **exact HTML text the customer accepted** — even after the merchant later rewrites the policy.
- **Export the log** — **Export** button (icon `far fa-arrow-from-bottom`) in the table's additional-buttons slot. It opens a 2FA modal (`CC2FaAction`, action key `export_gdpr`); the merchant enters their current 2FA code (TOTP / email — see [[account-cc2fa]]) and the file downloads. See *Export* under Settings & fields.

The merchant **cannot** edit or delete records (immutable for audit — even Right-to-Erasure only anonymises PII rather than removing the row), and cannot export without 2FA.

## Settings & fields

### On-screen columns

| Field | Notes |
|---|---|
| **Title** (`title`) | Policy title that was accepted. |
| **Client / Customer** (`customer`) | Who accepted. |
| **Created** (`created_at_formatted`) | When the row was inserted. |
| **Updated** (`updated_at_formatted`) | Last-touched timestamp. |
| **Form** (`form`) | Which form captured the consent. |

The `ip` and `user_agent` values are stored on every row but their **list-view columns are commented out** in the component — they are NOT visible on screen. To inspect IP / device, use the Export.

### Stored per-row data

The log row holds: `customer_id` (null for guests), `email` (lower-cased, trimmed — always set, even for guests), `content_id` (references the snapshotted policy `title` + `content`), `form`, `ip`, and `user_agent` (shown as **Device**). The `form` value is one of: `register`, `contacts`, `submit_payment`, `segment_subscription_popup`, `policies_popup`, `mailchimp_newsletter`.

### Export format

The Export produces an **Excel (.xlsx)** file named `policy-acceptance-log-{YYYY-MM-DD-HH-MM-SS}.xlsx` (timestamped so exports never collide) with these 10 fixed columns:

| Column | Source |
|---|---|
| ID | Acceptance log row ID. |
| Customer ID | Linked customer (blank for guests). |
| Customer Name | From the customer record (blank for guests / anonymised). |
| Customer Phone | First non-empty of: shipping-address phone → billing-address phone → customer `alternative_phone` (blank for guests). |
| Customer Email | Email stored at acceptance time (always present). |
| Policy Title | Title from the snapshotted policy content. |
| Created At | First recorded (`YYYY-MM-DD HH:MM:SS`). |
| Updated At | Last touched. |
| Device | User-agent captured at acceptance. |
| Source | The `form` that captured the acceptance. |

For large logs (over 500 records by default, configurable via the 2FA task's `limit`), the Export runs as a background queue task (`generate_by_sql`, type `GdprAcceptanceExport`, chunk size 500): the merchant gets a "queued" response and the file appears in their downloads list when ready. Smaller logs export immediately.

## Business rules

### Immutable, append-only, retained indefinitely

Rows cannot be edited or deleted via the UI, and there is **no automated pruning** — acceptance records persist for the life of the store. This matches GDPR's "ability to demonstrate compliance" requirement (Article 5(2)).

### Policy text is snapshotted (content-hashed)

On acceptance the platform snapshots the policy's CURRENT name + content (keyed by a hash of name + content), not just a policy id. So the log always shows **exactly what the customer agreed to at the moment they agreed**, even after the merchant edits the wording. When the merchant edits a policy, future acceptances reference a NEW snapshot; past acceptances keep the OLD one.

### De-dup by (customer, email, content snapshot, form)

Re-accepting the SAME policy text via the SAME form **updates the existing row** (timestamp refresh), not a new row. A new row is written only when the policy text changes (new snapshot) — so a customer who accepted the old version and later hits a form gets a second row alongside the first; both are kept (acceptance history per snapshot, not just "last acceptance").

### When the log is written

Logging happens in middleware **after** the response is sent: when the request carries a `gdpr` or `terms` array AND the form response was OK, the platform iterates the policy IDs and writes/updates rows. The `form` name is derived from the active route: `site.newsletter.subscribe` → `mailchimp_newsletter`; `subscribers.subscriptions.form.store` (POST) → `segment_subscription_popup`; `checkout.payment.submit` → `submit_payment`; `contacts` → `contacts`; `site.gdpr.policies-popup` → `policies_popup`; default → `register`.

### Marketing-policy consent toggles `customers.marketing`

When the merchant designates a policy as the marketing policy (`marketing_policy` setting), accepting/rejecting it ALSO writes `customer.marketing = yes/no` and fires a `CustomerMarketingChange` event (the write is wrapped in `retry(5, …, 500ms)` to survive concurrent updates). Subscriber-list, mail-marketing, and customer-tag integrations listen for this. See [[apps-gdpr-requests]] / marketing apps.

### Right-to-Erasure does NOT clear the log

There is no action or listener that removes log rows when a customer is anonymised. The **fact** that consent existed at time T is the audit evidence and is retained; only the linked customer name/phone may become null when the customer record itself is anonymised. Erasure is handled in [[apps-gdpr-requests]].

### 2FA-gated Export + permission

Export requires 2FA because the log contains personal data — bypassing it would itself be a GDPR violation. Standard apps permission scope applies, and the admin must have 2FA active ([[account-cc2fa]]) to export. No customer notification fires on export.

### Customers do NOT see their own acceptance log

The acceptance log is **admin-only**. The storefront customer GDPR page (`/gdpr`) lets a customer edit details ([[customers-details]]), download their data ([[apps-gdpr-overview]]), and file Right-to-Information / Right-to-Erasure requests — but it does NOT list which policies they accepted or when.

## Related

- [[apps-gdpr-overview]] — GDPR hub.
- [[apps-gdpr-policy]] — policies whose acceptances are logged here.
- [[apps-gdpr-cookies]] — cookie consent state (separate flow).
- [[apps-gdpr-requests]] — customer-data requests (right-to-erasure flow interacts with this log).
- [[account-cc2fa]] — 2FA required for Export.
- [[customers-details]] — customer self-edit linked from the storefront `/gdpr` page.

## Open questions

- Whether a higher-level audit log records who exported the acceptance log and when (verify).
