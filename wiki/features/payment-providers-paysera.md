---
type: feature
nav_path: "Payment Providers → Paysera"
route_name: apps.paysera.settings
route_path: /admin/payment-providers/paysera
aliases: ["Paysera", "Paysera Lithuania", "Paysera bank", "Paysera payments"]
tags: [paymentproviders, payment-providers, paysera, international, eu, baltic, bank-transfer]
plan_gates: []
created: 2026-05-22
updated: 2026-05-27
source_count: 2
---
# Paysera

## Purpose

Paysera is a Lithuanian payment service provider offering a single integration that exposes many payment methods popular in the **Baltics, Poland, Ukraine, and surrounding Eastern European markets** — local bank transfers (Lithuania, Latvia, Estonia, Poland, Bulgaria, Romania, Russia), card payments (Visa, Mastercard), e-wallets (Paysera wallet, EPS, Skrill), and SMS-payment in some markets. The customer picks a method on Paysera's hosted page; CloudCart handles the redirect and the IPN status callback.

Paysera is the go-to for **Lithuanian and Baltic-focused stores**, and competitive in cross-border Eastern European e-commerce. The merchant signs up with Paysera, gets a project ID + signing password, and configures it here.

## Where to find it

Payment Providers → **Paysera**.

URL: `/admin/payment-providers/paysera`. Route name: `apps.paysera.settings`. Renders the standard Paysera edit form.

## What the merchant can do here

- Toggle the provider **Active**.
- Switch between **Test mode** and **Live mode** with the Test mode switch.
- Enter the **Project ID** (numeric, from your Paysera merchant dashboard).
- Enter the **Password** (the signing password from Paysera).
- Optionally enter the **Website verify META** tag — Paysera requires merchants to prove ownership of the storefront domain by adding a verification meta tag.
- Configure storefront name, logo, accepted-amount range, and an optional discount when paying with Paysera.

## Settings & fields

| Field / Control | What it does | Default | Validation / notes |
|---|---|---|---|
| **Test mode** switch | Toggles between Paysera sandbox and live processing. | Test mode ON (`configuration.mode` default `test`) | Stored as `configuration.mode = "test"` or `"live"`. Same merchant credentials are used in both modes — Paysera uses one project for test and live. Card border is orange in test, green in live. |
| **Project ID** | Numeric Paysera project identifier — used as the username in requests. | empty | `configuration.project_id`. Required. Validation: "Project ID is required". |
| **Password** | The signing password from Paysera — used to sign requests with the developer ID. | empty | `configuration.password` (masked). Required. Validation: "Password is required". Treat as secret. |
| **Website verify META** | The verification meta tag content provided by Paysera (placeholder example: `<meta name="verify-paysera" content="xxxxx.....xxxxx">`). | empty | `configuration.verify_meta`. Optional, no validation. Rendered into the storefront's `<head>` so Paysera can confirm domain ownership. |
| **Storefront name** | Display name on storefront. | "Paysera" | Common option. |
| **Logo** | Provider logo. | Paysera default | Common option. |
| **Amount from / Amount to** | Order-amount range when Paysera is available. | empty / empty | Common gate. |
| **Discount when paying with Paysera** | Flat / percent / shipping-free discount. | none | Common option. |

## Business rules

### Customer flow at checkout

1. Customer picks Paysera at checkout. CloudCart creates a payment.
2. CloudCart calls Paysera with: amount (major units), currency, transaction ID equal to the payment ID, notify/return/cancel URLs, billing card-address data, plus developer ID `12208355` and `buyerConsent: 1`.
3. Paysera returns a signed redirect form (HTML). The payment ID is stored as `provider_reference_id`, and the form is rendered to the customer and auto-submits via JavaScript — this avoids the URL-length limits a plain redirect would hit with large signed payloads. The signature covers all order fields, so any browser-side tampering (e.g. changing the price) invalidates it and Paysera rejects the request.
4. Customer reaches Paysera's hosted page, picks a method (bank, card, e-wallet), and completes it.
5. Paysera redirects the customer to CloudCart's return URL.
6. Paysera also POSTs an **IPN (Instant Payment Notification)** to CloudCart's webhook URL with the final status. CloudCart validates Paysera's signature and parses the transaction status. If the status is no longer `pending`, CloudCart persists the new state and returns Paysera's expected acknowledgement string (`OK`). Without that acknowledgement, Paysera keeps retrying the IPN.

### IPN signature validation — critical for security

Paysera signs every IPN with the merchant's password + project ID, validated on every incoming notification. If the signature is invalid, the IPN is rejected. **This prevents an attacker from POSTing fake "payment succeeded" notifications.**

If the signing password is misconfigured (e.g., a typo when entering it), every IPN fails validation, payments stick in `pending` indefinitely, and the merchant must fix the password.

### Developer ID — CloudCart's partner code

Every request includes `developerId: 12208355`, CloudCart's Paysera-partner attribution code — Paysera tracks platform usage through it. It's transparent to the merchant.

### Currency support

Paysera supports EUR primarily, plus USD, GBP, RUB, PLN, BGN, RON, CZK, and others depending on the merchant's contract with Paysera. The integration sends the store's native currency to Paysera; conversion (if any) happens at Paysera's side based on the merchant's account settings.

### Website verify META — domain ownership proof

Paysera requires merchants to prove they own the storefront domain before going live. Paysera issues a verification token in the merchant dashboard; the merchant pastes the full `<meta name="verify-paysera" content="...">` tag into the **Website verify META** field; CloudCart renders it in the storefront's `<head>`; Paysera crawls the domain and verifies it. Without this, Paysera may reject transactions or require manual per-transaction approval. New stores should set this before going live.

### Refunds

Supported. Refunds for bank-transfer methods may take several business days to reach the customer; card refunds are typically faster.

### Capture mode

Auto-capture only. Paysera operates as a redirect-collect mechanism — there's no manual-authorize / capture-later flow exposed here.

### Recurring / subscriptions

Not supported by this integration. Paysera offers recurring billing in their API but it's not wired here.

### 3D Secure

Handled by Paysera for card payments. Bank-transfer methods use the customer's banking 2FA at their bank's side.

### Saved cards / tokenization

Not exposed.

### Plan-gating

No plan-feature gate.

### Permission

Requires the standard payment-providers permission (`store.payment_providers`).

### Discount default

The default discount type when a Paysera discount is configured is `flat` (`configurationDefault.paysera.discount_type = 'flat'`).

## Related

- [[payment-providers]] — parent hub.
- [[payment-providers-skrill]] — alternative EU wallet provider.
- [[payment-providers-mollie]] — alternative EU multi-method gateway.
- [[orders-payment-refund]] — refund flow.
- [[settings-payment-providers]] — settings hub.

## Open questions

- ⏸️ The set of currencies a Paysera merchant can settle in is governed by their Paysera contract. CloudCart does not restrict currencies at the code level — Paysera rejects unsupported currencies at request time. The merchant should confirm with Paysera what their account is provisioned for.
