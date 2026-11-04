---
type: concept
nav_path: "Concept → Discount stacking → uses counter"
aliases: ["uses counter", "max_uses", "maxused_user", "discounts_used_statuses", "Recomputed not incremented", "Auto-decrement on cancel", "Per-customer cap", "Code PRO uses aggregate", "Container discount uses"]
tags: [marketing, discounts, stacking, uses, counters, concepts]
plan_gates: []
created: 2026-06-10
updated: 2026-11-04
source_count: 3
---

> Part of [[discount-stacking]]. See the hub for the other aspects (code_apply toggle, evaluation order, cart code slots, plan gating, Cart Rules interaction, per-variant rows).

# Discount stacking — uses counter

## Definition

Every [[discount|Discount]] has a **`uses`** counter and (optionally) a **`max_uses`** cap. The counter governs whether the discount keeps attaching at checkout — once `uses >= max_uses`, the discount stops firing (even with the date window still open).

The most important property: **`uses` is recomputed from scratch on every order status change of any order using the discount, NOT incremented per redemption.**

The recompute counts every distinct order in one of the **counted statuses**, configured globally via the **`discounts_used_statuses`** setting on [[settings-statuses]]. The default counted statuses are:

- `paid`
- `completed`
- `fulfilled`

A merchant can add Cancelled or Refunded to the list, and those orders then count; `chargebacked`, `disputed`, `timeouted`, `failed` and `voided` are not selectable. A pending order that is marked fulfilled counts under the defaults. The total recount leaves out negative statuses for fulfilled orders; the per-customer count does not.

## Scope

Covered:

- The recompute-from-scratch model + the `discounts_used_statuses` setting.
- Auto-decrement on cancel / refund (recovers `max_uses` slots) under the default statuses.
- Symmetric re-count on recovering a cancelled order back to a counted status.
- The 10-second async delay on the recompute.
- Code PRO per-child recompute + parent `SUM(uses)` aggregation.
- The Container discount's own count; an individual code has no counter.
- `maxused_user` per-customer cap and what it counts.

Not covered here:

- The `code_apply` toggle — see [[discount-stacking-code-apply]].
- Container codes in the cart — see [[discount-stacking-cart-code-slots]].
- The plan-feature counters that limit how many discounts can exist — see [[discount-stacking-plan-gating]].

## Contrasts

- **Recomputed vs incremented** — most platforms increment a counter on every redemption. CloudCart recomputes from scratch on every status change of every order using the discount. The recompute is the **only** mechanism that updates `uses`.
- **`uses` vs `max_uses` vs `maxused_user`** — `uses` is the live count. `max_uses` is the cap across the whole discount. `maxused_user` is a per-customer cap that runs in parallel with `max_uses`.
- **Counted vs uncounted statuses** — controlled by the global `discounts_used_statuses` setting on [[settings-statuses]]. Default counted = `paid`, `completed`, `fulfilled`.
- **Code PRO vs Container counter semantics** — Code PRO recomputes **per code** individually, then sets the campaign's `uses = SUM(code.uses)`. A Container discount has its own `uses`, recounted like all others. An individual Container code has no counter, and an order does not use it up.

## Where it applies

- **Every order status change** (on [[orders-status-change]]) triggers the recompute on the affected discount(s). The recompute is dispatched **asynchronously with a 10-second delay**. It sends no webhook.
- **Checkout** reads `uses` against `max_uses` at attachment time — when `uses >= max_uses`, the discount becomes invisible to customers (no more attachments).
- **`maxused_user` per-customer cap** runs for logged-in customers, on codes at entry and on no-code Orders over and Countdown.
- **[[orders-discount-add]]** — adding a discount from the admin runs no customer limits.
- **Cancellation / refund / chargeback** — under the default statuses, the recompute drops `uses` by 1 for the cancelled order, freeing the slot back up (a discount that had hit `max_uses` becomes redeemable again).
- **Re-marking a cancelled order back to a counted status** — re-counts it (counter goes back up).

### Auto-decrement on cancel / refund — counter slot freed

Because the counter is recomputed (not incremented), cancelling a previously-counted order **automatically frees the slot back up**. A discount that had hit `max_uses` becomes redeemable again as soon as the order drops out of the counted-status set. Conversely, recovering a cancelled order back to a counted status re-counts it.

### Code PRO recompute — per-child + parent aggregate

Code PRO discounts run a per-child recompute on every status change of orders that used any Code PRO child. The parent Code PRO discount's `uses` is then set to `SUM(child.uses)` across all child codes. So one order status change triggers a per-code re-tally + a parent-aggregate update.

### Container `uses`

A Container discount recounts like all others, so cancelling a counted order frees a use on the Container discount. The individual code has no counter: it stays reusable until turned off or deleted, or until the Container's own `max_uses` is reached.

### `maxused_user` — per-customer cap

`maxused_user` counts this customer's uses on orders in counted statuses. On Code PRO it counts across the whole campaign. A cancelled order that was already fulfilled still counts here, though not in the total `uses` figure.

If the count reaches `maxused_user`, the code is refused for that customer with *"You have used this discount code the maximum number of times"* — other customers can still redeem. The limit is checked at code entry for logged-in customers.


### Counting is per-discount, not per-line

`uses` counts **discount-applied-to-order**, not line items. So a single order with a 10% code on top of a 20% Fixed discount counts once toward the code's `uses` and once toward the Fixed discount's `uses` — two separate counters.

## Related

- [[discount-stacking]] — hub.
- [[discount-stacking-code-apply]] — when a code and a product discount share a line, each has its own counter.
- [[discount-stacking-cart-code-slots]] — Container codes in the cart.
- [[discount-stacking-plan-gating]] — the orthogonal per-type plan counters.
- [[discount]] — entity with `uses`, `max_uses`, `maxused_user`.
- [[discount-code]] — Container code entity (no independent `uses`).
- [[order-status-workflow]] — decides whether an order counts.
- [[orders-status-change]] — the transition event that fires the async recompute.
- [[settings-statuses]] — `discounts_used_statuses` setting.
- [[customer]] — `customer_id` is the identity for `maxused_user`.
- [[marketing-discounts-code-pro]] — per-code `uses` + campaign `SUM(uses)` aggregation.
- [[marketing-discounts-codes]] — Container codes; no counter of their own.
- [[order-processing-pipeline]] — the full pipeline that fires the recompute on every status change.

## Open Questions

None.
