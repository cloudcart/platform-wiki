---
type: feature
nav_path: "Apps → Cart Rules → Scoping"
route_name: ""
route_path: ""
aliases: ["Cart rule scoping", "Cart-level vs product-level rules", "Rule target", "Cart rule applies to"]
tags: [apps, cart-rules, marketing, promotions, scoping]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

> Part of [[apps-cart-rules]]. See the hub for the other aspects (conditions, actions, stacking, cooldowns, examples, known issues).

# Cart Rules — Scoping

## Purpose

A cart rule's **scope** is the boundary between *"what makes the rule fire"* and *"what gets the discount"*. Two layers determine scope:

1. **Row triggers** — decide whether the rule fires at all for a given cart. These can also semantically scope the rule (e.g., *"only fires when at least one Brand X item is in the cart"*).
2. **Action triggers** — decide which cart lines (or the whole cart) actually receive the discount when the row matched.

Scoping resolves to one of two distinct paths inside the matcher:

- **Cart-level** — the action applies once to the whole-cart total (and is subject to winner-takes-all stacking).
- **Product-level** — the action applies per-line to each matching cart line (and stacks additively with other product-level matches on the same line).

The choice between cart-level and product-level scope is determined by whether the action has any product-targeting action-trigger. **No action triggers → cart-level. Any product / vendor / category / tag / selection / `product_*_price` / `product_from_condition` action trigger → product-level.**

## Where to find it

There is no dedicated *Scope* control in the rule editor — scope is **implicit** in how the merchant configures the action's *Action triggers* sub-list at `/admin/apps/cart-rules/rules/create` (or `/edit/{id}`). Leaving action triggers empty makes the rule cart-level; adding a product-targeting action trigger makes it product-level.

## What the merchant can do here

Practical scoping recipes:

| Intended scope | Action-trigger configuration |
|---|---|
| Whole cart (cart-level) | Action triggers list empty |
| Specific products only | Action trigger `filter_type=product`, `operator=in`, `records=[id…]` |
| Specific vendor's items only | Action trigger `filter_type=vendor`, `operator=in`, `records=[vendor_id]` |
| Specific category only | Action trigger `filter_type=category`, `operator=in`, `records=[category_id]` |
| Specific tag only | Action trigger `filter_type=tag`, `operator=in`, `records=[tag_id]` |
| Specific smart-collection only | Action trigger `filter_type=selection`, `operator=in`, `records=[selection_id]` |
| Cheapest matching line only (BOGO) | Action trigger `filter_type=product_lowest_price` |
| Most-expensive matching line only | Action trigger `filter_type=product_highest_price` |
| Same items the row's triggers identified (chain row → action) | Action trigger `filter_type=product_from_condition` |
| Items OTHER than the row's triggers identified (buy X get Y free) | Action trigger `filter_type=product_not_from_condition` |
| Specific customer group only | Row trigger `condition_type=customer`, `filter_type=customer_group`, `record_type=customer_group`, `operator=in`, `records=[group_id]` |

For the action-trigger filter taxonomy and the extras (`product_lowest_price`, etc.), see [[cart-rules-actions]].

## Settings & fields

### Row-level vs action-level scoping

| Layer | What it controls | Lives in |
|---|---|---|
| Row triggers | Whether the row's action fires at all | `cart_rule_trigger_condition` rows on the row |
| Action triggers | Which cart lines (or none → whole cart) receive the modification | `cart_rule_action_trigger_condition` rows on the action |

### Customer-group scoping

Targeting customers is done **only through the customer-group filter** at the row-trigger level. Membership in [[customers-custom-groups|custom customer groups]] is the proxy for any audience segmentation Cart Rules can do. The auto-created **Guests** group is the proxy for "is guest checkout" — `IN Guests` targets guests, `NOT IN Guests` targets registered customers.

For audience definitions that depend on behaviour (last-order-recency, AOV, abandon history), the merchant builds a [[marketing-segments|Segment]], assigns its members to a custom group, then triggers the rule on that group. Cart Rules don't read segment membership directly.

### Geographic / per-store scoping

Cart Rules have **no native country / region / per-store-location scoping** — geo-targeting is not on the filter list. Workarounds: use the customer-group proxy (segment by geography → group → trigger on group), or use one of the geo-aware app-level features. See [[geo-targeting]].

### Customer fallback (guest checkout)

When the cart's order has no customer (guest checkout), a **default customer is materialised with the guest group ID** before the matcher runs. This means customer-level triggers can still evaluate against guest orders — they always match the Guests group. The merchant can target guests explicitly by including the Guests group in a `customer_group IN` trigger; conversely, `customer_group NOT IN Guests` filters them out.

### Customer-specific exemption

A merchant can exclude one specific customer from a rule by:

- Putting them in a [[customers-custom-groups|custom group]] that the rule's `customer_group` trigger does NOT target (use `customer_group` with `operator=not_in`).

No per-customer "blocklist" exists separately from groups.

## Business rules

### Empty action triggers → cart-level scope (winner-takes-all)

When a row's action has zero action-triggers, the action is **cart-level**. Cart-level actions stack as **winner-takes-all** across all matched rules (only the single highest-`value` cart-level match applies). See [[cart-rules-stacking]] for the full mechanic.

### Any product-targeting action-trigger → product-level scope (accumulates)

When the action has even ONE product / vendor / category / tag / selection / `product_*_price` / `product_from_condition` action-trigger, the action is **product-level**. Product-level actions accumulate per matching line — a 5%-off-Brand-X rule + a 3%-off-summer rule will both apply to a Brand X summer item.

### Row triggers narrow firing; action triggers narrow targeting

A common merchant mistake is to confuse the two:

- *"10% off the whole cart when cart > 100 EUR"* — row trigger: `cart_amount gt 100 EUR`. Action triggers: **empty**.
- *"10% off Brand X items only, when cart > 100 EUR"* — row trigger: `cart_amount gt 100 EUR`. Action triggers: `vendor IN [Brand X]`.
- *"10% off Brand X items only, when at least one Brand X item is in the cart"* — row trigger: `vendor IN [Brand X]`. Action trigger: `product_from_condition` (so the discount targets only the Brand X items the row trigger identified, not the whole cart).

### Products consumed across rules (not across rows of the same rule)

When a rule successfully matches (any one of its rows fires), the matched products are **removed from the cart-data pool** before the engine moves on to evaluate the next rule. This is a scoping side-effect: a "broad" rule with high `sort_order` that matches many products will starve later, more-specific rules. See [[cart-rules-stacking]] for the consumption mechanics and the merchant-impact example.

### Variant- and option-level scoping

The product-level filter list (see [[cart-rules-conditions]]) includes `product_variant` and `product_option` for scoping by a variant attribute (e.g., *"only Size = L"*) or a line option (e.g., *"only items with engraving applied"*). Both are string-pool filters — comparisons are case-insensitive.

## Related

- [[apps-cart-rules]] — hub.
- [[cart-rules-conditions]] — full filter taxonomy used for row-trigger scoping.
- [[cart-rules-actions]] — action triggers + the extras (`product_lowest_price`, `product_from_condition`).
- [[cart-rules-stacking]] — cart-level vs product-level resolution; products-consumed-across-rules.
- [[customers-custom-groups]] — the audience-scoping primitive Cart Rules reads.
- [[marketing-segments]] — segment → custom group bridge for behaviour-based audiences.
- [[geo-targeting]] — geographic targeting is NOT native to Cart Rules; this concept covers the workarounds.
- [[products-options-overview]] / [[variant]] — entities the `product_option` / `product_variant` filters read.

## Open questions

None.
