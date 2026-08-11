---
type: feature
nav_path: "Orders → Ordered Products → Export"
route_name: admin.core.export
route_path: /admin/api/core/export-import/export_orders_products
aliases: ["Ordered Products export", "Products by orders export", "Order products CSV", "Aggregated product export", "Експорт на поръчани продукти", "Износ на продукти по поръчки"]
tags: [orders, products, export, csv, 2fa, async]
plan_gates: ["export_orders"]
created: 2026-05-23
updated: 2026-06-10
source_count: 9
---
# Ordered Products export

## Purpose

The **Export** button on the [[orders-ordered-products]] page — produces a CSV file of the cross-order product pivot (every product / variant + aggregated quantities + order ID list + supplier info when applicable). Used by merchants for:

- Spreadsheet-based restocking analysis.
- Purchase-order generation (data feed for supplier negotiations).
- Inventory planning based on demand-by-variant.
- Bulk data extraction for ERP / accounting integration.
- Sales-by-SKU reporting outside the platform's built-in analytics.

The export respects every filter applied to the Ordered Products page (date range, status, supplier, property option) — exporting the SAME pivot the merchant currently sees. This is distinct from the per-order [[orders-export]] (one row per order line) — here each row is a product / variant aggregated across all matching orders.

This concept is split into 6 aspect pages — drill into the one that matches the question rather than reading the cluster end-to-end.

## Sub-pages (in this cluster)

- [[ordered-products-export-trigger-2fa]] — the Export button, where it lives, the shared 2FA email / TOTP modal, expiry windows, conditional `2fa_email` flag, the `cc.ajax.success` response routing by `type`.
- [[ordered-products-export-csv-schema]] — fixed 10-column pivot schema + 3 Suppliers-app columns, one row per variant × options, supplier-column rename by filter, quantity normalisation, order IDs `;`-separated, header translation / currency.
- [[ordered-products-export-sync-vs-async]] — 50-row sync threshold; chunk parameter (`1000`, validated `1`–`1000`); queue `export6`; inner `chunkById` of 250; click-time SQL snapshot; ZIP assembly on S3; filename patterns.
- [[ordered-products-export-filter-scope]] — filter captured at click time; status-filter recommendation; empty / unbounded scope warning; fresh aggregation re-run at export time; page-export parity.
- [[ordered-products-export-delivery]] — sync browser download vs async email + in-app alert; notification gating (`administrator_email_notifications` + `mail_file_download`); file retention; Archive folder storage in `files/archive/`.
- [[ordered-products-export-permissions-plan]] — staff permission grants (`products_by_orders.export`); the `export_orders` plan-feature mapping nuance; legacy `OrderProductsNewExport` job alias.

## Where to find it

From [[orders-ordered-products]] → top-right header → **Export** button (primary blue). The button opens a 2FA confirmation modal (when 2FA email is active) before the export proceeds. See [[ordered-products-export-trigger-2fa]].

## What the merchant can do here

- Trigger the export after applying filters — see [[ordered-products-export-trigger-2fa]].
- Receive the result (sync download or async email) — see [[ordered-products-export-delivery]].
- Narrow scope by filter on the parent pivot page — see [[ordered-products-export-filter-scope]].

### What the merchant CANNOT do here

- Pick the column set / format from the UI — the schema is fixed (CSV-only). See [[ordered-products-export-csv-schema]].
- Export a per-row selection — there are no checkboxes on the parent pivot; the export uses the filter scope. See [[ordered-products-export-filter-scope]].
- Skip 2FA when 2FA email is active. See [[ordered-products-export-trigger-2fa]].
- Choose XLSX / XML output — CSV only.
- Resume / cancel a running async job.

## Settings & fields

The Export action has no merchant-facing settings on this surface — it consumes filters from the pivot page and runs against fixed platform parameters. Each aspect documents its own settings:

| Surface | Settings / fields documented in |
|---|---|
| Chunk / limit thresholds (`1000` / `50`) | [[ordered-products-export-sync-vs-async]] |
| 2FA expiry windows (60 min email, 2 min TOTP) | [[ordered-products-export-trigger-2fa]] |
| Staff permission grants (`products_by_orders.export`) | [[ordered-products-export-permissions-plan]] |
| Plan-feature mapping (`export_orders`) | [[ordered-products-export-permissions-plan]] |
| Notification gating (`administrator_email_notifications`, `mail_file_download`) | [[ordered-products-export-delivery]] |
| CSV column schema (10 / 13 columns) | [[ordered-products-export-csv-schema]] |

## Business rules

- **Export respects the current filter scope.** Captured at click time. See [[ordered-products-export-filter-scope]].
- **Async threshold — 50 product rows.** Above 50 the export goes async automatically with `chunk=1000` per job. See [[ordered-products-export-sync-vs-async]].
- **One row per variant.** Product X (Red, M) and Product X (Red, L) are separate rows with separate quantities. See [[ordered-products-export-csv-schema]].
- **Suppliers app changes the schema.** 10 columns without the app, 13 with it. See [[ordered-products-export-csv-schema]].
- **Status filter strongly recommended.** The pivot includes all statuses by default — cancelled / refunded inflate demand if not filtered out. See [[ordered-products-export-filter-scope]].
- **Result delivered by email for async.** Plus an in-app alert that always fires. See [[ordered-products-export-delivery]].
- **Staff permission required.** `orders` + `products_by_orders.all` + `products_by_orders.export`. See [[ordered-products-export-permissions-plan]].

## Plan gates

This feature is gated by the `export_orders` plan-feature — the same boolean access gate that controls [[orders-export]]. A verbatim `export_orders_products` mapping is NOT registered separately, so a merchant who has `export_orders` in their plan can use BOTH exports, and a merchant without it has neither button. Full nuance (boolean gate, no feature-pack extension, the staff-permission layer that gates the action regardless of plan) is in [[ordered-products-export-permissions-plan]]. When the gate is hit, the merchant is redirected to [[plan-features]] for the per-feature upsell ([[plan-gates]] / [[plan-vs-feature-pack]]).

## Related

- [[orders-ordered-products]] — parent pivot page (the Export button lives here).
- [[orders-supplier-products]] — Suppliers-app focused version of the same pivot.
- [[orders-export]] — orders export (per-order rows, different schema).
- [[orders-invoices-export]] — invoices export (different scope).
- [[orders]] — orders list (the source data).
- [[orders-details]] — clicking order IDs in the pivot opens there.
- [[products-property]] — properties + options used in the pivot's Property-option filter.
- [[apps]] — Suppliers app changes column schema.
- [[settings-statuses]] — status taxonomy used by the status filter.
- [[settings-staff]] — `products_by_orders.export` permission grant.
- [[settings-queue-view]] — async job status for large exports.
- [[order]] — entity page.
- [[product]] — entity page.

## Open questions

(none — manually-added lines DO appear, variant text uses in-cell product-editor formatting, removed-after-placement lines are excluded once the line is deleted, and file retention matches [[orders-export]] — Filemanager-stored, CDN URL persists indefinitely.)
