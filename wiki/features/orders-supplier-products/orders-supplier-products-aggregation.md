---
type: feature
nav_path: "Suppliers → Products by orders → Aggregation"
route_name: suppliers.products_by_orders
route_path: /admin/suppliers/products-by-orders
aliases: ["Products by orders aggregation", "Ordered quantity sum", "Order ID truncation", "Per-variant rows", "Cross-order quantity totals"]
tags: [orders, products, suppliers, smarty]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 4
---
> Part of [[orders-supplier-products]]. See the hub for the other aspects (overview, filters, Suppliers app, export).

# Products by orders — aggregation semantics

## Purpose

Documents HOW the **Products by orders** screen sums quantities into rows — the grouping key, why variants count as separate rows, the silent order-ID list truncation, the multi-store scope, and the all-status default-view trap. This is the most consequential aspect for accuracy: a merchant placing restock orders off these numbers needs to understand exactly what each row counts. The screen itself is described on the hub [[orders-supplier-products]].

## Where to find it

On the **Products by orders** grid (route `suppliers.products_by_orders`), the **Ordered quantity** and **Order IDs** columns reflect the aggregation. Changing any filter (see [[orders-supplier-products-filters]]) re-runs the aggregation against the new scope.

## What the merchant can do here

The merchant reads aggregated demand: each row = one product (+ variant) with the SUM of quantities across all orders in scope, plus the list of contributing order IDs. The merchant uses this to decide restock quantities per product / variant / supplier.

## Settings & fields

### Aggregation semantics

Each row represents **one product (+ variant)** with the SUM of quantities across all orders matching the filter. If Product X (Red, Size M) appears in 5 orders with quantities 2, 1, 3, 1, 2 → the row shows `ordered_quantity = 9` and `order_ids = 101,103,108,112,115`. If the merchant filters by a date range, only orders within that range contribute. Changing the filter changes the aggregation.

### Grouping key — by product × SKU × 3 variant axes

The aggregation groups order lines by `product_id, sku, v1, v2, v3` and sums `quantity`. So:

- Each unique (product, SKU, variant1, variant2, variant3) tuple is ONE row.
- An order line with no variants (sku-less) → grouped by product_id + empty variant axes.
- An order line that DUPLICATES the same SKU at different prices (e.g., promotional vs full-price) → still ONE aggregated row (the price displayed comes from one of them, not averaged).

### Per-variant counts separately

A product with variants (Size M vs L) shows as MULTIPLE rows — one per variant — not one aggregated row. So the merchant sees quantities per variant for granular restocking.

## Business rules

### Aggregation includes ALL orders by default

The page's default view (no filter applied) aggregates products across ALL order statuses including refunded / cancelled / chargebacked. The merchant should APPLY the status filter (typically paid + completed) to exclude cancelled orders from the supplier aggregate — otherwise the merchant may over-order from suppliers based on inflated demand numbers. See [[orders-supplier-products-filters]].

### Date range — unbounded by default

When the merchant opens the page with no filter, the list runs against the FULL order history (all dates). There is NO automatic current-month default. For large stores the merchant should apply a date filter (recent month / quarter) early to keep the list responsive and meaningful.

### Order ID list — silent truncation past ~100 orders

The `order_ids` column is built by concatenating every contributing order ID into one text value, and the database caps how long that concatenated value can be (typically about 1024 characters), so it can TRUNCATE the list for high-volume products. After about 100 orders for one product, the merchant may see a clipped list. This is a silent data-loss point — the **Ordered quantity** total is unaffected, but the **Order IDs** list may not show every contributing order.

### Multi-store aggregation — per-store by default

For merchants on the Stores app, each store sees its own scope. The page does NOT aggregate cross-store automatically. To get a multi-store view the merchant either switches stores in admin or exports each store separately (see [[orders-supplier-products-export]]) and combines externally.

### Side effects

**None** — aggregation is a read-time computation; no data is written.

## Related

- [[orders-supplier-products]] — hub.
- [[orders-supplier-products-filters]] — filters that scope what gets aggregated.
- [[orders-supplier-products-export]] — exporting the aggregated rows.
- [[orders-supplier-products-suppliers-app]] — per-variant supplier lookup keyed on the same variant axes.
- [[product]] — entity page.
- [[order]] — entity page.

## Open questions

None.
