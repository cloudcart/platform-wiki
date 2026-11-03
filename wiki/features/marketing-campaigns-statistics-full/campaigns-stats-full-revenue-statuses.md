---
type: feature
nav_path: "Marketing → Campaigns → Statistics → Revenue statuses"
route_name: campaigns.statistics.full.revenue
route_path: /admin/campaigns/statistics/full/revenue
aliases: ["Campaign revenue statuses", "What counts as revenue", "revenue_statuses setting", "Segments revenue filter", "Кои статуси са приход"]
tags: [marketing, campaigns, statistics, revenue, order-status]
plan_gates: ["abandoned_orders", "campaigns"]
created: 2026-05-23
updated: 2026-06-10
source_count: 2
---

> Part of [[marketing-campaigns-statistics-full]]. See the hub for the other aspects (dashboard, revenue panel, attribution metadata, attribution mechanic, order processing).

# What counts as "revenue"

## Purpose

The revenue figures on the [[campaigns-stats-full-dashboard]] Turnover card and the [[campaigns-stats-full-revenue-panel]] order list only count orders in certain statuses. This page documents **which** statuses qualify, how the filter is merchant-configurable, and why a cancelled order drops out of the numbers even though its attribution metadata stays.

## Where to find it

The qualifying status set is read from the **Segments** app's `revenue_statuses` setting. There is no dedicated screen on the statistics pages — the filter applies automatically to every campaign revenue query.

## What the merchant can do here

A merchant can change which order statuses count as revenue by editing the **Segments** app's `revenue_statuses` setting. The Statistics revenue queries automatically respect it — a merchant who configures their store to count "shipped" orders as revenue will see the same statuses applied to campaign attribution.

## Settings & fields

### `revenue_statuses` — the configurable revenue filter

The "what counts as revenue" filter is **not** hard-coded — it reads from the Segments app `revenue_statuses` setting. The default, if unset: `paid`, `completed`, `fulfilled`, `pending`. The merchant can override this to include or exclude specific statuses.

## Business rules

### Main-status vs fulfillment-status split

The platform's order-status pool contains both regular `orders.status` values (e.g. `paid`, `cancelled`) AND `orders.status_fulfillment` values (e.g. `fulfilled`, `unfulfilled`). The revenue query splits the configured `revenue_statuses` list across these two columns, then OR-joins them:

`WHERE orders.status IN (<main statuses>) OR (orders.status_fulfillment IN (<fulfilment statuses>) AND orders.status NOT IN (<negative statuses like cancelled, refunded>))`

So a fulfilment-status-only revenue criterion **still excludes cancelled orders** even if they happened to be fulfilled.

### Negative-status list is auto-computed

The "what does NOT count as revenue" list is computed automatically as:

`all order statuses MINUS (configured revenue statuses + 'pending')`

So any order status not configured as revenue (and not `pending`) is treated as negative for the OR-join above. Changing the `revenue_statuses` setting **auto-updates** the exclusion criteria — there is no separate "what NOT to count" config.

### Cancelled / refunded orders keep their attribution but leave the revenue

A customer who clicked a campaign link, placed an order, then cancelled it: the order's `cc_campaign_id` meta row **stays** (see [[campaigns-stats-full-attribution-metadata]]), but the order no longer matches the revenue-status filter — so it is **NOT** included in the revenue numbers. Typical qualifying statuses are the "real" ones (NEW, ACCEPTED, IN_PROGRESS, SHIPPED, COMPLETED) and not CANCELLED or REFUNDED, but the exact set is whatever the merchant's [[settings-statuses]] / Segments config defines.

## Related

- [[marketing-campaigns-statistics-full]] — hub.
- [[campaigns-stats-full-dashboard]] — Turnover KPI uses this filter.
- [[campaigns-stats-full-revenue-panel]] — the order list uses this filter.
- [[campaigns-stats-full-attribution-metadata]] — attribution survives even when the order drops out of revenue.
- [[settings-statuses]] — order-status configuration backing the status pool.
- [[order]] — Order entity carrying `status` / `status_fulfillment`.

## Open questions

No outstanding questions.
