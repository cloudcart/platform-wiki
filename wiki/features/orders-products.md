---
type: feature
nav_path: "Orders → Order details → Products (CRUD)"
route_name: admin.orders.products.list
route_path: /admin/orders/action/products/:order_id
aliases: ["Order products", "Order line items", "Add product to order", "Edit product on order", "Order CRUD products", "Per-line discount", "Управление на продукти в поръчка"]
tags: [orders, products, line-items, crud, smarty, hub]
plan_gates: []
created: 2026-05-21
updated: 2026-08-03
source_count: 10
---

# Order products (add / edit / remove on order)

## Purpose

The flow for **modifying the products on an existing order** — adding new line items, editing quantity / price / per-item options, removing lines, applying or removing per-line discounts, viewing fulfilled-line details, and the stock + side-effects cascade that every action triggers.

This page is the **hub** for the cluster. The merchant-facing detail (modal field catalogues, validation rules, history action keys, side-effect chains) is split across 7 aspect pages — drill into the aspect that matches the question.

## Where to find it

From [[orders-details]] → **Products table** in the order summary section. Per-row actions appear via the cog icon on each line (visible only on editable lines); the global Add action sits as a `+ Add product` button (or empty-state CTA) below the table. The full table layout + cog menu is documented on [[orders-details-products]].

### Sub-routes (`/admin/orders/action/products/{order_id}/`)

| Route name | Method | Purpose |
|---|---|---|
| `admin.orders.products.list` | GET | Open the product picker. |
| `admin.orders.products.add` | GET | Open the Add modal for a specific product. |
| `admin.orders.products.store` | POST | Save the new line. |
| `admin.orders.products.edit` | GET | Open the Edit modal. |
| `admin.orders.products.update` | POST | Save line changes. |
| `admin.orders.products.delete` | GET | Remove a line. |
| `admin.orders.products.add-discount` | GET | Open the per-line discount modal. |
| `admin.orders.products.store-discount` | POST | Save the per-line discount. |
| `admin.orders.products.delete-discount` | GET | Remove a per-line discount (specific or all). |
| `admin.orders.products.select-delete-discount` | GET | Pick which line discount to remove (when multiple). |
| `admin.orders.products.delete-modifications` | GET | Remove a line modification. |
| `admin.orders.products.fulfillment-popover` | GET | Show the per-line fulfillment popover. |

## Sub-pages (in this cluster)

This feature is split into 7 aspect pages — drill into the aspect that matches the question, not the whole hub.

- [[orders-products-add]] — `+ Add product` flow; picker + Add modal; `override_price` flag; fractional quantity; digital-product rules; `order_product_added` history entry.
- [[orders-products-edit]] — Edit modal; price-on-edit (no `override_price` flag needed); per-item / per-order option editing; **no variant swap**; `order_product_edit` history entry.
- [[orders-products-delete]] — Remove flow; **last-product blocked**; transactional cascade (digital files / taxes / discounts / options / modifications / fulfillment); **bundle cascade**; `order_product_removed` history entry.
- [[orders-products-line-discount]] — Per-line discount modal (Flat / Percent, default Percent); select-delete-discount picker for stacked discounts; "already has a discount" gate; flat-must-be-less-than-price validation; `order_product_discount_add` / `order_product_discount_remove` / `order_product_modification_remove` history entries.
- [[orders-products-fulfillment-popover]] — Read-only popover on fulfilled lines (tracking URL + fulfillment date); the only per-line view that survives `order_fulfillment_id` being set; void waybill via [[orders-shipping-waybill]] to edit / delete.
- [[orders-products-stock-effects]] — Tracked-snapshot rule on the line; add → decrement, edit → diff, delete → restore; `tracking` + `continue_selling` matrix; stock-locations app per-zone sum; search-index re-index + `product.updated` webhook ripple.
- [[orders-products-side-effects]] — Recalculation cascade (totals + tax + shipping + discount); `cc.ajax.reload` panel chain; full history action-key map; `order.updated` webhook (drafts skip); customer-notify on add only; DB row lock.

## What the merchant can do here

- **Add** a line via the catalog picker — see [[orders-products-add]].
- **Edit** an existing line's quantity / price / option values — see [[orders-products-edit]] (no variant change here — delete + re-add to swap variant).
- **Remove** a line — see [[orders-products-delete]] (cannot remove the last line).
- **Attach / remove a per-line discount** — see [[orders-products-line-discount]].
- **Inspect a fulfilled line** via the popover — see [[orders-products-fulfillment-popover]].

### What the merchant CANNOT do here

