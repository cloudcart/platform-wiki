---
type: feature
nav_path: "Orders → open an order → Returns → Refund"
route_name: admin.core.orders.returns.refund-card
route_path: ""
aliases: ["Return refund", "Refund to card", "Return refund method", "return bank refund", "return voucher refund", "partial card refund return", "refund_method", "refunded_amount", "return refund side effects", "Refund to wallet", "CloudCart Wallet refund", "Refund as store credit", "Връщане в портфейл", "CloudCart Портфейл"]
tags: [orders, returns, refund, payment, card, credit-note, wallet]
plan_gates: []
created: 2026-07-24
updated: 2026-11-03
source_count: 1
---

> Part of [[orders-returns]]. See the hub for the other aspect (lifecycle & states).

# Order returns — refund methods & side-effects

## Purpose

How a return gives the customer their money back — the refund method chosen on the return, how a **card** refund is executed through the gateway (for both full and partial returns), how a **wallet** refund credits store credit, and how the two scopes differ in what they do to the order.

## Where to find it

On the return, worked from [[orders-details]]. The return stores the chosen **refund method** (editable via the return's *Refund* controls) and a **refund-to-card** action that calls the gateway.

## What the merchant can do here

- Choose how the customer is repaid. The **Issue return** form offers **By card**, **By bank transfer**, **CloudCart Wallet**, **Exchange** and **No refund**. The refund editor on an existing return offers By card, By bank transfer and No refund.
- Trigger the **card refund** through the payment gateway for a supported provider.
- Record a manual refund reference (bank reference / gateway id) when the money is moved outside the platform.

## Settings & fields

### Refund methods (`refund_method`)

| Method | Behaviour |
|---|---|
| **`card`** | Refund back to the original online-payment gateway — executed by the platform (see below). |
| **`bank`** | Manual bank transfer; the return captures the customer's **name / IBAN / BIC** for the payout. |
| **`voucher`** | Store voucher / discount code recorded by hand, with the code in `refund_reference`. The return forms no longer offer it; it stays readable on older returns and is accepted by the API. |
| **`wallet`** | **CloudCart Wallet** (`CloudCart Портфейл` in the Bulgarian returns list) — credits the customer's [[virtual-wallet|Virtual Wallet]] as store credit, with no gateway. Offered for a registered customer outside the Guests group. See below. |
| **`exchange`** | Recorded as an exchange rather than a money refund. |
| **`none`** | No refund (e.g. a goodwill restock). |

The return also records `refunded_amount`, `refunded_at`, and `refund_reference` (the gateway refund id, transfer reference, or voucher code) once the refund is done.

## Business rules

### Card refund — executed by the platform, full AND partial

The return's **refund-to-card** action calls the payment provider's API **matched to the return's scope**: a **full** return issues a **full refund**; a **partial** return issues a **partial refund** of the return's frozen total. Each is offered only when the gateway supports that capability:

- **Full + partial refunds:** **Stripe, PayPal, Revolut, CloudCart Pay**.
- **Full-only or unsupported:** Mollie, PayU, Mokka, Klear, COD, and others — a partial return then hides the card option and the merchant uses `bank` (or the provider's own dashboard). See [[orders-payment-refund-provider-matrix]].

It is **idempotent**: if the charge is already refunded at the gateway (a retry, or an out-of-band refund), the platform reconciles to the gateway's reality instead of erroring.

### Refund to the wallet — executed at once

Choosing **CloudCart Wallet** on the **Issue return** form credits the wallet as soon as the return is issued. There is no separate refund action and no gateway call.

- **Any order** can be refunded this way, whatever paid it. The method does not depend on the wallet top-up being switched on.
- The credit is a **new** wallet credit: type Refund, message `Refund for order #:order` / `Връщане на средства по поръчка #:order`, expiry from **Refunded-funds expiry** ([[virtual-wallet-settings]]). The wallet transaction number goes into `refund_reference`.
- **Order in a negative status:** the credit is the returned value minus the wallet money already spent on that order. The spent part comes back to the balance on its own — see [[virtual-wallet-order-lifecycle]].
- **Order in a positive status (partial return):** the full returned value is credited.
- If the credit fails, the return stays issued and the form shows a warning.

The returns list can be filtered by this method. The customer's account shows it as `Wallet` / `Портфейл`.

Wallet top-up and gift card lines themselves never go on a return or a credit note; see [[wallet-gift-instrument-checkout]].

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
- [[virtual-wallet]] — the store credit behind the CloudCart Wallet method.

## Open questions

None.
