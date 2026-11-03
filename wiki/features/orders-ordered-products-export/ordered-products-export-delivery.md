---
type: feature
nav_path: "Orders → Ordered Products → Export → Delivery"
route_name: admin.core.export
route_path: /admin/api/core/export-import/export_orders_products
aliases: ["Ordered Products export download", "Products by orders export email", "Aggregated product export notification", "Order products export file retention", "Ordered Products export archive folder"]
tags: [orders, products, export, csv, delivery, notifications, files]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 4
---

> Part of [[orders-ordered-products-export]]. See the hub for related aspects (trigger / 2FA, CSV schema, sync vs async, filter scope, permissions / plan).

# Ordered Products export — delivery

## Purpose

Documents **how the finished export reaches the merchant** — direct browser download for small pivots, email + in-app alert for large async pivots — plus the notification toggles that gate the email, where the file is stored, the encoding that lets Excel open it cleanly, and file retention.

## Where to find it

- **Synchronous result**: downloads directly in the browser the moment the export completes.
- **Asynchronous result**: arrives as an email with a download link, plus an in-app alert in the notification bell, plus the file in [[settings-files]] → Archive folder.

The path is decided by row count — see [[ordered-products-export-sync-vs-async]].

## What the merchant can do here

- Download the file directly (sync) or via the emailed link / in-app alert / Files page (async).
- Re-download an async export later from [[settings-files]] (the file persists).

The merchant CANNOT re-download a synchronous export after the browser download (it is not stored), and cannot rely on the email alone if notifications are disabled (the in-app alert and Files page remain).

## Settings & fields

### Email notification gating (async)

The "your file is ready" email respects two per-merchant toggles on [[settings-admin-notifications]]:

| Setting | Required value | Effect when off |
|---------|----------------|-----------------|
| `administrator_email_notifications` | `yes` (global toggle) | No admin emails at all. |
| `mail_file_download` | `yes` (per-event toggle) | No "file ready" email for this export. |

If either is off, the file is still generated and uploaded — but no email goes out. The merchant uses the in-app alert or visits [[settings-files]] manually.

## Business rules

### Synchronous vs asynchronous delivery

- **Synchronous (≤ 50 rows)**: builds the CSV in memory, returns rows to the browser, browser downloads. Not stored server-side.
- **Asynchronous (> 50 rows)**: queues a background batch on `export6`; the final step bundles the parts into a ZIP and emails the download link. See [[ordered-products-export-sync-vs-async]].

### In-app alert ALWAYS fires (independent of email)

When the ZIP is ready, the platform creates an in-app success alert in the notification bell with both a direct download link and a link to the file in [[settings-files]]. The alert appears **even if the email notification is disabled** — so a merchant who turned off `mail_file_download` still gets notified in-app.

### UTF-8 BOM + CRLF on the asynchronous CSV

The async (queued) CSV writer prepends the UTF-8 BOM bytes (EF BB BF) and uses CRLF (`\r\n`) line endings on every row including the header. Both ensure Excel-on-Windows opens the file in UTF-8 mode without character corruption (Bulgarian / Cyrillic / accented characters survive). The synchronous browser-built CSV path may handle encoding client-side; Excel-import behaviour is consistent for the more common async file. The column layout itself is in [[ordered-products-export-csv-schema]].

### Archive stored in `files/archive/`

The bundled ZIP is stored under the merchant's site folder at `/{site_id}/files/archive/` on S3-compatible storage with `mime=application/zip`. Merchants find it in [[settings-files]] → Archive folder. There is **no platform-side scheduled purge** — merchants delete manually to reclaim storage quota. File retention matches [[orders-export-delivery]]: Filemanager-stored, CDN URL persists indefinitely.

## Related

- [[orders-ordered-products-export]] — hub.
- [[ordered-products-export-sync-vs-async]] — which path (sync download vs async email) is chosen.
- [[ordered-products-export-csv-schema]] — the column layout inside the delivered file.
- [[orders-export-delivery]] — the orders export equivalent (same notification gating + retention).
- [[settings-admin-notifications]] — `administrator_email_notifications` + `mail_file_download` toggles.
- [[settings-files]] — Archive folder where the async ZIP lands.
- [[settings-queue-view]] — async job status while the file is being built.

## Open questions

None.