- **Add / edit / remove anything on an INVOICED order** — the whole line-editing UI is hidden once an invoice number exists (fiscal rule). Correct it with a credit note / return, or sell the extra item on a new order.
- Add to a `completed`, `paid + fulfilled`, `refunded`, or `cancelled` order — cog hidden.
- Edit / remove a line that's part of a generated waybill — void via [[orders-shipping-waybill]] first.
- Add a duplicate digital product to the same order (rejected).
- Bulk-add multiple products in one save — the picker adds one at a time.
- Swap variant on an existing line via Edit — delete and re-add.
- Mutate lines via JSON-API v2 — the [[api-order-products]] resource is read-only; admin-only writes (see [[orders-products-side-effects]] for the read-vs-mutate rationale).

## Settings & fields

Field catalogues live per-aspect:

- Picker (Modal 1) + Add modal (Modal 2): [[orders-products-add]].
- Edit modal (Modal 3): [[orders-products-edit]].
- Per-line discount modal (Modal 4) + select-delete picker (Modal 5): [[orders-products-line-discount]].
- Fulfillment popover (Modal 6): [[orders-products-fulfillment-popover]].

## Business rules

Cluster-wide invariants — each aspect documents its share in detail.

- **🔴 An INVOICED order cannot be edited at all** — once an invoice number exists the line-editing UI is gone (fiscal rule; corrections go through a credit note / return). Un-fulfilling does **not** re-open it. See [[orders-details-products]].
- **Action visibility is otherwise gated on order state** — cog appears only on non-invoiced, pending / paid / authorized, non-fulfilled, non-archived orders with non-fulfilled lines. See [[orders-details-products]] for the visibility matrix.
- **Fulfilled lines lock changes** — void the waybill via [[orders-shipping-waybill]] first.
- **Stock validation gates on `tracking` + `continue_selling`** — see [[orders-products-stock-effects]].
- **Recalculation cascade fires on every save** — totals + tax + shipping + discount re-eval. See [[orders-products-side-effects]].
- **History entries use the action-key map** — `order_product_added` / `order_product_edit` / `order_product_removed` / `order_product_discount_add` / `order_product_discount_remove` / `order_product_modification_remove`. Full map on [[orders-products-side-effects]].
- **Customer-notify fires on ADD only** — edit / remove / discount changes are silent; use [[orders-notify-customer]] manually.
- **Drafts skip `order.updated`** — stock-side `product.updated` still fires.
- **Per-line discounts are SEPARATE from order-level** — order-level discount flow is [[orders-discount-add]].

## Programmatic access

Order line items are exposed as the **read-only** [[api-order-products]] resource on JSON-API v2 — useful for fetching the contents of an order along with per-line price, quantity, variant, options, modifications, and digital-file references. The endpoint is part of the order's relationship graph (see [[api-orders]]).

**Line-item CRUD is admin-panel-only.** JSON-API v2 does not allow mutation — see [[orders-products-side-effects]] for the rationale (every mutation triggers the full recalculation cascade + side-effects chain, which the platform requires to flow through validated admin paths).

## Related

- [[orders-details]] — parent page hosting the products table.
- [[orders-details-products]] — products table SECTION on the details page (cog menu lives there).
- [[orders]] — list (for finding orders).
- [[orders-add]] — manual order creation uses the same product-add flow.
- [[orders-shipping-waybill]] — fulfilled lines must have their waybill voided before edit.
- [[orders-history]] — where the action-key entries appear.
- [[orders-discount-add]] — order-level discount (different from per-line).
- [[orders-notify-customer]] — manual customer comms for edit / remove.
- [[orders-credit]] — credit-note + refund flow for paid-order modification.
- [[orders-status-change]] — cancel an order (alternative to deleting every line).
- [[products-products]] — product catalog (source of products being added).
- [[products-variants-options]] — variant parameters surfaced in the variant selector.
- [[products-inventory]] — per-variant stock screen affected by every line-CRUD action.
- [[products-change-log]] — audit trail with `action = order` Initiator.
- [[settings-cart]] — `order_status_for_quantity_decrease` (decrement timing).
- [[settings-taxes]] — tax delete-and-recompute on every save.
- [[settings-hooks]] — `order.updated` + `product.updated` webhooks.
- [[marketing-discounts]] — automated discount rules that may already discount a line.
- [[api-order-products]] — read-only JSON-API v2 resource.
- [[json-api-v2]] — read-vs-mutate principle.
- [[order]] — entity page.
- [[product]] — entity page.
- [[order-processing-pipeline]] — full status-transition pipeline (product-line edits feed in).
- [[inventory-tracking]] — stock concept hub.
- [[inventory-decrement-timing]] — when stock comes off during the order's status journey.
- [[inventory-restock]] — symmetric restock semantics on cancel / refund / line delete.

## Open questions

None at the hub level. Aspect-specific (verify) items are flagged inside each aspect page.
