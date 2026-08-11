---
type: feature
nav_path: "Customers → Export customers"
route_name: admin.core.export
route_path: /admin/api/core/export-import/export_customers
aliases: ["Export customers", "Customer export", "CSV export", "Download customer list", "Експорт на клиенти", "Сваляне на клиенти", "Експортиране на клиенти"]
tags: [customers, export, csv, 2fa, plan-gated]
plan_gates: ["customer_export"]
created: 2026-05-23
updated: 2026-06-10
source_count: 7
---

# Export customers

## Purpose

The **Export customers** action lets the merchant download their customer list as a CSV file. It is **not a standalone page in the sidebar** — it is launched from the **header of the Customers list** ([[customers]]) via the **Export customers** button. The download is **gated by two-factor authentication** (admin must enter a 2FA code) and **gated by plan feature** (`customer_export`).

The exported CSV reflects the current filter state of the Customers list: if the merchant has applied filters (active, banned, marketing, tag, group, country, state), only matching customers are exported. For small result sets the file is generated synchronously and returned in the response; for larger sets the platform falls back to a background job delivered through the **Queue jobs** page ([[settings-queue-view]]).

This concept is split into 5 aspect pages — drill into the one that matches the question rather than reading the cluster end-to-end.

## Sub-pages (in this cluster)

- [[customers-export-trigger-2fa]] — the Export button location, the mandatory 2FA modal flow, TOTP vs email code expiry windows, the "fresh code per export" rule, and the no-bypass requirement.
- [[customers-export-filter-scope]] — how the export inherits the Customers-list filters, the Vue → legacy filter-key remapping, and the pagination / sort stripping.
- [[customers-export-sync-vs-async]] — the 5 000-row synchronous threshold, the `csv` vs `queue` response shapes, the 10 000-row queue chunking, and the multi-part file delivery for large exports.
- [[customers-export-csv-schema]] — the fixed 19-column layout + appended custom-field columns, the Phone fallback chain, the store-currency conversion of "Total Spent", and the UTF-8 BOM difference between sync and queued files.
- [[customers-export-plan-permissions]] — the `customer_export` plan gate, the `customers.export` permission grant, what the export does NOT include, the audit side-effects, and the JSON-API v2 alternative for live integrations.

## Where to find it

Sidebar → **Customers** → click **Export customers** in the page header (top-right, next to **Import** and **+ Add customer**). The action is exposed through the Customer hub's header — it is NOT a dedicated route. See [[customers-export-trigger-2fa]] for the button + 2FA modal.

## What the merchant can do here

- Trigger an export from the Customers list header — see [[customers-export-trigger-2fa]] for the 2FA modal flow.
- Narrow the exported set by applying list filters before clicking — see [[customers-export-filter-scope]].
- Receive a direct download (small sets) or a queued file (large sets) — see [[customers-export-sync-vs-async]].

### What the merchant CANNOT do here

- Pick which columns to export — the column set is fixed. See [[customers-export-csv-schema]].
- Export specific selected customers by checkbox — the export uses the FILTER scope. See [[customers-export-filter-scope]].
- Choose the export format — CSV only. See [[customers-export-csv-schema]].
- Skip the 2FA modal — every export requires a fresh code. See [[customers-export-trigger-2fa]].
- Export across multiple stores at once, export deleted customers, or schedule recurring exports — see [[customers-export-plan-permissions]].

## Settings & fields

The Export action itself has no merchant-facing settings on this surface — it consumes filters from the Customers list and runs against fixed platform parameters. Each aspect documents its own settings:

| Surface | Settings / fields documented in |
|---|---|
| 2FA code expiry windows (2 min TOTP / 60 min email) | [[customers-export-trigger-2fa]] |
| Filter-key remapping (`accept_marketing` → `marketing`, etc.) | [[customers-export-filter-scope]] |
| Synchronous limit (5 000) + queue chunk size (10 000) | [[customers-export-sync-vs-async]] |
| Fixed CSV column list (19 + custom fields) | [[customers-export-csv-schema]] |
| `customer_export` plan gate + `customers.export` permission | [[customers-export-plan-permissions]] |

## Business rules

- **Every export needs a fresh 2FA code.** No "remember this device" option. See [[customers-export-trigger-2fa]].
- **Export respects the current filter scope.** Captured at click time; pagination / sort are stripped. See [[customers-export-filter-scope]].
- **Synchronous threshold — 5 000 rows.** Above it the export goes to a background job; the merchant cannot force sync mode. See [[customers-export-sync-vs-async]].
- **Large exports arrive as multiple part files.** A 60 000-row export delivers six `part_N.csv` files, not one. See [[customers-export-sync-vs-async]].
- **Sync and queued files open differently in Excel.** Only the queued path prepends the UTF-8 BOM. See [[customers-export-csv-schema]].
- **Plan-gated by `customer_export`.** Without it the button surfaces an upgrade prompt. See [[customers-export-plan-permissions]].
- **Default shipping address only.** Customers with multiple addresses collapse to one row. See [[customers-export-csv-schema]].

## Related

- [[customers]] — the parent list page that hosts the **Export customers** button in its header.
- [[customers-import]] — the inverse operation (bulk-add customers from CSV).
- [[customers-custom-fields]] — definitions of custom fields included as extra columns in the export.
- [[customers-custom-groups]] — group names appear in the `Customer Group` column.
- [[customers-details]] — per-customer detail page (the export aggregates these fields per customer).
- [[account-cc2fa]] — authenticator-app 2FA setup; required to authorise exports.
- [[account-cc2fa-email]] — email fallback for 2FA.
- [[settings-queue-view]] — where queued large exports complete and become downloadable.
- [[settings-import-history]] — sibling concept (imports rather than exports).
- [[settings-staff]] — moderator permission grants for the Customers export.
- [[plan-gates]] — `customer_export` is a plan-gated feature.
- [[background-queue-inventory]] — catalogue of all background processes; covers when a customer export switches from synchronous to queued.
- [[json-api-v2]] / [[api-customers]] — the API alternative for live integrations.

## Open questions

(All resolved.)
