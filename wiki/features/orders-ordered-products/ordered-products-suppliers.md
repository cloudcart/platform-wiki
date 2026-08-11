---
type: feature
nav_path: "Orders → Ordered Products → Suppliers app behaviour"
route_name: suppliers.products_by_orders
route_path: /admin/products_by_orders
aliases: ["Ordered Products suppliers column", "Cheapest supplier highlight", "Ordered Products supplier filter", "Suppliers app pivot behaviour", "Поръчани продукти — доставчици"]
tags: [orders, products, suppliers, apps]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 4
---
> Part of [[orders-ordered-products]]. See the hub for related aspects (overview, filters, aggregation, status scope, API).

# Ordered Products — Suppliers app behaviour

## Purpose

How the **Suppliers** app changes the [[orders-ordered-products]] pivot: it adds a supplier column, a supplier filter, flips the default sort, and highlights the cheapest in-stock supplier per variant. This aspect answers "why is there a Suppliers column / filter, and why does my supplier filter exclude variants I expected?". For the supplier-focused variant of the whole surface, see [[orders-supplier-products]].

## Where to find it

Sidebar → **Orders** → **Ordered Products**. The supplier column / filter appear ONLY when the **Suppliers** app ([[apps]]) is installed; without it the page is a pure product pivot.

## What the merchant can do here

### With the Suppliers app installed

- **Supplier filter** appears in the rail (single-select from configured suppliers).
- **Suppliers column** appears with rich rendering (name + cheapest-supplier marker).
- **Default sort** flips to `supplier_name DESC` (groups products by supplier).
- The **export** includes supplier columns ([[orders-ordered-products-export]]).

### Without the app

- Supplier filter hidden.
- Suppliers column hidden.
- Default sort uses the standard `orders_products.id DESC`.

## Settings & fields

### Cheapest-supplier highlight — base-price comparison

When a product has multiple configured suppliers AND the app is on, the platform highlights the supplier with the LOWEST current configured `price`. This is a **base-price comparison only** — it does NOT factor in MOQ, shipping, or lead time. Treat the highlight as a starting point, not a procurement decision.

### Highlight requires `variant_id` match + `in_stock = 1`

The cheapest-supplier column joins via the order line's `variant_id` to the per-supplier product records, and only counts records flagged `in_stock = 1`:

- Order lines without a `variant_id` (rare legacy cases) get no supplier highlight.
- Out-of-stock supplier records are skipped — if ALL configured suppliers for a product are flagged out-of-stock, no highlight appears.

## Business rules

### Supplier filter narrows to "cheapest in-stock supplier matches"

The **Supplier** filter narrows products to those where the chosen supplier is the CHEAPEST in-stock supplier for that variant — NOT simply "all variants the supplier carries":

- A variant with suppliers A, B, C where C is cheapest and in-stock appears ONLY when filtering by supplier C.
- Filtering by A or B EXCLUDES that variant — even though A and B are configured suppliers for it.

This is non-intuitive. For full supplier-coverage analysis the merchant uses [[orders-supplier-products]] or the Suppliers app's own list, not this filter.

### Supplier filter requires in-stock supplier records

The filter restricts to supplier records flagged `in_stock = 1`. So the merchant might miss aggregations for products whose preferred supplier is currently out-of-stock even when alternative suppliers exist.

### Side effects

None — the Suppliers columns / filters are read-only additions to a pure read view. No procurement action is taken from this page.

## Related

- [[orders-ordered-products]] — hub.
- [[orders-supplier-products]] — Suppliers-app focused version of the same surface (full supplier-coverage analysis).
- [[apps]] — the Suppliers app provides these columns + filter.
- [[orders-ordered-products-export]] — export gains 3 supplier columns when the app is on.
- [[order]] — entity page.
- [[product]] — entity page.

## Open questions

(None.)
