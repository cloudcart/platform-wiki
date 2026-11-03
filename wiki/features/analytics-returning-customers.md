---
type: feature
nav_path: "Analytics → Total Customers (Returning)"
route_name: analytics
route_path: /admin/analytics
aliases: ["Returning customers", "New vs returning customers", "Returning customer rate", "Върнали се клиенти", "Нови срещу върнали се клиенти"]
tags: [analytics, ccanalytics, orders, customer, returning-customers, total-customers]
plan_gates: []
created: 2026-05-22
updated: 2026-06-10
source_count: 10
---
# Returning customers

## Purpose

The **"Returning customers"** metric answers: *"Of the customers who ordered in the period, how many had ordered before vs how many are first-time buyers?"* It is the headline indicator of repeat-business health.

**It is a derived metric, not a standalone card.** It is computed and surfaced inside the **Total Customers** box (key `total-customers`) on the [[analytics]] dashboard, split into a **New** and a **Returning** data series. There is no separate `returning-customers` card: the default dashboard layout includes an `id: "returning-customers"` entry with `disabled: true`, so it shows as a hidden node in the box-reorder UI but never renders on its own.

## Where to find it

Sidebar → **Analytics** dashboard → **Total Customers** card (third box from the top by default, after Total Sales and Total Orders). The card shows one stacked chart with two series:

- **New** / **Нови** — customers placing their first-ever order in the period.
- **Returning** / **Върнали се** — customers who had at least one prior order before this one.

The card header shows running totals for **New** and **Returning** plus a headline **total** (their sum). Per-point tooltip: *"{count} new customer|{count} new customers"* / *"{count} returning customer|{count} returning customers"* (pluralised).

## What the merchant can do here

- **Read the split** — two summary counters (New, Returning) above a stacked time-series chart, auto-bucketed (hourly / daily / weekly / monthly) by the selected range.
- **Toggle industry compare** (`hasIndustryCompare: true`) — overlays the platform's industry benchmark for similar stores. Total Customers is the only customer-level box with this enabled out of the box. Compare badge text: *"For period {period} Total Customers: {value} where is {percent} above/below the average for {industry}"*.
- **No drill-down.** Unlike Categories / Brands / Discount boxes, Total Customers has **no Details screen, no View More, no per-record click-through**. To see *which* customers, use the [[customers]] list with an order-history filter — customer identity is intentionally not exposed at this surface.
- **No previous-period delta.** Compare = `period`/`year` produces no trend arrow or previous block (`header.previous = null`), so the box renders identically regardless of compare mode.
- **No device split** ("Show devices" has no effect — customers are device-agnostic).

Box tooltip (BG is more explicit than EN — it states the dependency on the used-statuses config):

- **EN**: *"Total unique customers, depend on selected order statuses in Settings. Customers made more than one order in your store VS customers made an order into a time frame."*
- **BG**: *"Общ брой уникални клиенти, процентът клиенти, които са направили повече от една поръчка във Вашия магазин и процент клиенти, които са направили само една поръчка в рамките на избрания период от време. Данните се визуализират спрямо избраните статуси на поръчки в Настройки."*

No-data state: *"No data available for the selected range."* On HTTP 504: *"We cannot generate statistics for the selected period, please reduce it."*

## Settings & fields

No box-specific configurable settings. Dashboard-level controls that affect it:

| Control | Effect |
|---------|--------|
| Date range (`from / to`) | Period filter; also drives chart x-axis bucketing (Group is auto-determined). |
| Compare (`no` / `period` / `year`) | Ignored for this metric — output is identical (`header.previous = null`). |
| Industry compare | Toggle from box header; overlays the platform benchmark when enabled. |
| **Order statuses** (Settings cog) | Selects which orders count as customer activity at query time — see Business rules. |
| **Industry** (Settings cog) | Drives the industry-compare benchmark. Recompute lag: up to 1 week. |

