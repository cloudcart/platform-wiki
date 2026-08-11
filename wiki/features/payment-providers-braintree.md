---
type: feature
nav_path: "Payment Providers → Braintree"
route_name: apps.braintree.settings
route_path: /admin/payment-providers/braintree
aliases: ["Braintree", "Braintree gateway", "PayPal Braintree"]
tags: [paymentproviders, payment-providers, braintree, international, paypal-group, card-gateway]
plan_gates: []
created: 2026-05-22
updated: 2026-06-10
source_count: 2
---
# Braintree

## Purpose

Braintree is a global card-payment gateway owned by PayPal that supports 130+ currencies. It is **direct card processing**: the customer enters their card on a CloudCart-hosted page (powered by Braintree's Drop-In JS module), Braintree tokenizes it in an iframe (CloudCart never sees raw card data), and the charge runs server-side. There is no PayPal-style wallet redirect — the customer stays on the merchant's site throughout.

Braintree is the pick for merchants who want direct card processing with **their own Braintree merchant account** (not PayPal standard checkout, not Stripe), plus optional 3D Secure verification. The merchant signs up directly with Braintree, gets API credentials, and processes cards through this integration.

## Where to find it

Payment Providers → **Braintree**. URL: `/admin/payment-providers/braintree`. Route name: `apps.braintree.settings`.

## What the merchant can do here

- Toggle the provider **Active**.
- Switch between **Test mode** (Braintree sandbox) and **Live mode**.
- Enter the **Merchant ID**, **Public Key**, **Private Key**, and **Merchant Account ID** — separately for test and live.
- Pick the **Account Currency** for test and live — the currency of the Braintree merchant-account (accounts are currency-locked at the merchant-account level).
- Toggle **3D Secure Verification** for test and live independently.
- Configure storefront name, logo, payment-method description, accepted-amount range, and an optional discount when paying with Braintree.

## Settings & fields

| Field / Control | What it does | Default | Validation / notes |
|---|---|---|---|
| **Test mode** switch | Toggles between Braintree sandbox and live processing. | Test mode ON | Stored as `configuration.mode = "test"` or `"live"`. |
| **Merchant ID** (test / live) | Your Braintree merchant ID for the mode. | empty | Required when corresponding mode is selected. |
| **Public Key** (test / live) | Public-key half of the Braintree API key pair. | empty | Required for the active mode. |
| **Private Key** (test / live) | Private-key half of the API key pair. | empty | Required for the active mode. Treat as a secret. |
| **Merchant Account ID** (test / live) | Identifies which Braintree merchant-account (sub-merchant) under your gateway receives the funds. | empty | Required for the active mode. Braintree allows multiple merchant-accounts per gateway, each currency-locked. |
| **Account Currency** (test / live) | Currency of the linked merchant-account. | `AED` | Searchable select from 130+ ISO 4217 currencies. Must match the merchant-account's actual currency in Braintree. |
| **3D Secure Verification** (test / live) | If ON, payments are forced through 3DS (issuer-side cardholder authentication). | OFF | Each mode toggled independently. When OFF, 3DS only fires when the issuer mandates it. |
| **Storefront name** | Display name on storefront. | "Braintree" | Common option. |
| **Logo** | Provider logo. | Braintree default | Common option. |
| **Amount from / Amount to** | Order-amount range when Braintree is available. | empty / empty | Common gate. |
| **Discount when paying with Braintree** | Flat / percent / shipping-free discount. | none | Common option. |

Setting keys: `configuration.{test,live}_merchant_id`, `_public_key`, `_private_key`, `_merchant_account_id`, `_currency`, and the `test_3ds` / `live_3ds` switches.

**Per-field validation:** each test field is `required_if:configuration.mode,test`; each live field is `required_if:configuration.mode,live`. Attribute labels: "Test/Live Merchant ID", "Test/Live Public Key", "Test/Live Private Key", "Test/Live Merchant Account ID". No custom messages (the application framework default `required_if`).

**Supported currencies:** 130+ ISO 4217 — including AED, AUD, BGN, BRL, CAD, CHF, EUR, GBP, JPY, PLN, RON, USD, ZAR, and many more.

## Business rules

### Customer flow at checkout

1. Customer picks Braintree. CloudCart fetches a one-time client token from Braintree.
2. The token renders Braintree's **Drop-In UI** module in the browser — card, CVV, expiry are entered into Braintree's iframe.
3. The module tokenizes the card and POSTs a `payment_method_nonce` back to CloudCart.
4. CloudCart calls Braintree's transaction-sale endpoint with the amount (in the merchant-account currency), the nonce, the merchant-account ID, and — if 3DS is on — a 3D-Secure-required flag.
5. Braintree either **succeeds immediately** → status `completed`, or **requires 3DS** → the customer authenticates on an issuer screen, then returns and the transaction finalizes.
6. Request + response are logged to the order's payment log.

### Tokenization — Drop-In, not Hosted Fields

CloudCart uses Braintree's **Drop-In UI** (the full payment-method picker), not Hosted Fields, so the merchant cannot skin a custom card form. The Drop-In automatically shows whichever wallet methods the merchant has enabled in their Braintree control panel — **PayPal, Apple Pay, Google Pay, Venmo**, etc. There is no per-method toggle in CloudCart; wallet methods are turned on/off entirely in the Braintree dashboard. Card vaulting is disabled (`card.vault.vaultCard: false`), so every purchase is treated as fresh.

### Currency — account-locked, single-currency

Each Braintree merchant-account is **locked to one currency**, and this integration supports only **one merchant-account-ID per mode**. The configured Account Currency MUST match the merchant-account's actual currency in Braintree. On every purchase the order amount is converted from the **store currency** to the **merchant-account currency** using CloudCart's currency tables at checkout, then sent to Braintree. Example: a BGN store with a USD merchant-account shows BGN prices, converts the total to USD at checkout, charges the card in USD, and the merchant sees USD in their Braintree dashboard.

For **true multi-currency** (EU customers pay EUR, Brazilian customers pay BRL, etc.) the merchant needs a gateway that switches currency per request, such as [[payment-providers-stripe]] — Braintree-via-CloudCart is locked to one currency.

### 3D Secure (optional)

When the per-mode 3DS toggle is ON, **every** transaction is forced through 3DS: the customer authenticates with their issuing bank (mobile-app push, SMS OTP, or biometric), and checkout requires liability to shift before the payment submits. A failed verification shows a "3D Secure Verification Failed" error and the customer retries. If the issuer doesn't support 3DS, the transaction is rejected. When the toggle is OFF, 3DS only fires when the issuer mandates it (e.g. EU PSD2 SCA on high-value transactions). Test and live are toggled independently.

### Refunds, voids, capture, recurring

- **Void** — cancels a not-yet-settled transaction (typically same-day).
- **Refund** — returns funds on an already-settled transaction; status → `refunded`. The integration chooses void vs refund based on transaction state.
- **Capture** — auto-capture only (auth + capture together). No manual capture or hold.
- **Recurring / saved cards** — not supported; this integration is one-off purchase only (no vault, no subscriptions).

### Settings UI behaviour

The form shows **exactly one mode card at a time** — the inactive mode card is hidden entirely (`isVisible: mode === 'test'` / `'live'`), unlike Stripe which shows both cards locked. Fields render inline inside the card (no slide-out). The 3DS switch is per-mode.

### Plan-gating & permission

No plan-feature gate. Permission: `hasApiPermission:settings,store.payment_providers`.

### Sandbox / test cards

In test mode, use Braintree's standard sandbox test card numbers (e.g. `4111 1111 1111 1111` for a generic success; other numbers trigger specific declines). The sandbox merchant-account ID is whatever the merchant set up in their Braintree sandbox dashboard.

## Related

- [[payment-providers]] — parent hub.
- [[payment-providers-paypal]] — sibling product (same PayPal group).
- [[payment-providers-stripe]] — alternative direct card processor with per-request multi-currency support.
- [[payment-providers-cloudcart-pay]] — CloudCart's own card gateway.
- [[orders-payment-refund]] — refund flow.
- [[settings-payment-providers]] — settings hub.

## Open questions

(none)
