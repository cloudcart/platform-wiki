---
type: entity
nav_path: "Entity → Discount → Stacking and evaluation"
aliases: ["Discount stacking", "Code stacking", "Discount evaluation order", "Discount vs Cart Rule"]
tags: [marketing, discounts, entity, stacking, evaluation]
created: 2026-06-10
updated: 2026-11-04
source_count: 6
---

# Discount — Stacking and evaluation

> Part of [[discount]]. See the hub for related aspects (fields, lifecycle, business rules, webhooks/API).

## Identity

How the platform decides whether multiple discounts can coexist on the same cart line, and the order in which Discounts and [[apps-cart-rules|Cart Rules]] are evaluated at checkout. This is the **most-asked merchant-facing rule** about discounts.

## Aliases

- "Stacking" — refers to whether a code applies on top of an existing per-product discount.
- "Evaluation order" — refers to the sequence of product discounts, line-level codes, Cart Rules and order-level discounts.

## Key Attributes

### Default: `code_apply = 0`

Only product-level discounts count as "already discounted". By default, an Orders-over code or a free-shipping code with a threshold is **refused** at entry if any cart line holds a product discount (e.g., a Fixed discount on one of the products), with *"This discount code can not be applied because you already have a discounted products at your cart"*. Free shipping for all and Code PRO are refused with *"Invalid discount code"*. A code for every product or a specific target is **accepted** and skips those lines; if all are discounted, nothing comes off and no message shows. A Container code is never refused for this.

### `code_apply = 1` — "The discount is applied even when the cart contains discounted products."

When the merchant toggles this option in the discount editor to ON:

- The code also applies to lines holding a product discount.
- On those lines it comes off the reduced amount: a 10% code on a line already 20% off takes 10% off the discounted price.
- If `apply_regular_price = 1` is ALSO set, the comparison below decides instead.

See [[discount-stacking]] and [[discount-stacking-code-apply]] for the full concept walkthrough.

### `apply_regular_price` is a comparison (not always wins)

When `apply_regular_price = 1` is set on a code-based discount, the code is worked out on the regular price and compared with the current discounted price. If the code's price is lower, it replaces the product discount; otherwise the line keeps the product discount and no code. Never both.


### Order-of-evaluation: where Cart Rules sit

The checkout pipeline applies product discounts and line-level codes first, then [[apps-cart-rules|Cart Rules]], then order-level discounts. A "Cart total > 100 EUR" Cart Rule trigger sees the total after product discounts and line-level codes, not after an Orders-over discount, Countdown or payment-method discount.

See [[discount-stacking-evaluation-order]] for the full ordering, including how several no-code Discounts that target `order_over` are resolved: the highest threshold the subtotal passes wins, whatever it saves. Largest saving applies only among several Orders-over conditions inside one Code PRO code.

### Mutual exclusion: stand-alone code XOR Container codes (per cart)

The cart cannot mix a stand-alone Promo / Code PRO code with Container codes. Entering one clears the other (see [[discount-entity-business-rules]] for the `discount_code` / `discount_container_code` column split). So the customer can:

- Enter many Container codes (the highest Container total wins, and a code applies only if it fits what remains of that Container's value).
- NOT mix a stand-alone code with Container codes.
- NOT stack two stand-alone codes.

### What can sit on one order together

One product discount per line, one code or a set of Container codes, one no-code Orders over, Countdown, the payment-method discount, one cart-level rule, and product-level rules. Order-level kinds do not exclude each other. Product-level discounts on one line never add up.

- **Quantity tier or no-code product discount + code** — the code reaches the line only if `code_apply = 1`, and comes off the reduced amount.
- **Countdown, no-code Orders over or payment-method discount + code** — these are order-level, so they neither block a code nor are blocked by it.


## Where it appears

- [[marketing-discounts]] — the *"The discount is applied even when the cart contains discounted products."* toggle in the per-discount editor.
- [[checkout-flow]] — the storefront flow that performs stacking evaluation.
- [[orders-discount-add]] — admin-side add-to-existing-order runs no stacking switch and no customer limits.

## Related

- [[discount]] — hub.
- [[discount-entity-fields]] — the `code_apply` and `apply_regular_price` fields.
- [[discount-entity-business-rules]] — the cart `discount_code` / `discount_container_code` column split.
- [[discount-stacking]] — concept-level overview of stacking semantics.
- [[discount-stacking-code-apply]] — deep dive on the `code_apply` flag.
- [[discount-stacking-evaluation-order]] — the full ordering and the `order_over` winner.
- [[apps-cart-rules]] — companion engine, evaluated after line-level discounts and before order-level discounts.
- [[cart]] — where the stacking columns live.

## Open Questions

None.
