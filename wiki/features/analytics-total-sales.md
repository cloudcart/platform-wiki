---
type: feature
nav_path: "Analytics → Total Sales"
route_name: analytics
route_path: /admin/analytics (box rendered on Dashboard)
aliases: ["Total Sales", "Sales over time", "Общи продажби", "Продажби за периода"]
tags: [analytics, ccanalytics, orders, total-sales]
plan_gates: []
created: 2026-05-22
updated: 2026-06-10
source_count: 8
---
# Total Sales

## Purpose

The **Total Sales** box answers the merchant's most fundamental commercial question: **"How much money did my store make in this period?"** It is the headline revenue number on the Analytics Dashboard — a single big amount summing every order that fell within the selected date range and matched the store's "analytics-counted" order statuses, plus a line chart showing how that revenue is distributed across the period (hourly for short ranges up to yearly for long ones, chosen automatically).

This is the first box in the default dashboard layout (`navigationSort: 0`) and the box every merchant looks at first when opening Analytics.

This page is the **hub** for the Total Sales cluster. The mechanics that need detail — which orders count, comparison math, the industry-compare badge, and the per-order drill-down — each live on a dedicated aspect page listed below.

## Where to find it

Sidebar → **Analytics** → top-left card on the Dashboard.

The card's title reads **"Total Sales"** (only the title is kept in English in the BG translation; subtitle and tooltip are localised). The subtitle reads **"Sales over time"** / **"Продажби за периода"**.

The box key is `total-sales`. The box type is `chart` (line chart). The route is `/admin/analytics`. Clicking the card or its "Details" action opens the deep-dive views described under [[analytics-details]] / [[analytics-more-details]] / [[analytics-full]].

## What the merchant can do here

- Read a **big amount** in store currency — total revenue for the selected range (orders' `amount_without_shipping` summed; see [[analytics-total-sales-order-filter]] for the exact field).
- See a **comparison delta** (percentage + arrow) versus the previous period or previous year when comparison is enabled — see [[analytics-total-sales-comparison]].
- Read a **line chart** spanning the range; hover any point for the exact amount, order count, and date label.
- See an **industry-compare** indicator when the plan allows it (`hasIndustryCompare: true`) — see [[analytics-total-sales-industry-compare]].
- **Drill down** (`hasDetails: true`) into the per-line breakdown of everything that contributed to the period's total — see [[analytics-total-sales-details]].
- Use **"View more"** to pivot into the [[analytics-top-order-products-by-units-sold]] box (`viewMore: 'top-order-products-by-units-sold'`) — "OK, I sold X — but WHICH products drove it?".

### Card tooltip (the (?) icon)

**English:** *"Total amount sales plus taxes and shipping, depend on selected order statuses in Settings."*

**Bulgarian:** *"Общата сума на продажбите включително такси и доставки. Данните се визуализират спрямо избраните статуси на поръчки в Настройки."*

Note: the tooltip says "includes taxes and shipping", but the backend sums `amount_without_shipping` — the verified field is documented on [[analytics-total-sales-order-filter]].

## Settings & fields

The box has **no settings of its own**. It is driven by the Dashboard-wide controls:

- The shared **date-range picker** (component `DateRangePicker.vue`) and the resulting **auto time-bucket grouping** — see [[analytics-total-sales-comparison]].
- The Dashboard **"Compare" selector** (`no` / `period` / `year`) — see [[analytics-total-sales-comparison]].
- The merchant's **analytics-counted order statuses**, edited under **Settings → Analytics settings** — see [[analytics-total-sales-order-filter]] and [[settings-statuses]].
- All money is in store currency only; the pipeline does not convert. Empty periods render a flat zero chart with no special "no data" card.

## Business rules

The non-obvious behaviour is split across the aspect pages; the cross-cutting rules are:

- **Which orders and which money count** is governed by the merchant's analytics-status configuration and a hidden status-vs-fulfillment expansion — see [[analytics-total-sales-order-filter]].
- **The headline is not channel-filtered** — a multi-channel store sees the aggregate across all channels.
- **No the application framework-level cache** — the Dashboard queries the analytics store live; freshness is the lag of the per-order ingestion job into the pre-rolled summary collection.
- **"View more" pivots away** — it opens [[analytics-top-order-products-by-units-sold]], not a "more details" view of Total Sales.

## Sub-pages (in this cluster)

- [[analytics-total-sales-order-filter]] — which orders count (analytics-status list + hidden status/fulfillment expansion), which money field is summed, and the pre-rolled storage layout.
- [[analytics-total-sales-comparison]] — the date-range shortcuts, automatic time-bucket grouping, and the `period` / `year` comparison math.
- [[analytics-total-sales-industry-compare]] — the industry-average benchmark badge, its weekly/UTC data source, and why it can disagree with the headline.
- [[analytics-total-sales-details]] — the per-line drill-down table, its columns, the 1,000-row cap, and the Export fallback.

## Recommended merchant use

Look at this box first whenever:

- Reviewing a campaign's commercial impact — set the range to the campaign window and compare to the previous period.
- Year-over-year planning — set the range to "Previous year" with compare to `year`.
- Health check after a price change or promotion — set range to "Last 7 days" with compare to `period`.

Then pivot to [[analytics-top-order-products-by-units-sold]] (which products drove revenue), [[analytics-total-orders]] (order count vs amount), or [[analytics-average-order-value]] (whether AOV moved).

## Related

- [[analytics]] — parent hub.
- [[analytics-total-orders]] — sibling box, counts orders instead of summing money.
- [[analytics-average-order-value]] — Total Sales / Total Orders.
- [[analytics-customer-value]] — revenue per unique customer.
- [[analytics-top-order-products-by-units-sold]] — the **"View more"** target.
- [[analytics-details]] / [[analytics-more-details]] / [[analytics-full]] — drill-down pages.
- [[settings-statuses]] — where the merchant defines which order statuses count as "analytics-visible".
- [[order]] — entity backing every row.
- [[order-status-workflow]] — how an order moves through statuses.
- [[plan-gates]] — `cc_analytics.allow_industry_compare`, `cc_analytics.allow_period_compare`, `cc_analytics.compare_range`.

## Open questions

_None._
