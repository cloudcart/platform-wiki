---
type: feature
nav_path: "Analytics → Products by traffic → Data source"
route_name: analytics
route_path: /admin/analytics
aliases: ["Products by traffic data source", "Products by traffic attribution", "View deduplication", "What counts as a view", "Продукти спрямо посещения — източник на данни"]
tags: [analytics, ccanalytics, products, traffic, top-products-by-traffic, data-source]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 8
---
> Part of [[analytics-top-products-by-traffic]]. See the hub for the other aspects (UI surface, export).

# Products by traffic — data source & attribution

## Purpose

Explains **what a "view" is** in the Products-by-traffic report and where the numbers come from: the underlying analytics data, the UUID × hour × device de-duplication that prevents page-refresh inflation, the admin-traffic exclusion, the bundles-included default, the drill-down levels, the auto group-granularity rule, and the force-limit caps. Read this for "why does this product show N views?" questions.

## Where to find it

There is no separate screen for this — it describes the data behind the [[analytics-top-products-traffic-ui|Products-by-traffic dashboard box, Details, and ViewMore]] at `/admin/analytics`. `collectDataFrom: '2023-01-01'` — date ranges earlier than 2023-01-01 return no data for any store.

## What the merchant can do here

- Understand exactly which page-view events feed the ranking (and which are filtered out).
- Reason about why repeated visits by the same person within an hour count once.
- Know that bundle products appear in this box alongside regular products by default.
- Predict the time-bucket granularity that ViewMore will use for a given date range.

## What the merchant sees

### Metric definition — what counts as a "view"

A "view" in this box is **one product-page view event** as recorded by the visitor tracking system ([[analytics-pipeline]]), which deduplicates within an hour-uuid bucket: multiple page refreshes within the same hour by the same visitor on the same device count as **one** view.

### Drill-down levels (verified against backend)

| Level | View | Returns |
|-------|------|---------|
| Dashboard | Dashboard query | Top 5 products (`TABLE_RECORDS_LIMIT`) |
| Details | Details query | Full paginated table (page size 100) of all viewed products in the period |
| ViewMore | ViewMore query | Per-date series for one product id |
| Details export | Details export query | Same as Details but unpaginated (CSV export) — see [[analytics-top-products-traffic-export]] |
| ViewMore export | ViewMore export query | Same as ViewMore but unpaginated |

ViewMore intervals are pre-generated date buckets, capped at `DETAILS_FORCE_LIMIT = 1000` buckets (force-limit toggle on the paginator). The dashboard top-N is fixed at 5 (`TABLE_RECORDS_LIMIT`), hardcoded; Details/ViewMore paginate at 100/page (`DETAILS_PAGINATION_LIMIT`). The merchant cannot configure these limits from the UI.

## Settings & fields

### Vue box configuration

| Key | Value | Meaning |
|-----|-------|---------|
| `key` | `top-products-by-traffic` | Box identifier (matches backend trait route). |
| `type` | `table` | Renders as ranked table. |
| `collectDataFrom` | `2023-01-01` | Earliest date where product-traffic data exists. |
| `viewMore` | `true` | Has per-row time-series drill-down. |
| `hasDetails` | `true` | Has Details paginated screen. |
| `hasViewMoreChart` | `true` | Charts the views over time. |
| `navigationSort` | `11` | Position on the dashboard. |
| `details.group` | `false` | One row per product (not grouped). |
| `details.defaultSorting` | views DESC, sales DESC | Default Details sort. |

### Data source — the analytics products data

The numbers come from pre-aggregated product-traffic analytics data. Each record is one (`product_id`, `hour`, `device`) bucket with `total` (deduplicated views in that hour) and `unique` (distinct UUIDs in that bucket). These records are produced by the hourly products rollup, which processes raw visitor-tracking events on a rolling 1-hour interval.

## Business rules

### Attribution model — UUID × hour × device de-duplication

The hourly rollup behind this box:

