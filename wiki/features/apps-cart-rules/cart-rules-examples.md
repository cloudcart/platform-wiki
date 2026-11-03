---
type: feature
nav_path: "Apps → Cart Rules → Examples"
route_name: ""
route_path: ""
aliases: ["Cart rule examples", "Cart rule recipes", "Cart rule worked scenarios", "BOGO", "VIP free shipping", "Tiered cart discount"]
tags: [apps, cart-rules, marketing, promotions, examples, recipes]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

> Part of [[apps-cart-rules]]. See the hub for the other aspects (conditions, actions, scoping, stacking, cooldowns, known issues).

# Cart Rules — Worked examples

## Purpose

This page collects 5 end-to-end recipes the merchant is most likely to want. Each example shows the rule structure as it lives on the wire — `condition_type`, `filter_type`, `value_type`, `value`, `records` — so the merchant (or an integrator using the GraphQL `createCartRule` mutation) can reproduce it directly. Each recipe also notes the [[cart-rules-stacking|stacking]] implications.

## Where to find it

These are configurations to set inside the **rule editor** at `/admin/apps/cart-rules/rules/create`. The *Generate with AI* button accepts a natural-language description and emits a rule of approximately the form below — but the AI's output is NOT post-validated against the schema, so review it before saving.

## What the merchant can do here

Use these as starting templates. Adapt the `records` arrays to your store's IDs, the `value` amounts to your currency target (send the **human value** — `50` for 50 EUR, `10` for 10%; the platform stores it ×100, see [[cart-rules-conditions]] → *Value scale*), and the `customer_group` IDs to your custom groups.

## Settings & fields — the worked examples

### Example 1 — "10% off when cart total > 50 EUR"

The simplest cart-level rule. Triggers on the cart's total; discounts the whole cart by 10%.

- **1 row.**
- **Row trigger:** `condition_type=cart`, `filter_type=cart_amount`, `value_type=gt`, `value=50` (50 EUR — send the human value; stored as `5000` cents).
- **Action:** `value_type=percent`, `value=10` (10%).
- **Action triggers:** empty (applies to whole cart).
- **Scope:** cart-level → subject to [[cart-rules-stacking|winner-takes-all]] if other cart-level rules also match.
- **Suggested title:** *"10% off carts over 50 EUR"*.
- **Suggested message:** *"Spend over 50 EUR and save 10%!"* (shows on lower-tier rows of a multi-row tiered rule — see Example 4 for the upsell pattern).

### Example 2 — "Buy 5 from Brand X, get the cheapest free" (BOGO)

The classic BOGO pattern. Row triggers identify *that* the customer qualifies (5+ Brand X items); action triggers narrow *which* line gets the discount (the cheapest of those Brand X items).

- **1 row.**
- **Row trigger 1:** `condition_type=product`, `filter_type=vendor`, `record_type=vendor`, `operator=in`, `records=[<Brand X id>]`.
- **Row trigger 2:** `filter_type=product_quantity`, `value_type=gte`, `value=5` (scoped to Brand X items in practice).
- **Action:** `value_type=percent`, `value=100`.
- **Action trigger:** `filter_type=product_lowest_price` within Brand X scope (combine with `product_from_condition` to chain the row trigger's vendor constraint into the action's targeting — see [[cart-rules-actions]]).
- **Scope:** product-level (action targets a specific line) → discount accumulates with other product-level matches on the same line.
- **Suggested title:** *"Buy 5 Brand X items, the cheapest is free"*.

Variant — *"Buy any 3, get the cheapest free"*: drop trigger 1 (vendor filter), keep trigger 2 (`product_quantity gte 3`), drop the vendor scope on the action — `product_lowest_price` then targets the cheapest line of the whole cart.

### Example 3 — "Free shipping for VIP customers all summer"

Customer-group + date-window combo. The summer dates gate eligibility before the matcher runs.

- **1 row.**
- **Row trigger:** `condition_type=customer`, `filter_type=customer_group`, `record_type=customer_group`, `operator=in`, `records=[<VIP group id>]`.
- **Action:** `value_type=free_shipping`, `value=null`.
- **Rule fields:** `active_from=2026-06-01`, `active_to=2026-08-31`.
- **Scope:** cart-level (free_shipping is always cart-level) → competes with other cart-level matches via winner-takes-all. **Free shipping loses to any other cart-level percent / amount match** because `free_shipping` stores `value=null/0` — see [[cart-rules-stacking]] for the gotcha and [[cart-rules-actions]] for the receiver-pays-waybill side-effect.

If the intent is *"customer never pays shipping, sender always pays"* with the waybill picker auto-hiding the receiver-pays option, use the [[marketing-discounts-shipping|Native Free shipping discount]] instead.

