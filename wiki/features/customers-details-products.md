---
type: feature
nav_path: "Customers → Customer details → Products"
route_name: customers-products.new
route_path: /admin/customers-new/details/:id/products
aliases: ["Customer products", "Customer purchase history", "Products bought", "Купени продукти от клиента"]
tags: [customers, products, history]
plan_gates: []
created: 2026-05-21
updated: 2026-06-10
source_count: 8
---
# Customer products

## Purpose

The list of **every product purchase** the customer has ever made across all their orders. **One row per order-line** — if the customer bought the same product on three separate orders, three rows are shown (each linked to its respective order). This is a more granular view than [[customers-details-orders]] (which groups by order) — useful for the merchant to see exactly which items the customer favours, identify cross-sell opportunities, or check whether a specific product was sold to a specific customer.

## Where to find it

From [[customers-details]] → **Products** tab. The route is `/admin/customers-new/details/:id/products`.

## What the merchant can do here

A single paginated, read-only table. The merchant can:

- See every product line the customer has purchased.
- Click the product image to open the storefront product URL in a NEW tab (tooltip "See in store").
- Click the product name to open the product editor inside this admin (in-app navigation to `products-edit/:id`) — see [[products-products]].
- Click the order reference to open `/admin/orders/details/<order_id>` in a NEW tab.

### Seven columns

| Column | Notes |
|--------|-------|
| **Product** (`name`) | Product image (variant image preferred over product image; 150×150, falls back to the `noImage` placeholder) + name. Image and name are clickable as above. |
| **Order** (`order_id`) | Renders as `# <order_id>`. Click → order detail page in a NEW tab. |
| **Status** (`order_status`) | Shows a translated badge label (e.g. "Is paid" / "Cancelled") with colour driven by the raw status key (e.g. `paid`, `cancelled`). Reflects the order's **current** status, not a purchase-time snapshot. |
| **Sale** (`sale`) | Green check when the line carries the sale flag (`sale` is truthy AND not the literal string `"no"`); otherwise a dash `-`. Not clickable. |
| **Discount** (`order_discount_id`) | Green check when an **order-level** discount is attached (`order_discount_id` is non-null); otherwise a dash. Not clickable. |
| **Quantity** | Units of this product on the line. Plain text. |
| **Price** (`order_price_formatted`) | The line's price as recorded on the order (currency-formatted). Plain text. |

### What the merchant CANNOT do here

- Edit purchase data — read-only (no Create / Edit / Refund / Cancel modal, no bulk-action bar, no row-action column). All mutations live on the order detail page, reached via the **Order** column.
- Filter by date, status, or product category — only the free-text **query** search box is shown; no filter chips.
- Sort — no column is sortable; sort is fixed at most-recent-first.
- See variant detail (Size / Colour) or line-level discount specifics — those live on the order detail page.

## Settings & fields

This is a read-only summary table. No editable fields, no settings.

## Business rules

### One row per order-line (NOT aggregated)

Unlike a typical "products the customer bought" aggregate, this view shows ONE row per product per order line. A customer who bought the same product on three orders sees three rows. The merchant uses this granularity to trace specific purchase events rather than total quantity.

### Status column reflects CURRENT order state

The Status column shows each order's status at view time, NOT at purchase time. So if the customer's order was Paid two months ago but the merchant refunded it last week, the row now shows Refunded. This means the view doubles as "active purchases vs cancelled / refunded purchases" — useful when evaluating whether a customer's lifetime value is real or includes rolled-back orders.

### Sale and Discount columns are HISTORICAL

Unlike Status (which is live), the Sale flag and Discount association are captured at order time. Removing a sale flag from a product later does NOT change the historical row — so the Sale column is a true record of "was this purchase made under sale conditions?".

### Sale / Discount rendering rules

Both columns use the same renderer: a green check when the bound key is truthy AND not equal to the literal string `"no"`, otherwise a dash. So `sale="yes"` or `sale=true` → check; `sale="no"` → dash (despite "no" being a truthy string); a null/missing `order_discount_id` → dash, any non-null id → check.

### Auto-scoped to one customer (through the order)

The list is automatically filtered by `customer_id`, and the merchant cannot widen it to other customers. The scope traverses the order relation, so lines tied to orders without a `customer_id` (guest checkouts) do NOT appear.

### Permission gate uses **orders**, not customers

The list requires the **orders** permission (`hasApiPermission:orders`), NOT the customers permission. A merchant role with customers access but no orders access sees the Products tab in the UI, but the list will not load. (The validation requires one of `customer_id` or `order_id`, `required_without`; this tab always passes `customer_id`, while the order detail page reuses the same list with `order_id`.)

### Voided AND archived order lines DO appear here (unlike the Orders tab)

No default scope excludes voided or archived parent orders, so their lines are returned with the Status badge showing the parent order's current status (e.g. "Voided"). This is a deliberate difference from the Orders tab, which hard-excludes voided orders and requires the Archived filter to see archived ones. Useful when the merchant wants the customer's COMPLETE history of items ever ordered — including rolled-back ones.

### Item-level discounts exist in the data but aren't shown

Per-line discount detail (name + amount) is present in the data but not surfaced in any column. The Discount column reflects only ORDER-level discounts (via `order_discount_id`); per-line specifics are visible only by clicking through to the order detail page.

### Default pagination = 25

Default page size 25, following the global grid cap.

## Related

- [[customers-details]] — parent details page.
- [[customers-details-orders]] — aggregated view by order (parent of the order lines listed here).
- [[products-products]] — clicking a product name navigates here.
- [[marketing-discounts]] — order-level discount referenced by the Discount column.
- [[order]] — entity page.
- [[product]] — entity page.

## Open questions
