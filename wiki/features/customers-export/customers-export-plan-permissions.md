---
type: feature
nav_path: "Customers → Export customers → Plan & permissions"
route_name: admin.core.export
route_path: /admin/api/core/export-import/export_customers
aliases: ["Customer export plan gate", "Customer export permissions", "customer_export feature", "Customer export side effects", "Customer export API alternative", "Експорт на клиенти — права и план"]
tags: [customers, export, plan-gated, permissions, api]
plan_gates: ["customer_export"]
created: 2026-06-10
updated: 2026-06-10
source_count: 4
---

> Part of [[customers-export]]. See the hub for the other aspects (trigger & 2FA, filter scope, sync vs async, CSV schema).

# Export customers — plan & permissions

## Purpose

This aspect covers **who is allowed to run a customer export and what the platform records when they do**: the `customer_export` plan feature, the staff permission grants, the audit side-effects, the categories of data the export deliberately omits, and the JSON-API v2 alternative for live integrations.

## Where to find it

Plan eligibility is managed under the store's subscription plan ([[plan-gates]]); staff permission grants are managed under Settings → Staff ([[settings-staff]]). Both gate the **Export customers** button on the Customers list ([[customers]], [[customers-export-trigger-2fa]]).

## What the merchant can do here

- Run the export when their plan includes `customer_export` AND their staff role has the export grant.
- Pull the same read data programmatically via JSON-API v2 for system-to-system integrations (see below).

### What the merchant CANNOT do here

- Run the export on a plan without `customer_export` — the button shows but raises an upgrade modal.
- Run the export as a moderator without the `customers.export` grant — the button is hidden.
- Export multiple addresses, order history, marketing-engagement data, authentication artifacts, or soft-deleted customers (see Business rules).

## Settings & fields

### Plan feature `customer_export` gates the action

The Export customers action is plan-gated. Stores on plans without the `customer_export` feature see the button in the UI, but clicking it surfaces an upgrade prompt instead of launching the 2FA modal.

### Permissions

The export requires the `customers`, `customers.all`, `customers.export` permission grants. The export action is mapped to the permission set `[customers, customers.all, customers.export]`. Moderators ([[settings-staff]]) without the export grant do not see the button.

## Business rules

### What the export does NOT include

- **Multiple addresses per customer** — only the **default shipping address** fields are exported (see [[customers-export-csv-schema]]). Customers with multiple addresses get one row. To export all addresses, use the API (below).
- **Order history** — order metadata is NOT in the CSV. Use [[settings-import-history]] / report exports for order data.
- **Marketing engagement / open / click data** — none of this is in the customer export. Marketing analytics live in the Marketing module.
- **Password hashes, reset tokens, or other authentication artifacts** — never exported.
- **Soft-deleted customers** — only live records.

### Side effects

- A `CC2FaTasks` log row is created with `action = export_customers` and `status = pending`, then promoted to `verified` after the code is validated (see [[customers-export-trigger-2fa]]).
- The platform records the export request in the admin's activity log (for audit purposes).
- No webhook fires on export.
- No customer record is modified by the export.

## Programmatic access

For programmatic READ access to the customer list (the common export-style use case — pulling customers into a CRM, BI tool, or external analytics platform), use **JSON-API v2** — see [[api-customers]] for the list-customers endpoint with filter / pagination / sort support. Related read resources: [[api-customer-groups]], [[api-customer-shipping-address]], [[api-customer-billing-address]], [[api-customer-tags]].

**JSON-API v2 is for live integrations, NOT one-shot CSV downloads.** The Export customers action produces a single CSV file via the 2FA-gated background-job pipeline (with the UTF-8 BOM, queued chunking into 10 000-row part files for large exports — see [[customers-export-sync-vs-async]]). The API path is fundamentally different: paginated JSON pages, no 2FA, rate-limited per token, no CSV format. Pick the right tool — CSV for a periodic data dump the merchant uses in Excel; API for a system-to-system integration.

**API returns ALL addresses per customer; the CSV export only returns the DEFAULT shipping address fields.** If your integration needs every customer address, you MUST go through the API. The CSV export collapses each customer to one row.

**Same data scope** — the API never exposes password hashes, reset tokens, or saved-payment tokens. The `customer_export` plan feature gates the CSV action specifically; API read access is gated by the standard `customers` plan grants instead (verify per [[json-api-v2]]).

See [[json-api-v2]] for authentication, rate limit, and the side-effects principle.

## Related

- [[customers-export]] — hub.
- [[plan-gates]] — `customer_export` is a plan-gated feature.
- [[settings-staff]] — moderator permission grants for the Customers export.
- [[settings-import-history]] — sibling concept (imports rather than exports), useful for orders / products data.
- [[api-customers]] — JSON-API v2 list-customers endpoint (the API alternative).
- [[api-customer-groups]] / [[api-customer-shipping-address]] / [[api-customer-billing-address]] / [[api-customer-tags]] — related API read resources.
- [[json-api-v2]] — API authentication, rate limits, and side-effect principles.

## Open questions

(All resolved.)
