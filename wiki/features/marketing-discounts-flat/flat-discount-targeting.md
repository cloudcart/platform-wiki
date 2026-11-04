---
type: feature
nav_path: "Marketing → Discounts → Flat → Targeting"
route_name: discounts-create
route_path: /admin/marketing/discounts/create/global
aliases: ["Flat discount target", "Flat discount settings field", "Flat order_over", "Flat product target", "Flat category target", "Flat vendor target", "Flat smart collection target", "Flat category+vendor", "Flat discount distribution", "Cent-fix on first matched line", "force_save flat"]
tags: [marketing, discounts, flat, targeting, settings, distribution]
plan_gates: ["discount_global", "discount_coupon"]
created: 2026-06-10
updated: 2026-11-04
source_count: 4
---

> Part of [[marketing-discounts-flat]]. See the hub for the other aspects (form entry, value mechanics, eligibility, stacking, programmatic access).

# Flat discount — targeting

## Purpose

This page documents **where on the cart the Flat amount lands** — the seven values of the `settings` enum, how the amount distributes across multiple matched lines (with the cent-fix on the first matched line), and the `force_save` toggle that pins an `order_over` discount onto an existing order.

Tickets that land here: *"why is one line's discount 1 cent off from the others"*, *"the merchant edited an order and the discount disappeared"*.

## Where to find it

The **Discount target** block on the create / edit form (see [[flat-discount-form-entry]]). The dropdown picks the `settings` enum; selecting a value reveals the matching sub-form.

## What the merchant can do here

- Pick a target from the seven `settings` enum values.
- Combine `product_categories[]` + `vendors[]` via the **Category + vendor** intersection target.
- Toggle **Save the discount on your order** (`force_save`) on `order_over` targets.

## Settings & fields

| Field | Backend key | What it does | Validation |
|-------|-------------|--------------|------------|
| **Discount target** | `settings` | One of `all`, `order_over`, `product`, `product_category`, `product_vendor`, `selection`, `category_vendor`. | *"Settings must be one of: all, order_over, product, product_category, product_vendor, selection, category_vendor"*. |
| **Order amount threshold** | `order_over` | Cart-subtotal threshold for `order_over` target. | Required if settings=order_over; no maximum. *"Order over is required if settings is order over"*. |
| **Save the discount on your order** | `force_save` | When ON, the discount stays attached to a previously-saved order even when admin-side edits drop the cart below the threshold. | 1 / 0. Only shown for `order_over`. |
| **Products** | `products[]` | Product IDs to attach. | Required if settings=product. *"Products is required if settings is product"*. |
| **Product categories** | `product_categories[]` | Category IDs. | Required if settings=product_category; used with vendors for category_vendor. *"Product categories is required if settings is product category"*. |
| **Product vendors** | `vendors[]` | Vendor IDs. | Required if settings=product_vendor; used with categories for category_vendor. *"Vendors is required if settings is product vendor"*. |
| **Smart collections** | `selections[]` | Smart-collection IDs. | Required if settings=selection. *"Selections is required if settings is selection"*. |

### Target reference table

Each Flat discount targets exactly **one** of the seven values.

| Target value (`settings`) | Means | Companion fields |
|---------------------------|-------|------------------|
| `all` — *"For every product in the cart"* / *"За всеки продукт в количката"* | Code: the full amount off every line. No code: off each unit, as the product's own price. | — |
| `order_over` — *"Orders over"* / *"Поръчки над"* | Cart subtotal must be strictly above `order_over` EUR. One amount off the order. | `order_over` amount, optional `force_save`. |
| `product` — *"Specific product/s"* / *"Конкретен продукт/и"* | Only listed products carry the flat-off. | `products[]`. |
| `product_category` — *"Product category/categories"* / *"Продуктова категория"* | Only products in the listed [[products-categories]]. | `product_categories[]`. |
| `product_vendor` — *"Product vendor/s"* / *"Марка"* | Only products of the listed [[products-vendors]]. | `vendors[]`. |
| `selection` — *"Smart collection/s"* / *"Колекция"* | Only products in the listed [[products-smart-collections]]. | `selections[]`. |
| `category_vendor` — *"Product category/categories and vendor/s"* / *"Категория и производител"* | Intersection: products in category X **AND** by vendor Y. | Both `product_categories[]` and `vendors[]`. |

## Business rules

### What the amount comes off

See [[discount-stacking-amount-by-target]] for the full table.

- **Target = `all`, code** — the full amount comes off every line, once per line, whatever the quantity. No split, no rounding fix, no lower limit on a line, so a line and the total can go below zero.
- **Target = `all`, no code** — off each unit, as the product's own price, listings included. A product whose lowest price is below the amount gets nothing. Bundles are left out.
- **Target = `order_over`** — one amount off the order, shown as a row in the totals, when the subtotal is strictly above the threshold.
- **Target = `product` / `product_category` / `product_vendor` / `selection` / `category_vendor`, code** — one amount split proportionally across the matching lines. Non-matching lines keep their full price.
- **Same targets, no code** — off each unit of those products, as their own price.

### Cent-distribution rounding — drift compensation lands on the FIRST matched line

A Flat code on a specific target splits across the matching lines, so per-line rounding can cause the sum of allocated discount amounts to drift by 1-2 cents from the discount's total `type_value`. The platform runs an automatic **cent-fix step** after the per-line allocation:

- It sums all per-line discount amounts.
- If the sum does NOT equal the original `type_value`, the difference (positive or negative) is added to the **first matched line that took the code**.

This ensures the customer's total saving equals the discount exactly. On a multi-line cart, rounding alone moves the first line's discount by 1-2 cents. With `code_apply` off, the skipped lines' whole share lands there too (see [[flat-discount-stacking]]).

### `force_save` — keep the discount attached after admin-side edits

For Flat discounts with `settings = order_over`, the merchant can toggle **Save the discount on your order**. When ON, an admin editing an order that previously qualified for the discount keeps the discount attached **EVEN IF** the new cart contents fall below the `order_over` threshold. Without `force_save`, the discount stays listed on the order, but its amount stops being deducted while the subtotal is not above the threshold.

The toggle only appears for `order_over` (it's irrelevant for `all` and meaningless for product / category / vendor / selection targets where the discount lives on the matched lines themselves).

## Related

- [[marketing-discounts-flat]] — hub.
- [[flat-discount-value-mechanics]] — `type_value` cents storage + matched-subtotal ≥ amount rule + strictly-greater `order_over` check.
- [[flat-discount-eligibility]] — filters that apply before a target is matched.
- [[flat-discount-stacking]] — `code_apply` rules; the `code_apply = 0` skip on `all` and specific targets when the line is already discounted.
- [[products-categories]] — target via `product_categories[]`.
- [[products-vendors]] — target via `vendors[]`.
- [[products-smart-collections]] — target via `selections[]`.

## Open questions

None.
