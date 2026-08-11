---
type: feature
nav_path: "Marketing → Discounts → Flat → Targeting"
route_name: discounts-create
route_path: /admin/marketing-new/discounts/create/global
aliases: ["Flat discount target", "Flat discount settings field", "Flat order_over", "Flat product target", "Flat category target", "Flat vendor target", "Flat smart collection target", "Flat category+vendor", "Flat discount distribution", "Cent-fix on first matched line", "force_save flat"]
tags: [marketing, discounts, flat, targeting, settings, distribution]
plan_gates: ["discount_global", "discount_coupon"]
created: 2026-06-10
updated: 2026-06-10
source_count: 4
---

> Part of [[marketing-discounts-flat]]. See the hub for the other aspects (form entry, value mechanics, eligibility, stacking, programmatic access).

# Flat discount — targeting

## Purpose

This page documents **where on the cart the Flat amount lands** — the seven values of the `settings` enum, the mutual-exclusion validation rules between the target arrays, how the amount distributes across multiple matched lines (with the cent-fix on the first matched line), and the `force_save` toggle that pins an `order_over` discount onto an existing order.

Tickets that land here: *"my code says 'product categories can not be used with orders over'"*, *"why is one line's discount 1 cent off from the others"*, *"the merchant edited an order and the discount disappeared"*.

## Where to find it

The **Discount target** block on the create / edit form (see [[flat-discount-form-entry]]). The dropdown picks the `settings` enum; selecting a value reveals the matching sub-form.

## What the merchant can do here

- Pick a target from the seven `settings` enum values.
- Combine `product_categories[]` + `vendors[]` via the **Category + vendor** intersection target.
- Toggle **Save the discount in the order** (`force_save`) on `order_over` targets.

### What the merchant CANNOT do here

- Combine `products[]` with `order_over`.
- Combine `product_categories[]` with `products` / `order_over` / `selections`.
- Use a **parent category and its child** at the same time.

## Settings & fields

| Field | Backend key | What it does | Validation |
|-------|-------------|--------------|------------|
| **Discount target** | `settings` | One of `all`, `order_over`, `product`, `product_category`, `product_vendor`, `selection`, `category_vendor`. | Required. *"The field settings is required"*. |
| **Order amount threshold** | `order_over` | Cart-subtotal threshold for `order_over` target. | Required if settings=order_over; max **10,000 EUR** (1,000,000 cents). *"The field orders over can not be empty"*. |
| **Save the discount in the order** | `force_save` | When ON, the discount stays attached to a previously-saved order even when admin-side edits drop the cart below the threshold. | 1 / 0. Only shown for `order_over`. |
| **Products** | `products[]` | Product IDs to attach. | Required if settings=product. *"Please choose a product"*. Cannot combine with `order_over` / `product_categories`. |
| **Product categories** | `product_categories[]` | Category IDs. | Required if settings=product_category or category_vendor. *"Please choose a product category"*. Parent + child rejected. |
| **Product vendors** | `vendors[]` | Vendor IDs. | Required if settings=product_vendor or category_vendor. |
| **Smart collections** | `selections[]` | Smart-collection IDs. | Required if settings=selection. |

### Target reference table

| Target value (`settings`) | Means | Companion fields |
|---------------------------|-------|------------------|
| `all` — *"For every product in the cart"* | Cart-wide flat amount off. | — |
| `order_over` — *"Orders over"* | Cart subtotal must be ≥ `order_over` EUR. | `order_over` amount, optional `force_save`. |
| `product` — *"Specific product/s"* | Only listed products carry the flat-off. | `products[]`. |
| `product_category` — *"Product category/categories"* | Only products in the listed [[products-categories]]. | `product_categories[]`. |
| `product_vendor` — *"Product vendor/s"* | Only products of the listed [[products-vendors]]. | `vendors[]`. |
| `selection` — *"Smart collection/s"* | Only products in the listed [[products-smart-collections]]. | `selections[]`. |
| `category_vendor` — *"Product category/categories and vendor/s"* | Intersection: products in category X **AND** by vendor Y. | Both `product_categories[]` and `vendors[]`. |

