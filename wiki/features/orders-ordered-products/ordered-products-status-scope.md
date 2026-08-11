---
type: feature
nav_path: "Orders → Ordered Products → Status scope"
route_name: suppliers.products_by_orders
route_path: /admin/products_by_orders
aliases: ["Ordered Products status scope", "All statuses by default", "Pending not_fulfilled constraint", "Ordered Products date_added basis", "Поръчани продукти — обхват по статус"]
tags: [orders, products, status, fulfillment]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 4
---
> Part of [[orders-ordered-products]]. See the hub for related aspects (overview, filters, aggregation, suppliers, API).

# Ordered Products — status & date scope

## Purpose

Which orders actually count toward the [[orders-ordered-products]] pivot totals. This is the page's most important set of caveats — the defaults silently overstate demand, the `pending` filter hides partially-fulfilled orders, and the date filter is keyed to creation date rather than payment date. This aspect answers "why are my totals wrong / surprising?". The grouping math itself is in [[ordered-products-aggregation]].

## Where to find it

Sidebar → **Orders** → **Ordered Products**. The behaviours here are driven by the **Order status** and **Order date interval** filters in the rail — see [[ordered-products-filters]] for the filter operators.

## What the merchant can do here

The merchant controls scope through the filters, but must understand the non-obvious defaults:

- **Apply a status filter** (typically `paid` + `completed`) before trusting any total.
- **Apply a date filter** to bound the window and keep the query responsive.
- **Be aware** the `pending` status filter is narrower than it looks, and the date filter is keyed to order creation date.

## Settings & fields

### All order statuses included by default

With NO status filter applied, the pivot aggregates orders REGARDLESS of status — including `refunded` / `cancelled` / `chargebacked` / `failed` orders. This inflates `ordered_quantity`. The page does NOT auto-default to "paid / completed only" — scoping is the merchant's responsibility. Always apply the **Order status** filter before drawing demand conclusions.

### `pending` status has a hidden `status_fulfillment` constraint

When the merchant filters by status = `pending`, the platform ADDS an implicit filter `status_fulfillment = "not_fulfilled"`. So a `pending` order with **partial** fulfillment is EXCLUDED from the pivot. Other statuses (`paid`, `completed`, etc.) do NOT apply this implicit constraint.

Net effect: filtering `pending` actually shows "pending AND no-fulfillment-started" orders. Merchants tracking pending-but-partially-fulfilled inventory will miss those products in this view.

### Date filter operates on `date_added`

The **Order date interval** filter compares against the order's `date_added` (creation date) — NOT `date_paid`, `date_fulfilled`, or any other timestamp. So "last 30 days" means orders CREATED in the last 30 days, regardless of when they were paid or fulfilled. Merchants analysing fulfillment performance should account for this distinction.

### Unbounded date range by default

With no date filter, the pivot runs across the full order history. For stores with millions of order lines, apply a date filter early — both for query responsiveness and because "all time" totals are not useful for current restocking decisions.

## Business rules

### Scope your way to real demand

The reliable recipe for "real units sold": status = `paid` (+ `completed` if the store uses it) AND an explicit date interval. This excludes the cancelled / refunded / failed noise and bounds the window. Without both, the totals are an upper bound, not actual demand.

### Status values come from the store's taxonomy

The status options in the filter are the store's configured order statuses ([[settings-statuses]]) — they are not hard-coded. A store with custom statuses sees those in the dropdown; the `pending → not_fulfilled` implicit rule applies specifically to the `pending` status value.

### Side effects

None — filtering is part of a pure read view. The export ([[orders-ordered-products-export]]) carries the same status / date scope as the on-screen pivot.

## Related

- [[orders-ordered-products]] — hub.
- [[ordered-products-filters]] — the status / date filter operators.
- [[settings-statuses]] — the order status taxonomy the filter draws from.
- [[orders-ordered-products-export]] — export inherits this scope.
- [[order]] — entity page; `date_added`, `status`, `status_fulfillment`.

## Open questions

(None.)
