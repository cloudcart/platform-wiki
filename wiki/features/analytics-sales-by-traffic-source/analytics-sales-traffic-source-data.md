---
type: feature
nav_path: "Analytics → Sales by traffic source (referral) → Data source & pipeline"
route_name: analytics
route_path: /admin/analytics
aliases: ["Sales by traffic source data source", "Sales by traffic source pipeline", "orders_referer collection", "Sales by referral aggregation", "amount_without_shipping rule"]
tags: [analytics, ccanalytics, orders, traffic, sales-by-traffic-source]
plan_gates: []
created: 2026-06-10
updated: 2026-11-09
source_count: 12
---

> Part of [[analytics-sales-by-traffic-source]]. See the hub for related aspects (UI surfaces, attribution capture).

# Sales by traffic source — data source & pipeline

## Purpose

Documents **where the box's numbers come from and how they are computed**: the source collection, the order-status filter, the shipping-excluded amount rule, the device split, and the four query shapes (Dashboard / Details / ViewMore / counts) that back the surfaces in [[analytics-sales-traffic-source-ui]]. The per-order referer values consumed here are captured upstream — see [[analytics-sales-traffic-source-attribution]].

## Where to find it

No dedicated UI — this is the back-end machinery behind the "Sales by traffic source (referral)" dashboard box. The merchant influences it only through the **Settings → Analytics → Order statuses** selection (see below) and the period / compare pickers on the dashboard.

## What the merchant can do here

- Understand why revenue in this box differs from totals elsewhere (shipping is excluded).
- Know which orders count toward the revenue (the same statuses chosen in Settings → Analytics).
- Understand why very long periods can time out (504) and need to be narrowed.

## What the merchant sees

The merchant sees only the aggregated output — ranked revenue rows, the Details table, and the ViewMore chart described in [[analytics-sales-traffic-source-ui]]. This page explains the numbers behind those rows.

## Settings & fields

The only merchant-facing control is **Settings → Analytics → Order statuses**, which feeds the status filter applied to every query (see Business rules). The box itself has no per-merchant or per-store data overrides.

## Business rules

### Status filter — driven by the dashboard's Settings panel

The match filter applied to every query incorporates the merchant's used-statuses-by-type list. The set of order statuses included in revenue and order counts is **the set chosen under "Order statuses that will be included in the analyses"** in the panel the **Settings** button (cog icon) opens on the Analytics dashboard ([[analytics-overview-settings]]) — there is no per-box override. This is the standard "depend on selected order statuses in Settings" rule from the box tooltip.

### Amounts are `amount_without_shipping`

`aggregate` is summed from `amount_without_shipping` and divided by 100 (cents → currency units) in the final stage. This is the order total; only shipping the receiver pays the courier directly is taken off, as in the other Orders-tab boxes ([[analytics-total-sales-order-filter]]).

### Views / Sessions and Conversion rate (Details)

The Details table and its export add two columns per row:

- **Views / Sessions** — arrivals from the visits side, the data behind [[analytics-sessions-by-traffic-source]]: one per visitor per hour for each outside source (a referring site, or none for **Direct**) and set of UTM tags. Navigation inside the store is not counted. A row gets the arrivals whose `{group}-{name}` label equals its own, in the same period.
- **Conversion rate** — the row's orders ÷ its views × 100, or 0 when it has no views. It can exceed 100%.

Orders and visits meet only through that label, never per visitor. The visits side labels an arrival by the referring site and the UTM tags alone: it never reads click IDs or `utm_source=cloudcart`. So the order rows **Google Ads …**, **Meta Ads**, **TikTok Ads** and **CloudCart** never find a visits row with their label and always show 0 views and 0.00% conversion, while their orders and amounts count normally. Those visits are counted under the referring site's row, or under **Direct**. How an order gets its label is on [[analytics-sales-traffic-source-attribution]].

### Mobile / desktop split

Each row carries a `device` object: `{ mobile, desktop, total }`. Total equals the sales count for that referer. Used by the tooltip to show "Orders: {total}" with the per-device subdivision.

### Filter narrowing — `ids` parameter

When the merchant filters the Details screen by specific referer keys, the `ids` list is passed through to a `referer_key in [ids]` filter. Otherwise the match is `referer_key != null` (any non-null referer key counts).

### Apply scope — platform-wide, no overrides

This box has no per-merchant or per-store overrides. The same status filter, the same `idx_dashboard` index hint, and the same shipping-excluded amount rule apply to every store on the platform.

## How it works

### Data source

The backend aggregates from the `analytics.orders_referer` collection on the `the analytics store-analytics` connection, hinted with `idx_dashboard`. Each document represents one order with its referer attribution attached (referer_key, referer_name, referer_group, device, amount_without_shipping). Those attribution fields are written upstream by the storefront session middleware — see [[analytics-sales-traffic-source-attribution]].

### Drill-down levels (verified against backend)

| Level | Method | Returns |
|-------|--------|---------|
| Dashboard | Dashboard query | Top 5 referers (`TABLE_RECORDS_LIMIT`) |
| Details | Details query | Full paginated table (page size 100) of all referers in the period |
| ViewMore | ViewMore query | Per-date series for one referer key |
| Details export | Details export query | Same as Details but unpaginated (for CSV export) |
| ViewMore export | ViewMore export query | Same as ViewMore but unpaginated |

ViewMore intervals are pre-generated date buckets, capped at `DETAILS_FORCE_LIMIT = 1000` buckets if the chosen period would generate more (force-limit toggle on the paginator).

### Pipeline shape (Dashboard)

The aggregation is a 6-stage pipeline:

1. Match — date window + status filter + `referer_key` filter.
2. Group by `referer_key` — sums `amount_without_shipping`, counts orders, splits by device, picks first `referer_name` and `referer_group`.
3. Sort — `aggregate` DESC, `sales` DESC.
4. Limit — top 5.
5. Add-fields — builds the `device` object, sets `viewMore = referer_key`, divides amount by 100, packs `meta.row1 = sales`.
6. Project — drops `_id`.

The aggregation is run with `allowDiskUse: true` and `hint: idx_dashboard`.

### Pipeline shape (Details vs Dashboard)

Almost identical to Dashboard but:

- No limit stage (the box paginates externally via skip + limit per page).
- Field names are slightly different: `page_name` and `page_help` (instead of `name` and `group`) — that's because the Details screen's column key is `page_name`.

### Pipeline shape (ViewMore)

ViewMore aggregates over the same collection but groups by **date bucket** (hourly / daily / weekly / monthly / yearly per period picker). Each row in the output is a date bucket for a single `referer_key`. The aggregated buckets are zip-joined back to the pre-generated intervals collection so date holes (periods with zero orders) still appear as zero-rows.

### Count for pagination

The details-count query runs a two-stage group (group by `referer_key` then count) so the paginator gets the **distinct referer count** for the period.

## Related

- [[analytics-sales-by-traffic-source]] — hub.
- [[analytics]] — chooses which order statuses count for revenue.
- [[analytics-details]] — the paginated Details screen this pipeline feeds.
- [[order]] — entity page for orders.
- [[order-status-workflow]] — status set definitions used by the status filter.

## Open questions

_None._
