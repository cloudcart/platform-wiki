---
type: concept
nav_path: "Concept → Discount stacking → code_apply toggle"
aliases: ["code_apply", "The discount is applied even when the cart contains discounted products", "apply_regular_price", "Apply to the regular price of products", "Code refused when cart has discounted products", "Stacking toggle"]
tags: [marketing, discounts, stacking, code_apply, concepts]
plan_gates: []
created: 2026-06-10
updated: 2026-11-04
source_count: 3
---

> Part of [[discount-stacking]]. See the hub for the other aspects (evaluation order, cart code slots, uses counter, plan gating, Cart Rules interaction, per-variant rows).

# Discount stacking — code_apply toggle

## Definition

Every code-based [[discount|Discount]] carries a **`code_apply`** flag that decides what happens to cart lines that already hold a product discount. Only product-level discounts count as "already discounted": an order-level discount such as a no-code Orders over, Countdown or a payment-method discount neither blocks a code nor is blocked by it. No-code discounts have no such switch.

**`code_apply = 1`** — label *"The discount is applied even when the cart contains discounted products."* The code also applies to lines holding a product discount, on the reduced amount.

**`code_apply = 0`** (default):

| Code | Result |
|------|--------|
| Orders over, or free shipping with a threshold | Refused at entry if any line holds a product discount, with *"This discount code can not be applied because you already have a discounted products at your cart"*. A flat Orders-over code already in the cart is removed without a message if a discounted product is added later; free shipping is not rechecked. |
| Free shipping for all, and Code PRO | Refused at entry with *"Invalid discount code"*. |
| Every product or a specific target | Accepted; lines with a product discount are skipped. If all are discounted, nothing comes off and no message shows. |
| Container | Never refused for this. Its default is on, and its form has no such switch. |

The toggle is editable per-discount on the discount-edit screen. The merchant flips it to `1` for, say, a 10%-off newsletter code that should also reach products with a permanent Fixed discount.

When `code_apply = 1`, a second toggle becomes available: **`apply_regular_price`** (*"Apply to the regular price of products, if this discount is greater"*).

- **`apply_regular_price = 0`** (default) — the code applies to the line's reduced price. On a line already 20% off, a 10% code takes 10% off the discounted price.
- **`apply_regular_price = 1`** — the code is worked out on the regular price and compared with the current discounted price. If the code's price is lower, it replaces the product discount; otherwise the line keeps the product discount and no code. Never both.

## Scope

Covered:

- The `code_apply` 0 / 1 toggle and what it does to each kind of code.
- The `apply_regular_price` modifier (available when `code_apply = 1`).
- The comparison `apply_regular_price = 1` makes.
- Free-shipping codes vs no-code free shipping.

Not covered here:

- The implicit evaluation order across multiple discount types — see [[discount-stacking-evaluation-order]].
- The cart-level mutual exclusivity between stand-alone and Container codes — see [[discount-stacking-cart-code-slots]].
- How Cart Rules fit in — see [[discount-stacking-cart-rules-interaction]].
- What the amount comes off for each target — see [[discount-stacking-amount-by-target]].

## Contrasts

- **`code_apply` vs. cumulation** — on a line, `code_apply = 1` does compound: the code comes off the amount the product discount already reduced. It does not change how order-level discounts are calculated; those share one subtotal.
- **`code_apply` vs. `apply_regular_price`** — `code_apply` decides whether a code reaches lines with a product discount. `apply_regular_price` only matters once it does, and changes the **base** the code computes against.
- **`apply_regular_price` is a comparison, not an override** — the code replaces the product discount only on lines where it gives a lower price. Other lines keep the product discount and no code.
- **Free-shipping code vs no-code free shipping** — a free-shipping code follows `code_apply` at entry, for both targets. A no-code free-shipping discount has no switch and ignores other discounts.

## Where it applies

- **Storefront checkout** — when the customer types a code, the engine reads the discount's `code_apply` flag and refuses the code, or accepts it and skips or reduces lines as above.
- **Admin "apply discount to order"** on [[orders-discount-add]] — runs no `code_apply` check. The only refusal is an order that already has an order-level discount.
- **JSON-API v2** — discounts POSTed through [[api-discounts]] with `code_apply = 0` behave exactly as admin-created ones; the rule is enforced at the **checkout engine layer**, not at the API write layer.
- **Container codes** — never refused for `code_apply`. See [[discount-stacking-cart-code-slots]].

### Storefront UI implications

When a code is refused, the customer sees the message above and the code is not attached; the product discount stays. The customer must remove the discounted product or use a different code.

A code on every product or a specific target shows inside each product line with the code in brackets and adds no totals row. An Orders-over code is a row in the totals. The customer never sees which `code_apply` flag is set.

## Related

- [[discount-stacking]] — hub.
- [[discount-stacking-evaluation-order]] — the fixed chain that decides what is worked out first.
- [[discount-stacking-cart-code-slots]] — stand-alone and Container codes in the cart.
- [[discount-stacking-cart-rules-interaction]] — Cart Rules run after line-level codes.
- [[discount]] — entity carrying `code_apply`, `apply_regular_price`.
- [[marketing-discounts]] — primary CRUD screen where the toggles live.
- [[marketing-discounts-shipping]] — free-shipping discounts and codes.
- [[marketing-discounts-fixed]] — per-product Fixed discounts; a typical product discount on a line.
- [[orders-discount-add]] — admin "apply discount to order"; no `code_apply` check.
- [[api-discounts]] — JSON-API v2 endpoint; same enforcement at the checkout engine layer.

## Open Questions

None.
