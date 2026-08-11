---
type: concept
nav_path: "Concept → Inventory tracking → Restock on cancel / refund"
aliases: ["Inventory restock", "Stock return on cancel", "Stock return on refund", "Automatic restock", "Per-line decrement-tracking flag", "Re-credit semantics"]
tags: [catalog, inventory, stock, orders, cancellation, refund, concepts]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[inventory-tracking]]. See the hub for the other aspects (variant model, decrement timing, oversell, bundle stock, multi-warehouse, in-stock badge, debugging playbook).

# Inventory — restock on cancel / refund

## Definition

When an order moves **OUT of a decrementing status** (the merchant cancels, the customer charges back, a refund is issued, the order voids before capture, etc.), the platform **automatically returns** the previously decremented quantity to the affected Variant. There is **no separate "Restock" action** in the admin — restock is automatic on any negative-status transition.

The mechanism is a **per-line decrement-tracking flag** stored on each order's line items. When stock was decremented during the order's lifecycle, the line is flagged. When the order leaves the decrementing status, the platform reads the per-line flag and re-credits only the lines that were actually decremented. This prevents double-counting in adversarial sequences (cancel-then-mark-paid-then-cancel-again, etc.).

## Scope

Covered:

- The automatic-restock rule on negative-status transitions.
- The per-line decrement-tracking flag and what it prevents.
- The symmetric flow for re-decrement when the merchant re-marks a cancelled order as paid.
- Edge cases when the same order moves through multiple status transitions.

Not covered here:

- When the original decrement happens — see [[inventory-decrement-timing]].
- Refund money-movement audit (the financial side of refund) — see [[orders-credit]].
- How to investigate "stock returned unexpectedly" tickets — see [[inventory-debugging-playbook]].

## Contrasts

- **Automatic restock vs manual restock** — CloudCart has no manual "Restock" button. Stock return is purely a side-effect of status transitions. To restock manually, the merchant has to edit the Variant's `quantity` directly on [[products-inventory]] or the product editor — the Change log will then record the change with the admin's name as the Initiator (see [[inventory-debugging-playbook]]).
- **Per-line flag vs naive re-credit** — without the per-line flag, sequences like "cancel a `pending` order with setting = `paid`" would erroneously credit stock that was never decremented. The flag tracks whether each specific line was decremented, so the re-credit fires only when there's something to return.
- **Decrement IN vs re-credit OUT** — the two flows are symmetric. The same matrix that decides whether to decrement on transition IN (see [[inventory-decrement-timing]]) also decides whether to re-credit on transition OUT.

## Where it applies

Every status transition out of a decrementing state runs the re-credit check. Concrete examples:

- **Merchant cancels a `paid` order** → stock returned (the order WAS decrementing, so the cancel triggers re-credit).
- **Merchant cancels a `pending` order whose setting is "decrement at `paid`"** → no stock movement (nothing was ever decremented, nothing to return — the per-line flag stays `false`).
- **Merchant refunds a `completed` order** → stock returned.
- **Merchant re-marks a `cancelled` order as `paid`** → stock decrements again (the re-decrement path is symmetric — the per-line flag flips back to `true`).
- **Merchant cancels a `pending` order whose setting is "decrement at `pending`"** → stock returned (it was decremented at submit; the cancel reverses it).
- **Payment-gateway chargeback** → order status transitions to `chargebacked`; stock returns automatically.
- **Order auto-times-out** (payment gateway returns failure after the merchant's grace period) → status `timeouted`; stock returns if it was decremented.

### Negative statuses that trigger restock

All of these terminal / failure statuses re-credit any previously decremented stock on transition IN:

- `cancelled`
- `refunded`
- `voided`
- `failed`
- `chargebacked`
- `disputed`
- `timeouted`

Conversely, transitions BETWEEN these statuses (e.g. `cancelled → refunded`) do nothing — the stock was already credited back when the order first hit a negative state.

### Order-edit deletes a line — also restocks

When the merchant removes a line item from an order on [[orders-details]] (the "Remove" action on a product row), the platform restocks that Variant's quantity if the line had been decremented. Same per-line flag mechanism. See [[orders-products]] for the full per-line edit flow (`productRemove`, `productEdit`, `productAdd`) — each writes a corresponding entry to the product's [[products-change-log|Change log]] with `action = order` so investigations can trace the source.

### Refund vs partial refund — both restock

A full refund on a `paid` order restocks every line. A partial refund (refunding only some line items) restocks only the affected lines — the per-line flag is checked individually. The merchant doesn't pick "restock or not" — it's automatic per line per the per-line flag state.

## Related

- [[inventory-tracking]] — hub.
- [[inventory-decrement-timing]] — symmetric flow when stock comes off.
- [[inventory-oversell]] — when `continue_selling = yes`, re-credit goes from 0 to N normally (no clamp on credit, only on decrement).
- [[inventory-debugging-playbook]] — investigating "stock returned and we didn't do it" tickets.
- [[orders-details]] — per-order cancel / refund / void.
- [[orders-credit]] — credit-note / refund flow (financial side).
- [[orders-status-change]] — status transitions that fire restock.
- [[orders-products]] — line-item edits (`productAdd` / `productEdit` / `productRemove`) trigger restock.
- [[products-change-log]] — every restock writes a `variants.updated` entry on the product's Change log with the originating order as the Initiator.
- [[order-processing-pipeline]] — the full status-transition pipeline.

## Open Questions

None.
