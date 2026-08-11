---
type: feature
nav_path: "Orders → open an order → Returns → Refund"
route_name: admin.core.orders.returns.refund-card
route_path: ""
aliases: ["Return refund", "Refund to card", "Return refund method", "return bank refund", "return voucher refund", "partial card refund return", "refund_method", "refunded_amount", "return refund side effects"]
tags: [orders, returns, refund, payment, card, credit-note]
plan_gates: []
created: 2026-07-24
updated: 2026-07-24
source_count: 1
---

> Part of [[orders-returns]]. See the hub for the other aspect (lifecycle & states).

# Order returns — refund methods & side-effects

## Purpose

How a return gives the customer their money back — the refund method chosen on the return, how a **card** refund is executed through the gateway (for both full and partial returns), and how the two scopes differ in what they do to the order.

## Where to find it

On the return, worked from [[orders-details]]. The return stores the chosen **refund method** (editable via the return's *Refund* controls) and a **refund-to-card** action that calls the gateway.

## What the merchant can do here

- Choose (or change) how the customer is repaid: card, bank transfer, voucher, or "handled manually".
- Trigger the **card refund** through the payment gateway for a supported provider.
- Record a manual refund reference (bank / voucher / gateway id) when the money is moved outside the platform.

## Settings & fields

### Refund methods (`refund_method`)

| Method | Behaviour |
|---|---|
| **`card`** | Refund back to the original online-payment gateway — executed by the platform (see below). |
| **`bank`** | Manual bank transfer; the return captures the customer's **name / IBAN / BIC** for the payout. |
| **`voucher`** | Store voucher / discount code — issued manually; the code is kept in `refund_reference`. |
| **`wallet`** | CloudCart Wallet — a future method, hidden in the UI until it exists. |
| **`exchange`** | Recorded as an exchange rather than a money refund. |
| **`none`** | No refund (e.g. a goodwill restock). |

The return also records `refunded_amount`, `refunded_at`, and `refund_reference` (the gateway refund id, transfer reference, or voucher code) once the refund is done.

## Business rules

### Card refund — executed by the platform, full AND partial

The return's **refund-to-card** action calls the payment provider's API **matched to the return's scope**: a **full** return issues a **full refund**; a **partial** return issues a **partial refund** of the return's frozen total. Each is offered only when the gateway supports that capability:

- **Full + partial refunds:** **Stripe, PayPal, Revolut, CloudCart Pay**.
- **Full-only or unsupported:** Mollie, PayU, Mokka, Klear, COD, and others — a partial return then hides the card option and the merchant uses `bank` (or the provider's own dashboard). See [[orders-payment-refund-provider-matrix]].

It is **idempotent**: if the charge is already refunded at the gateway (a retry, or an out-of-band refund), the platform reconciles to the gateway's reality instead of erroring.

### The two scopes have different order-level side-effects

- **Full refund** → the local payment flips to `refunded`, so the **order** flips to `refunded` too, and PaymentSync **auto-restores stock** (see [[orders-payment-refund-side-effects]]).
- **Partial refund** → the order status is **left untouched** (the payment is not fully refunded). Instead the platform re-computes the customer's effective spend so **income totals and [[marketing-segments|segments]]** reflect that they paid less. Restock for a partial comes from **receiving the return**, not from the refund (see [[orders-returns-lifecycle]]).

### Relationship to the standalone Refund button

The **Refund payment** button on the payment ([[orders-payment-refund]]) is a **different surface** and is **full-amount only**. The **return** flow is the way to refund only part of an order for the capable gateways — see [[orders-payment-refund-partial-refunds]] for the two surfaces side by side.

## Related

- [[orders-returns]] — hub.
- [[orders-returns-lifecycle]] — states, receipt / restock, and the credit-note-locks-full rule.
- [[orders-payment-refund]] — the standalone full-only Refund button.
- [[orders-payment-refund-partial-refunds]] — the two refund surfaces compared.
- [[orders-payment-refund-provider-matrix]] — which gateways support refund / partial refund.
- [[orders-payment-refund-side-effects]] — what a full refund cascades (status flip, stock).
- [[orders-credit]] — the credit note the return issues.

## Open questions

None.
