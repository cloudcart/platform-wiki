---
type: feature
nav_path: "Analytics → Date range & Compare"
route_name: analytics
route_path: /admin/analytics
aliases: ["Analytics date range", "Analytics compare", "Compare previous period", "Compare previous year", "Analytics look-back cap", "Analytics timezone", "Analytics plan gates"]
tags: [analytics, dashboard, date-range, compare, plan-gates, timezone]
plan_gates: ["cc_analytics.allow_period_compare", "cc_analytics.allow_industry_compare", "cc_analytics.compare_range"]
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[analytics]]. See the hub for the other aspects (dashboard shell, settings panel, box catalog, industry compare, data freshness).

# Analytics — date range & Compare

## Purpose

This aspect covers the two controls at the top of the Analytics dashboard that change the *period* the boxes describe: the **date-range picker** (which sets the window for ALL boxes at once) and the **Compare** selector (which overlays a prior-period or prior-year series for trend comparison). It also covers the three plan features that gate those controls, the maximum look-back cap, and the store-timezone rule that decides what "today" means.

## Where to find it

Both controls sit at the top of the Analytics dashboard at `/admin/analytics`. The chosen values round-trip into the URL bar as `dateFrom`, `dateTo`, and `compare`, so a view can be bookmarked or shared.

## What the merchant can do here

- **Pick a date range** with quick presets (Today, Yesterday, Last 7 days, Last 30 days, This month, etc.). Changing the range refreshes ALL visible boxes via a debounced reload (500 ms).
- **Pick a Compare mode** — `No comparison` (default), `Compare: Previous period`, or `Compare: Previous year` — to overlay the prior series on every chart and table.

## Settings & fields

| Field / Control | What it does | Default | Validation / notes |
|-----------------|--------------|---------|--------------------|
| Date range | Two dates (from / to) applied to ALL boxes. | Last 30 days. | Maximum look-back is capped by the plan-gated `cc_analytics.compare_range` value (in months). The picker visually disables dates beyond that. CloudCart employees see `null` (no cap). |
| Compare | One of `no` / `period` / `year`. | `no` | The `period` and `year` options are gated by `cc_analytics.allow_period_compare`. If not allowed, the dropdown is shown but locked with a "Plans that support this functionality are: {plans}" tooltip. |

## Business rules

### Plan-gated comparisons

The dashboard reads three plan features at load time (`POST /admin/api/core/plan`):

| Plan feature | What it controls | Default if not allowed |
|--------------|------------------|------------------------|
| `cc_analytics.allow_period_compare` | The `Compare: Previous period` and `Compare: Previous year` dropdown options. | Locked; tooltip shows the plans that unlock it. |
| `cc_analytics.allow_industry_compare` | The industry-average line on charts (and triggers a fetch of `/admin/api/analytics/statistic` when allowed). See [[analytics-overview-industry-compare]]. | Industry line hidden. |
| `cc_analytics.compare_range` | The maximum look-back range (in months) the date picker allows. | 12 months. |

CloudCart employees get all three flags forced to `value: true` and `compare_range = null` (unlimited) — independent of the plan, so support staff can read any range when troubleshooting. See [[plan-gates]] for the platform-wide gate concept.

### Time-zone of the dashboard

The date range the merchant picks is interpreted in the **store's primary timezone** (the `site.timezone` setting), not UTC and not the merchant's browser timezone. Internally, "today 00:00 - 23:59" becomes the UTC equivalent of those local hours; the aggregated data is then read back in the SAME store timezone so hourly buckets line up with the merchant's expectation of "9-10 AM".

The `dateFrom` / `dateTo` returned from the API are converted back to the store timezone for display. So a store with timezone `Europe/Sofia` and a US-based staff member viewing the dashboard at 14:00 New York time still sees "today" defined by Sofia's clock (currently 21:00 Sofia), not their local clock.

### Comparison overlay vs industry overlay

The Compare selector overlays the **same store's** prior-period or prior-year data. That is distinct from the **industry-average** overlay (a cross-store benchmark line), which is a separate plan feature and uses a fixed status set — see [[analytics-overview-industry-compare]].

## Related

- [[analytics]] — hub.
- [[analytics-overview-industry-compare]] — the separate cross-store benchmark line and its plan gate.
- [[analytics-overview-settings]] — the statuses filter that defines what counts toward each box.
- [[analytics-overview-data-freshness]] — why a just-placed order may not be in the range yet.
- [[plan-gates]] — concept page on plan-feature flags.
- [[plan]] — the merchant's plan entity.

## Open questions

_None._
