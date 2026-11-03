---
type: feature
nav_path: "Analytics → Full"
route_name: analytics.viewMore
route_path: /admin/analytics/full/:box/:record
aliases: ["View more", "Analytics full list", "Full table", "Full report", "Виж повече", "Пълен изглед"]
tags: [ccanalytics, analytics, full, table, view-more]
plan_gates: ["cc_analytics.allow_period_compare", "cc_analytics.compare_range"]
created: 2026-05-21
updated: 2026-06-10
source_count: 8
---
# Full

## Purpose

The **View more** screen is the full paginated list behind a top-N table card from the Analytics dashboard. The dashboard's table boxes (Products by units sold, Top Brands, Top Categories, Landing pages, Sales by location, Sales by Source / Medium, etc.) only show **5 rows** by default (`TABLE_RECORDS_LIMIT = 5`). When the merchant clicks **View more** on one of these cards — or follows the "View more" link from a column inside the Details drill-in — they land here on the full list.

Compared to [[analytics-details]] (which is a per-METRIC drill — one chart + one metric's supporting rows), this screen is a per-COLLECTION drill: the same kind of table the dashboard showed at 5 rows, but now with the full record set, paginated 100 / page, with sorting, an inline time-series chart on top (when the box has `hasViewMoreChart: true`), and the same Compare / Group / Export controls.

The route's `:record` parameter is what the merchant clicked into — it can be a record id (for a "view more" of one parent record's children) or an empty string (for a "view more" of the top-level list).

This page is the **hub** for the View more cluster. The mechanics that need their own page are split into aspect pages (see below); this hub keeps the navigation map plus the drill model.

## Sub-pages (in this cluster)

- [[analytics-full-boxes]] — which dashboard boxes have a View more list (`viewMore: true`), the string-valued `viewMore` redirect, per-box sort order, and dynamic breadcrumb building.
- [[analytics-full-chart-pagination]] — the inline per-row time-series chart, Compare / Group controls, 100-row server-side pagination, the per-box `DETAILS_FORCE_LIMIT` cap, kill switches, timezone, 504 mapping, device-column boundary.
- [[analytics-full-csv-export]] — the Export flow: compare-aware Export modal, `CC2FaAction` 2FA gate, async delivery, `view: view_more` flag, 150 000-row cap, one-active-export-per-box lock.

## Where to find it

Two paths lead here:

- **From a dashboard table card** — click the **View more** link in the card footer. Routes to `/admin/analytics/full/:box/` (empty record) for the box's top-level full list.
- **From a row inside [[analytics-details]]** — when a row has a "View more" column action (e.g., a country row in Sales by location has "View more" pointing at the country's full set of orders). Routes to `/admin/analytics/full/:box/:record`.

If the merchant navigates to a box without `viewMore` enabled, the router's `beforeEnter` guard rejects them to `/admin/error-404` — see [[analytics-full-boxes]]. URL query parameters round-trip: `dateFrom`, `dateTo`, `compare`, `group`, `page` — bookmarkable.

## What the merchant can do here

- See the **full paginated table** of all rows in this box for the date range (instead of just the top 5) — 100 rows per page; see [[analytics-full-chart-pagination]].
- See an **inline per-row time-series chart** above the table for boxes with `hasViewMoreChart: true` — see [[analytics-full-chart-pagination]].
- **Change the date range, Compare mode, and time grouping** — all refresh chart and table.
- **Export to CSV** through the 2FA + async export job — see [[analytics-full-csv-export]].
- **Navigate back via the breadcrumb** — `Analytics → {box title} → {parent record (if any)}`; see [[analytics-full-boxes]].

## Settings & fields

| Field / Control | What it does | Default | Validation / notes |
|-----------------|--------------|---------|--------------------|
| Date range | Two dates (from/to). | Standard global default (last 30 days). | Max look-back is `cc_analytics.compare_range` plan feature. See [[analytics-full-chart-pagination]]. |
| Compare | `no` / `period` / `year`. | `no` (or URL query). | Gated by `cc_analytics.allow_period_compare`. See [[analytics-full-chart-pagination]]. |
| Group | `hourly` … `year` / `none`. | `hourly` (or URL query). | Re-filtered by date range. See [[analytics-full-chart-pagination]]. |
| Page | Pagination index. | 1 | 100 rows per page (`DETAILS_PAGINATION_LIMIT`); enforced server-side. |

## Business rules

The detailed rules live on the aspect pages:

- **Which boxes are reachable** (`viewMore: true`), the string-valued redirect, sorting, and breadcrumb building — [[analytics-full-boxes]].
- **Chart, pagination, force-limit, kill switches, timezone, 504, device boundary** — [[analytics-full-chart-pagination]].
- **Export modal, 2FA, row caps, export lock, permissions** — [[analytics-full-csv-export]].

The drill model in brief: reaching this URL requires the `reports` / `reports.reports` permission. The screen requests the extended (full) data for that box and record with the current date / compare / group / page; the platform validates `compare`, routes to a per-box report builder, reads the per-record paginated rows from the analytics data store, applies the merchant's order-statuses + devices filters, and returns the headers, table rows, and breadcrumb title plus the export-allowed flag and day count. The screen maps columns and, when `hasViewMoreChart: true`, post-processes the table data into a chart.

## How it works (verified against backend)

When the merchant lands on `/admin/analytics/full/:box/:record`:

1. The screen requests the extended (full) data for that box and record with the current `dateFrom`, `dateTo`, `compare`, `group`, and `page` values.
2. The platform parses the interval, validates `compare`, routes to a per-box report builder, sets the record id on it, and runs either the no-compare or the period-compare view-more query depending on `compare`.
3. The report builder reads the per-record paginated rows from the analytics data store, applies the merchant's order-statuses + devices filters, and returns the headers, table, and `titleValue` (which drives the breadcrumb — see [[analytics-full-boxes]]).
4. The screen maps columns from the box's `viewMore.columnTypes` config, formats values via its `viewMore.row` config, and (if `hasViewMoreChart: true`) post-processes the raw table data into a chart via the box config's `viewMore.chart` settings (`tableToChart`, `datasets`, `labels`).

The pre-aggregated rows that produce these tables are stored per-box (top products, top brands, landing pages, orders sources, orders locations, etc.). Many use a per-hour or per-day rollup so the View more chart can show finer granularity without re-aggregating.

## Related

- [[analytics]] — the dashboard the merchant came from.
- [[analytics-details]] — the per-metric drill-in (alternative path, with sub-views).
- [[analytics-more-details]] — third-level drill (only Sales by Source / Medium → Campaign).
- [[analytics-full-boxes]] — eligible boxes + breadcrumb (aspect).
- [[analytics-full-chart-pagination]] — chart, pagination, limits (aspect).
- [[analytics-full-csv-export]] — export flow (aspect).
- [[product]] — Top Products rows link out to product pages.
- [[category]] — Top Categories rows link out to category pages.
- [[vendor]] — Top Brands rows link out to vendor pages.
- [[bundle]] — Top Bundles rows.
- [[order]] — sales rows can link to specific orders.
- [[settings-staff]] — `reports.reports` / `reports.reports_export` permissions.
- [[settings-statuses]] — the status filter that limits which orders count.
- [[plan-gates]] — `cc_analytics.allow_period_compare` and `compare_range` gates.

## Open questions

_None._
