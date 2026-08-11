---
type: feature
nav_path: "Analytics → Total Sales → Which orders count"
route_name: analytics
route_path: /admin/analytics (box rendered on Dashboard)
aliases: ["Total Sales order filter", "Total Sales counted statuses", "Total Sales money field", "amount_without_shipping", "Кои поръчки влизат в Общи продажби"]
tags: [analytics, ccanalytics, orders, total-sales]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 8
---
> Part of [[analytics-total-sales]]. See the hub for the other aspects (comparison math, industry-compare badge, Details drill-down).

# Total Sales — which orders & money count

## Purpose

This page documents **what the Total Sales headline actually sums**: which orders are admitted by the shared match filter, the hidden status-vs-fulfillment expansion the merchant cannot see in Settings, and which money field on each order is added up. This is the section support cites when a merchant asks *"why is my Total Sales number lower than my real revenue?"*.

## Where to find it

The behaviour is driven by **Settings → Analytics settings**, statuses_title: *"Order statuses that will be included in the analyses"*. The merchant ticks the order statuses that should count; the Total Sales box on the Dashboard then reflects that selection. The status taxonomy itself lives on [[settings-statuses]].

## What the merchant can do here

- Add or remove order statuses from the analytics-counted set (e.g. add `delivered` so delivered orders count toward revenue).
- Understand that any status they tick which isn't a valid analytics status is silently dropped.

## Settings & fields

### Which orders count toward the total

Every Orders-category analytics box runs through the shared match filter, which restricts to:

1. `site_id = <current store>` — scoped per-store.
2. `date ∈ [from-startOfDay, to-endOfDay]` — `dateFrom` / `dateTo` parsed in **store timezone**, then converted to UTC for the match. The time-bucket projections themselves run with `timezone: <store-tz>`, so per-bucket cutoffs land at local midnight.
3. **Order statuses configured for analytics** — pulled from the merchant's `cc_analytics.statuses` configuration.

The **default set** (if the merchant hasn't customised) is `paid`, `completed`, `pending`, `authorized` (payment) and `fulfilled` (fulfillment). Any custom selection is intersected with the valid-statuses dropdown — invalid keys are silently dropped. A merchant who wants `delivered` to count must add it under Settings → Analytics settings; otherwise `delivered`-only orders are invisible to this box.

### Currency / units

All money fields are stored in the store currency's **minor unit × 100** (e.g. `12345` = 123.45 BGN). The pipeline sums in this scaled integer; the display layer applies `moneyFormat`. A merchant who switched currencies will see historical orders summed in the new currency's scaled-integer space — legacy orders carry the old currency's raw integer, so they look numerically off. The pipeline does not convert.

## Business rules

### Hidden status-filter mechanics

The configured status list is expanded into a status-vs-fulfillment OR clause at query time:

- `paid`, `completed`, `authorized` → matched as `status IN [...]`.
- `pending` → matched ONLY when `status=pending AND status_fulfillment=not_fulfilled`. A pending order whose fulfillment has progressed is excluded even though the merchant ticked `pending`.
- `fulfilled` → matched as `status_fulfillment=fulfilled AND status NOT IN <any-status-the-merchant-DESELECTED>`. Shipped orders count regardless of financial status, EXCEPT when that financial status is one the merchant explicitly removed (e.g. a fulfilled-but-cancelled order is excluded if `cancelled` was deselected).
- Other fulfillment statuses (`not_fulfilled`, `partly_fulfilled`) are matched on `status_fulfillment` directly.

### Which money field is summed

The pipeline sums `amount_without_shipping`. Despite the tooltip phrasing ("sales plus taxes and shipping"), the verified backend sums the **products + product-discounts + VAT** portion of each order — shipping amount and shipping discount are excluded from the headline number.

The full per-line breakdown shown in [[analytics-total-sales-details]] does separately list `shipping_amount`, `shipping_discount_amount`, `tax_amount`, `vat_amount`, `discount_amount`, and `products_discount_amount` — but the chart and the big amount are `amount_without_shipping` aggregations.

### Storage layout & performance

| Collection | Purpose |
|------------|---------|
| `analytics.orders` | Raw analytics order document (one per order, full payload) |
| `analytics.total_orders` | Pre-rolled summary used by the headline boxes — Total Sales reads this |
| `analytics.orders_detailed` | Per-line breakdown used by the Details drill-down |

The headline aggregation runs against `analytics.total_orders` (pre-rolled-up, one document per order) using index `idx_total_sales` over `[site_id, date, status, status_fulfillment, amount]`. The read is a tight match → group (sum `amount_without_shipping`) → project chain, fast because pre-aggregation is done by background ingestion jobs. The connection is `the analytics store-analytics`. Very long ranges use `allowDiskUse: true`.

There is **no the application framework-level cache** of the response — the Dashboard always queries live. Headline freshness is therefore the lag of the per-order ingestion job into `analytics.total_orders`.

## Related

- [[analytics-total-sales]] — hub.
- [[settings-statuses]] — the order-status taxonomy the analytics-counted list is drawn from.
- [[analytics-total-sales-details]] — the per-line table that exposes the excluded shipping/tax fields separately.
- [[analytics-total-sales-industry-compare]] — uses a **hardcoded** status filter, not this configurable list.
- [[order]] — entity backing every counted row.
- [[order-status-workflow]] — how an order moves through statuses.

## Open questions

_None._
