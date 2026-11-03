---
type: concept
nav_path: "Concept → Discount stacking"
route_name: ""
route_path: ""
aliases: ["Discount stacking", "Stacking discounts", "Combining discounts", "Cumulative discounts", "Promo stacking", "Discount cumulation", "Натрупване на отстъпки", "Стек на отстъпки", "Комбиниране на отстъпки", "Куп. отстъпки заедно"]
tags: [marketing, discounts, stacking, concepts]
plan_gates: []
created: 2026-05-23
updated: 2026-06-10
source_count: 6
---

# Discount stacking

## Definition

**Discount stacking** is the set of rules that decide what happens at checkout when more than one [[discount|Discount]] could apply to the same cart at the same time. CloudCart has **7 distinct discount types** (`flat`, `percent`, `shipping`, `fixed`, `quantity`, `countdown`, `code-pro`), and a single cart can be a candidate for several at once — e.g. a global percent-off, a fixed-price override on one product, a quantity-tier deal on another, a free-shipping coupon, and a countdown discount. **Container** is NOT a separate type — it's a percent/flat variant with `is_container = 1` (a code-grouping mode) surfaced as its own card in the type-picker. The stacking rules govern which of these attach, which get suppressed, and in what order they evaluate.

The single most important rule is the **`code_apply`** toggle on every code-based discount: it decides whether a promo code is REJECTED when the cart already has a discount applied (default `code_apply = 0`), or stacks on top (`code_apply = 1`, set per-discount, with an `apply_regular_price` modifier to re-evaluate against catalog rather than discounted price). See [[discount-stacking-code-apply]].

This concept is split into 7 aspect pages. The Assistant should drill into the aspect that matches the question, not read every page.

## Sub-pages (in this cluster)

- [[discount-stacking-code-apply]] — `code_apply = 0 / 1` toggle; `apply_regular_price` max-of-two modifier; shipping `order_over` always-applies carve-out.
- [[discount-stacking-evaluation-order]] — implicit priority chain (per-product Fixed → Quantity → Up-sell → Countdown → Global/Code → Cart Rules); store-level uniqueness limits; `order_over` winner = largest absolute saving.
- [[discount-stacking-cart-code-slots]] — `discount_code` vs `discount_container_code` cart-level mutual exclusivity; sequential Container consumption against parent `total_value` cap; parent's `code_apply` governs child redemption.
- [[discount-stacking-uses-counter]] — `uses` recomputed-from-scratch (not incremented) on every order status change; `discounts_used_statuses`; auto-decrement on cancel; Code PRO `SUM(uses)`; Container parent aggregate; `maxused_user`.
- [[discount-stacking-plan-gating]] — the 7 plan-feature counters (`discount_global`, `discount_coupon`, `discount_fixed`, `discount_quantity`, `discount-code-pro`, `discount-code-pro-generator`, `discount_labels`).
- [[discount-stacking-cart-rules-interaction]] — Cart Rules run AFTER Discounts; cart-level winner-takes-all (no `combine_rules` setting); product-level accumulate; `sort_order` only on Cart Rules.
- [[discount-stacking-cooldown-and-attachments]] — 10-min `active`-toggle cooldown (only no-code Flat/Percent/Shipping/Fixed with `is_code = 0` AND `is_container = 0`); per-product attachment regeneration; `force_save` persistence.

## Why it matters to the merchant

Stacking is the silent multiplier on every promotion. Six high-impact consequences:

- **`code_apply` default is reject.** A 10%-off newsletter coupon left at `code_apply = 0` silently fails for every customer who already has a Fixed-discounted product in the cart. See [[discount-stacking-code-apply]].
- **Shipping `order_over` always applies** — regardless of `code_apply = 0`. The most common merchant pitfall.
- **No user-controllable Discount priority** — the chain is hard-coded. Cart Rules have `sort_order`; Discounts don't. See [[discount-stacking-evaluation-order]].
- **`uses` auto-decrements on cancel / refund** — recomputed (not incremented), so cancelled orders **free the slot back up**. A campaign that hit `max_uses` accepts fresh redemptions as soon as orders get cancelled. See [[discount-stacking-uses-counter]].
- **Container codes are the ONLY way to stack codes** — typing two stand-alone codes overwrites; only a Container campaign accepts multiple codes in one cart. See [[discount-stacking-cart-code-slots]].
- **The 10-minute toggle cooldown** protects high-catalog stores — every active-flip rebuilds `product_to_discount` joins. Quantity / Countdown / Code PRO are NOT throttled. See [[discount-stacking-cooldown-and-attachments]].

## Scope

What this concept covers is split across the 7 sub-pages listed above: the `code_apply` toggle + `apply_regular_price` modifier + shipping `order_over` carve-out; the evaluation chain across the 7 discount types + Cart Rules; the cart's two code slots and the Container parent / child relationship; the `uses` / `max_uses` / `maxused_user` counter mechanics; the 7 plan-feature counters per type; the Cart Rules layer above Discounts; and the 10-minute cooldown + per-product attachment regeneration + `force_save` persistence.

What it does NOT cover:

