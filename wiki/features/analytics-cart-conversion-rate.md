---
type: feature
nav_path: "Analytics → Conversion Rate"
route_name: analytics
route_path: /admin/analytics
aliases: ["Conversion Rate", "Cart conversion rate", "Site conversion rate", "Conversion rate over time", "Процент на реализация"]
tags: [analytics, ccanalytics, cart, conversion-rate]
plan_gates: []
created: 2026-05-22
updated: 2026-06-10
source_count: 9
---
# Conversion Rate

## Purpose

A merchant-facing chart that shows the **percentage of visits that resulted in an order** — the single top-line conversion-rate metric for the store. It's what most merchants think of when they ask "what's my conversion rate?": orders divided by visitors over a chosen period.

This is the *outcome* the rest of the cart funnel feeds into. Where [[analytics-abandoned-carts]] and [[analytics-abandoned-checkout]] tell you *where* in the funnel the leak is, this box tells you the **final outcome** — what fraction of all visitors became paying customers.

## Where to find it

Analytics dashboard → **Conversion Rate** box. It sits high on the dashboard (`navigationSort: 4`), alongside Total Visits and the funnel.

Box `key: "cart-conversion-rate"`, `type: "chart"` — a percentage headline plus a sparkline-style chart over time.

## What the merchant can do here

- See the **headline percentage** (e.g. "1.8%") for the selected period.
- See the trend in the chart underneath.
- Compare to the **previous period** (delta next to the headline).
- Compare against the **industry benchmark** (`hasIndustryCompare: true`).
- Change the **date range** and **grouping** (hourly / daily / weekly / monthly / quarterly / yearly).
- Hover the chart for per-bucket tooltips: "1.8% for 2026-05-22".

This box has **no Details drill-down** (`hasDetails: false`). To see *which* orders or visitors contributed, use the dedicated funnel boxes ([[analytics-cart-conversion-funnel]], [[analytics-abandoned-carts]], [[analytics-abandoned-checkout]]) or the Orders list.

### Box card surface (chart-type)

| Surface | When it appears | What it does |
|---------|-----------------|--------------|
| **Box title** | Always | "Conversion Rate" (EN) / Bulgarian equivalent. |
| **Box tooltip (dotted)** | On hover | "Percentage of visits resulting of orders, depend on selected order statuses in Settings." |
| **Headline number** (`text1`) | Always | The store-wide conversion rate, `percentFormat`. |
| **Subtitle** | Below headline | "Conversion rate over time" (EN). |
| **Previous period delta** (`text3`) | Compare = `period` / `year` | "Previous period: 1.6%". When the previous range begins before `collectDataFrom = 2023-01-13`, the value is replaced with **"N/A"** + a tooltip explaining the cutoff. |
| **Trend arrow** | Compare set | Up green / down red. |
| **Industry compare badge** | `hasIndustryCompare: true` AND benchmark loaded | Pill below the chart with "above/below industry" text. |
| **No-data state** | Empty range | "No data available for the selected range." |
| **Period-cutoff alert** | `dateFrom` < `2023-01-13` | "There is no data for the selected period. Please select a period after 13.01.2023 to view data." |
| **504 timeout** | API HTTP 504 | "We cannot generate statistics for the selected period, please reduce it." |

### Dashboard Settings panel (cog icon)

- **Order statuses** — directly affects the numerator (orders count). Default: Paid / Completed / Pending / Authorized / Fulfilled. The denominator (sessions) is independent of statuses.
- **Industry** — drives the industry-compare benchmark on this box. Recompute lag: up to 1 week.
- **Show devices** — no effect (this box has no device split in the headline rendering).
- **Show boxes sort** — drag/visibility tree.
- **Reset to default / Save / Cancel** — dashboard-wide semantics.

## Settings & fields

### Box configuration

