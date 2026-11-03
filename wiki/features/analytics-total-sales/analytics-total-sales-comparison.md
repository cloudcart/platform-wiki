---
type: feature
nav_path: "Analytics → Total Sales → Time range & comparison"
route_name: analytics
route_path: /admin/analytics (box rendered on Dashboard)
aliases: ["Total Sales comparison", "Total Sales date range", "Total Sales time buckets", "Period compare", "Year compare", "Период за сравнение"]
tags: [analytics, ccanalytics, orders, total-sales]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 8
---
> Part of [[analytics-total-sales]]. See the hub for the other aspects (which orders count, industry-compare badge, Details drill-down).

# Total Sales — time range & comparison

## Purpose

This page documents how the Total Sales window is chosen and compared: the Dashboard date-range shortcuts, the **automatic** time-bucket grouping that sets the chart's X-axis granularity, and the exact `period` / `year` comparison math behind the delta badge. This is what support cites when a merchant asks *"why is my chart grouped weekly?"* or *"what exactly is it comparing me to?"*.

## Where to find it

The Dashboard's shared date-range picker (component `DateRangePicker.vue`) and the Dashboard-wide **"Compare"** selector drive this box. They sit above the box grid on the Analytics Dashboard and apply to every box at once.

## What the merchant can do here

- Pick a date range via a built-in shortcut or a custom from/to.
- Turn comparison on (`period` or `year`) to get a delta percentage and arrow under the headline.
- (The merchant cannot pick the chart's bucket size for this box — it is automatic; see below.)

## Settings & fields

### Time-range options

| Shortcut | Range |
|----------|-------|
| **Today** | Today only |
| **Yesterday** | Yesterday only |
| **Last 7 days** | Now − 7 days … now |
| **Last 30 days** | Now − 30 days … now |
| **Last 90 days** | Now − 90 days … now |
| **Last month** | Now − 1 month … now (rolling) |
| **Last year** | Now − 1 year … now (rolling) |
| **Previous month** | Whole previous calendar month |
| **Previous year** | Whole previous calendar year |
| **Custom** | Any from-date / to-date the merchant picks |

Plan-gated `cc_analytics.compare_range` (months back) trims unavailable shortcuts.

### Time-bucket grouping (auto)

The chart's X-axis bucket size is chosen automatically from the range length:

| Range length (days, end-inclusive) | Auto group |
|---------------------|------------|
| < 3 | **hourly** |
| 3 – 60 | **daily** |
| 61 – 90 | **weekly** |
| 91 – 730 | **monthly** |
| > 730 | **yearly** |

The merchant cannot pick a custom group for this box — the dashboard uses `auto`. The [[analytics-total-sales-details|Details view]] (drill-down) does support explicit `group=daily/weekly/monthly/...` parameters.

**Verified breakpoints:** `diff = from.diffInDays(to) + 1`. The 61–90 day bucket is `weekly`, not daily. All bucket date-strings are computed in **store timezone** (Windows-Zones-mapped IANA TZ), NOT UTC — so a daily bucket boundary respects the merchant's local midnight even though the raw `$match` filter is UTC-converted.

### Comparison options (Dashboard-wide selector)

| Value | Effect |
|-------|--------|
| `no` (default) | No comparison — just the current period |
| `period` | Compare to the immediately-preceding period of the same length |
| `year` | Compare to the same period **N years earlier**, where `N = max(1, ceil(diffInDays / 365))` |

`cc_analytics.allow_industry_compare` and `cc_analytics.allow_period_compare` plan limits may hide `period` / `year`.

## Business rules

### Year-compare is adaptive

For ranges ≤ 365 days the compare period is exactly 1 year earlier. For longer ranges it shifts back enough whole years to fit without overlapping the current period (e.g. a 400-day range compares to N=2 years earlier). The `years` count is surfaced in the API response as the `years` field.

### Period-compare math

The previous window is `from.subDays(from.diffInDays(to) + 1) … from.subDays(1)` — same length as the current window, ending exactly the day before the current `from`. Inclusive on both ends in store timezone.

### Date boundary & DST

`dateFrom` / `dateTo` arrive as `Y-m-d` and are parsed at store-tz `startOfDay` / `endOfDay`. UTC values are derived by shifting from store-tz, so a daylight-saving transition on the boundary day shifts the window by an hour at the edge.

### Empty state

If no order matches the filter, the per-bucket array is empty; the chart renders all-zero data points and the headline shows the store currency's zero (`0.00 BGN` etc.). There is no special "no data" card.

## Related

- [[analytics-total-sales]] — hub.
- [[analytics-total-sales-order-filter]] — which orders are admitted into each bucket before grouping.
- [[analytics-total-sales-industry-compare]] — a separate benchmark badge whose granularity is always weekly regardless of the chosen range.
- [[analytics-total-sales-details]] — the drill-down that supports explicit (non-auto) grouping.
- [[plan-gates]] — `cc_analytics.allow_period_compare`, `cc_analytics.compare_range`.

## Open questions

_None._
