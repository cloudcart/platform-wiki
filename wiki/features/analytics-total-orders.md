---
type: feature
nav_path: "Analytics → Total Orders"
route_name: analytics
route_path: /admin/analytics (box rendered on Dashboard)
aliases: ["Total Orders", "Order count", "Total sales over time", "Общ брой поръчки", "Общи продажби за периода"]
tags: [analytics, ccanalytics, orders, total-orders]
plan_gates: []
created: 2026-05-22
updated: 2026-05-27
source_count: 7
---
# Total Orders

## Purpose

The **Total Orders** box answers: **"How many orders did my store receive in this period?"** Where [[analytics-total-sales]] tells the merchant the **money**, this box tells them the **volume** — the count of orders that matched the store's analytics-counted statuses inside the selected date range.

It is the second box in the default dashboard layout and the companion to Total Sales: together they show whether revenue moves are driven by **more orders** or **bigger orders** (AOV).

## Where to find it

Sidebar → **Analytics** → second box on the Dashboard (right of Total Sales). Route: `/admin/analytics`. The box key is `total-orders`; it renders as a line chart.

The card title reads **"Total Orders"** (kept in English even in the BG translation). The subtitle reads **"Total sales over time"** / **"Общи продажби за периода"** — note the subtitle re-uses Total-Sales wording, a translation quirk in the source.

## What the merchant can do here

