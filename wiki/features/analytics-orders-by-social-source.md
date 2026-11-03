---
type: feature
nav_path: "Analytics → Sales by Source / Medium"
route_name: analytics
route_path: /admin/analytics
aliases: ["Sales by Source / Medium", "Sales by Source/Medium", "Sales by Source / Medium / Campaign", "Orders by social source", "UTM sales", "UTM source medium campaign", "Продажби по източник / средство", "Продажби по utm"]
tags: [analytics, ccanalytics, orders, traffic, utm, orders-social-source]
plan_gates: []
created: 2026-05-22
updated: 2026-06-10
source_count: 10
---
# Sales by Source / Medium

## Purpose

Answers **which marketing channels actually drive purchases?** Ranks orders by the **`utm_source` / `utm_medium`** the visitor first arrived with ("facebook / cpc", "google / organic", "newsletter / email"), then drills deeper into the **`utm_campaign`** that caused the click, so sales attribute to specific named campaigns — not just channels.

It is one of the deepest drill-downs in Analytics: six views (Dashboard → Details → SubDashboard → SubDetails → MoreDetails → ViewMore), more than most boxes.

Tooltip (EN / BG): *"Total sales of orders, grouped by the type of traffic source per device linked them to your online store, depend on selected order statuses in Settings."* / *"Общо продажби от поръчките, групирани по типа източник на трафик на устройство, който ги е довел до Вашия онлайн магазин. Данните се визуализират спрямо избраните статуси на поръчки в Настройки."*

## Where to find it

Analytics dashboard. Box title **"Sales by Source / Medium"** (EN+BG identical). `navigationSort` is 20 — sits next to **Sales by traffic source (referral)** ([[analytics-sales-by-traffic-source]]). The Details title is the templated **"Sales by {details}"** (the clicked source); the ViewMore breadcrumb reads **"Sales by Source / Medium / Campaign"**.

## What the merchant can do here

- See the **top 5 sources** (utm_source / medium) by order revenue on the dashboard, with a device split.
- Open **Details** — paginated list of every source that produced orders.
- Click a source → **SubDashboard** — top 5 `full_source` values (source + campaign tail) under it.
- Drill to **SubDetails** — paginated full list of full_sources under one source.
- Drill to **MoreDetails** — reverse drill: for one full_source, which sources contribute (paginated).
- Drill to **ViewMore** — per-date time-series for one full_source, with `utm_campaign` surfaced as a `campaign` field per date bucket, plus the area-line chart.
- Filter by specific referrer hosts (multi-select), export each level to CSV, compare against the previous period.

## What the merchant sees

Each dashboard row is one **`source`** (a `utm_source / utm_medium` pair, e.g. `facebook / cpc`). The amount is total revenue attributed to that source in the period; the meta-row shows the orders count, formatted "Order X / Orders X" (EN) / "Поръчка X / Поръчки X" (BG), plus a per-device badge (hover → "Orders: {total}").

A row is **only clickable if it has at least one campaign attached** — sources with no `utm_campaign` are non-drillable.

Box-card surfaces:

| Surface | When it appears | What it does |
|---|---|---|
| In-card sub-drill | Click a row with campaigns attached | Swaps body to the source/medium sub-table in the same card; title morphs to "Sales by google". Back-arrow returns. |
| Per-row **View more** link | Each row with viewMore data | Routes to [[analytics-full]] for that source — Source / Medium / Campaign breakdown + inline time-series chart. |
| **View details** link (top-right) | Items > 0 | Opens [[analytics-details]] for the full table. |
| No-data state | Empty range | "No data available for the selected range." |
| 504 timeout | API HTTP 504 | "We cannot generate statistics for the selected period, please reduce it." |

This box does **not** show a data-cutoff alert and has **no** industry comparison.

### Details / ViewMore columns

Both the Details (per-source) and ViewMore (per-date) tables use the same columns; default Details sort is **sales DESC**:

