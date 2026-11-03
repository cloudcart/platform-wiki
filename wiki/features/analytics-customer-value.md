---
type: feature
nav_path: "Analytics → Customer Value"
route_name: analytics
route_path: /admin/analytics (box rendered on Dashboard)
aliases: ["Customer Value", "Customer Lifetime Value", "CLV proxy", "Order value over time", "Средна стойност на клиент", "Средна стойност на клиент за периода"]
tags: [analytics, ccanalytics, orders, customer-value, customer-lifetime-value]
plan_gates: []
created: 2026-05-22
updated: 2026-06-10
source_count: 9
---
# Customer Value

## Purpose

The **Customer Value** box answers: **"How much revenue does each unique customer generate in this period, on average?"** Where [[analytics-average-order-value]] (AOV) divides revenue by the **number of orders**, this box divides revenue by the **number of unique customers** — a buyer who places 3 orders in the period counts ONCE in the denominator. The result is a **period-bounded Customer Value** that approximates customer lifetime value (CLV) for the chosen window.

It sits in the customer-cohort row of the Dashboard, between Total Customers and AOV. The box key is `customer-value`; the box type is `chart` (line chart).

## Where to find it

Sidebar → **Analytics** → Customer Value card.

The card title reads **"Customer Value"** (kept in English even in the BG UI). The subtitle reads **"Order value over time"** (EN) / **"Средна стойност на клиент за периода"** (BG) — the EN subtitle is recycled from AOV, a translation-source quirk.

## What the merchant can do here

- See a **big headline amount** — the period's whole Customer Value, money-formatted in store currency.
- See a **comparison delta** (percent + up/down arrow) when Dashboard `compare` is set to `period` or `year`.
- Read a **line chart** of Customer Value over time buckets. Tooltip: *"{amount} for {date} from {count} order(s)"*.
- See an **industry-compare badge** when the plan grants it: *"For period {period} Customer Value: {value} where is {percent} above the average for {industry}"*.

There is **no drill-down Details view** (`hasDetails` is not set, so no "View details" link renders). For per-customer breakdowns, pivot to [[analytics-orders-by-country]] or read Total Customers / Total Sales together.

### Card tooltip

**EN:** *"Total value of all orders divided by unique customers, depend on selected order statuses in Settings."*

**BG:** *"Общата стойност на всички поръчки, разделена на уникалните клиенти. Данните се визуализират спрямо избраните статуси на поръчки в Настройки."*

Note: the tooltip phrasing is a simplification — the figure is mathematically equivalent to `total_revenue / unique_customers` but is composed as `AOV × purchase frequency` (see Business rules).

### Box card surface (chart-type)

Beyond the elements listed above, the card also shows:

- **Previous-period delta** (compare = `period` / `year`): "Previous period: {amount}" + trend arrow (up green / down red).
- **No-data state** (empty range): "No data available for the selected range."
- **504 timeout** (API HTTP 504): "We cannot generate statistics for the selected period, please reduce it."

This box does NOT define a `collectDataFrom` cutoff — date ranges back to the store's earliest order are valid, with no cutoff alert.

## Settings & fields

### Dashboard Settings panel (cog icon)

- **Order statuses** — directly controls which orders feed the numerator. Default: `paid` / `completed` / `pending` / `authorized` / `fulfilled`. Changing it re-computes Customer Value on next refresh (statuses applied at query time). Same list as Total Customers, Total Sales, Total Orders, and AOV — see [[settings-statuses]].
- **Industry** — drives the industry-compare benchmark (recompute lag up to 1 week).
- **Show devices** — no effect (this box has no device split).
- **Show boxes sort** — drag/visibility tree; can hide or move the box within the chart-type group.
- **Reset to default / Save / Cancel** — dashboard-wide.

### Time-range and grouping

Same Dashboard date-range picker and auto-grouping as the other Orders boxes. Shortcuts: Today / Yesterday / Last 7 / Last 30 / Last 90 days / Last month / Last year / Previous month / Previous year / Custom.