1. Takes raw product-page view events that carry a product id, within the rollup's hour window, **excluding any visitor id (`uuid_id`) that starts with `admin-`** (so admin-panel previews never inflate traffic).
2. Groups by `(uuid_id, hour, product_id, device)` — collapses all repeated views by the same visitor on the same product within the same hour into **one** per-visitor hour count.
3. Re-groups by `(hour, product_id, device)` — sums those per-visitor hour counts into `total` and counts distinct visitor ids into `unique`.

So a single visitor refreshing the product page 50 times in an hour → **1 unique** and **1 total** for that hour. The same visitor returning the next hour → **another 1+1**.

### Mobile / desktop split

Every document has a `device` field (`mobile` or `desktop` — `desktop` is the fallback when the browser device is unknown). The dashboard rolls these up into a `device` sub-object `{ mobile, desktop, total }` used by the per-row tooltip.

### Excluded admin traffic

Visitors whose id (`uuid_id`) starts with `admin-` (any casing) are filtered out of the hourly rollup. This is how the admin panel's own product preview doesn't pollute merchant traffic metrics.

### Bundles included by default

The product-traffic data contains BOTH regular products and bundle products — they live side-by-side, distinguished only by the `product_type` field (`product` or `bundle`). This box does **not** filter on `product_type`, so **bundles appear in this box alongside regular products**. If a bundle's product-page traffic is competitive with regular products, it can take a top-5 slot. The [[analytics-top-bundles-by-traffic]] box is the bundle-only filtered view of the same data.

### Filter narrowing & carve-outs

When the merchant filters Details by specific product ids, the `ids` list is passed through to a `product_id in [ids]` filter. Otherwise the Dashboard match is `product_id > 0` and the Details match is `product_id != null` — slightly different defaults: Dashboard ignores zero-id rows, Details accepts them.

### Auto group granularity (ViewMore)

When `group=auto` (default), the period diff in days drives the bucketing rule:
- `> 730 days` → yearly
- `> 90 days` → monthly
- `> 60 days` → weekly
- `< 3 days` → hourly (uses the hourly-rollup data — see [[analytics-top-order-products-by-sales]])
- otherwise → daily

The merchant overrides via the `group` dropdown, which changes which dataset ViewMore reads from (hourly = a different dataset).

### How the rollups work (verified against backend)

**Dashboard** is a 6-step rollup: filter (site_id + date window + product id filter) → group by `product_id` (sums `total` into `aggregate`, picks last `product_name` / `product_url` / `device`, splits mobile vs desktop) → sort aggregate DESC → keep top 5 → build the `device` object and set `viewMore = product_id` if id > 0 → drop internal fields. Tuned for large catalogues and can spill to disk if needed.

**Details** is the Dashboard rollup without the top-5 cap (paginated externally via skip + limit); the details-count query runs a two-stage grouping (group by `product_id`, then count) so the paginator gets the **distinct product count** for the period.

**ViewMore** reads the same data but groups by **date bucket** (hourly / daily / weekly / monthly / yearly per the period picker); the date-bucket formatting joins the grouped buckets back to the full interval list so date holes (periods with zero views) still appear as zero-rows in the chart.

Every query adds `site_id` and a UTC date range (`from` start-of-day, `to` end-of-day). The date filter is always tenant-scoped — no cross-site reads.

### Empty state behaviour

No views in period → empty dashboard result → "No data" placeholder. Details paginator's total = 0. ViewMore intervals still render with zero-rows because the date-bucket join always includes the full pre-generated interval list.

This box has no per-merchant or per-store overrides — same hour-uuid-device dedup, same admin-uuid exclusion, same rollup behaviour platform-wide.

## Related

- [[analytics-top-products-by-traffic]] — hub.
- [[analytics-top-products-traffic-ui]] — the dashboard / Details / ViewMore rendering of this data.
- [[analytics-top-products-traffic-export]] — unpaginated CSV export of the same queries.
- [[analytics-pipeline]] — the products-per-day rollup that builds this data.
- [[analytics-top-bundles-by-traffic]] — same data filtered to `product_type = bundle`.
- [[analytics-top-order-products-by-sales]] — sibling box; documents the hourly-rollup data.
- [[product]] — product entity.

## Open questions

_None._
