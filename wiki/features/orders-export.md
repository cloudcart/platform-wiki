---
type: feature
nav_path: "Orders → Export"
route_name: admin.core.export
route_path: /admin/api/core/export-import/export_orders
aliases: ["Orders export", "Export orders", "Export to CSV", "Bulk order export", "Експорт на поръчки", "Износ на поръчки"]
tags: [orders, export, csv, 2fa, async, smarty]
plan_gates: ["export_orders"]
created: 2026-05-23
updated: 2026-06-10
source_count: 10
---

# Orders export

## Purpose

The **Export** button on the [[orders]] list page — produces a CSV file with all orders matching the current filter scope. Used for accounting feeds, business-intelligence imports, end-of-period reports, and CRM data exports.

The export respects every filter the merchant has applied to the orders list — exporting the SAME rows the merchant currently sees. With no filters, it covers the full order history (chunked + asynchronous). This is the **canonical bulk orders export**; there is no separate per-order or selection-based variant from this surface — the merchant filters down to the desired scope, then clicks Export.

This concept is split into 6 aspect pages — drill into the one that matches the question rather than reading the cluster end-to-end.

## Sub-pages (in this cluster)

- [[orders-export-trigger-2fa]] — the Export button + the 2FA email / TOTP modal flow, expiry windows, conditional `2fa_email` flag, CC2FaTasks tokens, `extra` payload sanitisation.
- [[orders-export-sync-vs-async]] — the 50-order threshold; chunk / limit parameters (default `500` / `50`, validated range `1`–`1000`); queue `export6`; inner `chunkById` of 250; rapid-click no-dedup behaviour.
- [[orders-export-csv-schema]] — fixed column list (46+ columns), multi-row layout (one row per line item), product-option ghost rows, language-translated headers, UTF-8 BOM + CRLF on async files, date / currency formatting per merchant.
- [[orders-export-delivery]] — sync browser download, async email + in-app alert, notification gating (`administrator_email_notifications` + `mail_file_download`), file retention (no auto-purge), Filemanager storage in `files/archive/`, partial-completion behaviour on failure.
- [[orders-export-filter-scope]] — filter captured at click time; archived-orders handling; no selection-based export; SQL-snapshot consistency for async chunks.
- [[orders-export-permissions-plan]] — staff permission grant (`orders.export`); the `export_orders` plan-feature mapping (registered but NOT effective because the URL pattern mismatches the live route); per-admin 2FA configuration drives whether the modal appears.

## Where to find it

From [[orders]] → top-right header → **Export** button (white outline style).

The button opens a two-factor authentication modal (when 2FA email is active for the merchant or the admin has TOTP configured) before the export proceeds. Once verified, the export runs. The modal is bypassed entirely when the platform `2fa_email` flag is OFF and the admin has no `cc2fa_secret` set.

## What the merchant can do here

- Trigger the export — see [[orders-export-trigger-2fa]] for the 2FA modal flow.
- Receive the result — see [[orders-export-delivery]] for sync vs async delivery, email, and in-app alert.
- Narrow scope by filter — see [[orders-export-filter-scope]] for filter capture and the no-selection rule.

### What the merchant CANNOT do here

- Pick custom columns from this UI — the export uses a fixed canonical schema. See [[orders-export-csv-schema]].
- Choose between CSV / XLSX / XML — only CSV is produced.
- Export specific selected orders by checkbox — the export uses the FILTER scope, not row selection. See [[orders-export-filter-scope]].
- Skip 2FA when the modal is in play — see [[orders-export-trigger-2fa]].
- Cancel a running async export job from this UI — it runs to completion.
- Re-download a previously generated export from the button — the email link / Files page is the only retrieval surface. See [[orders-export-delivery]].

## Settings & fields

The Export action itself has no merchant-facing settings on this surface — it consumes filters from the orders list and runs against fixed platform parameters. Each aspect documents its own settings:

| Surface | Settings / fields documented in |
|---|---|
| Chunk / limit thresholds (`500` / `50`) | [[orders-export-sync-vs-async]] |
| 2FA expiry windows (60 min email, 2 min TOTP) | [[orders-export-trigger-2fa]] |
| Staff permission grants (`orders.export`) | [[orders-export-permissions-plan]] |
| Plan-feature mapping (`export_orders`) | [[orders-export-permissions-plan]] |
| Notification gating (`administrator_email_notifications`, `mail_file_download`) | [[orders-export-delivery]] |
| CSV column schema (46+ columns) | [[orders-export-csv-schema]] |

## Business rules

- **Export respects the current filter scope.** Captured at click time. See [[orders-export-filter-scope]].
- **Async threshold — 50 orders.** Above 50 the export goes async automatically; the merchant cannot force sync mode. See [[orders-export-sync-vs-async]].
- **Email delivery — required for async.** Result is delivered ONLY by email link (plus in-app alert). See [[orders-export-delivery]].
- **2FA is per-admin.** Modal appears based on the admin's configured 2FA, not the store's. See [[orders-export-trigger-2fa]].
- **Single format — CSV only.** No XLSX / XML / JSON option. See [[orders-export-csv-schema]].
- **Not effectively plan-gated.** The `export_orders` plan-feature mapping is registered but its URL pattern does not match the live route. See [[orders-export-permissions-plan]].
- **Staff permission required.** `orders` + `orders.all` + `orders.export` grants. See [[orders-export-permissions-plan]].

## Related

- [[orders]] — parent list (the Export button lives here).
- [[orders-invoices-export]] — separate CSV export of invoices.
- [[orders-invoices-download]] — bulk PDF download of invoices.
- [[orders-ordered-products-export]] — alternative cross-order product-pivot CSV export.
- [[orders-user-files]] — separate page for customer-attached files.
- [[settings-staff]] — `orders.export` permission grant.
- [[settings-queue-view]] — async job status for large exports.
- [[settings-files]] — where the async ZIP lands (Archive folder).
- [[settings-admin-notifications]] — `mail_file_download` toggle for "your file is ready" emails.
- [[order]] — entity page (the exported records).
- [[background-queue-inventory]] — catalogue of all background processes; covers when an orders export switches from synchronous to queued and how to track it.
- [[plan-gates]] / [[plan-vs-feature-pack]] / [[plan-features]] — plan-feature framework (the `export_orders` mapping is documented in [[orders-export-permissions-plan]]).

## Open questions

(All resolved.)
