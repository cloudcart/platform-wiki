---
type: feature
nav_path: "Analytics → Products by sales → Export & cache"
route_name: analytics
route_path: /admin/analytics
aliases: ["Products by sales export", "Products by sales CSV export", "Products by sales 2FA export", "Products by sales cache", "Продукти по продажби — експорт"]
tags: [analytics, ccanalytics, orders, products, top-order-products-by-sales, export]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 9
---
> Part of [[analytics-top-order-products-by-sales]]. See the hub for the other aspects (UI surface, status filter, data source).

# Products by sales — export & cache

## Purpose

Documents the **CSV export flow** for the "Products by sales" Details / ViewMore tables — the Export link, the optional comparison-data choice, the 2FA gate, the asynchronous queue, the email delivery, and the row cap — plus the 60-second client-side cache that the dashboard box uses to avoid refetching.

## Where to find it

The **Export** link sits top-right of the Details and ViewMore toolbars (only when the merchant has the export permission). Completed exports land in [[settings-import-history]]. The cache is invisible — it just makes repeated period/compare toggles feel instant.

## What the merchant can do here

- Export the full (unpaginated) Details or ViewMore table to CSV.
- Optionally include a second CSV with the comparison-period data when a comparison is active.
- Receive the file by email and download it from Import history.

## What the merchant sees

1. Click **Export**.
2. If a comparison is active, the **ExportModal** opens first with a checkbox *"Include comparison data (separate csv file)"*. If comparison = `no`, the modal is skipped and the flow goes straight to 2FA.
3. The **CC2FaAction modal** ([[account-cc2fa]]) asks for a 6-digit code (email or TOTP). If 2FA is disabled on the account, the request auto-submits with code `cc` and no modal appears.
4. A toast confirms: *"The export is being processed. You will receive an email with the download link."*
5. The merchant gets an email with the download link when the file is ready; the file also appears in [[settings-import-history]].

## Settings & fields

| Key | Value | Meaning |
|-----|-------|---------|
| `allowExport` | from perm `reports.reports_export` | When false, the Export link is hidden entirely. |
| `CcAnalyticsConfig.export.limit` | 150 000 | Max rows an export job will produce. |
| `CcAnalyticsConfig.compare_range` | 12 months | How far back the date picker (and thus export) can reach. |

## Business rules

### Export is asynchronous and queued

The POST to `/admin/api/import-export/export_analytics` enqueues the job onto queue `export7` and responds `{ type: "queue" }`. The job builds the CSV (or two CSVs if comparison data was requested) and emails the merchant when ready. The export uses the **unpaginated** Details / ViewMore pipeline, so it bypasses the 1000-product Details force-limit described in [[analytics-top-order-products-sales-data-source]] (the force-limit applies only when the pipeline's limit is numeric, which the export path is not).

### Export row cap — 150 000 rows

The export queue limit is **150 000 rows** (`CcAnalyticsConfig.export.limit`). If the table holds more rows than that, Export shows a toast and refuses to start. (Most stores stay well under this; it mainly affects very wide ViewMore exports over long ranges.)

### Permission gate

The Export link only renders when the merchant's role includes `reports.reports_export` (`allowExport: true`). Without it, the data is still viewable on screen but cannot be exported.

### Client-side 60-second cache

The dashboard box caches its response under the key `${routeName}.${boxKey}.${dateFrom}.${dateTo}.${compare}` for 60 seconds. Toggling Compare back and forth within that window does **not** trigger a refetch. The cache invalidates when the range/compare changes to a new key, or when `cacheHash` updates (e.g. after a Settings → Analytics save). This is a read-side performance cache only — it does not affect what statuses count (see [[analytics-top-order-products-sales-status-filter]]).

## Related

- [[analytics-top-order-products-by-sales]] — hub.
- [[analytics-top-order-products-sales-data-source]] — the unpaginated pipeline the export reuses + the force-limit it bypasses.
- [[analytics-top-order-products-sales-ui]] — the toolbar where the Export link lives.
- [[account-cc2fa]] — the 2FA modal in the export flow.
- [[settings-import-history]] — where completed export files land.

## Open questions

_None._
