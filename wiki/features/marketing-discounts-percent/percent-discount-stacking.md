---
type: feature
nav_path: "Marketing → Discounts → Percent → Stacking"
route_name: discounts-create
route_path: /admin/marketing-new/discounts/create/global
aliases: ["Percent discount stacking", "code_apply", "apply_regular_price", "Percent + Flat winner-takes-all"]
tags: [marketing, discounts, percent, stacking]
plan_gates: ["discount_global", "discount_coupon"]
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

> Part of [[marketing-discounts-percent]]. See the hub for the other aspects (editor, fields, targeting, validity, plan gates, programmatic access).

# Percent discount — stacking with other discounts + Cart Rules

## Purpose

This page documents how a Percent discount combines with other discounts and Cart Rules at checkout: when the engine stacks them, when it picks a winner-takes-all, when a code is rejected on an already-discounted cart, and the `code_apply` / `apply_regular_price` interaction.

## Where to find it

Stacking behaviour runs in the storefront cart engine on every cart-totals computation. There's no admin URL for it — the merchant influences it indirectly via the `code_apply` and `apply_regular_price` toggles on a code-based Percent ([[percent-discount-editor]]), and via the broader `discounts_used_statuses` setting (see [[settings-statuses]]). The cross-type stacking ladder lives on [[discount-stacking]].

## What the merchant can do here

- Toggle `code_apply` (default OFF) on a code-based Percent to allow it on carts that already have a per-product discount.
- Toggle `apply_regular_price` (visible only when `code_apply = 1`) to make the engine pick the catalog-price-based percent if it would save the customer more.
- Plan around the Percent + Flat winner-takes-all rule on shared `order_over` no-code by avoiding equal-valued overlapping rules.
- Layer Percent with Cart Rules knowing Cart Rules evaluate AFTER the Percent reduction.

## Settings & fields

### Stacking-related fields (code-based Percent only)

| Field | Backend key | What it does |
|---|---|---|
| **Apply discount even if the cart contains products with a discount** | `code_apply` | Defaults OFF. When ON, the code is not rejected on `order_over` carts with already-discounted lines. |
| **Apply to the regular price of products, if this discount is greater** | `apply_regular_price` | Visible only when `code_apply = 1`. The engine picks whichever of (catalog × percent) or (discounted × percent) gives the larger customer saving. |

Full validation strings + the other code-only fields live on [[percent-discount-fields]].

## Default-off stacking (`code_apply = 0`)

For code-based Percent discounts, the default `code_apply = 0` means the code is **rejected at checkout** if ANY cart line already has a per-product discount (e.g., a [[marketing-discounts-fixed]] on one of the items). The merchant must explicitly enable **"Apply discount even if the cart contains products with a discount"** to stack.

For cart-wide Percent discounts (no code), `code_apply` is irrelevant — the discount applies regardless of existing per-product discounts; the engine subtracts based on the line price (with the `apply_regular_price` rule below).

The rejection is target-specific. It is triggered by a Percent code with target `order_over` when any cart line already has a discount, or (for shipping codes) target `all` with discounted lines — see [[marketing-discounts-shipping]]. A Percent code targeting **specific products / categories / vendors / selections** does NOT reject on an already-discounted cart; it applies (subject to the `apply_regular_price` rule at the per-line stage).

## Apply-regular-price re-evaluation

When the cart matches and a code-based Percent is valid, the percent always applies; `apply_regular_price` then governs which base price it computes against. With `code_apply = 1` AND `apply_regular_price = 1`, the engine computes per-line both:

- The percent against the line's **discounted** price (post-Fixed-discount).
- The percent against the line's **catalog (regular)** price.

It applies whichever yields the **larger customer saving** — guaranteeing the customer always gets the better deal between the catalog-price-based code and an already-running per-product discount.

## Percent + Flat — winner-takes-all when both are `order_over` no-code

