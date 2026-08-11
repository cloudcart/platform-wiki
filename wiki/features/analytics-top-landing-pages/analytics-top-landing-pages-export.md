---
type: feature
nav_path: "Analytics → Landing pages by visits → Export"
route_name: analytics
route_path: /admin/analytics
aliases: ["Landing pages by visits export", "Landing pages CSV export", "Export landing-page traffic", "Landing pages report cache", "Целеви страници — експорт"]
tags: [analytics, ccanalytics, landing-pages, traffic, top-landing-pages, export]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 7
---

> Part of [[analytics-top-landing-pages]]. See the hub for the other aspects (UI surface, data source / attribution).

# Landing pages by visits — export & cache

## Purpose

Documents how the merchant exports **Landing pages by visits** data to CSV (the modal, the 2FA step, the async queue, the row cap) and the 60-second client-side cache on the dashboard box. The data being exported is defined in [[analytics-top-landing-pages-data-source]]; the on-screen tables are in [[analytics-top-landing-pages-ui]].

## Where to find it

On the **Details** or **ViewMore** screen of the Landing pages by visits box, the **Export** link sits at the top-right of the toolbar (cloud-download icon). It is hidden when `allowExport: false` (permission `reports.reports_export`).

## What the merchant can do here

- Export the full Details table (every viewed page in the period) as CSV.
- Export a single page's ViewMore time-series as CSV.
- Optionally include a separate comparison-period CSV when a compare period is selected.
- Receive the finished file by email and re-download it from [[settings-import-history]].

## Settings & fields

### Export flow (modal / 2FA / queue)

1. Click **Export** → ExportModal opens with an *"Include comparison data (separate csv file)"* checkbox when compare ≠ `no`; otherwise it goes straight to the 2FA step.
2. **CC2FaAction modal** ([[account-cc2fa]]) — 6-digit code; auto-submits `cc` if 2FA is off on the account.
3. POST `/admin/api/import-export/export_analytics` → queue `export7` → toast *"The export is being processed. You will receive an email with the download link."*
4. The async export writes the CSV(s); the merchant gets an email; the file is available in [[settings-import-history]].

### Export caps

| Cap | Value | Effect |
|-----|-------|--------|
| Export row limit | **150 000 rows** | The async export will not write more than this many rows. |
| ViewMore force-limit | `DETAILS_FORCE_LIMIT = 1000` | On-screen ViewMore is capped at 1000 intervals; the force-limit banner steers the merchant to Export to see the rest. |

### Client-side 60-second cache

The dashboard box caches its result under the key `${routeName}.${boxKey}.${dateFrom}.${dateTo}.${compare}` for **60 seconds**. Re-rendering the dashboard with the same date range / compare selection within 60 seconds reads the cached payload instead of re-querying. Changing any part of the key (date range, compare mode) bypasses the cache.

## Business rules

- **Export requires the `reports.reports_export` permission** — staff without it never see the Export link.
- **Export is gated behind 2FA** — the CC2FaAction modal always runs; it auto-submits the literal code `cc` only when 2FA is disabled on the account, so the merchant is not blocked.
- **Export is asynchronous** — it does not download in-browser; the merchant must wait for the email or check [[settings-import-history]]. This is why large reports (capped at 150 000 rows) do not time out the browser.
- **Comparison data is a separate file** — when compare ≠ `no` and the checkbox is ticked, the comparison period is written as its own CSV, not merged into the primary file.

## Related

- [[analytics-top-landing-pages]] — hub.
- [[analytics-top-landing-pages-ui]] — the toolbar that hosts the Export link.
- [[analytics-top-landing-pages-data-source]] — what data the export contains.
- [[account-cc2fa]] — the 2FA modal in the export flow.
- [[settings-import-history]] — where the finished CSV(s) land.
- [[analytics]] — parent hub.

## Open questions

_None._
