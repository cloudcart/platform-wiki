---
type: feature
nav_path: "Orders → Order details → Payment → Refund → Partial refunds"
route_name: admin.orders.payment.refund
route_path: /admin/orders/action/payment/refund/:payment_id
aliases: ["Partial refund", "Refund partial amount", "Stripe dashboard partial refund", "PayPal dashboard partial refund", "order_payment_partially_refunded"]
tags: [orders, payment, refund, partial, webhook]
plan_gates: []
created: 2026-06-10
updated: 2026-07-24
source_count: 4
---

> Part of [[orders-payment-refund]]. See the hub for the other aspects (visibility, provider matrix, gateway quirks, side effects, status-flip rules, API access).

# Payment refund — partial refunds

## Purpose

CloudCart now has **two platform-side refund surfaces with different capabilities**. The standalone **Refund payment** button (see [[orders-payment-refund]]) is still **full-amount only** — it refunds the entire payment with no amount input. But the **order-return "refund to card"** flow — issued from a return on [[orders-details]] — **executes partial refunds through the gateway** for providers that support them (**Stripe, PayPal, Revolut, CloudCart Pay**): a full return refunds in full, a partial return refunds only the returned amount. A third path — the provider's own dashboard — remains the fallback for unsupported gateways, syncing back via webhook. This page explains all three, the history actions, and the reconciliation steps.

## Where to find it

- **Platform-side partial** — issue an **order-return** on [[orders-details]] and use its **refund-to-card** action; for Stripe / PayPal / Revolut / CloudCart Pay a partial return refunds only the returned amount through the gateway.
- **Standalone Refund button** — **full-amount only**, no partial input (see [[orders-payment-refund]]).
- **Gateway dashboard (fallback)** — for unsupported providers, issue the partial refund in the provider's own dashboard (Stripe Dashboard, PayPal Refunds UI, Mollie portal, etc.); the inbound state lands as action 21 in [[orders-history]] via webhook.

## What the merchant can do here

### Issue a partial refund via the gateway's dashboard

1. Open the payment provider's merchant dashboard (Stripe / PayPal / etc.).
2. Find the original charge / transaction.
3. Use the gateway's UI to issue a partial refund for the desired amount.
4. The gateway emits a webhook to CloudCart with the partial-refund event.
5. CloudCart records action 21 (`order_payment_partially_refunded`) in [[orders-history]].

### Manually reconcile the order

Because the refund is partial, the order's line items / totals don't automatically adjust. The merchant must:

1. Edit the order on [[orders-details]] to adjust line items or totals to reflect the partial refund.
2. Generate a credit note via [[orders-credit]] for the partial amount (for tax compliance).
3. Optionally send the credit note to the customer (the credit-note flow has a dedicated Send action that emails the customer — see [[orders-credit]]).

## Settings & fields

This page documents a flow that has no platform-side settings. The configuration lives in the gateway's dashboard (per-provider).

## Business rules

### The standalone Refund button is full-amount only

The **Refund payment** button (on the payment — see [[orders-payment-refund]]) passes the payment to the gateway's refund API with **no amount parameter** — the gateway is asked to refund the FULL payment amount. The merchant cannot specify a partial sum from this button; there is no amount field on it. To refund only part of an order, use an **order-return** (below).

### Platform-side partial refunds via an order-return

Issuing a **return** on an order ([[orders-details]]) exposes a **"refund to card"** action that refunds through the gateway **matched to the return's scope**: a **full** return calls the gateway's full refund; a **partial** return calls its **partial refund** (only the returned amount). The card option is shown only when the gateway supports that mode:

- **Partial-refund-capable** (full AND partial): **Stripe, PayPal, Revolut, CloudCart Pay**.
- **Full-only or unsupported**: Mollie, PayU, Mokka, Klear, COD, and others — a partial return hides the card option and the merchant falls back to a **bank-transfer** payout (recording the gateway id in `refund_reference`) or the gateway dashboard.

This is the platform-side partial-refund path — for the capable providers the merchant no longer needs the gateway dashboard. Unlike a webhook / dashboard partial, a return **does** restock and adjust the order's returned totals. The [[apps-aftercare|Withdraw-from-contract]] app feeds partial withdrawals straight into this flow — see [[aftercare-order-return-sync]].

### History actions 20 / 21

- Action 20 (`order_payment_refunded`) — a **full** refund (the standalone Refund button, or a full order-return card refund).
- Action 21 (`order_payment_partially_refunded`) — a **partial** refund reported by the gateway.

The old rule that *"no platform-side button produces a partial refund"* **no longer holds**: the order-return refund flow issues partial refunds directly for the capable providers (above). A partial refund can therefore originate either from a **CloudCart order-return** or from the **gateway's own dashboard** (synced back via webhook).

### Partial refund does NOT auto-flip the order

When action 21 arrives via webhook, the local payment status does NOT flip to `refunded` (because the payment isn't fully refunded). The order status does NOT auto-flip to `refunded` either. The history entry records the partial-refund event but the order continues to show its prior status until the merchant either:

- Issues additional partials until the cumulative refund equals the full amount (each partial logs an action 21), then manually marks the order refunded.
- Adjusts the order's payment / line totals manually via [[orders-details]].

### Refund button is hidden after a full refund

The Refund button only appears when the payment status is `completed`. Once a full refund has flipped the payment to `refunded`, the button is gone — the platform does NOT allow a "second refund" attempt via this UI. For any subsequent partial-refund flow, the merchant uses the provider's dashboard.

So the typical multi-step partial-refund flow looks like:

1. Issue partial refund #1 in gateway dashboard → action 21 logs.
2. Issue partial refund #2 in gateway dashboard → action 21 logs.
3. Merchant manually adjusts the order in CloudCart to reflect the cumulative refund.

### Stock is NOT auto-restored on partial

The PaymentSync stock auto-restore (see [[orders-payment-refund-side-effects]]) fires when the local payment status flips to `refunded`. A partial refund via **webhook / gateway dashboard** does NOT change the local payment status (it stays `completed`), so stock auto-restore does NOT fire — the merchant manually decrements / re-adds stock per the partial-refund line items. (A partial refund issued via an **order-return** is different: the return itself restocks its returned lines and adjusts the order totals.)

### Provider-specific partial-refund support

Platform-side partial refunds (via the order-return flow) are wired for **Stripe, PayPal, Revolut, and CloudCart Pay**. Other gateways (Mollie, PayU, Mokka, Klear, …) are full-only or unsupported on the platform side — for those a partial refund is still done in the provider's own dashboard and synced back via webhook. BNPL / COD providers generally do not support refunds at all — see [[orders-payment-refund-provider-matrix]].

## Related

- [[orders-payment-refund]] — hub.
- [[orders-returns]] / [[orders-returns-refunds]] — the order-return flow that issues platform-side partial refunds.
- [[orders-payment-refund-side-effects]] — what fires on a (full) refund — partial does NOT cascade.
- [[orders-payment-refund-status-flip-rules]] — order status logic (partial refunds don't auto-flip).
- [[orders-history]] — action 21 lands here.
- [[orders-credit]] — credit-note flow used to document partial refunds for tax.
- [[orders-details]] — manual order-edit surface for reconciliation.
- [[settings-hooks]] — inbound webhook surface.
- [[payment-providers-cloudcart-pay-transactions]] — example provider that surfaces partial state.

## Open questions

None.