When a Global Percent (`order_over` target, no code) and a Global Flat (`order_over` target, no code) both qualify on the same cart, **they do NOT stack — only the one yielding the larger absolute saving wins**. The cart-engine groups all `order_over` Flat + Percent matches into one pool and picks the discount with the highest computed saving. Examples on a 150 EUR cart:

- "20% off over 100 EUR" saves 30 EUR; "10 EUR off over 50 EUR" saves 10 EUR → **20% wins** (30 > 10).
- "10% off over 50 EUR" saves 15 EUR; "20 EUR off over 100 EUR" saves 20 EUR → **20 EUR Flat wins** (20 > 15).
- Two equally-valued rules → undefined which wins (the engine picks whichever the database returns first); the merchant should avoid creating overlapping equal-value rules.

## Other combinations DO stack

These live in independent slots in the engine:

- A no-code Percent (`order_over`) + a Code-based Percent → both apply.
- A no-code Percent + a per-product Fixed → both apply.
- A no-code Percent + a Quantity tier → both apply.
- A no-code Percent + a Countdown discount → both apply.
- A no-code Percent + a Free-shipping discount → both apply.
- A no-code Percent + a Cart Rule (cart-level or product-level) → both apply (Cart Rules evaluate against the post-Percent total — see *Cart Rules vs Percent discount ordering* below).

For code-based stacking, the `code_apply` toggle on the code-based discount gates whether it accepts a cart with any already-discounted line.

## Cart Rules vs Percent discount ordering

When [[apps-cart-rules]] coexist with a Percent discount, Discounts apply **first**, then Cart Rules. The Cart Rule's trigger evaluates against the cart total AFTER the Percent discount has reduced it.

## Stacking with other code-based Percent

Two code-based Percent discounts cannot apply on the same cart — the cart stores ONE code at a time. Switching codes overwrites the previous. (For multi-code scenarios, merchants use [[marketing-discounts-code-pro]]; codes there each fire separately.)

## Quantity-discount interaction — separate engine slots

When a Percent code with `code_apply = 1` lands on a cart line that already qualifies for a Quantity-discount tier (see [[marketing-discounts-quantity]]), the engine applies them in **separate slots**: the Quantity tier acts on the line first (line-level price drop), then the Percent code's allocation acts on the discounted line subtotal. There is no special "subtract the tier save" step at the Percent allocation stage — the Percent is simply computed against whatever per-unit price remains after the Quantity tier has applied.

Merchant-visible outcome: both savings show as separate negative lines in the cart breakdown. Total saving = Quantity-tier saving + (Percent × post-tier-price). Without `code_apply = 1`, the Percent code silently skips any line already on a Quantity tier (per the "Default-off stacking" rule).

## Business rules

- **Per-customer cap auto-clears the code** — if a logged-in customer hits the `maxused_user` cap for this Percent code, the platform doesn't merely fail to apply — it **wipes the code off the cart** and returns: *"You have already used this discount the maximum number of times"*. They'd need to enter a different code.
- **Cart Rules trigger sees the post-Percent total** — design cart-rule thresholds with the Percent reduction in mind.

## Related

- [[marketing-discounts-percent]] — hub.
- [[marketing-discounts-flat]] — sister type that shares the `order_over` winner-takes-all pool.
- [[marketing-discounts-fixed]] — per-product Fixed; the type that triggers `code_apply = 0` rejection on `order_over` Percent codes.
- [[marketing-discounts-quantity]] — Quantity tiers; separate engine slot.
- [[marketing-discounts-countdown]] — Countdown discount; stacks freely.
- [[marketing-discounts-shipping]] — Free shipping; stacks freely + has its own `code_apply = 0` exception for target=`all`.
- [[marketing-discounts-code-pro]] — multi-code campaigns.
- [[apps-cart-rules]] — evaluated AFTER Percent discounts.
- [[discount-stacking]] — cross-type stacking ladder + cooldown table.
- [[percent-discount-validity]] — strictly-greater `order_over` rule and per-customer cap mechanics.

## Open questions

None.
