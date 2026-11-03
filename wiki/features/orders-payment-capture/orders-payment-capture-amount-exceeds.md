---
type: feature
nav_path: "Orders → Order details → Payment → Capture / Cancel → Amount-exceeds rule"
route_name: admin.orders.payment.capture
route_path: /admin/orders/action/payment/capture-authorization/:payment_id
aliases: ["Order amount exceeds authorized", "Capture blocked amount mismatch", "Edited order after authorization", "Authorized amount cap", "Capture danger alert"]
tags: [orders, payment, capture, authorization, validation]
plan_gates: ["authorize_payment"]
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[orders-payment-capture]]. See the hub for the other aspects (buttons & visibility, provider matrix, side effects, automatic triggers, API access).

# Payment capture — order amount exceeds authorized

## Purpose

The one concrete failure case the platform actively surfaces through the `allow_capture_authorization` string state: when an order has been **edited after authorization** so that its total now EXCEEDS the originally-authorized amount, the platform refuses to capture and explains why. The same guard also blocks the merchant from side-stepping the cap via a manual status change.

## Where to find it

On [[orders-details]], in the **Payment action row** of an Authorized order whose `price_total` is now greater than the authorized payment amount. Instead of the Capture button, the merchant sees a **danger alert**.

## What the merchant can do here

When the gap exists, the merchant has two valid paths:

1. **Edit the order down** to fit within the authorized amount (remove products, reduce shipping, or add a discount that closes the gap), then capture.
2. **Cancel the authorization** and request a fresh payment for the new, higher amount.

The merchant CANNOT capture, and CANNOT manually flip the status to Paid, while the total exceeds the authorized amount.

## Settings & fields

### The danger alert

When the order's `price_total` is GREATER than the originally-authorized amount, the Capture button is replaced by a danger alert reading:

> *"The order amount is `<total>` and cannot exceed the authorized payment `<authorized>`."*

This is driven by the **string state** of the `allow_capture_authorization` property (see [[orders-payment-capture-buttons]] for the full 3-state model). The button stays hidden **even if the provider supports capture** — this rule is enforced platform-side, not at the gateway.

## Business rules

### Why the gap appears

This typically happens when the merchant edits the order after authorization — adds products, increases shipping, or adds discounts that don't fully cover the increase. Pre-auth reserved a fixed amount; a card authorization cannot be captured for MORE than it reserved, so the platform blocks the over-capture rather than letting the gateway reject it.

### Capturing _less_ is the normal supported path

The block triggers **only when the order total exceeds** the hold. The opposite — **down-capture** — is fully supported and needs no cancel / re-charge: if the order is edited **below** the authorized amount (e.g. the picked weight is lower — see [[orders-payment-capture]]), Capture stays available and charges the **reduced** total, not the original hold. This is exactly how variable-weight orders (groceries, deli, meat / fish) avoid a small refund.

### The block also applies to status changes — not just the Capture button

When the merchant tries to change the order's status via the status pill (see [[orders-status-change]]) or via bulk-update on [[orders]], the **same `allow_capture_authorization` check runs**. If the order's total exceeds the authorized amount, the status change is REJECTED with the same error message. The merchant cannot "side-step" the gap by manually flipping the status to Paid — they must either bring the total down or cancel the auth and re-charge.

### Resolution paths summary

| Situation | Resolution |
|-----------|------------|
| Order edited up by a small amount | Edit the order back down to ≤ authorized amount, then capture. |
| New total is genuinely higher and must stand | Cancel the authorization, ask the customer to re-pay the new amount. |
| Merchant tries to force-flip status to Paid | Blocked with the same error; not a valid workaround. |

## Related

- [[orders-payment-capture]] — hub.
- [[orders-payment-capture-buttons]] — the `allow_capture_authorization` 3-state property (this is the string state).
- [[orders-status-change]] — manual status change, which the same guard blocks.
- [[orders]] — bulk status update, also subject to the guard.
- [[orders-details]] — where the danger alert renders.

## Open questions

None.