- A **big count** at the top of the card — the number of orders for the selected range (integer, number-formatted).
- A **comparison delta** (percentage + arrow) when the Dashboard's `compare` selector is `period` or `year`.
- A **line chart** of order volume across the period, time-bucketed automatically (hourly / daily / weekly / monthly / yearly — see Settings & fields).
- A **drill-down** to the Details table — one row per order, with the order-header financial breakdown columns (not per-line — for per-line use Total Sales' Details).
- An **industry comparison** badge when the plan allows — *"For period <period> Total Orders: <value> where is <percent> above/below the average for <industry>"*.

### Card tooltip

**English:** *"Total number of orders, depend on selected order statuses in Settings."*

**Bulgarian:** *"Общ брой поръчки. Данните се визуализират спрямо избраните статуси на поръчки в Настройки."*

## Settings & fields

### Time-range options

Same Dashboard-wide date-range picker as Total Sales. Built-in shortcuts: Today / Yesterday / Last 7 days / Last 30 days / Last 90 days / Last month / Last year / Previous month / Previous year / Custom.

### Auto group-by

| Range length (days, inclusive) | Bucket |
|--------------|--------|
| < 3 | hourly |
| 3 – 60 | daily |
| 61 – 90 | weekly (NOT daily) |
| 91 – 730 | monthly |
| > 730 | yearly |

Buckets use **store timezone**, so daily/hourly buckets respect local midnight.

### Comparison

Same three values as Total Sales — `no`, `period`, `year` (Dashboard-wide selector). Industry comparison adds a fourth visual layer when the plan allows.

### Details table columns (drill-down)

When the merchant opens Details, they see one row per order:

| Column | EN label | BG label | Notes |
|--------|----------|----------|-------|
| `date` | Date | Дата | Order date (default sort: asc) |
| `order` | Order | Поръчка | Links to `/admin/orders/details/<id>?preview=1` |
| `subtotal` | Sub total | Междинна сума | Money-formatted |
| `discounts` | Discounts | Отстъпки | Money-formatted |
| `vat_amount` | Vat | ДДС | Money-formatted |
| `tax_amount` | Fees | Такса | Money-formatted |
| `shipping` | Shipping | Доставка | Money-formatted; **set to 0 when the shipping payer is the receiver** (see Business rules) |
| `amount` | Total | Общо | Money-formatted, the headline order total |

## Business rules

### Which orders count

Identical filter to Total Sales:

- Current store only.
- Order `date` within the selected range, with day boundaries parsed in store timezone.
- Order financial / fulfillment status matched against the store's `cc_analytics.statuses` config (default: `paid`, `completed`, `pending`, `authorized`, `fulfilled`). Notable expansions:
  - `pending` matches ONLY when `status_fulfillment = not_fulfilled` — a pending order whose fulfillment moved on is excluded.
  - `fulfilled` matches any financial status EXCEPT statuses the merchant has explicitly removed from the list. A fulfilled-but-cancelled order falls out if the merchant deselected `cancelled`.

Total Orders only counts orders (it does not sum money), so it runs faster than Total Sales over the same range.

### What's NOT included

- **Drafts / abandoned carts** — tracked separately and never counted here.
- **Anonymous orders are NOT excluded** (unlike Total Customers). A guest-checkout order still counts because Total Orders just counts orders.
- **Cancelled / voided orders** — counted only if `cancelled` / `voided` was added to `cc_analytics.statuses` (default config excludes both).
- **Test orders** — there is no "test order" flag; a manually-created test order that matches the status filter WILL be counted. To exclude tests, set them to a non-counted status via the order-status workflow.

### "Shipping payer = receiver" exception in the Details view

In the Details table, `shipping` and the shipping discount are **zeroed out when the shipping payer is the receiver** (`shipping_payer == PAYER_RECEIVER` — cash-on-delivery / receiver-pays-courier). There the shipping cost is paid directly to the courier at delivery, not collected by the merchant, so it is not counted as merchant revenue. The `amount` (Total) column reflects this.

The adjustment is **only applied in Details** — the headline count and chart are unaffected (they only count orders, they don't sum money).

### Default Details sort

Default sort is `date asc` (oldest first); the merchant can re-sort by any column. When many orders share the same date, the underlying row order follows internal order id (roughly creation order).

### Comparison and details

- `compare=period` rebuilds the previous window as the equal-length span ending the day before the current window; `compare=year` shifts back whole years (`N = max(1, ceil(diffInDays/365))`).
- The **Details table does NOT show comparison data** even when `compare=period/year`. It always shows the current-window rows.
- The headline-count compare delta uses custom math: when the previous period is `0` it returns +100% / -100% rather than infinity.

### Date boundary, currency, empty state, cache

- **Date boundary**: day boundaries parsed in store timezone. A DST transition inside the boundary day shifts the window by an hour.
- **Currency / units**: count box — no currency. Money in the Details rows is store currency only.
- **Empty state**: renders zeros and an empty chart; no special "no data" card.
- **Filter scope**: not channel-filtered; aggregates across all sales channels.
- **Cache**: no caching — always queried live; freshness equals the analytics ingestion lag.

### Details pagination cap

100 rows per page, hard cap 1,000 rows (same as Total Sales). Export returns the full set.

### No "View more" pivot

Unlike Total Sales (which pivots to top products), Total Orders has no `viewMore` — the drill-down is just Details.

## Recommended merchant use

Consult this box when:

- Tracking volume growth — is the store getting busier, regardless of price?
- Investigating an unexpected revenue change — pair with Total Sales and AOV: did revenue drop because of fewer orders or smaller ones?
- Operational capacity planning — orders/day in peak vs. off-season. Use the hourly grouping (ranges < 3 days) to find peak hours.

## Related

- [[analytics]] — parent hub.
- [[analytics-total-sales]] — the money companion of this box.
- [[analytics-average-order-value]] — Total Sales / Total Orders.
- [[analytics-percentage-of-orders]] — order-size distribution.
- [[analytics-orders-by-country]] — orders broken down by buyer location.
- [[analytics-customer-value]] — revenue per unique customer.
- [[analytics-details]] / [[analytics-more-details]] / [[analytics-full]] — drill-down pages.
- [[settings-statuses]] — defines which statuses count.
- [[order]] — entity backing every row.
- [[order-status-workflow]] — status flow context.
- [[plan-gates]] — `cc_analytics.allow_industry_compare`.

## Open questions

_None._
