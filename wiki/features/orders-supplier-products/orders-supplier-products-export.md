---
type: feature
nav_path: "Suppliers → Products by orders → Export"
route_name: suppliers.products_by_orders
route_path: /admin/suppliers/products-by-orders
aliases: ["Products by orders export", "Export ordered products", "Supplier products export", "ACTION_EXPORT_ORDERS_PRODUCTS", "Chunked product export"]
tags: [orders, products, suppliers, smarty, export]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---
> Part of [[orders-supplier-products]]. See the hub for the other aspects (overview, filters, aggregation, Suppliers app).

# Products by orders — export

## Purpose

Documents the **Export** action on the **Products by orders** screen — the inline-vs-async threshold, the chunking limits, the fixed field set, and the fact that the export honours the currently-applied filters. Export is how the merchant gets the aggregated demand OUT of the platform and into a purchasing workflow, since the page itself has no Generate-PO action (see [[orders-supplier-products-overview]]). The screen is described on the hub [[orders-supplier-products]].

## Where to find it

The **Export** button sits on the top-right breadcrumb row of the **Products by orders** page (route `suppliers.products_by_orders`). It is rendered by the shared admin import/export partial with the action key `ACTION_EXPORT_ORDERS_PRODUCTS` and uses the standard async-task UI helper.

## What the merchant can do here

Click **Export** to produce a downloadable file of the filtered product list. The export honors the currently-applied filters (date, status, supplier, property option — see [[orders-supplier-products-filters]]), so the merchant filters first, then exports exactly what's on screen. The merchant does not wait at the screen — for large exports the result arrives via the standard task-queue notification.

## Settings & fields

### Fixed field set

The export uses a FIXED column set per the Suppliers app — typically product name, variant, supplier name, supplier price, and total quantity in scope. Merchants CANNOT pick custom fields from this UI.

### Limits

- **Chunk size**: 1000 products per chunk.
- **Max chunks**: 50.
- **Hard cap**: 50 × 1000 = **50,000 products** per export job.

## Business rules

### Inline vs async threshold — 50 products

- If the filtered list has **≤ 50 products**, the export runs INLINE in the request (synchronous download).
- If **> 50 products**, the export is CHUNKED into 1000-product chunks and queued as async tasks (up to 50 chunks). The merchant sees an "Export queued" message and the download appears later via the standard task-queue notification.

### Very large datasets

For exports exceeding the 50,000-product cap, the merchant must apply more aggressive filters (narrower date range, specific supplier, specific status) to reduce the dataset below the cap. See [[orders-supplier-products-filters]] and the aggregation rules in [[orders-supplier-products-aggregation]].

### Multi-store

The export is per-store, matching the page's per-store scope. To combine stores, the merchant exports each store separately and merges externally — see [[orders-supplier-products-aggregation]].

### Side effects

The export only READS data and produces a file — it does NOT change any order, product, or supplier state, and it does NOT notify suppliers.

## Related

- [[orders-supplier-products]] — hub.
- [[orders-supplier-products-overview]] — the read-only page Export feeds (no Generate-PO action).
- [[orders-supplier-products-filters]] — filters the export honours.
- [[orders-supplier-products-aggregation]] — what each exported row counts.
- [[orders-supplier-products-suppliers-app]] — supplier columns in the export.

## Open questions

- Whether the export file format is CSV or XLSX (or merchant-selectable) `(verify)`.
