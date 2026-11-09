---
type: feature
nav_path: "Payment Providers → myPOS → Refund, capture & sync"
route_name: apps.mypos.overview
route_path: /admin/payment-providers/mypos
aliases: ["myPOS refund", "myPOS Refund API", "myPOS Trnref", "myPOS sync", "myPOS GetPaymentStatus", "myPOS reconciliation", "myPOS capture mode", "myPOS auto-capture", "Възстановяване myPOS"]
tags: [paymentproviders, payment-providers, mypos, refund, sync, capture, reconciliation]
plan_gates: []
created: 2026-06-10
updated: 2026-11-09
source_count: 3
---

> Part of [[payment-providers-mypos]]. See the hub for related aspects (setup & config pack, payment lifecycle, save card).

# myPOS — Refund, capture & sync

## Purpose

This aspect covers the post-purchase money-movement and reconciliation surface for myPOS: **full refunds** through myPOS's Refund API, the **Sync payment** status check that settles payments the webhook didn't deliver, and the **capture mode** (single-message auto-capture only — no pre-authorize / delayed-capture). These are the behaviours support reaches for when a merchant asks "how do I refund a myPOS order?" or "why is this payment still Pending?".

## Where to find it

A refund is triggered from the order details Refund action (see [[orders-payment-refund]]); there is no refund control on the myPOS settings screen. Sync runs when the merchant clicks **Sync payment** on the order's payment row ([[orders-mark-paid-adjacent-actions]]); there is no automatic periodic check for myPOS. The myPOS settings page itself (see [[mypos-setup-config-pack]]) intentionally has no Authorization row because there is no two-phase capture surface.

## What the merchant can do here

- **Refund a myPOS payment in full** from the order details page — see [[orders-payment-refund]].
- **Click Sync payment** on a payment stuck in Requested / Pending to ask myPOS for its result.
- **Understand that myPOS captures immediately** — there is no separate "capture later" step to perform.

## Settings & fields

This aspect exposes no settings of its own. Refunds use the full payment amount (no amount input is rendered). The capture mode is fixed (auto-capture). The myPOS field layout lives on [[mypos-setup-config-pack]].

## Business rules

### Refund support

Full refunds call myPOS's `Refund` API endpoint with the original `Trnref` (transaction reference) and amount. After myPOS confirms, the platform marks the payment `Refunded`. Partial refunds are protocol-supported but **no amount input is exposed in the admin UI today** — refunds use the full payment amount.

### Capture mode — auto-capture only

myPOS's Virtual Checkout integration on CloudCart is **single-message capture only** — there is no pre-authorize / delayed-capture surface today. A capture entry point exists in code but is treated as the standard purchase complete-flow, not a delayed-capture step. This is why the myPOS settings page has no Authorization row (see [[mypos-setup-config-pack]]). Plan-gate-irrelevant.

### Sync — on request, not periodic

The sync flow calls myPOS's `GetPaymentStatus` API with the `OrderID` to reconcile statuses that the webhook didn't deliver. Unlike Fibank or Stripe, myPOS has **no automatic per-payment check and no timeout**: a payment that got neither the notification nor the shopper's return stays `Requested`, and its order stays `pending`, until the merchant clicks **Sync payment** (or changes the order status by hand). If myPOS answers with an error (for example, it has no payment for that Order ID), the sync shows that error and the payment is left as it was.

The reconciled `PaymentStatus` maps to the platform's [[payment-status]] the same way as the live webhook path (see [[mypos-payment-lifecycle]] for the full mapping table):

| myPOS `PaymentStatus` | Mapped |
|---|---|
| `1` | `Completed` |
| `2` | `Pending` |
| anything else | `Canceled` |

So a payment that completed at myPOS but whose IPN never reached CloudCart flips to `Completed` on the merchant's Sync; one myPOS reports in any other state becomes `Canceled`, which cancels the order ([[payment-status-vs-order-status]]).

## Related

- [[payment-providers-mypos]] — hub.
- [[payment-status]] — Completed / Pending / Canceled / Refunded mapping.
- [[orders-payment-refund]] — initiates a full refund through myPOS from the order details page.
- [[orders-payment-manual]] — manual payment entry (offline / outside myPOS).

## Open questions

_None._
