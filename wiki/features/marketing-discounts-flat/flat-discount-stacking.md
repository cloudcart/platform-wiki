---
type: feature
nav_path: "Marketing → Discounts → Flat → Stacking"
route_name: discounts-create
route_path: /admin/marketing/discounts/create/code
aliases: ["Flat discount stacking", "code_apply flat", "apply_regular_price flat", "Flat plus quantity tier", "Flat plus cart rules"]
tags: [marketing, discounts, flat, stacking, code_apply, apply_regular_price]
plan_gates: ["discount_global", "discount_coupon"]
created: 2026-06-10
updated: 2026-11-04
source_count: 4
---

> Part of [[marketing-discounts-flat]]. See the hub for the other aspects (form entry, targeting, value mechanics, eligibility, programmatic access).

# Flat discount — stacking

## Purpose

How a Flat discount interacts with other discounts and rules on the same cart: the `code_apply` default-off stacking block per target, the `apply_regular_price` comparison, which no-code `order_over` discount wins when several qualify, and the order against Quantity tiers and Cart Rules.

Tickets that land here: *"my Flat code does nothing on a cart that already has a Fixed-discount item"*, *"my Flat-over-100 + Percent-over-100 are both active — which wins"*, *"my Flat code applied but only to some lines"*.

## Where to find it

The two stacking toggles live in the **Generate a discount code** block on the create / edit form (code variant) — see [[flat-discount-form-entry]]. They appear only on **code-based** Flat discounts.

## What the merchant can do here

- Enable **`code_apply`** to let a code-based Flat discount stack on cart lines that already carry a per-product discount (see Settings below).
- Enable **`apply_regular_price`** (needs `code_apply = 1`) so the code is worked out on the regular price and compared with the current discounted price (see below).

### What the merchant CANNOT do here

- Stack a code-based Flat on a discounted cart line WITHOUT `code_apply = 1`.
- Stack several no-code `order_over` discounts — only the highest threshold the subtotal passes applies, whatever it saves.

## Settings & fields

| Field | Backend key | What it does | Validation |
|-------|-------------|--------------|------------|
| **The discount is applied even when the cart contains discounted products** | `code_apply` | Allows stacking on already-discounted lines. | 1 / 0. Defaults OFF. |
| **Apply to the regular price of products, if this discount is greater** | `apply_regular_price` | When ON, the code is worked out on the regular price and replaces the product discount if that price is lower; otherwise the line keeps the product discount and no code. | 1 / 0. Only shown when `code_apply = 1`. |

## Business rules

### Default-off stacking — what `code_apply = 0` does (code-based Flat)

With the default `code_apply = 0`, a code-based Flat discount does not stack on a line that already holds a product discount ([[marketing-discounts-fixed|Fixed]], no-code Flat or Percent on products, Quantity tier). No-code `order_over` discounts do not count as "already discounted". The exact behaviour depends on the target:

- **Target `order_over`** — refused at entry when ANY line holds a product discount, with *"This discount code can not be applied because you already have a discounted products at your cart"*. A code already in the cart is removed without a message if such a product is added later.
- **Target `all` / `product` / `product_category` / `product_vendor` / `selection` / `category_vendor`** — accepted; lines with a product discount are skipped. If all are discounted, nothing comes off and no message shows. On a specific target the full amount still comes off: the first line that took the code absorbs the skipped lines' share, so it can go below zero. With matching lines of 60 EUR (discounted) and 40 EUR and 20 EUR off, the 40 EUR line takes all 20 EUR.

To stack on a previously-discounted cart, enable **`code_apply = 1`**; `apply_regular_price` then decides the price basis (below).

**No-code Flat discounts** have no such switch. A no-code `order_over` applies on the subtotal after product discounts. A no-code Flat on `all` or a specific target is itself a product discount (see the end of *Several no-code `order_over` discounts* below).

### Apply-regular-price comparison

When `code_apply = 1` AND `apply_regular_price = 1` on a code-based Flat, the code is worked out on the line's **regular price** and compared with the current discounted price. If the code's price is lower, it replaces the product discount; otherwise the line keeps the product discount and no code. Never both.

### Several no-code `order_over` discounts — highest threshold wins

