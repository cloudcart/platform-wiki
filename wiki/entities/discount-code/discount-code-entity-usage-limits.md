---
type: entity
nav_path: "Entity → Discount Code → Usage limits"
aliases: ["Code usage cap", "max_uses", "uses counter", "Code redemption limit", "Counted-status increment", "Лимит на употреба на код", "Брояч на код"]
tags: [entity, marketing, discounts, codes]
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[discount-code]]. See the hub for the other aspects (two-table model, customer binding, lifecycle, API access).

# Discount Code — usage limits

## Identity

This aspect covers how many times a Discount Code can be redeemed — the `max_uses` / `uses` cap, what counts as a redemption, and the difference between Container and Code PRO counter behavior. The non-obvious part: **cancelled / refunded orders behave differently depending on code type** — Code PRO auto-frees a slot, Container does not.

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

The `uses` counter increments only when an order using the code reaches one of the **counted statuses** (per the `discounts_used_statuses` setting — default: `paid`, `completed`, `fulfilled`). Orders that fail (`failed`, `cancelled`, `refunded`, `chargebacked`) do NOT consume a slot — they free the code back up for the next customer. This prevents fraud-protection delays from "wasting" a one-time code.

### Code PRO `uses` counter — recomputed, not incremented

For Code PRO codes, the `uses` counter is **NOT incremented** on each new order. Instead it is **recomputed** on every order-status change by counting all counted-status orders that currently reference this code. Practical effect: cancelled or refunded orders **auto-decrement** the counter (because they no longer count toward the recompute), unlike Container codes where the counter is incremented at order-placement and not decremented on cancellation.

Merchant-visible consequence: if a customer redeems a Code PRO discount, then the merchant cancels the order, the Code PRO `uses` counter goes back down. The customer's `maxused_user` cap also frees up. For Container codes, the cancellation does NOT auto-decrement.

### The four interacting caps

A code has up to four caps that all check independently — the cart engine checks ALL applicable caps before letting the customer redeem:

1. **Per-code `max_uses`** — this specific code's total redemptions.
2. **Per-Discount `usage_limit`** — the overall parent Discount's total redemptions (across all codes).
3. **Per-customer `usage_limit_customer`** (parent Discount) — how many times one customer can use the discount across any code.
4. **Per-code per-customer cap** (Code PRO `maxused_user`) — for Code PRO, how many times one customer can use THIS specific code.

The per-customer cap on the parent Discount prevents the same customer from redeeming the code multiple times even when `max_uses` allows it. Customer-identity matching for caps 3 and 4 is by customer ID — see [[discount-code-entity-customer-binding]].

## Where it appears

- [[marketing-discounts-code-pro]] — Code PRO management; exposes `max_uses`, `maxused_user` per code.
- [[marketing-discounts-codes]] — Container codes; inherit `max_uses` / `maxused_user` from the parent.
- [[marketing-discounts]] — the parent Discount edit form exposes `usage_limit` and `usage_limit_customer`.
- [[orders-details]] — order-status transitions are what drive counter increments / recomputes.

## Related

- [[discount-code]] — hub.
- [[discount]] — parent Discount; carries `usage_limit` and `usage_limit_customer`.
- [[order]] — counted-status transitions drive the counter.
- [[discount-stacking]] — how a capped code interacts with other discounts in the same cart.

## Open Questions

None.
