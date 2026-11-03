---
type: feature
nav_path: "Analytics → Average Order Value"
route_name: analytics
route_path: /admin/analytics (box rendered on Dashboard)
aliases: ["Average Order Value", "AOV", "Order value over time", "Средна стойност на поръчките", "Средна стойност на поръчките за периода"]
tags: [analytics, ccanalytics, orders, average-order-value, aov]
plan_gates: []
created: 2026-05-22
updated: 2026-06-10
source_count: 6
---
# Average Order Value

## Purpose

The **Average Order Value (AOV)** box answers: **"On average, how much does a single order in my store earn me?"** It is the third pillar of the headline trio (alongside [[analytics-total-sales]] and [[analytics-total-orders]]) and the box every merchant looks at when wondering whether to push **upsells / cross-sells / minimum-for-free-shipping** thresholds.

It is the total value of orders in the selected period divided by the number of those orders. The average is computed directly by the analytics layer as a true mean, not derived in the browser from the other two boxes.

This is box `navigationSort: 8` in the default dashboard layout (Sales-focused, second row).

## Where to find it

Sidebar → **Analytics** → AOV card on the Dashboard.

The card's title reads **"Average Order Value"** (the title stays English even in the BG translation; the rest is localised). The subtitle reads **"Order value over time"** / **"Средна стойност на поръчките за периода"**.

The box key is `average-order-value`. The box type is `chart` (line chart). The route is `/admin/analytics`.

## What the merchant can do here

- A **big amount** at the top — the average order value for the whole selected period, in store currency.
- A **comparison delta** when the Dashboard `compare` control is set to `period` or `year`.
- A **line chart** of AOV across time buckets. The Y-axis is money, the X-axis is the time bucket. Hover any point to see that bucket's average, its order count, and the date range.
- An **industry-compare** badge (`hasIndustryCompare: true`) — *"For period <period> Average Order Value: <value> where is <percent> above the average for <industry>"* — when the plan allows.

No drill-down Details view is configured on this box (`hasDetails` is not set — the box is view-only).

### Card tooltip

**English:** *"Total value of all orders divided by total number of orders, depend on selected order statuses in Settings."*

**Bulgarian:** *"Общата сума на всички поръчки, разделена на броя поръчки. Данните се визуализират спрямо избраните статуси на поръчки в Настройки."*

## Settings & fields

### Time-range and grouping

Same Dashboard-wide date-range picker and auto-grouping as the other Orders boxes. Shortcuts: Today / Yesterday / Last 7 days / Last 30 days / Last 90 days / Last month / Last year / Previous month / Previous year / Custom.

Auto-group buckets:

| Range length (days, inclusive) | Bucket |
|--------------|--------|
| < 3 | hourly |
| 3 – 60 | daily |
| 61 – 90 | weekly (NOT daily) |
| 91 – 730 | monthly |
| > 730 | yearly |

### Comparison options

| Value | Effect |
|-------|--------|
| `no` | No comparison |
| `period` | vs. the immediately-preceding period |
| `year` | vs. the same period one year earlier |

Plan-gated.

### Chart tooltip rows

| Field | Shown as |
|-------|----------|
| `amount` | the bucket's AOV, money-formatted |
| `count` | orders in the bucket |
| `date` | bucket date |

The chart tooltip template reads: *"{amount} for {date} from {count} order|{amount} for {date} from {count} orders"* (pluralised by order count).

### Hypothetical details columns (not currently exposed)

The frontend config defines detail-row labels and formatters for `amount`, `orders`, `discount_amount`, `products_discount_amount`, `tax_amount`, `vat_amount`, `shipping_amount`, and `shipping_discount_amount` — but because `hasDetails: true` is not set on the box, the Details view never appears in the UI. This is wired-but-disabled scaffolding for a future drill-down. (Verify with product before promising merchants details access.)

## Business rules

### Calculation

