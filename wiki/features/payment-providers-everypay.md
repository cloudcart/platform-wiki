---
type: feature
nav_path: "Payment Providers → Everypay"
route_name: apps.everypay.settings
route_path: /admin/payment-providers/everypay
aliases: ["Everypay", "EveryPay", "every-pay", "Everypay EU"]
tags: [paymentproviders, payment-providers, everypay, international, eu, baltic, card-gateway]
plan_gates: []
created: 2026-05-22
updated: 2026-06-11
source_count: 2
---
# Everypay

## Purpose

Everypay is a European card-payment gateway, originating from **Estonia** and operating across the **Baltics (Estonia, Latvia, Lithuania), Finland, and other EU markets**. It accepts Visa, Mastercard, Maestro, and Amex. The integration uses Everypay's hosted card-tokenization JS (similar to Braintree's Drop-In or Stripe's Checkout) — the customer enters card details in an Everypay-hosted popup, the card is tokenized, and CloudCart server-side charges the token. It is well-suited to **Baltic and Northern European stores** wanting a regional alternative to Stripe with potentially better local-card support. The merchant signs up with Everypay, receives a public + secret key pair, and configures them here.

## Where to find it

Payment Providers → **Everypay**. URL: `/admin/payment-providers/everypay`. Route name: `apps.everypay.settings`.

## What the merchant can do here

- Toggle the provider **Active**.
- Switch between **Test mode** and **Live mode** with the Test mode switch.
- Enter the **Public Key** — used by the customer's browser to tokenize cards via Everypay's JS.
- Enter the **Secret Key** — used by CloudCart server-side to authenticate API calls.
- Configure storefront name, logo, accepted-amount range, and an optional discount when paying with Everypay.

## Settings & fields

| Field / Control | What it does | Default | Validation / notes |
|---|---|---|---|
| **Test mode** switch | Toggles between Everypay sandbox and live processing. | Test mode ON | Stored as `configuration.mode = "test"` or `"live"`. |
| **Public Key** | The Everypay public key — used by the customer's browser to interact with Everypay's tokenization JS. Setting key `configuration.public_key`. | empty | Required. Message: "Public key is required." Placeholder: "Enter your public key for Everypay". |
| **Secret Key** | The Everypay secret key — used by CloudCart to authenticate API calls. Setting key `configuration.secret_key`. | empty | Required. Message: "Secret key is required." Placeholder: "Enter your secret key for Everypay". Treat as secret. |
| **Storefront name** | Display name on storefront. | "Everypay" | Common option. |
| **Logo** | Provider logo. | Everypay default | Common option. |
| **Amount from / Amount to** | Order-amount range when Everypay is available. | empty / empty | Common gate. |
| **Discount when paying with Everypay** | Flat / percent / shipping-free discount. | none default `discount_type: 'flat'` | Common option. |

The Everypay key card stays visible in both Test and Live mode; only its border colour changes with the mode.

## Business rules

### Customer flow at checkout

1. Customer picks Everypay at checkout. CloudCart loads Everypay's checkout JS via the tokenization endpoint.
2. CloudCart renders a popup configured with the public key, the amount, and the test/live mode flag.
3. Customer enters card details in the Everypay-hosted popup — Everypay tokenizes the card and returns a one-time nonce to CloudCart.
4. CloudCart's storefront posts the nonce back to CloudCart's payments API.
5. CloudCart calls Everypay's purchase endpoint with: amount (in minor units, converted to EUR if the store is non-EUR), the nonce, a description (the payment's site reference ID + the site URL), and the secret key.
6. Everypay charges the card and returns the transaction; its transaction token is saved as the payment's provider reference for later sync and refund.
7. CloudCart maps the response status to the platform payment statuses and finalizes the payment.

### Currency — EUR-only

The integration **always sends EUR to Everypay** regardless of the store's currency. If the store sells in a non-EUR currency (e.g., BGN, RON, USD), CloudCart converts the amount to EUR before calling Everypay. This is hard-coded — there is no currency picker in the settings. For non-EUR stores, customers see the EUR amount on Everypay's popup and the merchant receives EUR. Whether Everypay's broader product line offers other settlement currencies is irrelevant here — the CloudCart wrapper only sends EUR.

### Status mapping

Everypay returns one of these statuses, which CloudCart maps:

- `Captured` → `completed`
- `Refunded` → `refunded`
- `Pending` → `requested`
- `Canceled` → `cancelled`
- (other / unknown) → `failed`

### Status sync (pull-based, no webhooks)

This integration does **not** receive webhooks for status changes. Instead it polls: on the customer's return from the gateway and via the periodic sync queue, CloudCart calls Everypay's transaction-status endpoint with the saved transaction token and secret key, logs the response to the order's payment log, maps the returned status (same `Captured`/`Refunded`/`Pending`/`Canceled`/other table), and persists the latest status. A fresh status requires an explicit sync. The payment log preserves both request and response, which makes diagnosing customer-reported issues (e.g., "I was charged but the order says failed") straightforward via the support tools.

### Refunds

Supported via Everypay's refund endpoint. CloudCart calls it with the saved transaction token, the amount (read from the original transaction's stored data), and an empty description. The refund status is mapped via the same `Captured`/`Refunded`/etc. table — a successful refund moves the payment status to `refunded`.

### Capture mode

Auto-capture. The integration always issues a purchase (auth + capture together). There is no manual-authorize / capture-later flow.

### 3D Secure

Handled by Everypay automatically when the card requires it. The customer is prompted by their issuing bank during the tokenization popup if 3DS is mandated.

### Recurring / subscriptions

Not implemented at this layer.

### Saved cards / tokenization

The saved Everypay token is per-transaction (used for sync and refund of that same transaction), **not** a vaulted-card token. Each new purchase requires fresh card entry.

### Settlement entity

CloudCart's side is configuration-only (public + secret key). Which Everypay settlement entity the merchant ends up on is determined by the live keys their Everypay contract issues, not by anything in CloudCart.

### Plan-gating & permission

No plan-feature gate. Requires the standard payment-providers permission (`store.payment_providers`).

### Test mode setup

In test mode, use Everypay's sandbox test card numbers (see Everypay's developer documentation). The sandbox public + secret key pair is separate from the live pair — switching modes just swaps which key pair is read.

## Related

- [[payment-providers]] — parent hub.
- [[payment-providers-stripe]] — alternative international card gateway with broader currency support.
- [[payment-providers-cloudcart-pay]] — CloudCart's own card gateway.
- [[orders-payment-refund]] — refund flow.
- [[settings-payment-providers]] — settings hub.

## Open questions

(none)
