---
type: feature
nav_path: "Orders → Order details → Payment → Capture / Cancel → Side effects"
route_name: admin.orders.payment.capture
route_path: /admin/orders/action/payment/capture-authorization/:payment_id
aliases: ["Capture side effects", "Cancel side effects", "Capture cascade", "Capture history actions", "Btepos loyalty split call", "BoricaWay4 retry idle", "No email on capture"]
tags: [orders, payment, capture, authorization, side-effects, webhook, history]
plan_gates: ["authorize_payment"]
created: 2026-06-10
updated: 2026-08-06
source_count: 4
---

> Part of [[orders-payment-capture]]. See the hub for the other aspects (buttons & visibility, provider matrix, amount-exceeds rule, automatic triggers, API access).

# Payment capture / cancel — side effects on success

## Purpose

Catalogues what changes when a Capture or a Cancel succeeds at the gateway — status flips, stock movement, webhook, history actions — plus the per-provider quirks (loyalty split-call, retry behaviour) and the deliberate no-customer-email gap.

## Where to find it

Triggered by a successful Capture or Cancel call from [[orders-details]] (per [[orders-payment-capture-buttons]]). The cascades below run AFTER the gateway returns success. They are observed in [[orders-history]] and the order header — there are no per-action toggles on this surface.

## What the merchant can do here

This page documents automatic behaviour. The merchant observes the outcomes (status badge, stock change in the product [[products-change-log|Change log]], history timeline) but cannot toggle individual side effects on this surface.

## Settings & fields

### Side effects on Capture success

- Payment status: Authorized → **Completed**.
- Order status: typically `pending` → `paid` (per platform rules; see [[settings-statuses]]).
- The standard payment-sync recalc runs, including **stock decrement** / fulfillment workflows depending on configuration.
- `order.updated` webhook fires (see [[settings-hooks]]).
- An entry appears in the order's [[orders-history]] timeline.

### Side effects on Cancel success

- Payment status: Authorized → **Cancelled** / **Voided**.
- Order status: typically `pending` → `cancelled` (per platform rules; depends on whether the order itself should cancel or just the payment void).
- `order.updated` webhook fires.
- **Stock is restored** if any was reserved.
- An entry appears in the order's [[orders-history]].

### History action codes

| Action | When |
|--------|------|
| 49 (`order_authorized`) | The initial authorization event. |
| 45 (`order_paid`) | Typically follows a successful Capture (status flips to paid). |
| 40 (`order_voided`) | A Cancel that voids the order. |
| 35 (`order_cancelled`) | A Cancel that cancels the order. |

The merchant can audit who captured / cancelled, and when, in [[orders-history]].

## Business rules

### No customer email on capture success

The capture handler updates the payment status and runs the standard payment-sync recalc + stock decrement. **No direct customer notification line is emitted by the capture handler itself.** If the customer is notified, it is because the order's status moved to "paid" and the status-change email was allowed through by the order's `notify_customer` flag, the template's own active flag and the store-wide `customer_email_notifications` switch — there is no per-status toggle. A merchant with any of those off will not send the customer anything on capture. The same applies to Cancel — any customer email is a side effect of the resulting status change, not the capture / cancel action.

The customer's gateway-side notifications (a card processor's receipt email, etc.) may still arrive based on the customer's own gateway settings, independent of CloudCart.

### Btepos and BoricaWay4 split the call when loyalty was used

For **Btepos / BoricaWay4** specifically, if the original purchase used a loyalty / points portion (recorded in the provider's `merchantOrderParams` + `attributes` data), the capture / cancel makes **TWO sequential gateway calls** — one for the loyalty order, one for the cash portion. If one succeeds and the other fails, the platform throws the second-call error; the loyalty portion may already be captured / cancelled while the cash portion isn't. When the outcome looks partial, the merchant should check the gateway's own dashboard to reconcile.

### Retry behaviour — BoricaWay4 has built-in idle retry

**BoricaWay4** capture / cancel / refund calls go through a `retryIdle` helper — if the gateway returns an idle / timeout response, the platform retries the call automatically before giving up. Other gateways do NOT retry — a single failure is final and the merchant must click Capture / Cancel again.

### Success-message reuse — intentional convention

Capture returns the toast *"Payment synced successfully"*; Cancel returns *"Payment refunded successfully"*. These messages are reused from other flows. The wording can mislead support staff reading the source, but the underlying gateway calls (capture vs cancel) are distinct and correct.

## Related

- [[orders-payment-capture]] — hub.
- [[orders-payment-capture-buttons]] — the actions that trigger these cascades.
- [[orders-payment-capture-auto-triggers]] — the automatic capture / cancel paths that produce the same side effects.
- [[orders-history]] — where actions 49 / 45 / 40 / 35 land.
- [[settings-statuses]] — the status-notification config that decides whether the customer is emailed.
- [[settings-hooks]] — `order.updated` webhook.
- [[products-change-log]] — where the capture's stock decrement is logged.
- [[order-processing-pipeline]] — the paid / negative-status side-effect cascade.

## Open questions

None.