When several no-code `order_over` discounts qualify, flat or percent, **they do NOT stack — only the one with the highest threshold the subtotal passes applies, whatever it saves**. If that one cannot apply (a flat larger than the subtotal), none does. Examples on a 150 EUR cart:

- "10 EUR off over 50 EUR" vs "20% off over 100 EUR" → **the 20% wins** (threshold 100).
- "50 EUR off over 50 EUR" vs "5% off over 100 EUR" → **the 5% wins** (threshold 100), saving 7.50 EUR.
- Equal thresholds → undefined which wins; merchants should avoid them.

**Other combinations DO stack** — they live in independent slots in the discount engine:

- Global Flat (`order_over`) + a **Code-based** Percent → both apply (different slots).
- Global Flat (`order_over`) + a per-product **Fixed** → both apply (Fixed is per-line, before the cart-level engine).
- Global Flat (`order_over`) + a [[marketing-discounts-quantity|Quantity tier]], a [[marketing-discounts-countdown|Countdown]], or a [[marketing-discounts-shipping|Free-shipping]] discount → both apply.

For code-based stacking, the `code_apply` toggle on the code-based discount still gates whether it accepts a cart that already has a discounted line (see *Default-off stacking* above).

Product-level discounts on one line never add up. Among Fixed and no-code Flat or Percent on `all` or a specific target, the lowest final price wins; a Quantity tier is used instead of them.

### Quantity-tier interaction — separate slots

When a Flat code with `code_apply = 1` lands on a line that also qualifies for a [[marketing-discounts-quantity|Quantity tier]], the two apply in **separate slots**: the tier acts on the line FIRST, then the Flat allocation acts on the already-discounted subtotal. There is no "subtract tier save" step at the Flat stage. Both show inside the product line's price, with no separate row in the totals; total saving = tier saving + Flat saving (Flat computed against the post-tier subtotal). On per-product targets the Flat code still respects `code_apply` — without `code_apply = 1`, tier-discounted lines are skipped.

### Cart Rules vs Flat discount ordering

[[apps-cart-rules|Cart Rule]] conditions see the total after product discounts and line-level codes, before order-level discounts. So a Flat on `all` or a specific target can drop the cart below a rule's threshold; a Flat on `order_over` cannot. A product-level Cart Rule's reduction is already in the subtotal that `order_over` is checked against, so it can push the cart below that threshold.

### Stacking matrix — quick summary

| Cart state | No-code Global Flat | Code-based Flat |
|---|---|---|
| No per-product discounts | applies | applies (subject to eligibility) |
| Has per-product discount + `code_apply = 0` | `order_over` applies; on `all` or a specific target the lowest final price wins | **refused with a message** on `order_over`; **skips** already-discounted lines on `all` and specific targets |
| Has per-product discount + `code_apply = 1` | `order_over` applies; on `all` or a specific target the lowest final price wins | applies; `apply_regular_price` governs the basis |
| Has a Quantity tier | `order_over`: both apply. On `all` or a specific target: the tier is used instead | `code_apply = 1`: both apply in separate slots; `code_apply = 0`: Flat skips tier lines |
| Several no-code `order_over` | highest threshold the subtotal passes wins | n/a (codes live in a different pool) |

## Related

- [[marketing-discounts-flat]] — hub.
- [[flat-discount-targeting]] — `code_apply = 0` SKIP rule references the target enum here.
- [[flat-discount-value-mechanics]] — Flat code matched-subtotal-≥-amount rule (different reject path).
- [[flat-discount-eligibility]] — eligibility gates that run BEFORE `code_apply`.
- [[marketing-discounts-percent]] — sister type; shares the no-code `order_over` pool.
- [[marketing-discounts-fixed]] — per-product Fixed; lives in a separate engine slot.
- [[marketing-discounts-quantity]] — Quantity tiers in a separate slot.
- [[marketing-discounts-countdown]] — Countdown stacks with Flat.
- [[marketing-discounts-shipping]] — Free-shipping stacks with Flat.
- [[apps-cart-rules]] — conditions see the total after product discounts and line-level codes.
- [[discount-stacking]] — cross-discount stacking matrix for all discount types.

## Open questions

None.
