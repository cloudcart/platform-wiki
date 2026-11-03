---
type: feature
nav_path: "Payment Providers → NestPay"
route_name: apps.nestpay.settings
route_path: /admin/payment-providers/nestpay
aliases: ["NestPay", "Nestpay", "Turkish card gateway", "Asseco NestPay", "Akbank card", "Garanti card", "İşbank card"]
tags: [paymentproviders, payment-providers, nestpay, turkey, card, 3ds, redirect]
plan_gates: []
created: 2026-05-22
updated: 2026-06-10
source_count: 2
---
# NestPay

## Purpose

**NestPay** is the Asseco-built card-processing platform deployed by most major Turkish banks (Akbank, Garanti BBVA, İşbank, Finansbank/QNB, Halkbank, Ziraat, and others). CloudCart integrates the NestPay 3D-Pay-Hosting flow, so a merchant whose acquiring is on one of these banks can accept Visa / Mastercard charges. At checkout the customer is redirected to the bank's NestPay-hosted page, completes 3D Secure (mandatory on Turkish card transactions), and is bounced back to the store.

Each Turkish bank runs its own NestPay instance with bank-specific endpoint URLs, so the merchant must pick **which bank** their NestPay account is with — that choice points the integration at the right host. NestPay is the strongest fit for merchants selling to Turkish customers in Turkish Lira, though other currencies work if the bank contract allows.

## Where to find it

Sidebar → **Payment Providers** → click **NestPay**. The route is `/admin/payment-providers/nestpay` (route name `apps.nestpay.settings`); the internal provider key is `nestpay`.

## What the merchant can do here

- **Install / Uninstall** the NestPay method.
- **Toggle Active** on / off in the header.
- **Switch Test / Live mode** — points at the bank's sandbox or production host.
- **Pick the acquiring bank** — drives which NestPay endpoint is called.
- **Enter bank-issued credentials** — Client ID, Username, Password, Store Key.
- **Pick the settlement currency** (TRY is standard).
- **Override the customer-facing label** — logo, title, description.
- **Set an amount range** (min / max) and an optional **discount** for the method.
- **Refund a completed NestPay payment** from the order page (see [[orders-payment-refund]]).

## Settings & fields

All six `configuration` fields are required; the panel shows them inline (no expand-to-edit). The border colour follows the selected mode. Default config: `{ mode: 'test', discount_type: 'flat' }`.

| Field (`configuration.*`) | What it does | Validation |
|---|---|---|
| **mode** | Test environment vs production. | `test` / `live`. Default `test`. |
| **client_id** | NestPay merchant ID issued by the bank. | Required. Error: "Client id is required" |
| **username** | API username issued by the bank. | Required. Error: "NestPay username is required" |
| **password** | API password (masked). | Required. Error: "NestPay password is required" |
| **storekey** | HMAC secret signing every request, verifying every response. | Required. Error: "Storekey is required" |
| **bank** | Searchable select of the bank deployment to call (drives the endpoint). | Required. Error: "Bank is required" |
| **currency** | Settlement currency. | Required. Error: "Currency is required" |
| **Logo / Title / Description** | Storefront-label override. | — |
| **Min / Max amount** | Range filter for the method. | — |
| **Discount** | Discount applied when the customer picks NestPay. | — |

**Bank options** (11, hardcoded): `bktbank` (BKT Banka, Albania), `intesabank` (Banca Intesa, Serbia), `isbank` (İş Bankası), `akbank` (Akbank), `finansbank` (Finansbank), `denizbank` (Denizbank), `kuveytturk` (Kuveytturk), `halkbank` (Halkbank), `anadolubank` (Anadolubank), `hsbc` (ING Bank / Citibank / Cardplus), `ziraatbank` (Ziraat Bankası). All Turkish except the first two Balkans options. The merchant picks the bank named on their NestPay contract.

**Currency options** (4, hardcoded): `ALL`, `RSD`, `TRY`, `EUR`.

A known validation quirk: only `configuration.client_id.required` shows its custom message ("Client id is required"); the other five custom messages are bound to the wrong rule keys, so the merchant sees the default `required` message with the localized field label instead.

## Business rules

### Bank dropdown drives the endpoint

The **bank** setting is the routing key, not just a label — it selects the actual NestPay API host. Credentials are scoped to one bank, so picking the wrong bank makes every request fail with an authentication error. The merchant must match the bank on their contract.

### Currency auto-conversion

NestPay only accepts the configured settlement currency. If the order is in another currency, the platform converts the payment amount and currency **before** the redirect and persists both. Most Turkish-market merchants use TRY, so an EUR cart is converted to TRY at the platform exchange rate before the NestPay page appears.

### Customer flow — hosted redirect with 3D-Pay-Hosting

NestPay is a hosted-redirect gateway using the `3d_pay_hosting` method, which handles card entry and 3D Secure on the bank page (no embedded iframe):

1. The platform builds a signed POST form (transaction ID, amount, currency, return URL, cancel URL, language `en`).
2. The form auto-submits to the bank's NestPay endpoint.
3. The customer enters card details; the 3DS challenge runs (typically a one-time SMS code).
4. NestPay POSTs back to `payments.return/nestpay`.

The return is matched by the `oid` query parameter (set to the internal payment ID on initiation). If `oid` is missing or unknown, the platform returns "Bad Request".

### 3D Secure enforcement

Turkish card rules mandate 3DS on every e-commerce transaction. The `3d_pay_hosting` mode enforces it on the bank page — the customer cannot bypass the challenge, and CloudCart does not flag 3DS itself.

### Status mapping

| NestPay result | Status |
|---|---|
| Successful | **Completed** |
| Any non-success — declined, 3DS-failed, customer abort, technical error | **Failed** |
| Any exception during return processing | **Failed** (raw data preserved) |

3DS failure lands in **Failed**, not Cancelled.

### Sale vs Pre-Auth

Not exposed in the UI. The integration is hard-coded to immediate sale (`3d_pay_hosting`). NestPay supports pre-auth as a transaction type, but CloudCart surfaces no toggle. Merchants needing pre-auth + delayed capture should use [[payment-providers-borica-way4|Borica Way4]] or another gateway with a capture flow.

### Refunds

**Refund payment** on a completed NestPay order (see [[orders-payment-refund]]) calls NestPay's refund endpoint with the same transaction ID (the internal payment ID) for the full amount. On success the status flips to **Refunded** and a fresh `provider_reference_id` from the refund response replaces the original.

### What the persisted log strips

Before storing the response in `provider_data`, the platform trims NestPay-internal fields — `refreshtime`, `lang`, `maskedCreditCard`, `querypointhash`, `redirectUrl`, `okUrl`, `md`, `failUrl`, `encoding`, `HASHPARAMS`, `HASHPARAMSVAL`, `countdown`, `pid` — keeping only audit-relevant fields (transaction reference, amount, status, response code).

### Plan-tier gating

None — NestPay has no `plan_gates` declaration.

## Related

- [[payment-providers]] — parent hub.
- [[settings-payment-providers]] — global list where NestPay is installed / uninstalled.
- [[orders-payment-refund]] — refund initiation for NestPay payments.
- [[payment-provider]] — entity definition.
- [[payment-status]] — Completed / Failed / Refunded mapping.
- [[checkout-flow]] — storefront checkout concept page.
- [[multi-currency]] — context for the currency auto-conversion behaviour.

## Open questions

(none)
