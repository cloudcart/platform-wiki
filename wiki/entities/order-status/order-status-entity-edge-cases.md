---
type: entity
nav_path: "Entity → Order Status → Edge cases & negative-status semantics"
aliases: ["Negative status semantics", "Fulfillment auto-reset", "Reversal lock", "Order locked after cancellation", "Auto-created return", "Authorization auto-cancel", "is_draft clearing", "Stock-decrement reversal skip"]
tags: [entity, orders, statuses, edge-cases, negative-flow]
created: 2026-06-10
updated: 2026-08-06
source_count: 3
---

> Part of [[order-status]]. See the hub for the other aspects (canonical values, relationships, custom statuses, side-effects, API access).

# Order Status — Edge cases & negative-status semantics

## Identity

Beyond the documented cascade (see [[order-status-entity-side-effects]]), a handful of verified backend behaviours fire on specific transitions. This aspect catalogues the negative-status shared rules (revenue exclusion, fulfillment reset, payment auth release), the auto-created return and the reversal lock that follows it, the credit-note gate, draft-meta clearing, and the stock-reversal edge case for deleted products.

## Aliases

- **Negative-status semantics** — the rules shared by the 7 negative statuses.
- **Fulfillment auto-reset** — `status_fulfillment` flips back to `not_fulfilled` on negative status.
- **Authorization auto-cancel** — pre-auth hold released on negative status.
- **Auto-created return** — a system return recorded when a committed sale is cancelled / refunded.
- **Reversal lock** — a cancelled / refunded order with a reversal on it can no longer change status.
- **Stock-reversal skip** — restock silently skips lines whose variant FK is NULL.

## Key Attributes

### Negative-status semantics — shared rules

The 7 negative statuses (`voided`, `timeouted`, `cancelled`, `failed`, `refunded`, `chargebacked`, `disputed`) share several rules:

- **Excluded from revenue / income / segment reports.** Analytics filters drop them from totals.
- **Reverse the discount usage counter.** Transitioning into a negative state from a counted state decrements `uses` and reopens the per-customer cap.
- **Trigger stock restore.** If the order had decremented stock, returning to a negative state restores it. See [[inventory-restock]].

### Negative status flip also resets fulfillment

When the merchant moves an order into ANY of the 7 negative statuses, the platform also resets `status_fulfillment` from `fulfilled` back to `not_fulfilled` in the same save. The merchant sees both fields change with one click. The fulfillment-cleared transition does NOT fire a separate webhook; it rides along with the status-change webhook. (verify)

### Negative-status side-effect also cancels payment authorisation

When entering a negative status AND there's an active payment with non-empty `authorize_amount` (a pre-auth hold), the platform invokes a cancel-authorisation call on the payment gateway to release the funds upstream. This is automatic. If the gateway call fails, the order's status still changes locally but the hold may not be released — the merchant has to manually contact the gateway. This is most visible on `authorized → voided` and `authorized → cancelled` transitions. (verify)

### Cancelling / refunding a committed sale auto-records a return

Moving an order to `cancelled` or `refunded` — and only those two of the seven negative statuses — auto-records a **system return** when the order was a committed sale (already invoiced, or coming from a positive status such as `paid`). It is created straight as `returned`, with source `refund`, created by the system, covering the remaining quantity. No credit note is needed and the record is idempotent. These are real return records, so they show up in return reporting even though no goods came back — see [[orders-returns-lifecycle]]. A cancel of a never-committed order records nothing.

### The reversal lock — a committed cancellation is one-way

Once that return record exists, or a credit number has been issued, the order's status is **locked**: the only change still accepted is a toggle between `cancelled` and `refunded`. Everything else — re-opening to `paid`, to `pending`, to a custom status — is refused with *"The order is locked after a cancellation/refund — its status can no longer be changed."*

There is **no** credit-number clearing on the way out. A merchant who cancels a paid or invoiced order by mistake cannot flip it back; they need a new order (or a debit note on the accounting side). A plain cancel of an unpaid, uninvoiced order has no reversal record and stays freely reversible.

The lock covers the order's status only. The order's **payments** stay changeable so the actual money refund can be processed, and a delayed gateway notification can still correct a spurious cancel — that recovery path does not run through this validation.

### Credit-note gate

Credit notes ([[orders-credit]]) can only be issued when (1) the order's status is `cancelled` OR `refunded`, AND (2) the order has an `invoice_number` already populated. Common workflow: invoice while `paid` → refund → status moves to `refunded` → issue credit note (gate now open).

### `is_draft` meta is cleared by status change

Whenever the merchant changes the status on a draft order via the dropdown, the platform explicitly deletes the `is_draft` meta entry from the order's meta table. So the FIRST status change on a draft order (typically `pending → cancelled` via the only available dropdown option for drafts) is what flips the order out of draft mode and into the normal lifecycle. The "Create order" button does the same thing via a different path. See [[order-status-entity-canonical-values]] for the draft sub-state mechanics. (verify)

### Stock-decrement reversal skips missing variants

If a product was deleted between the original `paid` decrement and a later `refunded` restore, no stock event runs for that line — the order line's variant FK is set to NULL on product delete, and the restore silently skips lines that reference missing variants. Re-enabling stock tracking on a previously-untracked product mid-cycle does NOT retroactively restore the original decrement. (verify)

### Why the dropdown shows only 6 built-ins

The dropdown excludes `chargebacked`, `disputed`, `timeouted`, `failed`, `voided` because those are **gateway-driven** — they fire only via payment-provider sync events, never via merchant action. The remaining 6 (`authorized`, `pending`, `paid`, `completed`, `cancelled`, `refunded`) are the merchant-pickable set. Custom statuses appear after these 6. See [[order-status-entity-canonical-values]] for the full taxonomy.

### Side-effect ordering reminder

The above side-effects fire as part of the broader cascade documented in [[order-status-entity-side-effects]] — they're not a separate pipeline. The fulfillment auto-reset happens as part of the single status-change save (one DB write), not as a follow-up update.

## Where it appears

- [[orders-details]] — the merchant sees fulfillment flip simultaneously with status on negative transitions.
- [[orders-history]] — records each side-effect in the same history row (one row per status change, not per side-effect).
- [[orders-credit]] — credit-note gate enforced here; issuing the credit note arms the reversal lock.
- [[orders-archive]] — archived orders bypass these rules (status-locked).
- [[orders-add]] — `is_draft = 1` set on admin-placed orders; cleared on first status change or "Create order".
- [[settings-hooks]] — single webhook fires even when multiple side-effects ride along.

## Related

- [[order-status]] — hub.
- [[order-status-entity-side-effects]] — the main cascade these edge cases ride within.
- [[order-status-entity-canonical-values]] — the draft sub-state + 11-value taxonomy.
- [[order-status-entity-api-access]] — API triggers the same edge cases.
- [[order-status-negative-semantics]] — sibling concept page in the workflow cluster.
- [[inventory-restock]] — the stock-restore mechanics that pair with negative-status flips.
- [[orders-credit]] — credit-note issuance; the credit number arms the reversal lock.
- [[orders-returns-lifecycle]] — the auto-created system return.

## Open Questions

None.
