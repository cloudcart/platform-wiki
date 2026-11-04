---
type: entity
nav_path: "Entity → Discount Code → Usage limits"
aliases: ["Code usage cap", "max_uses", "uses counter", "Code redemption limit", "Counted-status increment", "Лимит на употреба на код", "Брояч на код"]
tags: [entity, marketing, discounts, codes]
created: 2026-06-10
updated: 2026-11-04
source_count: 3
---

> Part of [[discount-code]]. See the hub for the other aspects (two-table model, customer binding, lifecycle, API access).

# Discount Code — usage limits

## Identity

This aspect covers how many times a Discount Code can be redeemed — the `max_uses` / `uses` cap, what counts as a redemption, and the difference between Container and Code PRO codes. Cancelling a counted order frees a use on the discount, Container discounts included. An individual Container code has no counter.

## Aliases

- **Use cap** / **Redemption limit** — the maximum number of times a code can be redeemed.
- **Uses counter** — the running tally of redemptions.
- **Counted statuses** — the order statuses that consume a slot.

## Key Attributes

### Single-use vs multi-use per `max_uses`

- `max_uses = 1` → the code burns after the first redemption (one-time use across all customers).
- `max_uses = N` (N > 1) → the code can be redeemed up to N times total across all customers.
- `max_uses = null` → unlimited (the parent Discount may still have its own overall cap).

### Counted-status increments — cancelled orders don't burn a slot

The `uses` counter counts an order only when it is in one of the **counted statuses** (per the `discounts_used_statuses` setting — default: `paid`, `completed`, `fulfilled`). With the default set, orders that fail (`failed`, `cancelled`, `refunded`, `chargebacked`) do NOT consume a slot — they free the code back up for the next customer. A merchant can add Cancelled or Refunded to the list, and those orders then count. This prevents fraud-protection delays from "wasting" a one-time code.

### `uses` counter — recomputed, not incremented

The `uses` counter is **NOT incremented** on each new order. Instead it is **recomputed** on every order-status change by counting all counted-status orders that currently reference the discount or Code PRO code. Practical effect: cancelled or refunded orders **auto-decrement** the counter under the default statuses, on Container discounts too.

An individual Container code has no counter: an order does not use it up, and it stays reusable until turned off or deleted, or until the Container's own `max_uses` is reached. `maxused_user` is counted separately: a cancelled order that was already fulfilled still counts there.

### The interacting caps

The limits are `max_uses` and `maxused_user` on the discount, and the same pair on each Code PRO code:

1. **Per-code `max_uses`** (Code PRO) — this specific code's total redemptions.
2. **Discount `max_uses`** — the discount's total redemptions, enforced on every kind of code.
3. **Discount `maxused_user`** — how many times one logged-in customer can use it.
4. **Code PRO `maxused_user`** — the same limit on a Code PRO code; it counts across the whole campaign.

Customer-identity matching for the per-customer caps is by customer ID. See [[discount-code-entity-customer-binding]].


## Where it appears

- [[marketing-discounts-code-pro]] — Code PRO management; exposes `max_uses`, `maxused_user` per code.
- [[marketing-discounts-codes]] — Container codes; the Container discount carries `max_uses` / `maxused_user`.
- [[marketing-discounts]] — the Discount edit form exposes `max_uses` and `maxused_user`.
- [[orders-details]] — order-status transitions drive the recount.

## Related

- [[discount-code]] — hub.
- [[discount]] — carries `max_uses` and `maxused_user`.
- [[order]] — counted-status transitions drive the counter.
- [[discount-stacking]] — how a capped code interacts with other discounts in the same cart.

## Open Questions

None.