## Business rules

### Cart-wide vs targeted distribution

- **Target = `all`** — The flat amount is subtracted from the **whole cart**. If the merchant offers 20 EUR off a 100 EUR cart, the customer pays 80 EUR.
- **Target = `order_over`** — Same as `all`, but only applies when cart subtotal ≥ `order_over`. The discount itself is still cart-wide. (Note: code-based variants use a **strictly-greater** check — see [[flat-discount-value-mechanics]].)
- **Target = `product` / `product_category` / `product_vendor` / `selection` / `category_vendor`** — The flat amount is subtracted from the **subtotal of the matched lines**, then distributed proportionally across those lines (so each line's per-unit price reflects its share). Non-matched lines keep their full price.

### Mutual-exclusion validation between target arrays

The validator rejects forbidden field combinations at save time:

- *"The field products can not be used with orders over"*.
- *"The field product_categories can not be used with orders over"*.
- *"The field product_categories can not be used with products"*.
- *"The field product_categories can not be used with selections"*.

Each Flat discount targets exactly **one** of the seven enum values; the cross-field validators ensure the companion arrays match the picked target.

### Parent + child category rejected

When the merchant picks `product_category` or `category_vendor` and the selected `product_categories[]` contains both a parent category AND any of its descendants, the save rejects with:

> *"Parent and Child product categories, can not be included"*

The merchant must pick either the parent OR the children, not both — the engine cannot disambiguate which level the discount targets when both are present.

### Cent-distribution rounding — drift compensation lands on the FIRST matched line

Because a Flat discount distributes across multiple cart lines (when target is multi-line), per-line rounding can cause the sum of allocated discount amounts to drift by 1-2 cents from the discount's total `type_value`. The platform runs an automatic **cent-fix step** after the per-line allocation:

- It sums all per-line discount amounts.
- If the sum does NOT equal the original `type_value`, the difference (positive or negative) is added to the **first matched line** in the cart's iteration order.

This ensures the customer's total saving equals the discount exactly — no rounding loss in the merchant's favour or the customer's favour. The merchant-visible side-effect: on a multi-line cart, the first matched line's per-unit discount may be 1-2 cents higher or lower than mathematically expected — that's the drift fix, not a bug.

### `force_save` — keep the discount attached after admin-side edits

For Flat discounts with `settings = order_over`, the merchant can toggle **Save the discount in the order**. When ON, an admin editing an order that previously qualified for the discount keeps the discount attached **EVEN IF** the new cart contents fall below the `order_over` threshold. Without `force_save`, editing such an order removes the discount.

The toggle only appears for `order_over` (it's irrelevant for `all` and meaningless for product / category / vendor / selection targets where the discount lives on the matched lines themselves).

### Cart-engine matching loop

At checkout the discount engine, for each active Flat discount, first applies the eligibility filters (`customer_groups[]`, `geo_zone_id`, `only_customer`, date window, uses-remaining — see [[flat-discount-eligibility]]), then reads `settings` and matches the cart per the **Target reference table** above. It computes the matched subtotal, applies the flat amount capped to that subtotal so the discount never exceeds it (see [[flat-discount-value-mechanics]]), and for multi-line matches distributes proportionally and runs the cent-fix step.

## Related

- [[marketing-discounts-flat]] — hub.
- [[flat-discount-value-mechanics]] — `type_value` cents storage + matched-subtotal ≥ amount rule + strictly-greater `order_over` check on codes.
- [[flat-discount-eligibility]] — filters that apply BEFORE the cart-engine matching loop.
- [[flat-discount-stacking]] — `code_apply` rules; the `code_apply = 0` silent skip on `product` / `product_category` targets when the line is already discounted.
- [[products-categories]] — target via `product_categories[]`.
- [[products-vendors]] — target via `vendors[]`.
- [[products-smart-collections]] — target via `selections[]`.

## Open questions

None.
