---
type: feature
nav_path: "Orders → Order details → Payment → Refund → Status flip rules"
route_name: admin.orders.payment.refund
route_path: /admin/orders/action/payment/refund/:payment_id
aliases: ["Refund order status flip", "Order status after refund", "Multi-payment refund", "Manual override blocks refund flip", "Split deposit refund"]
tags: [orders, payment, refund, status, lifecycle]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[orders-payment-refund]]. See the hub for the other aspects (visibility, provider matrix, gateway quirks, side effects, partial refunds, API access).

# Payment refund — order status flip rules

## Purpose

After a refund succeeds, the **payment record** flips to `refunded` unconditionally — but whether the **order itself** flips to `refunded` depends on a conditional auto-recalc that inspects ALL payment records on the order and a manual-override flag. This page documents the exact conditions under which the order's status auto-flips, why it sometimes doesn't, and how multi-payment / split-deposit orders behave.

## Where to find it

The status flip is automatic on the order header in [[orders-details]] and the order's row in the [[orders]] list. When the flip succeeds, an action 43 (`order_refunded`) entry appears in [[orders-history]]. When the flip does NOT happen, only the payment-level action 20 appears — the order header still shows the prior status.

## What the merchant can do here

Recognise whether to expect an order-level flip after refunding, and (if needed) manually change the order status via [[orders-status-change]] to bring it in line.

## Settings & fields

The auto-flip is not configurable per-refund. Two factors determine the outcome:

| Factor | Effect |
|--------|--------|
| Other completed / authorized / pending payments on the order | If any remain, the order does NOT flip. |
| Manual status override flag on the order | If set (merchant changed status via [[orders-status-change]]), auto-recalc is SKIPPED. |

## Business rules

### Order auto-flips to `refunded` only when all payments are reversed

When the refund succeeds, the platform recalculates the order's status from ALL payment records. The order flips to `refunded` ONLY when **all four** of these are true:

- No payments are in `authorized` state.
- No payments are in `completed` state.
- No payments are in pending states.
- At least one payment is `refunded`.

So if the order has TWO payments (e.g., a split deposit + balance) and only ONE is refunded, the order's status stays at `paid` (because the other is still `completed`). The merchant must refund BOTH payments for the order to flip to `refunded`. This applies to:

- Multi-currency orders with separate payment records per currency.
- Split-deposit orders (deposit + balance).
- Any scenario where the order has more than one OrderPayment record.

### Manual status override blocks auto-flip

If the merchant previously changed the order's status manually via the status pill (per [[orders-status-change]]), the platform sets a `manual` flag and the auto-recalc is SKIPPED. So refunding a payment on a manually-set order leaves the order's status as whatever the merchant chose — the **payment** record updates (and the per-payment side-effects of [[orders-payment-refund-side-effects]] still fire), but the **order's** status does NOT auto-flip to `refunded`.

To bring a manually-overridden order's status in line with the refund, the merchant changes the status again via [[orders-status-change]], explicitly choosing `refunded`. This will re-record a new manual entry.

### Action 43 — when it fires

Action 43 (`order_refunded`) lands in [[orders-history]] **only** when the conditional auto-flip succeeds. So:

- Single-payment fully-refunded order, no manual override → action 20 + action 43 both fire.
- Multi-payment order where only one payment refunded → action 20 fires; action 43 does NOT (yet).
- Manually-overridden order → action 20 fires; action 43 does NOT (auto-recalc skipped).

The merchant looking for "did the order itself flip?" should look for action 43 specifically.

### Partial refunds never auto-flip

A partial refund (action 21 — see [[orders-payment-refund-partial-refunds]]) does NOT change the local payment's status from `completed` to `refunded` — so the order's auto-recalc never runs. The order's status stays at whatever it was before the partial refund.

### Re-mark-paid behaviour after refund

If after a refund the merchant re-marks a payment as `completed` (via [[orders-payment-mark-paid]] or a webhook), the recalc runs again — the order can flip back out of `refunded` if the conditions stop holding. The status field is recomputed on every payment event, not latched.

### Refund cascade across multi-payment orders

The merchant doing batch refunds on a multi-payment order should expect:

1. Refund payment #1 → payment #1 flips, order stays at `paid` (because payment #2 still `completed`).
2. Refund payment #2 → payment #2 flips, order auto-flips to `refunded`. Action 43 fires.

Or, if the merchant decided to keep payment #2 (e.g., refunding only the deposit), the order stays at `paid` indefinitely — which is correct, because the order isn't fully reversed.

## Related

- [[orders-payment-refund]] — hub.
- [[orders-payment-refund-side-effects]] — payment-level cascade (always fires on refund).
- [[orders-payment-refund-partial-refunds]] — partial refunds never auto-flip the order.
- [[orders-status-change]] — manual status override (blocks auto-recalc).
- [[orders-payment-mark-paid]] — re-mark flow that can flip status back out of `refunded`.
- [[orders-history]] — action 43 entry indicates the order-level flip.
- [[orders-details]] — order header shows the resulting status.
- [[order-processing-pipeline]] — full status-transition pipeline.

## Open questions

None.
