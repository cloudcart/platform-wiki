---
type: feature
nav_path: "Orders → Ordered Products"
route_name: suppliers.products_by_orders
route_path: /admin/products_by_orders
aliases: ["Ordered Products", "Products by orders", "Order products view", "Aggregated product list", "Cross-order product pivot", "Поръчани продукти", "Продукти по поръчки"]
tags: [orders, products, aggregation, smarty]
plan_gates: []
created: 2026-05-23
updated: 2026-06-10
source_count: 6
---
# Ordered Products

## Purpose

The **Ordered Products** view — a cross-order aggregated pivot of EVERY product (or product variant) that has been ordered across the store. Each row shows one product / variant with the SUM of units sold and the list of order IDs that contain it. Merchants use it for:

- Restocking decisions ("how many of Product X did I sell this month?").
- Sales analytics by product (which SKUs move, which don't).
- Cross-referencing customer demand against current stock.
- Feeding external purchase-order workflows or supplier negotiations.

This is a **pivot from the order-line side** — instead of one row per order (as in [[orders]]), it lists ORDERED PRODUCTS (one row per product, with the orders that contain it). The view is **read-only** — the merchant cannot edit products or orders from here.

This page is the **hub** for a cluster of aspect pages. It is intentionally slim — drill into the aspect that matches the question.

## Sub-pages (in this cluster)

- [[ordered-products-overview]] — the pivot grid: columns, default sort, navigation actions, what the merchant can / cannot do, modal inventory.
- [[ordered-products-filters]] — the five filters (date / ID interval, status, property-option, supplier), operators, the two-step property-option picker, and the hidden text-search filter.
- [[ordered-products-aggregation]] — GROUP BY semantics, per-variant pivoting, the comma-separated order-ID string, currency rendering, archived-order inclusion, membership-once contribution.
- [[ordered-products-status-scope]] — what gets counted: all-statuses-by-default caveat, the implicit `pending → not_fulfilled` constraint, and `date_added` as the date basis.
- [[ordered-products-suppliers]] — the Suppliers-app conditional column / filter / sort, and the cheapest-in-stock-supplier highlight logic.
- [[ordered-products-api]] — programmatic access: the read-only [[api-order-products]] resource exposes raw line records; the pivot itself is admin-only.

The CSV **Export** button on this page is documented separately in [[orders-ordered-products-export]]. The Suppliers-app-focused variant of the same surface is [[orders-supplier-products]].

## Where to find it

Sidebar → **Orders** → **Ordered Products**.

Listed in the Orders section of the sidebar, separately from the main Orders list. The label is *"Ordered products"* (translated as `sidebar.products_by_orders`). The page route is `suppliers.products_by_orders` (`/admin/products_by_orders`).

## What the merchant can do here

- **Browse the pivot** — one row per product / variant with aggregated quantity + order-ID list. See [[ordered-products-overview]].
- **Filter the pivot** — by date interval, order-ID interval, status, property-option, and (with the Suppliers app) supplier. See [[ordered-products-filters]].
- **Click through** — each product name opens the product editor ([[products-products]]); each order ID opens the order detail ([[orders-details]]) in a new tab.
- **Export the filtered pivot to CSV** — via the top-right **Export** button. See [[orders-ordered-products-export]].

What the merchant CANNOT do: edit products / orders inline, run order bulk actions, save a custom filter set, or change the aggregation pivot (it is fixed at the product / variant level). See [[ordered-products-overview]] for the full read-only boundary.

## Settings & fields

This page has **no settings of its own** — it is a read-only reporting surface. The field-level detail (columns, filter operators, aggregation grouping) is documented per aspect:

- Columns + sort → [[ordered-products-overview]].
- Filter operators + the two-step property-option picker → [[ordered-products-filters]].
- Aggregation grouping (`product_id + sku + v1 + v2 + v3`) → [[ordered-products-aggregation]].
- Suppliers-app conditional fields → [[ordered-products-suppliers]].

## Business rules

The cross-cutting rule: **the pivot aggregates orders of ALL statuses by default** — including refunded / cancelled / failed orders — which can inflate apparent demand. The merchant should always apply a status filter (typically `paid` + `completed`) before drawing conclusions. The full set of scoping caveats (status default, the implicit `pending → not_fulfilled` constraint, `date_added` as the date basis, archived-order inclusion) lives in [[ordered-products-status-scope]] and [[ordered-products-aggregation]].

The page is permission-gated to admins with orders access — the `suppliers.products_by_orders` route is part of the orders permission scope.

## Related

- [[orders]] — parent orders list (the source data — this page pivots THE order lines).
- [[orders-details]] — clicking order IDs opens there.
- [[orders-products]] — per-order product CRUD (different scope — a single order's line items).
- [[orders-ordered-products-export]] — CSV export of the pivot.
- [[orders-supplier-products]] — Suppliers-app focused version of the same page.
- [[products-products]] — clicking a product name opens the product editor.
- [[products-property]] — properties + options used in the Property-option filter.
- [[settings-statuses]] — order status taxonomy used in the status filter.
- [[apps]] — Suppliers app provides supplier columns + filter.
- [[api-order-products]] — read-only JSON-API v2 resource (raw line records).
- [[json-api-v2]] — API overview.
- [[order]] — entity page.
- [[product]] — entity page.

## Open questions

(All resolved — distributed to the aspect pages.)