- Per-type configuration screens for individual discount types — see each `marketing-discounts-*` feature page.
- The Code PRO multi-code campaign structure — see [[marketing-discounts-code-pro]].
- Container codes auto-generation — see [[marketing-discounts-codes]].
- How a discount is created or edited — see [[marketing-discounts]].
- Visual labels and banners (technically discount-type rows but don't reduce price) — see [[products-banners-labels]].
- The customer-side "from X / now Y" pricing display — that's a storefront / listing-engine topic.

## Contrasts

- **Stacking vs. cumulation** — "stacking" specifically refers to whether multiple discounts attach simultaneously. "Cumulation" (10% then 5% off the result) is NOT how CloudCart combines discounts; each discount computes against its own base. See [[discount-stacking-evaluation-order]].
- **Stacking vs. priority** — stacking decides WHETHER; priority decides WHAT ORDER. See [[discount-stacking-evaluation-order]].
- **Stacking vs. Cart Rules** — Discounts evaluate FIRST; Cart Rules see the post-discount cart total. See [[discount-stacking-cart-rules-interaction]].
- **Stacking vs. plan-gating per type** — plan-gating limits how many of each type can be created; stacking is the runtime checkout decision. See [[discount-stacking-plan-gating]].
- **`force_save` vs. stacking** — `force_save` is a *persistence* rule (keep attached on order edit), not a stacking rule. Required for `shipping` and `order_over`. See [[discount-stacking-cooldown-and-attachments]].

## Where it applies

The stacking rules govern every Discount-attachment moment on the platform. Each sub-page documents its own surface. The cross-cutting attachment surfaces are:

- [[checkout-flow]] — discounts evaluated during cart, applied at submit.
- [[cart]] — carries the attached-discounts list + the two code slots.
- [[order]] — snapshots the discounts that applied at submit time.
- [[orders-discount-add]] — admin "apply discount to order"; runs the same stacking rules.
- [[orders-details]] — order-level discounts as action rows, line-level on order-product lines.
- [[api-discounts]] — JSON-API v2 endpoint; identical enforcement at the checkout engine layer.

## Programmatic access

Stacking rules apply identically when discounts are created or updated via **JSON-API v2** — `code_apply`, `apply_regular_price`, `force_save`, and the cart-engine deduplication rules are enforced at the **checkout engine layer**, not the API write layer. A discount POSTed through [[api-discounts]] with `code_apply = 0` behaves exactly as one created in the admin panel. The merchant cannot bypass stacking rules by writing through the API. See [[api-discounts]], [[api-discount-codes]], [[api-discount-codes-pro]], [[json-api-v2]].

## Related

- [[discount]] — master entity carrying `code_apply`, `apply_regular_price`, `force_save`, `uses`, `max_uses`, `maxused_user`.
- [[discount-code]] — Container child-code entity.
- [[marketing-discounts]] — primary CRUD screen for all discount types.
- [[marketing-discounts-flat]] / [[marketing-discounts-percent]] / [[marketing-discounts-shipping]] / [[marketing-discounts-fixed]] / [[marketing-discounts-quantity]] / [[marketing-discounts-countdown]] / [[marketing-discounts-code-pro]] / [[marketing-discounts-codes]] — per-type feature pages.
- [[marketing-discounts-code-pro-generator]] — bulk code generator for Code PRO.
- [[marketing-discounts-code-pro-export]] — export Code PRO codes.
- [[marketing-discounts-products]] — per-product price overrides for Fixed discounts.
- [[cart-rule]] — entity that evaluates AFTER discounts.
- [[apps-cart-rules]] / [[apps-cart-rules-rules]] — Cart Rules feature pages.
- [[apps-up-cross-sell]] — Up-sell / Cross-sell with discount integration.
- [[cart]] — discount evaluation happens against the cart at checkout.
- [[order]] — orders snapshot the applied discounts at submit time.
- [[orders-discount-add]] — apply a discount to an existing order; runs stacking rules.
- [[orders-details]] — order-level vs. line-level rows.
- [[customer]] — `maxused_user` per-customer cap, `only_customer` registered-only gate.
- [[checkout-flow]] — full cart→order journey; discounts attach during cart, applied at submit.
- [[cart-vs-order-lifecycle]] — entity lifecycle for cart and order.
- [[order-status-workflow]] — statuses that drive whether the `uses` counter increments.
- [[plan-gates]] — per-type discount-counter plan-feature gates.
- [[settings-statuses]] — `discounts_used_statuses` setting that controls counted statuses.
- [[settings-hooks]] — `discount.*` webhook events fire on CRUD.
- [[geo-zone]] — region restriction on a discount (`geo_zone_id`).
- [[customer-group]] — `customer_groups[]` restriction.
- [[analytics-top-order-discounts]] / [[analytics-top-order-product-discounts]] — usage analytics.
- [[products-banners-labels]] — visual discount-type rows that don't reduce price.
- [[order-processing-pipeline]] — the discount-usage counter increment side-effect that fires after every status change.
- [[order-totals-pipeline]] — the order-of-operations: discounts apply at stage 2 (before shipping + VAT), each against its own base.

## Open Questions

No outstanding questions — all previously-flagged items resolved during this pass.
