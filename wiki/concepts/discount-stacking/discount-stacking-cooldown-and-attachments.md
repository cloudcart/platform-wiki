---
type: concept
nav_path: "Concept → Discount stacking → Cooldown & attachments"
aliases: ["10-minute discount cooldown", "Active toggle cooldown", "last_status_change", "force_save", "Per-product attachment regeneration", "product_to_discount join", "From X now Y listing", "Discount CRUD storefront propagation"]
tags: [marketing, discounts, stacking, cooldown, attachments, concepts]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[discount-stacking]]. See the hub for the other aspects (code_apply toggle, evaluation order, cart code slots, uses counter, plan gating, Cart Rules interaction).

# Discount stacking — cooldown & attachments

## Definition

Two mechanisms protect the platform from Discount-related write storms:

- **The 10-minute toggle cooldown** — the merchant can only flip a discount's `active` flag once every 10 minutes. The cooldown applies **per discount, not per store**, and ONLY to no-code Flat / Percent / Shipping / Fixed discounts (the ones that materialise per-product attachments). All other types can be toggled freely. (verify)
- **The per-product attachment regeneration** — every Discount **create / update / delete** rebuilds the `product_to_discount` join table that feeds the storefront's "from X / now Y" listing display. For high-catalog stores (10,000+ products) this regeneration is the bottleneck on save-perf.

The third mechanism on this page, **`force_save`**, is a per-discount persistence flag that keeps the discount attached on order edit even when the cart no longer matches the conditions. It's required for `shipping` and `order_over` discounts because admin-side edits frequently disturb the line set that originally justified the discount.

## Scope

Covered:

- The 10-minute `active` toggle cooldown + which discount types it applies to.
- The `last_status_change` meta-data row that enforces the cooldown.
- The dev / CLI bypass behaviour of the cooldown.
- The per-product attachment regeneration on every Discount CRUD.
- The `force_save` persistence flag.
- Which discount types skip the regeneration (code-based discounts are no-op).

Not covered here:

- The runtime stacking toggle (`code_apply`) — see [[discount-stacking-code-apply]].
- The `uses` recomputation on order status changes — see [[discount-stacking-uses-counter]] (the recompute path is separate from the attachment regeneration path).
- The customer-side display of "from X / now Y" pricing — that's a storefront / listing-engine topic.

## Contrasts

- **Toggle cooldown vs `uses` recompute** — different async paths. The toggle cooldown protects the per-product attachment regeneration. The `uses` recompute fires on order status changes. They run on different queues. (verify)
- **`force_save` vs `code_apply`** — `force_save = 1` is a **persistence** rule (keeps the discount attached on edit). `code_apply` is a **stacking** rule (whether the discount can attach when others exist). They operate at different lifecycle moments and are independent.
- **Discount types with vs. without attachment regeneration** — Global, Fixed, Quantity, Countdown each materialise `product_to_discount` rows. Code-based discounts (Promo, Container, Code PRO) do NOT — they don't show on storefront listings, so the regeneration is a no-op.

## Where it applies

- **Discount-edit screen** active-toggle button — runs the 10-minute cooldown check.
- **Discount-create / -update / -delete** (admin or JSON-API v2) — fires the per-product attachment regeneration.
- **Order-edit** on [[orders-details]] — `force_save` decides whether the previously-attached discount stays when the cart no longer matches.
- **Storefront listing pages** — read the `product_to_discount` join to show "from X / now Y" prices.

### The 10-minute cooldown — which types it applies to

The cooldown stamp is set only for discounts where `type ∈ {flat, percent, shipping, fixed}` **AND** `is_code = 0` **AND** `is_container = 0`. (verify) So:

| Discount type | 10-min cooldown applies? |
|---|---|
| Global (no-code) Flat / Percent / Shipping / Fixed | **Yes** |
| Code-based Flat / Percent / Shipping coupon | **No** |
| Container code | **No** |
| Quantity discount | **No** |
| Countdown discount | **No** |
| Code PRO discount | **No** |

Practical implication: merchants can toggle a Quantity, Countdown, or Code PRO discount as often as they like; only the no-code "global" Flat / Percent / Shipping / Fixed discounts (the ones that materialise per-product attachments) are throttled — because those are the ones with the heavy `product_to_discount` regeneration cost.

### Cooldown error message + bypass

Within the cooldown window, attempting to toggle returns: *"You've already activated this discount. Please wait:minutes minutes in order to be able to deactivate it again."*

The cooldown is enforced via a `last_status_change` meta-data row stored per discount, compared against the current time minus 10 minutes (in UTC). The mechanism is **bypassed in development environments and command-line contexts** — the cooldown is a UI-protection feature, not a security guard. (verify)

### Per-product attachment regeneration — bottleneck on high-catalog stores

Beyond the toggle cooldown, the platform regenerates `product_to_discount` join rows on **every** Discount create / update / delete. This is what feeds the storefront's "from X / now Y" listing display — the regeneration ensures that newly-saved discounts immediately reflect on category pages and product detail pages.

For most discount types (Global, Fixed, Quantity, Countdown), the regeneration is the bottleneck on save-perf for high-catalog stores. For code-based discounts (Promo, Container, Code PRO), there's no per-product attachment because code-based discounts don't show on storefront listings — the regeneration is a no-op. (verify)

### `force_save` — persistence on order edit

`force_save = 1` keeps a discount attached to a previously-saved order even if admin-side edits make the cart no longer meet the conditions (e.g., removing the qualifying product from an order with a free-shipping-over-X discount). Without `force_save`, the discount detaches automatically when the merchant edits the order and the cart-condition fails.

The flag is **required** for `shipping` and `order_over` discounts because order-edit operations frequently disturb the line set that originally justified the discount. The merchant rarely toggles this manually — it's set by the platform when the discount is configured.

## Related

- [[discount-stacking]] — hub.
- [[discount-stacking-code-apply]] — runtime stacking toggle (independent of `force_save`).
- [[discount-stacking-uses-counter]] — `uses` recompute is a separate async path.
- [[discount-stacking-evaluation-order]] — `force_save` decides whether the discount stays in the chain on order edit.
- [[discount]] — entity carrying `force_save`, `is_code`, `is_container`, `last_status_change`.
- [[marketing-discounts]] — discounts CRUD; every save fires the regeneration.
- [[marketing-discounts-flat]] / [[marketing-discounts-percent]] / [[marketing-discounts-shipping]] / [[marketing-discounts-fixed]] — the four no-code types subject to the cooldown.
- [[marketing-discounts-quantity]] / [[marketing-discounts-countdown]] / [[marketing-discounts-code-pro]] — discount types **NOT** subject to the cooldown.
- [[orders-details]] — order-edit; `force_save` decides retention.
- [[api-discounts]] — JSON-API v2; same regeneration fires on API writes.
- [[background-queue-inventory]] — analogous queue concept for inventory; the discount-attachment regeneration is a sibling async pattern.

## Open Questions

None.
