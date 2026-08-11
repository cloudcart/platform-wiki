---
type: feature
nav_path: "Analytics → Products by traffic → Export & cache"
route_name: analytics
route_path: /admin/analytics
aliases: ["Products by traffic export", "Products by traffic CSV", "Products by traffic 2FA export", "Продукти спрямо посещения — експорт"]
tags: [analytics, ccanalytics, products, traffic, top-products-by-traffic, export]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 8
---
> Part of [[analytics-top-products-by-traffic]]. See the hub for the other aspects (UI surface, data source / attribution).

# Products by traffic — export & cache

## Purpose

Documents how the merchant gets the Products-by-traffic data **out of the dashboard** as a CSV file — the Export link, the optional comparison-data modal, the 2FA gate, the asynchronous queue + email delivery, and the row caps that can block an export. It also covers the 60-second client-side cache that makes toggling the date / compare controls feel instant.

## Where to find it

The **Export** control (cloud-download icon) sits in the top-right toolbar of the Details and ViewMore screens at `/admin/analytics/details/top-products-by-traffic` (and `/extended/{product_id}`). It is **not** present on the dashboard box — export is a Details / ViewMore action only. Completed exports land in [[settings-import-history]].

## What the merchant can do here

- Export the current Details or ViewMore table to CSV.
- Optionally include comparison-period data as a second CSV file.
- Confirm the export with a 2FA code (when 2FA is enabled on the account).
- Receive a download link by email once the queued job finishes.

## What the merchant sees

### Export flow (modal / 2FA / queue)

1. Merchant clicks **Export** (cloud-download icon).
2. **If compare = `no`** → goes straight to the 2FA gate. **If compare ≠ `no`** → opens the **ExportModal** first.
3. **ExportModal** ([[analytics-details]] shared component): title *"Export your report"*, body *"Report will be exported as a CSV (comma separated values) table."* + checkbox *"Include comparison data (separate csv file)"*. Buttons **Export** / **Cancel**.
4. **CC2FaAction modal** ([[account-cc2fa]]): if the staff member has 2FA enabled (email or TOTP), the modal asks for the 6-digit code. If 2FA is disabled on the account, the request is auto-submitted with code `cc` and no modal is shown.
5. The POST to `/admin/api/import-export/{action}` (action = `export_analytics`) places the export onto the dedicated analytics-export queue and immediately returns `{ type: "queue" }`.
6. Toast: *"The export is being processed. You will receive an email with the download link."*
7. The actual CSV writing happens asynchronously; the merchant is emailed when ready and the file appears in [[settings-import-history]].

### Client-side 60-second cache

The dashboard box caches its response under `${routeName}.${boxKey}.${dateFrom}.${dateTo}.${compare}` for 60 seconds — so toggling Compare back-and-forth doesn't refetch. The cache invalidates when the merchant changes date or compare, or when `cacheHash` changes (e.g., after Settings → Analytics is saved).

## Settings & fields

The export flow is governed by backend permissions, plan features, and fixed row caps rather than merchant-editable settings:

| Control | Value / gate | Meaning |
|---------|--------------|---------|
| Export availability | `allowExport` (perm `reports.reports_export`) | Hidden when the staff member lacks the export permission; hidden during loading. |
| 2FA gate | account 2FA on/off | 6-digit code when on; auto-code `cc` when off. |
| Export queue | Dedicated analytics-export queue | Async processing; email delivery. |
| Export row cap | `150 000` rows per file (`CcAnalyticsConfig.export.limit`) | Hard cap on a single CSV file. |
| Comparison data | "Include comparison data" checkbox | Produces two CSV files (current + previous), delivered together. |

## Business rules

### Export row cap

Export queue limit: **150 000 rows per file** (`CcAnalyticsConfig.export.limit`). If the table currently shows more than that, the Export link is disabled with toast *"The generate request contains the {total} row. The maximum number of rows to export is {limit}"*.

### Comparison data = two files

If the merchant ticks "Include comparison data" and exports, the job produces **two CSV files** (current + previous period) — both delivered together. The job-permission gate is `reports.reports_export`.

### Force-limit interaction

The on-screen table is itself capped at `DETAILS_FORCE_LIMIT = 1000` rows; when that cap is hit the yellow banner steers the merchant to Export to get the complete data (export is unpaginated, subject only to the 150 000-row cap). The force-limit mechanics live on [[analytics-top-products-traffic-data-source]]; the banner UI is on [[analytics-top-products-traffic-ui]].

## Related

- [[analytics-top-products-by-traffic]] — hub.
- [[analytics-top-products-traffic-ui]] — the Export link in the toolbar + the force-limit banner.
- [[analytics-top-products-traffic-data-source]] — the unpaginated export queries + the 1000-row force-limit.
- [[analytics-details]] — shared ExportModal component.
- [[account-cc2fa]] — the 2FA gate component.
- [[settings-import-history]] — where finished exports appear.

## Open questions

_None._
