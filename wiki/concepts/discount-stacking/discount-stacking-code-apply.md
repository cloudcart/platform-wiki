---
type: concept
nav_path: "Concept → Discount stacking → code_apply toggle"
aliases: ["code_apply", "Apply discount only to products with no other discount", "apply_regular_price", "Shipping order_over carve-out", "Stacking toggle", "Reject-on-conflict toggle"]
tags: [marketing, discounts, stacking, code_apply, concepts]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[discount-stacking]]. See the hub for the other aspects (evaluation order, cart code slots, uses counter, plan gating, Cart Rules interaction, cooldown / attachments).

# Discount stacking — code_apply toggle

## Definition

Every code-based [[discount|Discount]] carries a **`code_apply`** flag that decides what happens when the customer types the code into a cart that already has another discount applied. This is the central stacking rule on CloudCart. (verify)

| Value | Label in admin | Behaviour at checkout |
|-------|----------------|----------------------|
| **`0`** (default) | "Apply discount only to products with no other discount" | The code is **rejected** if the cart contains any line that already has a discount (e.g., a Fixed discount on one product). The customer sees: the code didn't apply; the cart total stays the same. |
| **`1`** | "Apply discount even if the cart contains products with a discount" | The code applies **on top of** existing per-product discounts. |

The toggle is editable per-discount on the discount-edit screen. The merchant flips it to `1` for, say, a 10%-off newsletter coupon that should stack with a permanent product-level Fixed discount.

When `code_apply = 1`, a second toggle becomes available: **`apply_regular_price`**.

- **`apply_regular_price = 0`** (default) — the code applies against the line's **post-discount** price. If the product already has a 20% Fixed discount, the 10% coupon stacks on the discounted price.
- **`apply_regular_price = 1`** — the code re-evaluates against the **original catalog price** (ignoring the per-product Fixed discount) — whichever yields the larger discount wins. This is how merchants offer "10% off any product OR the existing sale, whichever is bigger".

## Scope

Covered:

- The `code_apply` 0 / 1 toggle and its merchant-facing labels.
- The `apply_regular_price` modifier (only meaningful when stacking is allowed).
- The max-of-two comparison semantics of `apply_regular_price = 1`.
- The shipping-coupon `order_over` carve-out that bypasses `code_apply = 0`.

Not covered here:

- The implicit evaluation order across multiple discount types — see [[discount-stacking-evaluation-order]].
- The cart-level mutual exclusivity between stand-alone and Container codes — see [[discount-stacking-cart-code-slots]].
- How Cart Rules sit on top of all of this — see [[discount-stacking-cart-rules-interaction]].

## Contrasts

- **`code_apply` vs. cumulation** — `code_apply = 1` does **not** mean "10% then 5% off the result". Each discount still computes against its own base; `code_apply` just decides whether a code is allowed to attach when other discounts exist.
- **`code_apply` vs. `apply_regular_price`** — `code_apply` is the gate (allow / reject when other discounts present). `apply_regular_price` only matters once the gate is open and changes the **base** the code computes against.
- **`apply_regular_price` is max-of-two, not blind override** — when `apply_regular_price = 1` and the matching line has a per-product discount, the runtime computes the code's discount against the **catalog price** and compares it to the existing per-product discount amount. Whichever yields the larger discount wins for that item. If the existing per-product discount is larger or equal, the item is skipped. (verify) For `flat`-type codes the comparison uses a proportional split: `line_amount = line_total × (code_value / cart_subtotal)`.
- **Shipping `order_over` always applies — the carve-out** — a shipping discount with `settings = order_over` (free shipping over X) **always applies** when the cart total reaches the threshold, regardless of `code_apply`. The rationale: free-shipping promos are order-level perks the merchant wants honoured. A shipping discount with `settings = all` (free shipping on every order) follows the standard `code_apply` rule. (verify)

The shipping-coupon `order_over` carve-out is the most common merchant pitfall — a merchant who sets `code_apply = 0` on a shipping coupon and expects rejection with other discounts present will see it apply anyway when the cart matches `order_over`.

## Where it applies

- **Storefront checkout** — when the customer types a code, the engine reads the discount's `code_apply` flag and either accepts, rejects, or stacks.
- **Admin "apply discount to order"** on [[orders-discount-add]] — the same `code_apply` check runs server-side; the admin cannot bypass it by attaching from the back-office.
- **JSON-API v2** — discounts POSTed through [[api-discounts]] with `code_apply = 0` behave exactly as admin-created ones; the rule is enforced at the **checkout engine layer**, not at the API write layer.
- **Container codes** — when a child code is redeemed, the platform evaluates the **parent's** `code_apply` for the reject-on-conflict check, not the child's. See [[discount-stacking-cart-code-slots]] for the parent / child relationship.

### Storefront UI implications

When stacking is rejected (`code_apply = 0` + cart has discount), the storefront customer sees code-entry feedback: the code is "invalid for this cart" — no auto-detachment of the pre-existing discount. The customer must remove the discounted product or use a different code.

When stacking applies, the cart shows both discounts as separate line items in the cart totals — line-discount + order-level discount = total discount. The customer never sees which `code_apply` flag is set.

## Related

- [[discount-stacking]] — hub.
- [[discount-stacking-evaluation-order]] — the implicit priority chain that decides which discount evaluates first.
- [[discount-stacking-cart-code-slots]] — Container parent `code_apply` rules child redemption.
- [[discount-stacking-cart-rules-interaction]] — Cart Rules run after `code_apply` resolves.
- [[discount]] — entity carrying `code_apply`, `apply_regular_price`.
- [[marketing-discounts]] — primary CRUD screen where the toggles live.
- [[marketing-discounts-shipping]] — `order_over` shipping discount, where the carve-out applies.
- [[marketing-discounts-fixed]] — per-product Fixed discounts; the typical "existing discount" that `code_apply = 0` rejects against.
- [[orders-discount-add]] — admin "apply discount to order"; runs the same `code_apply` check.
- [[api-discounts]] — JSON-API v2 endpoint; same enforcement at the checkout engine layer.

## Open Questions

None.
