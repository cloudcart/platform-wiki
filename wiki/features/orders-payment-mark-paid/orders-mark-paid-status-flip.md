---
type: feature
nav_path: "Orders → Order details → Payment → Mark as paid → Status flip rules"
route_name: admin.orders.payment.mark_paid
route_path: /admin/orders/action/payment/mark_paid/:payment_id
aliases: ["Mark-paid status flip", "Order status after mark paid", "Payment status precedence", "Split payment flip", "Manual flag skips recalc", "Reverse mark as paid"]
tags: [orders, payment, manual-payment, status, lifecycle]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[orders-payment-mark-paid]]. See the hub for the other aspects (form & visibility, post-paid pipeline, adjacent actions, API position).

# Mark as paid — order-status flip rules

## Purpose

Marking a payment completed flips the **payment** record unconditionally, but the **order's** status is then auto-recalculated by a precedence rule that inspects ALL payment records. This page documents the exact precedence (which is count-based, NOT amount-based), why a partial payment can flip the whole order to "paid", when the auto-recalc is skipped, how authorized payments interact, and how to reverse a mark-as-paid.

## Where to find it

The status flip is automatic on the order header in [[orders-details]] and the order's row in the [[orders]] list. The flip's traces appear in the [[orders-history]] timeline. When the auto-recalc is skipped (manual override), the order header keeps its prior status even though the payment record updated.

## What the merchant can do here

Recognise whether to expect an order-level flip after marking a payment paid, and — if the order was previously set manually — understand why the order status will NOT change. To bring the order in line, the merchant changes the status manually via [[orders-status-change]].

## Settings & fields

The auto-flip is not configurable per-action. Two factors determine the outcome:

| Factor | Effect |
|--------|--------|
| Count of payment records in each state | Decided by a fixed precedence (see below), NOT by the sum of paid amounts vs the order total. |
| Manual status override flag (`manual=1`) on the order | If set (merchant changed status via [[orders-status-change]]), auto-recalc is SKIPPED. |

## Business rules

### Order status auto-flip is precedence-based, NOT amount-based

Marking the payment as completed runs the platform's payment-status recalc. The new order status is decided by the COUNT of payment records in each state, with this precedence (first hit wins):

1. Any payment in `authorized` → order status `authorized`.
2. Any payment in `completed` → order status `paid` (or `completed` if fulfilment is already `fulfilled` AND the `order_complete` setting is enabled).
3. Any payment in `pending`/`initiated`/`requested`/`held` → order status `pending`.
4. Only after the four above are zero: chargebacked > refunded > voided > failed > cancelled > timeouted.

So on a split-payment order (e.g., partial COD + partial bank transfer) — once ONE of the two payments is marked as paid, the order's status flips straight to "paid", even if the second payment is still pending. The platform does NOT compare the sum of completed payments against the order total before flipping status. The merchant should be aware: mark-as-paid on a partial payment will declare the whole order paid in the eyes of the platform, and downstream notifications / invoice generation (see [[orders-mark-paid-pipeline]]) will fire.

### Auto-flip is SKIPPED when the order has `manual=1`

If the order's status was changed manually by an admin (via the status pill on [[orders-details]]), the platform sets a `manual` flag and STOPS auto-recalculating the status from payment events. So if the merchant manually flipped an order to "completed" first and THEN clicked Mark-as-paid, the order's status stays at "completed" (not "paid") — the payment record updates but the platform respects the manual override. Subsequent mark-as-paid / refund actions still update payment records but won't change the order status until the merchant clears the manual flag (typically by manually switching status again via [[orders-status-change]]).

### Status mapping precedence applies to authorized orders too

If the order has a payment in `authorized` state (pre-auth from one of the supported gateways — see [[orders-payment-capture]]), marking a SEPARATE offline payment record as paid does NOT release the auth. The auth-related rules (negative-status → cancel auth, fulfilment → capture auth) apply on the AUTHORIZED payment record only.

### Reversing a mark-as-paid — refund or status change

There is no dedicated "undo mark as paid" action. To reverse:

1. **For real refunds**: use the refund flow per [[orders-payment-refund]], which works only on online gateway payments.
2. **For correction (no real refund needed)**: change the order's status manually via the status pill (per [[orders-status-change]]) back to pending. The platform's no-state-machine design allows this transition, but the payment record stays at status=completed until the merchant clears it directly (which requires CloudCart support intervention).

## Related

- [[orders-payment-mark-paid]] — hub.
- [[orders-mark-paid-pipeline]] — the cascade whose status-recalc step this page details.
- [[orders-payment-capture]] — authorized payments and the auth release/capture rules.
- [[orders-payment-refund]] — the real-money reversal path.
- [[orders-status-change]] — manual status override (sets the `manual` flag that blocks auto-recalc).
- [[orders-details]] — order header shows the resulting status.
- [[orders]] — order list row shows the resulting status.
- [[orders-history]] — timeline of the status transition.
- [[order-processing-pipeline]] — the full status-transition pipeline.

## Open questions

None.
