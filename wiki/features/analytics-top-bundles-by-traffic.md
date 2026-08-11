---
type: feature
nav_path: "Analytics → Bundles by traffic"
route_name: analytics
route_path: /admin/analytics
aliases: ["Bundles by traffic", "Top bundles by traffic", "Top viewed bundles", "Most visited bundles", "Бъндъли спрямо посещения", "Топ бъндъли по трафик"]
tags: [analytics, ccanalytics, products, bundles, traffic, top-bundles-by-traffic]
plan_gates: []
created: 2026-05-22
updated: 2026-06-10
source_count: 7
---
# Bundles by traffic

## Purpose

Same as [[analytics-top-products-by-traffic]] but **restricted to bundle products** (product `type = bundle`). Shows which bundles attract the most product-page visits — useful for checking whether a new bundle is getting organic discovery, and (alongside [[analytics-top-order-bundles-by-sales]]) whether that traffic converts into sales. A bundle page renders like any product page (one URL, one `viewProduct` event), so traffic accounting is identical to the regular box; only the bundle-type filter differs.

Tooltip: *"Top bundles depend on visits in your online store."* (BG not registered — falls back to EN.)

## Where to find it

Analytics dashboard → **Bundles by traffic** box. `navigationSort: 11` (sits beside the parent products box). Box `key: "top-bundles-by-traffic"`, `type: "table"` — a top-5 ranked table with per-row mobile/desktop tooltips. Clicking the box opens Details; clicking a bundle row drills into a per-date chart (ViewMore).

`collectDataFrom` is **not set**, so the front-end enforces no minimum date — any range is allowed and the backend returns zero if no bundle existed yet. Bundles predate 2023, so this is safe.

## What the merchant can do here

- See the top 5 most-viewed bundles (mobile/desktop split) on the dashboard.
- Open **Details** (click the box title) — a paginated table of every bundle viewed in the period; filter by specific bundle ids.
- Drill into **ViewMore** (click a row) — a per-date traffic chart for that single bundle.
- Change the **date range** (page-level picker, re-fetches) and **compare** against the previous period.
- Export Details / ViewMore data as CSV.

## What the merchant sees

### Dashboard box (top 5)

| Element | What it is |
|---------|------------|
| Title row | EN: "Bundles by traffic" (no BG registered — shows EN even in Bulgarian locale) |
| Each top-5 row | Bundle name (linked), `meta.row1` units chip ("Units {value}"), `meta.row4` views chip ("Views {value}"), per-device split tooltip |
| Row sort / limit | Total views DESC, top 5 |

### Details screen (full table)

Columns (EN labels; no BG registered — all fall back to EN):

| Column key | EN label |
|------------|----------|
| `product_name` | Name |
| `views` | Views / Sessions |
| `orders` | Orders |
| `quantity` | Units |
| `amount` | Amount |
| `conversion_rate` | Conversion rate |

Default sort: `views` DESC, then `sales` DESC. Page size: 100. `details.group = false` (one row per bundle). Column formatters are **reused** from [[analytics-top-order-products-by-units-sold]] (same as [[analytics-top-products-by-traffic]]) — links, number formatting, and conversion-rate cells render identically.

### ViewMore (per-bundle over time)

Clicking a bundle row in Details opens a per-date breakdown for that single bundle (columns: Date / Views/Sessions / Orders / Amount / Units / Conversion rate, same as [[analytics-top-products-by-traffic]]). `hasViewMoreChart: true` — a purple-filled area chart of views per period. Tooltip (EN): *"{count} view for {date}|{count} views for {date}"*.

### Details / ViewMore toolbar (every UI control)

| Control | What it does | Plan / config gate |
|---------|--------------|----------------------|
| **Date range picker** | Re-fetches. | Capped by `cc_analytics.compare_range` (default 12 months). |
| **Compare select** | `No comparison` / `Previous period` / `Previous year`. | `cc_analytics.allow_period_compare`. Always rendered. |
| **Group select** | `Hourly` / `Daily` / `Weekly` / `Monthly` / `Quarterly` / `Yearly` / `None`. ViewMore only (Details forces `details.group: false`). | **Hourly hidden if range > 7 days**, **Daily hidden if range > 90 days**. |
| **Export link** | Triggers ExportModal + 2FA flow. | Hidden when `allowExport: false` (perm `reports.reports_export`). |
| **Force-limit banner** | *"This report shows up to {total} results. To see all results, you can [Export]"* | Fires when ViewMore is capped at 1000 rows. |