- **Per-bucket value (each chart point)** is the mean order amount within that bucket.
- **Headline value (the big number)** is the total order amount across the whole period divided by the total order count — a correct **weighted mean**, not the simple average of the chart points.

Because the chart points are per-bucket means, they will not visually average back to the headline when buckets hold different numbers of orders. The headline is always exact regardless of bucketing.

The amount used is `amount_without_shipping` — the same field as [[analytics-total-sales]]. So AOV reflects **product subtotal + product discounts + VAT**, but **not shipping**. A store that wants shipping in AOV would need a custom dashboard (not exposed).

**Period-compare math**: the same formula runs on each window. A window with zero orders is forced to `0` (no division-by-zero). The compare arrow shows ±100% when one window is zero and the other non-zero, never infinity.

### Order-status filter

Identical to all other Orders boxes — uses the analytics-counted-statuses config (default: `paid`, `completed`, `pending`, `authorized`, `fulfilled`). See [[settings-statuses]] / Analytics settings.

Same hidden expansion rules: `pending` matches only when fulfillment is `not_fulfilled`; `fulfilled` orders match unless their financial status was explicitly de-selected.

**Industry comparison** uses its own hardcoded status filter (`paid`/`completed`/`authorized` + `pending`+`not_fulfilled` + `fulfilled`). Each store's AOV (total amount ÷ order count) is averaged across stores in the same industry.

### Currency, decimals, empty state, cache

- **Currency / units**: store currency only. No FX.
- **Decimals**: the headline AOV is **not** rounded or ceiled here. (The `aov` helper used by [[analytics-percentage-of-orders]] / Sales Distribution does ceil — a different path.)
- **Date boundary**: ranges are parsed and bucketed in the store timezone.
- **Empty state**: the headline shows `0` (e.g. `0.00 BGN`) when there are no orders; a bucket with no orders renders as `0` on the chart.
- **Filter scope**: not channel-filtered.
- **Cache TTL**: none.

## How it works (verified against backend)

The box runs a single analytics query against the per-order summary data — no Details or ViewMore path.

It applies the status-aware order filter, groups by the auto-bucket (yielding both a per-bucket sum+count and a per-bucket average), and returns points sorted by date ascending so the chart reads left-to-right. Each point carries `date`, `amount` (the bucket's average), `total_amount`, and `count`. The read reuses the same index as [[analytics-total-sales]], so it is fast.

The display wires `text1` → the headline AOV (money-formatted), `text2` → the compare percentage, and `text3` → the compare delta amount.

## Recommended merchant use

Watch this box when:

- Considering raising / lowering a **free-shipping threshold** — if AOV is below the threshold, raising it pressures more customers below it; if AOV is above, the threshold is "soft".
- Pricing-strategy review — sustained AOV drops with stable order count usually mean buyers are shifting to cheaper products / smaller carts.
- A/B-testing cross-sells or upsells — set a tight range around the test window and compare to the immediately-preceding equal period.
- Promotion-discount-impact check — a sale that drops AOV but lifts Total Orders is doing what it should; a sale that drops both is leaking margin without driving volume.

Pair with:

- [[analytics-total-sales]] + [[analytics-total-orders]] for the classic "is growth from price or volume?" diagnosis.
- [[analytics-percentage-of-orders]] (Sales distribution) to see WHERE the average sits inside the order-size histogram.
- [[analytics-top-order-product-discounts]] to find discounts dragging AOV down.

## Related

- [[analytics]] — parent hub.
- [[analytics-total-sales]] — the numerator.
- [[analytics-total-orders]] — the denominator.
- [[analytics-percentage-of-orders]] — order-amount distribution.
- [[analytics-customer-value]] — same shape but divides by unique customers, not order count.
- [[analytics-details]] / [[analytics-more-details]] / [[analytics-full]] — drill-down pages.
- [[settings-statuses]] — which statuses count.
- [[order]] — entity.
- [[plan-gates]] — `cc_analytics.allow_industry_compare`, `cc_analytics.allow_period_compare`.

## Open questions

_None._
