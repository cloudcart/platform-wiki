---
type: feature
nav_path: "Analytics → Sales by location"
route_name: analytics
route_path: /admin/analytics (box rendered on Dashboard)
aliases: ["Sales by location", "Orders by country", "Orders by city", "Geographic sales", "Продажби по местоположение", "Продажби по държава"]
tags: [analytics, ccanalytics, orders, orders-by-country, geography, locations]
plan_gates: []
created: 2026-05-22
updated: 2026-06-10
source_count: 9
---
# Sales by location (Orders by country)

## Purpose

The **Sales by location** box (internal key `orders-by-country`) answers: **"Which countries — and which cities within them — are generating my orders and revenue?"** It is a **ranked table** of the top countries by order amount, with a mobile-vs-desktop split per row and a drill-down chain:

```
Top 5 countries → all countries → cities in one country → orders in one city → trend chart
```

It sits in the geography / segmentation row near the bottom of the Analytics dashboard, alongside the other location boxes.

## Where to find it

Sidebar → **Analytics** → "Sales by location" card.

The card title reads **"Sales by location"** (kept in English in the Bulgarian translation; the body is localised). When the merchant drills into a specific country, the title becomes **"Sales by location {country}"** (e.g. *"Sales by location Bulgaria"*).

Its traffic-side sibling [[analytics-sessions-by-country]] (sessions / visits) can be registered as a child of this card. When it is, the card title turns into a `<select>` dropdown letting the merchant switch between **Sales by location** and **Visits by location** in the same slot.

## What the merchant can do here

The dashboard card shows a **5-row table** — the **top 5 countries** by sales amount in the selected period. Each row shows:

- **Flag / country name** (e.g. "Bulgaria").
- **Orders count** — number of orders from this country (label *"Order {value}|Orders {value}"*, singular/plural picked at render).
- **Sales amount** — sum of order amounts (label *"Sale {value}|Sales {value}"*).
- **Device split** — mobile vs desktop badge (hover tooltip *"Orders: {total}"*).
- **Drill-down chevron** — opens the country's city breakdown (shown only when the country has city data).

There is **no industry comparison** on this box (geographic mix is too store-specific).

### Drill-down layers

1. **Click a country row** → in-card sub-drill showing the **top 5 cities** in that country (same row shape, ranked by amount). Click a city to drill again; use the **back arrow** (top-left) to return to the countries list.
2. **View details** on a country → full paginated list of **all** countries (not capped to 5), opening [[analytics-details]].
3. **View details** on a city → full paginated list of all cities in that country.
4. **View more** → a trend chart of orders + amount per time-bucket for the selected country/city, on [[analytics-full]]. This is the only view of this box that is a chart rather than a table.

### Card states

- **No data** for the range: *"No data available for the selected range."*
- **Timeout** on a large range: *"We cannot generate statistics for the selected period, please reduce it."*
- This box has **no data-collection cutoff** — date ranges back to the store's earliest order are valid (no cutoff alert).

### Card tooltip (dotted, on hover)

**English:** *"Total amount of all orders by location per device on your online store, depend on selected order statuses in Settings."*

**Bulgarian:** *"Общата сума на всички поръчки по местоположение на устройство във Вашия онлайн магазин. Данните се визуализират спрямо избраните статуси на поръчки в Настройки."*

## Settings & fields

### Dashboard Settings panel (cog icon)

- **Order statuses** — directly controls which orders are summed by this box (see Business rules). Changing it changes the numbers on the next refresh.
- **Industry** — no effect here (no industry compare).
- **Show devices** — toggling OFF hides the per-row mobile/desktop badges and tooltips.
- **Show boxes sort** — drag/visibility tree; the `sessions-by-country` sibling can be reordered as a child of this box, which controls the card's title-selector dropdown.
- **Reset to default / Save / Cancel** — dashboard-wide.

### Time-range, grouping, comparison

Same Dashboard date-range picker as all Orders boxes. This is a **table** box — it does not chart over time on the dashboard; the time-bucketed view is the **View more** drill-down. Comparison (`no` / `period` / `year`) applies on the View-more chart, which overlays the previous period as a dashed line.

### Drill-down list columns

The all-countries / all-cities lists and the View-more chart table show:

| Column | EN label | BG label |
|--------|----------|----------|
| Name (country / city) | Name | Заглавие |
| Orders | Orders | Поръчки |
| Amount | Amount | Сума |

The View-more table also has a **Date** (Дата) column per time-bucket.

### Pagination caps

The dashboard view is capped to **5 rows**. The all-countries / all-cities lists paginate at **100 rows per page**, hard-capped at **1,000 rows**; beyond that the merchant must export.

## Business rules

### Which orders count

Same site + date-window + counted-status filter as all Orders boxes. The default counted statuses are `paid`, `completed`, `pending`, `authorized`, and `fulfilled` (editable in the Settings panel — see [[settings-statuses]]). This box **additionally excludes orders with no country**, so orders with no location data never appear.

### Location comes from the SHIPPING address

The country and city are read from the order's **shipping address** (its country and city fields), not the billing address. An order with no shipping address (e.g. a digital-only order with no shipping step) is **skipped entirely** — it contributes no location row. City names are title-cased before storage, so `"sofia"`, `"SOFIA"`, and `"Sofia"` collapse into one row.

### Amount INCLUDES shipping

This box sums the order's **full amount** (goods **plus** shipping fees). So a country's total here is slightly higher than the same country's contribution to [[analytics-sales-by-traffic-source]] or [[analytics-landing-pages-by-sales]], which both strip shipping out. Worth knowing when reconciling totals across boxes.

### What "mobile" means here

The order's device is captured at checkout from the browser's User-Agent. The rule is **mobile OR tablet → "mobile", else → "desktop"** — so **tablets are counted as mobile** here. A buyer who ordered from an iPad shows as "mobile". This differs from [[analytics-sessions-by-device]] (visits side), which keeps tablet as its own category.

## Related

- [[analytics]] — parent hub.
- [[analytics-sessions-by-country]] — traffic-side counterpart (configurable as this card's child).
- [[analytics-total-orders]] — the global order volume this box partitions by location.
- [[analytics-total-sales]] — the global revenue.
- [[analytics-orders-by-social-source]] — traffic-source segmentation peer.
- [[analytics-sales-by-traffic-source]] / [[analytics-landing-pages-by-sales]] — other sales-attribution boxes (these exclude shipping).
- [[analytics-sessions-by-device]] — visits-side device split (tablet kept separate).
- [[analytics-details]] / [[analytics-full]] — drill-down pages.
- [[settings-statuses]] — which order statuses count.
- [[order]] — entity carrying the shipping address that drives location.
- [[geo-targeting]] — per-country logic in CloudCart.
- [[plan-gates]] — `cc_analytics.allow_period_compare`.

## Recommended merchant use

Watch this box for: **planning shipping zones / carriers** (a dominant city may justify a courier-specific contract); **geo-targeted marketing** (top non-domestic countries → translated ads, localised campaigns); **regional promotions** (drill into the top country, target under-performing cities); and **cross-border tax / compliance** (review a foreign country's accumulated sales against a registration threshold, e.g. EU OSS reporting).

Pair with [[analytics-sessions-by-country]] (which countries convert vs only browse) and [[analytics-orders-by-social-source]] (which sources drive a country's orders).

## Open questions

_None._
