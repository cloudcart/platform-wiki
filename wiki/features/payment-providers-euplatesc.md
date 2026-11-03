---
type: feature
nav_path: "Payment Providers → EuPlatesc"
route_name: apps.euplatesc.settings
route_path: /admin/payment-providers/euplatesc
aliases: ["EuPlatesc", "Euplatesc", "Romanian card gateway", "Romanian card payments", "EuPlatesc RON"]
tags: [paymentproviders, payment-providers, euplatesc, romania, card, ron, redirect]
plan_gates: []
created: 2026-05-22
updated: 2026-05-27
source_count: 2
---
# EuPlatesc

## Purpose

**EuPlatesc** is a Romanian card-acquiring gateway built into CloudCart for merchants who sell to Romanian customers and need to accept Visa / Mastercard charges in **Romanian Leu (RON)**. The customer is redirected from the CloudCart checkout to the EuPlatesc-hosted payment page, enters card details there (so the merchant never touches PAN data), and is bounced back to the store. Authorisation happens through the standard EuPlatesc integration; refunds and a transaction-status sync are also supported from the order page.

The merchant signs a contract directly with EuPlatesc, receives a **Merchant ID (MID)** and a **KEY** (HMAC secret), and pastes those two values into the settings here. Once the credentials are filled in and the provider row is marked Active, the EuPlatesc method appears on the storefront checkout for orders priced in RON (orders in other currencies are auto-converted to RON at the platform exchange rate before the redirect).

## Where to find it

Sidebar → **Payment Providers** → click **EuPlatesc**.

The route is `/admin/payment-providers/euplatesc`. The internal provider key is `euplatesc`. The settings panel uses the shared payment-provider settings shell (same as every other gateway).

## What the merchant can do here

- **Install / Uninstall** the EuPlatesc payment method through the standard payment-provider overview controls.
- **Toggle Active** on / off in the header — controls whether EuPlatesc appears on the storefront checkout.
- **Enter EuPlatesc credentials** (Merchant ID + KEY) — both required for any transaction to be attempted.
- **Override the customer-facing label** — logo, title, description shown to the buyer at checkout.
- **Set an amount range** (min / max) for when the method should be offered.
- **Configure a discount** (flat, percent, or shipping waive) when the customer pays with EuPlatesc.
- **Refund a completed EuPlatesc payment** from the order page (see [[orders-payment-refund]]) — the system calls back into EuPlatesc.
- **Sync a payment's status** if the storefront return was missed (e.g., browser closed) — the platform queries EuPlatesc for the latest transaction state and reconciles.

## Settings & fields

| Field / Control | What it does | Default | Validation / notes |
|-----------------|--------------|---------|--------------------|
| **Merchant ID** (`configuration.mid`) | EuPlatesc-assigned merchant identifier — paired with the KEY when signing every request. | Empty | Required. Error: "Merchant ID is required." |
| **KEY** (`configuration.key`) | HMAC secret EuPlatesc gives you alongside the MID — never shared with customers, used to sign and verify every exchange. | Empty | Required. Error: "KEY is required." |
| **Logo / Title / Description** | Standard label override for the storefront checkout. | Provider defaults | Standard payment-provider settings fields. |
| **Min / Max amount** | Restrict the method to orders inside this RON range. | Empty (any amount) | Standard payment-provider behaviour. |
| **Discount** | Discount applied when customer picks EuPlatesc. | None | Standard. |

## Business rules

### Forced currency: RON

EuPlatesc only acquires in **Romanian Leu (RON)**. The integration hard-codes the request currency to RON. When a customer reaches checkout in a non-RON currency (e.g., EUR or USD), the platform converts the payment amount to RON at the configured exchange rate **before** the redirect to EuPlatesc — both the payment's amount and currency are updated and persisted, then the redirect form is built in RON. The customer sees the RON amount on the EuPlatesc payment page.

### Customer flow — full redirect

EuPlatesc is a **hosted redirect** gateway: the platform builds a signed POST form and renders it back to the browser, which auto-submits to EuPlatesc. The customer enters card details on EuPlatesc's page, completes 3DS challenge if required, and is returned to CloudCart at `payments.return/euplatesc`. The platform reads the EuPlatesc response on return, marks the payment as Completed or Failed, and forwards the customer to the storefront's order-confirmation page.

The return-from-EuPlatesc identifies the payment by the `invoice_id` query parameter (which the platform sets to the internal Payment ID when initiating the redirect). If `invoice_id` is missing or unknown, the platform returns "Bad Request" without touching the order.

### What the customer enters at EuPlatesc

The platform forwards to EuPlatesc:
- The internal Payment ID as the `orderId`.
- The order number (or hash, depending on the store's *Order ID display* setting) as the `orderName`.
- The amount in RON minor units.
- The customer's first name, last name, email (from the order).
- Three URLs back to CloudCart: `successurl`, `failedurl`, and `backtosite` — all route to the same `payments.return/euplatesc` endpoint.

### Refunds

Calling **Refund payment** on a completed EuPlatesc order (see [[orders-payment-refund]]) issues a refund request to EuPlatesc. EuPlatesc's response is logged and on success the platform's payment status flips to **Refunded** (see [[payment-status]]).

### Status sync

If the customer's browser closes mid-redirect or the return webhook is missed, the platform can re-query EuPlatesc for the transaction state. The response replaces the stored provider data and updates the payment status to Completed or Failed accordingly. This is usually triggered automatically by a scheduled status reconciliation; it can also run on demand from the order page.

### No test/live toggle

EuPlatesc has **no test/live mode switch** anywhere in the settings UI — the form only collects Merchant ID and KEY (plus the standard logo / amount-range / discount rows), so there is no Test/Live pill in the header and no mode card. The merchant submits whatever credentials EuPlatesc gave them and the integration uses production endpoints. To test, EuPlatesc issues sandbox credentials that point to their test environment; the credentials themselves drive the environment, and the platform doesn't override the URL.

### Card brand support + 3DS

Visa and Mastercard are the standard EuPlatesc-acquired brands. No card-brand toggles are exposed in the CloudCart UI — whichever brands EuPlatesc supports on the merchant's contract are accepted automatically. 3DS handling (3D Secure 2.0 challenge / frictionless) is owned by EuPlatesc; the platform doesn't pass 3DS flags directly. A **declined 3DS challenge or a customer-aborted card form both map to Failed** — there is no separate Canceled state, so from the merchant's view both look identical.

### Plan-tier gating

None — EuPlatesc has no `plan_gates` declaration. Any plan that can install payment providers can install EuPlatesc.

### Return-payload mapping

On return from EuPlatesc, the platform reads the POST-back: success → payment **Completed** with the transaction reference stored; failure → **Failed**. The full response payload is logged to the order's payment log (visible to CloudCart support, not to the merchant), with the `ExtraData` and `query_trace` keys stripped to keep the log compact.

## Related

- [[payment-providers]] — parent hub.
- [[settings-payment-providers]] — global list where EuPlatesc is installed / uninstalled.
- [[orders-payment-refund]] — refund initiation for EuPlatesc payments.
- [[orders-payment-capture]] — manual-capture surface (EuPlatesc uses immediate purchase, so no separate capture step).
- [[payment-providers-mobilpay]] — the other Romanian gateway integrated in CloudCart (legacy NETOPIA stack).
- [[payment-provider]] — entity definition.
- [[payment-status]] — Completed / Refunded / Failed mapping.
- [[checkout-flow]] — concept page on the storefront checkout.
- [[multi-currency]] — context for the RON auto-conversion behaviour.

## Open questions

(none)
