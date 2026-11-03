---
type: concept
nav_path: "Concept → Order status workflow → Action gates"
aliases: ["Order action gates", "What can I do per status", "Edit gate", "Refund gate", "Invoice gate", "Credit note gate", "Mark as completed gate", "Cancel order gate"]
tags: [orders, statuses, gates, actions, concepts]
plan_gates: []
created: 2026-06-10
updated: 2026-08-06
source_count: 3
---

> Part of [[order-status-workflow]]. See the hub for the other aspects (taxonomy, custom statuses, transitions, auto-transitions, side-effects, negative semantics).

# Order status — action gates

## Definition

Separately from the rules that block certain *transitions* ([[order-status-transitions]]), the platform gates **what the merchant can do with the order at each step**. The status pill controls which buttons / actions appear on [[orders-details]] and which API calls succeed against [[api-orders]]. This page covers those surrounding actions — line-item edits, refund, invoice issuance, credit note, cancel — once the order is in a given state.

This page is the canonical reference for "which actions are available in which status".

## Scope

Covered:

- The action-availability table per status.
- The credit-note gate (status + invoice number combination).
- The refund gate (driven by payment status, not order status).
- The bulk-action UI vs the underlying endpoint.

Not covered here:

- The status taxonomy itself — see [[order-status-taxonomy]].
- The transitions that move the order between gates — see [[order-status-transitions]].
- The side-effects fired when a gated action is taken — see [[order-status-side-effects]].
- The credit-note issuance flow in detail — see [[orders-credit]].

## Contrasts

- **Action gate vs transition rule** — transitions ([[order-status-transitions]]) are blocked by five specific rules; actions are gated per current status, which is the tighter constraint.
- **Order-status-driven gate vs payment-status-driven gate** — Edit / Cancel / Mark as Completed / Issue credit note are gated by **order** status; **Refund** is gated by **payment** status ([[payment-status]]).
- **Credit-note gate (compound)** — requires BOTH the order to be in `cancelled` / `refunded` AND `invoice_number` to be populated. Either condition alone is insufficient.
- **UI bulk action vs underlying endpoint** — the bulk ribbon exposes only "Mark as completed"; the endpoint behind it accepts the same merchant-pickable set the dropdown shows, and rejects the 5 gateway-driven statuses.
- **Cancel that restocks vs cancel that doesn't** — Cancel is never refused for stock reasons; but a deleted product / `tracking = no` line is skipped silently, so the cancel succeeds with no stock returned.

## Where it applies

Action gates apply on every order-management surface — the per-order action buttons on [[orders-details]], the bulk ribbon on [[orders]], and the [[api-orders]] mutation endpoints. Same gates, three entry points.

### Action-availability table

| Action | Status required |
|--------|----------------|
| **Edit line items / customer / address** | `pending`, `paid`, `authorized` |
| **Mark as Paid** | Any non-paid status (typically `pending` / `authorized`); subject to payment-gateway readiness |
| **Capture authorisation** | `authorized` |
| **Refund** | `paid` (or any status where a payment record is in `completed` state — see "Refund gate" below) |
| **Mark as Completed** | `paid` **OR** `status_fulfillment = fulfilled` — either one is enough. Only an order that is *neither* is refused (auto-promotion handles the `paid` + `fulfilled` case if `order_complete = 1` — see [[order-status-auto-transitions]]) |
| **Cancel order** | Any status except `paid` / `completed`; not gated by stock — see [[order-status-transitions]] |
| **Issue invoice** | Any status with payment captured (varies by store invoicing settings on [[settings-invoicing]]) |
| **Issue credit note** | `cancelled` OR `refunded` AND `invoice_number` is populated — see [[orders-credit]] |
| **Issue receipt** | Any status with payment captured |
| **Any status change at all** | Blocked outright while the order is archived, and while it is a cancelled / refunded order carrying a return or credit number (the reversal lock) — see [[order-status-negative-semantics]] |
| **Bulk status change (from list)** | UI ribbon exposes "Mark as completed"; the endpoint accepts the merchant-pickable set only |

Once the order is `completed` or in a negative status ([[order-status-negative-semantics]]), much of the merchant's editing surface locks down.

### Refund gate — driven by payment status, not order status

The **refund button** is gated by the **payment** status (see [[payment-status]]), not the order status. So an order can technically be refunded from any status where a payment record exists in `completed` state — including `pending` if a payment has been captured separately, or `completed` if the merchant paid out before completing the order.

