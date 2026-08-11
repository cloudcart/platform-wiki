---
type: feature
nav_path: "Analytics → Full → CSV Export"
route_name: analytics.viewMore
route_path: /admin/analytics/full/:box/:record
aliases: ["View more export", "Full list CSV export", "view_more export", "Export modal view more", "Експорт на пълния списък"]
tags: [ccanalytics, analytics, full, view-more, export, csv]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 8
---
# Full — CSV export

> Part of [[analytics-full]]. See the hub for the drill model and the other aspects (available boxes, chart & pagination).

## Purpose

This aspect covers the **Export** action on the View more full list — how the merchant turns the on-screen table into a downloadable CSV, the compare-aware Export modal, the 2FA gate, the async delivery channel, the `view: view_more` request flag, and the row-count and concurrency limits. The flow is identical to [[analytics-details]]'s export, differing only in the `view` marker carried with the request.

## Where to find it

The full list screen at `/admin/analytics/full/:box/:record` → the **Export** link (cloud-download icon) at the top-right.

## What the merchant can do here

- Export the current full-list table as a **plain CSV** file.
- When Compare is active, choose whether to **include comparison data** (a second CSV for the previous period).
- Receive the file through the standard async export channel after a 2FA confirmation.

## Settings & fields

| Field / Control | What it does | Default | Validation / notes |
|-----------------|--------------|---------|--------------------|
| Export link | Starts the export flow. | Visible only when `allowExport: true` and not currently loading. | Permission-gated on `reports.reports_export`. |
| "Include comparison data (separate csv file)" | Export modal checkbox (compare only). | Unchecked. | When checked, the job writes TWO CSV files (current + previous). |

## Business rules

### When the Export link shows

The Export button only renders when `allowExport: true` (server-evaluated `reports.reports_export` permission) AND the screen is not loading.

### Export modal (Compare = period / year only)

If `compare !== 'no'`, the Export link opens the **Export modal** (`ExportModal.vue`) — title "Export your report", body line "Report will be exported as a CSV (comma separated values) table.", checkbox "Include comparison data (separate csv file)", footer buttons "Export" (cloud-download icon) + "Cancel". On Export → opens the `CC2FaAction` modal next. If `compare === 'no'`, the modal is skipped — the Export link opens `CC2FaAction` directly.

### `CC2FaAction` gate and async delivery

All exports go through the `CC2FaAction` two-factor confirmation modal (`action: "export_analytics"`, full date / compare / group / view / box / record props). On successful 2FA the export is enqueued; the merchant sees the toast *"Your file will be generated shortly. You will be notified when it is ready!"* and the file arrives through the standard async export channel ([[settings-import-history]] / file-asset notification). See [[account-cc2fa]] for the 2FA flow itself.

### Export of View more uses the `view: view_more` flag

The exported CSV name and audit trail mark the request as `view: view_more` (versus `details` from [[analytics-details]] or `more_details` from [[analytics-more-details]] or `sub_details` from a sub-view). The export query also carries the `box`, the `record`, and the current date / compare / group. If the merchant ticked "Include comparison data", the `export` prop becomes `"currently,previous"` (two CSV files); otherwise `"currently"` (one CSV).

### Row-count cap

Hard cap at **150,000 rows** (the Analytics admin `export.limit` config). Over that, the export button is disabled with a tooltip showing the actual row count vs limit.

### One active export per box

The export endpoint refuses a second request for the same box while the first is still queued / running: response is *"You already have a request for this file. Please wait for it to be generated."* (HTTP 400). The lock is keyed by box id, NOT by view — so a merchant who exports Top Products by Sales **details** cannot start a Top Products by Sales **view-more** export until the first finishes (and vice versa). See [[analytics-details]] for the same shared lock.

### Permission

Reaching `/admin/analytics/full/:box/:record` at all requires `hasApiPermission:reports,reports.reports`. Export adds the `reports.reports_export` requirement on top.

## Related

- [[analytics-full]] — hub.
- [[analytics-details]] — shares the identical export flow and the box-keyed export lock.
- [[analytics-more-details]] — third-level drill; its export carries `view: more_details`.
- [[account-cc2fa]] — the 2FA confirmation flow behind every export.
- [[settings-import-history]] — the async file-delivery / notification channel.
- [[settings-staff]] — `reports.reports` / `reports.reports_export` permissions.

## Open questions

_None._
