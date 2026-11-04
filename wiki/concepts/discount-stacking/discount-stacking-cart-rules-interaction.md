---
type: concept
nav_path: "Concept → Discount stacking → Cart Rules interaction"
aliases: ["Cart Rules vs Discounts", "Cart Rules before order-level discounts", "Cart-level Cart Rule winner-takes-all", "Product-level Cart Rule stacking", "sort_order on Cart Rules", "No combine_rules setting", "Cart Rule cart total condition"]
tags: [marketing, discounts, stacking, cart-rules, concepts]
plan_gates: []
created: 2026-06-10
updated: 2026-11-04
source_count: 3
---

> Part of [[discount-stacking]]. See the hub for the other aspects (code_apply toggle, evaluation order, cart code slots, uses counter, plan gating, per-variant rows).

# Discount stacking — Cart Rules interaction

## Definition

[[apps-cart-rules|Cart Rules]] are a separate promotion engine evaluated **after product discounts and line-level codes, and before order-level discounts**. A Cart Rule that says *"if cart total > 50 EUR, free shipping"* sees the total after product discounts and line-level codes. It does not see no-code Orders over discounts, Orders-over codes, Countdown or payment-method discounts. Those are calculated, and their thresholds checked, on the subtotal after product-level rule reductions.

This layering means Cart Rules are for **complex multi-trigger promotions** (e.g., "buy 2 from category A AND 1 from category B, get 30% off the cheapest") while Discounts handle single-target rules with first-class storefront support (the "from X / now Y" listing display).

## Scope

Covered:

- The ordering: product discounts and line-level codes, then Cart Rules, then order-level discounts.
- The cart-level vs. product-level Cart Rule stacking semantics.
- The `sort_order` field that's on Cart Rules but NOT on Discounts.
- The fact that there is NO `combine_rules` setting — the cart-level winner-takes-all is hard-coded.
- What Cart Rules can do: their conditions and their three actions.

Not covered here:

- The internal Discount-engine evaluation chain — see [[discount-stacking-evaluation-order]].
- The Cart Rule field-by-field configuration — see [[apps-cart-rules-rules]].
- The Cart Rule scoping mechanics — see [[apps-cart-rules]].

## Contrasts

- **Discounts vs Cart Rules — runtime ordering** — product discounts and line-level codes first. Cart Rules evaluate against that total and their product-level reductions land on the lines. Order-level discounts then work on the resulting subtotal.
- **Discount `code_apply` vs Cart Rule stacking** — Discounts use the `code_apply` toggle (see [[discount-stacking-code-apply]]). Cart Rules use a different mechanism: cart-level rules are winner-takes-all by `value`; product-level rules accumulate per line. The two engines do NOT share stacking semantics.
- **Cart Rule `sort_order` vs Discount implicit priority** — Cart Rules expose `sort_order` per rule (user-controllable). Discounts have only the [[discount-stacking-evaluation-order|hard-coded implicit priority]]; no user-controllable priority field.
- **Cart-level Cart Rule winner-takes-all vs Product-level Cart Rule accumulate** — these are two different Cart Rule stacking modes that operate inside the Cart Rules engine itself. They are NOT discount-stacking concepts.

## Where it applies

A subscription line whose plan option has **Combine with other discounts** off ([[apps-subscriptions-plans]]) still counts towards a rule's conditions, but receives none of the rule's line discount.

Every cart update and order submit on the platform runs this sequence:

- **Storefront cart updates** — items added / removed, codes entered, shipping zones picked.
- **Storefront submit** — final snapshot.
- **Admin order edit** on [[orders-details]] — re-running the chain on edit.

### Cart-level Cart Rule stacking — only the HIGHEST-VALUE match wins per cart

Multiple matched cart-level Cart Rules do **NOT sum**. The Cart Rule engine sorts matched cart-level actions by their stored `value` (descending) and applies **ONLY the top one**, silently dropping the rest. See [[apps-cart-rules]] *"Cart-level stacking"*.

Example: two whole-cart percent-off rules (50% and 30%) → only the 50% applies; the 30% is dropped without surfacing.

**There is NO `combine_rules` setting.** The cart-level winner-takes-all rule is hard-coded; the merchant cannot toggle it.

### Product-level Cart Rule stacking — multiple rules accumulate per line

Different product-level Cart Rules targeting the same product line each contribute their modification, subject to a defensive cap:

- A fixed-amount modification is dropped if it would push the line price negative.
- Percent modifications are always allowed.

See [[apps-cart-rules]] *"Product-level stacking"*. (verify)

### What Cart Rules can do

- **Actions: only amount, percent and free shipping.** They reduce an already discounted line or the order. No price-setting, no adding amounts, no forced method.
- **Multi-trigger conditions** ("buy from category A AND category B").
- **Explicit priority via `sort_order`** — merchant decides which rule evaluates first.

Discounts, conversely, are simpler and have first-class storefront support (the "from X / now Y" listing display on category pages and product detail pages) — Cart Rules do NOT show on the storefront listing.

### When to pick which

- **Single-target rule** ("10% off when this code is used") → Discount. Simpler, has storefront listing support.
- **Multi-trigger promotion** ("buy 2 from A AND 1 from B, get 30% off cheapest") → Cart Rule.
- **Cart-total threshold for free shipping** → either (a Shipping discount with `order_over`, or a Cart Rule); the Shipping discount has the `force_save` switch for order edit.

## Related

- [[discount-stacking]] — hub.
- [[discount-stacking-code-apply]] — Discount-side stacking toggle (separate engine).
- [[discount-stacking-evaluation-order]] — the full chain, Cart Rules included.
- [[discount-stacking-product-rows]] — `force_save` on order edit.
- [[cart-rule]] — entity evaluated after product discounts and line-level codes.
- [[apps-cart-rules]] — master Cart Rules screen.
- [[apps-cart-rules-rules]] — per-rule editor with `sort_order` field.
- [[discount]] — the entity Cart Rules work alongside.
- [[cart]] / [[order]] — the artefacts both engines write against.
- [[orders-details]] — order-edit re-runs both engines.

## Open Questions

None.
