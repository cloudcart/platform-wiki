---
type: feature
nav_path: "Analytics → Conversion Funnel"
route_name: analytics
route_path: /admin/analytics
aliases: ["Conversion Funnel", "Cart conversion funnel", "Поведенческа фуния", "Фуния за реализация"]
tags: [analytics, ccanalytics, cart, conversion-funnel]
plan_gates: []
created: 2026-05-22
updated: 2026-05-27
source_count: 7
---
# Conversion Funnel

## Purpose

A 3-step funnel visualisation that ties together the entire purchase journey: **Cart → Initiated Checkout → Orders**. It shows for the selected period how many unique shoppers entered each stage of the funnel and, by visual inspection, where the biggest drop-off is happening.

Where [[analytics-abandoned-carts]] tells you "what percentage abandoned at the cart stage" and [[analytics-abandoned-checkout]] tells you "what percentage abandoned at the checkout stage", **this box puts both transitions on a single chart** alongside the final conversion to a placed order — so you see the leaking funnel as one picture.

## Where to find it

Analytics dashboard → **Conversion Funnel** box. `navigationSort: 5` (sits immediately above the Abandoned-cart and Abandoned-checkout boxes).

Box `key: "cart-conversion-funnel"`, `type: "funnel"` — the only Analytics box that renders as a literal funnel chart (3 horizontal bars, widest at the top, narrowest at the bottom).

## What the merchant can do here

- See the **three funnel stages** in order: Cart, Initiated Checkout, Orders.
- Compare **Desktop vs Mobile vs Total** — the funnel can be filtered or split by device using the box header (Bulgarian: "Desktop", "Mobile", "Total").
- Read each stage's **absolute count** and the **percent-of-previous-stage** progression.
- Change the **date range** in the page-level date picker; the funnel re-fetches.
- (No industry comparison on this box — `hasIndustryCompare` is not set.)

## Settings & fields

### Box configuration (Vue)

| Property | Value | Meaning |
|----------|-------|---------|
| `key` | `cart-conversion-funnel` | Unique identifier for this box. |
| `type` | `funnel` | Renders as a 3-stage funnel chart (not a percentage headline). |
| `collectDataFrom` | `2023-01-13` | Earliest date where cart-funnel data exists. |
| `navigationSort` | `5` | Display order on the dashboard. |
| `funnel.colors` | `[['#8c58df', '#D2BDF1FF'], ['#FF4589', '#fdb42d'], []]` | Per-stage colour pairs: stage 1 purple/light-purple, stage 2 pink/orange, stage 3 default. |

### Funnel stages

| Stage | Label EN | Label BG | What it measures |
|-------|----------|----------|------------------|
| 1 | Cart | Кошница | Unique visitors who added at least one item to the cart in the period. |
| 2 | Initiated Checkout | Започната поръчка | Unique visitors who advanced to the checkout page. |
| 3 | Orders | Поръчки | Unique visitors who completed an order whose status is in the merchant-selected list (see [[analytics]] or settings for status selection). |

### Device groups (selectable in the box header)

| Group | Bulgarian | What it shows |
|-------|-----------|---------------|
| `desktop` | Desktop | Funnel for sessions where `device != 'mobile'` (includes tablet). |
| `mobile` | Mobile | Funnel for sessions where `device == 'mobile'`. |
| `total` | Total | Sum of desktop + mobile (entire store). |

### Tooltip text (exact UI quotes)

The box tooltip reads (English): `"Event sequence data for number of customers reached to the cart, percentage of customers reached to the initiated checkout, and percentage of customers created an order, depend on selected order statuses in Settings."`

Bulgarian equivalent in the language file (where present): same intent — funnel of customers reaching cart → initiated checkout → order, where the "Order" stage depends on which order statuses the merchant has selected in Analytics Settings.

## Business rules

### Stage 3 (Orders) depends on the Order Status filter

The third stage (Orders) is **not all placed orders** — it's only orders whose status is in the **list of statuses the merchant selected in Analytics → Settings** (see [[analytics]]). Default selection typically includes Paid, Fulfilled, Pending, Authorized payment, and Shipped — but the merchant can change this. So:

- Including Cancelled in the selection → cancelled orders count toward the funnel's "Orders" stage (artificially inflates conversion).
- Excluding Pending → real orders that haven't been paid yet appear as "didn't convert" (artificially deflates conversion).

This is also why the on-screen tooltip explicitly says "depend on selected order statuses in Settings" — the merchant needs to be aware of the filter.

### Stage 1 and Stage 2 are NOT filtered by order status

Cart and Initiated Checkout are pure cart-funnel counts from the store's behavioural data. They reflect *what the shopper did in the store*, not what later happened with the order — so the same cart counted in Stage 1 stays counted even if its eventual order is excluded from Stage 3.

### Data source and freshness

Stages 1 and 2 draw from the same cart-analytics data as the Abandoned boxes, refreshed on a 1-hour cadence. Admin sessions are excluded. The Orders stage is counted separately from the orders data and appended to the funnel.

### What counts as Stage 1 vs Stage 2

Stages 1 and 2 are NOT raw visitor counts — they are **deduplicated carts** per hourly bucket:

- **Stage 1 (Cart)** — distinct carts that had at least one add-to-cart in the period. A shopper who adds many items to the same cart in the same hour is counted **once**; a new cart in a later hour is a second count.
- **Stage 2 (Initiated Checkout)** — distinct carts that reached the checkout page. This fires the moment the **checkout page loads** (route `checkout`), NOT when the shopper clicks "Continue to checkout" in the cart drawer. So a shopper who lands on checkout from any entry point (cart, deep-link, abandoned-cart restore email) counts toward Stage 2 — even with no add-to-cart in the period.
- **Stage 3 (Orders)** — count of orders matching the merchant's selected statuses, counted from the moment the order is created (regardless of later status changes).

This is why **Stage 2 can occasionally exceed Stage 1** for a small period: deep-links into checkout, abandoned-cart restore flows, and carts persisting from the previous hour all show up at Stage 2 without a matching same-bucket add-to-cart. Over a long enough window the funnel "evens out", but for short ranges (an hour or a single day) the merchant may see inverted bars.

### Date / timezone semantics

The date range matches on local-day boundaries: ranges are built in the **store timezone**, so the funnel respects the merchant's local day rather than UTC.

### Mobile vs desktop categorisation

Same as elsewhere on the dashboard: `device == 'mobile'` → mobile; everything else (tablet, desktop) → desktop. Tablets are folded into desktop for merchant-facing simplicity.

### No detail drill-down

The funnel box does **not** have a "View details" link (`hasDetails` is unset / `false`). To investigate *which* customers abandoned at which stage, the merchant uses the Abandoned-carts and Abandoned-checkout sub-pages, the Carts list, or the orders list.

### Uniform across stores

The funnel definitions are identical across every CloudCart store. The only per-store difference is which order statuses the merchant has selected as "counted as orders" in [[analytics]].

## Related

- [[analytics]] — parent hub.
- [[analytics-abandoned-carts]] — drop-off between Stage 1 (Cart) and Stage 2 (Initiated Checkout).
- [[analytics-abandoned-checkout]] — drop-off between Stage 2 (Initiated Checkout) and Stage 3 (Orders).
- [[analytics-cart-conversion-rate]] — the same Stage 1 → Stage 3 ratio expressed as a single % over time.
- [[analytics]] — order statuses included in Stage 3.
- [[order]] — entity definition; Stage 3 counts these.
- [[checkout-flow]] — Stage 2 maps to this entity.

## Open questions

_None._