## Business rules

### New vs Returning classification — the `customer_orders` field

Each order carries a `customer_orders` field — the count of orders the customer had placed **before** this one (all history, **any** status, even cancelled/refunded, even years ago). It is computed once at ingest and not normally recomputed:

- `customer_orders == 0` AND `customer_id != null` → **New** (first-ever order).
- `customer_orders > 0` AND `customer_id != null` → **Returning**.
- `customer_id == null` (guest checkout) → **excluded entirely** from New, Returning, and Total.

Because the prior-order check uses **all** historical orders regardless of status, a customer whose only previous order was cancelled is still "Returning" on their next order — even if the merchant excludes cancelled orders from the analytics filter. If `customer_id` is later back-linked to a guest order, the classification can flip on the next re-ingest.

### Guests are dropped, not just hidden

Guest orders (`customer_id` empty) are **deleted** from the returning-customers data at ingest, so they cannot land in any bucket. If Total Orders exceeds Total Customers, the gap is guest-checkout volume. See [[subscriber-vs-customer]] for the customer / guest / subscriber distinction.

### Unique counting + headline de-duplication

Each series counts **unique** customer IDs, so a customer placing 3 orders in one day counts as **1** for that day. For the headline counters, New is reduced by the set of Returning IDs first, so a customer who placed their first order **and** a follow-up in the same period is counted as **Returning only**, never double-counted. The per-bucket chart does not apply this de-dup — it may show the same customer as New on day 1 and Returning on day 5; only the headline reconciles them.

### Status filter — applied at query time

The merchant's selected analytics statuses (Settings → Analytics; default: Paid, Completed, Pending+not_fulfilled, Authorized, Fulfilled) filter the data at the dashboard query, so changing the selection updates the chart on next refresh with **no re-ingest**. Note the asymmetry: this filter shapes the dashboard counts, but the prior-order check (`customer_orders > 0`) always uses all statuses.

### Industry benchmark uses a fixed status list

The industry benchmark computes returning rates with a **fixed** status set (`paid`, `completed`, `pending+not_fulfilled`, `authorized`, `fulfilled`) — **not** the merchant's selection. So a merchant who narrows their own filter to only `paid` is compared against the broader default cohort and may appear "below industry" purely because of the narrower numerator. This mismatch is intentional, to keep the benchmark comparable across stores. The benchmark is the per-industry median (verify).

## How it works (verified against backend)

- The metric renders as two series inside the Total Customers box config (`total-customers`, `type: "chart"`, `hasIndustryCompare: true`, translation keys `text.new` / `text.returning`). There is no separate `returning-customers` config file.
- Two reads back the box: one for the per-bucket time series (New + Returning counts per bucket) and one for the whole-period headline (New, Returning, Total with the New−Returning de-dup applied).
- Data lives in a dedicated returning-customers analytics collection, upserted per order event; each document stores the precomputed `customer_orders`, plus `status` / `status_fulfillment` used for the query-time filter. The document `date` is the order's `date_added` rounded to the start of the hour in UTC, so buckets snap to the hour; the date-range picker shifts the merchant's local from/to into UTC before matching. The query uses the `idx_dashboard` index on `[site_id, date, status, status_fulfillment]`.
- The `returning-customers` entry in the default layout (with `disabled: true`) exists for backwards compatibility and never resolves to its own endpoint or card.

## Related

- [[analytics]] — parent hub.
- [[analytics-total-customers]] — the Total Customers box that hosts this New/Returning split.
- [[customer]] — entity definition.
- [[customers]] — customer list page where merchants filter by order history.
- [[subscriber-vs-customer]] — customer / guest / subscriber distinction; relevant because guests are excluded here.
- [[settings-statuses]] — the used-statuses filter this box depends on.
- [[analytics-top-categories-by-sales]], [[analytics-top-brands-by-sales]] — peer Orders-area boxes.

## Open questions

_None._
