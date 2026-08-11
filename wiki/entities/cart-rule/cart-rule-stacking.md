---
type: entity
nav_path: "Entity → Cart Rule → Stacking"
aliases: ["Cart Rule stacking", "Cart Rule priority", "Cart Rule sort order", "Cart-level vs product-level stacking"]
tags: [entity, marketing, automation, discounts, rules-engine, stacking]
created: 2026-06-10
updated: 2026-06-10
source_count: 5
---

# Cart Rule — Stacking

> Part of [[cart-rule]]. See the hub for related aspects (fields, rows-and-triggers, actions, lifecycle, evaluation).

## Identity

How [[cart-rule|Cart Rules]] interact with each other and with [[discount|Discounts]] when more than one could apply to the same cart at the same time. The headline rule: **cart-level actions are winner-takes-all; product-level actions accumulate.**

## Aliases

- "Cart Rule stacking" / "Cart Rule priority" — merchant-facing terms.
- "Cart Rule sort order" — the `sort_order` field that controls evaluation order.
- "Cart-level vs product-level stacking" — the split this page exists to document.

## Key Attributes

Stacking semantics ride on these per-rule + per-action fields:

- **`sort_order`** (rule) — evaluation priority; higher = first. Auto-set to `MAX(sort_order)+1` on create.
- **`group`** (action) — `cart` (whole-cart) vs `product` (per-line). Drives the winner-takes-all vs accumulate split.
- **`value`** (action) — used by the cart-level highest-`value`-wins tiebreaker.

## Cart Rules run AFTER standard Discounts

The checkout pipeline evaluates [[discount|Discounts]] FIRST (per their own stacking rules — see [[discount-stacking]]). Once discounts have attached, Cart Rules run against the **post-discount** cart. This means a Cart Rule that says *"if cart total > 50 EUR, free shipping"* sees the cart total AFTER all discounts applied — so a 50% discount that brought a 100 EUR cart down to 50 EUR won't trigger this rule (the post-discount total is now exactly at the threshold, not over).

Cart Rules cannot be "seen" by standard Discounts. The reverse direction doesn't exist. See [[discount-stacking-evaluation-order]] for the full ordering.

## Rules stack — split by scope

Stacking behaviour is **split by scope** (verify — recorded against the cart-rule cart event handler):

### Cart-level (whole-cart) action stacking — HIGHEST-VALUE wins

When multiple rules each produce a cart-level match (whole-cart actions like *"5% off the cart"*, *"50 EUR off the order"*, *"free shipping for the order"*), the platform groups all matched cart-level actions and selects the **single highest `value`** — the others are dropped without surfacing to the merchant or customer. Two whole-cart percent rules — 50% and 30% — on the same cart will yield ONLY the 50% applied; the 30% does not stack on top, does not appear on the cart summary, does not appear in the order's discount list.

This is hard-coded behaviour — there is NO merchant-toggleable setting to change it. (Older wiki phrasing referred to a `combine_rules` setting; no such setting exists anywhere on the platform.)

### Product-level (per-line) action stacking — ACCUMULATE on affected lines

When multiple rules each produce a product-level match (per-line actions like *"15% off Brand X items"*, *"3 EUR off Summer category"*), each matching rule contributes its modification independently to the targeted lines. So a category rule giving 5% off summer items AND a brand rule giving 10% off Brand X products will both attach to a *"Brand X summer T-shirt"* line.

One defensive cap: a fixed-amount modification is silently dropped if it would push the per-unit price below zero (percent modifications are always allowed). See [[cart-rule-actions]].

### Merchant implication

The *"stack 3 deals on one cart"* design pattern only works for product-level actions, OR for a mix of one cart-level + multiple product-level. Two competing cart-level percent rules → only the higher one applies. To run *"5% category-wide + 3% loyal-customer bonus + free shipping"*, the 5% and 3% must be **product-level** (targeting specific lines) and the free shipping is a **cart-level** standalone; the merchant cannot define both 5% and 3% as cart-level whole-cart rules and expect them to combine.

## `sort_order` = evaluation priority, NOT winner picker

The `sort_order` field controls evaluation order for purposes of running rules through the engine in a defined sequence, but does NOT change the cart-level winner-takes-all rule. Drag-and-drop reorder on the list updates `sort_order` for the affected rules in one operation. Higher = evaluated first.

### Auto-assigned sort order on create

When a brand-new Cart Rule is saved (no `sort_order` supplied by the merchant — which is the default since the form doesn't expose the field), the model's `creating` hook calls `MAX(sort_order) + 1` across the merchant's existing rules and writes that value before persistence. So a freshly-created rule always lands at the top of the priority stack. The merchant can re-order afterwards via drag-and-drop, but a brand-new rule is guaranteed visible at position 1 without any merchant action.

## Where it appears

- [[cart-rules-stacking]] — feature-side aspect on the same topic from the merchant editor UX.
- [[discount-stacking]] — concept page on overall stacking semantics including Discounts.
- [[discount-stacking-evaluation-order]] — the cross-cluster ordering (Discounts then Cart Rules).
- [[discount-stacking-cart-rules-interaction]] — concept-side analysis of the interaction layer.

## Related

- [[cart-rule]] — hub.
- [[cart-rule-rows-and-triggers]] — within-rule row OR-fallback (different mechanism from cross-rule stacking).
- [[cart-rule-actions]] — the cart-level vs product-level split that drives stacking behaviour.
- [[cart-rule-evaluation]] — when stacking re-computes.
- [[discount]] — sibling engine evaluated first.

## Open Questions

None.