### Example 4 — "Stacked tiered cart with bonus free shipping over 200 EUR"

A multi-row tier ladder + a separate free-shipping deal in the same rule. The tier ladder is an **OR-fallback** — only ONE of its rows fires — but a separate row for free shipping evaluates independently because the engine's *one-row-per-rule* rule applies… **wait, it doesn't here.** The OR-fallback rule says only ONE row per rule fires. To stack the tiered discount with free shipping, the merchant must use **TWO separate rules**, not one rule with two rows.

**Rule A — tiered cart-amount discount (one rule, two rows):**

- **Row 1** (`sorting=1`, evaluated FIRST per the [[cart-rules-stacking|reverse-evaluation rule]]):
  - **Trigger:** `filter_type=cart_amount`, `value_type=gt`, `value=100` (100 EUR).
  - **Action:** `value_type=percent`, `value=10`.
  - **Message:** *"You qualify for 10% off — applied!"* (optional; usually only NEXT-tier messages show).
- **Row 0** (`sorting=0`, evaluated only if Row 1 didn't match):
  - **Trigger:** `filter_type=cart_amount`, `value_type=gt`, `value=50` (50 EUR).
  - **Action:** `value_type=percent`, `value=5`.
  - **Message:** *"Spend over 100 EUR for 10% off instead!"* (the merchant's standing upsell hint for tier 2).

**Rule B — separate free-shipping rule, lower `sort_order`:**

- **1 row.**
- **Row trigger:** `filter_type=cart_amount`, `value_type=gt`, `value=200` (200 EUR).
- **Action:** `value_type=free_shipping`, `value=null`.

**Stacking note:** Rule A is product-level if its action has product-targeting action-triggers, OR cart-level if action triggers are empty. With empty action triggers (as written), both Rule A's match and Rule B's `free_shipping` are cart-level → they compete via winner-takes-all → the percent rule wins (positive `value`) and free shipping is **silently dropped**. To get *"both 10% off AND free shipping above 200 EUR"*, the merchant must make Rule A product-level (e.g., add an action-trigger restricting it to a specific category, or use `product_from_condition` paired with a row trigger that identifies a product subset) — then Rule A is product-level and Rule B (cart-level free shipping) coexists.

This is one of the most frequently-misunderstood configurations. See [[cart-rules-stacking]] for the full mechanic.

### Example 5 — "Reward 3-time customers — 10% loyalty discount"

Customer-aggregate trigger. Uses the `order_count` aggregate that reads `customer.completed_orders` — only `paid` / `completed` orders count (see [[cart-rules-conditions]]).

- **1 row.**
- **Row trigger:** `condition_type=customer`, `filter_type=order_count`, `value_type=gte`, `value=3`.
- **Action:** `value_type=percent`, `value=10`.
- **Scope:** cart-level (no action triggers).
- **Suggested title:** *"Loyalty 10% off — thanks for being a returning customer!"*.

**Caveat:** the customer aggregate `completed_orders` is updated when an order reaches `paid` / `completed` — it does NOT include `pending` orders. A customer with 5 pending unpaid orders will still match `order_count gte 3` as `false` until at least 3 of them clear. There is also no *"customer's last order was within N days"* filter; the only customer-level numeric aggregates exposed are `order_count` and `order_amount` (both lifetime totals).

## Business rules

These examples assume the default behaviour described on the hub. Each is fully verified against the matcher source. Two cross-cutting rules to remember when adapting them:

- **Provide human values; the save helper stores them ×100.** Money: send `50` for 50 EUR (stored `5000` cents). Percent: send the whole percent — `10` for 10% (stored `1000`). Quantity/count: plain integers (`2` = 2). Free shipping's `value=null`. See [[cart-rules-conditions]] → *Value scale*.
- **Multi-row rules are an OR-fallback ladder, not accumulating.** Only ONE row per rule fires. To stack effects, use multiple rules — and remember that products are consumed across rules in `sort_order DESC`. See [[cart-rules-stacking]].

## Related

- [[apps-cart-rules]] — hub.
- [[cart-rules-conditions]] — the trigger taxonomy used in every example.
- [[cart-rules-actions]] — discount types + action-triggers (`product_lowest_price`, `product_from_condition`, etc.).
- [[cart-rules-scoping]] — cart-level vs product-level scope choice in every recipe.
- [[cart-rules-stacking]] — why Rule A + Rule B in Example 4 must be configured carefully.
- [[cart-rules-cooldowns]] — date-window gating used in Example 3.
- [[marketing-discounts-shipping]] — alternative free-shipping mechanism with `has free shipping` flag set.
- [[customers-custom-groups]] — custom customer groups used as audience targets.

## Open questions

None.
