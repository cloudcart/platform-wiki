---
type: entity
nav_path: "Entity → Discount → Stacking and evaluation"
aliases: ["Discount stacking", "Code stacking", "Discount evaluation order", "Discount vs Cart Rule"]
tags: [marketing, discounts, entity, stacking, evaluation]
created: 2026-06-10
updated: 2026-06-10
source_count: 6
---

# Discount — Stacking and evaluation

> Part of [[discount]]. See the hub for related aspects (fields, lifecycle, business rules, webhooks/API).

## Identity

How the platform decides whether multiple discounts can coexist on the same cart line, and the order in which Discounts and [[apps-cart-rules|Cart Rules]] are evaluated at checkout. This is the **most-asked merchant-facing rule** about discounts.

## Aliases

- "Stacking" — refers to whether a code applies on top of an existing per-product discount.
- "Evaluation order" — refers to Discounts → Cart Rules ordering.

## Key Attributes

### Default: stacking is OFF (`code_apply = 0`)

By default, a promo code is **REJECTED** at checkout if any cart line already has a discount applied (e.g., a Fixed discount on one of the products). The customer sees a validation error and the code is not attached to the cart.

### Enabling stacking — "Apply discount even if the cart contains products with a discount"

When the merchant toggles this option in the discount editor to ON (`code_apply = 1`):

- The code applies on top of existing per-product discounts.
- The code's amount stacks additively with whatever per-product discount already lives on the line.
- If `apply_regular_price = 1` is ALSO set, the code re-evaluates against the ORIGINAL catalog price (ignoring per-product discounts) if that would yield a larger discount — see below.

See [[discount-stacking]] and [[discount-stacking-code-apply]] for the full concept walkthrough.

### `apply_regular_price` is a max-of-two-discounts filter (not always wins)

When `apply_regular_price = 1` is set on a code-based discount and the cart contains items with per-product discounts, the code applies the **larger of**:

1. The discount value against the **catalog (regular) price**.
2. The existing per-product discount that's already attached.

The runtime filter iterates each matching item, computes the would-be discount amount against the regular price (or via proportional split for `flat` types: `add = code_value / cart_subtotal; line_amount = line_total * add`), and **skips the item** if the resulting amount would be less than the existing per-product discount.

So `apply_regular_price = 1` does NOT blindly override — it only swaps in the code's discount when doing so would help the customer more.

### Order-of-evaluation: Discounts before Cart Rules

When both Discounts and [[apps-cart-rules|Cart Rules]] coexist, the checkout pipeline applies **Discounts first, then Cart Rules**. A "Cart total > 100 BGN" Cart Rule trigger sees the POST-discount cart total, not the pre-discount one.

See [[discount-stacking-evaluation-order]] for the full ordering matrix, including how two competing same-type Discounts that target `order_over` are resolved (`total_value` DESC — largest absolute saving wins, NOT the highest threshold).

### Mutual exclusion: stand-alone code XOR Container codes (per cart)

The cart cannot mix a stand-alone Promo / Code PRO code with Container codes. Entering one clears the other (see [[discount-entity-business-rules]] for the `discount_code` / `discount_container_code` column split). So the customer can:

- Stack many Container codes against a single Container parent (up to the parent's `total_value` cap).
- NOT mix a stand-alone code with Container codes.
- NOT stack two stand-alone codes.

### Stacking with quantity / countdown / global discounts

- **Quantity discount + code** — the code stacks if `code_apply = 1`; the quantity tier applies first, then the code on top.
- **Countdown discount + code** — same as quantity.
- **Global discount + code** — global discounts attach automatically; whether the code can apply on top depends on `code_apply` like every other case.

## Where it appears

- [[marketing-discounts]] — the "Apply discount even if the cart contains products with a discount" toggle in the per-discount editor.
- [[checkout-flow]] — the storefront flow that performs stacking evaluation.
- [[orders-discount-add]] — admin-side add-to-existing-order respects the same stacking rules.

## Related

- [[discount]] — hub.
- [[discount-entity-fields]] — the `code_apply` and `apply_regular_price` fields.
- [[discount-entity-business-rules]] — the cart `discount_code` / `discount_container_code` column split.
- [[discount-stacking]] — concept-level overview of stacking semantics.
- [[discount-stacking-code-apply]] — deep dive on the `code_apply` flag.
- [[discount-stacking-evaluation-order]] — Discounts → Cart Rules ordering and same-type tie-breaking.
- [[apps-cart-rules]] — companion engine that evaluates AFTER Discounts.
- [[cart]] — where the stacking columns live.

## Open Questions

None — all previously-flagged stacking items resolved (see hub Open Questions).
