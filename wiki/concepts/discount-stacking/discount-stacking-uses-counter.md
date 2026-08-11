---
type: concept
nav_path: "Concept → Discount stacking → uses counter"
aliases: ["uses counter", "max_uses", "maxused_user", "discounts_used_statuses", "Recomputed not incremented", "Auto-decrement on cancel", "Per-customer cap", "Code PRO uses aggregate", "Container uses aggregate"]
tags: [marketing, discounts, stacking, uses, counters, concepts]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[discount-stacking]]. See the hub for the other aspects (code_apply toggle, evaluation order, cart code slots, plan gating, Cart Rules interaction, cooldown / attachments).

# Discount stacking — uses counter

## Definition

Every [[discount|Discount]] has a **`uses`** counter and (optionally) a **`max_uses`** cap. The counter governs whether the discount keeps attaching at checkout — once `uses >= max_uses`, the discount stops firing (even with the date window still open).

The most important property: **`uses` is recomputed from scratch on every order status change of any order using the discount, NOT incremented per redemption.** (verify)

The recompute counts every distinct order in one of the **counted statuses**, configured globally via the **`discounts_used_statuses`** setting on [[settings-statuses]]. The default counted statuses are:

- `paid`
- `completed`
- `fulfilled`

Orders in `cancelled` / `refunded` / `failed` / `voided` / `chargebacked` / `disputed` / `timeouted` (i.e., [[order-status-workflow]] `NEGATIVE_STATUS`) NEVER count toward the counter. This protects merchants from inflating discount usage on bogus or fraudulent orders.

## Scope

Covered:

- The recompute-from-scratch model + the `discounts_used_statuses` setting.
- Auto-decrement on cancel / refund (recovers `max_uses` slots).
- Symmetric re-count on recovering a cancelled order back to a counted status.
- The 10-second async delay on the recompute.
- Code PRO per-child recompute + parent `SUM(uses)` aggregation.
- Container parent uses aggregation; children consumed via `active = 0`.
- `maxused_user` per-customer cap and how guest emails interact with it.

Not covered here:

- The `code_apply` reject-on-conflict toggle — see [[discount-stacking-code-apply]].
- The Container parent / child structural relationship — see [[discount-stacking-cart-code-slots]].
- The plan-feature counters that limit how many discounts can exist — see [[discount-stacking-plan-gating]].

## Contrasts

- **Recomputed vs incremented** — most platforms increment a counter on every redemption. CloudCart recomputes from scratch on every status change of every order using the discount. The recompute is the **only** mechanism that updates `uses`. (verify)
- **`uses` vs `max_uses` vs `maxused_user`** — `uses` is the live count. `max_uses` is the cap across the whole discount. `maxused_user` is a per-customer cap that runs in parallel with `max_uses`.
- **Counted vs uncounted statuses** — controlled by the global `discounts_used_statuses` setting on [[settings-statuses]]. Default counted = `paid`, `completed`, `fulfilled`. Default uncounted = the negative-status set.
- **Code PRO vs Container counter semantics** — Code PRO recomputes **per child code** individually, then sets the parent's `uses = SUM(child.uses)`. Container aggregates redemptions against the parent only; individual child code rows don't carry an independent `uses` counter (the row is just "consumed", typically via `active = 0` after redemption, since each Container code is single-use). (verify)

## Where it applies

- **Every order status change** (on [[orders-status-change]]) triggers the recompute on the affected discount(s). The recompute is dispatched **asynchronously with a 10-second delay** on the `order-events6` queue. (verify)
- **Checkout** reads `uses` against `max_uses` at attachment time — when `uses >= max_uses`, the discount becomes invisible to customers (no more attachments).
- **`maxused_user` per-customer cap** runs at checkout, after the global cap check.
- **[[orders-discount-add]]** — manually attaching also runs the cap checks.
- **Cancellation / refund / chargeback** — the recompute drops `uses` by 1 for the cancelled order, freeing the slot back up (a discount that had hit `max_uses` becomes redeemable again).
- **Re-marking a cancelled order back to a counted status** — re-counts it (counter goes back up).

### Auto-decrement on cancel / refund — counter slot freed

Because the counter is recomputed (not incremented), cancelling a previously-counted order **automatically frees the slot back up**. A discount that had hit `max_uses` becomes redeemable again as soon as the order drops out of the counted-status set. Conversely, recovering a cancelled order back to a counted status re-counts it.

### Code PRO recompute — per-child + parent aggregate

Code PRO discounts run a per-child recompute on every status change of orders that used any Code PRO child. The parent Code PRO discount's `uses` is then set to `SUM(child.uses)` across all child codes. So one order status change triggers a per-code re-tally + a parent-aggregate update.

### Container `uses` — parent-only aggregate

Container parent discount aggregates redemptions against the parent. Individual child code rows don't carry an independent `uses` counter — the row is just "consumed" (typically via `active = 0` after redemption, since each Container code is single-use). (verify)

### `maxused_user` — per-customer cap

When `maxused_user` is set on a discount, the platform counts how many counted-status orders THIS customer (or guest email) has placed using the discount. If that count `>= maxused_user`, the code is rejected for that specific customer / email — but other customers can still redeem.

The count is per `customer_id`, not per email. Guest checkout typically creates ONE customer record per email (subsequent guest orders by the same email re-use the same `customer_id`), so the per-customer cap effectively applies to guest emails too — provided the platform was able to match the new guest order's email to an existing customer record. If two distinct customer rows somehow exist for the same email (data anomaly), each is counted separately.

### Counting is per-discount, not per-line

The `uses` counter increments by **discount-applied-to-order**, not by line-item. So a single order with a 10% coupon stacked on top of a 20% Fixed discount counts once toward the coupon's `uses` and once toward the Fixed discount's `uses` — two separate counters, both `+1`.

## Related

- [[discount-stacking]] — hub.
- [[discount-stacking-code-apply]] — `code_apply` is the gate; once allowed, both counters increment.
- [[discount-stacking-cart-code-slots]] — Container parent vs child structural relationship.
- [[discount-stacking-plan-gating]] — the orthogonal per-type plan counters.
- [[discount]] — entity with `uses`, `max_uses`, `maxused_user`.
- [[discount-code]] — Container child-code entity (no independent `uses`).
- [[order-status-workflow]] — drives whether the counter increments.
- [[orders-status-change]] — the transition event that fires the async recompute.
- [[settings-statuses]] — `discounts_used_statuses` setting.
- [[customer]] — `customer_id` is the identity for `maxused_user`.
- [[marketing-discounts-code-pro]] — per-child `uses` + parent `SUM(uses)` aggregation.
- [[marketing-discounts-codes]] — Container child codes; `active = 0` on consumption.
- [[order-processing-pipeline]] — the full pipeline that fires the recompute on every status change.

## Open Questions

None.
