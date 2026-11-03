---
type: feature
nav_path: "Orders → Order details → Products → Edit"
route_name: admin.orders.products.update
route_path: /admin/orders/action/products/:order_id/update/:line_id
aliases: ["Edit order line", "Order edit product", "Edit line quantity", "Edit line price", "Redaktirai produkt v porachka"]
tags: [orders, products, line-items, edit]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[orders-products]]. See the hub for the other aspects (add, delete, line discount, fulfillment popover, stock effects, side effects).

# Order products — Edit line

## Purpose

The flow for **editing an existing product line** on an order — re-pricing the line, changing the quantity, tweaking an already-attached discount value, or adjusting per-item / per-order option values. The line's **variant cannot be swapped** here; to change variant the merchant must delete and re-add the line via [[orders-products-add]].

## Where to find it

[[orders-details]] → products table → per-row cog → **Edit**. The cog is visible only for pending / paid orders with non-fulfilled, non-digital lines (see [[orders-details-products]] for the cog-visibility matrix).

## What the merchant can do here

- **Change the quantity** (fractional supported — min 0.001).
- **Re-price the line** by typing a new per-unit `price` (no separate `override_price` flag is required on edit — the price input is always honoured).
- **Tweak an already-attached discount's value** inline (only when the line has an existing discount).
- **Edit per-item option values** — for each per-item modification (length / square / engraving / gift-wrap / etc.), set a new amount (flat currency mask OR percent mask, per option type).
- **Edit per-order option values** — same idea for options that apply at the order level.
- **Save** — POST `admin.orders.products.update`.

## Settings & fields

### Edit modal (Modal 3 — `product/edit.tpl`)

| Field | Element | Default | Visible when |
|---|---|---|---|
| **Quantity** | Text input | line's stored `quantity_unit_input` | Hidden for digital products (digital lines have qty=1 forever). |
| **Price** | Text input (currency mask) | line's stored per-unit price | Always shown. |
| **Existing-discount value** | Text input (currency-mask or percent-mask, depending on existing discount type) | line's existing discount value | Shown only when the line `hasDiscount`. |
| **Per-item option values** | Variable (one row per option, chunked 2-per-row) | option's stored amount | Each non-length / non-square per-item option. Flat options use currency-mask input on `option[<id>][discount_price]`; percent options use percent-mask. A hidden `option[<id>][price]` carries the original price. |
| **Non-per-item option values** | Same | Same | One row per non-per-item option (from `getSingleOptions`). |
| **Length-square option fields** | Composite | Inherited | Length / square options use dedicated includes (`options/length.tpl`, `options/square.tpl`) that combine length + weight inputs — visible when the product has those modification types. |

Submission posts to `admin.orders.products.update`. On success, fires `cc.ajax.reload` on `#order_preview`, `#order_summary`, `#order_history` (3 panels) — see [[orders-products-side-effects]].

### No variant change

There is **no variant selector** on the Edit modal — the merchant CANNOT swap variant on an existing line. To change variant: delete the line via [[orders-products-delete]] and re-add via [[orders-products-add]].

## Business rules

### Pricing is a snapshot — defaults to stored value

The price input defaults to the line's stored per-unit price (the snapshot taken at add-time), NOT the variant's current catalog price. A catalog price change after the order was created does NOT auto-propagate — the order keeps its historical pricing. Re-pricing is a manual decision per line.

### Quantity edit applies the diff to stock

When the line is tracked (the variant's `tracking` flag was on at the time the line was created), saving a quantity change adjusts the variant's `quantity` by the DIFF — not the new total. If `tracking` was OFF at line creation, no stock adjustment happens regardless of the variant's current tracking flag. See [[orders-products-stock-effects]] for the tracked-snapshot rule.

### Edit triggers a shipping re-quote

Saving a quantity / price edit re-runs the courier quote API to recompute shipping cost — a new weight or value may change the rate. The order's shipping line may update silently. The merchant should verify the shipping total after editing.

### Edit triggers tax recalculation

Each line's tax is recomputed against the order's VAT-eligible address and the product's taxability. The platform deletes ALL non-product-level VAT taxes and re-computes them on every line save, so totals stay consistent. See [[settings-taxes]].

### Edit fires `order_product_edit` history entry

Every save writes an entry with action key `order_product_edit` (action code 29) on [[orders-history]] — see [[orders-products-side-effects]].

### Customer is NOT notified on edit

Editing a line does NOT send an automatic customer email. For comms, the merchant uses [[orders-notify-customer]] manually.

### Fulfilled lines are blocked from edit

Once the line is part of a generated waybill (`order_fulfillment_id` is set), the Edit option in the cog is BLOCKED. The merchant must void the waybill via [[orders-shipping-waybill]] first.

### Drafts skip the `order.updated` webhook

For draft orders (created via [[orders-add]] but not yet finalised), edits do NOT fire `order.updated` — see [[orders-products-side-effects]] for the webhook gating.

## Related

- [[orders-products]] — hub.
- [[orders-products-add]] — to swap variant, delete then re-add.
- [[orders-products-delete]] — removing a line.
- [[orders-products-line-discount]] — the tweak-discount-value inline path uses the Edit modal; adding a NEW discount is on its own modal.
- [[orders-products-stock-effects]] — quantity-edit diff applied to stock; tracked-snapshot rule.
- [[orders-products-side-effects]] — panel reloads, history action keys, webhook gating.
- [[orders-details-products]] — products table where the cog → Edit lives.
- [[orders-shipping-waybill]] — void waybill before editing a fulfilled line.
- [[settings-taxes]] — tax recalc per save.
- [[products-change-log]] — stock changes from quantity edits appear on the product's Change log.

## Open questions

None.
