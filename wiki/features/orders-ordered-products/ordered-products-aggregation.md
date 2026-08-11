---
type: feature
nav_path: "Orders → Ordered Products → Aggregation"
route_name: suppliers.products_by_orders
route_path: /admin/products_by_orders
aliases: ["Ordered Products aggregation", "Per-variant pivot", "GROUP BY product variant", "Ordered Products quantity SUM", "Поръчани продукти — агрегация"]
tags: [orders, products, aggregation, variants]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 4
---
> Part of [[orders-ordered-products]]. See the hub for related aspects (overview, filters, status scope, suppliers, API).

# Ordered Products — aggregation semantics

## Purpose

How the [[orders-ordered-products]] pivot actually rolls up order lines into rows: the grouping key, why variants split into separate rows, the comma-separated order-ID string, per-order currency rendering, and which lines are in / out of the SUM (archived, soft-deleted, membership renewals). This aspect answers "why does my row total look like that?". The *status / date* scoping that decides which orders qualify is in [[ordered-products-status-scope]].

## Where to find it

Sidebar → **Orders** → **Ordered Products**. Each row is one aggregated product / variant; the math described here runs entirely in the database at query time.

## What the merchant can do here

The merchant cannot change the aggregation — it is fixed at the product / variant level. What the merchant should understand:

- Each row = ONE product / variant + the SUM of quantities across all orders matching the current filter.
- Example: Product X (Red, M) appearing in 5 orders with quantities 2, 1, 3, 1, 2 shows `ordered_quantity = 9` and `order_ids = 101, 103, 108, 112, 115`.
- Variants count **separately**: Product X (Red, M) and Product X (Red, L) are two distinct rows.

A merchant who wants product-level totals (without the per-variant split) must export ([[orders-ordered-products-export]]) and aggregate externally.

## Settings & fields

### Grouping key — `product_id + sku + v1 + v2 + v3`

The pivot groups by these five fields together:

- Two products with the same SKU but different IDs are separate rows.
- The same variant recorded with a different SKU at order time (manual SKU edit on the order) shows as a separate row.
- Variants with the same `product_id` but different `v1` / `v2` / `v3` are separate rows.

If the merchant later renames a variant's parameters (e.g. `v1` from "Red" to "Crimson"), past order lines with the old value keep aggregating separately from new lines with the new value.

### `ordered_quantity` — unit-based SUM

`ordered_quantity` is `SUM(quantity)` and is unit-based, not currency-based — no currency conversion happens on it.

### `order_ids` — comma-separated string

The query produces `order_ids` as a comma-separated string of order IDs per product (via `GROUP_CONCAT`). The page splits it client-side and renders each ID as a hyperlink to the order detail. For products in many orders the cell can be long, but every ID stays scannable / clickable.

## Business rules

### Aggregation runs in the database at query time

The roll-up is computed with `GROUP BY` on product + variant (plus supplier when the Suppliers app is on), `SUM(quantity)` for the totals, and `GROUP_CONCAT` for the order-ID list. The page is therefore fast even on large order histories — the merchant pays no in-memory aggregation cost.

### Per-order currency rendering

The `line_price` column formats each row's price using THAT specific order's currency and language — not the store default. Multi-currency stores may see different currency symbols in the same column. `ordered_quantity` is unit-based, so it is unaffected.

### Archived orders ARE included; soft-deleted lines are NOT

The pivot query does NOT apply an archived filter — order lines from archived orders DO appear in the aggregation. Soft-deleted order lines are excluded by the standard soft-delete scope. A merchant who wants to exclude archived orders' contribution must filter at the [[orders]] level downstream — it cannot be done from this pivot.

### Membership subscriptions contribute ONCE

CloudCart storefront subscriptions are the Membership app ([[orders-subscriptions]]). Each membership tracks days remaining on the SAME originating order — renewals do NOT generate a new order per cycle. So a subscription contributes its line items to this pivot once (the initial purchase), not per cycle.

### Side effects

None — aggregation is part of a pure read view. No state changes from browsing.

## Related

- [[orders-ordered-products]] — hub.
- [[ordered-products-status-scope]] — which orders qualify for the SUM (status / date / fulfillment scoping).
- [[orders-subscriptions]] — Membership app; why renewals don't double-count.
- [[orders-ordered-products-export]] — export to aggregate product-level totals externally.
- [[variant]] — the variant identity (`v1` / `v2` / `v3`) the pivot groups on.
- [[order]] — entity page.
- [[product]] — entity page.

## Open questions

(None.)
