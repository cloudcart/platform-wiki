---
type: feature
nav_path: "Payment Providers → Skrill"
route_name: apps.skrill.settings
route_path: /admin/payment-providers/skrill
aliases: ["Skrill", "Skrill wallet", "Skrill payments"]
tags: [paymentproviders, payment-providers, skrill, international, wallet, eu]
plan_gates: []
created: 2026-05-22
updated: 2026-05-27
source_count: 2
---
# Skrill

## Purpose

Skrill is a European e-wallet and payment gateway popular for digital-goods purchases, gambling/gaming transactions, and cross-border remittance. Customers redirect to Skrill's hosted checkout, log in to their Skrill wallet (or pay as a guest with a card / local bank transfer), and Skrill notifies CloudCart of the result via webhook.

Skrill is well-known in the **UK, Germany, Poland, and other European markets**, particularly among users who prefer wallet-based payments over direct card entry. Skrill also offers fast cross-border money flow without the merchant having to manage international card-acquiring relationships directly.

## Where to find it

Payment Providers → **Skrill**.

URL: `/admin/payment-providers/skrill`. Route name: `apps.skrill.settings`.

## What the merchant can do here

- Toggle the provider **Active**.
- Enter the **Email** of the Skrill merchant account — used as the recipient identifier.
- Enter the **Merchant ID** (numeric, from the Skrill merchant dashboard).
- Enter the **API Password** (set in the Skrill MQI / Automated Payments Interface settings — distinct from the merchant's login password).
- Enter the **Signature Secret** — used to MAC the webhook callback so CloudCart can verify it actually came from Skrill.
- Pick the **Signature Hash Algorithm**: MD5 or SHA-256.
- Configure storefront name, logo, accepted-amount range, and an optional discount when paying with Skrill — common option group.

## Settings & fields

| Field / Control | What it does | Default | Validation / notes |
|---|---|---|---|
| **Email** | The Skrill account email — used as the payment recipient identifier. | empty | Required, must be a valid email. Translation key: `payment_provider.label.skrill.email`. Help: "This is the email from your Skrill account." |
| **Merchant ID** | The numeric merchant ID from Skrill's dashboard. | empty | Required. Help: "This is the merchant ID from your Skrill account." |
| **API Password** | The Skrill API password (set in MQI / Automated Payments Interface settings). | empty | Required. Help: "This is the API password from your Skrill account." |
| **Signature Secret** | The shared secret used to verify Skrill's webhook signature. | empty | Required. Help: "This is the signature secret algorithm from your Skrill account." |
| **Signature Hash Algorithm** | Algorithm Skrill uses to sign webhook callbacks: MD5 or SHA-256. Must match the algorithm set in Skrill's merchant dashboard. | empty | Required. Dropdown with two options: `md5` / `sha256`. Help: "This is the signature hash algorithm from your Skrill account." |
| **Storefront name** | Display name on storefront. | "Skrill" | Common option. |
| **Logo** | Provider logo. | Skrill default | Common option. |
| **Amount from / Amount to** | Order-amount range when Skrill is available. | empty / empty | Common gate. |
| **Discount when paying with Skrill** | Flat / percent / shipping-free discount. | none | Common option. |

## Business rules

### Customer flow at checkout

1. Customer picks Skrill at checkout. CloudCart creates a `Payment` row.
2. CloudCart builds a redirect to Skrill's hosted payment page, passing: merchant email, merchant ID, transaction ID, currency, amount, return URL, cancel URL, status URL (webhook), and a description.
3. Customer is redirected to Skrill, logs in (or pays as guest with a card / local bank), and approves the payment.
4. Skrill redirects the customer to CloudCart's return URL.
5. Skrill **also** POSTs a status notification to CloudCart's status URL (webhook). This is the authoritative status update — the redirect URL is just for UX.
6. CloudCart verifies the webhook's signature (using the saved signature secret + hash algorithm) before trusting the status.

### Webhook signature verification — critical for security

Skrill's status URL POSTs an `md5sig` or `sha2sig` field along with payment details. CloudCart computes the expected signature using the configured secret + algorithm and compares — if they don't match, the webhook is rejected. **This prevents an attacker from POSTing a fake "payment succeeded" notification to CloudCart's status URL**. The merchant must set the same signature secret and algorithm both on Skrill's side and in CloudCart's settings, or webhooks will be rejected as invalid.

### Currency

Skrill supports a wide range of currencies — EUR, USD, GBP, PLN, and many others. CloudCart sends the payment in the store's currency; Skrill may convert at their end based on the merchant's Skrill account settings. Refer to Skrill's documentation for the up-to-date list of supported currencies.

### Refunds

Refund flow depends on the Skrill API password's permissions; CloudCart calls Skrill's refund endpoint against the saved transaction reference. Refunds typically take several business days to reach the customer.

### Capture mode

Auto-capture only. There is no manual-authorize / capture-later flow for Skrill in this integration.

### Recurring / subscriptions

Skrill supports recurring billing through their MQI, but CloudCart's integration is one-off purchase only. No recurring at this layer.

### Saved cards / tokenization

Not exposed. Skrill manages wallet-level customer recognition itself — returning customers see their saved Skrill account on the Skrill side.

### 3D Secure

Handled by Skrill for card payments (Skrill's hosted page enforces 3DS when the card requires it). Wallet payments don't go through 3DS.

### Plan-gating

No plan-feature gate.

### Deprecation status

Skrill is **NOT** deprecated — it remains available to new merchants (only `sofort` and `instamojo` are on the platform's deprecated list). That said, Skrill's wallet market share has declined and most new stores choose [[payment-providers-cloudcart-pay|CloudCart Pay]], [[payment-providers-stripe|Stripe]], or [[payment-providers-mollie|Mollie]] instead — a market preference, not a CloudCart policy. The settings screen is an older form layout (no Vue SPA), so unlike modern providers it offers no test/live mode switch, save-card toggle, or rich-text description editor.

### Permission

`hasApiPermission:settings,store.payment_providers`.

### Test mode

The Skrill integration does **not** have an explicit test-mode toggle on this settings screen. The merchant tests by using their Skrill sandbox / merchant-test environment credentials (Skrill provides a separate test merchant account for sandbox testing). Switching between sandbox and live is done by swapping the merchant credentials in CloudCart — there is no `mode` flag stored in configuration.

## How it works (verified against backend) — signature algorithm choice

Skrill's webhook signature can be computed with either MD5 (legacy, default) or SHA-256 (recommended). The choice is made in the Skrill dashboard (MQI settings) and must match the algorithm picked in CloudCart's settings.

- **MD5** — Skrill's legacy default. Cryptographically weak; acceptable for webhook authentication but not state-of-the-art.
- **SHA-256** — stronger; recommended for new integrations where the Skrill account allows it.

If the two sides mismatch (e.g. CloudCart set to SHA-256 but Skrill sending MD5), every webhook fails verification and payments stay stuck in `pending` until the merchant fixes it.

Required fields are validated for presence on save, but there's no API-ping check — a typo in the API password won't surface until the first real transaction.

## Related

- [[payment-providers]] — parent hub.
- [[payment-providers-paypal]] — alternative wallet provider.
- [[payment-providers-mollie]] — alternative EU multi-method gateway.
- [[orders-payment-refund]] — refund flow.
- [[settings-payment-providers]] — settings hub.

## Open questions

(none)
