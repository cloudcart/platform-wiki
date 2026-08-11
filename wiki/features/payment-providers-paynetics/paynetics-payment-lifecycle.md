---
type: feature
nav_path: "Payment Providers → Paynetics → Payment lifecycle"
route_name: apps.paynetics.overview
route_path: /admin/payment-providers/paynetics
aliases: ["Paynetics payment lifecycle", "Paynetics purchase", "Payoo hosted page", "Paynetics 3DS", "Paynetics return URL", "Paynetics pid", "Paynetics hash signing", "payoo-api-hash", "Paynetics status mapping", "Плащане Paynetics"]
tags: [paymentproviders, payment-providers, paynetics, lifecycle, 3ds, return-url, card-gateway]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

> Part of [[payment-providers-paynetics]]. See the hub for related aspects (setup & UI, feature gaps).

# Paynetics — Payment lifecycle

## Purpose

This aspect covers the end-to-end charge flow for Paynetics: how the platform builds and signs the request, redirects the customer to Paynetics's hosted **Payoo** page for mandatory 3-D Secure, and reads the result from an **encrypted return URL** that carries the status directly (no separate webhook callback). It also documents the card networks, currency handling, order reference format, and the binary status mapping.

## Where to find it

There is no admin screen for the lifecycle itself — it runs at checkout when a customer picks Paynetics as the payment method. The settings that feed it (Mode, credentials) live on [[paynetics-setup-ui]]. The resulting [[payment-status]] is visible on the order details page.

## What the merchant can do here

- **Observe the charge result** on the order — `Completed` (success) or `Failed` (error / anything else).
- **Understand why a payment may stay `Pending`** — if the customer never reaches the return URL (network drop, browser crash), the status doesn't settle automatically; see [[paynetics-gaps]] for the missing sync.
- **Manually reconcile** a stranded payment by checking Paynetics's portal and marking the order accordingly.

## Settings & fields

This aspect exposes no settings of its own — it is the runtime flow. The Mode (Test/Live) radio and credential keys it consumes are documented on [[paynetics-setup-ui]].

## Business rules

### Payment lifecycle

1. **Purchase** builds a payment payload (order ID = platform payment ID, amount, currency, description, customer details, success URL, error URL), JSON-encodes it, base64-encodes the JSON, and includes that as the `pm` parameter.
2. **Request signing** — every Paynetics call carries three HTTP fields:
   - `payoo-api-key` = the merchant's API key
   - `payoo-api-request-date` = current Unix timestamp
   - `payoo-api-hash` = `HMAC-SHA256(api_key + request_date + operation + optional user_token, secret)`, keyed with the merchant's secret.
3. **Authenticate** — the platform POSTs to `/authenticate/request` with the signed payload. Paynetics validates the signature, decodes the payload, and renders its hosted Payoo page to the customer.
4. **3DS** happens on Paynetics's hosted page (see below — mandatory).
5. **Return** — the status is encoded into the encrypted `pid` return parameter (see below).

### 3-D Secure is mandatory

Every Paynetics charge runs through 3DS on Paynetics's hosted Payoo page. The merchant cannot disable 3DS — Paynetics policy enforced by the underlying card networks for EEA cards.

### Encrypted return URL (status-in-URL, no webhook dependency)

The integration uses **per-payment encrypted return URLs** instead of a separate webhook callback (one for success, one for error):

```
Success: <cc_payments_domain>/return/provider/paynetics?pid=<base64(AES(payment_id|success))>
Error: <cc_payments_domain>/return/provider/paynetics?pid=<base64(AES(payment_id|error))>
```

The status is encoded directly into the encrypted `pid` parameter — the platform decrypts on return and reads `success` or `error` after the `|`, then updates the payment row. The customer's browser carries the status back; no IPN callback is required. This makes Paynetics resilient to webhook delivery issues, but it also means the platform has **no fallback if the customer never reaches the return URL**.

### Status code mapping (binary)

The status is binary — there's no `Pending`, no `Authorized`, no nuanced statuses today.

| `pid` payload | Mapped platform [[payment-status]] |
|---------------|-----------------------------------|
| AES-decrypted suffix `success` | `Completed` |
| AES-decrypted suffix `error` (or anything else) | `Failed` |

### Card networks supported

Visa, Mastercard. (Maestro / Amex / JCB depend on Paynetics's per-merchant acquiring contract.)

### Currency support

Paynetics is a **multi-currency** processor — the merchant's account can be provisioned for **BGN, EUR**, and other currencies depending on the contract. The platform sends the storefront order's currency directly to Paynetics on each transaction — no platform-side conversion.

### Order ID format

The platform sends `reference = <payment ID>` (the platform's internal payment row ID). This is what Paynetics stores as the merchant reference and is included in their internal records / portal.

### Same URL for test and live

The integration's test and live endpoint URLs are both set to `https://pm.payoo.paynetics.digital` — the mode flag is sent to Paynetics inside the signed payload, but the endpoint URL doesn't change. This is consistent with Paynetics's architecture where mode is determined by the API-key namespace, not the URL.

## Related

- [[payment-providers-paynetics]] — hub.
- [[payment-status]] — Completed / Failed mapping for Paynetics charges.
- [[checkout-flow]] — concept page on storefront checkout.

## Open questions

_None._
