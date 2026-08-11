---
type: feature
nav_path: "Analytics → Products by sales → Data source"
route_name: analytics
route_path: /admin/analytics
aliases: ["Products by sales data source", "Products by sales aggregation", "Products by sales variant rollup", "Products by sales force-limit", "Продукти по продажби — източник на данни"]
tags: [analytics, ccanalytics, orders, products, top-order-products-by-sales, aggregation]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 9
---
> Part of [[analytics-top-order-products-by-sales]]. See the hub for the other aspects (UI surface, status filter, export).

# Products by sales — data source

## Purpose

Explains **where the numbers come from**: the pre-aggregated daily data that feeds the box, how variants roll up into the parent product, what the `product_id = 0` orphan bucket means, how device order-counts are tallied, and the 1000-product force-limit on the Details table. This is the page to read when a merchant asks why a product's revenue here doesn't match the order ledger, or why a deleted product's sales vanished from the ranking.

## Where to find it

This is back-end behaviour behind the "Products by sales" box on the Analytics dashboard — it has no separate screen. The effects are visible in the dashboard top-5, the Details table, and the ViewMore chart.

## What the merchant can do here

- Filter Details to specific products via the multi-select (the `ids` parameter).
- Understand why some revenue is **not** attributed to any product row (orphan bucket).
- Understand why large catalogues show "up to 1000 results" with an Export prompt (force-limit).

## What the merchant sees

When a catalogue exceeds 1000 distinct products in the period, the Details table shows only the top 1000 by revenue and surfaces the force-limit banner (*"This report shows up to {total} results. To see all results, you can [Export]"*). Otherwise the data source is invisible — the merchant just sees rows.

## Settings & fields

No merchant-editable settings. The relevant internal constants:

| Name | Value | Meaning |
|------|-------|---------|
| `DETAILS_FORCE_LIMIT` | 1000 | Max distinct products surfaced in Details. |
| `ids` | (request param) | Multi-select product filter; intersected as `product_id in [ids]`. |

## Business rules

### Pre-aggregated daily data

The numbers come from pre-aggregated daily analytics data:

- Dashboard / Details / Count: a daily-rollup dataset — one record per `(site_id, date, product_id)` per day.
- ViewMore: an hourly-rollup dataset if the period picker is `hourly`, otherwise the daily-rollup dataset.

Each record carries `product_id`, `name`, `url`, `unit`, `quantity`, `amount`, `orders`, `product_view`, `mobile`, `desktop` — pre-summed per day. The box just rolls these up across the date window. The status set baked into this data is fixed — see [[analytics-top-order-products-sales-status-filter]].

### Amounts are full `amount` (NOT `amount_without_shipping`)

The `amount` field is summed directly from `amount` in the per-day data — the **product line value** (price × quantity × tax handling done when the daily data is built). Shipping is not part of a product line, so the distinction doesn't change the figure here, but the field name differs from the Sales-by-Source boxes. The final step divides `amount` by 100 (cents → currency units).

### Variants aggregate into the parent product

When the daily data is built, each order line records both `product_id` and `variant_id`. The dashboard / Details / ViewMore rollups group **only by `product_id`** — variants are rolled up into their parent. A merchant viewing "Products by sales" sees **one row per product** regardless of how many variants it has; there is no per-variant ranking surfaced. The per-day data is keyed on `(site_id, date, product_id)`, so variants are pre-summed during the daily rollup. (The per-variant stock model is a separate concept — see [[inventory-variant-model]].)

### Orphan / deleted products bucket — `product_id = 0`

The daily data stores `product_id = 0` when the order line's product no longer exists or was a one-off line with no catalogue product. The dashboard excludes these rows (`product_id > 0`). Details inherit the same filter unless the merchant explicitly opts in via the `ids` parameter. **Effect:** orders with deleted catalogue products silently drop from this ranking — the revenue still exists in the order ledger but is not attributable to any current product row.

### Distinct order counting — `mobile`, `desktop`, `sales`

The per-day data's `mobile` and `desktop` fields are built by collecting the distinct order ids per device and counting them — they are **distinct order counts** per device, not row counts (same for `orders`). Implication: a single mobile order containing 5 products counts as `mobile = 1` for each of those 5 product rows in the per-day data. At the dashboard level, summing `mobile` across days for one product gives the count of distinct mobile order-**days**, not orders — so for products selling across multiple days, `mobile + desktop` can exceed the actual unique-order count (a minor reporting quirk).

### Force-limit at 1000 distinct products

`DETAILS_FORCE_LIMIT = 1000`. If the period contains more than 1000 distinct products, the Details view truncates to the top 1000 (by amount) and the force-paginator exposes only that subset, with `total` clamped at 1000. This prevents arbitrarily long tables for stores with massive catalogues. The Export path bypasses pagination (the limit is applied only when numeric) — see [[analytics-top-order-products-sales-export]].

### How the rollups work (verified against backend)

| Level | Returns |
|-------|---------|
| Dashboard | Filter (date + site_id + `product_id > 0`) → group by `product_id` → sort `amount` DESC, `sales` DESC → keep top 5 → set `meta.row1 = quantity`, ÷100, build device object, set `viewMore = id` if id > 0. |
| Details | Same as Dashboard but with an optional 1000-row force-limit (between the sort and the final step) when `total > 1000`; skip/limit pagination is appended only when the limit is numeric. |
| ViewMore | Switches between the hourly-rollup and daily-rollup data per grouping mode; groups by date bucket; joins the pre-generated interval list so empty days appear as zero-rows. |
| Count | Two-stage grouping — first by `(product_id, name)`, then a count. The composite key matters because the same product id can carry a different name across records (renamed mid-period). |

The rollups are tuned for large catalogues and can spill to disk if needed.

## Related

- [[analytics-top-order-products-by-sales]] — hub.
- [[analytics-top-order-products-sales-status-filter]] — the fixed status set baked into the collection.
- [[analytics-top-order-products-sales-export]] — how the Export path bypasses the force-limit.
- [[analytics-top-order-products-by-units-sold]] — sibling box reading the same collection, ranked by quantity.
- [[inventory-variant-model]] — the per-variant stock model (contrast: this box rolls variants up to the product).
- [[product]] — product entity.
- [[order]] — order entity; the source of the per-day aggregation.

## Open questions

_None._
