---
type: concept
nav_path: "Concept → Storefront known issues → Cart discount codes"
aliases: ["Storefront discount code issues", "Code stacking issues", "Container vs promo code", "Discount code conflicts"]
tags: [storefront, cart, discounts, codes, issues]
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

> Part of [[storefront-known-issues]]. See the hub for the other aspects (framework, inventory, cart lifecycle, listing / search, display + customer, pending bugs).

# Storefront issues — discount codes in the cart

## Definition

The discount-code entries in the storefront-issues catalogue cover behaviours that surface when **two codes interact** on the same cart — a container code already applied and the customer types a promo code, or two promo codes against the same cart, or a free-shipping coupon overlapping with a percentage-off promo. Every entry below is **By design** and ultimately governed by [[discount-stacking]]; the symptoms look like silent bugs because the cart UI typically does not surface the conflict-resolution rule in a tooltip — it just applies the latest valid code and clears the prior slot.

Three catalogue entries are in this group: container-code vs promo-code mutual exclusion at the cart level, default single-code-only behaviour, and the free-shipping / `order_over` carve-outs that bypass the single-code rule.

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
- **Single code default vs stacking** — every code-based discount carries a `code_apply` flag. Default is `0` (don't allow stacking) — when one discount is already attached and a new code is typed, the new code is rejected. Flipping `code_apply = 1` per-discount makes that specific discount stackable with whatever code came first. See [[discount-stacking]].
- **Shipping / `order_over` carve-outs** — discounts of `type = shipping` and `order_over` discounts have a hard-coded carve-out that bypasses `code_apply` — they always apply on top regardless of what other code is already attached. The merchant cannot disable this carve-out. To the customer it looks like *"the free-shipping coupon worked but I expected my other promo to be removed"*.

## Where it applies

The three catalogue entries:

| # | Behaviour | Affected page(s) | Category | What to tell the merchant |
|---|---|---|---|---|
| 7 | Typing a promo code wipes previously-entered container codes (or vice versa) with no error message | Cart, checkout | By design | The cart's `discount_code` and `discount_container_code` slots are mutually exclusive at the cart level — setting one silently clears the other. See [[discount-stacking]]. The merchant should communicate this to customers in the campaign description. |
| 8 | A second promo code is rejected when one is already applied (no stacking) | Cart, checkout | By design | Default `code_apply = 0` on every code-based discount means new codes are rejected when a discount is already attached. The merchant flips `code_apply = 1` per-discount to allow stacking. See [[discount-stacking]]. |
| 9 | Free-shipping coupon applies even when a non-stacking promo is already on the cart | Cart, checkout | By design | Shipping discounts (`type = shipping`) and `order_over` discounts have a carve-out — they always apply regardless of `code_apply`. See [[discount-stacking]]. |

### Support-agent quick path

All three are **By design**. When a merchant reports *"discount codes are deleting each other"*, the agent's response is:

1. Confirm which entry applies — was the prior code a container code (entry 7) or a promo code (entry 8)? Was the conflicting code a shipping / `order_over` discount (entry 9)?
2. Surface the rule from [[discount-stacking]].
3. If the merchant wants stacking, point them at the per-discount `code_apply` flag in `marketing-discounts-codes` (when applicable).
4. If the merchant wants to keep customers from getting confused, recommend they spell out the policy in the campaign description — the cart UI does not auto-surface the conflict.

### Why this is **By design** and not a bug

The mutual-exclusion + single-code-default rules predate the modern cart. Changing them retroactively would either break long-running campaigns or silently inflate discounts on every store. The platform's position is documented in [[discount-stacking]]: opt-in stacking via `code_apply = 1` is the supported model.

## Related

- [[storefront-known-issues]] — hub.
- [[storefront-issue-framework]] — the four categories.
- [[discount-stacking]] — concept page that governs all three entries.
- [[marketing-discounts]] — discount editor admin feature.
- [[settings-cart]] — cart-level configuration.

## Open Questions

- Should the cart UI surface a non-blocking notice when entry 7 fires ("your previous code was replaced")? — currently silent; merchants ask for this regularly. The behaviour itself is By design but the lack of a UI signal is a candidate UX improvement.
- Are there themes that DO show a tooltip on entry 8? (verify per theme.)
