---
type: feature
nav_path: "Analytics → Details → Chart & Compare"
route_name: analytics.details.subView
route_path: /admin/analytics/details/:box/:id
aliases: ["Details chart", "Details compare", "Period comparison", "Previous period", "Previous year", "Сравнение по период", "Графика в детайли"]
tags: [ccanalytics, analytics, details, chart, compare]
plan_gates: ["cc_analytics.allow_period_compare", "cc_analytics.compare_range"]
created: 2026-06-10
updated: 2026-06-10
source_count: 9
---
# Details — Chart & Compare

> Part of [[analytics-details]]. See the hub for the drill-level model and the other aspects (export, grouping & dates, access & limits).

## Purpose

This aspect covers the **time-series chart** at the top of the Details screen and the **Compare** control that overlays a prior period on it. Together they answer *"is this metric trending up or down, and how does that compare to the period before?"* for a single dashboard box.

## Where to find it

Analytics dashboard → **View details** on a box → the chart sits at the top of the Details screen (above the table); the **Compare** dropdown sits with the date-range and group controls. Both also appear on the sub-view when the box's `subDetails` config opts in.

## What the merchant can do here

- See the full-width line chart for the single metric (same component as the dashboard card, but bigger).
- Switch **Compare** between **No comparison**, **Previous period**, and **Previous year**.
- Read the prior-period series as a second line overlaid on the current period, and read side-by-side current + previous columns in the table beneath.

## Settings & fields

| Field / Control | What it does | Default | Validation / notes |
|-----------------|--------------|---------|--------------------|
| Compare | `no` / `period` / `year`. | `no` (or the URL query value). | Plan-gated by `cc_analytics.allow_period_compare`. Hidden entirely when the box sets `details.compare: false` (e.g., Total Sales does this). |

The chart renders only if the box opts in via `details.chart` (defaults to `true` for `chart`-type boxes).

## Business rules

### When the chart shows vs hides

The line chart at the top renders only when ALL of these are true:

- The box's `type` is `chart` (not `table` / `bar` / `funnel`).
- The box's config does NOT set `details.chart: false`.
- A valid date range is selected.

For `table`-type boxes (most top-N tables — Top Products, Top Brands, Categories, etc.) there is no chart on the first-level Details; the screen is just the full table. The chart returns when the merchant goes one deeper into [[analytics-full]] via View more (where `hasViewMoreChart: true`).

### Comparison-mode behaviour

When `compare = period` or `compare = year`:

- The chart overlays a second series (the prior-period line) on top of the current period.
- The table shows side-by-side "currently" + "previous" columns for the comparable metric (e.g., a row reads `Orders: 42 → 38`).
- The CSV export flow switches to the compare-aware Export modal — see [[analytics-details-csv-export]].

The Compare control is plan-gated. If the plan doesn't allow it, the dropdown is shown locked with a tooltip listing the plans that unlock it (`Plans that support this functionality are: <plans>`).

### Exact previous-period math

The Details / ViewMore / MoreDetails screens compute the prior period via the same `IntervalParse` trait the dashboard uses:

| Compare mode | Previous from | Previous to |
|--------------|----------------|--------------|
| `period` | dateFrom minus (daysDiff + 1) → start of day | dateFrom minus 1 day → end of day |
| `year` | dateFrom minus N years → start of day (N = the platform code) | dateTo minus N years → end of day |

So a 28-day range with Compare = Previous period compares against the previous 28 days (NOT the calendar prior month). A 14-month range with Compare = Previous year compares against **two** years ago (the date diff exceeds 365, so N = 2).

### No industry-average overlay

The Details screen does NOT show the industry-average overlay — that's a Dashboard-only feature. Inside Details, "Compare" only ever means prior-period or prior-year for THIS store.

### Compare validation

The `compare` query parameter is server-validated: any value other than `no`, `period`, or `year` returns HTTP 404 for the whole fetch — see [[analytics-details-access-limits]] for the validation/kill-switch details.

## Related

- [[analytics-details]] — hub.
- [[analytics]] — the dashboard, where the industry-average overlay lives.
- [[analytics-full]] — View-more table, where `table`-type boxes get their chart.
- [[plan-gates]] — `cc_analytics.allow_period_compare` and `compare_range`.

## Open questions

_None._
