---
type: feature
nav_path: "Orders → Order details → Products → Per-line discount"
route_name: admin.orders.products.store-discount
route_path: /admin/orders/action/products/:order_id/store-discount/:line_id
aliases: ["Per-line discount", "Line item discount", "Manual product discount", "Order line discount", "Remove product discount", "Otstapka na produkt v porachka"]
tags: [orders, products, line-items, discount, manual-discount]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[orders-products]]. See the hub for the other aspects (add, edit, delete, fulfillment popover, stock effects, side effects).

# Order products — Per-line discount

## Purpose

The flow for **attaching a manual discount to a specific line** on an order — a flat-currency amount off the per-unit price OR a percentage off — distinct from order-level discounts ([[orders-discount-add]]) and from automated [[marketing-discounts]] rules. Also the flow for removing line-level discounts, including the **select-delete-discount picker** that opens when a line has multiple stacked discounts.

## Where to find it

[[orders-details]] → products table → per-row cog → **Add product discount** (visible when the line has NO existing discount and isn't MSRP). To remove: cog → **Remove product discount**.

## What the merchant can do here

- **Add a manual line discount** — pick type (Flat or Percent), type the amount, save.
- **Tweak an existing line discount's value** — done inline from the Edit modal (see [[orders-products-edit]] — the existing-discount-value field).
- **Remove a line discount** — single-discount lines fire a direct delete confirmation; multi-discount lines route to the select-delete picker.
- **Remove a per-line modification** — separate route `delete-modifications`, not part of this discount flow (see Business rules below).

## Settings & fields

### Per-line discount add modal (Modal 4 — `product/add-discount.tpl`)

The modal is currently **manual-only** — the existing-discount picker is commented out in the template. The merchant sees ONLY two fields:

| Field | Element | Default | Notes |
|---|---|---|---|
| **Discount type** | Select | **Percent** | Two options: **Flat** (currency amount off line price) OR **Percent** (% off line price). |
| **Discount amount** | Text input | empty | Mask switches dynamically: percent-mask when type=Percent, currency-mask when type=Flat. The affix shows `%` or the currency symbol per the site's `currency.position` setting (before / after). |

A hidden input `discount_variant=manual` is submitted. There is NO reason / note field, NO existing-discount picker. To attach a discount from an existing [[marketing-discounts]] rule, the merchant uses the order-level discount flow on [[orders-discount-add]] — that modal still surfaces existing campaigns.

Submission posts to `admin.orders.products.store-discount`. On success, fires `cc.ajax.reload` on `#order_preview`, `#order_summary`, `#order_history`.

### Select-delete-discount picker (Modal 5 — `products/select_discount_to_delete.tpl`)

Opens automatically when a line has MULTIPLE discounts attached (manual + discount-code, or any combination) AND the merchant clicks **Remove product discount**. The platform throws a `SidebarOpen` exception (when `hasMultipleDiscounts` returns true on the `delete-discount` route) to surface the picker. Single-discount lines skip this — they go straight to direct delete.

| Column | Notes |
|---|---|
| **Name** | *"Global discount"* (for manual) or the `discount_code` label. |
| **Discount** | Per-unit discounted amount. |
| **Total** | Total discount across the line quantity. |
| **Action** | Red minus icon — `data-confirm` confirms then POSTs to `admin.orders.products.delete-discount/<key>` where `<key>` is `global` (manual) or `discount_code`. |

The merchant picks WHICH discount to remove. This prevents accidental removal of the wrong discount when multiple are stacked.

## Business rules

### Per-line discount BLOCKS when a discount already exists on the line

The "Add discount" modal rejects with *"Product already has a discount"* if the line ALREADY has any kind of discount attached (manual, code-applied, or auto-applied from [[marketing-discounts]]). The merchant must REMOVE the existing line discount first before adding a new one. So "stacking per-line discounts" via this manual modal is not possible — the multiple-discounts state arises only when an automated discount-code or campaign applies ON TOP of an existing manual one (or vice-versa), not via repeated use of this form.

### Flat discount must be STRICTLY less than the line price

Manual flat discounts are validated: the discount value must be **strictly less than the line's per-unit price**. If the entered flat discount equals or exceeds the line price, the platform rejects with *"Flat discount must be less than product price"*. For 100%-off scenarios, the merchant uses **Percent** type with value 100.

### Per-line discounts are separate from order-level discounts

Line discounts are MANUAL merchant adjustments at the line level — they:

- Do NOT show in [[marketing-discounts]] reports.
- Are visible in the order's totals breakdown.
- Can be stacked with order-level discounts ([[orders-discount-add]]).
- Survive line-quantity edits — the discount stays on the line.

### Order-level discount cascade — "modifications" are line-level mirrors

When an order-level discount applies, the platform creates cascading line-level entries called **modifications** that mirror the discount across individual lines. Removing a single line's modification is handled by `admin.orders.products.delete-modifications`; removing the parent order discount uses `admin.orders.products.delete-discount`. The cog menu picks the right route automatically — the merchant doesn't see the distinction directly. See [[orders-discount-add]] for the full cascade flow.

### History entries — distinct action keys per discount action

- `order_product_discount_add` (action code 30) — per-line discount added.
- `order_product_discount_remove` (action code 32) — per-line discount removed.
- `order_product_modification_remove` (action code 56) — per-line modification removed.

See [[orders-products-side-effects]] for the full action-key map.

### Customer is NOT notified on discount add or remove

Discount add / remove does NOT email the customer. The auto-notify fires only on product **add** (see [[orders-products-add]]). For comms, the merchant uses [[orders-notify-customer]] manually.

### Drafts skip the `order.updated` webhook

For draft orders, discount add / remove does NOT fire `order.updated`. See [[orders-products-side-effects]].

## Related

- [[orders-products]] — hub.
- [[orders-products-edit]] — the existing-discount-value field on the Edit modal lets the merchant tweak an attached discount's value inline.
- [[orders-products-side-effects]] — history action keys + panel reloads.
- [[orders-details-products]] — products table where the cog → Add/Remove discount lives.
- [[orders-discount-add]] — order-level discount flow + existing-discount picker (the per-line modal's commented-out feature lives there).
- [[marketing-discounts]] — automated discount rules that may already have discounted the line (and block the manual add).
- [[orders-history]] — discount add / remove appear in the timeline.

## Open questions

None.
