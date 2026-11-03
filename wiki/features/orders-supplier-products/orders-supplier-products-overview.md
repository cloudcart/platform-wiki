---
type: feature
nav_path: "Suppliers → Products by orders → Layout & columns"
route_name: suppliers.products_by_orders
route_path: /admin/suppliers/products-by-orders
aliases: ["Products by orders layout", "Supplier products columns", "Order products table", "Products by orders read view"]
tags: [orders, products, suppliers, smarty]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 4
---
> Part of [[orders-supplier-products]]. See the hub for the other aspects (filters, aggregation, Suppliers app, export).

# Products by orders — layout & columns

## Purpose

Documents what the **Products by orders** screen looks like and what the merchant can / cannot do with it. The page is a Smarty + jQuery + AJAX grid (no Vue) that renders ONE row per ordered product (+ variant), aggregated across all orders matching the active filter. It is the read-only front end of the cross-order demand-analysis workflow described on the hub [[orders-supplier-products]].

## Where to find it

Sidebar → Suppliers / Products → **Products by orders** (when the Suppliers app is installed) OR via direct route `suppliers.products_by_orders`.

- GET on the route renders the page chrome (header + filter form + empty grid).
- POST on the same route returns the AJAX grid data. The grid wrapper carries a `data-url` for the data load; filters use Select2 + `form_datetime` pickers; export uses the standard async-task UI helper.

## What the merchant can do here

### Header

- Page title: *"Products"* (`global.products`).
- **Export** button (top-right) — async chunked export of the filtered product list. See [[orders-supplier-products-export]].

### List table (5 columns, 4 without Suppliers app)

| Column | Notes |
|--------|-------|
| **Product** (`name_list`) | Product name + image + variant info. Custom rendering. |
| **Order IDs** (`order_ids`) | Comma-separated list of order IDs containing this product (each clickable, opens the order in a new tab via the `admin.orders.details` route). |
| **Line price** | The line price (typically per-unit price at order time). |
| **Ordered quantity** | The SUM of quantities across all matching orders for this product. Normalised display. See [[orders-supplier-products-aggregation]]. |
| **Suppliers** (conditional — only when Suppliers app installed) | Supplier name(s) + cheapest-supplier info from the per-product supplier configuration. See [[orders-supplier-products-suppliers-app]]. |

### What the merchant CANNOT do here

- **Edit products** — it's read-only aggregation. The merchant clicks through to the product editor ([[products-products]]) for changes.
- **Bulk-update orders** (e.g., bulk mark-as-fulfilled) — this is a products view, not an orders view.
- **See per-order detail** — only the aggregated quantity and order-ID list. To dig into one order, click an order ID to open [[orders-details]].
- **Generate a purchase order** to a supplier directly — there is NO "Generate PO from this view" button. The data is the INPUT to that workflow (export → email to supplier / ERP entry / external PO system).

## Settings & fields

The page has no settings of its own. The only thing that changes its shape is whether the **Suppliers** app is installed — which adds the fifth (Suppliers) column and flips the default sort. See [[orders-supplier-products-suppliers-app]].

## Business rules

### No "Generate PO" action

The page is READ-ONLY — it lists products and aggregates demand but does NOT have a "Generate PO from this view" button. The merchant uses Export to produce a file of the filtered data, then drives the purchase order via their own workflow (email to supplier, ERP entry, or external PO system).

### Pure read view — NO supplier notifications

The page does NOT auto-notify suppliers when orders come in. There is NO "auto-send PO email to supplier" trigger from this view. The merchant manually communicates demand to suppliers (export → email → external workflow). For automated supplier communications, the merchant needs ERP integration apps like Gensoft, Universum, Barsy, Versus, etc.

### NO order-splitting — multi-supplier orders are reported, not split

If a customer's order contains products from MULTIPLE suppliers, the order is ONE order record in [[orders]]. The customer sees one combined invoice. This page just AGGREGATES the demand cross-supplier; it does NOT auto-split the order into per-supplier fulfillment requests. Order splitting (if needed for the merchant's workflow) is a manual or app-driven step downstream.

### Order ID list rendering

The `order_ids` column shows a comma-separated list of IDs, each as a hyperlink to the corresponding order's detail page. Useful for the merchant clicking through to a specific order. The list can be truncated for high-volume products — see [[orders-supplier-products-aggregation]].

### Permission

Standard orders permission + (when Suppliers app installed) suppliers permission.

### Side effects

**None** — pure read view. No state changes.

## Related

- [[orders-supplier-products]] — hub.
- [[orders]] — parent list of orders.
- [[orders-products]] — per-order product CRUD (different scope).
- [[orders-details]] — clicking order IDs opens detail there.
- [[products-products]] — clicking a product name opens its editor.
- [[order]] — entity page.
- [[product]] — entity page.

## Open questions

None.