| Property | Value | Meaning |
|----------|-------|---------|
| `key` | `cart-conversion-rate` | Unique identifier; matches the backend metric. |
| `type` | `chart` | Percentage headline + over-time chart. |
| `collectDataFrom` | `2023-01-13` | Earliest date with cart-conversion-rate data. |
| `hasIndustryCompare` | `true` | Industry benchmark comparison enabled. |
| `hasDetails` | `false` | No drill-down details screen. |
| `navigationSort` | `4` | Display position; high on the dashboard. |

### Metric definition (verified against backend)

`Conversion rate = (orders in period) ÷ (visitors / sessions in period)`, expressed as a percentage and rounded to one decimal.

| Term | Definition |
|------|------------|
| **Visitors / Sessions** | The store-session count — the **same denominator** as [[analytics-online-store-sessions]] (Total Visits). |
| **Purchase / Orders** | Orders whose status is in the merchant-selected list (see Business rules). |
| **Rate** | Orders ÷ Visitors, per bucket. |

The headline rate is the per-bucket math summed over the whole period, so the headline always matches the chart-bucket sum.

## Business rules

### "Orders" depends on the Order Status filter

This is the most important rule on the box. The order count is **not all orders placed in the period** — it is only orders whose status is in the merchant-selected list in [[analytics]] (Analytics → Settings → Order statuses).

Default selection commonly includes: Paid, Fulfilled, Pending, Authorized payment, Shipped. The merchant can adjust the selection — that immediately changes the conversion-rate number. If the merchant adds **Cancelled** to the list, cancelled orders count as conversions (rate goes up). If the merchant removes **Pending**, unpaid-but-real orders fall out (rate goes down). Each matching order counts 1 toward the total (not its amount).

The official tooltip text reads: `"Percentage of visits resulting of orders, depend on selected order statuses in Settings."` (Bulgarian: "Процент посещения, довели до поръчки от общия брой посещения. Данните се визуализират спрямо избраните статуси на поръчки в Настройки.")

### Denominator is the store-sessions count (same as Total Visits)

The denominator (Sessions / Visitors) is the store-session count — the **same source** used by [[analytics-online-store-sessions]] (Total Visits). The two numbers track exactly. Sessions are **not** status-filtered (sessions are not order-bound); only the orders numerator respects the order-status selection.

(The box's internal detail-table config labels this column "Visitors / Sessions" and pre-defines columns for `date`, `sessions`, `cart`, `checkout`, `orders`, and `rate`, but those columns are inactive because `hasDetails: false`. They are retained so the Details view can be reactivated later without rework.)

### Data freshness

The visitor / cart / checkout figures refresh on a roughly 1-hour cadence; the orders side is updated by the orders pipeline. Admin sessions (UUIDs matching `/^admin-.*/i`) are excluded throughout.

### Mobile vs desktop categorisation

The underlying data carries a device split (mobile / desktop) for the chart's per-device view. As elsewhere on the dashboard, `device == 'mobile'` → mobile; everything else → desktop (tablet folded in).

### Industry comparison

Because `hasIndustryCompare: true`, the box shows the merchant's rate against the aggregated benchmark for stores in the same industry. The benchmark is computed by a separate per-industry rollup (recompute lag up to 1 week) that anonymises the inputs. The merchant's own number is never exposed to peers; only the aggregate is shared back.

### Applies to every store

The conversion-rate definition is identical for every store. Only the order-status filter is configurable per-store, and the platform respects that selection uniformly. The chart's bucket range matches the date picker's exact range (no window expansion).

## Related

- [[analytics]] — parent hub; also the order-status selection that drives the Orders count.
- [[analytics-cart-conversion-funnel]] — the same data shown as a 3-stage funnel.
- [[analytics-abandoned-carts]] — the abandonment metric one step before this one.
- [[analytics-abandoned-checkout]] — the abandonment metric between checkout and order.
- [[analytics-online-store-sessions]] — the "Total Visits" metric; supplies the identical denominator.
- [[order]] — entity counted in the numerator.

## Open questions

_None._
