---
type: feature
nav_path: "Payment Providers → iCard"
route_name: apps.icard.settings
route_path: /admin/payment-providers/icard
aliases: ["iCard", "iCard payment gateway", "iCard BG"]
tags: [paymentproviders, payment-providers, icard, card-gateway, bulgaria]
plan_gates: []
created: 2026-05-22
updated: 2026-05-22
source_count: 0
---
# iCard

## Purpose

**iCard** is a Bulgarian payment service provider (also active across the EU) that issues prepaid cards + provides an Internet Payment Gateway (IPG) for online card acceptance. The CloudCart integration lets the merchant accept Visa / Mastercard / Maestro through iCard's hosted payment page — the customer is redirected to iCard, enters card details, completes 3DS, and returns to the storefront with a payment confirmation.

iCard is favoured by Bulgarian merchants who already hold an iCard merchant account or want lower per-transaction fees than the bank-routed gateways (BoricaWay4, DSK Bank, Fibank, UBB).

## Where to find it

Sidebar → **Settings → Payment methods** → **iCard** row → **Settings**.

The page's breadcrumb reads "Payment providers → iCard". The route is `/admin/payment-providers/icard`.

## What the merchant can do here

- Enter iCard merchant credentials (live + test).
- Toggle **Test mode** to point the integration at iCard's sandbox.
- Activate / deactivate the method at storefront checkout.
- Configure the per-method **storefront name** (what the customer sees in the payment-method list).
- Set per-method **min order amount** + per-country availability via [[settings-payment-providers]] common fields.

What the merchant **cannot** do here:
- Issue refunds from CloudCart — refunds happen in the iCard merchant portal.
- Change the supported card networks — iCard accepts what iCard's contract permits.
- Bypass 3DS — Visa / Mastercard / Maestro on iCard ALWAYS go through 3DS Secure (issuer policy).

## Settings & fields

Every credential exists in TWO variants — one for live mode, one for test mode. The merchant can save both at once and switch between them with the Mode toggle (`live` vs `test`).

| Field | Required | What it is |
|-------|----------|------------|
| **Mode** | yes | `live` / `test`. Toggles which set of credentials is used and which iCard endpoint is hit. |
| **Merchant ID** (`merchant_id` / `test_merchant_id`) | yes (numeric) | iCard merchant account ID. |
| **Terminal ID** (`terminal_id` / `test_terminal_id`) | yes | iCard terminal identifier — one per acquiring agreement / currency. |
| **Key Index** (`key_index` / `test_key_index`) | yes (numeric) | Index of the signing key used to sign outgoing payment requests. |
| **Key Index Resp** (`key_index_resp` / `test_key_index_resp`) | yes (numeric) | Index of the verification key used to validate iCard's response. |
| **Private Key** (`private_key` / `test_private_key`) | yes | The merchant's RSA private key (PEM) used to sign requests. iCard provides this during onboarding. |
| **API Public Key** (`api_public_key` / `test_api_public_key`) | yes | iCard's API public key (PEM) used to verify iCard's response signature. |

So configuring iCard requires SIX cryptographic-grade fields per environment + the merchant must have an active iCard contract. This is the most credential-heavy gateway in the BG portfolio.

## Business rules

### Live and test credentials co-exist on one row

Each iCard configuration row holds BOTH sets of credentials simultaneously. Toggling Mode flips which set is used at runtime — the merchant does NOT have to re-enter credentials when moving from test to live (or back). The non-active set remains stored on the same row.

### Redirect-based flow

The customer is redirected to iCard's hosted payment page (`https://gate.icards.eu/...` for live, sandbox URL for test). They enter card details on iCard's domain (which means the merchant doesn't need PCI-DSS scope for cardholder data) and are returned to CloudCart's success / cancel URLs after 3DS.

### Signed request + verified response

Every payment request the platform sends iCard is **signed with the merchant's private key**. iCard's response is **verified against iCard's API public key**. If either signature is missing or invalid, the platform rejects the response (preventing tampered confirmations).

This is why the integration has FOUR key-related fields (private key + public key + two key indexes) — iCard supports key rotation, and the indexes tell iCard which key version to use.

### 3DS is mandatory

All Visa / Mastercard / Maestro transactions through iCard go through 3D Secure 2.x. The merchant cannot disable this — it's enforced by card-network policy and iCard's gateway.

### Refunds via iCard portal

CloudCart does NOT expose a refund button for iCard transactions. The merchant logs into the iCard merchant portal and issues refunds there. After a refund on iCard's side, the merchant manually marks the CloudCart order as refunded via [[orders-payment-refund]].

### Permission

Standard payment-providers permission scope. Configuring iCard requires the merchant to have access to **Settings → Payment methods**.

## Related

- [[settings-payment-providers]] — payment methods landing page (iCard appears as a row).
- [[payment-providers]] — payment providers hub.
- [[orders-payment-mark-paid]] — after iCard confirms, the order is marked paid.
- [[orders-payment-refund]] — refunds are processed in iCard's portal, then mirrored in CloudCart.
- [[payment-providers-borica-way4]] / [[payment-providers-mypos]] / [[payment-providers-paynetics]] — alternative Bulgarian card gateways.

## How it works

### Dedicated module for iCard's Internet Payment Gateway

The integration uses a dedicated module that wraps iCard's Internet Payment Gateway (IPG) protocol, handling outbound payment requests and inbound response verification.

### Key rotation via separate indexes

The split between **Key Index** (signing) and **Key Index Resp** (verification) lets the merchant rotate keys independently — they can move to a new private key for outgoing signing without simultaneously changing the public key they use to verify iCard's responses.

### Numeric format enforced on IDs and indexes

**Merchant ID**, **Key Index**, and **Key Index Resp** MUST all be numeric. Letters or hex strings are rejected at save time.

## Open questions

(none)

## Verified — currencies, wallets, recurring

- **Currencies the CloudCart integration accepts**: BGN, EUR, USD, GBP, RON, CHF, JPY, CAD, AUD (nine ISO codes). Any other cart currency raises an "Unsupported currency for iCard" error at purchase time. Whether iCard's terminal can actually settle in all nine depends on the merchant's contract; if iCard's side rejects, the transaction fails after CloudCart accepts the cart.
- **Apple Pay / Google Pay**: NOT exposed in CloudCart's iCard integration. The IPG protocol wrapper handles standard card flows (Visa / Mastercard / Maestro); wallet methods are not surfaced as separate buttons. Merchants who need wallet checkout should use [[payment-providers-borica-way4|Borica Way4]] (MPay) or [[payment-providers-cloudcart-pay|CloudCart Pay]].
- **Recurring payments / stored cards**: NOT exposed in CloudCart's iCard integration. Every purchase requires the customer to enter card details fresh. iCard's underlying gateway may support tokenisation on some contracts, but CloudCart does not surface it.
