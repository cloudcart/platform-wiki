---
type: feature
nav_path: "Marketing → Discounts → Flat → Stacking"
route_name: discounts-create
route_path: /admin/marketing-new/discounts/create/code
aliases: ["Flat discount stacking", "code_apply flat", "apply_regular_price flat", "Flat percent winner-takes-all", "Flat plus quantity tier", "Flat plus cart rules", "Flat 10000 combinations cap", "Flat silent rejection"]
tags: [marketing, discounts, flat, stacking, code_apply, apply_regular_price]
plan_gates: ["discount_global", "discount_coupon"]
created: 2026-06-10
updated: 2026-06-11
source_count: 4
---

> Part of [[marketing-discounts-flat]]. See the hub for the other aspects (form entry, targeting, value mechanics, eligibility, programmatic access).

# Flat discount — stacking

## Purpose

How a Flat discount interacts with other discounts and rules on the same cart: the `code_apply` default-off stacking block (with per-target silent-rejection variants), the `apply_regular_price` re-evaluation rule, the winner-takes-all behaviour when a Global Flat and Global Percent both qualify on `order_over`, slot ordering against Quantity tiers and Cart Rules, and the 10,000 max-combinations cap.

Tickets that land here: *"my Flat code does nothing on a cart that already has a Fixed-discount item"*, *"my Flat-over-100 + Percent-over-100 are both active — which wins"*, *"my Flat code applied but only to some lines"*.

## Where to find it

The two stacking toggles live in the **Generate a discount code** block on the create / edit form (code variant) — see [[flat-discount-form-entry]]. They appear only on **code-based** Flat discounts.

## What the merchant can do here

- Enable **`code_apply`** to let a code-based Flat discount stack on cart lines that already carry a per-product discount (see Settings below).
- Enable **`apply_regular_price`** (needs `code_apply = 1`) so the Flat allocation is compared against the catalog price as well as the post-Fixed-discount price, picking whichever gives the larger customer saving.

### What the merchant CANNOT do here

- Stack a code-based Flat on a discounted cart line WITHOUT `code_apply = 1`.
- Stack a no-code Global Flat + Global Percent on `order_over` — the engine picks one winner (largest absolute saving).
- Target more than **10,000 combinations** (products × categories × customer_groups × selections).

## Settings & fields

| Field | Backend key | What it does | Validation |
|-------|-------------|--------------|------------|
| **Apply discount even if the cart contains products with a discount** | `code_apply` | Allows stacking on already-discounted lines. | 1 / 0. Defaults OFF. |
| **Apply to the regular price of products, if this discount is greater** | `apply_regular_price` | When ON, re-evaluates against the catalog price (ignoring per-product Fixed discounts) if that yields a bigger discount. | 1 / 0. Only shown when `code_apply = 1`. |

## Business rules

### Default-off stacking — what `code_apply = 0` does (code-based Flat)

With the default `code_apply = 0`, a code-based Flat discount will not stack on a cart that already has a discounted line. The exact behaviour depends on the target:

- **Target `order_over`** — the code is **silently rejected at checkout** when ANY line already has a discount (per-product [[marketing-discounts-fixed|Fixed]], Quantity tier, an active Percent code, etc.). The cart total does not change and **no** "already discounted" error is shown to the customer.
- **Target `product` / `product_category` / `product_vendor` / `selection` / `category_vendor`** — the code passes validation, then the per-line application phase silently **SKIPS** any already-discounted line. Merchant-visible outcome: the code "applies" but only to lines that had no prior discount.

To force-stack on a previously-discounted cart, enable **`code_apply = 1`**. The engine checks this flag before applying: `code_apply = 0` + an existing discount → rejected/skipped as above; `code_apply = 1` → applied, with `apply_regular_price` then governing the price basis (below).

For **no-code (cart-wide) Flat discounts**, `code_apply` is irrelevant — the discount always applies regardless of existing per-product discounts, subtracting based on the line subtotal.

### Apply-regular-price re-evaluation

When `code_apply = 1` AND `apply_regular_price = 1` on a code-based Flat, the engine compares the Flat share against the line's **discounted** price (post-Fixed-discount) and against the line's **catalog (regular)** price, applying whichever gives the **larger customer saving**. This guarantees the customer gets the better of the catalog-price code and an already-running per-product discount.

