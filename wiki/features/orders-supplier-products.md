---
type: feature
nav_path: "Suppliers → Products by orders"
route_name: suppliers.products_by_orders
route_path: /admin/suppliers/products-by-orders
aliases: ["Products by orders", "Supplier products", "Order products list", "Cross-order products", "Продукти от поръчки", "Продукти по доставчик"]
tags: [orders, products, suppliers, smarty]
plan_gates: []
created: 2026-05-21
updated: 2026-06-10
source_count: 8
---
# Products by orders (supplier view)

## Purpose

A **cross-order aggregated view of ordered products** — shows EVERY product across ALL orders matching the filter, grouped / sortable by supplier. Used by merchants running multi-supplier catalogs (the **Suppliers** app installed) to:

- See "how many units of Product X did I sell across all orders this month?" — for restocking.
- Generate purchase orders to suppliers based on aggregated demand.
- Identify which suppliers are driving the most order volume.
- Filter by category property (e.g., "all products in category=Shoes with property=Brand: Nike").
- Export the aggregated data for external reporting.

Without the Suppliers app installed, the page still works but with reduced functionality (no supplier column, no supplier-grouped sort).

This is a **separate top-level page** (under Suppliers, not under Orders), distinct from [[orders-products]] (which is per-order). It is a **pure read view** — no state changes, no supplier auto-notifications.

This page is a hub. Its detailed behaviour is split into five aspect pages — see **Sub-pages** below. The Assistant should drill into the aspect that matches the question rather than reading all five.

## Sub-pages (in this cluster)

- [[orders-supplier-products-overview]] — page layout, the 5-column table (4 without Suppliers app), what the merchant can / cannot do, read-only nature, no Generate-PO, no order-splitting.
- [[orders-supplier-products-filters]] — the 4-5 filters (single-active two-tier dropdown), the two-step Property-option injection, the Pending-status fulfillment constraint, and `date_added` filter semantics.
- [[orders-supplier-products-aggregation]] — how rows are summed (per product × SKU × 3 variant axes), per-variant separate rows, the `GROUP_CONCAT` order-ID truncation, multi-store scope, and the all-status default-view warning.
- [[orders-supplier-products-suppliers-app]] — the Suppliers app integration: supplier column, cheapest-supplier highlight (in-stock-only, lowest unit price), per-variant supplier lookup, the supplier-filter display-only quirk, default-sort flip.
- [[orders-supplier-products-export]] — the async chunked Export (50 × 1000 = 50,000 cap), the 50-product inline-vs-async threshold, the fixed field set, and how the export honours the active filters.

## Where to find it

Sidebar → Suppliers / Products → **Products by orders** (when the Suppliers app is installed) OR via direct route.

Routes:
- `suppliers.products_by_orders` (GET) — initial render.
- (same route, POST) — AJAX grid data load.

## What the merchant can do here

- View an aggregated, filtered, supplier-sortable table of ordered products. Full layout + column reference: [[orders-supplier-products-overview]].
- Narrow the aggregate by supplier, order date interval, order ID interval, order status, or category property option — only one filter active at a time. See [[orders-supplier-products-filters]].
- Export the filtered table to file (async, chunked). See [[orders-supplier-products-export]].
- Click an order ID to open that order in [[orders-details]]; click a product name to open its editor in [[products-products]].

The merchant **cannot** edit products, bulk-update orders, or generate a purchase order directly from this page — it is read-only aggregation feeding a downstream (manual or app-driven) purchasing workflow. Details: [[orders-supplier-products-overview]].

## Settings & fields

This page has **no configurable settings of its own** — its behaviour is driven entirely by:

- Whether the **Suppliers** app is installed (controls the supplier column, supplier filter, default sort, and cheapest-supplier highlight — see [[orders-supplier-products-suppliers-app]]).
- The per-product / per-variant supplier configuration set in the product editor (price, in-stock flag) consumed by the cheapest-supplier logic.
- The currently-applied filter (date / ID / status / supplier / property option).
- The order status taxonomy from [[settings-statuses]] feeding the status filter.

## Business rules

- **App / plan gating** — the supplier column, supplier filter, supplier-grouped default sort and cheapest-supplier highlight require the Suppliers app installed AND active. The page itself works without it but provides less value. See [[orders-supplier-products-suppliers-app]].
- **Cross-order aggregation drives purchase orders** — the typical workflow is filter by date + status → sort by supplier → export → review quantities → place a PO externally. The page produces the input, not the PO.
- **Default view aggregates ALL statuses** — including refunded / cancelled. The merchant should apply a status filter to avoid over-ordering. See [[orders-supplier-products-aggregation]].
- **No order-splitting** — a multi-supplier customer order remains one order record; this view only reports the cross-supplier demand. See [[orders-supplier-products-overview]].
- **Side effects: none** — pure read view, no supplier notifications.

## Related

- [[orders]] — parent list of orders.
- [[orders-products]] — per-order product CRUD (different scope).
- [[orders-details]] — clicking order IDs in this view opens detail there.
- [[products-products]] — clicking a product name opens its editor.
- [[products-property]] — property + options used in the property-option filter.
- [[apps]] — the Suppliers app provides the supplier column and filter.
- [[settings-statuses]] — order status taxonomy used in the status filter.
- [[order]] — entity page.
- [[product]] — entity page.

## Open questions

None.
