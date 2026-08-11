---
type: feature
nav_path: "Orders → Ordered Products → Programmatic access"
route_name: suppliers.products_by_orders
route_path: /admin/products_by_orders
aliases: ["Ordered Products API access", "Products-by-orders programmatic", "Ordered Products JSON-API", "Поръчани продукти — програмен достъп"]
tags: [orders, products, api, json-api-v2]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---
> Part of [[orders-ordered-products]]. See the hub for related aspects (overview, filters, aggregation, status scope, suppliers).

# Ordered Products — programmatic access

## Purpose

How an integration reproduces the [[orders-ordered-products]] pivot outside the admin panel. The short answer: the platform exposes the raw order-line dataset over JSON-API v2, but the merchant-facing aggregation (product-grouped SUM + order-ID concat) is admin-only and must be recomputed client-side. This aspect answers "can I get this report via the API?".

## Where to find it

The underlying dataset is the read-only [[api-order-products]] resource on JSON-API v2 — see [[json-api-v2]] for auth, pagination, and the read-vs-mutate principle. There is no API endpoint that returns this page's pivot directly.

## What the merchant can do here

### Pull the raw order lines

The [[api-order-products]] resource returns **one record per order line**, with `product_id`, `variant`, `quantity`, `price`, plus the parent `order_id` for joining. An integration uses this to build:

- Cross-order product analytics.
- Supplier-restock pipelines.
- Sales-by-SKU reports outside the admin UI.

### Recompute the pivot client-side

To replicate the admin view, the integration:

1. Fetches the line records, filtered by date / status / supplier / property as needed (filters available on the API resource — see [[api-order-products]]).
2. Groups by product / variant and runs `SUM(quantity)` + an order-ID list client-side — mirroring the database aggregation documented in [[ordered-products-aggregation]].

## Settings & fields

### What the API exposes vs. what it doesn't

| Available via API | Admin-panel-only |
|-------------------|------------------|
| Raw order-line records (`product_id`, `variant`, `quantity`, `price`, `order_id`) | The product-grouped pivot (`SUM(quantity)` + `GROUP_CONCAT(order_ids)`) |
| Read access (GET) to order products | The Suppliers-app supplier filter + cheapest-supplier highlight ([[ordered-products-suppliers]]) |

The resource is **read-only** — POST / PATCH / DELETE are not part of its contract (consistent with the read-vs-mutate principle on [[json-api-v2]]).

## Business rules

### The pivot is admin-only by design

JSON-API v2 surfaces raw order-line records, not the merchant's aggregation. The page's specific pivot — product-grouped with `SUM(quantity)` and `GROUP_CONCAT(order_ids)` — is admin-panel-only. Integrations recompute it.

### Supplier cross-reference is admin-only too

The Suppliers-app supplier filter and the cheapest-in-stock-supplier highlight ([[ordered-products-suppliers]]) are NOT exposed via the API — the resource returns line-level data, not the supplier cross-reference logic.

### Records are checkout-time snapshots

The order-line records are snapshots at checkout time — the linked product / variant may have been edited or deleted since. Integrations should not assume the IDs still resolve to a current catalog record.

### Side effects

None — read-only resource. No state changes from querying.

## Related

- [[orders-ordered-products]] — hub.
- [[api-order-products]] — the read-only JSON-API v2 resource (raw line records).
- [[json-api-v2]] — API overview; auth, pagination, read-vs-mutate principle.
- [[ordered-products-aggregation]] — the aggregation an integration must recompute.
- [[ordered-products-suppliers]] — the supplier logic that is admin-only.
- [[order]] — entity page.
- [[product]] — entity page.

## Open questions

(None.)
