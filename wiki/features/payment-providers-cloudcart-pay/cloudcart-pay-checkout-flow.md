---
type: feature
nav_path: "Payment Providers → Cloudcart Pay → Checkout flow"
route_name: apps.cloudcart_pay.overview
route_path: /admin/payment-providers/cloudcart_pay
aliases: ["CloudCart Pay checkout flow", "CloudCart Pay embedded checkout", "CloudCart Pay hosted checkout", "CloudCart Pay Apple Pay Google Pay", "CloudCart Pay capture"]
tags: [paymentproviders, payment-providers, cloudcart-pay]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 1
---

> Part of [[payment-providers-cloudcart-pay]]. See the hub for the other aspects (account model, activation gate, refunds + webhooks, saved card) and the four lifecycle tabs.

# CloudCart Pay — checkout flow

## Purpose

This page documents how a customer actually pays when they pick CloudCart Pay at checkout — the embedded vs hosted modes, which card brands and wallets are accepted, why capture is always immediate, how currency is handled, and the idempotency behaviour that prevents double charges. It is the page to read for "how does the card form appear?" or "does CloudCart Pay support Apple Pay?" questions.

## Where to find it

This behaviour happens on the **storefront checkout**, not in the admin panel — CloudCart Pay surfaces there as a card payment option once activated (see [[checkout-flow]]). The merchant configures the method from Sidebar → **Payment Providers** → **CloudCart Pay**.

## What the merchant can do here

- **Offer inline (embedded) card entry** on the modern checkout, so the customer never leaves the store.
- **Accept Visa / Mastercard plus Apple Pay and Google Pay** out of the box.
- **Rely on automatic capture** — funds are captured immediately on a successful payment; there is no separate manual-capture step.

## Settings & fields

There are no merchant-facing fields specific to the checkout flow — the mode (embedded vs hosted) is chosen automatically by the storefront, and wallets are always auto-enabled. The customer-facing label is set on the [[payment-providers-cloudcart-pay-settings|Settings tab]]; the *Save customer card* option that affects the checkout session is documented in [[cloudcart-pay-save-card]].

## Business rules

### Checkout mechanism — hosted checkout + embedded JS

CloudCart Pay uses the platform's **Checkout Session** API in two modes:

- **Embedded checkout** (`ui_mode=embedded`) — the default when the storefront uses the modern checkout JS. The customer enters card details inline within the CloudCart checkout; a popup is rendered with the order total; `payment_method_types` is forced to `card`. On submission the platform confirms the payment intent; on failure it falls back to a confirm-checkout-js fallback path.
- **Hosted checkout** (`ui_mode=hosted`) — fallback. CloudCart Pay creates a checkout session and returns a redirect URL; the customer completes payment on the provider-hosted page and is bounced back to `payments.return` with `?pid=<payment_id>` (the return URL is `<cc_payments_domain>/return/provider/cloudcart_pay?pid=<payment_id>`).

In both modes the card brand, expiry, and last 4 digits are captured and shown on the [[payment-providers-cloudcart-pay-transactions|Transactions]] tab. The platform stores the payment-intent ID as `provider_reference_id` along with the checkout session ID.

### Apple Pay + Google Pay auto-enabled

Apple Pay and Google Pay wallets are auto-enabled (`display=auto`) on every checkout session, in both embedded and hosted modes. The merchant does not configure them separately.

### Two-phase capture — auto-capture only

`capture_method=automatic` is hard-coded on every checkout session. There is **no** Authorize-then-Capture flow exposed in the CloudCart Pay integration today — funds are captured immediately on a successful payment. This is why [[orders-payment-capture|manual capture]] is effectively a no-op for CloudCart Pay charges.

### Currency handling

Whatever the storefront's order currency is, the platform passes it directly to the provider. The connected account's supported settlement currencies are listed in [[payment-providers-cloudcart-pay-payouts]]; if a customer's currency isn't supported by the account, the checkout-session creation is rejected and the customer cannot complete the CloudCart Pay payment in that currency.

### Idempotency — no duplicate charges on retry

The checkout-session and refund APIs are idempotent on `client_reference_id` (set to `<order_id>`) and refund ID respectively. If the platform retries a checkout creation for the same order, the provider returns the existing session rather than a duplicate charge. The sync fallback also re-reads the live state rather than re-confirming — see [[cloudcart-pay-refunds-webhooks]].

## Related

- [[payment-providers-cloudcart-pay]] — hub.
- [[checkout-flow]] — storefront checkout where CloudCart Pay surfaces as a card option.
- [[payment-providers-cloudcart-pay-transactions]] — where each checkout's card brand / last-4 / status appears.
- [[payment-providers-cloudcart-pay-payouts]] — supported settlement currencies.
- [[orders-payment-capture]] — manual capture (immediate for CloudCart Pay because of auto-capture).
- [[cloudcart-pay-save-card]] — how the save-card setting changes the checkout session.
- [[payment-status]] — Completed / Failed mapping for CloudCart Pay charges.

## Open questions

(none)
