---
type: feature
nav_path: "Analytics → Details"
route_name: analytics.details.subView
route_path: /admin/analytics/details/:box/:id
aliases: ["Box details", "Drill-down", "Analytics drill-in", "Box details view", "View details", "Детайли", "Подробен изглед"]
tags: [ccanalytics, analytics, details, drill-down]
plan_gates: ["cc_analytics.allow_period_compare", "cc_analytics.compare_range"]
created: 2026-05-21
updated: 2026-06-10
source_count: 9
---
# Details

## Purpose

The Details screen is the **per-box drill-in** view from the Analytics dashboard. When the merchant clicks **View details** on any dashboard box that has `hasDetails: true` in its config, they land here: a single focus screen for that one metric, with a time-series chart at the top and the full paginated supporting table below.

This page is where the merchant moves from *"how many orders this month?"* (one number on the dashboard) to *"which individual orders made up that number, broken down by date / device / source / status?"* (the full row-by-row evidence). It is also the gateway to deeper drill-downs — clicking any row opens a **sub-view** with the next level down (e.g., for `orders-by-country` → clicking a country opens that country's cities; for `top-categories-by-sales` → clicking a category opens the products inside that category).

This page is the **hub** for the Details cluster. The mechanics that need their own page are split out into aspect pages (see below); this hub keeps the navigation map plus the drill-level model.

## Where to find it

Analytics dashboard → click **View details** on any dashboard box with the drill-in enabled. The breadcrumb at the top reads "Analytics → {box title}" (and adds the sub-row's text for the sub-view).

If a merchant navigates to `/admin/analytics/details/<unknown-box>` or to a box whose `hasDetails: false`, the router's `beforeEnter` guard redirects to `/admin/error-404`.

URL query parameters round-trip into the URL bar: `dateFrom`, `dateTo`, `compare`, `group`, `page` — bookmarkable and shareable.

## What the merchant can do here

- See the **time-series chart** for this single metric at the top — see [[analytics-details-chart-compare]] for the show/hide rules and comparison overlay.
- See the **paginated data table** beneath the chart — the underlying rows that compose the chart. Columns are box-specific (Date / Order / Product name / Quantity / Total sale for sales; Country / Sales / Orders / Sessions for geography; etc.).
- **Change the date range** with the picker — refreshes both chart and table. See [[analytics-details-grouping-dates]].
- **Switch the Compare mode** (No comparison / Previous period / Previous year) — side-by-side current + previous columns. Plan-gated. See [[analytics-details-chart-compare]].
- **Change the time grouping** (Hourly, Daily, Weekly, Monthly, Quarterly, Yearly, None). See [[analytics-details-grouping-dates]].
- **Click into a row** for a deeper drill (the **sub-view**) — only on boxes whose rows have a meaningful next layer (country → cities, category → products, brand → products, landing page → orders).
- **Click a "Hooked" View-more link** to jump to the [[analytics-full]] full table for that record. Renders only when the box has `viewMore: true` (or a string pointing at the related box).
- **Export the report as CSV** (button top-right). See [[analytics-details-csv-export]].

## Settings & fields

| Field / Control | What it does | Default | Validation / notes |
|-----------------|--------------|---------|--------------------|
| Date range | Two dates (from/to). | The standard global default range (last 30 days). | Maximum look-back capped by `cc_analytics.compare_range` plan feature (12 months default). See [[analytics-details-grouping-dates]]. |
| Compare | `no` / `period` / `year`. | `no` (or whatever was in the URL query). | Plan-gated by `cc_analytics.allow_period_compare`. Hidden when the box sets `details.compare: false`. See [[analytics-details-chart-compare]]. |
| Group | `hourly` / `daily` / `weekly` / `monthly` / `quarterly` / `year` (Yearly) / `none`. | `hourly` (overridable from the URL). | Hidden when the box sets `details.group: false`; options re-filter as the range changes. See [[analytics-details-grouping-dates]]. |
| Page | Pagination page index for the table. | 1 | Page size fixed server-side at 100 rows / page (`DETAILS_PAGINATION_LIMIT`). See [[analytics-details-access-limits]]. |

The chart, group selector, and compare selector are only rendered if the box's config opts in (`details.chart`, `details.group`, `details.compare`). All three default to `true` for `chart`-type boxes.

## Business rules

### The three drill levels

Two URL patterns share this experience plus a rare third level:

- `/admin/analytics/details/:box` (route `analytics.details.view`) — the first-level drill on a box.
- `/admin/analytics/details/:box/:id` (route `analytics.details.subView`) — the second-level sub-drill on one row from the first-level table. Both levels share the same layout and controls.
- A small number of boxes (currently only `orders-social-source` / Sales by Source / Medium) have a THIRD level — see [[analytics-more-details]]. Reached by clicking a row in the sub-view; the breadcrumb extends to `Analytics → Sales by Source / Medium → Google → google / cpc`.

### Sub-views (clicking a row → deeper drill)

Some boxes' rows are clickable — clicking opens `analytics.details.subView` (`/admin/analytics/details/:box/:id`) with the same chart/table layout but for THAT specific record. The router `beforeEnter` guard still requires `hasDetails: true` on the box.

The titleValue returned by the backend becomes part of the breadcrumb: simple text for a single record, or an array of `{text, id}` entries which become clickable mid-breadcrumb steps. For example, on Sales by location → click "Bulgaria" → the breadcrumb reads `Analytics → Sales by location → Bulgaria` and the table now lists the cities of Bulgaria. Click "Sofia" → the breadcrumb becomes `Analytics → Sales by location → Bulgaria → Sofia` and the table lists individual orders in Sofia.

The sub-view uses the box's `subDetails` config block — separate `compare` / `group` flags, separate `columnTypes`, separate default sort. So a box can allow compare on the first level but disable it on the sub-view (the default for `details.subDetails.group` is `false`, hiding the group selector by default on sub-views).

### How a fetch resolves (verified against backend)

When the merchant lands on `/admin/analytics/details/:box`:

1. The screen requests the details data for that box with the current `dateFrom`, `dateTo`, `compare`, `group`, and `page` values.
2. The platform parses the interval, validates `compare`, and routes to a per-box report builder that runs the no-compare or period-compare query.
3. The report builder reads pre-aggregated rows from the analytics data store, applies the merchant's status filter + device toggle, paginates, and returns the headers, table rows, export-allowed flag, and day count.
4. The screen maps each column to a display type from the box's `details.columnTypes` config (e.g., `total_sale: 'price'` → money formatting; `order: 'number'` → a link to the order page).
5. The chart panel reuses the dashboard's line chart, taller, inside the details view.

Clicking a row navigates to `analytics.details.subView` with the row's id; the sub-view loads the details data for that one record. Columns, the breadcrumb title, and the drill chain are re-resolved per sub-view. Changing the date range, compare, or group debounces 500 ms then re-fetches and resets pagination to page 1.

## Sub-pages (in this cluster)

- [[analytics-details-chart-compare]] — when the line chart shows vs hides; comparison-mode overlay + side-by-side columns; exact previous-period / previous-year math; no industry-average overlay.
- [[analytics-details-csv-export]] — the Export link, the compare-aware Export modal, the CC2FaAction 2FA gate, the async delivery, the 150k row cap, the force-limit alert, and the one-active-export-per-box lock.
- [[analytics-details-grouping-dates]] — the group selector, the server-side auto-grouping ladder, range-driven option filtering, and store-timezone date parsing.
- [[analytics-details-access-limits]] — permission gates, fixed pagination, the `no`/`period`/`year`-only compare validation (404), the inherited kill switches, and the pre-17-Jan-2023 device "N/A" cutoff.

## Related

- [[analytics]] — the dashboard hub the merchant came from.
- [[analytics-full]] — the deeper "View more" full table view for table boxes.
- [[analytics-more-details]] — the third-level drill (Source/Medium → Campaign).
- [[settings-staff]] — `reports.reports` and `reports.reports_export` staff permissions.
- [[settings-statuses]] — the order-statuses filter that controls which orders count.
- [[order]] — table rows in sales / order drill-ins link to individual orders.
- [[product]] — table rows in product drill-ins link to products.
- [[customer]] — customer drill-ins link here.
- [[category]] — category drill-ins.
- [[vendor]] — brand drill-ins.
- [[plan-gates]] — the `cc_analytics.allow_period_compare` and `compare_range` gates.

## Open questions

_None._
