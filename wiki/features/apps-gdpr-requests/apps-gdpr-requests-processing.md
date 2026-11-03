---
type: feature
nav_path: "Apps → GDPR → Requests → Processing"
route_name: apps.gdpr.requests
route_path: /admin/apps/gdpr/requests
aliases: ["GDPR request processing", "Processing a data subject request", "Erasure scope", "30-day GDPR deadline", "Right to erasure retention", "GDPR portability format", "Anonymise customer GDPR"]
tags: [apps, gdpr, compliance, requests, workflow]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 4
---
# GDPR → Requests: processing workflow

> Part of [[apps-gdpr-requests]]. See the hub for the other aspects (types & channels, data model).

## Purpose

This aspect documents the **merchant's operational workflow** for resolving a data subject request and the legal / safety rules that bound it. It covers the 30-day response window (and the absence of any built-in deadline indicator), identity verification, the true scope of erasure under legal retention, the manual anonymisation step on the customer record (with no rollback), the portability export format, the side effect of each request type, the lack of any customer-side status notification, and the missing type-filter dropdown in the admin list.

## Where to find it

The merchant processes requests from the admin Requests tab (`/admin/apps/gdpr/requests` — see [[apps-gdpr-requests]]). The actual data actions — anonymising fields, generating an export, correcting a record — are performed on the related customer record via [[customers-details]], not inside the GDPR app's own UI.

## What the merchant can do here

- Read each request's type and message, then perform the matching action (export, anonymise, unsubscribe).
- Mark the request **processed** once the action is complete (sets `processed_at` — see [[apps-gdpr-requests-data-model]]).
- Respond to the customer **directly by email** using the email captured on the request, since the platform sends no automatic status update.

What the merchant **cannot** do here: see an overdue badge, undo an anonymisation, filter the list by type via a dropdown, or fully delete records the merchant is legally required to retain.

## Settings & fields

### Side effects per request type

| Request type | Side effects |
|---|---|
| `info` (Access) | Generate a customer-data export; no DB change. |
| `download` (Portability) | Generate a machine-readable export. |
| `delete` (Erasure) | Anonymise personal fields on the customer record + related (addresses, etc.); retain financial / audit records. |
| `marketing_unsubscribe` | Remove the customer from marketing; no deletion. |

### No built-in 30-day deadline indicator

The only timestamps stored are `created_at` and `processed_at` (see [[apps-gdpr-requests-data-model]]). There is no deadline field, no "overdue" badge, no countdown, and no alert when 30 days approach. **The merchant must track GDPR's 30-day response window manually** by watching the `created_at` column.

### No type-filter dropdown in the admin list

The admin search runs a `LIKE` match against `email`, `type`, and the joined customer fields (`email`, `first_name`, `last_name`). There is no curated "filter by type" dropdown — to filter by type the merchant must type the type slug (`info`, `download`, `delete`, `marketing_unsubscribe`) into the search bar.

## Business rules

### 30-day response window

GDPR requires the merchant to respond within ONE MONTH (extendable to 3 months for complex requests). Because the platform surfaces no overdue indicator, the merchant must self-monitor against `created_at`.

### Identity verification

Before processing Erasure / Access requests, the merchant SHOULD verify the requester is genuinely the data subject (e.g., the customer is logged in as them, or has confirmed their email). Otherwise an attacker could submit fake requests to weaponise the right-to-erasure against the merchant's customers.

### Erasure scope — retention overrides full deletion

Right-to-erasure does NOT mean deleting ALL data. The merchant retains:

- Financial / tax records (per local commerce law, typically 5–10 years).
- Audit-required records (e.g., the [[apps-gdpr-acceptance]] consent log, anonymised).
- Records under legal hold (active disputes / litigation).

Erasure typically means anonymising the customer's personal identifiers (name, email, phone, address → "Deleted customer") while keeping the financial / audit trail intact. [[orders]] are normally retained under financial retention even after erasure.

### Erasure has no rollback / grace period

There is no automated customer-erase action the GDPR Requests page calls, and no soft-delete / grace-period mechanism. The merchant marks a `delete` request processed (sets `processed_at`) but the actual anonymisation is done manually on [[customers-details]]. **Once the merchant manually anonymises the fields, there is no built-in undo** — recovery would require database backups outside the GDPR app's UI.

### Portability format

Right-to-portability requires the export to be in a **structured, commonly-used, machine-readable format** (JSON / CSV / XML). The merchant generates this export.

### No customer-side notification on status change

There is no event that fires when `processed_at` is set, no email template for status updates, and no notification integration triggered by marking a request processed. When the merchant resolves a request, the customer does NOT receive an automatic update — **the merchant must respond directly by email** using the captured email address.

### Customer cannot track their request status from the storefront

The storefront customer GDPR page (`/gdpr`) lets the customer SUBMIT a request but does NOT list previously-submitted requests or show their status. **Status tracking is admin-only** — customers cannot see whether their request is open or processed from their account page.

## Related

- [[apps-gdpr-requests]] — hub.
- [[apps-gdpr-requests-data-model]] — the `processed_at` flag the merchant sets to close a request (referenced inline above).
- [[apps-gdpr-requests-types-channels]] — the request types whose side effects are tabled above.
- [[customers-details]] — where the merchant performs the actual anonymisation / correction (referenced inline above).
- [[apps-gdpr-acceptance]] — consent log retained (anonymised) through erasure.
- [[orders]] — retained under financial retention even after erasure.

## Open questions

None.
