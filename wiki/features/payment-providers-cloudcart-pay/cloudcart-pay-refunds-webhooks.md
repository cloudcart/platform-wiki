---
type: feature
nav_path: "Settings → Payment methods → CloudCart Pay → Refunds & payment updates"
route_name: apps.cloudcart_pay.overview
route_path: /admin/payment-providers/cloudcart_pay
aliases: ["CloudCart Pay refunds", "CloudCart Pay partial refund", "CloudCart Pay webhooks", "CloudCart Pay status mapping", "CloudCart Pay order stuck in requested", "CloudCart Pay refunded status", "Връщане на пари CloudCart Pay", "Частично възстановяване CloudCart Pay"]
tags: [paymentproviders, payment-providers, cloudcart-pay, refunds, webhooks]
plan_gates: []
created: 2026-06-10
updated: 2026-10-06
source_count: 2
---

> Part of [[payment-providers-cloudcart-pay]]. See the hub for the other aspects (account model, activation gate, checkout flow, express checkout, Apple Pay domain, saved card) and the six tabs.

# CloudCart Pay — refunds & payment updates

## Purpose

What happens to a CloudCart Pay payment after the shopper pays: how full and partial refunds are made, how payment notifications keep the order's payment status current, and the background check that closes payments nobody finished. It is the page for "can I refund part of an order?", "I refunded but the transaction still says Succeeded" and "why is the order stuck in requested?".

## Where to find it

- **Full refund** — the **Refund payment** button on the order ([[orders-payment-refund]]).
- **Partial refund** — an order return refunded to the card ([[orders-returns]], [[orders-payment-refund-partial-refunds]]), or a partial withdrawal in the **Withdraw from contract** app ([[apps-aftercare]]).
- The result shows on the order and on the [[payment-providers-cloudcart-pay-transactions|Transactions tab]]. Payment notifications and the background check run on their own and have no screen.

## What the merchant can do here

- **Refund a whole payment** from the order.
- **Refund part of a payment** through a return, and refund further parts later.
- **See the refunded amount** on the Transactions tab (**Partially Refunded** / **Refunded**).
- **Rely on automatic status updates** — no manual sync is needed.

## Settings & fields

None. The refund amount comes from the return, or is the whole payment for the **Refund payment** button.

## Business rules

### Full refund

**Refund payment** on the order refunds the whole payment through CloudCart Pay. When the refund succeeds, the payment's status becomes **Refunded** (see [[payment-status]]). A refusal is shown as *"CloudCart Pay refund error: <reason>"*.

### Partial refund

CloudCart Pay supports partial refunds. They are made from an **order return** whose refund goes back to the card: a partial return refunds only the returned amount, a full return refunds the whole payment. The **Withdraw from contract** app uses the same partial refund for a partial withdrawal.

- After a partial refund the payment **stays Completed** and the order status does not change; the rest of the payment can be refunded later in further parts.
- Errors: *"CloudCart Pay partial refund error: <reason>"* or *"CloudCart Pay partial refund failed: <status>"*.
- The standalone **Refund payment** button has no amount field; it always refunds in full.

On the [[payment-providers-cloudcart-pay-transactions|Transactions tab]] the payment then shows **Partially Refunded**, or **Refunded** once the refunded amount reaches the payment amount. The payment platform keeps the payment itself as succeeded and records the refund next to it, which is why the tab works out the refund label from the refunded amount — see [[cloudcart-pay-transactions-status-amount]].

### Payment notifications

CloudCart receives payment notifications for all CloudCart Pay stores at one platform address. A notification is accepted only when it is authentic and recent. It is treated as a signal only: CloudCart reads the payment's current state from CloudCart Pay and updates the order from that. Notifications come for a completed checkout, an authorized or captured payment, a successful payment and a failed attempt. There is no notification for a refund, a cancellation or an expired session; refunds made from CloudCart update the payment directly.

The same notification address carries account events too; those become the account alerts described in [[ccpay-onboarding-review-alerts]].

### How the payment status is set

| State of the payment at CloudCart Pay | Payment status on the order |
|---|---|
| Paid / checkout complete | Completed |
| Processing, or waiting for the shopper (e.g. 3-D Secure) | Pending |
| Session expired | Timed out |
| Cancelled | Cancelled |
| Declined and the session can no longer be paid | Failed |
| Declined but the session is still open | Unchanged — the shopper can retry |

A payment that is already **Completed** is never moved back, and completing it happens only once — even if the notification, the shopper's return from the bank page and the background check all arrive at the same moment. Stock, invoices and saved cards are therefore processed once.

### Background check: orders no longer stay "requested"

When a payment starts, a background check is scheduled. It looks at the payment **10 minutes** later, then every **5 minutes**, and updates the status as in the table. If the payment is still open **3 hours** after it started, it is closed as **timed out**, so the order no longer sits in "requested". The payment session itself stays payable for 2 hours (see [[cloudcart-pay-checkout-flow]]).

### Daily statistics

CloudCart compiles daily CloudCart Pay statistics per store for its own team. There is no merchant screen for them.

## Related

- [[payment-providers-cloudcart-pay]] — hub.
- [[orders-payment-refund]] — the full refund from the order.
- [[orders-payment-refund-partial-refunds]] — partial refunds across payment methods.
- [[orders-returns]] — returns that refund to the card.
- [[apps-aftercare]] — withdrawals that can refund part of a payment.
- [[payment-providers-cloudcart-pay-transactions]] — where refunds show.
- [[cloudcart-pay-transactions-status-amount]] — how the refund labels are worked out.
- [[payment-status]] — payment status definitions.
- [[cloudcart-pay-checkout-flow]] — the payment session.

## Open questions

- Whether support can force a status refresh of a single CloudCart Pay payment from the order page (no such action was found for CloudCart Pay).
- How a refund made outside CloudCart (for example by CloudCart Pay's own team) reaches the order, since no refund notification exists.