| Column key | EN label | BG label |
|---|---|---|
| `page_name` / `date` | Name / Date | Заглавие / Дата |
| `orders` | Orders | Поръчки |
| `amount` | Amount | Сума |
| `views` | Visitors / Sessions | Посещения / Сесии |
| `conversion_rate` | Conversion rate | Conversion rate |

### Dashboard Settings panel (cog icon)

- **Order statuses** — controls which orders are summed (see Business rules). Default: Paid, Completed, Pending, Authorized payment, Fulfilled. Applies at next refresh.
- **Show devices** — toggling OFF hides per-row device badges.
- **Show boxes sort** — drag/visibility tree. The sibling **Traffic by Source / Medium** box (`sessions-by-social-source`) may be registered as a child here → the title becomes a dropdown to switch between Sales and Traffic in the same card.
- **Reset to default / Save / Cancel** — dashboard-wide.

## Settings & fields

Box config keys: `key` = `orders-social-source`; `type` = `table`; `viewMore`, `hasDetails`, `hasViewMoreChart` all true; `navigationSort` = 20; Details default sort = `sales` DESC; ViewMore groups by date bucket.

## Business rules

### `source` and `full_source` are UTM strings, not domains

A common misread is to assume `full_source` is a referrer domain. It is not. Both fields are built only from the UTM tags on the URL the buyer first arrived through:

| Field | How it's built | Example |
|---|---|---|
| `source` | `<utm_source> / <utm_medium>` | `facebook / cpc` |
| `full_source` | `<utm_source> / <utm_medium> / <utm_campaign>` | `facebook / cpc / spring_promo` |

Missing UTM components are substituted with `--`. **Orders with no UTM tags at all are skipped entirely** — an organic visitor who later buys does NOT appear here, only in [[analytics-sales-by-traffic-source]] (the referer-host box). Because the row label is a `source / medium` pair, two visitors who clicked the same Facebook campaign with different mediums (cpc vs paid-social) show as separate rows.

### Drill identity is the UTM string, not a host

The drill-down identifier is the `source / medium` string for SubDashboard / SubDetails, and the full `source / medium / campaign` string for MoreDetails / ViewMore. The frontend passes these verbatim — so any change to UTM tagging by the merchant creates a **new** row rather than merging into the old one.

### Order-status filter

Every view (Dashboard, Details, SubDashboard, SubDetails, MoreDetails, **and** ViewMore) honours the merchant's chosen analytics statuses from **Settings → Analytics → Order statuses** — the same set as every other Orders-tab box. ViewMore here keeps the status filter, unlike Landing-pages-by-sales ViewMore which drops it (see [[analytics-landing-pages-by-sales]]).

### Amounts exclude shipping

`amount` is the sum of order totals **without shipping** — same convention as the rest of the Orders-tab boxes. Shipping fees are excluded.

### Referrer-host filter

When a `referrerHosts` selection is passed, results are restricted to those source / full_source values; without it, all non-null sources are included.

### Six-view drill-down (verified against backend)

| View | What it returns |
|---|---|
| Dashboard | Top 5 sources by amount |
| Details | Paginated full list of sources |
| SubDashboard | Top 5 `full_source` for one chosen source |
| SubDetails | Paginated full_source list for one source |
| MoreDetails | Paginated sources contributing to one full_source (reverse drill) |
| ViewMore | Per-date time-series for one full_source (with `campaign`) |

This shape is rarer than the standard 3-level pattern: Sales by Source / Medium is one of the only boxes with both SubDashboard / SubDetails AND a parallel MoreDetails reverse-drill.

## Related

- [[analytics]] — parent hub; also chooses which order statuses are counted.
- [[analytics-sales-by-traffic-source]] — sibling box, ranks referers (no UTM drill).
- [[analytics-landing-pages-by-sales]] — sibling box, ranks landing pages.
- [[analytics-full]] — per-source Source / Medium / Campaign breakdown view.
- [[analytics-details]] — the full per-source table.
- [[apps-google-analytics]] — external analytics integration.
- [[order]] — order entity page.

## Open questions

_None._
