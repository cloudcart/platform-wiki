---
type: feature
nav_path: "Orders → Ordered Products → Overview"
route_name: suppliers.products_by_orders
route_path: /admin/products_by_orders
aliases: ["Ordered Products grid", "Ordered Products columns", "Products-by-orders pivot grid", "Ordered Products read-only view", "Поръчани продукти — изглед"]
tags: [orders, products, aggregation, smarty]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 4
---
> Part of [[orders-ordered-products]]. See the hub for related aspects (filters, aggregation, status scope, suppliers, API).

# Ordered Products — overview

## Purpose

The grid surface of the [[orders-ordered-products]] pivot: the columns it shows, how it sorts by default, the click-through navigation, and the strict read-only boundary. This aspect answers "what does this page show and what can I touch?". The aggregation math behind the rows is in [[ordered-products-aggregation]]; the filter rail is in [[ordered-products-filters]].

## Where to find it

Sidebar → **Orders** → **Ordered Products**. The page header breadcrumb reads *"Products"*. A primary-blue **Export** button sits top-right (documented in [[orders-ordered-products-export]]).

## What the merchant can do here

### List columns (4 — or 5 with the Suppliers app)

| Column | Field | Sortable | Notes |
|--------|-------|----------|-------|
| **Product** | `name_list` | No | Product name + variant info + image. Rich rendering with a link to the product editor. |
| **Order IDs** | `order_ids` | No | Comma-separated list of order IDs containing this product. Each ID is clickable — opens the order detail in a new tab. |
| **Product price** | `line_price` | No | Per-unit price at order time, currency-formatted per the order's own currency / language. |
| **Product quantity** | `ordered_quantity` | No | SUM of quantities across all matching orders for this product / variant. |
| **Suppliers** | (conditional) | Yes (Suppliers app only) | Supplier name(s) + cheapest-supplier highlight — see [[ordered-products-suppliers]]. |

### Default sort

- **Without** the Suppliers app: `orders_products.id DESC` (newest order lines first).
- **With** the Suppliers app: `supplier_name DESC` (groups products by supplier) — see [[ordered-products-suppliers]].

### Click-through navigation

- **Product name** → opens the product editor at `/admin/products/edit/<id>` (check stock, edit description, adjust price against the aggregated demand). See [[products-products]].
- **Order ID** → opens the order's detail page at `/admin/orders/details/{id}` in a new tab. See [[orders-details]].

### What the merchant CANNOT do here

- **Edit products** — read-only aggregation. Click a product name to reach the editor.
- **Run order bulk actions** (mark fulfilled, etc.) — this is a products view, not an orders view. Use [[orders]] for order-level bulk actions.
- **See per-order detail inline** — only the aggregated quantity + order-ID list. Drill in by clicking an order ID.
- **Generate a purchase order** to a supplier directly — but the data feeds that workflow (manual or via the Suppliers app).
- **Save a custom filter set** — every filter is ad-hoc per session.
- **Switch the aggregation pivot** (by category / vendor / tag) — the pivot is fixed at the product / variant level.

## Settings & fields

This surface has **no settings of its own** — it is a read-only grid. The only interactive controls are the filter rail ([[ordered-products-filters]]) and the **Export** button ([[orders-ordered-products-export]]).

### Modal field inventory (verified template: `products/products_by_order.tpl`)

The page has **no modals or sub-flows** of its own — verified against the template:

- **Breadcrumb** header titled "Products".
- **Export** button (top-right) — opens the standard async chunked-export panel (synchronous up to 50 product rows, asynchronous in 1000-row chunks above that). See [[orders-ordered-products-export]].
- **Filter rail** included from `orders/filters/supplier_products`. The property-option two-step picker lives in the filter rail itself, not in a modal — see [[ordered-products-filters]].
- **Grid** with the columns above. Each product name + each order ID is hyperlinked but navigates AWAY (no inline panel).

No add / edit / delete modals exist — the merchant cannot mutate the pivot from this page.

## Business rules

### Pure read view — no side effects

Filtering, sorting, and browsing change no state. The only navigation away is clicking a product name (→ product editor) or an order ID (→ order detail). There is no bulk-action dropdown at the bottom of the grid (unlike most listing pages) — intentional, since a "selection of pivot rows" has no meaningful action.

### Empty / null state

A filter combination that returns nothing renders zero rows with the standard "no results" indicator. There is no custom empty-state illustration (unlike [[orders]], which has a "no orders yet" box) — the empty state is simply a blank grid.

### Permission

Permission-gated to admins with orders access; the `suppliers.products_by_orders` route is part of the orders permission scope.

### Modern Vue migration — not yet shipped

The page currently renders via Smarty + jQuery + the legacy grid system. A Vue replacement has not shipped. When the modern admin replaces this surface, the underlying behaviour should be preserved. `(verify)` whether a Vue variant is in flight.

## Related

- [[orders-ordered-products]] — hub.
- [[orders]] — parent orders list (the source data).
- [[orders-details]] — clicking an order ID opens here.
- [[products-products]] — clicking a product name opens the product editor.
- [[orders-ordered-products-export]] — the top-right Export button.
- [[order]] — entity page.
- [[product]] — entity page.

## Open questions

`(verify)` whether a modern Vue replacement of this grid is in flight.
