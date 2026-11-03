---
type: feature
nav_path: "Analytics → Sales by traffic source (referral)"
route_name: analytics
route_path: /admin/analytics
aliases: ["Sales by traffic source", "Sales by traffic source (referral)", "Sales by referral", "Sales by referer", "Referral sales", "Продажби по източник на трафик", "Продажби по реферал"]
tags: [analytics, ccanalytics, orders, traffic, sales-by-traffic-source]
plan_gates: []
created: 2026-05-22
updated: 2026-06-10
source_count: 11
---
# Sales by traffic source (referral)

## Purpose

Answers the merchant's question: **which referring websites send traffic that actually buys?** The box ranks external referers (the domain or service that pointed the visitor at the store) by **total order revenue** in the selected period. Rows are bucketed into coarse referer groups — Search, Social, Email, Paid, News, Payments, Direct, Unknown — so a merchant can quickly see whether sales come from organic search, social channels, ads, etc., without scanning dozens of host names.

Tooltip (EN / BG): *"Total amount of all orders grouped by the type of traffic source, depend on selected order statuses in Settings."* / *"Общата сума на всички поръчки, групирани по източник на трафик. Данните се визуализират спрямо избраните статуси на поръчки в Настройки."*

This page is the **hub** for a 3-aspect cluster. It gives the high-level orientation; drill into the aspect that matches the question.

## Sub-pages (in this cluster)

- [[analytics-sales-traffic-source-ui]] — everything the merchant sees and clicks: dashboard top-5 card, in-card sub-drill, Details table, per-referer ViewMore chart, Settings panel, Vue config, referer-group labels.
- [[analytics-sales-traffic-source-attribution]] — where each order's referer comes from: storefront session middleware, ad-click params (`gclid` / `gad_source` / `fbclid` / `ttclid`), UTM tags, `gad_source` network mapping, first-touch session attribution, `referer_key` composition, the Direct bucket, the internal `campaign` group.
- [[analytics-sales-traffic-source-data]] — the data source and computation: `analytics.orders_referer` collection, the Settings-driven status filter, the shipping-excluded amount rule, device split, and the four query shapes (Dashboard / Details / ViewMore / counts).

## Where to find it

Analytics dashboard. The box title is **"Sales by traffic source (referral)"** in both EN and BG. `navigationSort` is 21 (further down the dashboard). The box opens as a ranked top-5 table; clicking it expands to the Details screen; clicking a referer row drills into a per-date time-series chart. Full surface-by-surface walkthrough in [[analytics-sales-traffic-source-ui]].

## What the merchant can do here

- See the top 5 referring websites by **order revenue** in the selected period.
- Open the **Details** screen — paginated full list of every referer that produced at least one order.
- Drill into a **ViewMore** time-series chart of revenue per date for a single referer.
- Filter Details by specific referer keys, sort, and export to CSV.
- Switch the period and compare against the previous period (dashed overlay line).

For the full interaction catalogue see [[analytics-sales-traffic-source-ui]].

## Settings & fields

The only merchant-facing control is **Settings → Analytics → Order statuses**, which decides which orders count toward revenue (default: Paid / Completed / Pending / Authorized / Fulfilled). There is no per-box override. The Vue config (box `key = sales-by-traffic-source`, `type = table`, `viewMore`, `hasDetails`, `hasViewMoreChart`, `navigationSort = 21`) and the referer-group dictionary are documented on [[analytics-sales-traffic-source-ui]]. The status-filter and amount rules are on [[analytics-sales-traffic-source-data]].

## Business rules

- **Revenue excludes shipping.** Amounts sum `amount_without_shipping` — only the goods portion counts. See [[analytics-sales-traffic-source-data]].
- **Status filter follows Settings → Analytics.** The orders counted are exactly the statuses the merchant chose there; no per-box override. See [[analytics-sales-traffic-source-data]].
- **First-touch session attribution.** A referer is captured on the buyer's first visit and attached to whatever order they eventually place — not the visit on which checkout completed. See [[analytics-sales-traffic-source-attribution]].
- **"Direct" never shows a group chip.** Orders with no referer land in the Direct bucket, whose group label is forced to `null`. See [[analytics-sales-traffic-source-attribution]].
- **Platform-wide, no overrides.** Same status filter, same index hint, same shipping-excluded amount rule for every store. See [[analytics-sales-traffic-source-data]].

## Related

- [[analytics]] — parent hub; chooses which order statuses count for revenue.
- [[analytics-orders-by-social-source]] — sibling box, ranks by source/medium with utm_campaign drill-down.
- [[analytics-landing-pages-by-sales]] — sibling box, ranks landing pages where the order was placed.
- [[analytics-sessions-by-traffic-source]] — the Visits-side counterpart that can share this card slot.
- [[apps-google-analytics]] — separate, external analytics integration.
- [[order]] — entity page for orders.
- [[order-status-workflow]] — status set definitions.

## Open questions

_None._
