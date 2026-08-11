---
type: entity
aliases: ["Payment status vs order status", "Payment status independence", "Payment status side effects", "Credit note gating", "Платежен статус срещу статус на поръчка"]
tags: [orders, payments, entity]
created: 2026-06-10
updated: 2026-06-10
source_count: 0
---

> Part of [[payment-status]]. See the hub for the other aspects (values, lifecycle, provider mappings).

# Payment Status vs Order Status

## Identity

This page covers the **single most important rule** about payment status: it is **independent of the order's `status`**. The two are separate columns that evolve on separate timelines. It also documents what *does* and *does not* key off payment status — credit-note and archive eligibility key off ORDER status, while the cascade of side-effects (stock decrement, customer email, webhook) fires when the PAYMENT saves as `completed`.

## Aliases

- "Payment vs order status" — the independence rule.
- "What 'paid' means" — informal merchant phrasing.
- Bulgarian: "Платежен статус срещу статус на поръчка".

## Key Attributes

### Independent of order status

The **single most important rule**: payment status is INDEPENDENT of the order's `status`. An order can be `completed` (workflow done) while the payment is `refunded` (money returned). A workflow rule on [[settings-statuses]] CAN tie the two — e.g., "when an order is moved to status `refunded`, mark the payment as refunded" — but at the data layer the two columns are separate. The merchant should always check BOTH when reasoning about an order's true state. The two status enums and how they interact at status-change time are detailed in [[order-status-workflow]].

### Credit-note eligibility checks order status, not payment status

The credit-note flow (per [[orders-credit]]) gates on the **order's** `status IN (cancelled, refunded)` AND the order has an `invoice_number`. It does NOT directly check payment status. So the merchant flow is: refund the payment (payment status → `refunded`) → set the order status to `refunded` → THEN credit-note becomes available.

### Archive eligibility checks order status only

Archiving an order (per [[orders-archive]]) is gated on order status (`completed` or `cancelled`) — not on payment status. So a refunded payment on a completed order can be archived; an order with a `completed` payment but `pending` order status cannot.

### Status set on save — the side-effect cascade

When the platform saves a payment with `status = completed`:

- An order-history row is written (visible in [[orders-history]]).
- The order's `email_sent` flag drives whether the "Paid" customer notification fires (per [[settings-statuses]] toggle).
- Stock is decremented for the order's products (if not already decremented at an earlier counted status) — see [[inventory-decrement-timing]].
- Discount uses counter increments (if the discount's counted-status set includes `paid`).
- The `order.updated` webhook fires (see [[settings-hooks]]).
- The order's overall `status` MAY auto-transition (e.g., `pending` → `paid`) via the platform's status mapping rules.

### Renaming a status doesn't change behaviour

The merchant can rename `completed` to "Paid in full" (or any custom label) via [[settings-statuses]] Payment tab — but the underlying enum value `completed` is unchanged. All gates ("refund button visible when payment is `completed`") continue to work because they check the enum, not the label.

### Where it does NOT cascade — `chargebacked`

Setting a payment to `chargebacked` records the bank's action but does **NOT** automatically reverse stock or fire customer notifications. To reverse stock / record the loss, the merchant must also move the **Order** status to `cancelled` or `refunded` — that triggers the cascade per [[order-status]] business rules. (The provider-side detail of how `chargebacked` and `disputed` are reached lives on [[payment-status-provider-mappings]].)

## Where it appears

- [[orders-details]] — shows both the order status and the payment status; merchants reason about an order using both.
- [[orders-credit]] — credit-note eligibility (gates on ORDER status).
- [[orders-archive]] — archive eligibility (gates on ORDER status).
- [[orders-history]] — records the order-history row written when a payment saves as `completed`.
- [[settings-statuses]] — Payment tab (rename labels) + workflow rules that can tie the two status enums.
- [[settings-hooks]] — `order.updated` webhook fires on payment-status change.

## Related

- [[payment-status]] — hub.
- [[order-status]] — the order's overall workflow status (the OTHER enum).
- [[order-status-workflow]] — how the two enums interact at status-change time.
- [[orders-credit]] — credit-note flow (gated by ORDER status).
- [[orders-archive]] — archive gating (also ORDER status).
- [[orders-history]] — the order-history audit row.
- [[settings-statuses]] — label rename + workflow rules.
- [[settings-hooks]] — webhook side-effect.
- [[inventory-decrement-timing]] — stock decrement triggered on `completed`.

## Open Questions

No outstanding questions.
