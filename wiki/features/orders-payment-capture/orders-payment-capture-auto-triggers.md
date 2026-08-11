---
type: feature
nav_path: "Orders → Order details → Payment → Capture / Cancel → Automatic triggers"
route_name: admin.orders.payment.capture
route_path: /admin/orders/action/payment/capture-authorization/:payment_id
aliases: ["Fulfillment auto-capture", "Auto-capture on shipping", "Negative status auto-cancel authorization", "captureAutomaticAuthorization", "Capture without clicking"]
tags: [orders, payment, capture, authorization, fulfillment, automation]
plan_gates: ["authorize_payment"]
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[orders-payment-capture]]. See the hub for the other aspects (buttons & visibility, provider matrix, amount-exceeds rule, side effects, API access).

# Payment capture / cancel — automatic triggers

## Purpose

For most two-phase orders the merchant **never clicks Capture or Cancel manually**. The platform captures automatically when a fulfillment is added, and cancels automatically when the order moves to a negative status. This page documents both automatic paths and when the manual buttons are still needed.

## Where to find it

These triggers fire from the normal order workflow — the fulfillment / shipping action (see [[orders-shipping-waybill]]) and the order status pill (see [[orders-status-change]]) — not from the Capture / Cancel buttons themselves. The buttons on [[orders-details]] remain available for the cases the automation doesn't cover.

## What the merchant can do here

The merchant triggers these flows indirectly:

- **Ship the order** (mark a fulfillment as added) → the authorization is captured automatically (gateway-dependent).
- **Move the order to a negative status** (cancel / void / refund / etc.) → the authorization is cancelled automatically.

The merchant uses the manual **Capture** button only when they want to capture WITHOUT shipping.

## Settings & fields

### Fulfillment auto-captures the authorization (gateway-dependent)

When the merchant marks a fulfillment as added — i.e. ships the goods, per [[orders-shipping-waybill]] — the platform **automatically calls the gateway's capture-authorization API in the background**, provided:

- the gateway supports `captureAutomaticAuthorization`, AND
- the payment still has an open `authorize_amount`.

So for two-phase orders the merchant typically does NOT need to click Capture manually — shipping the order triggers it. The manual Capture button is mostly used when the merchant wants to capture WITHOUT shipping (e.g. custom-made goods being prepared, or digital licences activated outside the fulfillment flow).

### Negative-status flip auto-cancels the authorization

Conversely, when the order status moves to **any negative status** (cancelled, voided, refunded, failed, chargebacked, timeouted, disputed) AND the payment still has an open `authorize_amount`, the platform **automatically calls the gateway's cancel-authorization API**. So cancelling an authorized order via the status pill releases the hold without a separate Cancel-button click.

## Business rules

### When the manual buttons are still needed

| Scenario | Capture happens via |
|----------|---------------------|
| Normal order — ship then charge | Auto-capture on fulfillment add. |
| Capture without shipping (custom goods, digital licence) | Manual **Authorize `<amount>`** button. |
| Cancel an authorized order | Auto-cancel on negative-status flip (or the manual **Cancel authorization** button). |
| Gateway lacks `captureAutomaticAuthorization` | Manual Capture button only. |

### Side effects are the same as the manual path

Whether capture / cancel happens automatically or via the button, the resulting cascade (status flips, stock decrement, webhook, history actions) is identical — see [[orders-payment-capture-side-effects]].

### Amount-exceeds guard still applies

The auto-capture path is still subject to the authorized-amount cap. If the order was edited above the authorized amount, capture is blocked the same way — see [[orders-payment-capture-amount-exceeds]].

### Programmatic equivalent

Creating a fulfillment through JSON-API v2 on a two-phase order also triggers the indirect auto-capture — this is the one supported API path to capture funds. See [[orders-payment-capture-api-access]].

## Related

- [[orders-payment-capture]] — hub.
- [[orders-payment-capture-side-effects]] — the cascade these triggers produce.
- [[orders-payment-capture-amount-exceeds]] — the cap that auto-capture still respects.
- [[orders-payment-capture-api-access]] — the fulfillment-add indirect-capture API path.
- [[orders-shipping-waybill]] — the fulfillment / shipping action that auto-captures.
- [[orders-status-change]] — the negative-status flip that auto-cancels.
- [[api-order-fulfillment]] — writable resource; fulfillment add auto-captures.
- [[order-processing-pipeline]] — the authorise-then-capture trigger at fulfillment.

## Open questions

None.
