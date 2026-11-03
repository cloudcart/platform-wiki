---
type: feature
nav_path: "Analytics → Total Customers"
route_name: analytics
route_path: /admin/analytics (box rendered on Dashboard)
aliases: ["Total Customers", "New vs Returning customers", "Unique customers", "Customers over time", "Общ брой клиенти", "Клиенти за периода"]
tags: [analytics, ccanalytics, orders, total-customers, returning-customers, new-customers]
plan_gates: []
created: 2026-05-22
updated: 2026-05-27
source_count: 6
---
# Total Customers

## Purpose

The **Total Customers** box answers: **"How many unique buyers did my store have in this period, and what's the split between new vs. returning?"** It is the customer-side companion to the order-volume box ([[analytics-total-orders]]) — instead of counting orders, it counts the distinct people who placed them.

The headline is a **single big number** (unique customers) with **two sub-counts** underneath: **New customers** (first-ever purchase at this store) and **Returning customers** (had a prior order before this period). A small line chart shows how each cohort tracks over time. This is `navigationSort: 2` — third box in the default dashboard layout.

## Where to find it

Sidebar → **Analytics** → Total Customers card.

The card's title reads **"Total Customers"** (title shown in English even in the BG admin, body localised). The subtitle reads **"Customers over time"** / **"Клиенти за периода"**.

The box key is `total-customers`. The box type is `chart` (a multi-dataset line chart — one dataset for "new", one for "returning").

## What the merchant can do here

- A **big number** at the top — total unique customers in the selected period (new + returning).
- A **2-column header** below it showing the New / Returning split:
  - **New** / **Нови** — count of first-time customers
  - **Returning** / **Върнали се** — count of repeat customers
- A **line chart** with two datasets superimposed — "new" per bucket and "returning" per bucket. The tooltip per point reads e.g. *"42 new customers"* (pluralised by count, label localised).
- An **industry-compare** badge (`hasIndustryCompare: true`) when the plan allows.

No drill-down Details view configured.

### Card tooltip

**English:** *"Total unique customers, depend on selected order statuses in Settings. Customers made more than one order in your store VS customers made an order into a time frame."*

**Bulgarian:** *"Общ брой уникални клиенти, процентът клиенти, които са направили повече от една поръчка във Вашия магазин и процент клиенти, които са направили само една поръчка в рамките на избрания период от време. Данните се визуализират спрямо избраните статуси на поръчки в Настройки."*

The wording is awkward in both languages; the verified definition is:

- **Returning** = customer who already had at least one **prior** order at the time of this period's purchase — a known customer before this period started.
- **New** = customer with NO prior orders at the time of this period's purchase — first-time-ever buyer.

Both counts are de-duplicated **per customer** (see [[customer]]): a customer who orders 3 times in the period counts once in the appropriate bucket.

## Settings & fields

### Time-range and grouping

Same Dashboard date-range picker and auto-grouping as the other Orders boxes:

| Range length (days, inclusive) | Bucket |
|--------------|--------|
| < 3 | hourly |
| 3 – 60 | daily |
| 61 – 90 | weekly |
| 91 – 730 | monthly |
| > 730 | yearly |

### Comparison

`no` / `period` / `year` via the Dashboard selector (plan-gated). **However — Total Customers does NOT actually produce compare data.** When a merchant selects `period` or `year`, the box still renders only the current period's New / Returning counts. The compare-arrow / delta percentage that other boxes show are absent here. (This is a known asymmetry — other Orders boxes' chart shows two overlaid periods, this one does not.)

### Header columns and label translations

The 2-column header and chart labels use these strings:

| Column | EN | BG |
|--------|------|------|
| New | New | Нови |
| Returning | Returning | Върнали се |

The chart tooltip label is `"{count} {label} customer|{count} {label} customers"` (pluralised by count, label localised).

## Business rules

### How "new" vs "returning" is determined

The decision is fixed **when each order is placed**, not recomputed at view time, from the buyer's **prior order count** at that moment: **0 prior orders** → **new** (first-time-ever buyer); **1+ prior orders** → **returning**. So "new in May 2026" means the customer's very first order was in May 2026 — a customer who first bought in 2024 and re-bought in May 2026 is **returning** in the May box.

**Hidden behavior — the prior-order count ignores status.** It counts every earlier order by the same customer regardless of status, so drafts, cancelled, and refunded prior orders all count toward "returning". A customer with one cancelled prior order is treated as returning on their next purchase, even though that cancelled order is itself invisible to this analytics box.

### De-duplication per customer

Each customer is counted once per period: a customer with 5 orders contributes only 1 to the count. If a customer would qualify as both "new" and "returning" within one period (their first-ever order and a later repeat purchase both fall inside it), the **whole-period total** counts them only as **returning**, never in both buckets. The **per-bucket chart series** does not apply this guard, so per-bucket new/returning numbers may not sum exactly to the header totals in that edge case.

### Anonymous orders are excluded

Orders without a logged-in customer (guest checkouts where no customer record was created) are **silently dropped** from this box. A store with heavy guest checkout will see Total Customers significantly under Total Orders ([[analytics-total-orders]]). Because the data is pre-built by a background ingestion job, a guest order that later has a customer attached only appears here AFTER the next ingestion run.

### Order-status filter

Same as all Orders boxes — only the analytics-counted statuses are included (default: `paid`, `completed`, `pending`, `authorized`, `fulfilled`). Same hidden expansion rules: `pending` requires `not_fulfilled`; `fulfilled` excludes statuses the merchant has DE-selected from the analytics-counted list. See [[settings-statuses]].

**Industry-comparison** uses a HARDCODED status filter (`paid/completed/authorized` + `pending+not_fulfilled` + `fulfilled`) — it does NOT respect the merchant's custom analytics-statuses config. So the industry badge's baseline may differ from the headline calculation.

### Freshness, empty state, scope

- **Currency / units**: count box — no currency.
- **Empty state**: when the period has no qualifying customers, the chart line is flat-zero and the New / Returning header columns show `0`.
- **Filter scope**: not channel-filtered.
- **Freshness**: figures are live (no caching), limited only by how recently the background ingestion job last ran.
- **Date boundary**: parsed and bucketed in the store's timezone.

## Recommended merchant use

Watch this box to:

- Gauge **customer-acquisition campaign** impact — a campaign should lift "New" without hurting "Returning". One that lifts only Returning is a discount/loyalty move.
- Diagnose churn — if Returning trends down while New stays flat or grows, the store is leaking repeat customers faster than it acquires new ones.
- Track loyalty / retention — over a long range (Last year), a growing Returning-vs-New ratio means existing buyers are coming back more.

Pair with [[analytics-customer-value]] (value per unique customer), [[analytics-total-orders]] (orders / customer ratio = purchase frequency), and [[analytics-total-sales]] (revenue per customer = Total Sales / Total Customers).

## Related

- [[analytics]] — parent hub.
- [[analytics-customer-value]] — money side of the customer view.
- [[analytics-total-orders]] — orders per customer.
- [[analytics-total-sales]] — revenue per customer.
- [[analytics-orders-by-country]] — customer locations.
- [[settings-statuses]] — which statuses count toward the customer counts.
- [[customer]] — entity backing each unique customer counted.
- [[subscriber-vs-customer]] — concept clarifying the distinction.
- [[plan-gates]] — `cc_analytics.allow_industry_compare`, `cc_analytics.allow_period_compare`.

## Open questions

_None._
