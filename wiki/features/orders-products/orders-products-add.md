---
type: feature
nav_path: "Orders → Order details → Products → Add"
route_name: admin.orders.products.store
route_path: /admin/orders/action/products/:order_id/store
aliases: ["Add product to order", "Order add line item", "Order line add", "Product picker on order", "Dobavi produkt v porachka"]
tags: [orders, products, line-items, add, picker]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 4
---

> Part of [[orders-products]]. See the hub for the other aspects (edit, delete, line discount, fulfillment popover, stock effects, side effects).

# Order products — Add line

## Purpose

The flow for **adding a new product line to an existing order** — the merchant clicks `+ Add product` under the products table on [[orders-details-products]], browses the catalog via the picker, picks a variant + quantity (and optionally overrides the per-unit price for this line only), and saves. This is the same flow used during draft-order construction on [[orders-add]].

## Where to find it

From [[orders-details]] → products table → `+ Add product` button below the table (or as an empty-state CTA if the order has no lines yet). The button opens the picker as a side-panel (in preview mode) or a wide modal.

## What the merchant can do here

- **Browse / search** the catalog via the standard products filter (vendor / category / status / tags / text search) — same controls as the main [[products-products]] list.
- **Pick a variant** when the product has one (one Select2 dropdown per parameter, `p1`/`p2`/`p3`; layout switches to 3-column when the product has 3 params).
- **Fill in per-product fields** (custom checkboxes / text / textarea / radio / select / file / image / length / square / weight options).
- **Type a quantity** (supports fractional values — min 0.001).
- **Override the per-unit price** for this line only by ticking the `override_price` checkbox and typing a `price` value.
- **Save** — POST `admin.orders.products.store`.

## Settings & fields

### Picker (Modal 1)

| Element | Notes |
|---|---|
| **Filter bar** | Reuses the products list filter UI from [[products-products]]. |
| **Listing columns** | Image + name (`name`) — Parameters — Quantity (clickable, opens Add modal) — Edit icon. |
| **Empty state** | "No products to show" + products icon when the catalog is empty. |

The merchant clicks the quantity cell on a row → opens the Add modal below.

### Add modal (Modal 2 — `product/add.tpl`)

| Field | Element | Default | Notes |
|---|---|---|---|
| **Parameter selector(s)** | Select2 dropdowns (`p1`, `p2`, `p3`) | — | One per product parameter. Picking the first enables the second. |
| **Per-product fields** | Variable | — | Custom fields chunked 2-per-row; included from `product/options/<type>.tpl`. Each adds a typed entry to `option[<field_id>]`. |
| **Variant info table** | Read-only | — | Shown after parameters resolve: SKU / Barcode / Price (with discounted variant) / Quantity / Weight. |
| **Quantity** | Text input | `minimum_unit` from variant (default `1`) | Numeric, min 0.001 (fractional supported). When `grocery_store` app is installed AND variant has a unit configured, decimal step + min + step-divisibility come from the unit definition. |
| **Override price** | Checkbox (`override_price`) | **CHECKED** | When checked, the typed `price` overrides the variant's catalog price for THIS line only. When unchecked, the variant's current catalog price is used (`price` input is ignored on save). |
| **Price** | Text input (currency mask) | empty | Manual per-unit price; only honoured when `override_price` is checked. |

Submission posts via `ajaxForm` to `admin.orders.products.store`. On success, fires `cc.ajax.reload` on FIVE sub-panels: `#order_preview` (preview mode only), `#order_summary`, `#order_customer`, `#order_shipping_address`, `#order_billing_address`.

### Pricing snapshot at add-time

The platform reads the variant's **current** catalog price at the moment of save and writes it to the line. A later catalog price change does NOT auto-propagate to existing order lines. See `## Pricing — snapshot` on the hub.

### Bulk add — not supported

The picker adds ONE product per save. There is no multi-select. For bulk order construction, the merchant uses [[orders-add]] (manual order) with repeats or the JSON-API v2 (see [[api-orders]]). (verify)

## Business rules

### Add is gated on order state

The `+ Add product` button is hidden when the order is in `completed`, `paid + fulfilled`, `refunded`, or `cancelled` status — only `pending` / `paid` non-fulfilled orders accept new lines. See [[orders-details]] header for the editable-state matrix.

### Stock validation — variant must have enough

When the variant has `tracking = yes` AND `continue_selling = no` AND the requested quantity exceeds available stock, the platform throws *"Not enough quantity for `<quantity>`"* and the line is NOT added. No auto-cap. When `continue_selling = yes`, oversell is allowed — see [[orders-products-stock-effects]].

### Last product cannot be removed → adding is mandatory before delete

The platform requires every order to have at least one line. Combined with the delete-blocks-last-line rule (see [[orders-products-delete]]), the merchant must add a replacement before removing the last existing line.

### Adding a duplicate digital product to the same order is blocked

If the merchant tries to add a digital product that is ALREADY a line on the order, the platform rejects with *"Cannot add digital product already in cart"*. Digital products are unique per order — the same digital file cannot be sold twice in one order.

### Adding a digital product to an all-digital order auto-fulfils

When the order has products AND all existing products are digital (no physical lines), adding another digital product auto-creates a new fulfillment for the added line — digital products are fulfilled instantly. For mixed orders (physical + digital), the added digital line is NOT auto-fulfilled — the merchant runs the normal fulfillment flow on [[orders-shipping-waybill]].

### Customer notification fires on ADD only

The platform emails the customer (per the order's `notify_customer` setting) ONLY for product ADD events. Edit and remove do NOT notify. For removal / price-change comms, the merchant uses [[orders-notify-customer]] manually.

### History entry — `order_product_added`

Adding a line writes a history entry with action key `order_product_added` (action code 24) on [[orders-history]] — see [[orders-products-side-effects]] for the full action-key map.

### Plan-feature gate — `multi_variants`

When the product has variants and the store is on a plan WITHOUT the `multi_variants` plan-feature, variant pickers are disabled / hidden. (verify)

## Related

- [[orders-products]] — hub.
- [[orders-products-edit]] — re-pricing or re-quantity an existing line.
- [[orders-products-delete]] — removing a line; cannot remove the last one.
- [[orders-products-line-discount]] — applying a manual per-line discount AFTER adding.
- [[orders-products-stock-effects]] — stock decrement timing on add.
- [[orders-products-side-effects]] — recalc cascade + panel reloads after save.
- [[orders-details-products]] — the products table section on order details.
- [[orders-add]] — manual order creation uses the same add flow.
- [[products-products]] — the catalog browsed by the picker.
- [[products-variants-options]] — variant parameters surfaced in the selector.
- [[settings-cart]] — `order_status_for_quantity_decrease` (stock decrement timing).
- [[inventory-decrement-timing]] — when add actually moves stock.

## Open questions

- Confirm `multi_variants` plan-feature gate on variant selectors (verify).
- Confirm bulk-add via JSON-API v2 is supported via `api-orders` includes (verify).
