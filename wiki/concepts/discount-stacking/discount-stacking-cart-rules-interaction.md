---
type: concept
nav_path: "Concept → Discount stacking → Cart Rules interaction"
aliases: ["Cart Rules vs Discounts", "Cart Rules run after Discounts", "Cart-level Cart Rule winner-takes-all", "Product-level Cart Rule stacking", "sort_order on Cart Rules", "No combine_rules setting", "Cart Rules post-discount cart total"]
tags: [marketing, discounts, stacking, cart-rules, concepts]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[discount-stacking]]. See the hub for the other aspects (code_apply toggle, evaluation order, cart code slots, uses counter, plan gating, cooldown / attachments).

# Discount stacking — Cart Rules interaction

## Definition

[[apps-cart-rules|Cart Rules]] are a completely separate promotion engine that runs **after** all Discount logic. They see the **post-discount cart total**. So a Cart Rule that says *"if cart total > 50 EUR, free shipping"* sees the cart total AFTER all discounts applied. Discounts never see Cart Rules. (verify)

This layering means Cart Rules are for **complex multi-trigger promotions** (e.g., "buy 2 from category A AND 1 from category B, get 30% off the cheapest") while Discounts handle single-target rules with first-class storefront support (the "from X / now Y" listing display).

## Scope

Covered:

- The ordering: Discounts evaluate first, then Cart Rules.
- The cart-level vs. product-level Cart Rule stacking semantics.
- The `sort_order` field that's on Cart Rules but NOT on Discounts.
- The fact that there is NO `combine_rules` setting — the cart-level winner-takes-all is hard-coded.
- Capabilities Cart Rules have that Discounts do not (set tax rate, free gift, change shipping options).

Not covered here:

- The internal Discount-engine evaluation chain — see [[discount-stacking-evaluation-order]].
- The Cart Rule field-by-field configuration — see [[apps-cart-rules-rules]].
- The Cart Rule cooldowns / scoping mechanics — see [[apps-cart-rules]].

## Contrasts

- **Discounts vs Cart Rules — runtime ordering** — Discounts evaluate FIRST. After all discounts attach, Cart Rules evaluate against the POST-discount cart total. Discounts never see Cart Rules' modifications.
- **Discount `code_apply` vs Cart Rule stacking** — Discounts use the `code_apply` reject-or-allow toggle (see [[discount-stacking-code-apply]]). Cart Rules use a different mechanism: cart-level rules are winner-takes-all by `value`; product-level rules accumulate per line. The two engines do NOT share stacking semantics.
- **Cart Rule `sort_order` vs Discount implicit priority** — Cart Rules expose `sort_order` per rule (user-controllable). Discounts have only the [[discount-stacking-evaluation-order|hard-coded implicit priority]]; no user-controllable priority field.
- **Cart-level Cart Rule winner-takes-all vs Product-level Cart Rule accumulate** — these are two different Cart Rule stacking modes that operate inside the Cart Rules engine itself. They are NOT discount-stacking concepts. They matter to this hub only because Cart Rules sit downstream of Discounts.

## Where it applies

Every cart update and order submit on the platform runs Discounts → Cart Rules in that order:

- **Storefront cart updates** — items added / removed, codes entered, shipping zones picked.
- **Storefront submit** — final snapshot.
- **Admin order edit** on [[orders-details]] — re-running the chain on edit.

### Cart-level Cart Rule stacking — only the HIGHEST-VALUE match wins per cart

Multiple matched cart-level Cart Rules do **NOT sum**. The Cart Rule engine sorts matched cart-level actions by their stored `value` (descending) and applies **ONLY the top one**, silently dropping the rest. (verify) See [[apps-cart-rules]] *"Cart-level stacking"*.

Example: two whole-cart percent-off rules (50% and 30%) → only the 50% applies; the 30% is dropped without surfacing.

**There is NO `combine_rules` setting.** The cart-level winner-takes-all rule is hard-coded; the merchant cannot toggle it.

### Product-level Cart Rule stacking — multiple rules accumulate per line

Different product-level Cart Rules targeting the same product line each contribute their modification, subject to a defensive cap:

- A fixed-amount modification is dropped if it would push the line price negative.
- Percent modifications are always allowed.

See [[apps-cart-rules]] *"Product-level stacking"*. (verify)

### What Cart Rules can do that Discounts cannot

- **Set a tax rate** on the cart / line.
- **Attach a free gift product** to the order.
- **Change shipping options** (e.g., force a specific carrier).
- **Multi-trigger conditions** ("buy from category A AND category B").
- **Explicit priority via `sort_order`** — merchant decides which rule evaluates first.

Discounts, conversely, are simpler and have first-class storefront support (the "from X / now Y" listing display on category pages and product detail pages) — Cart Rules do NOT show on the storefront listing.

### When to pick which

- **Single-target rule** ("10% off when this code is used") → Discount. Simpler, has storefront listing support.
- **Multi-trigger promotion** ("buy 2 from A AND 1 from B, get 30% off cheapest") → Cart Rule.
- **Free-gift offer** → Cart Rule.
- **Cart-total threshold for free shipping** → either (a Shipping discount with `order_over`, or a Cart Rule); the Shipping discount has the `force_save` persistence on order edit.

## Related

- [[discount-stacking]] — hub.
- [[discount-stacking-code-apply]] — Discount-side stacking toggle (separate engine).
- [[discount-stacking-evaluation-order]] — Discount-side priority chain that runs before Cart Rules.
- [[discount-stacking-cooldown-and-attachments]] — `force_save` persistence on order edit.
- [[cart-rule]] — entity that evaluates AFTER discounts.
- [[apps-cart-rules]] — master Cart Rules screen.
- [[apps-cart-rules-rules]] — per-rule editor with `sort_order` field.
- [[discount]] — the entity Cart Rules sit on top of.
- [[cart]] / [[order]] — the artefacts both engines write against.
- [[orders-details]] — order-edit re-runs both engines.

## Open Questions

None.
