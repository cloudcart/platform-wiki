---
type: feature
nav_path: "Analytics → More Details"
route_name: analytics.moreDetails
route_path: /admin/analytics/more-details/:box/:column/:id
aliases: ["Third-level drill", "Campaign drill", "Source drill", "Source / Medium / Campaign", "More details", "Допълнителни детайли", "Дълбок изглед"]
tags: [ccanalytics, analytics, more-details, drill-down]
plan_gates: ["cc_analytics.allow_period_compare", "cc_analytics.compare_range"]
created: 2026-05-21
updated: 2026-05-27
source_count: 7
---
# More Details

## Purpose

**More Details** is the deepest drill in the Analytics navigation tree — a third level beyond [[analytics-details]]. Where Details breaks a metric down row-by-row and a sub-view breaks down one of those rows, More Details breaks down one dimension of that sub-row. It is used only in boxes with a meaningful third axis to slice on.

The canonical example is the **Sales by Source / Medium** box (`orders-social-source`):

| Level | URL | What it shows |
|-------|-----|---------------|
| Dashboard card | `/admin/analytics` | Top 5 traffic sources by sales. |
| Details | `/admin/analytics/details/orders-social-source` | Full table of sources for the date range, same columns. |
| SubDetails | `/admin/analytics/details/orders-social-source/google` | Within "Google", the breakdown by medium (organic, cpc, email). |
| **MoreDetails** | `/admin/analytics/more-details/orders-social-source/source/google%2Forganic` | Within "google / organic", the breakdown by **campaign** (utm_campaign). |

Each level adds one dimension of granularity — Source → Medium → Campaign — so the merchant can answer *"how much revenue did the 'spring-sale-2026' campaign on Google organic specifically bring in?"*.

## Where to find it

The merchant reaches More Details by drilling THREE deep — usually by clicking a row in the [[analytics-details]] sub-view on a box that supports the third level.

Navigating to a box that does not support details (`/admin/analytics/more-details/<unsupported-box>/...`) redirects to `/admin/error-404`. The guard reuses the Details support flag (`hasDetails: true`); there is no separate "more details" flag.

URL query parameters round-trip: `dateFrom`, `dateTo`, `compare`, `group`, `page`.

## What the merchant can do here

- See the **full paginated table** for the deepest slice — for `orders-social-source`, campaigns within a (source, medium) pair.
- **Change the date range, Compare mode, and time grouping** (controls detailed below).
- **Paginate**, **export to CSV** (same async + two-factor flow as the other Analytics screens), and **navigate back via the breadcrumb**, which stacks every prior drill level.

There is NO chart on this screen. The third-level drill is data-only.

## Settings & fields

| Field / Control | What it does | Default | Validation / notes |
|-----------------|--------------|---------|--------------------|
| Date range | Two dates. | Standard global default (last 30 days). | Capped by `cc_analytics.compare_range` plan feature. |
| Compare | `no` / `period` / `year`. | `no` (or URL query). | Visibility from `details.subDetails.compare` (default `true`). Plan-gated by `cc_analytics.allow_period_compare`. |
| Group | `hourly` / `daily` / `weekly` / `monthly` / `quarterly` / `year` / `none`. | `hourly`. | Visibility from `details.subDetails.group` (default `false` — hidden on this screen unless the box explicitly enables it). |
| Page | Pagination index. | 1 | 100 rows per page, server-enforced. |

## Business rules

### Which boxes support MoreDetails

Currently exactly **one box** has a real third-level implementation: `orders-social-source` (Sales by Source / Medium → Campaign drill). Because the route layer accepts the screen for any `hasDetails: true` box (see "Where to find it"), every other box reaches it but returns empty rows.

### Multi-level navigation flow

The merchant clicks down through the levels shown in the Purpose table: Dashboard box → "View details" → Details (sources) → click "Google" → SubDetails (mediums) → click "organic" → MoreDetails (campaigns).

The breadcrumb stacks each step (`Analytics → Sales by {details} → Google → google / organic`) and mid-breadcrumb steps are clickable, so the merchant can hop back to "Google" without returning all the way to Details.

### Compare / Group flags shared with sub-views

