---
type: concept
nav_path: "Concept → Discount stacking"
route_name: ""
route_path: ""
aliases: ["Discount stacking", "Stacking discounts", "Combining discounts", "Cumulative discounts", "Promo stacking", "Discount cumulation", "Натрупване на отстъпки", "Стек на отстъпки", "Комбиниране на отстъпки", "Куп. отстъпки заедно"]
tags: [marketing, discounts, stacking, concepts]
plan_gates: []
created: 2026-05-23
updated: 2026-11-04
source_count: 6
---

# Discount stacking

## Definition

**Discount stacking** is the set of rules that decide what happens at checkout when more than one [[discount|Discount]] could apply to the same cart at the same time. Discounts are stored as `flat`, `percent`, `shipping`, `fixed`, `quantity` or `code-pro`, and a single cart can be a candidate for several at once — e.g. a global percent-off, a fixed-price override on one product, a quantity-tier deal on another, a free-shipping code, and a countdown discount. **Countdown** is a flat or percent discount with timer settings, and **Container** is a flat or percent discount with `is_container = 1`; each has its own card in the type-picker. The stacking rules govern which of these apply, which are left out, and in what order they evaluate.

The single most important rule is the **`code_apply`** toggle on a code-based discount: it decides what happens to lines that already hold a product discount. Off (default `code_apply = 0`), an Orders-over code, a free-shipping code or a Code PRO code is refused at entry, while a code for every product or a specific target is accepted and skips those lines. On (`code_apply = 1`), the code also applies to them, with an `apply_regular_price` modifier that compares the code with the current discounted price. See [[discount-stacking-code-apply]].

This concept is split into 8 aspect pages. The Assistant should drill into the aspect that matches the question, not read every page.

## Sub-pages (in this cluster)

- [[discount-stacking-amount-by-target]] — what a flat or percent amount comes off for each target, with and without a code, and what happens when it is larger than the cart.
- [[discount-stacking-code-apply]] — `code_apply = 0 / 1` toggle: which codes are refused and which skip discounted lines; `apply_regular_price` comparison.
- [[discount-stacking-evaluation-order]] — the fixed chain (one product discount per line → line-level code → Cart Rules → order-level discounts → free shipping); threshold boundaries; `order_over` winner = highest threshold passed.
- [[discount-stacking-cart-code-slots]] — `discount_code` vs `discount_container_code` cart-level mutual exclusivity; Container codes as one store-wide pool; the highest Container total wins.
- [[discount-stacking-uses-counter]] — `uses` recomputed-from-scratch (not incremented) on every order status change; `discounts_used_statuses`; auto-decrement on cancel; Code PRO `SUM(uses)`; the Container discount's own count.
- [[discount-stacking-plan-gating]] — what the admin form, JSON-API v2 and GraphQL check on create; the plan-feature keys (`discount_global`, `discount_coupon`, `discount_fixed`, `discount_quantity`, `discount-code-pro`, `discount-code-pro-generator`, `discount_labels`).
- [[discount-stacking-cart-rules-interaction]] — Cart Rules run after product discounts and line-level codes, before order-level discounts; cart-level winner-takes-all (no `combine_rules` setting); product-level accumulate; `sort_order` only on Cart Rules.
- [[discount-stacking-product-rows]] — the per-variant rows behind listing prices: which discounts create them and when they rebuild; `force_save` on order edit.

## Why it matters to the merchant

Stacking is the silent multiplier on every promotion. Six high-impact consequences:

- **`code_apply` is off by default.** A 10%-off newsletter code for every product, left at `code_apply = 0`, comes off only the lines with no product discount; if every line holds one, nothing comes off and no message shows. An Orders-over code is refused outright. See [[discount-stacking-code-apply]].
- **A free-shipping code follows `code_apply` at entry.** With the switch off and a discounted line, it is refused. If the discounted product is added after the code is in the cart, free shipping stays. A no-code free-shipping discount has no switch.
- **No user-controllable Discount priority** — the chain is hard-coded. Cart Rules have `sort_order`; Discounts don't. See [[discount-stacking-evaluation-order]].
- **`uses` auto-decrements on cancel / refund** — recomputed (not incremented), so cancelled orders **free the slot back up**. A campaign that hit `max_uses` accepts fresh redemptions as soon as orders get cancelled. See [[discount-stacking-uses-counter]].
- **Container codes are the ONLY way to have several codes in one cart** — typing two stand-alone codes overwrites; Container codes accumulate. See [[discount-stacking-cart-code-slots]].
- **The Active switch takes effect immediately**, any number of times, on every discount type. It sends no webhook and starts no rebuild of per-variant rows. See [[discount-stacking-product-rows]].

## Scope

What this concept covers is split across the 8 sub-pages listed above: what an amount comes off for each target; the `code_apply` toggle + `apply_regular_price` modifier; the evaluation chain across discount types + Cart Rules; the cart's two code slots and Container codes; the `uses` / `max_uses` / `maxused_user` counter mechanics; the plan-feature keys and create checks; where Cart Rules sit among discounts; and the per-variant rows + `force_save`.

What it does NOT cover:

