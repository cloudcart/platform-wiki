---
type: concept
nav_path: "Concept → Discount stacking → Evaluation order"
aliases: ["Discount evaluation order", "Discount priority", "Quantity tier", "Up-sell discount priority", "order_over winner selection", "Highest threshold wins", "Discount threshold boundaries"]
tags: [marketing, discounts, stacking, priority, evaluation, concepts]
plan_gates: []
created: 2026-06-10
updated: 2026-11-04
source_count: 3
---

> Part of [[discount-stacking]]. See the hub for the other aspects (code_apply toggle, cart code slots, uses counter, plan gating, Cart Rules interaction, per-variant rows).

# Discount stacking — evaluation order

## Definition

When multiple discounts could match the same cart, CloudCart evaluates them in a fixed **implicit priority chain**. There is **no user-controllable priority field on Discounts** (unlike [[cart-rule|Cart Rules]] which have `sort_order`).

The implicit evaluation order:

1. **One product discount per line**, the first that fits: up-sell offer, cross-sell offer, bundle price, Quantity tier, otherwise the cheapest active row among Fixed and no-code Flat or Percent. Product-level discounts on one line never add up.
2. **A line-level code** on the reduced amount, subject to `code_apply` (see [[discount-stacking-code-apply]]).
3. **Cart Rules** ([[cart-rule]]) — conditions see the total after steps 1 and 2; product-level reductions land on the lines. See [[discount-stacking-cart-rules-interaction]].
4. **Order-level discounts**, each on that same subtotal: no-code Orders over, Orders-over code, Countdown, payment-method discount, cart-level Cart Rule. These kinds do not exclude each other.
5. **Free shipping**, last, one only: no-code or cross-sell, else code, else payment method, else Cart Rule.

One order can carry one product discount per line, one code or a set of Container codes, one no-code Orders over, Countdown, the payment-method discount, one cart-level rule, and product-level rules.

## Scope

Covered:

- The 5-step implicit evaluation chain.
- The limits on Countdown (checkout uses one) and on Quantity (one per product).
- The `order_over` winner-selection rule among several eligible no-code Flat / Percent discounts, and the threshold boundaries.
- The shipping-discount resolution path (one per cart, first-match-wins).
- The cumulation-vs-stacking distinction (line level compounds; order level shares one subtotal).

Not covered here:

- The `code_apply` toggle — see [[discount-stacking-code-apply]].
- How Cart Rules interleave with discounts — see [[discount-stacking-cart-rules-interaction]].
- Order-level vs line-level snapshot on the order — see [[orders-details]] sections.

## Contrasts

- **Stacking vs. cumulation** — "stacking" means multiple discounts apply to the same cart. On one line they compound: a 10% code on a line already 20% off takes 10% off the discounted price, unless `apply_regular_price` is on. Order-level discounts are calculated on the subtotal after line reductions and share that one base among themselves.
- **Stacking vs. priority** — stacking decides WHETHER multiple discounts apply. Priority decides in WHAT ORDER the engine evaluates them. CloudCart has the implicit chain above but does NOT expose a user priority field on Discounts.
- **Implicit Discount priority vs. explicit Cart Rule `sort_order`** — Discounts have a hard-coded chain; the merchant cannot reorder. Cart Rules expose `sort_order` per rule.

## Where it applies

The chain governs every discount-attachment moment on the platform:

- **Storefront cart updates** — adding / removing items, changing quantities, applying a code.
- **Storefront submit** — the snapshot frozen onto the [[order|Order]].
- **Admin order edit** on [[orders-details]] — quantity / line edits re-run the chain.
- **`orders-discount-add` action** — adding a discount from the admin runs no stacking switch and no customer limits. The only refusal is an order that already has an order-level discount.

### Subscription lines that take no other discount

A subscription line bought on a plan option with **Combine with other discounts** off ([[apps-subscriptions-plans]]) skips the line-level steps of this chain: no product discount, no line-level code, no cart-rule line discount. One-time lines in the same cart run the chain as usual, and an order-level code (target `order_over`, or a shipping code) still applies.

### Countdown and Quantity limits

- **Countdown discount** — a second one can be saved. Checkout uses the first active one found, and tries no other.
- **Per-product Quantity discount** — a product can be in only one Quantity discount, active or not. Validation: *"Product is already in use"*.

### `order_over` winner selection — highest threshold wins

When several no-code `order_over` Flat / Percent discounts qualify on the same cart, the highest threshold the subtotal passes wins, whatever it saves, flat or percent. If that one cannot apply, none does; no other is tried.

Example: *"10 EUR off over 50 EUR"* vs *"5 EUR off over 100 EUR"* on a 150 EUR cart → the 5 EUR discount wins. Largest saving applies only among several Orders-over conditions inside one Code PRO code.

### Threshold boundaries

- **No-code flat or percent, Orders over** — subtotal strictly above the threshold. Subtotal = lines after product discounts, line-level codes and product-level Cart Rule reductions.
- **Code flat or percent, Orders over** — strictly above, at entry and in totals.
- **No-code free shipping** — at or above, measured on the total before shipping (after whole-order discounts).
- **Free-shipping code with a threshold** — at entry the products subtotal must be strictly above it; once accepted, at or above on the total before shipping.
- **Countdown** — at or above, on the products subtotal. Not rechecked on a placed order.
- **Code PRO `order_over`** — at or above, on the subtotal of the lines.
- **Code PRO on any other target** — its amount is a minimum unit price per line, at or above. For `all`, lines are checked in cart order and the first below the minimum stops that condition.

### Shipping-discount resolution — one per cart, first-match wins

The platform allows only **one shipping discount per cart**: no-code or cross-sell, else code, else payment method, else Cart Rule. The resolution tries every no-code shipping discount; the first that qualifies attaches and the rest are skipped. One that does not qualify does not end the search. This is a separate path from the highest-threshold rule above — shipping discounts don't compete by amount.

### Order-level vs. line-level attachment

Discounts can attach at two scopes; the order's `discount_amount` total is the sum of all attached discounts (order-level + line-level):

- **Order-level discounts** (Orders over with or without a code, free shipping, Countdown, payment-method discount) — show as one action row at the order level on [[orders-details]].
- **Line-level discounts** (Fixed, Quantity tier, no-code Flat or Percent, a code for every product or a specific target) — show on the individual order-product line. Target `all` is never one order-level amount: without a code it sits on each unit, with a code on each line. See [[discount-stacking-amount-by-target]].

## Related

- [[discount-stacking]] — hub.
- [[discount-stacking-code-apply]] — the `code_apply` switch behind step 2.
- [[discount-stacking-cart-rules-interaction]] — Cart Rules, step 3.
- [[marketing-discounts-fixed]] — per-product Fixed; step 1.
- [[marketing-discounts-quantity]] — Quantity-tier; step 1.
- [[apps-up-cross-sell]] — Up-sell / Cross-sell; step 1.
- [[marketing-discounts-countdown]] — Countdown; step 4.
- [[marketing-discounts-flat]] / [[marketing-discounts-percent]] / [[marketing-discounts-shipping]] — no-code product rows at step 1, Orders over at step 4, free shipping at step 5.
- [[discount]] — entity with `total_value`, `order_over`, `settings`.
- [[cart-rule]] — sibling engine with explicit `sort_order`.
- [[orders-details]] — order-level vs. line-level rows.
- [[cart]] / [[order]] — where the snapshot lands.

## Open Questions

None.