| Range length | Bucket |
|--------------|--------|
| < 3 days | hourly |
| 3 – 60 days | daily |
| 91 – 730 days | monthly |
| > 730 days | yearly |

### Comparison

`no` / `period` / `year` via the Dashboard selector (plan-gated).

### Chart tooltip formatters

| Field | Format |
|-------|--------|
| `amount` | money-formatted — the bucket's customer value |
| `count` | number-formatted — orders in the bucket |
| `date` | bucket date |

## Business rules

### Calculation

Per time bucket the analytics pipeline computes:

- `avg_order_value` = mean of `amount_without_shipping` over the bucket's orders.
- `purchase_frequency` = bucket order count ÷ bucket unique-customer count.
- `customer_value` = `purchase_frequency × avg_order_value` ≈ average revenue per customer.

The whole-period headline runs the same math without bucketing. This is mathematically equivalent to `total_revenue / unique_customers` over the same orders; it is expressed as a product only because it reuses the same intermediate metrics as the AOV box, which makes auditing and re-running easier. The headline total is truncated to integer scaled minor units.

### Guest / anonymous orders are excluded

Orders with no `customer_id` (guest checkout) are **dropped at ingest** — they are never stored in the customer-value collection. So the order count counts **customer-attributed orders only**, and the unique-customer denominator can never include a null.

Consequence: a store with 80 customer orders and 20 guest orders shows `count = 80`, not 100. Because of this, Customer Value × Total Customers is **non-comparable** with [[analytics-total-sales]] (which counts all orders, including guests). For high-guest-checkout stores, Customer Value will be lower than a naive `Total Sales / Total Customers`.

### Per-order revenue uses `amount_without_shipping`

The revenue numerator is `amount_without_shipping`, which subtracts shipping cost from the order's `price_total` **only when the buyer pays for shipping**. If the merchant pays for shipping (`shipping_payer != receiver`), `amount_without_shipping == price_total`. So a store running free-shipping promotions counts the full order toward Customer Value, while a paid-shipping store carves out shipping — making period-over-period comparisons unreliable when shipping policy changes.

### Order-status filter

Only orders in the merchant-selected analytics statuses count (default `paid` / `completed` / `pending` / `authorized` / `fulfilled`) — identical to all Orders boxes. See [[settings-statuses]].

### Currency

`amount_without_shipping` is stored in scaled minor units (e.g. `12345` = 123.45) in the **store's primary currency**. There is NO multi-currency normalization — secondary-currency orders are converted to primary currency before reaching the collection. For stores that changed their base currency, older buckets may be in the old currency without rescaling, which can produce confusing trends.

### How this relates to "CLV"

True CLV accumulates a customer's whole lifetime across all orders. This box is a **bounded approximation** — Customer Value over the chosen window. For a lifetime-style view, set a wide range ("Last year"+); for early-value, set Last 30 days.

## Recommended merchant use

Watch this box when:

- Assessing **acquisition spend** — if cost-per-acquisition exceeds Customer Value, the channel is unprofitable on a first purchase.
- Designing **customer segmentation** — pair with [[analytics-total-customers]] to see whether high value comes from many small repeat orders or fewer big ones.
- Evaluating **loyalty / re-engagement** — a campaign that lifts purchase frequency raises Customer Value even if AOV stays flat.
- **Annual planning** — range "Last year", compare = `year`.

Pair with [[analytics-total-customers]] (denominator), [[analytics-total-sales]] (numerator), and [[analytics-average-order-value]] (≈ AOV × purchase frequency).

## Related

- [[analytics]] — parent hub.
- [[analytics-total-customers]] — the unique-customer count this box divides by.
- [[analytics-average-order-value]] — one of the two factors in this box's calculation.
- [[analytics-total-sales]] — revenue total.
- [[analytics-total-orders]] — order count (numerator of purchase frequency).
- [[analytics-orders-by-country]] — location-dimension pivot for breakdowns.
- [[settings-statuses]] — which order statuses count.
- [[customer]] — entity backing each customer_id.
- [[plan-gates]] — industry-compare / period-compare gating.

## Open questions

_None._