- Per-type configuration screens for individual discount types — see each `marketing-discounts-*` feature page.
- The Code PRO multi-code campaign structure — see [[marketing-discounts-code-pro]].
- Container codes auto-generation — see [[marketing-discounts-codes]].
- How a discount is created or edited — see [[marketing-discounts]].
- Visual labels and banners (technically discount-type rows but don't reduce price) — see [[products-banners-labels]].
- The customer-side "from X / now Y" pricing display — that's a storefront / listing-engine topic.

## Contrasts

- **Stacking vs. cumulation** — "stacking" refers to whether multiple discounts apply to the same cart. On one line they compound: a 10% code on a line already 20% off takes 10% off the discounted price, unless `apply_regular_price` is on. Order-level discounts are calculated on the subtotal after line reductions and share that one base among themselves. See [[discount-stacking-evaluation-order]].
- **Stacking vs. priority** — stacking decides WHETHER; priority decides WHAT ORDER. See [[discount-stacking-evaluation-order]].
- **Stacking vs. Cart Rules** — Cart Rules evaluate after product discounts and line-level codes and see that total; order-level discounts come after them. See [[discount-stacking-cart-rules-interaction]].
- **Stacking vs. plan-gating per type** — plan checks decide whether a discount can be created; stacking is the runtime checkout decision. See [[discount-stacking-plan-gating]].
- **`force_save` vs. stacking** — `force_save` is a *persistence* switch (keep attached on order edit), not a stacking rule, and it is the merchant's own choice. See [[discount-stacking-product-rows]].

## Where it applies

The stacking rules govern every Discount-attachment moment on the platform. Each sub-page documents its own surface. The cross-cutting attachment surfaces are:

- [[checkout-flow]] — discounts evaluated during cart, applied at submit.
- [[cart]] — carries the attached-discounts list + the two code slots.
- [[order]] — snapshots the discounts that applied at submit time.
- [[orders-discount-add]] — admin "apply discount to order"; no stacking switch and no customer limits. It refuses an order that already has an order-level discount.
- [[orders-details]] — order-level discounts as action rows, line-level on order-product lines.
- [[api-discounts]] — JSON-API v2 endpoint; identical enforcement at the checkout engine layer.

## Programmatic access

Stacking rules apply identically when discounts are created or updated via **JSON-API v2** — `code_apply`, `apply_regular_price`, `force_save`, and the cart-engine deduplication rules are enforced at the **checkout engine layer**, not the API write layer. A discount POSTed through [[api-discounts]] with `code_apply = 0` behaves exactly as one created in the admin panel. The merchant cannot bypass stacking rules by writing through the API. See [[api-discounts]], [[api-discount-codes]], [[api-discount-codes-pro]], [[json-api-v2]].

## Related

- [[discount]] — master entity carrying `code_apply`, `apply_regular_price`, `force_save`, `uses`, `max_uses`, `maxused_user`.
- [[discount-code]] — Container and Code PRO code entity.
- [[marketing-discounts]] — primary CRUD screen for all discount types.
- [[marketing-discounts-flat]] / [[marketing-discounts-percent]] / [[marketing-discounts-shipping]] / [[marketing-discounts-fixed]] / [[marketing-discounts-quantity]] / [[marketing-discounts-countdown]] / [[marketing-discounts-code-pro]] / [[marketing-discounts-codes]] — per-type feature pages.
- [[marketing-discounts-code-pro-generator]] — bulk code generator for Code PRO.
- [[marketing-discounts-code-pro-export]] — export Code PRO codes.
- [[marketing-discounts-products]] — per-product price overrides for Fixed discounts.
- [[cart-rule]] — entity evaluated after product discounts and line-level codes, before order-level discounts.
- [[apps-cart-rules]] / [[apps-cart-rules-rules]] — Cart Rules feature pages.
- [[apps-up-cross-sell]] — Up-sell / Cross-sell with discount integration.
- [[cart]] — discount evaluation happens against the cart at checkout.
- [[order]] — orders snapshot the applied discounts at submit time.
- [[orders-discount-add]] — apply a discount to an existing order; runs no stacking switch.
- [[orders-details]] — order-level vs. line-level rows.
- [[customer]] — `maxused_user` per-customer cap, `only_customer` registered-only gate.
- [[checkout-flow]] — full cart→order journey; discounts attach during cart, applied at submit.
- [[cart-vs-order-lifecycle]] — entity lifecycle for cart and order.
- [[order-status-workflow]] — statuses that decide whether an order counts in `uses`.
- [[plan-gates]] — per-type discount-counter plan-feature gates.
- [[settings-statuses]] — `discounts_used_statuses` setting that controls counted statuses.
- [[settings-hooks]] — `discount.*` webhook events fire on CRUD.
- [[geo-zone]] — region restriction on a discount (`geo_zone_id`).
- [[customer-group]] — `customer_groups[]` restriction.
- [[analytics-top-order-discounts]] / [[analytics-top-order-product-discounts]] — usage analytics.
- [[products-banners-labels]] — visual discount-type rows that don't reduce price.
- [[order-processing-pipeline]] — the discount-usage recount that fires after every status change.
- [[order-totals-pipeline]] — the order-of-operations: discounts apply at stage 2 (before shipping + VAT).

## Open Questions

No outstanding questions — all previously-flagged items resolved during this pass.
