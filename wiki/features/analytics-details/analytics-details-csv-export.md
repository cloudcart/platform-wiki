---
type: feature
nav_path: "Analytics → Details → CSV Export"
route_name: analytics.details.subView
route_path: /admin/analytics/details/:box/:id
aliases: ["Details export", "Analytics CSV export", "Export report", "Export with comparison", "Експорт на отчет", "Export modal"]
tags: [ccanalytics, analytics, details, export, csv]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 9
---
# Details — CSV Export

> Part of [[analytics-details]]. See the hub for the drill-level model and the other aspects (chart & compare, grouping & dates, access & limits).

## Purpose

This aspect covers the **Export** action on the Details screen — how the merchant turns the on-screen table into a downloadable CSV, the compare-aware Export modal, the 2FA gate, the async delivery channel, and the row-count and concurrency limits that can block an export.

## Where to find it

Analytics dashboard → **View details** on a box → the **Export** link (cloud-download icon) at the top-right of the Details screen. Present on the first-level Details, the sub-view, and the [[analytics-full]] view-more table.

## What the merchant can do here

- Export the current table as a **plain CSV** file.
- When Compare is active, choose whether to **include comparison data** (a second CSV for the previous period).
- Receive the file through the standard async export channel after a 2FA confirmation.

## Settings & fields

| Field / Control | What it does | Default | Validation / notes |
|-----------------|--------------|---------|--------------------|
| Export link | Starts the export flow. | Visible only when `allowExport: true` and not currently loading. | Permission-gated on `reports.reports_export` — see [[analytics-details-access-limits]]. |
| "Include comparison data (separate csv file)" | Export modal checkbox (compare only). | Unchecked. | When checked, the job writes TWO CSV files (current + previous). |

## Business rules

### When the Export link shows

The Export link is only rendered when:

- The backend returned `allowExport: true` (computed from the merchant's `reports` / `reports.reports_export` permission).
- The merchant is not currently loading data.

### Export modal (Compare = period / year only)

When `compare !== 'no'`, the Export link does NOT trigger 2FA immediately. Instead it opens the **Export modal** (`ExportModal.vue`) — a small dialog with:

- **Modal title**: "Export your report" (EN) / Bulgarian equivalent. May be overridden by box.
- **Body line 1**: "Report will be exported as a CSV (comma separated values) table."
- **Body checkbox**: ☐ "Include comparison data (separate csv file)" — checked = export job writes TWO CSV files (current period + previous period); unchecked = only the current period.
- **Footer button "Export"** (cloud-download icon) — submits the choice, then opens the `CC2FaAction` modal that gates the actual job enqueue with 2FA.
- **Footer button "Cancel"** (red) — closes the modal without enqueueing.

When `compare === 'no'`, the Export link skips the modal entirely and goes straight to the `CC2FaAction` modal (no choice — only the current period to export).

### `CC2FaAction` modal

A 2-factor confirmation modal shared across the platform. For analytics exports it carries the `action: "export_analytics"` flag plus props containing `dateFrom`, `dateTo`, `compare`, `group`, `view` (details / sub_details / view_more / more_details), `box`, `record`, and `export` (= "currently" or "currently,previous"). On successful 2FA the export job is enqueued on the `export7` queue; the merchant sees the toast *"Your file will be generated shortly. You will be notified when it is ready!"*. The file is delivered through the standard async export channel ([[settings-import-history]] / file-asset notification). See [[account-cc2fa]] for the 2FA flow itself.

### Row-count cap

There is a hard cap of **150,000 rows per export** (the Analytics `export.limit` config). If the table holds more rows than that, the Export button shows a tooltip — *"The generate request contains the {total} row. The maximum number of rows to export is {limit}"* — and refuses to start.

### Force-limit alert

If the backend caps the table at the platform code rows (some pipelines do this for performance — e.g., the landing-pages and top-categories-from-products joins), the table shows a yellow alert above the data: *"This report shows up to {total} results. To see all results, you can [Export]"*. The merchant must export to see the full set.

### CSV-only (no XLSX)

The Export link produces a **plain CSV** file using the streaming writer. There is no XLSX option here despite some legacy docs mentioning Excel. When Compare is `period` or `year` and the merchant opts to include comparison data, the job writes **two separate CSV files** (one current, one previous) — NOT a zipped pair or a multi-sheet workbook. Each file's name is suffixed with the date range it covers and `currently` / `previous`.

### One active export per box

The export endpoint refuses a second request for the same box while the first is still queued / running: response is *"You already have a request for this file. Please wait for it to be generated."* (HTTP 400). The lock is keyed by box id, NOT by view (details vs viewMore vs subDetails). So a merchant who exports Top Products by Sales **details** cannot start a Top Products by Sales **view-more** export until the first finishes.

## Related

- [[analytics-details]] — hub.
- [[account-cc2fa]] — the 2FA confirmation flow behind every export.
- [[settings-import-history]] — the async file-delivery / notification channel.
- [[settings-staff]] — `reports.reports_export` permission that unlocks Export.
- [[analytics-full]] — the view-more table that shares the same box-keyed export lock.

## Open questions

_None._