After a successful refund:

- Order's `status` is set to `refunded`.
- Order's discount uses decrement (if the discount was counted at `paid`).
- Stock is restored (if it was decremented at `paid`) — see [[inventory-restock]].
- Customer notification fires (if enabled per [[settings-statuses]]).
- `order.updated` webhook fires ([[settings-hooks]]).
- The merchant can then issue a credit note via [[orders-credit]] — the credit-note gate (status in `cancelled` / `refunded` + invoice number populated) is now satisfied.

### Credit-note gate

Credit notes ([[orders-credit]]) can only be issued when:

1. The order's `status` is `cancelled` OR `refunded`, **AND**
2. The order has an `invoice_number` already populated (i.e., an invoice was issued earlier).

Typical flow: issue the invoice while `paid` (populates `invoice_number`) → refund the order (status moves to `refunded`) → issue the credit note (gate now open). The credit note re-uses the order's invoice number as its credit-number reference per the [[settings-invoicing]] credit-note numbering scheme.

Once the credit note is issued, the order can no longer be re-marked `paid` at all — the reversal lock closes it to everything except a `cancelled` ↔ `refunded` toggle. See [[order-status-negative-semantics]].

### Cancel order — not gated by stock

No endpoint checks stock before cancelling. The only stock-related behaviour is cosmetic: the one-click **Cancel order** shortcut in the order's action menu is hidden when a line can no longer be given back cleanly — but the status pill still cancels the order, and the cancel succeeds.

What can happen silently is the restock: if the product on the order has been DELETED since the order was placed, or its `tracking` flag has been toggled to `no`, the stock-reverse step is skipped — the cancel succeeds but no stock is added back. See [[inventory-restock]].

The real refusals on Cancel are elsewhere: a `paid` or `completed` order cannot be cancelled (*"Only open orders can be canceled."* — refund it instead), an archived order cannot change status, and an order whose authorised payment is smaller than its total cannot change status at all, cancel included.

### Bulk-action UI vs underlying endpoint

The [[orders]] list's bulk action ribbon prominently shows **Mark as completed**. The bulk-status endpoint behind it validates against the **same merchant-pickable set the dropdown offers** — the 5 gateway-driven statuses (`chargebacked`, `disputed`, `timeouted`, `failed`, `voided`) are rejected with *"Invalid status"*, as is `abandoned` (not a status at all). So:

- Default merchant UI flow → only `completed` is reachable in bulk.
- Scripts / [[api-orders]] integrations → can drive the other merchant-pickable statuses, but not the gateway-owned ones.

Per-order changes for all other statuses currently require [[orders-details]] (the per-order pill) or [[orders-status-change]] (the dedicated flow).

### Useful examples

- **Credit note for a refunded order.** Order is `paid` with an invoice issued → merchant clicks **Refund** → status flips to `refunded` → the **Issue credit note** button on [[orders-credit]] is now enabled (status `refunded` + invoice number present).
- **Line-item edit lockout.** Adding a line to a `completed` order is refused (edits need `pending`, `paid`, or `authorized`). The merchant either moves the order back to `paid` (allowed — no rule blocks `completed → paid`, see [[order-status-transitions]]), edits, and re-marks `completed`; or cancels and creates a new order for the extra items. Note that "cancel and redo" is not available once a credit note or return exists on the order — the reversal lock has closed it.
- **Refund without invoice.** A refund on an order that never had an invoice succeeds (the refund gate is payment-driven), but the credit-note button stays disabled — the gate requires `invoice_number` populated. The merchant must issue an invoice first (itself possibly blocked per [[settings-invoicing]]), then the credit note.

## Related

- [[order-status-workflow]] — hub.
- [[order-status-transitions]] — how the status changes that drive gate availability.
- [[order-status-negative-semantics]] — the reversal lock that closes a committed cancellation / refund.
- [[order-status-side-effects]] — what fires when a gated action succeeds.
- [[orders-details]] — where the action buttons live.
- [[orders-credit]] — credit-note flow.
- [[orders-invoice]] — invoice issuance.
- [[orders-receipt]] — receipt issuance.
- [[payment-status]] — separate field that gates the refund button.
- [[settings-invoicing]] — invoice / credit-note numbering scheme.
- [[inventory-restock]] — stock-restore mechanics referenced by Cancel.
- [[api-orders]] — JSON-API v2 with the same gates applied.

## Open Questions

None.
