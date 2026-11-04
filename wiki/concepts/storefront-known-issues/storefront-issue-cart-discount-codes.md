---
type: concept
nav_path: "Concept → Storefront known issues → Cart discount codes"
aliases: ["Storefront discount code issues", "Code stacking issues", "Container vs promo code", "Discount code conflicts"]
tags: [storefront, cart, discounts, codes, issues]
created: 2026-06-10
updated: 2026-11-04
source_count: 2
---

> Part of [[storefront-known-issues]]. See the hub for the other aspects (framework, inventory, cart lifecycle, listing / search, display + customer, pending bugs).

# Storefront issues — discount codes in the cart

## Definition

The discount-code entries in the storefront-issues catalogue cover behaviours that surface when **two codes interact** on the same cart — a container code already applied and the customer types a promo code, or two promo codes against the same cart, or a code with a threshold or free shipping on a cart that holds discounted products. Every entry below is **By design** and ultimately governed by [[discount-stacking]]; the symptoms look like errors because the cart UI typically does not surface the conflict-resolution rule in a tooltip — it just applies the latest valid code and clears the prior slot.

Three catalogue entries are in this group: container-code vs promo-code mutual exclusion at the cart level, the single promo-code slot, and the refusal of threshold and free-shipping codes on carts holding discounted products.

## Scope

Covered:

- The three discount-code interaction entries that have generated support tickets.
- Cross-reference to [[discount-stacking]] for the full conflict-resolution model.

Not covered:

- Per-product discount math, percentage vs flat amount mechanics — see the `marketing-discounts-*` feature pages.
- The campaign-builder admin UI — see [[marketing-discounts]] / `marketing-discounts-codes`.
- Discount code generation / distribution flows — see the loyalty + refund-credit apps.

## Contrasts

- **Container code vs promo code mutual exclusion** — these two cart slots (`discount_code` and `discount_container_code`) hold different kinds of code (container codes are issued by loyalty / refund-store-credit flows; promo codes are marketing campaign codes). The cart cannot hold both — entering one silently clears the other, with no error message. To the customer it looks like *"my container code disappeared when I typed the promo"*. The agent's response: this is intentional; the merchant should communicate the policy to customers in the campaign description.
- **One promo code at a time** — the cart holds one promo code, so a new code replaces the previous one. `code_apply` has nothing to do with other codes; it decides how a code treats lines that already hold a product discount. See [[discount-stacking]].
- **Threshold and free-shipping codes with `code_apply` off** — a code with Orders over, or free shipping with a threshold, is refused when any line holds a product discount, with *"This discount code can not be applied because you already have a discounted products at your cart"*. A free-shipping code for all orders and a Code PRO code are refused with *"Invalid discount code"*. A code for all products or a specific target is accepted, and lines holding a product discount are skipped. Discounts without a code have no such switch.

## Where it applies

The three catalogue entries:

| # | Behaviour | Affected page(s) | Category | What to tell the merchant |
|---|---|---|---|---|
| 7 | Typing a promo code wipes previously-entered container codes (or vice versa) with no error message | Cart, checkout | By design | The cart's `discount_code` and `discount_container_code` slots are mutually exclusive at the cart level — setting one silently clears the other. See [[discount-stacking]]. The merchant should communicate this to customers in the campaign description. |
| 8 | A second promo code replaces the one already applied | Cart, checkout | By design | The cart holds one promo code, so a new code replaces it with no message. `code_apply` does not concern other codes. See [[discount-stacking]]. |
| 9 | A threshold or free-shipping code is refused on a cart holding discounted products | Cart, checkout | By design | With `code_apply` off, the code is refused while any line holds a product discount. Turning `code_apply` on for that discount allows it. See [[discount-stacking]]. |

### Support-agent quick path

All three are **By design**. When a merchant reports *"discount codes are deleting each other"*, the agent's response is:

1. Confirm which entry applies — was the prior code a container code (entry 7) or a promo code (entry 8)? Was the refused code one with a threshold or free shipping, on a cart holding discounted products (entry 9)?
2. Surface the rule from [[discount-stacking]].
3. If the merchant wants a code to work on lines holding a product discount, point them at the per-discount `code_apply` flag on the discount's form. A cart cannot hold two promo codes.
4. If the merchant wants to keep customers from getting confused, recommend they spell out the policy in the campaign description — the cart UI does not auto-surface the conflict.

### Why this is **By design**

The platform's rules are documented in [[discount-stacking]]. `code_apply` decides whether a code works on lines holding a product discount; the cart holds one promo code or a set of Container codes, not both.

## Related

- [[storefront-known-issues]] — hub.
- [[storefront-issue-framework]] — the four categories.
- [[discount-stacking]] — concept page that governs all three entries.
- [[marketing-discounts]] — discount editor admin feature.
- [[settings-cart]] — cart-level configuration.

## Open Questions

- Should the cart UI surface a non-blocking notice when entry 7 fires ("your previous code was replaced")? — currently silent; merchants ask for this regularly. The behaviour itself is By design but the lack of a UI signal is a candidate UX improvement.
- Are there themes that show a notice when entry 8 fires? (verify per theme.)
