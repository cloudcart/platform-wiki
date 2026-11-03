---
type: feature
nav_path: "Analytics → Products by sales"
route_name: analytics
route_path: /admin/analytics
aliases: ["Products by sales", "Top products by sales", "Best-selling products by sales", "Top order products by sales", "Продукти по продажби", "Най-продавани продукти"]
tags: [analytics, ccanalytics, orders, products, top-order-products-by-sales]
plan_gates: []
created: 2026-05-22
updated: 2026-06-10
source_count: 9
---
# Products by sales

## Purpose

Answers: **which products generate the most revenue?** Ranks the store's products by **total order value** (units × selling price summed across all orders in the period). Pairs with the sibling box [[analytics-top-order-products-by-units-sold]] (which ranks by quantity instead of revenue).

Tooltip (EN / BG): *"Best-selling products by their total value from all orders. The data is visualized according to the following statuses of orders - Paid, Completed, Pending, Authorized payment, Fulfilled."* / *"Най-продавани продукти според общата им стойност от всички поръчки. Данните се визуализират спрямо следните статуси на поръчки - Платена, Изпълнена, Изчакваща, Оторизирано плащане, Изпратена."*

**Important:** Unlike most analytics boxes, this one's tooltip names a **hardcoded** status set — Paid, Completed, Pending, Authorized payment, Fulfilled — rather than honouring Settings → Analytics → Order statuses. The full mechanics live in [[analytics-top-order-products-sales-status-filter]].

## Where to find it

Analytics dashboard. Box title: **"Products by sales"** (EN+BG, no separate BG translation). `navigationSort` is 9 — high-priority position near the top of the dashboard. The title row also doubles as `title_details` and `title_viewMore` (no template).

## What the merchant can do here

- See the top 5 revenue-generating products on the Analytics dashboard.
- Click the box to open the **Details** screen — paginated table of the top 1000 distinct products by revenue.
- Click a product row to open **ViewMore** — per-date time-series for that single product, plotting `amount` over time.
- Filter Details by specific product IDs, sort, switch period, compare against a previous period, and export to CSV.
- Click any product name to open the product's storefront page.

The full UI surface — dashboard box, Details columns, ViewMore chart, and the page-wide date / compare / group toolbar — is documented in [[analytics-top-order-products-sales-ui]]. The CSV export modal + 2FA + queue flow + client cache is in [[analytics-top-order-products-sales-export]].

## Sub-pages (in this cluster)

- [[analytics-top-order-products-sales-ui]] — the three drill-down levels (dashboard top-5, Details table, per-product ViewMore chart), every column, and the page-wide toolbar controls.
- [[analytics-top-order-products-sales-status-filter]] — the hardcoded Paid / Completed / Pending / Authorized payment / Fulfilled status set, the yellow alert banner, and why Settings → Analytics cannot change it.
- [[analytics-top-order-products-sales-data-source]] — the pre-aggregated daily collection, variant roll-up into the parent product, the orphan (`product_id = 0`) bucket, distinct-order counting, and the 1000-product force-limit.
- [[analytics-top-order-products-sales-export]] — the Export → modal → 2FA → queue flow, the 150 000-row export cap, and the 60-second client-side cache.

## Settings & fields

This box has no merchant-editable settings of its own. Its behaviour is fixed in Vue config:

| Key | Value | Meaning |
|-----|-------|---------|
| `key` | `top-order-products-by-sales` | Box identifier |
| `type` | `table` | Table layout |
| `viewMore` | `true` | Has per-row time-series |
| `hasDetails` | `true` | Has Details screen |
| `hasViewMoreChart` | `true` | Time-series chart |
| `navigationSort` | 9 | High dashboard position |
| `details.defaultSorting` | `amount` DESC, `sales` DESC | Default Details sort |
| `details.viewMore.group` | `true` | ViewMore groups by date bucket |

This box's Vue config **inherits** `formatters.alerts`, `formatters.details`, and most of `formatters.viewMore` from the `top-order-products-by-units-sold` box, but overrides the chart `tableToChart` to plot `amount` (instead of `quantity`).

The page-wide date / compare / group / export controls and their plan gates are tabulated in [[analytics-top-order-products-sales-ui]].

## Business rules

- **Hardcoded status set, not the merchant's Settings → Analytics set.** The data only counts orders in Paid / Completed / Pending (+ not-fulfilled) / Authorized / Fulfilled — fixed at ingestion, not at query time. Full mechanics + the alert banner: [[analytics-top-order-products-sales-status-filter]].
- **Amounts are full `amount`** (product line value), not `amount_without_shipping`; the final stage divides by 100 (cents → currency units). See [[analytics-top-order-products-sales-data-source]].
- **Variants roll up into the parent product** — one row per product regardless of variant count; the per-day collection is keyed by `(site_id, date, product_id)`. See [[analytics-top-order-products-sales-data-source]].
- **Deleted / orphan products** land in the `product_id = 0` bucket and are excluded from the ranking. See [[analytics-top-order-products-sales-data-source]].
- **Force-limit at 1000 distinct products** caps the Details table for large catalogues. See [[analytics-top-order-products-sales-data-source]].

## Related

- [[analytics]] — parent hub. Does NOT control this box's status set (it is hardcoded at ingestion).
- [[analytics-top-order-products-sales-ui]] — UI surface aspect.
- [[analytics-top-order-products-sales-status-filter]] — status-filter aspect.
- [[analytics-top-order-products-sales-data-source]] — data-source / aggregation aspect.
- [[analytics-top-order-products-sales-export]] — export + cache aspect.
- [[analytics-top-order-products-by-units-sold]] — sibling box, same data ranked by `quantity` instead of `amount`.
- [[analytics-top-order-bundles-by-sales]] — sibling box for bundles.
- [[analytics-landing-pages-by-sales]] — sibling traffic box.
- [[product]] — entity page for products.
- [[order]] — order entity page.

## Open questions

_None._
