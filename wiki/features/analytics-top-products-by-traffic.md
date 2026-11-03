---
type: feature
nav_path: "Analytics → Products by traffic"
route_name: analytics
route_path: /admin/analytics
aliases: ["Products by traffic", "Top products by traffic", "Top viewed products", "Most visited products", "Продукти спрямо посещения", "Топ продукти по трафик"]
tags: [analytics, ccanalytics, products, traffic, top-products-by-traffic]
plan_gates: []
created: 2026-05-22
updated: 2026-06-10
source_count: 8
---
# Products by traffic

## Purpose

Shows you which products bring the most visitors to your store — ranked by raw product-page views (not orders, not revenue). This is the "shop window" metric: a product can sit at the top of this box without selling a single unit, which is usually a signal that something downstream is broken (price too high, out of stock variants, weak product description, no clear call-to-action).

Tooltip (EN / BG): *"Top products depend on visits in your online store."* / *"Топ продукти спрямо посещения във Вашия онлайн магазин."*

Pair this box with [[analytics-top-order-products-by-sales]] (revenue ranking) and [[analytics-top-order-products-by-units-sold]] (units ranking) to spot the gap between *interest* and *conversion*. A product that ranks #1 here but doesn't appear in the top sales list is the obvious candidate to investigate.

## Where to find it

Analytics dashboard → **Products by traffic** box. `navigationSort: 11`, so it sits in the products cluster of the dashboard. Box `key: "top-products-by-traffic"`, box `type: "table"` — rendered as a top-5 ranked table. Clicking the box opens **Details**; clicking a product row drills into a per-date ViewMore time-series chart. `collectDataFrom: '2023-01-01'` — earlier date ranges return no data for any store.

## What the merchant can do here

- See the top 5 most-viewed products on the Analytics dashboard at a glance, with mobile/desktop split.
- Open **Details** — a paginated table of every product viewed in the period.
- Drill into **ViewMore** — a per-date traffic chart for a single product.
- Change the date range and compare against a previous period.
- Filter Details by specific product ids.
- Export Details / ViewMore data as CSV.

The full UI surface (dashboard box, Details columns, ViewMore chart, toolbar) is in [[analytics-top-products-traffic-ui]]. What a "view" means + where the numbers come from is in [[analytics-top-products-traffic-data-source]]. The CSV export modal + 2FA + queue + client cache is in [[analytics-top-products-traffic-export]].

## Sub-pages (in this cluster)

- [[analytics-top-products-traffic-ui]] — the three drill-down levels (dashboard top-5, Details table, per-product ViewMore chart), every column, and the page-wide date / compare / group / export toolbar.
- [[analytics-top-products-traffic-data-source]] — what counts as a "view", the UUID × hour × device de-duplication, the admin-traffic exclusion, the bundles-included default, the drill-down levels, the auto group-granularity rule, and the pipeline shapes.
- [[analytics-top-products-traffic-export]] — the Export → modal → 2FA → queue flow, the 150 000-row export cap, and the 60-second client-side cache.

## Settings & fields

This box has no merchant-editable settings of its own. Its behaviour is fixed in Vue config:

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

The Details column formatters are **reused** from [[analytics-top-order-products-by-units-sold]] — only the ranking metric (raw views) differs. The page-wide date / compare / group / export controls and their plan gates are tabulated in [[analytics-top-products-traffic-ui]].

## Business rules

- **A "view" is one product-page `viewProduct` event, deduplicated per UUID × hour × device** — 50 refreshes in an hour by the same visitor count as one view. Full attribution model: [[analytics-top-products-traffic-data-source]].
- **Admin-panel previews are excluded** — visitors with `uuid_id` matching `/^admin-.*/i` are filtered out, so the merchant's own previews don't inflate traffic. See [[analytics-top-products-traffic-data-source]].
- **Bundles appear alongside regular products** — the match does not filter `product_type`, so a high-traffic bundle can take a top-5 slot. The bundle-only view is [[analytics-top-bundles-by-traffic]]. See [[analytics-top-products-traffic-data-source]].
- **Top-N is fixed at 5; Details/ViewMore paginate at 100/page with a 1000-row force-limit.** The merchant cannot configure these. See [[analytics-top-products-traffic-data-source]].
- **All queries are tenant-scoped** (`site_id` + UTC date range) — no cross-site reads. See [[analytics-top-products-traffic-data-source]].

## Related

- [[analytics]] — parent hub.
- [[analytics-top-products-traffic-ui]] — UI surface aspect.
- [[analytics-top-products-traffic-data-source]] — data-source / attribution aspect.
- [[analytics-top-products-traffic-export]] — export + cache aspect.
- [[analytics-top-order-products-by-sales]] — sister box, ranks products by revenue (not views).
- [[analytics-top-order-products-by-units-sold]] — sister box, ranks products by units sold; provides the column formatters this box reuses.
- [[analytics-top-bundles-by-traffic]] — same logic, restricted to `product_type = bundle`.
- [[analytics-top-categories-by-traffic]] — sister box at the category level.
- [[analytics-top-landing-pages]] — page-level views (homepage + content pages).
- [[product]] — entity page.

## Open questions

_None._
