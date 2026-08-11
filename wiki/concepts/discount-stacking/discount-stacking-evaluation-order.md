---
type: concept
nav_path: "Concept → Discount stacking → Evaluation order"
aliases: ["Discount evaluation order", "Discount priority", "Per-product Fixed first", "Quantity tier", "Up-sell discount priority", "Countdown bucket", "order_over winner selection", "Largest absolute saving wins"]
tags: [marketing, discounts, stacking, priority, evaluation, concepts]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[discount-stacking]]. See the hub for the other aspects (code_apply toggle, cart code slots, uses counter, plan gating, Cart Rules interaction, cooldown / attachments).

# Discount stacking — evaluation order

## Definition

When multiple discounts could match the same cart, CloudCart evaluates them in a fixed **implicit priority chain**. There is **no user-controllable priority field on Discounts** (unlike [[cart-rule|Cart Rules]] which have `sort_order`). (verify)

The implicit evaluation order:

1. **Per-product Fixed discounts** — attach first, override the catalog price on each matching line.
2. **Quantity-tier discounts** — evaluate per-product against the matching line; only one Quantity discount can target any given product at a time.
3. **Up-sell / Cross-sell discounts** — when configured via [[apps-up-cross-sell]]; attach to up-sell / cross-sell bundles.
4. **Countdown discount** — applies at the whole-order bucket (only one Countdown can exist per store).
5. **Global / Code-based whole-order discounts** — apply against the post-line-discount cart total, subject to `code_apply` rules (see [[discount-stacking-code-apply]]).
6. **Cart Rules** ([[cart-rule]]) — run AFTER all of the above, against the post-discount cart total. See [[discount-stacking-cart-rules-interaction]].

## Scope

Covered:

- The 6-step implicit evaluation chain.
- The store-level uniqueness limits (one Countdown per store, one Quantity per product) that enforce single-target evaluation per slot.
- The `order_over` winner-selection rule among multiple eligible Flat / Percent discounts.
- The shipping-discount resolution path (one per cart, first-match-wins).
- The cumulation-vs-stacking distinction (each discount computes against its own base, not the previous discount's result).

Not covered here:

- The `code_apply` reject-or-allow toggle that gates code-based attachment — see [[discount-stacking-code-apply]].
- How Cart Rules interleave with discounts — see [[discount-stacking-cart-rules-interaction]].
- Order-level vs line-level snapshot on the order — see [[orders-details]] sections.

## Contrasts

- **Stacking vs. cumulation** — "stacking" specifically means multiple discounts attach to the same cart simultaneously. "Cumulation" — applying a 10% then 5% off the result — is **NOT** how the platform combines discounts. Multiple flat / percent discounts attach individually to the matching lines or the order, but **each is computed against its own base, not against the previous discount's result.**
- **Stacking vs. priority** — stacking decides WHETHER multiple discounts apply. Priority decides in WHAT ORDER the engine evaluates them. CloudCart has the implicit chain above but does NOT expose a user priority field on Discounts.
- **Implicit Discount priority vs. explicit Cart Rule `sort_order`** — Discounts have a hard-coded chain; the merchant cannot reorder. Cart Rules expose `sort_order` per rule.

## Where it applies

The chain governs every discount-attachment moment on the platform:

- **Storefront cart updates** — adding / removing items, changing quantities, applying a code.
- **Storefront submit** — the snapshot frozen onto the [[order|Order]].
- **Admin order edit** on [[orders-details]] — quantity / line edits re-run the chain.
- **`orders-discount-add` action** — manually attaching a discount runs the chain against the existing order.

### Store-level uniqueness limits

- **Countdown discount** — only ONE can exist per store. Trying to create a second returns: *"Countdown discount already exists"*.
- **Per-product Quantity discount** — only ONE active quantity discount can target any given product. Validation: *"A volume discount with this product already exists"*.

These exist because the storefront UI shows a single countdown banner and a single tiered-price ladder per product — multiple would conflict visually.

### `order_over` winner selection — largest absolute saving wins

When multiple `order_over` Flat / Percent discounts qualify on the same cart, the cart-engine resolves the winner by **largest absolute saving** — whichever discount yields the bigger discount amount wins. (verify)

Example: *"10 EUR off over 50 EUR"* vs *"5 EUR off over 100 EUR"* on a 150 EUR cart → the 10 EUR rule wins (it yields 10 EUR saving vs 5 EUR). The `order_over` threshold is only used to gate **eligibility**, not to pick the winner.

The strict-greater subtotal check on `order_over`:

- Codeless `order_over` — **strict `<`** comparison (verify).
- Code-based `order_over` shipping codes — **inclusive `>=`** comparison (verify).

### Shipping-discount resolution — one per cart, first-match wins

The platform allows only **one shipping discount per cart**. The resolution iterates eligible shipping discounts in first-match order; the first match attaches and the rest are skipped. (verify) This is a separate path from the `order_over` winner-by-saving rule above — shipping discounts don't compete by amount.

### Order-level vs. line-level attachment

Discounts can attach at two scopes; the order's `discount_amount` total is the sum of all attached discounts (order-level + line-level):

- **Whole-order discounts** (Global with `settings = all` / `order_over`, shipping discounts, Code-based discounts targeting the whole cart, Countdown) — show as one action row at the order level on [[orders-details]].
- **Per-line discounts** (Fixed, Global targeting specific products / categories / vendors, Quantity tier on a specific product line) — show on the individual order-product line.

## Related

- [[discount-stacking]] — hub.
- [[discount-stacking-code-apply]] — the `code_apply` gate that runs at step 5.
- [[discount-stacking-cart-rules-interaction]] — Cart Rules layer on top of the chain.
- [[marketing-discounts-fixed]] — per-product Fixed; step 1.
- [[marketing-discounts-quantity]] — Quantity-tier; step 2.
- [[apps-up-cross-sell]] — Up-sell / Cross-sell; step 3.
- [[marketing-discounts-countdown]] — Countdown; step 4.
- [[marketing-discounts-flat]] / [[marketing-discounts-percent]] / [[marketing-discounts-shipping]] — whole-order discounts at step 5.
- [[discount]] — entity with `total_value`, `order_over`, `settings`.
- [[cart-rule]] — sibling engine with explicit `sort_order`.
- [[orders-details]] — order-level vs. line-level rows.
- [[cart]] / [[order]] — where the snapshot lands.

## Open Questions

None.