Traffic boxes have **no status-filter alert** (no order data). The dashboard box itself does NOT show date / compare / group / export controls — those are page-wide.

### Export flow (modal / 2FA / queue)

1. Click **Export** → ExportModal with *"Include comparison data (separate csv file)"* checkbox when compare ≠ `no`; else straight to 2FA.
2. **CC2FaAction modal** ([[account-cc2fa]]) — 6-digit code (email/TOTP); auto-submits `cc` if 2FA is off.
3. POST `/admin/api/import-export/export_analytics` → queue `export7` → toast *"The export is being processed. You will receive an email with the download link."*
4. CSV(s) generated asynchronously; the file lands in [[settings-import-history]]. Export row limit: **150 000 rows**.

The dashboard box caches its result client-side under `${routeName}.${boxKey}.${dateFrom}.${dateTo}.${compare}` for 60 s.

## Settings & fields

### Box configuration

| Key | Value | Meaning |
|-----|-------|---------|
| `key` | `top-bundles-by-traffic` | Box identifier. |
| `type` | `table` | Ranked-table render. |
| `collectDataFrom` | (not set) | No frontend-enforced minimum date. |
| `viewMore` | `true` | Per-row time-series drill-down. |
| `hasDetails` | `true` | Details paginated screen. |
| `hasViewMoreChart` | `true` | Charts views over time. |
| `navigationSort` | `11` | Dashboard position. |
| `details.group` | `false` | One row per bundle. |
| `details.defaultSorting` | views DESC, sales DESC | Default Details sort. |

### Metric definition

A "view" is one `viewProduct` event for a product whose type is `bundle` at view time, deduplicated per hour × uuid × device exactly like the Products by traffic box (see [[analytics-top-products-by-traffic]] "Attribution model"). Admin uuids excluded; mobile/desktop split preserved.

## Business rules

### Same dataset as Products by traffic, plus a bundle filter

This box reads the **same traffic dataset** as [[analytics-top-products-by-traffic]] with one added `type = bundle` filter; the dashboard, Details, and ViewMore queries are otherwise identical (same grouping, sort, limit, drill-down):

| Level | Returns |
|-------|---------|
| Dashboard | Top 5 bundles |
| Details | Full paginated table (page size 100) of all viewed bundles in the period |
| ViewMore | Per-date series for one bundle id |
| Details / ViewMore export | Unpaginated for CSV export |

### Bundles ARE also counted in Products by traffic

The dataset is shared and [[analytics-top-products-by-traffic]] does not exclude bundles, so a bundle's views are counted in **both** boxes — they are not exclusive views.

### Type captured at view time, not at query time

The bundle-vs-regular discriminator is recorded when the visitor views the page, from the product's type at that moment. If a product is later converted between bundle and regular, its older views keep their original type — so rankings can include legacy bundle-type rows for products no longer bundles.

### Empty state and overrides

If the store has no bundles, or none received visits in the period, the box returns "No data" — stores without bundles see it permanently empty. There are no per-merchant or per-store overrides; every store with bundles sees the same ranking.

## How it works (verified against backend)

A bundle is a product type, not a separate entity (see [[bundles-list]]), so its views live in the shared product-traffic dataset and the "bundle" view is just a filter on top. Result rows match [[analytics-top-products-by-traffic]] in shape (id, name, url, device, aggregate, mobile, desktop, viewMore). ViewMore joins generated date intervals with the aggregated buckets so empty periods render as zero rows.

### Translation gap

There is no `top-bundles-by-traffic` translation key in the Analytics EN/BG files (verified by grep), so the box falls back to its inline `labels` object, which is **EN-only** — Bulgarian users see the EN strings.

## Related

- [[analytics]] — parent hub.
- [[analytics-top-products-by-traffic]] — parent box pattern; same structure with no bundle filter.
- [[analytics-top-order-bundles-by-sales]] — sister box, ranks bundles by revenue (not views).
- [[analytics-top-order-products-by-units-sold]] — provides the column formatters this box reuses.
- [[bundles-list]] — bundle entity model.
- [[product]] — entity page.

## Open questions

_None._