### Flat + Percent at the cart level — winner-takes-all on `order_over`

When a Global Flat (`order_over`) AND a Global Percent (`order_over`) both qualify, **they do NOT stack — only the one with the larger absolute saving wins**. The engine pools all `order_over` Flat + Percent matches and picks the highest saving. Examples on a 150 EUR cart:

- "10 EUR off over 50 EUR" (saves 10) vs "20% off over 100 EUR" (saves 30) → **the 20% wins** (30 > 10).
- "30 EUR off over 100 EUR" (saves 30) vs "20% off over 50 EUR" (saves 30) → **tie-break by the first record returned from the database** — undefined which wins; merchants should avoid equally-valued overlapping rules.

**Other combinations DO stack** — they live in independent slots in the discount engine:

- Global Flat (`order_over`) + a **Code-based** Percent → both apply (different slots).
- Global Flat (`order_over`) + a per-product **Fixed** → both apply (Fixed is per-line, before the cart-level engine).
- Global Flat (`order_over`) + a [[marketing-discounts-quantity|Quantity tier]], a [[marketing-discounts-countdown|Countdown]], or a [[marketing-discounts-shipping|Free-shipping]] discount → both apply.

For code-based stacking, the `code_apply` toggle on the code-based discount still gates whether it accepts a cart that already has a discounted line (see *Default-off stacking* above).

### Quantity-tier interaction — separate slots

When a Flat code with `code_apply = 1` lands on a line that also qualifies for a [[marketing-discounts-quantity|Quantity tier]], the two apply in **separate slots**: the tier acts on the line FIRST, then the Flat allocation acts on the already-discounted subtotal. There is no "subtract tier save" step at the Flat stage. The customer sees both as separate negative lines; total saving = tier saving + Flat saving (Flat computed against the post-tier subtotal). On per-product targets the Flat code still respects `code_apply` — without `code_apply = 1`, tier-discounted lines are silently skipped.

### Cart Rules vs Flat discount ordering

When [[apps-cart-rules|Cart Rules]] coexist with a Flat discount, Discounts apply **first**, then Cart Rules — the Cart Rule's trigger evaluates against the cart total AFTER the Flat discount has subtracted. So a Flat discount that drops the cart below a subtotal-threshold trigger will prevent that Cart Rule from firing. Account for this ordering when designing multi-layer promotions.

### Maximum combinations cap (10,000)

Same as Percent: when targeting the **intersection of products × categories × customer_groups × selections**, the cap is **10,000**. A create / update that would exceed it is rejected with a validation error, and the merchant must narrow one of the array dimensions.

### Stacking matrix — quick summary

| Cart state | No-code Global Flat | Code-based Flat |
|---|---|---|
| No per-product discounts | applies | applies (subject to eligibility) |
| Has per-product discount + `code_apply = 0` | applies (no check) | **rejected** on `order_over`; **silently skips** already-discounted lines on per-product targets |
| Has per-product discount + `code_apply = 1` | applies | applies; `apply_regular_price` governs the basis |
| Has a Quantity tier | both apply (Tier first, then Flat) | `code_apply = 1`: both apply in separate slots; `code_apply = 0`: Flat silently skips tier lines |
| Both Global Flat + Global Percent on `order_over` | winner-takes-all (larger saving wins) | n/a (codes live in a different pool) |

## Related

- [[marketing-discounts-flat]] — hub.
- [[flat-discount-targeting]] — `code_apply = 0` SKIP rule references the target enum here.
- [[flat-discount-value-mechanics]] — Flat code matched-subtotal-≥-amount rule (different reject path).
- [[flat-discount-eligibility]] — eligibility gates that run BEFORE `code_apply`.
- [[marketing-discounts-percent]] — sister type; winner-takes-all is between Flat and Percent on `order_over`.
- [[marketing-discounts-fixed]] — per-product Fixed; lives in a separate engine slot.
- [[marketing-discounts-quantity]] — Quantity tiers in a separate slot.
- [[marketing-discounts-countdown]] — Countdown stacks with Flat.
- [[marketing-discounts-shipping]] — Free-shipping stacks with Flat.
- [[apps-cart-rules]] — evaluated AFTER Flat discounts.
- [[discount-stacking]] — cross-discount stacking matrix for all discount types.

## Open questions

None.
