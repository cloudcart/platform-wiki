---
type: feature
nav_path: "Analytics → Abandoned carts rate"
route_name: analytics
route_path: /admin/analytics
aliases: ["Abandoned carts rate", "Abandoned carts", "Cart abandonment", "Изоставени колички", "Изоставени колички за периода"]
tags: [analytics, ccanalytics, cart, abandoned-carts]
plan_gates: []
created: 2026-05-22
updated: 2026-06-10
source_count: 9
---
# Abandoned carts rate

## Purpose

A merchant-facing chart that shows what **percentage of carts never reached the checkout page** — carts that were started (a customer added something and the cart became active) but where the shopper never advanced to checkout. It is the "early funnel leak" detector: friction inside the cart drawer, unexpected shipping totals shown in the cart, surprise upsells, or distracted visitors who left before they began typing a delivery address.

It pairs with [[analytics-abandoned-checkout]] (the *later* leak — shoppers who reached the checkout page but didn't place the order) and [[analytics-cart-conversion-funnel]] (the whole cart → checkout → order pipeline as one diagram).

## Where to find it

Analytics dashboard → **Abandoned carts rate** box (Bulgarian: "Изоставени колички", subtitle "Изоставени колички за периода"). Box `key: "abandoned-carts"`, box `type: "chart"`, `navigationSort: 6` — it sits mid-dashboard alongside the other cart metrics. Rendered as a percentage headline with an over-time chart underneath.

## What the merchant can do here

- See the **headline percentage** of abandoned carts for the selected period (e.g. "62.5%"), large and prominently formatted.
- Compare to the **previous period** (delta shown next to the headline) — Compare mode is set in the dashboard date picker.
- Compare against an **industry benchmark** (`hasIndustryCompare: true`) — CloudCart aggregates anonymised peer-store rates in the same industry; the merchant's own data is never shared, only the aggregate comes back.
- Hover the chart for per-bucket tooltips: "62.5% — 125 abandoned carts from 200 for 2026-05-22".
- Change the **date range** and **grouping** (hourly / daily / weekly / monthly / quarterly / yearly) — the box re-fetches.
- See a **mobile vs desktop** split in two text rows (icons `fa-mobile`, `fa-desktop`), unless the Show devices toggle is off.

The shared dashboard chrome — the cog **Settings panel** (statuses filter, industry, Show devices, box sort, Save / Reset, `cacheHash`) and the date / Compare picker — is documented on the hub: [[analytics-overview-settings]] + [[analytics-overview-date-compare]]. Box-specific notes:

- This is a **cart-event-driven** box: it reads the cart events feed and is **not** filtered by the "order statuses included in analyses" setting. (Some translations of the statuses tooltip imply otherwise — misleading for this box, accurate for sibling order-based boxes.)
- **No "View details" drill-down** — `hasDetails` is not set on `abandoned-carts`, so the per-bucket table router-link does not render.
- The industry-compare badge uses **reversed polarity** (`reverse: true`): for abandonment, "below the industry average" is the GOOD outcome, so the badge styles below-average as positive.

## Settings & fields

### Box configuration

| Property | Value | Meaning |
|----------|-------|---------|
| `key` | `abandoned-carts` | Unique identifier; matches the backend trait route. |
| `type` | `chart` | Percentage headline + over-time chart. |
| `collectDataFrom` | `2023-01-13` | Earliest date with any cart-abandonment data. Ranges before this return no data. |
| `hasIndustryCompare` | `true` | Industry benchmark available. |
| `navigationSort` | `6` | Display order on the dashboard. |

### Metric definitions

| Term | Definition |
|------|------------|
| **Cart (`unique`)** | Count of distinct `cart_id` values per bucket (`$addToSet` on the cart id). Counted **per cart, not per visitor** — one shopper with two separate carts in the hour counts as 2; one shopper adding 10 items to one cart counts as 1. |
| **Checkout (`uniqueCheckout`)** | Distinct `cart_id` values that fired `initiatedCheckout` in the bucket. Same per-cart dedup. |
| **Total (abandoned)** | `unique − uniqueCheckout` — carts that never reached checkout. |
| **Abandoned carts rate** | `100 − round(checkout / cart × 100, 1)`, rendered by `percentFormat`. Example: cart=200, checkout=125 → `100 − 62.5 = 37.5%`. |

### Device split

The dashboard returns three buckets per period; each carries `cart`, `checkout`, `total`:

| Bucket | Counted when | Shown as |
|--------|--------------|----------|
| `mobile` | `device == 'mobile'` | First row, icon `fa-mobile`. |
| `desktop` | `device != 'mobile'` (incl. tablet) | Second row, icon `fa-desktop`. |
| `total` | All devices | Headline percentage. |

## Business rules

### How "abandoned" is defined

A cart is abandoned if it (by `cart_id`) fired `addToCart` but never fired `initiatedCheckout` **in the same bucket**. `initiatedCheckout` fires the instant the `/checkout` route renders — any path that lands the shopper on the checkout page — so the metric measures shoppers who never reached the checkout **page**, regardless of whether they clicked "Continue to checkout" in the cart drawer. NOT counted as abandoned: reaching the checkout page via that button, via a saved-cart deep-link, or via a single-step Fast Order.

### Per-bucket reckoning (never re-reconciled)

The metric is calculated per bucket, not per visitor lifetime. A shopper who adds to cart in hour A and starts checkout in hour B counts as "abandoned" in A and "checkout" in B — the two are never reconciled. Consequence: **short-period rates (e.g. hourly) tend to be inflated** versus the same data at monthly granularity, because each bucket captures only intra-bucket funnel progression.

### Mobile vs desktop categorisation

The storefront tracker sets `device` to `mobile` / `tablet` / `desktop`. The dashboard groups **everything that is not `mobile` as `desktop`**, so tablet sessions merge into desktop. This matches every Analytics box — a deliberate merchant-facing simplification, not a data limitation.

### Hidden data-loss range — before 17 January 2023

A hard-coded protection block forces the device-split rows (`row1`, `row2`, `total`) to **'N/A'** when the range `from` is before **2023-01-17**, because device-split data was not consistently captured before then. `collectDataFrom` is `2023-01-13`, but device-aware rates are only trustworthy from 2023-01-17. A range straddling this boundary shows N/A in the mobile/desktop rows. Picking a range entirely before `collectDataFrom = 2023-01-13` triggers the yellow alert: "There is no data for the selected period. Please select a period after 13.01.2023 to view data."

### Trend-arrow polarity (verify)

The Vue config does **not** set `reverseColoring`, so the trend arrow renders up = green / down = red. Because lower abandonment is good, an UP arrow (abandonment INCREASED) shows green — a likely UI inversion. (verify intended semantics.)

### Empty / error states

- No cart events for the period (brand-new store, or pre-collection range): box shows `0%` with no chart line.
- HTTP 504 from the API: chart is replaced by "We cannot generate statistics for the selected period, please reduce it." / "Не може да генерираме статистика за избрания период, моля намалете го."

## How it works

The platform stores `addToCart` and `initiatedCheckout` events and aggregates them **once per hour** into precomputed buckets (`date`, `cart`, `checkout`, `total`) per hour × device — so the box can lag a real abandonment by up to an hour. The aggregator excludes admin/test sessions (`uuid_id` matching `^admin-.*`) and skips disabled sites. The box treats all stores uniformly: no per-merchant override of the abandonment definition, device split, or cadence; industry benchmarks aggregate the same metric across the vertical. The hourly read model is shared dashboard-wide — see [[analytics-overview-data-freshness]].

## Related

- [[analytics]] — parent hub for the Analytics area.
- [[analytics-abandoned-checkout]] — the *later* funnel leak (reached checkout, didn't order).
- [[analytics-cart-conversion-funnel]] — the same data as a 3-step funnel (cart → checkout → order).
- [[analytics-cart-conversion-rate]] — site-wide conversion rate (visitors → orders).
- [[analytics-online-store-sessions]] — denominator context: visitor volume in the same period.
- [[analytics-overview-settings]] — the cog Settings panel (statuses, industry, Show devices, box sort).
- [[analytics-overview-date-compare]] — the date-range + Compare picker.
- [[analytics-overview-data-freshness]] — the hourly precomputed-aggregation read model.

## Open questions

- Trend-arrow polarity: confirm whether up = green on this box (abandonment increased shown green) is intended or a UI inversion.