The third-level screen REUSES the box's `details.subDetails.compare` and `details.subDetails.group` flags (there are no separate `moreDetails.*` flags). So `details.subDetails.compare: false` disables Compare across both the sub-view and this screen. The default `details.subDetails.group: false` means the group selector is hidden here for most boxes — including `orders-social-source` unless explicitly overridden.

### Column types fall through

The columns inherit from `formatters.subDetails.columnTypes` first, falling back to `formatters.details.columnTypes`. The merchant sees the same money / number / device / date formatting as on the parent screens.

### URL `:column` parameter

In `/admin/analytics/more-details/:box/:column/:id`, `:column` names which parent-table column the merchant drilled into (always `source` for `orders-social-source`). The backend keys off `:id` (the parent record, e.g. `google%2Forganic`) and uses `:column` only for breadcrumb labelling.

### CSV export

Same mechanism as the other Analytics screens (see [[analytics-details]]):

- Button shows only with the `reports.reports_export` permission.
- When Compare is on, the Export modal offers *"Include comparison data (separate csv file)"* — two CSVs (current + previous) or one. When Compare is off, it skips straight to two-factor confirmation.
- Hard cap 150,000 rows; delivered async (CSV only, no XLSX). The export carries `view: more_details` plus the parent `:id` so the audit trail reproduces the exact slice.
- The **one-active-export-per-box lock** applies: if another export for `orders-social-source` (Details, Sub-details, or View more) is still running, this request returns the "request for this file is already in progress" 400.

### Force-limit alert

If the report is capped at 1,000 rows, the same yellow alert appears: *"This report shows up to {total} results. To see all results, you can [Export]"*.

### Compare validation — same 404 rule

The Compare query parameter is server-validated against the closed list `no` / `period` / `year`. Any other value returns HTTP 404 for the whole request.

### What it does NOT support

- No chart slot (unlike Details or View more) — a merchant wanting to chart this depth must export and chart externally.
- No fourth level — the drill stops at this depth.
- No industry-average overlay (Dashboard-only feature).
- No "Show more / View more" link — the data here IS the most-granular slice.

### Shared dashboard behaviours

This screen inherits the dashboard's behaviours with no per-screen overrides:

- Same kill-switch / disabled-site gating and empty-data behaviour as the dashboard.
- `dateFrom` / `dateTo` parsed in the store's primary timezone, not UTC.
- Device-breakdown cells show "N/A" when `dateFrom` is before **17 January 2023** — the events feed did not record device before that date.
- Amounts are summed in each order's original currency; a multi-currency store sums across currencies with NO conversion (single-currency stores see no anomaly — see the pipeline caveat).
- The dashboard's `cacheHash` is appended to every call here, so saving Settings immediately busts browser-level cache; cleared on Reset.

## How it works (verified against backend)

When the merchant lands on `/admin/analytics/more-details/:box/:column/:id`:

1. The screen calls `GET /admin/api/analytics/details/{box}/more/{details}?dateFrom=...&dateTo=...&compare=...&group=...&page=...`, where `{details}` is the URL-encoded id (e.g. `google%2Forganic`).
2. The backend parses the interval, validates `compare`, dispatches by compare type (no-compare or period-compare) to the per-box query, and sets the parent record id. Only boxes with explicit support (today, the Source / Medium → Campaign drill) return real data; others fall through to empty.
3. For `orders-social-source`, the query filters the source aggregations to the selected source/medium, groups by source + campaign, and returns rows paginated 100 / page.
4. Columns map from `formatters.subDetails.columnTypes` (falling back to `formatters.details.columnTypes`).

The response envelope is identical to the Details / SubDetails endpoints, so all three render in the same shared shell. Changing date range, compare, or group debounces 500ms, re-fetches, and resets to page 1.

## Related

- [[analytics]] — the dashboard hub.
- [[analytics-details]] — the parent Details / SubDetails screen the merchant drilled through to get here.
- [[analytics-full]] — the alternative "View more" deep path (paginated full list with chart).
- [[campaign]] — for `orders-social-source`, the rows here are utm_campaign values from the platform's campaign records.
- [[order]] — the source data for the social-source aggregations.
- [[settings-staff]] — `reports.reports` / `reports.reports_export` permissions.
- [[settings-statuses]] — which order statuses count toward these aggregations.
- [[plan-gates]] — `cc_analytics.allow_period_compare` and `compare_range` gates.

## Open questions

_None._
